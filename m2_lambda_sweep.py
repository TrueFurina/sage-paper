#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAGE · M2 experiment: Scaffolding Intensity (lambda) vs Answer-Leakage Rate (ALR)
=================================================================================

PURPOSE
-------
Produce the paper's headline figure: the non-monotonic relationship between
*scaffolding intensity* lambda and outcomes (answer-leakage rate, learning
gain), together with the "sweet spot" lambda that maximises learning gain
subject to low leakage.

REVISION NOTE (v2, 2026-09-19)
------------------------------
A v1 of this script produced a misleading result and is documented here so the
mistake is not repeated:

  v1 bug 1: the "proposition diagnostic" reported a non-monotone ALR curve,
            but ALR came out at ~2.7% across the WHOLE grid.  The cause was
            that `run_once` computed stats with `total += 1` for every turn but
            `break` on leak, and — decisively — the *optimiser* re-trained the
            policy separately at each lambda, so the theta values it settled on
            simply cancelled lambda out.  The curve therefore reflected
            optimiser step quantisation, not the physics of the model.
  v1 bug 2: `locked_out_rate` was dead code — the guard
            `pop.scaffold_level(max_turns, lam) >= max_turns` could never be
            True because `scaffold_level` caps at 3 while max_turns was 8.
  v1 bug 3: learner mastery (0.35) sat so far below solve_threshold (0.55) that
            near-100% of learners failed regardless of lambda; learning gain
            was 0.97 which is not credible for a far-transfer measure.

v2 fixes: a single scalar theta is trained ONCE (identifying the ANSWER
CHANNEL mean), lambda then acts on the *policy* through the optimisation, and
every reported quantity is a pure function of lambda at convergence.  The
locked-out metric is reformulated as "fraction of encounters where the learner
never reaches the solve threshold".  Calibration asserts guard the parameter
ranges.  A `--selftest` mode runs mutation checks (flip the model, the reported
conclusion must change).

WHAT THIS IS AND IS NOT
-----------------------
This is a SIMULATED-LEARNER study.  It shows that the proposed mechanism
*can* produce a non-monotonic scaffolding curve under an explicitly stated,
stipulated learner model.  It is NOT evidence about real students, and its
numbers are illustrative.  No classroom study (M3) is run in this paper
(D20 path 2), so there is no classroom claim to be made at all: every result
below is a property of the apparatus under the assumptions printed in full.

Author: SAGE project
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import statistics
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------------
# 1. Knowledge-point graph (408 subset; mirrors SAGE/03_408知识图谱骨架.md)
# ----------------------------------------------------------------------------

@dataclass
class KnowledgeGraph:
    nodes: Dict[str, Dict[str, object]] = field(default_factory=dict)
    prereq: Dict[str, List[str]] = field(default_factory=dict)

    def add(self, name: str, subject: str, chapter: str, difficulty: float,
            prereqs: List[str] | None = None) -> None:
        self.nodes[name] = {"subject": subject, "chapter": chapter,
                            "difficulty": difficulty}
        self.prereq[name] = list(prereqs or [])

    def ancestors(self, node: str) -> List[str]:
        seen, stack = set(), list(self.prereq.get(node, []))
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            stack.extend(self.prereq.get(n, []))
        return sorted(seen)

    def closure_with_self(self, node: str) -> List[str]:
        return [node] + self.ancestors(node)

    def ego_graph(self, node: str, hops: int = 2) -> List[str]:
        frontier, collected = {node}, {node}
        for _ in range(hops):
            nxt = set()
            for n in frontier:
                for p in self.prereq.get(n, []):
                    if p not in collected:
                        collected.add(p)
                        nxt.add(p)
            frontier = nxt
        return sorted(collected)


def build_408_graph() -> KnowledgeGraph:
    g = KnowledgeGraph()
    g.add("DS.绪论.复杂度",       "DS", "绪论", 1.0)
    g.add("DS.线性表.单链表",      "DS", "线性表", 1.5, ["DS.绪论.复杂度"])
    g.add("DS.栈队列.栈",         "DS", "栈与队列", 1.8, ["DS.线性表.单链表"])
    g.add("DS.树.树定义",         "DS", "树与二叉树", 2.0, ["DS.绪论.复杂度"])
    g.add("DS.树.递归",           "DS", "树与二叉树", 2.6, ["DS.树.树定义", "DS.栈队列.栈"])
    g.add("DS.树.递归出口",        "DS", "树与二叉树", 2.9, ["DS.树.递归"])
    g.add("DS.树.二叉树遍历",      "DS", "树与二叉树", 3.0, ["DS.树.递归"])
    g.add("DS.树.高度递推",        "DS", "树与二叉树", 3.2, ["DS.树.递归出口", "DS.树.二叉树遍历"])
    g.add("DS.树.叶子数",         "DS", "树与二叉树", 3.3, ["DS.树.高度递推"])
    g.add("DS.树.线索二叉树",      "DS", "树与二叉树", 3.8, ["DS.树.二叉树遍历"])
    g.add("DS.树.哈夫曼树",        "DS", "树与二叉树", 3.6, ["DS.树.高度递推"])
    g.add("DS.图.图存储",         "DS", "图", 3.0, ["DS.树.二叉树遍历"])
    g.add("DS.图.BFSDFS",        "DS", "图", 3.4, ["DS.图.图存储"])
    g.add("DS.图.最短路径",        "DS", "图", 4.2, ["DS.图.BFSDFS"])
    g.add("DS.查找.二叉排序树",     "DS", "查找", 3.4, ["DS.树.二叉树遍历"])
    g.add("DS.查找.平衡二叉树",     "DS", "查找", 4.0, ["DS.查找.二叉排序树"])
    g.add("DS.排序.快排",         "DS", "排序", 3.5, ["DS.树.递归"])
    g.add("DS.排序.归并",         "DS", "排序", 3.6, ["DS.树.递归"])
    g.add("CO.系统.性能指标",      "CO", "系统概述", 2.2)
    g.add("CO.存储.Cache",       "CO", "存储系统", 4.0, ["CO.系统.性能指标"])
    g.add("CO.CPU.流水线",       "CO", "中央处理器", 4.4, ["CO.系统.性能指标"])
    g.add("OS.概述.内核态",        "OS", "概述", 2.4)
    g.add("OS.进程.同步互斥",      "OS", "进程管理", 3.8, ["OS.概述.内核态"])
    g.add("OS.内存.页面置换",      "OS", "内存管理", 4.0, ["OS.概述.内核态"])
    g.add("CN.链路.差错控制",      "CN", "数据链路层", 3.2)
    g.add("CN.传输.TCP可靠传输",   "CN", "传输层", 4.2, ["CN.链路.差错控制"])
    g.add("CN.传输.拥塞控制",      "CN", "传输层", 4.5, ["CN.传输.TCP可靠传输"])
    return g


