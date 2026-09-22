#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAGE · M3 power analysis (2026-09-21)

WHY THIS SCRIPT EXISTS
----------------------
The 2026-09-21 re-run of M2 showed the attribution criterion is NOT sample-size
free: at 8 seeds the M3 mutant passed when it should have failed, meaning that
with too little data the criterion credits scaffolding for an effect the leak
channel produced -- exactly the error the apparatus exists to prevent.

That raises D12 item 3 (sample size) from "ask the user" to "give the user a
floor". This script computes that floor.

CRITICAL METHOD CHOICE (do not silently change this)
----------------------------------------------------
We do NOT use the effect sizes from our own simulator (M2). Those numbers are
constructed: the learner model is stipulated, so its effect size is whatever we
made it. Computing the required N from them would be circular -- we would be
using our own assumptions to validate how many subjects we need to test our
assumptions. D12 therefore must be answered with EXTERNAL effect sizes from
comparable published classroom interventions.

Reference points used here (all from documents already in this project):
  Brender et al. 2026 (AIED best paper), SG vs PR, N=66 total   -> d ~ 0.5
    (their reported perception contrast was d = 0.50)
  Smaller plausible effects for a shorter intervention          -> d = 0.3 / 0.4
  Optimistic case                                               -> d = 0.6

We also report the ANCOVA variant, since M3 has a pre-test covariate. Adding a
covariate reduces the required N by roughly (1 - rho^2), where rho is the
pre/post correlation. We use rho = 0.5, which is conservative for academic
outcomes; if the pre-test is a good predictor (rho higher) N falls further, so
this is a floor-of-a-floor in the safe direction.
"""
from math import sqrt

try:
    from statistics import NormalDist
    HAVE_STATISTICS = True
except Exception:  # pragma: no cover
    HAVE_STATISTICS = False


def z_for_two_sided_alpha(alpha: float) -> float:
    if HAVE_STATISTICS:
        return NormalDist().inv_cdf(1 - alpha / 2)
    raise RuntimeError("statistics.NormalDist unavailable")


def z_for_power(power: float) -> float:
    if HAVE_STATISTICS:
        return NormalDist().inv_cdf(power)
    raise RuntimeError("statistics.NormalDist unavailable")


def n_per_group_two_sample(d: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Normal-approximation sample size per group for a two-sample comparison."""
    za = z_for_two_sided_alpha(alpha)
    zb = z_for_power(power)
    return int(2 * ((za + zb) ** 2) / (d ** 2) + 0.999)  # ceil


def n_per_group_ancova(d: float, rho: float = 0.5, alpha: float = 0.05,
                       power: float = 0.80) -> int:
    """Per-group N when a pre-test covariate is included (ANCOVA)."""
    n = n_per_group_two_sample(d, alpha, power)
    return int(n * (1 - rho ** 2) + 0.999)  # ceil


def main() -> None:
    print("=" * 78)
    print("M3 POWER ANALYSIS -- required N PER GROUP")
    print("alpha = 0.05 two-sided, power = 0.80")
    print("Effect sizes are EXTERNAL (literature), never from our own simulator.")
    print("=" * 78)
    print()
    print(f"{'d':>6} | {'source / reading':<34} | {'t-test':>8} | {'ANCOVA':>8}")
    print(f"{'':>6} | {'':<34} | {'per grp':>8} | {'rho=.5':>8}")
    print("-" * 78)

    rows = [
        (0.30, "small; a short, low-dose intervention"),
        (0.40, "small-to-moderate"),
        (0.50, "Brender et al. 2026 contrast (d = 0.50)"),
        (0.60, "optimistic"),
    ]
    for d, label in rows:
        n_t = n_per_group_two_sample(d)
        n_a = n_per_group_ancova(d, rho=0.5)
        print(f"{d:>6.2f} | {label:<34} | {n_t:>8} | {n_a:>8}")

    print("-" * 78)
    print()
    print("THREE-ARM DESIGN (SAGE / answer-giving single agent / conventional self-study)")
    print("Total N at the reference effect size d = 0.50:")
    n_a = n_per_group_ancova(0.50, rho=0.5)
    print(f"    per group (ANCOVA, rho=.5) = {n_a}   -> total = {n_a * 3}")
    print()
    print("MINIMUM VIABLE variant -- the version that can still answer RQ1 only")
    print("(the attributable-share decomposition; it is a within-condition")
    print(" decomposition rather than a between-condition contrast, so it does")
    print(" NOT require detecting a group difference):")
    print("    one arm, pre-specified in `15` section 6.2")
    print("    still bounded below by the same pitfall: too few observations makes")
    print("    the criterion credit scaffolding for leak-suppression effects.")
    print()
    print("HONEST CAVEAT (must travel with every use of these numbers):")
    print("  * The normal approximation is optimistic for very small N; treat the")
    print("    small-d rows as indicative, not exact.")
    print("  * rho = 0.5 is conservative. A stronger pre-test correlation lowers N;")
    print("    a weaker one raises it above these figures.")
    print("  * Clustering matters: observations from one student are NOT independent.")
    print("    With ~20 problems per student, effective N is closer to the number of")
    print("    STUDENTS than to the number of observations. These figures are per-student.")
    print("  * Attrition and non-compliance require inflating the recruitment target")
    print("    above the analysable N (a common rule of thumb is +20%).")
    print()


if __name__ == "__main__":
    main()
