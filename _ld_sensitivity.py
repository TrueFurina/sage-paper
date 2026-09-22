"""leak_durable single-variable sensitivity scan (P0-1 fix).

WHY THIS EXISTS
---------------
The paper's first claim is that 86% of the rising-side improvement is
attributable to scaffolding rather than to leak suppression. That share is
produced by the attribution control, and its magnitude depends on
`leak_durable` -- the stipulated parameter that says how much durable mastery
a leaked answer confers.

`08` section 5.4 recorded a scan of this parameter, but at a configuration
that does not match the reported main result (its baseline reads 84% while the
40-seed main result reads 86%), so the two numbers cannot be placed side by
side in the paper. This script re-runs the scan at EXACTLY the main-result
configuration so that §6.1 and §6.3 speak with one voice.

It varies ONE thing: leak_durable. theta is refitted per value (as in main()),
and the control arm is the identical model with scaffolding disabled
(scaffold_gain = 0) and the SAME leak_durable, so the leak channel is held
constant between observed and control.

Run:
    python _ld_sensitivity.py --seeds 40 --problems 25 --learners 240
Output:
    data/leak_durable_sensitivity.json   (machine readable)
    _ld_sensitivity.out                  (human readable, because stdout is
                                          not always captured on this machine)
"""

import argparse
import json
import os
import time
from dataclasses import asdict

from m2_lambda_sweep import (LearnerModel, build_408_graph, run_sweep,
                             train_theta, proposition1_verdict, DEFAULT_GRID)

# Baseline is 0.012. Values are chosen to (a) bracket the previously recorded
# flip point ~0.45 densely and (b) extend past it, so the 50% bar is asserted
# on BOTH sides -- a bar measured on one side only is decoration.
LD_VALUES = [0.012, 0.05, 0.10, 0.20, 0.30, 0.40, 0.45, 0.50, 0.60, 0.70]


def scan_one(ld, seeds, problems, learners, graph):
    lm = LearnerModel(n_learners=learners, leak_durable=ld)
    theta = train_theta(lm, graph, min(seeds, 6), problems)
    rows = run_sweep(lm, graph, DEFAULT_GRID, seeds, problems, theta)

    clm = LearnerModel(**{**asdict(lm), "scaffold_gain": (0.0, 0.0, 0.0)})
    ctheta = train_theta(clm, graph, min(seeds, 6), problems)
    crows = run_sweep(clm, graph, DEFAULT_GRID, seeds, problems, ctheta)

    ok, notes = proposition1_verdict(rows, control_rows=crows)

    gains = [r["gain"][0] for r in rows]
    gi = max(range(len(gains)), key=lambda i: gains[i])
    left = gains[gi] - gains[0]
    right = gains[gi] - gains[-1]

    cg = [r["gain"][0] for r in crows]
    cgi = max(range(len(cg)), key=lambda i: cg[i])
    cleft = cg[cgi] - cg[0]

    share = (left - max(0.0, cleft)) / left if left > 1e-9 else 0.0
    return {
        "leak_durable": ld,
        "theta": round(theta, 4),
        "lambda_star": rows[gi]["lambda"],
        "gain_star": round(gains[gi], 4),
        "left_effect": round(left, 4),
        "right_effect": round(right, 4),
        "control_left_effect": round(cleft, 4),
        "attributable_share": round(share, 4),
        "verdict": "SUPPORTED" if ok else "REJECTED",
        "notes": notes,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=40)
    ap.add_argument("--learners", type=int, default=240)
    ap.add_argument("--problems", type=int, default=25)
    ap.add_argument("--values", type=str, default=None)
    ap.add_argument("--tag", type=str, default="",
                    help="suffix for output files, so parallel runs of "
                         "different leak_durable values do not clobber "
                         "each other")
    args = ap.parse_args()

    values = ([float(x) for x in args.values.split(",")] if args.values
              else LD_VALUES)
    graph = build_408_graph()
    t0 = time.time()
    results = []
    lines = []
    lines.append(f"leak_durable sensitivity | seeds={args.seeds} "
                 f"learners={args.learners} problems={args.problems}")
    lines.append("")
    lines.append(f"{'ld':>6} | {'theta':>7} | {'lam*':>5} | {'gain*':>7} | "
                 f"{'left':>8} | {'right':>8} | {'ctrl_left':>9} | "
                 f"{'share':>6} | verdict")
    lines.append("-" * 96)

    for ld in values:
        ts = time.time()
        r = scan_one(ld, args.seeds, args.problems, args.learners, graph)
        results.append(r)
        lines.append(f"{ld:>6.3f} | {r['theta']:>7.4f} | "
                     f"{r['lambda_star']:>5.2f} | {r['gain_star']:>7.4f} | "
                     f"{r['left_effect']:>+8.4f} | {r['right_effect']:>+8.4f} | "
                     f"{r['control_left_effect']:>+9.4f} | "
                     f"{r['attributable_share']:>5.0%} | {r['verdict']}")
        print(f"  ld={ld:<6} share={r['attributable_share']:.0%} "
              f"{r['verdict']} ({time.time() - ts:.1f}s)", flush=True)

    lines.append("")
    base = results[0]
    lines.append(f"BASELINE (ld={base['leak_durable']}): share = "
                 f"{base['attributable_share']:.0%}, lambda* = "
                 f"{base['lambda_star']}, gain* = {base['gain_star']}")
    shares = [(r["leak_durable"], r["attributable_share"]) for r in results]
    below = [p for p in shares if p[1] < 0.5]
    if below:
        lines.append(f"Share first drops below the 50% bar at "
                     f"leak_durable = {below[0][0]}")
    lines.append(f"elapsed {time.time() - t0:.1f}s")

    os.makedirs("data", exist_ok=True)
    tag = ("_" + args.tag) if args.tag else ""
    with open(f"data/leak_durable_sensitivity{tag}.json", "w",
              encoding="utf-8") as f:
        json.dump({"config": vars(args), "results": results}, f,
                  ensure_ascii=False, indent=2)
    with open(f"_ld_sensitivity{tag}.out", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