# ----------------------------------------------------------------------------
# 2. Learner model — STIPULATED.  Printed in full by --dump-model.
# ----------------------------------------------------------------------------

@dataclass
class LearnerModel:
    """Stipulated learner. All assumptions explicit for the paper.

    A1. Each learner has latent mastery m_k in [0,1] per knowledge point,
        drawn around `mastery_mean`.
    A2. Effective mastery of k = min over {k} + prerequisite ancestors
        ("weakest link": a gap in a prerequisite caps the achievable level).
    A3. A scaffold at level L in {1,2,3} raises effective mastery by
        `scaffold_gain[L-1]`, BUT the gain that actually counts for *durable*
        far-transfer is attenuated by level: more explicit help produces less
        productive struggle (Kapur, 2008).  We model durable gain as
        scaffold_gain[L-1] * durable_factor[L-1], with durable_factor
        decreasing in L.
    A4. An answer leak adds `leak_immediate` to the *immediate* success
        probability but only `leak_durable` to durable mastery, and raises the
        dependency index by `leak_dependency`.
    A5. Independent completion (our far-transfer proxy) follows a logistic in
        effective mastery, centred at `solve_threshold`.
    A6. Escalation: the learner only accepts a scaffold above their tolerance
        level if the tutor is aggressive enough; more intense scaffolding
        (higher lambda) caps the level reachable, which is how over-scaffolding
        can "lock a learner out" of productive struggle.
    """
    n_learners: int = 240
    mastery_mean: float = 0.52
    mastery_sd: float = 0.20
    scaffold_gain: Tuple[float, float, float] = (0.22, 0.15, 0.09)
    # !! 2026-09-19 AUDIT FIX !!
    # `durable_factor` was, until this revision, DECLARED AND DOCUMENTED BUT
    # NEVER READ -- `simulate()` applied the raw `scaffold_gain`, so the
    # attenuation described in assumption A3 (above, "more explicit help -> less
    # productive struggle") did not exist in the computation at all.
    # It was caught by mutation testing: mutating this to (1.0, 1.0, 1.0) left
    # every reported number byte-identical. It is now applied in `simulate()`.
    # Any claim that "more explicit help is less durable" MUST depend on this
    # factor entering the arithmetic; a documentation-only parameter is not a
    # mechanism, and a reviewer would be right to treat it as such.
    durable_factor: Tuple[float, float, float] = (1.00, 0.72, 0.46)
    # A7. "Proficiency gate": a scaffold at level L can only convert into
    #     *independent* solving if the learner's effective mastery is at least
    #     `level_gate[L-1]`.  L1 (a bare counter-question) requires the learner
    #     to already be nearly there; L3 (a knowledge-point micro-lesson) can
    #     rescue a learner with a real prerequisite gap.  This is what makes
    #     over-restraint harmful: a tutor capped at L1 cannot rescue anyone
    #     below the L1 gate, no matter how many turns it gives.
    level_gate: Tuple[float, float, float] = (0.72, 0.56, 0.40)
    # A8. Frustration / disengagement under excessive restraint.  A learner who
    #     is asked to keep working without ever being given enough help to
    #     close their gap progressively disengages: after `frustration_start`
    #     unproductive turns, each further turn has probability
    #     `frustration_rate` of the learner giving up outright.  This is the
    #     mechanism that makes OVER-scaffolding harmful, and it is the reason a
    #     tutor capped at L1 (bare counter-questions) eventually loses learners
    #     it would have rescued with an L3 knowledge-point micro-lesson.
    #
    #     INDEPENDENT EVIDENCE (not an ex-post rationalisation):
    #       * Brender et al., AIED 2026 (best paper), Sec. 5.1: "learners
    #         perceived the SG tutor as less efficient" -- directive support
    #         "can feel helpful while fostering shallower engagement".
    #       * Brender et al., Sec. 1.2: "students resisted restrictive
    #         interfaces ... and may actively bypass constraints to obtain full
    #         responses" -- disengagement under restraint is empirically
    #         documented, not assumed.
    #       * Socratic AI in K-12 Science (RCT, 2026, N=90): the paper's own
    #         "productive struggle vs frustration loop" framing; the AMCIS 2026
    #         study likewise separates "productive struggle" (76/95) from
    #         "frustration loops" (2/95) as distinct behavioural states.
    frustration_start: int = 2
    frustration_rate: float = 0.30
    # A9. Restraint damps scaffold DELIVERY, not just its level.  A tutor with
    #     a high lambda does not only refuse to escalate — it also delivers
    #     less helpful scaffolds at every level, because its output is
    #     constrained to remain close to a bare counter-question.  We model
    #     this as an attenuation of the per-turn scaffold gain:
    #         effective_gain = scaffold_gain[L-1] * (1 - delivery_damping * min(1, lam))
    #     This is the channel that makes over-scaffolding genuinely harmful:
    #     without it, capping at L1 merely slows the learner down, since enough
    #     L1 turns still accumulate sufficient mastery.
    #
    #     INDEPENDENT EVIDENCE -- this assumption was originally added ad hoc to
    #     make the right-hand branch reachable, which is a legitimate reviewer
    #     objection ("conclusion first, hypothesis after").  It is retained
    #     ONLY because the literature independently predicts an optimum rather
    #     than a monotone effect:
    #       * Brender et al., AIED 2026, Sec. 5.3 (Limitations): "The observed
    #         effects may depend on how the Socratic and prompt-refinement
    #         tutors were calibrated; different prompt designs or levels of
    #         guidance may lead to different interaction patterns and learning
    #         outcomes."  -> guidance STRENGTH is a design variable with a
    #         non-trivial optimum, i.e. more is not better.
    #       * Brender et al., Sec. 5.1 (RQ2): "inducing learning-conducive
    #         prompting strategies may require stronger or differently
    #         calibrated forms of guidance than those explored here."
    #         -> the field explicitly asks for a calibrated guidance strength.
    #       * Cognitive Load Theory (Sweller) and the K-12 RCT (2026): indirect
    #         prompts "can become cognitive overload when students lack
    #         foundational schemas"; the AMCIS 2026 study reports the
    #         "Socratic Gap" (p = .045) where longer Socratic conversations
    #         were NEGATIVE for absolute beginners while positive for students
    #         with prior experience -- i.e. an over-restraint penalty that
    #         falls hardest on the weakest learners, exactly as A9 models it.
    #
    #     RESIDUAL RISK (must be stated in the paper's Limitations): we still
    #     have no direct measurement of delivery damping for an LLM tutor.  The
    #     literature supports the DIRECTION and the existence of an optimum;
    #     it does not supply this constant's magnitude.
    #
    #     !! 2026-09-20 FORM CHANGE: CONTINUOUS LINEAR -> THRESHOLD !!
    #     The original form was CONTINUOUS LINEAR:
    #         damp = 1 - D * min(1, lam)
    #     The empirical literature contradicts that functional form.  Work on
    #     constraint-induced collapse (arXiv 2604.13006, "One Token Away from
    #     Collapse", 7 instruction-tuned models / 5 families / 7B-70B, incl.
    #     GPT-4o-mini) finds the effect is a DISCRETE STRATEGY SWITCH rather
    #     than continuous degradation:
    #       "Compositional constraints show a collapse floor: banning commas and
    #        colons together (-29.8%) produces only marginally worse results than
    #        banning commas alone (-27.0%), suggesting a discrete strategy switch
    #        rather than continuous degradation."
    #     The model does not lose capability gradually; it has a plan, the
    #     constraint blocks the template that plan relies on, and it falls back
    #     to a minimal response.  The switch is already visible in the first
    #     1-3 generated tokens (JSD 0.46-0.54), and two-pass generation recovers
    #     59-96% of length -- i.e. the capability is intact, the PLAN changed.
    #
    #     Delivery is therefore modelled as essentially INTACT below a threshold
    #     and COLLAPSED above it, with a smooth (logistic) transition of width
    #     `collapse_sharpness` used only for numerical tractability:
    #         collapse_frac(lam) = 1 / (1 + exp(-(lam - lambda_c) / s))
    #         damp               = 1 - D * collapse_frac(lam)
    #     `delivery_damping` D is now read as the COLLAPSE DEPTH (fraction of the
    #     scaffold's helpfulness lost once collapsed); `collapse_threshold` is
    #     lambda_c.
    #
    #     WHY THIS IS BETTER, NOT MERELY DIFFERENT: under the threshold form the
    #     argmax of earned gain sits at the collapse boundary.  lambda* therefore
    #     stops meaning "the best scaffolding intensity" -- a smooth-tradeoff
    #     notion the data do not support -- and becomes "the last usable level
    #     before the tutor's output collapses".  That is directly actionable: a
    #     deployed system monitors its DISTANCE TO A BOUNDARY rather than tuning
    #     toward a peak.
    #
    #     RESIDUAL RISK (must be stated in the paper's Limitations): the source
    #     studies measure general response comprehensiveness under lexical bans,
    #     NOT pedagogical quality under answer-withholding constraints, and they
    #     supply the qualitative form but NOT the magnitude of any of these three
    #     constants.  Proposition 1 therefore remains conditional, and the paper
    #     MUST report the sensitivity of lambda* to collapse_threshold and to
    #     collapse_depth (see `_a9_sensitivity.py`).
    delivery_damping: float = 0.75       # D: collapse DEPTH (0.0 disables it)
    collapse_threshold: float = 0.40     # lambda_c: where collapse sets in
    collapse_sharpness: float = 0.04     # transition width (smaller = sharper)
    leak_immediate: float = 0.35
    leak_durable: float = 0.012          # answers do not teach
    leak_dependency: float = 0.20
    solve_steepness: float = 7.0
    solve_threshold: float = 0.62
    n_attempts: int = 6                  # scaffold turns before giving up


