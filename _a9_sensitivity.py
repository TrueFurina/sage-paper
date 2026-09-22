"""A9 sensitivity analysis (SAGE M2).  v2 — 2026-09-20, threshold form.

QUESTION
--------
A9 governs how much of a scaffold the tutor actually delivers once its output is
constrained.  Under the threshold form the M2 model has THREE A9 constants:

    delivery_damping     D  -- collapse DEPTH (how much helpfulness is lost)
    collapse_threshold   lc -- WHERE collapse sets in
    collapse_sharpness   s  -- how abrupt the transition is

None of them is empirically measured.  The literature supplies the FORM (a step
with a floor: arXiv 2604.13006 "collapse floor ... a discrete strategy switch
rather than continuous degradation") but not the magnitude of any of them.

If the reported lambda* moves materially as these constants change, then "there
is a withholding boundary at lambda*" is not a property of SAGE's mechanism; it
is a property of unverified constants.  That distinction decides whether
contribution (2) survives.

DESIGN
------
Sweep each A9 constant in turn, holding the other two at their defaults, and for
each value report lambda*, earned gain at lambda*, both branch effects, the P6
attribution share, and whether the boundary proposition is SUPPORTED.  The whole
gain(lambda) curve is dumped so the shape can be inspected rather than trusted.

ERGODICITY / EQUIVARIANCE CHECK
-------------------------------
A naive reading of "lambda* moved" can be a pure artefact of where the grid
happens to sit relative to the constant being swept.  Each constant has an
invariance that holds the learner's EXPERIENCE fixed:

  * depth D      : rescale the grid so D*lambda is constant (same fraction of
                   the scaffold's potential actually delivered).
  * threshold lc : SHIFT the grid so (lambda - lc) is constant (same DISTANCE
                   to the collapse boundary).
  * sharpness s  : rescale around the boundary so the transition keeps its
                   width in units of s.

If lambda* is stable in the invariant coordinate, the movement was a grid
artefact; if it survives, the dependence is real.

!! COMPARISON DISCIPLINE (2026-09-20, learned the hard way) !!
The spread must be computed over the SAME set of swept values on both sides.
The previous version compared a rescaled set that EXCLUDED D=0 against a raw set
that INCLUDED it, and D=0 sits far to the right BY CONSTRUCTION (no collapse ->
no right branch -> the argmax floats to the grid end).  That inflated the raw
spread from 0.20 to 0.45 and made the script announce the opposite conclusion.
Structurally degenerate settings (collapse absent, or boundary unreachable) are
therefore excluded from the like-for-like spread and reported separately.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
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

# name -> (field, values to sweep, reference value)
SWEEPS: Dict[str, Tuple[str, List[float], float]] = {
    "damping": ("delivery_damping", [0.25, 0.50, 0.75, 1.00, 1.25], 0.75),
    "threshold": ("collapse_threshold", [0.20, 0.25, 0.30, 0.40, 0.50, 0.60], 0.40),
    "sharpness": ("collapse_sharpness", [0.02, 0.04, 0.08, 0.15], 0.04),
}
# Structurally degenerate: collapse switched off, or boundary pushed past the
# grid so nothing collapses within the swept range. Reported, never averaged in.
STRUCTURAL = {"damping": [0.0], "threshold": [5.0], "sharpness": []}


def curve(rows: List[Dict]) -> Dict:
    gains = [r["gain"][0] for r in rows]
    alrs = [r["alr"][0] for r in rows]
    gi = max(range(len(gains)), key=lambda i: gains[i])
    lo, hi = 0, len(gains) - 1
    return {
        "lambda_star": rows[gi]["lambda"],
        "gain_star": gains[gi],
        "left_effect": gains[gi] - gains[lo],
        "right_effect": gains[gi] - gains[hi],
        "gain_0": gains[lo],
        "gain_max": gains[hi],
        "alr_0": alrs[lo],
        "alr_max": alrs[hi],
        "interior": 0 < gi < hi,
        "curve": gains,
        "lambdas": [r["lambda"] for r in rows],
    }


def share_from_notes(notes: List[str]) -> float:
    for n in notes:
        if n.startswith("P6"):
            try:
                return float(n.split("share=")[1].split("%")[0]) / 100.0
            except Exception:
                return float("nan")
    return float("nan")


def bootstrap_optimum(rows: List[Dict], n_boot: int,
                      rng: random.Random) -> Tuple[float, float]:
    """Resample SEEDS with replacement, recompute argmax -> (mean, sd).

    The seed is the experimental unit; resampling it replicates the experiment.
    """
    per_seed = [[rec.learning_gain for rec in r["raw"]] for r in rows]
    n = len(per_seed[0])
    lams = [r["lambda"] for r in rows]
    stars: List[float] = []
    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        means = [statistics.fmean([col[i] for i in idx]) for col in per_seed]
        gi = max(range(len(means)), key=lambda i: means[i])
        stars.append(lams[gi])
    if len(stars) < 2:
        return (stars[0] if stars else float("nan")), 0.0
    return statistics.fmean(stars), statistics.stdev(stars)


def run_one(lm_base: LearnerModel, graph, lams, seeds: int, n_problems: int,
            field: str, value: float, n_boot: int, rng: random.Random) -> Dict:
    lm = LearnerModel(**{**asdict(lm_base), field: value})
    theta = train_theta(lm, graph, min(seeds, 6), n_problems)
    rows = run_sweep(lm, graph, lams, seeds, n_problems, theta)

    ctrl = LearnerModel(**{**asdict(lm), "scaffold_gain": (0.0, 0.0, 0.0)})
    cth = train_theta(ctrl, graph, min(seeds, 6), n_problems)
    crows = run_sweep(ctrl, graph, lams, seeds, n_problems, cth)

    ok, notes = proposition1_verdict(rows, control_rows=crows)
    star_mean, star_sd = bootstrap_optimum(rows, n_boot, rng)
    return {
        "value": value, "theta": theta, "supported": bool(ok),
        "share": share_from_notes(notes),
        "lambda_star_boot_mean": star_mean, "lambda_star_boot_sd": star_sd,
        **curve(rows), "notes": notes,
    }


def _collapse_frac(lam: float, lc: float, s: float) -> float:
    """A9's collision fraction: 0 = output intact, 1 = fully collapsed."""
    z = -(lam - lc) / max(1e-9, s)
    z = max(-60.0, min(60.0, z))
    return 1.0 / (1.0 + math.exp(z))


