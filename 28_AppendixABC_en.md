# SAGE · Appendices A–C (English draft)

> **Status (2026-09-22)**: first English draft. Sources: `01` §3.2 (A), `02` §§2–4/6 (B), `19` + `20` (C).
> **Standing restrictions**: (i) every element below is **designed, not validated** — say so where it matters;
> (ii) the knowledge graph is **v0.1 and has not been checked by a cryptography specialist**;
> (iii) the item bank is a **framework plus worked examples**, not a built instrument;
> (iv) the prompt templates are **our construction** and no claim is made that they are optimal or validated.
> **Internal anchors** (`01`, `02`, `19`, `20`) are for traceability and are removed at submission.

---

## Appendix A · The information bottleneck: formalisation and the threshold-versus-continuous contrast

### A.1 Setup

Let $s \in \mathcal{S}$ be the learner's (partially observable) knowledge state, $q$ an item, and $K(q) = \{k_1,\dots,k_m\}$ the chain of knowledge points the item decomposes into, with edges encoding prerequisite relations. A tutor is a policy $\pi(g \mid s, K(q))$ emitting a guidance utterance $g$. A conventional answer-oriented tutor emits a complete answer $a$; the object of interest here is the class of policies that emit guidance while withholding $a$.

Withholding is imposed as an information bottleneck on the pathway from learner state to revealed answer:

$$\min_{\pi}\;\; \mathcal{L}_{\text{coop}} \;+\; \lambda \cdot \hat{I}(s; a),$$

where $\mathcal{L}_{\text{coop}}$ is the cooperative learning-gain objective, $\hat{I}(s;a)$ is a variational estimate of the mutual information between learner state and revealed answer, and $\lambda$ is the **scaffolding intensity** — the single scalar through which guidance strength is set. Structurally this is the ordinary bottleneck: the policy is discouraged from routing answer-level information through its output in the way a bottleneck representation discards detail beyond what the task requires (Tishby et al., 2000; Alemi et al., 2017).

### A.2 What the penalty does and does not do — mandatory statement

**The penalty shapes the policy; it does not measure leakage.** This distinction is easy to elide and it is not elided here. In the simulation of §6 the implemented estimator is degenerate *as a measurement*: because the modelled emission probability is a deterministic monotone function of the learner's effective mastery, its squared correlation is approximately one by construction (measured 0.99988–0.99999 across the whole intensity range), and the estimate pins to its clipping ceiling at **every** setting — including the setting at which the empirical leak rate has fallen to 0.0003. An estimator that returns the same value when leakage is near-certain and when it is absent is measuring its own functional form.

Three consequences follow, and they are carried through §§5–8:

1. **No bounding claim is made.** We do not state that the bottleneck *bounds* answer leakage. The objective penalises a quantity; the penalised quantity is not an independent measurement of leakage.
2. **Leakage is reported with empirical measures only** — answer-leakage rate (ALR) and *Telling@N* (Mačina et al., 2023) — and in the present study those values are computed from the modelled emission event, so they are **properties of the stipulated model**, not an external estimate (Appendix C.5, §8.2).
3. **This independence will not be supplied by a classroom study**, because no classroom study is run (D20 path ②). The human-coded ALR a classroom extension would have provided is listed as future work, not as a pending result.

### A.3 Why the cost of restraint is modelled as a boundary, not a gradient

The functional form is a deliberate adoption of an empirically established one, not a modelling convenience. Work on constraint-induced collapse (arXiv 2604.13006; seven instruction-tuned models across five families, 7B–70B) reports that lexical constraints cost 14–48% of response comprehensiveness and — decisively here — that the cost is a **discrete strategy switch rather than continuous degradation**: banning commas and colons together (−29.8%) is only marginally worse than banning commas alone (−27.0%), which is the signature of a switch rather than a gradient. The mechanism is a **planning failure, not a capability limit**: two-pass generation recovers 59–96% of length, and the divergence between constrained and unconstrained generation is already visible in the first 1–3 tokens. The model does not gradually become less able to teach; it switches templates, and the switch has a location.