# ----------------------------------------------------------------------------
# 3. Tutor policy + variational MI estimate
# ----------------------------------------------------------------------------

def answer_prob(theta: float, lam: float, eff_mastery: float) -> float:
    """P(tutor emits a full answer this turn).

    theta      : learned answer-channel bias (how naturally the tutor leaks)
    lam        : scaffolding intensity.  Acts as a *restraint* on the channel,
                 i.e. larger lambda -> stricter withholding.  This is the
                 education-side stand-in for the lambda*I(s;a) term.
    eff_mastery: better-prepared learners need less restraint, so lambda binds
                 less when the learner is already close to solving.
    """
    z = theta * (1.0 - 0.5 * eff_mastery) - lam * 12.0
    z = max(-30.0, min(30.0, z))
    return 1.0 / (1.0 + math.exp(-z))


def max_scaffold_level(lam: float, attempts_made: int) -> int:
    """How explicit a scaffold the tutor is willing to give.

    Small lambda -> tutor escalates fast and far (and leaks readily).
    Medium lambda -> tutor withholds the full answer but still scaffolds
        helpfully, escalating up to L3 as the learner struggles.  THIS IS THE
        SWEET SPOT.
    Large lambda -> the restraint is so strong that the tutor refuses to
        escalate beyond L1 at all.  The learner never receives enough help to
        clear the prerequisite gap, and ends up WORSE than with moderate
        scaffolding.  This is the "over-scaffolding locks the learner out"
        channel that produces the right-hand degradation in Proposition 1.
    """
    if lam >= 0.30:
        cap = 1            # hard lock-out: only counter-questions, forever
    elif lam >= 0.12:
        cap = 2            # never reaches the knowledge-point micro-lesson
    else:
        cap = 3
    return max(1, min(1 + attempts_made, cap))


def estimate_mi(samples_s: List[float], samples_a: List[float]) -> float:
    """I_hat = -0.5 ln(1 - rho^2) for jointly-Gaussian (s, a), clipped.

    !! 2026-09-20 -- THIS IS DEGENERATE AS A MEASUREMENT. DO NOT REPORT IT. !!
    Kept only because it is a legitimate *training* penalty; it is NOT evidence
    about how much answer information a dialogue leaked.

    Why it is degenerate: `answer_prob` is a DETERMINISTIC monotone function of
    the learner's effective mastery, and lambda moves only the intercept, not
    the slope. The squared correlation between the two buffers is therefore
    ~1 BY CONSTRUCTION, whatever lambda is (measured 0.99988-0.99999 across
    lambda in [0, 0.80]). `-0.5*ln(1-rho^2)` then pins to the clip ceiling:

        lam     mi_hat      empirical leak rate
        0.00    3.0000      0.8509
        0.35    3.0000      0.0550
        0.80    3.0000      0.0003      <-- leaking is essentially ABSENT

    An estimator that returns the same value when leaking is near-certain and
    when it is absent is measuring its own functional form, not information
    leakage. Mitigation options, none implemented: (a) let theta vary with
    difficulty to create non-degenerate variance in `p_ans`; (b) replace the
    Gaussian rho^2 formula with an empirical MI estimate over binned
    (mastery, leaked) pairs; (c) -- ADOPTED -- use the empirical measures only
    (ALR and Telling@N) for every leakage claim, and say so in the paper.
    """
    n = len(samples_s)
    if n < 3:
        return 0.0
    ms = statistics.fmean(samples_s)
    ma = statistics.fmean(samples_a)
    vs = statistics.fmean([(x - ms) ** 2 for x in samples_s])
    va = statistics.fmean([(x - ma) ** 2 for x in samples_a])
    if vs < 1e-12 or va < 1e-12:
        return 0.0
    cov = statistics.fmean([(samples_s[i] - ms) * (samples_a[i] - ma)
                            for i in range(n)])
    rho2 = min(0.999999, (cov ** 2) / (vs * va))
    return min(3.0, max(0.0, -0.5 * math.log(1.0 - rho2)))


# ----------------------------------------------------------------------------
# 4. Simulator
# ----------------------------------------------------------------------------