def _logit(p: float) -> float:
    p = min(1.0 - 1e-12, max(1e-12, p))
    return math.log(p / (1.0 - p))


def equivariant_lams(base_lams: List[float], field: str, value: float,
                     ref: float, lc: float, s: float) -> List[float]:
    """Grid transformed so the LEARNER receives the same thing.

    !! 2026-09-20 BUG FIX, caught by unit-testing this very function !!
    The first version rescaled the grid by ref/value for delivery DEPTH, holding
    D*lambda constant. That was correct for the OLD continuous-linear form
    (`damp = 1 - D*min(1,lam)`), where delivery really was proportional to
    D*lambda. Under the THRESHOLD form it is wrong twice over:
      * `damp = 1 - D*collapse_frac(lam)` and collapse_frac is a SIGMOID in
        (lam - lc), so D*lambda is not the delivered quantity;
      * the old grid clip at lambda <= 1.0 was there to respect `min(1, lam)`,
        which no longer exists -- clipping now silently breaks the invariance.
    The quantity to hold constant is the amount actually DELIVERED,
    `damp = 1 - D*collapse_frac(lam)`, so we SOLVE for the lambda that
    reproduces each reference delivery level:

        collapse_frac(lam') = ref * collapse_frac(lam) / value
        lam' = lc + s * logit(collapse_frac(lam'))

    !! SIGN CHECK (this is the part that is easy to get backwards) !!
    The model computes `cf = 1 / (1 + exp(-(lam - lc)/s))`, i.e. cf is SMALL for
    small lam and LARGE once lam passes lc. Inverting: with v = (lam-lc)/s,
    `1/cf - 1 = exp(-v)` so `v = logit(cf)` and therefore `lam = lc + s*logit(cf)`
    -- PLUS, not minus. An earlier version used minus and produced a mirror-image
    grid (delivery collapsed exactly where it should have been intact); it was
    caught by unit-testing the transform against the model's own formula.
    """
    if value == 0:
        return base_lams
    out: List[float]
    if field == "delivery_damping":
        out = []
        for x in base_lams:
            cf_new = ref * _collapse_frac(x, lc, s) / value
            if cf_new >= 1.0:
                # The new depth is too shallow to reproduce this delivery level:
                # even full collapse cannot reach it, so push lambda far out.
                out.append(round(lc + 6.0 * s, 6))
            else:
                out.append(round(lc + s * _logit(cf_new), 6))
    elif field == "collapse_threshold":
        out = [x + (value - ref) for x in base_lams]
    else:
        out = [lc + (x - lc) * (value / ref) for x in base_lams]
    return sorted({round(v, 6) for v in out if -0.5 <= v <= 2.0})