We model the delivered helpfulness accordingly. Let $d(\lambda) \in [0,1]$ be the fraction of the intended scaffold content that actually reaches the learner. In the **continuous** reading one would write $d$ as a smooth decreasing function of $\lambda$ and locate an interior maximum of the earned-solve curve. In the **threshold** reading adopted here, helpfulness is approximately intact up to a collapse threshold $\lambda_c$ and substantially degraded beyond it:

$$d(\lambda) \;\approx\; 1 \quad (\lambda < \lambda_c), \qquad d(\lambda) \;\approx\; d_{\min} \quad (\lambda \ge \lambda_c),$$

with the transition occupying a narrow band. Since answer leakage falls monotonically in $\lambda$ while delivered helpfulness is flat and then drops, the earned-solve rate first rises and then falls, and its maximum is **not** an optimal intensity in the sense of a smooth trade-off. It is the **lower edge of a boundary**: the last constraint level at which the tutor can still teach.

**Simulation status.** Under the stipulated learner model (240 learners × 25 problems × 40 seeds, θ = 0.3578), earned independent solves run 0.1279 at λ = 0 → **0.5659** at the boundary → 0.2651 at λ = 0.8: a rising side of **+0.4380** and a falling side of **+0.3008**. Past the boundary the curve does not continue to decay but **saturates at a floor** (0.2642 at λ = 0.70 against 0.2651 at λ = 0.80, with overlapping intervals), which is the signature the literature predicts for a discrete switch rather than a continuous penalty. The boundary is located at **λ\* = 0.30** and reported **as an interval, [0.20, 0.45]**, because its position moves with three constants we stipulated and never measured.

### A.4 The covariate is delivery, not the knob

Two results bear on how the location should be read, and both are used in §7.2.

- When the grid is solved so that the **delivered fraction** $d$ is held constant, the spread of the located optimum across collapse depths collapses, and the optimum sits at the **same delivered fraction (≈0.94)** regardless of depth: depth changes *which* λ reaches that fraction, not *whether* it is reached. The covariate is therefore delivery — an observable quantity — rather than λ, whose meaning depends on unmeasured constants.
- Expressing the grid in distance-to-boundary units accounts for most of the remaining movement in the threshold sweep.

The operational consequence is stated once and used consistently: a deployed system should **monitor its distance to the boundary and its delivered fraction**, not tune toward a peak it cannot reliably locate. This is the practically useful form of the "differently calibrated" guidance the field has called for (Brender et al., 2026, §5.1).

---

## Appendix B · Scaffolding protocol: ladder, interception, and prompt templates

### B.1 The ladder is ordered by proximity, not by modality

The ladder is the operational form of λ. The system begins at the furthest level and ascends only when the learner is demonstrably stuck and asks for help. A larger λ permits a **lower** ceiling on the ladder, i.e. more restraint.

The ordering axis is the utterance's **proximity to the complete answer**, not its modality. The distinction is not cosmetic: under a modality ordering the amount of answer information revealed need not be monotone in the level, and the premise that larger λ means more restraint becomes unstable — an objection a reviewer can put in one sentence. Modality is retained as a **delivery-form field** within a level, so the same proximity may be delivered as a counter-question, a micro-explanation, or a hint.

| Level | Proximity (axis) | Typical delivery form (field) | Contains the answer? | Worked instance (cryptography) |
|---|---|---|---|---|
| **L1** | **furthest** — direction only, or locating the stuck point; supplies no new content | counter-question | no | "To show this scheme is secure under chosen-ciphertext attack, what would you assume first?" |
| **L2** | **intermediate** — supplies a prerequisite the learner lacks, but does not touch the item's solution | micro-explanation of a prerequisite | no (prerequisite only) | "Recall the order of a group element: in a prime-order group every non-identity element has order equal to that prime." |
| **L3** | **nearest** — supplies a sub-step or a relation; **the final step is always left to the learner** | local hint | no (final step withheld) | "Try the reduction chain *decisional Diffie–Hellman ⇒ this KEM is IND-CCA secure* — the last step is yours." |