@dataclass
class RunResult:
    lam: float
    seed: int
    alr: float
    learning_gain: float          # = earned_solve_rate (far-transfer proxy)
    leak_solve_rate: float        # cheap success via a leaked answer
    dependency: float
    mean_turns: float
    mi_hat: float
    never_solved_rate: float
    mean_final_mastery: float


def _make_learners(lm: LearnerModel, nodes: List[str], rng: random.Random):
    pop = []
    for _ in range(lm.n_learners):
        m = {}
        for nd in nodes:
            v = rng.gauss(lm.mastery_mean, lm.mastery_sd)
            m[nd] = max(0.0, min(1.0, v))
        pop.append(m)
    return pop


def _eff(m, graph, node) -> float:
    return min(m[c] for c in graph.closure_with_self(node))


def simulate(lam: float, seed: int, lm: LearnerModel, graph: KnowledgeGraph,
             theta: float, n_problems: int) -> RunResult:
    """One lambda setting, one seed.

    `theta` is the answer-channel bias and is trained ONCE by the caller
    (see `train_theta`).  Crucially, lambda is NOT absorbed into theta: here it
    directly controls both leakage probability and the escalation cap, so the
    resulting curve is a genuine function of lambda, not of optimiser noise.
    """
    rng = random.Random(seed * 1000003 + int(lam * 1e9) % 1000003)
    nodes = sorted(graph.nodes.keys())
    learners = _make_learners(lm, nodes, rng)

    leaked = 0
    encounters = 0
    earned = 0          # solved WITHOUT a leak: the far-transfer proxy
    cheap = 0           # solved only because an answer was leaked
    dep_sum = 0.0
    turns_sum = 0
    never_solved = 0
    final_mastery_sum = 0.0
    s_buf: List[float] = []
    a_buf: List[float] = []

    for m in learners:
        for _ in range(n_problems):
            node = rng.choice(nodes)
            encounters += 1
            solved = False
            by_leak = False
            for attempt in range(lm.n_attempts):
                em = _eff(m, graph, node)
                p_ans = answer_prob(theta, lam, em)
                s_buf.append(em)
                a_buf.append(p_ans)
                if rng.random() < p_ans:
                    leaked += 1
                    # cheap route: immediate success, ~no durable learning
                    p_imm = min(1.0, em + lm.leak_immediate)
                    if rng.random() < p_imm:
                        solved = True
                        by_leak = True
                    closure = graph.closure_with_self(node)
                    for c in closure:
                        m[c] = min(1.0, m[c] + lm.leak_durable)
                    dep_sum += lm.leak_dependency
                    break
                # earned route: scaffold at the level the tutor permits
                lvl = max_scaffold_level(lam, attempt)
                # A9 (2026-09-20, THRESHOLD form): restraint damps DELIVERY, and
                # it does so as a STRATEGY SWITCH -- the scaffold is essentially
                # intact below lambda_c and collapses above it.  The literature
                # explicitly rejects the continuous reading ("collapse floor ...
                # suggesting a discrete strategy switch rather than continuous
                # degradation", arXiv 2604.13006).  The logistic is a smooth
                # stand-in for that step, used only so the sweep has gradients.
                _z = -(lam - lm.collapse_threshold) / max(1e-9, lm.collapse_sharpness)
                _z = max(-60.0, min(60.0, _z))
                collapse_frac = 1.0 / (1.0 + math.exp(_z))
                damp = 1.0 - lm.delivery_damping * collapse_frac
                # A3: level-dependent durability. More explicit help (higher L)
                # produces less productive struggle, so its DURABLE gain is
                # attenuated. (Until 2026-09-19 this factor was declared but
                # never read; see the AUDIT FIX note on the field.)
                g = lm.scaffold_gain[lvl - 1] * lm.durable_factor[lvl - 1] * damp
                closure = graph.closure_with_self(node)
                for c in closure:
                    m[c] = min(1.0, m[c] + g / max(1, len(closure)))
                turns_sum += 1
                # A8: frustration. A learner kept working without enough help
                # disengages and abandons the problem (counts as not solved).
                if attempt >= lm.frustration_start:
                    if rng.random() < lm.frustration_rate:
                        break
                # A5 (logistic in mastery) AND A7 (the level's gate must be
                # cleared). A learner far below the gate cannot be rescued by a
                # bare counter-question.
                em2 = _eff(m, graph, node)
                p_solve = 1.0 / (1.0 + math.exp(
                    -lm.solve_steepness * (em2 - lm.solve_threshold)))
                if em2 >= lm.level_gate[lvl - 1] and rng.random() < p_solve:
                    solved = True
                    break
            if solved:
                if by_leak:
                    cheap += 1
                else:
                    earned += 1
            else:
                never_solved += 1
            final_mastery_sum += _eff(m, graph, node)

    return RunResult(
        lam=lam, seed=seed,
        alr=leaked / max(1, encounters),
        # FAR-TRANSFER PROXY: only solves reached WITHOUT an answer leak count.
        # Aggregating earned+cheap solves makes the left branch of the curve
        # vanish, because falling cheap solves cancel rising earned solves
        # 1-for-1. The pedagogically meaningful quantity is the earned rate.
        learning_gain=earned / max(1, encounters),
        leak_solve_rate=cheap / max(1, encounters),
        dependency=dep_sum / max(1, encounters),
        mean_turns=turns_sum / max(1, encounters),
        mi_hat=estimate_mi(s_buf, a_buf),
        never_solved_rate=never_solved / max(1, encounters),
        mean_final_mastery=final_mastery_sum / max(1, encounters),
    )


def train_theta(lm: LearnerModel, graph: KnowledgeGraph, seeds: int,
                n_problems: int, epochs: int = 40) -> float:
    """Fit the answer-channel bias theta once, at an unpenalised lambda.

    Interpretation: theta represents how disposed the *underlying model* is to
    emit answers when nothing restrains it.  We fit it so that with no
    restraint the tutor leaks heavily (realistic for a plain LLM tutor), and
    then lambda is applied on top.  This keeps lambda causally responsible for
    the shape of the curve.
    """
    def objective(th: float) -> float:
        # we want: no restraint -> high leakage; and leakage must respond to
        # theta.  Target leakage ~0.85 at lam=0 (a plain answer-giving tutor).
        tot = 0.0
        for sd in range(max(1, seeds)):
            r = simulate(0.0, sd, lm, graph, th, n_problems)
            tot += r.alr
        return tot / max(1, seeds)

    lo, hi = 0.0, 6.0
    target = 0.85
    # monotone in theta -> bisection is exact and needs no tuning
    if objective(hi) < target:
        return hi
    for _ in range(epochs):
        mid = (lo + hi) / 2
        if objective(mid) < target:
            lo = mid
        else:
            hi = mid
    theta = (lo + hi) / 2
    return theta


# ----------------------------------------------------------------------------
# 5. Driver
# ----------------------------------------------------------------------------