def invariant_star(r: Dict, field: str, value: float, ref: float,
                   lc: float, s: float) -> float:
    """Report lambda* in the coordinate where the learner's experience is fixed.

    * depth     -> the DELIVERED fraction at the optimum, `1 - D*cf(lambda*)`
                   (dimensionless; the largest invariant form available, since
                   lambda does not enter delivery linearly any more)
    * lc        -> lambda* - (value - ref), i.e. distance to the boundary
    * sharpness -> lambda* rescaled into reference-width units
    """
    lam = r["lambda_star"]
    if field == "delivery_damping":
        return 1.0 - value * _collapse_frac(lam, lc, s)
    if field == "collapse_threshold":
        return lam - (value - ref)
    return lc + (lam - lc) * (ref / value)


def main() -> None:
    ap = argparse.ArgumentParser(description="SAGE M2 A9 sensitivity (v2)")
    ap.add_argument("--which", default="all",
                    help="all | damping | threshold | sharpness")
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--learners", type=int, default=240)
    ap.add_argument("--problems", type=int, default=20)
    ap.add_argument("--boot", type=int, default=300)
    ap.add_argument("--outdir", type=str, default="data")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    if args.quick:
        args.seeds, args.learners, args.problems, args.boot = 10, 120, 12, 100

    which = list(SWEEPS) if args.which == "all" else [args.which]
    lm = LearnerModel(n_learners=args.learners)
    graph = build_408_graph()
    rng = random.Random(20260920)

    print("=" * 104)
    print("[A9] sensitivity of lambda* to the three unverified A9 constants")
    print(f"[A9] seeds={args.seeds} learners={args.learners} "
          f"problems={args.problems} bootstrap={args.boot}")
    print("=" * 104)

    all_results: Dict[str, List[Dict]] = {}
    all_erg: Dict[str, List[Dict]] = {}

    for name in which:
        field, values, ref = SWEEPS[name]
        print()
        print(f"### {name}  (field `{field}`, reference {ref})")
        print(f"{'value':>7} | {'theta':>6} | {'lam*':>6} | {'boot lam*':>15} | "
              f"{'gain*':>7} | {'left':>8} | {'right':>8} | {'attr':>5} | verdict")
        print("-" * 104)
        res: List[Dict] = []
        for val in values + STRUCTURAL.get(name, []):
            r = run_one(lm, graph, DEFAULT_GRID, args.seeds, args.problems,
                        field, val, args.boot, rng)
            r["structural"] = val in STRUCTURAL.get(name, [])
            res.append(r)
            tag = "  (structural: excluded from spread)" if r["structural"] else ""
            print(f"{val:>7.3f} | {r['theta']:>6.3f} | {r['lambda_star']:>6.2f} | "
                  f"{r['lambda_star_boot_mean']:>7.2f}+-{r['lambda_star_boot_sd']:<5.2f} | "
                  f"{r['gain_star']:>7.4f} | {r['left_effect']:>+8.4f} | "
                  f"{r['right_effect']:>+8.4f} | {r['share']:>4.0%} | "
                  f"{'SUPPORTED' if r['supported'] else 'REJECTED'}{tag}")
        all_results[name] = res

        # ---- equivariance ---------------------------------------------------
        how = ("grid solved so the DELIVERED fraction is constant"
               if field == "delivery_damping"
               else "shifted (lambda - lc constant)" if field == "collapse_threshold"
               else "scaled about the boundary (width in units of s)")
        inv_col = ("delivered fraction" if field == "delivery_damping"
                   else "lam* shifted" if field == "collapse_threshold"
                   else "lam* in ref-width units")
        print(f"  equivariance — {how}:")
        print(f"{'value':>7} | {'lam* (grid)':>12} | {inv_col:>22} | "
              f"{'gain*':>7} | {'right':>8} | {'attr':>5} | verdict")
        print("-" * 104)
        lc0 = lm.collapse_threshold
        s0 = lm.collapse_sharpness
        erg: List[Dict] = []
        for val in values:
            lams = equivariant_lams(DEFAULT_GRID, field, val, ref, lc0, s0)
            if len(lams) < 5:
                continue
            r = run_one(lm, graph, lams, args.seeds, args.problems,
                        field, val, args.boot, rng)
            r["scaled_lams"] = lams
            r["lambda_star_invariant"] = invariant_star(
                r, field, val, ref, lc0, s0)
            erg.append(r)
            print(f"{val:>7.3f} | {r['lambda_star']:>12.2f} | "
                  f"{r['lambda_star_invariant']:>22.4f} | {r['gain_star']:>7.4f} | "
                  f"{r['right_effect']:>+8.4f} | {r['share']:>4.0%} | "
                  f"{'SUPPORTED' if r['supported'] else 'REJECTED'}")
        all_erg[name] = erg

        # ---- like-for-like verdict -----------------------------------------
        emp = [r for r in res if not r["structural"]]
        emp_raw = [r["lambda_star"] for r in emp]
        emp_inv = [r["lambda_star_invariant"] for r in erg]
        sup_emp = [r["supported"] for r in emp]
        print(f"  -> lambda* over non-structural values: "
              f"{[round(x, 2) for x in emp_raw]}")
        print(f"  -> spread, grid units       = {max(emp_raw)-min(emp_raw):.2f}")
        if emp_inv:
            print(f"  -> spread, invariant units  = {max(emp_inv)-min(emp_inv):.2f}")
        print(f"  -> SUPPORTED for {sum(sup_emp)}/{len(sup_emp)} non-structural values")
        print(f"  -> attribution share range  = "
              f"{min(r['share'] for r in res):.0%} – "
              f"{max(r['share'] for r in res):.0%}")

    # ---- overall -----------------------------------------------------------
    print()
    print("=" * 104)
    print("OVERALL")
    print("=" * 104)
    for name, res in all_results.items():
        emp = [r for r in res if not r["structural"]]
        stars = [r["lambda_star"] for r in emp]
        sup = sum(1 for r in emp if r["supported"])
        print(f"  {name:<10} lambda* spread {max(stars)-min(stars):.2f} "
              f"over {len(emp)} values | SUPPORTED {sup}/{len(emp)} | "
              f"attribution {min(r['share'] for r in res):.0%}-"
              f"{max(r['share'] for r in res):.0%}")
    print()
    print("  Reading: the EXISTENCE of the boundary and the ATTRIBUTION SHARE")
    print("  should be stable across every A9 value. The LOCATION of lambda* is")
    print("  expected to move and must be reported as an interval, not a point.")

    path = os.path.join(args.outdir, "m2_a9_sensitivity_v2.json")
    with open(path, "w", encoding="utf-8") as f:
        def strip(rs):
            return [{kk: vv for kk, vv in r.items()
                     if kk not in ("notes", "curve", "lambdas")} for r in rs]
        json.dump({
            "seeds": args.seeds, "learners": args.learners,
            "problems": args.problems, "bootstrap": args.boot,
            "results": {k: strip(v) for k, v in all_results.items()},
            "ergodic": {k: strip(v) for k, v in all_erg.items()},
        }, f, ensure_ascii=False, indent=2)

    csv_path = os.path.join(args.outdir, "m2_a9_sensitivity_v2.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["swept_constant", "value", "lambda", "earned_gain"])
        for name, res in all_results.items():
            for r in res:
                for lam, g in zip(r["lambdas"], r["curve"]):
                    w.writerow([name, r["value"], lam, f"{g:.6f}"])

    print()
    print(f"[A9] json -> {path}")
    print(f"[A9] csv  -> {csv_path}")


if __name__ == "__main__":
    main()