**Two red lines.** No level reproduces a complete solution: for a cryptography item, "the answer" is a complete proof, a complete derivation, a runnable implementation, or the final ciphertext or numeric result — any one of these constitutes leakage. And L3 supplies only **up to the penultimate step**; the final step is always reserved for the learner, which is how the primary outcome (earned independent solve) is wired directly into the mechanism.

**Why cryptography makes the axis native.** The graded notion of proximity is a property of the discipline rather than something we constructed: a lemma is further from a complete proof than a derivation step, which is further than the key step, which is further than the finished proof. Each grade can be anchored to a node of the knowledge graph (Appendix C.6), so "how close the tutor came to the answer" is a labelled property of a tutoring turn rather than a judgement call. What the scenario supplies is that such a calibration *can* exist; the specific calibration of levels remains to be fixed with a domain expert.

### B.2 Interpretation rule shared by all levels

> **Design note (constructed, not validated).** The templates below are our construction. They are reported so that the constraint we imposed is inspectable and reproducible; no claim is made that they are optimal, and none was tuned against learner outcomes.

**System instruction (all levels).**
```
You are a cryptography tutor for a graduate course.
You may: ask questions, point at a relation, explain a prerequisite concept, or restate the
learner's problem in smaller terms.
You must not: state a complete proof, a complete derivation, a runnable implementation, or the
final ciphertext or numeric result — at any level, under any phrasing of the learner's request.
At the nearest level, stop one step short and leave that step to the learner.
If the learner asks for the answer directly, do not refuse flatly; shrink the problem instead.
```

**L1 — counter-question (furthest).**
```
Task: about "{item}", ask the single question that would let the learner name the next move.
Supply no content of your own: no definitions, no steps, no formulas beyond what the item states.
Anchor the question to the knowledge point the learner is stuck on: {k*}.
```

**L2 — prerequisite micro-explanation (intermediate).**
```
Task: the learner's blocker is {k*}, whose prerequisite {k_pre} is not in place.
Explain {k_pre} as a self-contained concept, with one minimal example that is NOT this item.
Do not reference the item's construction and do not perform any of its steps.
```

**L3 — local hint (nearest, final step withheld).**
```
Task: supply the sub-step or relation that unblocks {k*}, and nothing more.
Stop at the penultimate step. State explicitly that the final step is the learner's to take.
Do not assemble the steps already given into a worked solution, even if asked to summarise.
```

**Learner-facing constraint confirmation (used only when the learner presses).**
```
I won't write it out — that would take the problem away from you. Here is the smaller thing:
{degraded sub-problem}.
```

### B.3 Answer-seeking interception

```
trigger:   the learner requests the answer directly on N consecutive turns (N = 2 by default)
action:    the request is not granted; the exchange is converted into a degraded sub-problem,
           or into a narrower L3 hint (which, after the reordering above, is the nearest level:
           a sub-step with the final step withheld)
objective: to convert "give me the answer" into "a smaller task the learner can finish unaided"
instance:  "just tell me how to write the reduction" →
           "let me shrink it: write the two ciphertexts the challenger supplies in the IND-CCA
            game — which step is where you get stuck?"
```

Two commitments follow from the evidence in §2. First, the interception is a **degradation into a sub-problem, not a refusal**: the learner who genuinely cannot proceed receives a foothold, while the learner pressing for the answer is required to attempt something. This is robust to misidentification of intent, which matters because misclassifying a struggling learner as an answer-seeker is the more damaging error. Second, the constraint acts at the point of the *first* request, not only at the final level: in one geometry ITS dataset the most likely next action after a first hint is to request a second (87% of the time), and after the second, a third (88%); counting a further request as failure, success falls from 78% on the first attempt to 21% after the first hint (Goldin, Koedinger & Aleven, 2012, Table 2). A system that guards only the last rung has already lost the exchange. The interception counter is logged and reported as a behavioural index of dependency.