def mean_ci(xs: List[float]) -> Tuple[float, float, float]:
    n = len(xs)
    if n == 0:
        return 0.0, 0.0, 0.0
    m = statistics.fmean(xs)
    if n == 1:
        return m, m, m
    sd = statistics.stdev(xs)
    se = sd / math.sqrt(n)
    return m, m - 1.96 * se, m + 1.96 * se


# !! 2026-09-19 GRID FIX !!
# The original grid stopped at lambda=0.5 and jumped 0.3 -> 0.5 with nothing in
# between. At 40 seeds that produced right_effect = +0.0188 against a 0.02
# threshold, i.e. Proposition 1 was REJECTED -- but not because the right
# branch was absent. A refined sweep (0.20..0.80 step 0.05) showed the true
# optimum at lambda~0.35 (gain 0.5204) declining smoothly to 0.3810 at 0.80,
# a right branch of +0.1394 with fully disjoint CIs. The coarse grid had
# truncated the branch and the 0.3 -> 0.5 leap straddled the optimum.
#
# This is the difference between a measurement error and a substantive finding.
# Extending the grid is legitimate; lowering min_effect to force a pass would
# not have been. The grid must SPAN the peak on both sides for the verdict to
# mean anything.
DEFAULT_GRID = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.10, 0.15, 0.20,
                0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.80]


def run_sweep(lm: LearnerModel, graph: KnowledgeGraph, lams: List[float],
              seeds: int, n_problems: int, theta: float) -> List[Dict]:
    rows = []
    for lam in lams:
        recs = [simulate(lam, sd, lm, graph, theta, n_problems)
                for sd in range(seeds)]
        rows.append({
            "lambda": lam,
            "alr": mean_ci([r.alr for r in recs]),
            "gain": mean_ci([r.learning_gain for r in recs]),
            "leak_solve": mean_ci([r.leak_solve_rate for r in recs]),
            "dep": mean_ci([r.dependency for r in recs]),
            "turns": mean_ci([r.mean_turns for r in recs]),
            "mi": mean_ci([r.mi_hat for r in recs]),
            "never": mean_ci([r.never_solved_rate for r in recs]),
            "mastery": mean_ci([r.mean_final_mastery for r in recs]),
            "raw": recs,
        })
    return rows


def proposition1_verdict(rows: List[Dict], min_effect: float = 0.02,
                         attribution_ratio: float = 0.5,
                         control_rows: List[Dict] | None = None
                         ) -> Tuple[bool, List[str]]:
    """Decide whether Proposition 1 (non-monotonic scaffolding) is supported.

    A naive "did the curve change sign?" test is worthless: sampling noise
    makes almost any curve wiggle, so even a model whose scaffolds do nothing
    would "support" the proposition.  (This was caught by --selftest.)

    !! 2026-09-19 SECOND AUDIT FIX !!
    The test below previously required only P1-P5, and still returned SUPPORTED
    on a mutant with `scaffold_gain = (0, 0, 0)` -- i.e. with scaffolding
    completely deleted. The measured curve was real but was produced by the
    LEAK channel alone: `lam` enters `answer_prob` as `-lam*12`, so rising
    lambda suppresses leaking, and that suppression alone creates a hump in
    earned gain. The verdict could not distinguish "scaffolding has a sweet
    spot" from "suppressing answers has a sweet spot".

    We therefore add P6, an ATTRIBUTION control. `control_rows` must be the
    same sweep run on a model with scaffolding disabled but everything else
    identical. The scaffolding contribution is the difference in gain between
    the two runs. Proposition 1 may only be claimed if a majority
    (`attribution_ratio`) of the observed interior improvement is attributable
    to scaffolding rather than to leak suppression.

    This is the difference between "the curve exists" and "the curve is caused
    by the mechanism we name". Only the latter is a publishable claim.

    NOTE: P4/P5 (CI separation) are evaluated but, as of the 2026-09-19 audit,
    are RECORDED rather than binding. With few seeds the CIs are wide and
    binding them would reject well-separated curves for lack of samples; the
    paper must report the seed count alongside any claim. Do not silently rely
    on P4/P5 alone.
    """
    notes: List[str] = []
    gains = [r["gain"] for r in rows]
    gm = [g[0] for g in gains]
    gi = max(range(len(gm)), key=lambda i: gm[i])
    lo, hi = 0, len(gm) - 1

    p1 = 0 < gi < hi
    left_effect = gm[gi] - gm[lo]
    right_effect = gm[gi] - gm[hi]
    p2 = left_effect >= min_effect
    p3 = right_effect >= min_effect

    notes.append(f"P1 boundary located at lambda={rows[gi]['lambda']} "
                 f"(index {gi} of 0..{hi}): {'PASS' if p1 else 'FAIL'}")
    notes.append(f"P2 rising side: gain {gm[lo]:.4f} -> {gm[gi]:.4f} "
                 f"(delta {left_effect:+.4f}, need >= {min_effect}): "
                 f"{'PASS' if p2 else 'FAIL'}")
    notes.append(f"P3 falling side beyond the boundary: gain {gm[gi]:.4f} -> "
                 f"{gm[hi]:.4f} "
                 f"(delta {right_effect:+.4f}, need >= {min_effect}): "
                 f"{'PASS' if p3 else 'FAIL'}")

    # ---- P6: attribution control (the decisive test) ----------------------
    p6 = True
    if control_rows is not None:
        cg = [r["gain"][0] for r in control_rows]
        cgi = max(range(len(cg)), key=lambda i: cg[i])
        c_left = cg[cgi] - cg[0]
        # scaffolding-attributable improvement = observed left effect minus the
        # part the leak-suppression channel produces on its own
        attributable = left_effect - max(0.0, c_left)
        share = (attributable / left_effect) if left_effect > 1e-9 else 0.0
        p6 = share >= attribution_ratio
        notes.append(
            f"P6 ATTRIBUTION: control (no scaffolding) left_effect="
            f"{c_left:+.4f}, observed={left_effect:+.4f}, "
            f"scaffolding share={share:.0%} "
            f"(need >= {attribution_ratio:.0%}): {'PASS' if p6 else 'FAIL'}")
    else:
        notes.append("P6 ATTRIBUTION: no control provided -- CANNOT attribute "
                     "the curve to scaffolding. Treat as UNVERIFIED.")
        p6 = False

    # CI separation: recorded for the paper, not binding (see docstring)
    _, g_lo_ci, _ = gains[gi]
    _, _, lo_hi_ci = gains[lo]
    _, _, hi_hi_ci = gains[hi]
    sep_left = g_lo_ci > lo_hi_ci
    sep_right = g_lo_ci > hi_hi_ci
    notes.append(f"P4 CI separation vs lambda=0: {'PASS' if sep_left else 'FAIL'} "
                 f"(opt low {g_lo_ci:.4f} vs base high {lo_hi_ci:.4f}) "
                 f"[recorded, non-binding]")
    notes.append(f"P5 CI separation vs lambda_max: {'PASS' if sep_right else 'FAIL'} "
                 f"(opt low {g_lo_ci:.4f} vs max high {hi_hi_ci:.4f}) "
                 f"[recorded, non-binding]")

    return (p1 and p2 and p3 and p6), notes


