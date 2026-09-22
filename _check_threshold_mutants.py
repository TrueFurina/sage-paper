"""Fast, focused mutation check for the A9 THRESHOLD mechanism (2026-09-20).

WHY THIS EXISTS
---------------
`m2_lambda_sweep.py --selftest` runs all 11 mutants plus 4 liveness checks at
full learner counts, which takes on the order of an hour. That is the right
regression gate before submission, but it is too slow to iterate against while
developing a new mechanism.

This script checks ONLY the mutants that the threshold form introduced -- M8 and
M9 -- at reduced cost, so the question "is `collapse_threshold` actually load-
bearing, or is it decoration?" gets an answer in minutes rather than an hour.

A new mechanism without its own mutation check is exactly how `durable_factor`
stayed dead for months while being fully documented. The lesson generalises: the
day you add a mechanism, add the check that would notice if it stopped working.

USAGE
-----
    python _check_threshold_mutants.py                 # ~2-4 min
    python _check_threshold_mutants.py --seeds 8 --problems 10 --learners 120

Exits non-zero if any mutant fails to behave as predicted.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from m2_lambda_sweep import (  # noqa: E402
    DEFAULT_GRID,
    LearnerModel,
    build_408_graph,
    proposition1_verdict,
    run_sweep,
    train_theta,
)


def evaluate(lm: LearnerModel, graph, lams, seeds: int, n_problems: int):
    th = train_theta(lm, graph, min(seeds, 4), n_problems)
    rows = run_sweep(lm, graph, lams, seeds, n_problems, th)
    ctrl = LearnerModel(**{**asdict(lm), "scaffold_gain": (0.0, 0.0, 0.0)})
    cth = train_theta(ctrl, graph, min(seeds, 4), n_problems)
    crows = run_sweep(ctrl, graph, lams, seeds, n_problems, cth)
    gains = [r["gain"][0] for r in rows]
    gi = max(range(len(gains)), key=lambda i: gains[i])
    ok, notes = proposition1_verdict(rows, control_rows=crows)
    return ok, rows, gains, gi, notes


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--problems", type=int, default=12)
    ap.add_argument("--learners", type=int, default=120)
    args = ap.parse_args()

    lm = LearnerModel(n_learners=args.learners)
    graph = build_408_graph()
    lams = DEFAULT_GRID

    print("=" * 92)
    print("[THRESHOLD-MUTANT CHECK] is `collapse_threshold` load-bearing?")
    print(f"[THRESHOLD-MUTANT CHECK] seeds={args.seeds} learners={args.learners} "
          f"problems={args.problems}")
    print("=" * 92)

    base_ok, base_rows, base_gains, base_gi, _ = evaluate(
        lm, graph, lams, args.seeds, args.problems)
    print(f"  BASELINE      theta-fit done | peak={max(base_gains):.4f}"
          f"@{base_rows[base_gi]['lambda']} | "
          f"{'SUPPORTED' if base_ok else 'REJECTED'}")
    if not base_ok:
        print("  !! baseline does not support the proposition; the mutants below "
              "cannot be interpreted. Investigate before continuing.")
        raise SystemExit(1)

    # (mutant, tag, expected verdict)
    cases = [
        # M8: boundary pushed beyond the swept range -> nothing collapses ->
        # no falling side -> must REJECT.
        (LearnerModel(**{**asdict(lm), "collapse_threshold": 5.0}),
         "M8 threshold beyond grid (no collapse)", False),
        # M9: boundary at the far left -> tutor crippled across nearly the whole
        # grid -> no rising side either -> must REJECT.
        (LearnerModel(**{**asdict(lm), "collapse_threshold": 0.02}),
         "M9 threshold at far left (crippled throughout)", False),
        # M5 restated under the threshold form: zero collapse depth means output
        # never degrades -> must REJECT.
        (LearnerModel(**{**asdict(lm), "delivery_damping": 0.0}),
         "M5 collapse depth zero (no delivery loss)", False),
        # SANITY (not a mutant): a shifted but still reachable boundary must
        # still SUPPORT the proposition. If this rejects, the mechanism is
        # brittle rather than merely sensitive.
        (LearnerModel(**{**asdict(lm), "collapse_threshold": 0.55}),
         "SANITY threshold 0.55 (still reachable)", True),
        # M3 RECALIBRATED (2026-09-20). Under the old continuous-linear delivery
        # form, leak_durable=0.25 drove the scaffolding-attributable share to
        # 40% (<50%) and the diagnostic rejected. Under the threshold form the
        # scaffolding route is no longer progressively degraded, so its share is
        # larger and the flip point moved to ~0.45 (measured, see section 5.4 of
        # the audit record). The mutant must sit BEYOND the measured flip point.
        (LearnerModel(**{**asdict(lm), "leak_durable": 0.50}),
         "M3 leaks DO teach, beyond flip (0.50)", False),
        # This is the counterpart: just BELOW the flip point the diagnostic must
        # still SUPPORT. Asserting both sides is what makes the 50% bar a
        # measured boundary rather than a number that happens to pass.
        (LearnerModel(**{**asdict(lm), "leak_durable": 0.35}),
         "M3 below flip: leaks teach moderately (0.35)", True),
    ]

    results = []
    print()
    for mutant, tag, expected in cases:
        ok, rows, gains, gi, notes = evaluate(
            mutant, graph, lams, args.seeds, args.problems)
        agree = ok == expected
        results.append((tag, agree))
        p6 = [n for n in notes if n.startswith("P6")]
        share = p6[0].split("share=")[1].split(" ")[0] if p6 else "n/a"
        print(f"{'ok  ' if agree else 'FAIL'} {tag:<46} "
              f"peak={max(gains):.4f}@{rows[gi]['lambda']:<5} attr={share:<5} "
              f"{'SUPPORTED' if ok else 'REJECTED'}  "
              f"expect={'SUPPORTED' if expected else 'REJECTED'}")

    # Numeric liveness: mutating the threshold must move the NUMBERS, not only
    # the verdict. A no-op mutation would prove the parameter is dead.
    print()
    live = LearnerModel(**{**asdict(lm), "collapse_threshold": 0.60})
    _, _, live_gains, _, _ = evaluate(live, graph, lams, args.seeds, args.problems)
    moved = any(abs(a - b) > 1e-9 for a, b in zip(live_gains, base_gains))
    results.append(("collapse_threshold liveness", moved))
    print(f"{'ok  ' if moved else 'FAIL'} LIVENESS collapse_threshold: mutating "
          f"it {'CHANGES' if moved else 'does NOT change'} the reported gain "
          f"(must change; a no-op mutation proves the parameter is dead)")

    n_pass = sum(1 for _, ok in results if ok)
    print()
    print(f"[THRESHOLD-MUTANT CHECK] {n_pass}/{len(results)} passed")
    if n_pass < len(results):
        for tag, ok in results:
            if not ok:
                print(f"  FAILED: {tag}")
        raise SystemExit(1)
    print("[THRESHOLD-MUTANT CHECK] the threshold mechanism is load-bearing: "
          "removing it, or moving the boundary out of range in either "
          "direction, changes the conclusion, and mutating it changes the "
          "numbers.")


if __name__ == "__main__":
    main()