### B.4 Main loop

```
SAGE_Main(q, M):                        # q = item, M = learner-state graph memory
    K = Decompose(q, M)                 # knowledge-point chain K(q)
    k* = Reconstruct(M, q)              # locate the bottleneck
    level = 1                           # furthest level first
    while not Solved(student):
        g = Guide(k*, level, M)         # level-constrained generation (B.2)
        if AskForAnswer(student):       # interception (B.3)
            g = CounterAsk(g, k*)       # degrade to a smaller sub-problem
        resp = student.respond(g)
        M = UpdateMemory(M, resp)
        if Stuck(resp) and level < 3:
            level += 1                  # ascend one rung
        elif Solved(resp):
            break
    e = SelectExercise(k*, level, M)    # adaptive item from the bank (Appendix C)
    ans = student.answer(e)
    M = UpdateMemory(M, ans)
    return M
```

### B.5 Events the implementation must log

```
ViewOpened(student, view_id, ts)              # which learner-facing view was opened
ConfidenceReported(student, item, conf, ts)   # self-report; intervention only, never an outcome
DiagnosisShown(student, card_id, ts)          # exposure to the diagnostic card
GuidedToLevel(student, q, level, ts)          # the level the ladder actually reached
```

`GuidedToLevel` is the load-bearing one: it is the direct test of the hint cascade in this setting — if a high proportion of our learners continue from L1 to L2, the cascade of Goldin et al. (2012) is reproduced, which is itself evidence for locating the constraint at the lower rungs rather than the last. Note that in the present study these events are **specified as instrumentation, not analysed**: the simulation logs levels, but §6 reports no result about the learner-facing views (Appendix C.7, `21` §4.6).

---

## Appendix C · Item bank taxonomy, worked items, and the leakage coding manual

### C.1 Status and red line

The item bank is a **self-authored, constructed instrument** aligned to the graduate cryptography curriculum; it reproduces no copyright-protected examination. This appendix gives its **classification framework, annotation dimensions, sampling rule and worked examples** — it is **not** a built and validated instrument. The target scale is ≈300 items covering 46 knowledge points × three item types; **construction and expert review are outstanding**. Because the bank is constructed, item-level results are reported as demonstrations of the apparatus, not as measurements of curriculum mastery.

### C.2 Item types and the leakage threshold per type

| Type | What the learner must produce | What counts as a complete answer (= leakage) |
|---|---|---|
| `derivation` | a proof or derivation chain | the complete proof, the complete derivation, or the single decisive step that ends it |
| `implementation` | runnable code, or algorithmic steps | a complete runnable implementation, or "here is the ciphertext / numeric result" |
| `audit` | locate an error, correct it, or apply a criterion | naming the error location and its correction outright, removing the learner's chance to find it |

### C.3 Annotation dimensions

| Dimension | Values | Note |
|---|---|---|
| **Type** (required) | `derivation` / `implementation` / `audit` | — |
| **Knowledge point** (required, anchored to §C.6) | L0-xx / L1-xx / L2-xx / L3-xx | 1–3 per item; far-transfer items ≥2 |
| **Layer** (derived) | L0 / L1 / L2 / L3 | L0 mathematical foundations → L3 engineering and frontier |
| **Difficulty band** | 1 (single step) … 5 (multi-step reduction / cross-layer) | used by adaptive selection |
| **Far-transfer flag** | boolean | true = requires integrating ≥2 knowledge points *without* signalling which |

### C.4 Worked items (one per layer shown; the full bank is not built)