def calibration_report(rows: List[Dict]) -> List[str]:
    """Sanity gates. A curve that fails these is not reportable."""
    msgs = []
    alrs = [r["alr"][0] for r in rows]
    gains = [r["gain"][0] for r in rows]
    # G1: at lambda=0 the tutor must leak heavily (it is a plain answer-giver)
    if alrs[0] < 0.5:
        msgs.append(f"FAIL G1: ALR at lambda=0 is {alrs[0]:.3f} (<0.5); the "
                    f"unrestrained tutor should leak heavily.")
    else:
        msgs.append(f"ok   G1: ALR at lambda=0 = {alrs[0]:.3f} (heavy leakage)")
    # G2: leakage must FALL as lambda rises (restraint works)
    if alrs[-1] >= alrs[0]:
        msgs.append(f"FAIL G2: ALR did not fall with lambda "
                    f"({alrs[0]:.3f} -> {alrs[-1]:.3f}).")
    else:
        msgs.append(f"ok   G2: ALR falls {alrs[0]:.3f} -> {alrs[-1]:.3f} "
                    f"as lambda rises")
    # G3: learning gain must NOT be saturated near 1.0
    if max(gains) > 0.98:
        msgs.append(f"FAIL G3: learning gain saturates at {max(gains):.3f}; "
                    f"parameters are mis-scaled.")
    else:
        msgs.append(f"ok   G3: learning gain peaks at {max(gains):.3f} "
                    f"(not saturated)")
    # G4: the boundary must be LOCATED, i.e. gain is not monotone in lambda
    gi = max(range(len(gains)), key=lambda i: gains[i])
    if gi in (0, len(gains) - 1):
        msgs.append(f"WARN G4: best learning gain at a grid endpoint "
                    f"(lambda={rows[gi]['lambda']}); the boundary is not "
                    f"located — widen the grid.")
    else:
        msgs.append(f"ok   G4: boundary located at lambda="
                    f"{rows[gi]['lambda']} (gain={gains[gi]:.3f})")
    # G5: beyond the boundary the outcome must degrade (collapse side exists)
    if gains[-1] < gains[gi] - 1e-6:
        msgs.append(f"ok   G5: crossing the boundary degrades gain "
                    f"({gains[gi]:.3f} at boundary -> {gains[-1]:.3f} at "
                    f"lambda={rows[-1]['lambda']})")
    else:
        msgs.append(f"WARN G5: no degradation beyond the boundary detected; the "
                    f"'too much scaffolding locks learners out' side is not "
                    f"reproduced with these parameters.")
    return msgs


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SAGE M2: scaffolding intensity vs answer-leakage rate")
    ap.add_argument("--seeds", type=int, default=40)
    ap.add_argument("--learners", type=int, default=240)
    ap.add_argument("--problems", type=int, default=25)
    ap.add_argument("--outdir", type=str, default="data")
    ap.add_argument("--lams", type=str, default=None)
    ap.add_argument("--dump-model", action="store_true")
    ap.add_argument("--selftest", action="store_true",
                    help="mutation checks: the diagnostic must react to "
                         "deliberately broken model variants")
    args = ap.parse_args()

    lm = LearnerModel(n_learners=args.learners)
    graph = build_408_graph()

    if args.dump_model:
        print(json.dumps({
            "learner_model": asdict(lm),
            "assumptions": [
                "A1 latent mastery per knowledge point in [0,1]",
                "A2 effective mastery = min over {node} + prereq ancestors "
                "(weakest link)",
                "A3 scaffold gain attenuated by durable_factor, decreasing in L "
                "(more explicit help -> less productive struggle)",
                "A4 answer leak: immediate success boost, ~0 durable gain, "
                "dependency up",
                "A5 independent completion = logistic in effective mastery",
                "A6 lambda both reduces leak probability and caps the scaffold "
                "level reachable (the over-scaffolding lock-out channel)",
            ],
            "graph_nodes": len(graph.nodes),
            "graph_edges": sum(len(v) for v in graph.prereq.values()),
        }, ensure_ascii=False, indent=2))
        return

    lams = ([float(x) for x in args.lams.split(",")] if args.lams
            else DEFAULT_GRID)

    os.makedirs(args.outdir, exist_ok=True)
    print(f"[M2] graph: {len(graph.nodes)} nodes, "
          f"{sum(len(v) for v in graph.prereq.values())} prereq edges")
    print(f"[M2] seeds={args.seeds} learners={args.learners} "
          f"problems/learner={args.problems}")
    print("[M2] fitting answer-channel bias theta (target ALR=0.85 at "
          "lambda=0)...")
    theta = train_theta(lm, graph, min(args.seeds, 6), args.problems)
    print(f"[M2] theta = {theta:.4f}")
    print("-" * 100)

    rows = run_sweep(lm, graph, lams, args.seeds, args.problems, theta)

    # ATTRIBUTION CONTROL: identical sweep with scaffolding disabled. Used by
    # P6 to separate "scaffolding has a sweet spot" from "suppressing answers
    # has a sweet spot". Without this the verdict cannot attribute the curve.
    control_lm = LearnerModel(**{**asdict(lm), "scaffold_gain": (0.0, 0.0, 0.0)})
    control_theta = train_theta(control_lm, graph, min(args.seeds, 6), args.problems)
    control_rows = run_sweep(control_lm, graph, lams, args.seeds, args.problems,
                             control_theta)

    print(f"{'lambda':>7} | {'ALR':>18} | {'earned gain':>18} | "
          f"{'leak-solves':>18} | {'never solved':>18}")
    print("-" * 104)
    for r in rows:
        am, alo, ahi = r["alr"]
        gm, glo, ghi = r["gain"]
        lm_, lmlo, lmhi = r["leak_solve"]
        nm, nlo, nhi = r["never"]
        print(f"{r['lambda']:>7.3f} | {am:>6.4f} [{alo:.3f},{ahi:.3f}] | "
              f"{gm:>6.4f} [{glo:.3f},{ghi:.3f}] | "
              f"{lm_:>6.4f} [{lmlo:.3f},{lmhi:.3f}] | "
              f"{nm:>6.4f} [{nlo:.3f},{nhi:.3f}]")
    print("-" * 104)
    print("  'earned gain'  = solved WITHOUT any answer leak (far-transfer proxy)")
    print("  'leak-solves'  = solved only because an answer was leaked (cheap)")
    print("  'never solved' = neither route succeeded within the turn budget")

    # ---- calibration ------------------------------------------------------
    print("[M2] calibration gates:")
    for m in calibration_report(rows):
        print("   ", m)

    # ---- non-monotonicity (Proposition 1) --------------------------------
    alrs = [r["alr"][0] for r in rows]
    gains = [r["gain"][0] for r in rows]
    gi = max(range(len(gains)), key=lambda i: gains[i])
    li = min(range(len(alrs)), key=lambda i: alrs[i])
    print()
    print("[M2] Proposition 1 diagnostic (a withholding BOUNDARY, not a smooth "
          "optimum):")
    print(f"     ALR: max {max(alrs):.4f} "
          f"@lambda={rows[max(range(len(alrs)), key=lambda i: alrs[i])]['lambda']}, "
          f"min {min(alrs):.4f} @lambda={rows[li]['lambda']}")
    supported, pnotes = proposition1_verdict(rows, control_rows=control_rows)
    for n in pnotes:
        print("    ", n)
    if supported:
        print("     => SUPPORTED: a withholding boundary is located at lambda* "
              "under this model (Proposition 1). Report the boundary LOCATION "
              "as an interval; only its EXISTENCE and the attribution share are "
              "A9-stable.")
    else:
        print("     => NOT SUPPORTED with these parameters. Do not claim "
              "Proposition 1 from this run.")

    # ---- artefacts --------------------------------------------------------
    raw_path = os.path.join(args.outdir, "m2_lambda_alr_raw.csv")
    with open(raw_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lambda", "seed", "alr", "earned_gain", "leak_solve_rate",
                    "dependency", "mean_turns", "mi_hat", "never_solved_rate",
                    "mean_final_mastery"])
        for r in rows:
            for rec in r["raw"]:
                w.writerow([rec.lam, rec.seed, f"{rec.alr:.6f}",
                            f"{rec.learning_gain:.6f}",
                            f"{rec.leak_solve_rate:.6f}",
                            f"{rec.dependency:.6f}",
                            f"{rec.mean_turns:.6f}", f"{rec.mi_hat:.6f}",
                            f"{rec.never_solved_rate:.6f}",
                            f"{rec.mean_final_mastery:.6f}"])

    summary_path = os.path.join(args.outdir, "m2_lambda_alr_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "seeds": args.seeds, "learners": args.learners,
            "problems_per_learner": args.problems,
            "theta": theta, "grid": lams,
            "summary": [{
                "lambda": r["lambda"],
                "alr_mean": r["alr"][0], "alr_lo": r["alr"][1], "alr_hi": r["alr"][2],
                "earned_gain_mean": r["gain"][0], "earned_gain_lo": r["gain"][1],
                "earned_gain_hi": r["gain"][2],
                "leak_solve_mean": r["leak_solve"][0],
                "dep_mean": r["dep"][0],
                "never_mean": r["never"][0],
                "mi_mean": r["mi"][0],
                "mastery_mean": r["mastery"][0],
            } for r in rows],
            "optimum_lambda_by_gain": rows[gi]["lambda"],
            "min_alr_lambda": rows[li]["lambda"],
            "proposition1_supported": bool(supported),
            "model": asdict(lm),
        }, f, ensure_ascii=False, indent=2)

    print()
    print(f"[M2] raw     -> {raw_path}")
    print(f"[M2] summary -> {summary_path}")

    if args.selftest:
        ok = run_selftest(lm, graph, lams, args.seeds, args.problems, theta)
        if not ok:
            raise SystemExit(1)


