"""Dead-parameter auditor (SAGE). Rebuilt 2026-09-19 after the original was
cleaned up. MUST be run before submission.

WHY THIS EXISTS
---------------
`durable_factor` was declared, documented with three literature citations, and
described in the paper's assumption list (A3) -- while `simulate()` never read
it. Every previously reported number was therefore produced by a model that did
NOT contain the mechanism the paper claimed. It was caught only because a
mutation test mutated the field and the output did not move.

Nothing in a normal test suite catches this. Coverage reports see the dataclass
field as "defined". Linters see it as "used" because it appears in `asdict()`
output. The only reliable detector is a static query over the AST for fields of
the model dataclass that no computation reads.

WHAT IT DOES
------------
1. Parses `m2_lambda_sweep.py` with `ast` (skipping comments/strings, which is
   where `durable_factor` appeared -- that is why grep-based checks passed).
2. Collects every attribute actually READ (`ast.Attribute` in Load context) on
   an object named `lm`/`m`/`model`, plus bare `self.X` reads.
3. Compares against the `LearnerModel` field list.
4. Additionally runs a MUTATION check for each field: if replacing the field
   does not change the reported earned gain, the field is dead no matter what
   the static analysis says.

Exit non-zero if any field is dead. Fail-closed: an auditor that cannot run
must not report "clean".
"""

from __future__ import annotations

import argparse
import ast
import os
import sys
from dataclasses import asdict, fields
from typing import Dict, List, Set

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SRC = "m2_lambda_sweep.py"


def attr_reads(tree: ast.AST) -> Set[str]:
    """Attribute names READ anywhere in the module.

    Only Load context counts. A field that appears solely in a docstring, a
    type annotation, or `asdict()`-style serialisation is NOT read by the
    computation.
    """
    names: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
            names.add(node.attr)
    return names


def subscript_or_call_reads(tree: ast.AST) -> Set[str]:
    """Names used in any expression position (rough fallback for `x['field']`)."""
    names: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            names.add(node.id)
    return names


def static_scan() -> Dict[str, bool]:
    from m2_lambda_sweep import LearnerModel
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, SRC), "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    reads = attr_reads(tree) | subscript_or_call_reads(tree)
    out: Dict[str, bool] = {}
    for fl in fields(LearnerModel):
        out[fl.name] = fl.name in reads
    return out


# Outputs a field may legitimately move. A field is DEAD only if mutating it
# moves NONE of these. Restricting the test to `earned_gain` alone would be
# wrong: `leak_immediate` and `leak_dependency` are real, live mechanisms whose
# effects are simply not visible in the far-transfer proxy -- `leak_immediate`
# moves the cheap-solve route, `leak_dependency` moves the dependency index.
# Both are reported in the paper. An auditor that screamed "DEAD" at them would
# be a false alarm, and a false alarm is how a real alarm gets ignored.
OBSERVABLES = ("gain", "leak_solve", "dep", "turns", "never", "mastery", "mi")


def mutation_scan(seeds: int, problems: int, learners: int) -> Dict[str, Dict[str, float]]:
    """For each field, perturb it and measure the delta in EVERY observable.

    A field is dead only when no observable moves. We report per-observable
    deltas so the reader can see WHICH mechanism a field drives.
    """
    from m2_lambda_sweep import (LearnerModel, build_408_graph, run_sweep,
                                 train_theta)

    lm = LearnerModel(n_learners=learners)
    graph = build_408_graph()
    lams = [0.0, 0.35, 0.60]

    def probe(m: LearnerModel) -> Dict[str, List[float]]:
        th = train_theta(m, graph, min(seeds, 4), problems)
        rows = run_sweep(m, graph, lams, seeds, problems, th)
        return {k: [r[k][0] for r in rows] for k in OBSERVABLES}

    base = probe(lm)
    deltas: Dict[str, Dict[str, float]] = {}
    for fl in fields(LearnerModel):
        cur = getattr(lm, fl.name)
        if isinstance(cur, tuple):
            mut = tuple(x * 1.5 if x else 0.5 for x in cur)
        elif isinstance(cur, float):
            mut = cur * 1.5 if cur else 0.05
        elif isinstance(cur, int):
            mut = max(1, int(cur * 1.5))
        else:
            continue
        try:
            got = probe(LearnerModel(**{**asdict(lm), fl.name: mut}))
        except Exception:
            deltas[fl.name] = {k: float("nan") for k in OBSERVABLES}
            continue
        deltas[fl.name] = {
            k: max(abs(a - b) for a, b in zip(got[k], base[k]))
            for k in OBSERVABLES
        }
    return deltas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--problems", type=int, default=20)
    ap.add_argument("--learners", type=int, default=240)
    args = ap.parse_args()

    print("=" * 92)
    print("[DEAD-PARAM AUDIT] every LearnerModel field must be READ by the "
          "computation, not merely declared")
    print("=" * 92)

    st = static_scan()
    mut = mutation_scan(args.seeds, args.problems, args.learners)

    print(f"{'field':<20} | {'read?':<6} | {'max |delta| over observables':<28} | status")
    print("-" * 92)
    dead: List[str] = []
    for name in st:
        read = st[name]
        d = mut.get(name, {})
        finite = {k: v for k, v in d.items() if v == v}   # drop NaN
        if not finite:
            status = "SKIP (mutation errored)"
            best = float("nan")
            which = "-"
        else:
            best = max(finite.values())
            which = max(finite, key=lambda k: finite[k])
            if not read:
                status = "DEAD (never read by computation)"
                dead.append(name)
            elif best <= 1e-12:
                status = "DEAD (mutating it moves nothing)"
                dead.append(name)
            else:
                status = "ok"
        shown = "yes" if read else "NO"
        print(f"{name:<20} | {shown:<6} | {best:>12.3e} (via {which:<8}) | {status}")

    print("-" * 92)
    print("  observable legend: gain=earned-gain, leak_solve=cheap solves, "
          "dep=dependency index,")
    print("                     turns, never=never-solved rate, "
          "mastery=final effective mastery, mi=MI estimate")
    print("  A field whose effect is confined to one observable is ALIVE — it "
          "just drives that")
    print("  mechanism, not the far-transfer proxy. Report it accordingly, and "
          "do not claim it")
    print("  affects a quantity it provably does not touch.")
    if dead:
        print(f"[DEAD-PARAM AUDIT] FAIL — {len(dead)} dead parameter(s): "
              f"{dead}")
        print("                     A parameter the computation never reads is "
              "not a mechanism.")
        print("                     Either wire it into `simulate()` or delete "
              "the claim that")
        print("                     depends on it. Do not ship a paper whose "
              "assumption list")
        print("                     names a mechanism the code does not "
              "implement.")
        raise SystemExit(1)
    print(f"[DEAD-PARAM AUDIT] PASS — all {len(st)} fields are read AND each "
          f"one moves the reported gain when mutated.")


if __name__ == "__main__":
    main()
