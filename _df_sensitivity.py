"""durable_factor sensitivity (SAGE M2).  2026-09-20.

WHY THIS EXISTS
---------------
`durable_factor` was, until today, a DEAD parameter: declared, documented with
three literature citations, named in the paper's assumption list (A3) -- and
never read by `simulate()`. Every previously reported number was therefore
produced by a model that did not contain the mechanism the paper claimed.

It is now wired in. But being wired in is not the same as being understood: the
file has never had a sensitivity analysis, because before the fix there was
nothing to analyse. This script supplies the missing evidence.

WHAT IS SWEPT
-------------
`durable_factor` encodes assumption A3: more explicit help produces less
productive struggle, so a level-L scaffold's gain for DURABLE far-transfer is
attenuated relative to its immediate effect. The default (1.00, 0.72, 0.46) was
chosen to make levels 2 and 3 progressively less durable, with no empirical
source for the two numbers.

We parameterise the attenuation CONTRAST rather than the raw tuple, because that
is the quantity the claim is about:

    dur(c) = (1.00, 1.00 - 0.28*c, 1.00 - 0.54*c),  c >= 0

    c = 0.0  ->  (1.00, 1.00, 1.00)   no level-dependent durability at all
    c = 1.0  ->  (1.00, 0.72, 0.46)   the default
    c = 1.5  ->  (1.00, 0.58, 0.19)   stronger attenuation

c = 0 is the mutation-test case (it must destroy or at least change the
conclusion if durability is load-bearing); c = 1.0 is the baseline.

REPORTED
--------
lambda*, earned gain at lambda*, both branch effects, the P6 attribution share,
the verdict, and the whole curve -- so the effect of durability on the SHAPE can
be inspected rather than summarised away.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import statistics
import sys
from dataclasses import asdict
from typing import Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from m2_lambda_sweep import (  # noqa: E402
    DEFAULT_GRID,
    LearnerModel,
    build_408_graph,
    proposition1_verdict,
    run_sweep,
    train_theta,
)

C_GRID = [0.0, 0.5, 1.0, 1.25, 1.5, 2.0]


def dur_tuple(c: float) -> Tuple[float, float, float]:
    """Attenuation contrast -> the durable_factor tuple."""
    return (1.00,
            max(0.0, min(1.0, 1.00 - 0.28 * c)),
            max(0.0, min(1.0, 1.00 - 0.54 * c)))


def run_one(lm_base: LearnerModel, graph, lams, seeds: int, n_problems: int,
            c: float) -> Dict:
    lm = LearnerModel(**{**asdict(lm_base), "durable_factor": dur_tuple(c)})
    theta = train_theta(lm, graph, min(seeds, 6), n_problems)
    rows = run_sweep(lm, graph, lams, seeds, n_problems, theta)

    ctrl = LearnerModel(**{**asdict(lm), "scaffold_gain": (0.0, 0.0, 0.0)})
    cth = train_theta(ctrl, graph, min(seeds, 6), n_problems)
    crows = run_sweep(ctrl, graph, lams, seeds, n_problems, cth)

    ok, notes = proposition1_verdict(rows, control_rows=crows)
    gains = [r["gain"][0] for r in rows]
    gi = max(range(len(gains)), key=lambda i: gains[i])
    share = float("nan")
    for n in notes:
        if n.startswith("P6"):
            share = float(n.split("share=")[1].split("%")[0]) / 100.0
    return {
        "contrast": c,
        "durable_factor": dur_tuple(c),
        "theta": theta,
        "supported": bool(ok),
        "share": share,
        "lambda_star": rows[gi]["lambda"],
        "gain_star": gains[gi],
        "left_effect": gains[gi] - gains[0],
        "right_effect": gains[gi] - gains[-1],
        "gain_0": gains[0],
        "gain_max": gains[-1],
        "curve": gains,
        "lambdas": [r["lambda"] for r in rows],
        "notes": notes,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="SAGE M2 durable_factor sensitivity")
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--learners", type=int, default=240)
    ap.add_argument("--problems", type=int, default=20)
    ap.add_argument("--outdir", type=str, default="data")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    if args.quick:
        args.seeds, args.learners, args.problems = 10, 120, 12

    lm = LearnerModel(n_learners=args.learners)
    graph = build_408_graph()

    print("=" * 104)
    print("[DURABLE-FACTOR] sensitivity of the A3 mechanism (level-dependent "
          "durability)")
    print(f"[DURABLE-FACTOR] seeds={args.seeds} learners={args.learners} "
          f"problems={args.problems}")
    print("=" * 104)
    print(f"{'contrast':>9} | {'durable_factor':>20} | {'theta':>6} | "
          f"{'lam*':>6} | {'gain*':>7} | {'left':>8} | {'right':>8} | "
          f"{'attr':>5} | verdict")
    print("-" * 104)

    results: List[Dict] = []
    for c in C_GRID:
        r = run_one(lm, graph, DEFAULT_GRID, args.seeds, args.problems, c)
        results.append(r)
        tag = "  <- NO attenuation (mutation case)" if c == 0.0 else (
            "  <- default" if c == 1.0 else "")
        df = r["durable_factor"]
        print(f"{c:>9.2f} | ({df[0]:.2f},{df[1]:.2f},{df[2]:.2f}){'':>5} | "
              f"{r['theta']:>6.3f} | {r['lambda_star']:>6.2f} | "
              f"{r['gain_star']:>7.4f} | {r['left_effect']:>+8.4f} | "
              f"{r['right_effect']:>+8.4f} | {r['share']:>4.0%} | "
              f"{'SUPPORTED' if r['supported'] else 'REJECTED'}{tag}")

    base = next(r for r in results if r["contrast"] == 1.0)
    noatt = next(r for r in results if r["contrast"] == 0.0)

    print()
    print("=" * 104)
    print("SUMMARY")
    print("=" * 104)
    print(f"  durable_factor is LIVENESS-verified if c=0 differs from c=1:")
    print(f"    gain*  {base['gain_star']:.4f} -> {noatt['gain_star']:.4f} "
          f"(delta {noatt['gain_star'] - base['gain_star']:+.4f})")
    print(f"    lam*   {base['lambda_star']:.2f} -> {noatt['lambda_star']:.2f}")
    moved = abs(base["gain_star"] - noatt["gain_star"]) > 1e-9
    print(f"    => parameter is {'LIVE (good)' if moved else 'DEAD (BUG!)'}")
    stars = [r["lambda_star"] for r in results]
    shares = [r["share"] for r in results]
    sup = sum(1 for r in results if r["supported"])
    print(f"  lambda* across contrast {C_GRID}: "
          f"{[round(s, 2) for s in stars]}  spread={max(stars)-min(stars):.2f}")
    print(f"  attribution share range: {min(shares):.0%} - {max(shares):.0%}")
    print(f"  SUPPORTED for {sup}/{len(results)} values of the contrast")
    print()
    print("  Reading: A3 ('more explicit help is less durable') is load-bearing")
    print("  iff removing the attenuation (contrast 0) changes the numbers. The")
    print("  KEY question for the paper is whether lambda* MOVES with the")
    print("  contrast, because a boundary that shifts whenever an unmeasured")
    print("  constant is perturbed must be reported as an interval, not a point.")

    path = os.path.join(args.outdir, "m2_durable_factor_sensitivity.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "seeds": args.seeds, "learners": args.learners,
            "problems": args.problems, "contrast_grid": C_GRID,
            "results": [{k: v for k, v in r.items()
                         if k not in ("notes", "curve", "lambdas")}
                        for r in results],
            "notes": [r["notes"] for r in results],
        }, f, ensure_ascii=False, indent=2)

    csv_path = os.path.join(args.outdir, "m2_durable_factor_sensitivity.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["contrast", "lambda", "earned_gain"])
        for r in results:
            for lam, g in zip(r["lambdas"], r["curve"]):
                w.writerow([r["contrast"], lam, f"{g:.6f}"])

    print()
    print(f"[DURABLE-FACTOR] json -> {path}")
    print(f"[DURABLE-FACTOR] csv  -> {csv_path}")


if __name__ == "__main__":
    main()