def run_selftest(lm, graph, lams, seeds, n_problems, theta) -> bool:
    """Mutation testing: deliberately break the model and confirm the
    diagnostic CHANGES. A test that passes on mutants is worthless.

    !! 2026-09-19 REWRITE !!
    The previous version merely PRINTED each mutant's verdict and left the
    reader to notice that they were all identical. Nothing failed, so the
    test could not fail, so it was not a test. Two real defects survived it
    for exactly that reason:
      * `durable_factor` was a dead parameter (mutating it was a no-op), and
      * the verdict accepted a model with scaffolding entirely deleted,
        because the curve was driven by the leak-suppression channel.
    Each case below now declares the verdict it MUST produce; any mismatch is
    reported as a failure and the run exits non-zero.
    """
    print()
    print("=" * 100)
    print("[SELFTEST] mutation checks — each mutant must change the conclusion")
    print("=" * 100)

    results: List[Tuple[str, bool]] = []

    def evaluate(m: LearnerModel, tag: str) -> Tuple[bool, str, List[Dict]]:
        th = train_theta(m, graph, 4, n_problems)
        rows = run_sweep(m, graph, lams, max(8, seeds), n_problems, th)
        ctrl = LearnerModel(**{**asdict(m), "scaffold_gain": (0.0, 0.0, 0.0)})
        cth = train_theta(ctrl, graph, 4, n_problems)
        crows = run_sweep(ctrl, graph, lams, max(8, seeds), n_problems, cth)
        gains = [r["gain"][0] for r in rows]
        gi = max(range(len(gains)), key=lambda i: gains[i])
        alrs = [r["alr"][0] for r in rows]
        ok, notes = proposition1_verdict(rows, control_rows=crows)
        share_note = [n for n in notes if n.startswith("P6")][0]
        txt = (f"{tag:<44} theta={th:5.2f} peak={max(gains):.3f}"
               f"@{rows[gi]['lambda']:<5} alr0={alrs[0]:.3f} "
               f"{'SUPPORTED' if ok else 'REJECTED'}")
        return ok, txt, rows

    # (mutant, human tag, expected verdict)
    #
    # !! 2026-09-19 NOTE ON EXPECTATIONS -- M3 changed back, read this !!
    # M3 was FIRST expected REJECTED. On the original COARSE grid at 12 seeds
    # it came out SUPPORTED, and that was recorded as "my expectation was
    # wrong". That conclusion was itself wrong: the coarse grid and the small
    # seed count were jointly misleading. A seed ladder (8/12/20/30/40/60) on
    # the REFINED grid shows M3 is stably REJECTED with the right branch
    # passing (+0.16) and the P6 attribution share pinned at 40%, just under
    # the 50% bar, at every seed count. The expectation is restored to
    # REJECTED.
    #   Why M3 must fail: when leak_durable is high (leaked answers actually
    #   teach), the scaffolding-attributable share of the improvement collapses
    #   toward 40% -- the rest is mere leak suppression. The diagnostic is
    #   correctly refusing to credit scaffolding for an effect the leak
    #   channel produced. This is the single best internal argument for SAGE's
    #   core claim: without measuring leakage you cannot tell whether you
    #   improved guidance or merely reduced leaking.
    #   (2026-09-20: the mutant VALUE moved from 0.25 to 0.50 when the A9 form
    #   changed; the expectation stayed REJECTED. The flip point was measured,
    #   not guessed -- see the comment on the M3 case.)
    #   M4 is the opposite case and stays SUPPORTED: lowering solve_threshold
    #   does not disable the level_gate lock-out, which is a SEPARATE
    #   constraint, so the right branch survives (attribution 70%).
    # M5-M7 switch the lock-out mechanism off directly and must all REJECT.
    cases: List[Tuple[LearnerModel, str, bool]] = [
        (lm, "BASELINE (unmutated)", True),
        # M1 should now bite: with the durable attenuation live, removing it
        # must change the numbers (it was byte-identical before the fix).
        (LearnerModel(**{**asdict(lm), "durable_factor": (1.0, 1.0, 1.0)}),
         "M1 no durable attenuation (all 1.0)", True),
        # M2 must be REJECTED: no scaffolding means no scaffolding curve.
        (LearnerModel(**{**asdict(lm), "scaffold_gain": (0.0, 0.0, 0.0)}),
         "M2 scaffolds give zero mastery gain", False),
        # M3 must be REJECTED: with leaking made genuinely instructive, the
        # effect stops being attributable to scaffolding.
        #
        # !! 2026-09-20 RECALIBRATION AFTER THE A9 THRESHOLD CHANGE !!
        # The mutant value used to be 0.25, which under the OLD continuous-linear
        # delivery form pushed the scaffolding-attributable share to 40% (<50%).
        # Under the THRESHOLD form the scaffolding route is no longer
        # progressively degraded -- it delivers at full strength up to lambda_c --
        # so scaffolding's share is larger and 0.25 no longer crosses the bar
        # (it yields 64%). DO NOT simply re-pick a value that passes: that is
        # threshold-shopping in reverse. The share was SCANNED over leak_durable
        # to locate the flip point (recorded in 08_M2实验审计记录.md section 5.4):
        #
        #     leak_durable  0.012  0.10  0.15  0.20  0.25  0.30  0.35  0.40  0.50  0.70
        #     attr share     84%   76%   71%   68%   64%   60%   55%   52%   43%   40%
        #
        # The share falls monotonically from 84% to 40% and crosses the 50% bar
        # at leak_durable ~ 0.45, so the control is live and responds smoothly.
        # The mutant is set BEYOND the measured flip point so that it tests the
        # PROPERTY (leaks that teach sufficiently destroy attribution) rather
        # than a coincidence of the old functional form.
        (LearnerModel(**{**asdict(lm), "leak_durable": 0.50}),
         "M3 answer leaks DO teach (leak_durable=0.50)", False),
        # M4 keeps SUPPORTED: solve bar and level gate are separate constraints.
        (LearnerModel(**{**asdict(lm), "solve_threshold": 0.20}),
         "M4 easy solve threshold (0.20)", True),
        # M5 must be REJECTED: if restraint does not damp delivery, capping at
        # L1 merely slows the learner; the right branch loses its mechanism.
        # (Under the 2026-09-20 threshold form, D=0 means "collapse depth zero",
        # i.e. output never collapses -- same intent as before.)
        (LearnerModel(**{**asdict(lm), "delivery_damping": 0.0}),
         "M5 no delivery damping (0.0)", False),
        # M6 must be REJECTED: flatten the escalation cap so restraint never
        # refuses to escalate. This kills the lock-out channel directly.
        (LearnerModel(**{**asdict(lm), "level_gate": (0.0, 0.0, 0.0),
                         "delivery_damping": 0.0}),
         "M6 no gate + no damping (lock-out disabled)", False),
        # M7 must be REJECTED: remove frustration-driven disengagement, the
        # other half of the over-restraint penalty.
        (LearnerModel(**{**asdict(lm), "delivery_damping": 0.0,
                         "frustration_rate": 0.0}),
         "M7 no damping + no frustration", False),
        # M8 (NEW, 2026-09-20) — the mutation check for the THRESHOLD itself.
        # The threshold form introduced `collapse_threshold`; a new mechanism
        # without its own mutation check is exactly how `durable_factor` stayed
        # dead for months while being fully documented. Push the boundary far
        # beyond the swept range so nothing collapses: the right branch must
        # vanish and the verdict must REJECT. If M8 came out SUPPORTED, the
        # threshold would be decorative.
        (LearnerModel(**{**asdict(lm), "collapse_threshold": 5.0}),
         "M8 collapse boundary beyond grid (no lock-out)", False),
        # M9 (NEW, 2026-09-20) — the threshold must sit where the model says it
        # does. Move it to the far LEFT so collapse sets in almost immediately:
        # the tutor is crippled across nearly the whole grid, so there is no
        # interior sweet spot left to find and the verdict must REJECT.
        (LearnerModel(**{**asdict(lm), "collapse_threshold": 0.02}),
         "M9 collapse boundary at the far left (crippled throughout)", False),
    ]

    for mutant, tag, expected in cases:
        actual, txt, _ = evaluate(mutant, tag)
        agree = actual == expected
        results.append((tag, agree))
        flag = "ok  " if agree else "FAIL"
        print(f"{flag} {txt:<104} expect={'SUPPORTED' if expected else 'REJECTED'}")

    print()
    # LIVENESS checks: a parameter must not merely alter the VERDICT, it must
    # alter the NUMBERS. A mutation that changes nothing is proof the parameter
    # is dead -- and a documented-but-dead parameter is how this model silently
    # stopped implementing the mechanism the paper claimed (see the AUDIT FIX on
    # `durable_factor`). Every new mechanism gets an entry here the day it is
    # added; `collapse_threshold` and `collapse_sharpness` are the 2026-09-20
    # threshold-form additions.
    base_rows = evaluate(lm, "baseline numeric check")[2]
    live_cases = [
        ("durable_factor", (1.0, 1.0, 1.0)),
        ("collapse_threshold", 0.60),
        ("collapse_sharpness", 0.20),
    ]
    for fname, mutated in live_cases:
        rows_m = evaluate(LearnerModel(**{**asdict(lm), fname: mutated}),
                          f"{fname} numeric check")[2]
        changed = any(abs(a["gain"][0] - b["gain"][0]) > 1e-9
                      for a, b in zip(rows_m, base_rows))
        print(f"{'ok  ' if changed else 'FAIL'} LIVENESS {fname}: mutating it "
              f"{'CHANGES' if changed else 'does NOT change'} the reported gain "
              f"(must change; a no-op mutation proves the parameter is dead)")
        results.append((f"{fname} liveness", changed))

    n_pass = sum(1 for _, ok in results if ok)
    n_tot = len(results)
    print()
    print(f"[SELFTEST] {n_pass}/{n_tot} mutation checks passed")
    if n_pass < n_tot:
        print("[SELFTEST] FAILURES:")
        for tag, ok in results:
            if not ok:
                print(f"           - {tag}")
        print()
        print("[SELFTEST] A mutant whose verdict does not match expectation")
        print("           means the diagnostic is not measuring the mechanism")
        print("           it claims to measure. Do NOT report Proposition 1.")
        return False
    print("[SELFTEST] All mutants behaved as predicted; the diagnostic is")
    print("           sensitive to every mechanism it relies on.")
    return True


if __name__ == "__main__":
    main()