**Derivation.**
- **P-D1** (L0-06, difficulty 3): Let $p$ be prime and $g$ a generator of $\mathbb{Z}_p^{*}$. Show that an adversary who solves CDH can solve DLP; and explain why DLP hardness does **not** entail CDH hardness.
- **P-D2** (L1-07 → L2-05, difficulty 5): In the random oracle model, give the reduction showing ElGamal is IND-CPA secure, reducing the adversary's advantage to DLP. *far-transfer = true.*
- **P-D3** (L2-02, difficulty 4): Write the formal IND-CPA game and prove that no deterministic encryption scheme can satisfy IND-CPA.

**Implementation.**
- **P-I1** (L1-02, difficulty 3): Given the irreducible polynomial $x^8+x^4+x^3+x+1$, implement the AES S-box affine transform over GF(2⁸).
- **P-I2** (L3-03, difficulty 4): Given the SM2 recommended curve parameters, implement ECDSA signing and verification without a cryptographic library.
- **P-I3** (L3-09, difficulty 5): Implement single-bit homomorphic addition in a BFV-style construction and explain where the noise grows.

**Audit** (drawn mainly from L2-07, erroneous reductions).
- **P-A1** (L2-07, difficulty 4): The reduction below claims to reduce ElGamal's IND-CCA security to DLP in the ROM; it contains a **time-bound violation**. Identify and fix it.
- **P-A2** (L2-03 / L2-04, difficulty 5): An IND-CCA2 reduction fails to keep the decryption oracle self-consistent on the challenge ciphertext. At which step does the reduction break, and why?
- **P-A3** (L3-13, difficulty 4): Given a Solidity contract, identify the reentrancy or signature-replay vulnerability and give the minimal fix.

Audit items are the sharpest contrast with general-purpose tutoring: erroneous-reduction types (L2-07) are where general models err most and where graph anchoring is needed most. That is a design rationale, not a measured result — no comparison against a general model is reported in this paper.

### C.5 Far-transfer construction rules

Far-transfer items must integrate ≥2 knowledge points and must **not** signal which ones, forcing transfer. Cross-layer combinations are preferred (scheme × proof, as in P-D2; number theory × engineering, as in P-I3). All far-transfer items are reserved for the attribution contrast and, in a future extension, the delayed test; ordinary items populate adaptive practice.

### C.6 The knowledge graph (v0.1 — not yet specialist-verified)

Four layers, **46 nodes** and approximately **45 hard prerequisite edges**:

| Layer | Content | Nodes |
|---|---|---|
| **L0** | mathematical foundations: groups/rings/fields, modular arithmetic, Euler–Fermat, GF(p), GF(2ⁿ), DLP, elliptic curves and group law, ECDLP, bilinear pairings, lattices and basis reduction, LWE | 11 |
| **L1** | classical and modern schemes: DES, AES/Rijndael, modes of operation, stream ciphers, RSA, Diffie–Hellman, ElGamal, ECC, hash functions, MAC/HMAC, DSA/ECDSA, IBE, key management | 13 |
| **L2** | security definitions and proofs: computational hardness assumptions, IND-CPA, IND-CCA2, random oracle model, security reduction, provable security, typical errors in reductions | 7 |
| **L3** | engineering and frontier: SM4, SM3, SM2, SM9, side channels, PKI, secret sharing, MPC, homomorphic encryption, ZKP, DKG, threshold signatures, smart-contract security, cross-chain privacy, privacy-computing integration | 15 |

Representative edges (direction is prerequisite → dependent):
```
groups/rings/fields → modular arithmetic → Euler–Fermat theorem
GF(p) → discrete logarithm → Diffie–Hellman, ElGamal
GF(p) → elliptic curves and group law → ECDLP → ECC
hash functions → random oracle model ;  hardness assumptions → security reduction → provable security
security reduction → typical errors in reductions
secret sharing → MPC, DKG, threshold signatures ;  DKG + threshold signatures → cross-chain privacy
```
Three uses in SAGE: bottleneck localisation (walk prerequisite edges backwards from the stuck node), next-step selection (sample within a 1–2 hop ego-graph around $k^*$), and item selection (each node carries derivation/implementation/audit items at difficulty bands).

> ⚠️ **Mandatory caveat.** The graph is **v0.1 and has not been reviewed by a cryptography specialist**. The direction and necessity of individual prerequisite edges must be verified before this appendix is submitted. Its node and edge counts are stated **as actually built** (46 / ≈45); earlier internal figures of 613 nodes / 609 edges were spurious and are not used anywhere.

### C.7 Leakage coding manual (*Telling@N*, after Mačina et al., 2023)

**Unit.** Each tutor turn. **Verdict.** Binary.

A turn is coded as **leaking** if and only if it directly supplies any of:
1. a complete proof or complete derivation chain;
2. a runnable implementation (or its equivalent — the final ciphertext or numeric result);
3. for an audit item, the error location *and* its correction given outright.

A turn is **not** coded as leaking if it only supplies a counter-question, a local hint, a micro-explanation of a prerequisite, or a decomposition of the problem into a smaller sub-problem — including when the learner has asked for the answer repeatedly.

**Reliability protocol.** At least two coders independently code ≥20% of the corpus; agreement (κ) is reported; disagreements are arbitrated by a third coder. This protocol is **pre-specified for a classroom extension**; **within the present simulation no human coding is performed** — leakage is determined from the logged emission event, and the resulting values are properties of the stipulated model rather than independent measurements (§5.4, §8.2). The mutual-information estimator appearing in the training objective is **not** used as a leakage measure (Appendix A.2).

**Learner-facing views are not analysed in this study.** View B displays mastery per knowledge point, which **is** the primary outcome: it may be displayed and may serve as a criterion, but it must **not** enter the measurement model, or the analysis is circular. The metacognitive module is an **intervention only** and is never a reported outcome, because it depends on self-report.

---

## Honest-status notes (not for publication)

| # | Item | Status |
|---|---|---|
| 1 | Prompt templates (B.2) | **Our construction.** Not validated, not tuned against outcomes; presented only so the constraint is inspectable. Must not be described as optimal or empirically derived |
| 2 | Ladder ordering (B.1) | ✅ Aligned with the D9 decision of 2026-09-22 (axis = proximity; L2/L3 reordered so L2 is the prerequisite and L3 the nearest). The specific level calibration still requires domain-expert confirmation |
| 3 | Knowledge graph (C.6) | ⚠️ **v0.1, not specialist-verified**; 46 nodes / ≈45 edges as actually built. Prerequisite edges must be checked before submission. 🚫 613/609 figures are spurious |
| 4 | Item bank (C.2–C.4) | ⚠️ **Framework plus worked examples only**; ≈300 items not yet built; difficulty bands not yet calibrated; worked items not expert-reviewed |
| 5 | `GuidedToLevel` and other events (B.5) | Specified as instrumentation; **not analysed** in this paper. §6 reports no view-related result |
| 6 | Appendix A numbers | Threshold-form only: λ\* = 0.30, interval [0.20, 0.45], 0.5659, +0.4380 / +0.3008, 86% (76–88%), delivered ≈0.94. 🚫 Do not mix with superseded continuous-form values (0.35 / 0.5204 / 85%) |
| 7 | arXiv 2604.13006 (A.3) | Quoted as the *form* of the cost; it measures general response comprehensiveness under lexical bans, **not** pedagogical quality under answer-withholding. Cross-domain analogy, declared as such |
| 8 | Mačina spelling | ✅ Corrected to **Mačina** (previously "Macina") per the 2026-09-22 four-library check |
| 9 | Figures | Still not drawn. `05` §4.2 requires the step-shaped cost of restraint **against** the continuous alternative, with the boundary marked; this appendix supplies the derivation it should render |
