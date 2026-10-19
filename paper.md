# Semantic and Epistemic Governance in Language-Model Reasoning

Timothy O’Brien · ORCID [0009-0001-2589-347X](https://orcid.org/0009-0001-2589-347X). Independent researcher; no institutional affiliation.

Working research draft, 19 October 2026. Not peer reviewed. Copyright 2026 Timothy O’Brien. CC BY 4.0.

## Abstract

A language model can propose a change that achieves a requested goal while altering permissions elsewhere in a rule system. It can also reach a plausible conclusion from evidence that the governing policy does not authorize it to use. These are different errors. We distinguish semantic governance, concerning the admissibility and consequences of changes to a defined representation, from epistemic governance, concerning the admissibility and use of claims under explicit evidence rules. We formulate task-relative contracts for ontology changes, protected queries, authority, provenance, conflict handling and warranted action. We explain how these contracts interact and how model answers can be evaluated while accepting multiple valid witnesses, repairs and investigation plans. The framework draws on established work in ontology evolution, policy analysis, provenance and consistent query answering. Its contribution is an evaluation-oriented synthesis, not a claim to originate those theories or the terms themselves. The framework does not require a particular benchmark result and does not establish real-source truth, autonomous-agent containment or universal governance competence.

## 1. Introduction

Meaning and evidence create different obligations for a model answering a constrained reasoning problem. The first obligation is to understand what the rules permit and what a proposed change would imply. The second is to determine which claims are sufficiently supported to use in a conclusion. A model may satisfy either obligation while failing the other.

Consider a system in which a classification gives permission to perform an operation. Adding one classification edge can make that permission available to a previously ineligible starting profile. The visible goal may be achieved, yet the change may violate a constraint on additional access. Checking only the requested example would miss that consequence.

Now suppose a reviewer receives several reports saying that the change is safe. Their number is not sufficient by itself. Some reports may lack authority for the claim, refer to an old version, or repeat the same original observation. Other eligible reports may conflict. A model must apply a policy for accepting and using claims rather than merely express confidence or uncertainty.

We use semantic governance and epistemic governance as task-relative terms for these two obligations. Both have antecedents in existing research. The purpose is to make their interaction explicit enough to specify reproducible evaluations of language-model answers. The evaluated object is an LLM’s response under a declared input and assistance condition. An external checker, a release system and an autonomous agent are different objects and require different evidence.

The contribution has three parts: a pair of explicit task contracts separating change admissibility from evidence warrant; finite, executable examples showing noncomposing edits, conflicting corroboration and alternative valid answers; and a reporting contract separating answer content, delivery failures and external assistance. These are specifications and checked illustrations, rather than a new ontology logic or a measurement of model performance.

## 2. Intellectual foundations and scope

Ontology-based governance is established work. Calvanese and colleagues govern data-aware processes through an ontology and study verification of properties across evolving states. Their object is a formally specified process, whereas the present framework concerns whether a language model correctly answers a reasoning task about such constraints [1](#ref-calvanese).

Ontology inseparability, conservative extension and logical difference provide ways to compare the consequences of different representations. A benchmark that protects a specified permission query over a fixed finite input basis uses a narrower observable contract. It does not establish preservation of every possible query in an unrestricted ontology language [2](#ref-botoeva).

Provenance research studies how information depends on its origins and transformations. Provenance semirings formalize annotations through query evaluation, while PROV-O supplies a standardized ontology of provenance relationships. Neither the existence of a provenance graph nor the presence of different source names automatically establishes independent, truthful evidence. The policy must specify how those relationships affect acceptance [3](#ref-green), [4](#ref-provo).

Repair-based consistent query answering supplies an established response to inconsistency: preserve admissible consistent alternatives and ask which answers survive them. The choice of repair relation and the decision to reason across all repairs are substantive policy choices. They are not invented by applying them to LLM outputs [5](#ref-arenas).

Formal reasoning benchmarks such as ProofWriter already evaluate implications, proofs and abduction over supplied theories. External correction and behavioral tests also have substantial prior art. The narrower opportunity here is to connect changes in protected consequences with rules for accepting evidence, and to separate those obligations in a precise model-answer evaluation. The synthesis specifies an evaluation contract for model answers, drawing on these complementary methods [6](#ref-proofwriter), [7](#ref-checklist), [8](#ref-critic).

**Table 1. Established foundations and the narrower evaluation scope adopted here.**

| Established foundation | What it supplies | Scope adopted here |
| --- | --- | --- |
| Ontology-based process governance | Formal constraints on evolving data-aware processes | Judge an LLM answer; do not claim process enforcement |
| Inseparability and conservative extension | Compare consequences under a declared query vocabulary | Protect specified queries on a finite input basis |
| Provenance representations | Trace dependencies and transformations of information | Apply an explicit original-leaf corroboration rule |
| Consistent query answering | Retain answers across admissible repairs | State repair policy and compatible completion semantics |
| Formal language reasoning benchmarks | Evaluate consequences and supporting derivations | Distinguish supplied-candidate judgment from construction |
| Correction and behavioral testing | Separate evaluation conditions and sources of feedback | Disclose diagnostic information and stopping assistance |

Two boundaries are especially important. First, preserving a protected permission query on all profiles in a finite basis is not a conservative-extension theorem for an unrestricted ontology. Query selection and the input basis form part of the experimental contract. Second, provenance and authority play different roles. A record of a report's derivation can reveal shared origins, but source eligibility and the required corroboration threshold are additional policy inputs. A provenance formalism does not itself select that policy or establish the reported claim's truth.

The repair literature also makes it necessary to specify which alternatives count. The present examples use deletion-only, inclusion-maximal consistent subsets of supported facts. This instantiates a particular repair relation; it is not an assertion that every consistent-query-answering formalism uses the same one. Likewise, supplying an LLM with a concrete defect or consequence table is a stronger information condition than asking it to reconsider its response. The conceptual synthesis organizes these choices into an evaluation contract. It does not establish priority over the underlying theories, a new account of institutional governance, or the superiority of one normative conflict rule.

## 3. Semantic governance as a change contract

Let a semantic contract specify an initial ontology O, a vocabulary, a set X of admissible starting profiles, permitted changes, requested positive and negative goals, protected queries Q, and an expansion-approval policy. A query’s answer is evaluated under the declared semantics, including any operational treatment of inconsistent profiles.

For a protected query q and a proposed change d, the gain set contains exactly those admissible profiles for which q becomes true after the change and was false before it. Semantic admissibility requires that d can be applied, that every goal is satisfied, and that every protected gain satisfies the approval policy. A no-expansion task requires each gain set to be empty. A contract allowing particular expansions instead requires the corresponding approvals; approval does not make a failed goal correct.

This contract distinguishes the desired effect from allowed side effects. It also fixes the scope of the claim. Checking all subsets of a supplied finite vocabulary can be complete for that basis while saying nothing about new vocabulary, unmodeled relations or an inaccurate domain representation.

More precisely, write $q_O(x)\in\{0,1\}$ for the declared answer to a protected Boolean query on profile $x$, and $O\oplus d$ for an applicable change. Then

$$
G_q(O,d;X)=\{x\in X:q_{O\oplus d}(x)=1\ \land\ q_O(x)=0\}.
$$

If $P_q\subseteq X$ is the set of profile gains authorized for this particular change and version, admissibility requires all requested goals and $G_q(O,d;X)\subseteq P_q$ for every $q\in Q$. No expansion sets each $P_q$ to the empty set. Equality of all before-and-after query answers is stronger: no expansion alone permits losses. Applicability, version binding and any required approval certificate are additional checks; the gain equation does not authenticate them.

### 3.1 Direct, indirect and compositional consequences

An edit need not mention a permission head to change access. A new intermediate classification can connect existing rules. Removing a conflict can also restore an effective permission that was already derivable but suppressed by the conflict policy. The checker must therefore compare consequences rather than search only for syntactically sensitive edits.

Individually admissible changes need not remain admissible together. One change may enable the antecedent used by another. A later change must be evaluated against the relevant current state, or the complete batch must be checked under a contract that permits atomic application. These are different obligations: final-state preservation does not imply preservation at every intermediate prefix.

### 3.2 Constructive answers and counterexamples

A model may be asked to judge a supplied candidate, construct a valid change, or provide a counterexample to a preservation claim. Those tasks should not be treated as interchangeable. A correct judgment does not demonstrate that the model can synthesize a repair, and a valid repair does not prove that it can establish the absence of every counterexample.

When several changes or witnesses satisfy the contract, evaluation should execute and validate the submitted object. Comparing it to one example answer would confuse reference choice with semantic validity. Optimality is an additional requirement only when the task states it and the evaluator can establish it.

### 3.3 Checked example: individually preserving edits with a joint gain

Let the admissible profiles be all four subsets of {a, b}. The initial rules are: a implies m; b implies t; and m together with t implies release. Derivation uses the least forward-chaining closure. Profiles cannot initially contain the intermediate symbols m, t or u. The protected query asks whether release is derived. The original system grants release only to {a, b}.

Consider two additions: the first says a implies u, and the second says u implies t. The first alone leaves every protected answer unchanged. The second alone also preserves every answer, because no admissible profile or original rule supplies u. Together, however, they grant release to {a}. The first supplies u and the second supplies t, while the original rule already supplies m. This exhausts the four-profile basis; the only new gaining profile is {a}.

**Table 2. Exhaustive protected-query answers on the four admissible profiles. Only the joint edit creates a gain.**

| Starting profile | Original | First edit only | Second edit only | Both edits |
| --- | --- | --- | --- | --- |
| Empty | No | No | No | No |
| {a} | No | No | No | Yes |
| {b} | No | No | No | No |
| {a, b} | Yes | Yes | Yes | Yes |

Thus query preservation of separately checked edits does not compose automatically. This example concerns preservation alone; it does not claim that each edit satisfies an additional, unspecified positive goal. If the declared goal is to grant release to {a}, the combined edit meets that goal but fails a no-expansion contract. A different contract could permit exactly that gain through a valid approval. Those are two different policies applied to the same consequences, rather than two competing answers to one fixed task.

## 4. Epistemic governance as an evidence-use contract

Epistemic governance specifies which claims may be accepted and used for a particular purpose. This differs from generic reasoning about uncertain information. The contract can restrict source authority by claim and task, bind reports to current versions, require independent corroboration, and prescribe how conflicts are handled.

Let the evidence policy map a packet E to supported claims and a family of admissible consistent interpretations. A repair is one such interpretation under the chosen repair rule. Inclusion-maximal repairs contain every supported fact that can be added consistently; they need not contain the greatest number of facts. Other repair policies are possible and would define different tasks.

Each repair may leave facts unsettled. Consider all compatible completions across all repairs. An action is warranted allow when its release predicate is true in every admissible completion; warranted deny when false in every completion; otherwise the conclusion is undetermined. The admissible-world set must be nonempty, or the contract must explicitly define how an empty set is handled. Vacuous universal truth must not silently authorize an action.

Undetermined is not a denial. Operationally a system might hold both, but an evaluation must distinguish insufficient evidence from evidence establishing that release is impermissible. Similarly, an unsupported approval can be an epistemic error even when the unobserved underlying state would happen to allow the action.

For the deletion-only policy used here, let $S(E)$ be the finite set of supported Boolean literals, $T$ the fixed integrity constraints, and $\operatorname{Mod}_T(R)$ the Boolean worlds satisfying $T$ and every literal in $R$. Define

$$
\mathcal R(E)=\max_{\subseteq}\{R\subseteq S(E):\operatorname{Mod}_T(R)\ne\varnothing\},
\qquad
W(E)=\bigcup_{R\in\mathcal R(E)}\operatorname{Mod}_T(R).
$$

Here maximality is by set inclusion. For nonempty $W(E)$ and action predicate $r_a$, the decision is allow if $r_a$ holds in every world, deny if it holds in none, and undetermined otherwise. Consistent $T$ guarantees at least the empty supported subset has a completion; inconsistent $T$ requires an explicit failure policy. These definitions separate report admission, repair selection and action evaluation, and make no probability assignment to worlds.

### 4.1 Authority, provenance and truth

Authority is task-relative eligibility to supply a claim; it is not a measured probability of truth. A source may be authorized for one fact and not another. Provenance records how a report depends on earlier observations; different speakers can share an origin. Requiring mutually disjoint original observations is one explicit corroboration policy, not a universal definition of independence.

The policy cannot discover every lie from its internal structure alone. If all authorized reports consistently support a false claim and the supplied provenance contains no detectable defect, compliance with the contract need not reveal that external falsehood. An evaluation under this contract measures application of supplied authority and evidence rules, not the real-world reliability of those inputs.

### 4.2 Choosing further evidence

When an action remains undetermined, a model can be asked to choose a useful observation or a contingent investigation. The objective must be specified. Minimizing the worst number of unresolved actions and then worst total effort is different from maximizing expected information gain.

An investigation plan can be evaluated as a finite mathematical object. Its branches must correspond to attainable observations; prerequisites must hold where a query is used; and the claimed objective must be achieved. Generating that object is still an LLM reasoning task. It is not evidence that an autonomous agent can collect the observations, authenticate them or execute the resulting action safely.

### 4.3 Checked example: corroboration, conflict and warranted action

Let p denote verified authorization and c a confidentiality restriction. The integrity rule forbids p and c together. Each positive claim requires two current authorized reports whose sets of original observation leaves are disjoint. This is an illustrative contract: all five reports below are stipulated to satisfy the authority, scope and version checks.

**Table 3. Illustrative supported claims and original observation leaves. All reports pass the stipulated authority and version checks.**

| Report | Claim | Original observation leaves |
| --- | --- | --- |
| r1 | p | {o1, o2} |
| r2 | p | {o2, o3} |
| r3 | p | {o4} |
| r4 | c | {o5} |
| r5 | c | {o6} |

Reports r1 and r2 do not meet the stipulated disjoint-origin corroboration rule for p: they share o2. Report r3 supplies a disjoint original-observation set under that rule. Either {r1, r3} or {r2, r3} meets the quorum for p; {r4, r5} meets it for c. The supported fact set is therefore {p, c}, despite its inconsistency. Support admission and conflict resolution are separate stages of this policy.

The inclusion-maximal consistent repairs are {p} and {c}. Completing them under the integrity rule gives exactly two worlds: p true with c false, and p false with c true. Suppose release requires p and absence of c, override requires both p and c, and retain requires at least one of them. The warranted decisions are respectively undetermined, deny and allow. Returning allow for release would overlook an admissible world; returning undetermined for override would overlook that the integrity rule rules it out in every world.

One unit-cost observation of p resolves the only unresolved action. On its true branch release becomes allow; on its false branch release becomes deny. An observation of c achieves the same objective. Both one-query plans are optimal for minimizing unresolved actions first and worst path effort second: they achieve zero unresolved actions at effort one, whereas a zero-query plan leaves release unresolved. The observation filters the existing two worlds; it does not recompute repairs from an altered report set. Accepting either optimal query avoids making the evaluator's arbitrary reference choice part of the task.

Removing r3 illustrates another policy consequence. Then p lacks the required corroboration, while c remains supported. The only repair is {c}, and release becomes deny. Adding the report with a disjoint origin moves that answer to undetermined by admitting a conflicting alternative. Adding supported evidence can therefore revoke a warranted denial and increase indeterminacy under this repair policy; this example does not show withdrawal of an existing allowance.

Maximality must also remain distinct from maximum size. For a separate supported set {p, c, d}, suppose p conflicts with c and with d, while c and d are compatible. The inclusion-maximal repairs are {p} and {c, d}. A maximum-cardinality policy keeps only {c, d}; an inclusion-maximal policy keeps both. A decision depending on p can consequently differ. Neither policy may be substituted for the other after seeing a model's answer.

## 5. How the two obligations interact

The semantic question asks what follows from the represented rules and changes. The epistemic question asks what the authorized evidence warrants concluding about those conditions. Correct representation does not guarantee correct evidence use, and correct evidence use does not guarantee a valid change.

**Table 4. Logical separation of semantic change validity and warrant of an asserted eligibility claim. Every answer affirmatively asserts eligibility; these are conceptual possibilities, not model results.**

| Semantic change | Asserted eligibility | Interpretation |
| --- | --- | --- |
| Valid | Warranted | The proposed change and the affirmative eligibility claim satisfy their respective contracts |
| Invalid | Warranted | A warranted eligibility claim does not rescue an invalid proposed change |
| Valid | Unsupported | The change satisfies its contract, but the affirmative eligibility claim lacks the required support |
| Invalid | Unsupported | The proposed change is invalid and the affirmative eligibility claim is unsupported |

The table defines possibilities rather than reporting model observations. An evaluation can instantiate them with independently checked examples. A combined end-to-end task would require an additional specification connecting actual proposed changes to evidence selection and use. Results from separate semantic and epistemic tracks do not automatically establish competence on that combined task.

For a minimal four-cell construction, use the semantic example above and require the already satisfied goal that {a} derives m. An empty change is semantically valid; the combined change is invalid under no expansion. Separately, let a review-eligibility claim require two current, authorized, disjoint-origin reports. In every cell, consider an answer that proposes the indicated change and affirmatively asserts review eligibility. A packet containing the required report pair warrants that assertion; a packet containing only one report leaves eligibility undetermined, so the affirmative assertion is unsupported. Correctly returning undetermined for the one-report packet would satisfy the epistemic contract: insufficient evidence alone is not an evidence-use error. Pairing either proposed change with either evidence packet, while keeping the affirmative eligibility assertion fixed, realizes the four cells under one fixed pair of contracts. Eligibility remains a separate claim: two eligible reports do not prove that every protected semantic query was preserved. This construction illustrates the logical separation of obligations rather than measuring a model on a new joint task.

## 6. Evaluating language-model answers

An empirical protocol should fix the task version, input unit, model/provider, output contract, reasoning condition, resource allowance and assistance available before measuring outcomes. Complete-answer accuracy and component accuracy answer different questions. A correct release decision can conceal an incorrect explanation of the evidence; a partly correct explanation can still be insufficient to justify release.

Delivery errors, resource failures and substantive reasoning errors should remain distinguishable. A code-fenced answer rejected by a bare-JSON contract is not proof that its logical content is wrong. Conversely, extracting a useful object after observing results is a new reporting sensitivity analysis, not the original primary score. Token exhaustion remains a failure under the declared allowance but should not be described as the same mechanism as a completed invalid witness.

### 6.1 Feedback and correction

An unaided first answer, revision after an error notification, and revision after a diagnostic are separate conditions. An error-only message can tell the model that something is wrong without identifying a field or counterexample. A diagnostic provides additional information, potentially enough to resolve a substantial part of the problem. Its information content should be reported rather than described vaguely as reflection.

External reference-guided stopping is assistance in experimental control. Carrying a correct answer forward to later checkpoints creates cumulative retained success, not a fresh correct judgment at every checkpoint. Models initially at ceiling supply no failure-eligible correction trials under that procedure. Previous research already distinguishes intrinsic correction from tool-assisted revision; the present framework requires those differences to remain visible in governance measurements [9](#ref-huang), [8](#ref-critic).

**Table 5. Revision conditions supply different information. Equal revision counts do not equalize assistance.**

| Revision condition | New information supplied | Interpretation |
| --- | --- | --- |
| Reconsideration | A fixed request to revisit the answer | Another response conditioned on the earlier answer and revision instruction |
| Error notification | The answer violates the task contract | A correctness signal, without a localized diagnosis |
| Bounded diagnostic | A specified failed obligation or invalid certificate property | Assisted revision with disclosed diagnostic content |
| Full reference consequence information | Computed consequences or a complete solution certificate | A stronger oracle-assisted condition |

These conditions require separate histories from the same first answer to support a paired comparison. Equal numbers of permitted revisions do not equalize the information supplied. Reference-guided stopping can be used in each arm, but reached calls, eligible original failures, regressions and cumulative retained success must remain visible.

### 6.2 Difficulty and independent evidence

Longer prompts and more entities do not by themselves establish qualitatively harder reasoning. Global coupling, the need to establish absence of a counterexample, dense source dependence and contingent choices provide more precise construction dimensions. Their empirical difficulty still depends on the sampled instances and model condition.

Benchmarks developed after observing failures should disclose that adaptation. Fresh instances from a selected family can support prospective within-family evaluation once the protocol is frozen, but do not erase the development history. Paired task views, source contexts and presentation orders must be grouped by their underlying system when estimating uncertainty.

## 7. Limitations and research obligations

The formal contract is an abstraction. Its vocabulary, authority facts, admissible worlds, conflict policy and protected queries may omit important real conditions. The distinction between semantic and epistemic obligations is analytically useful but does not supply a complete social or institutional theory of governance. Its terminology is not asserted to be new.

Independent evaluators can still share a mistaken interpretation of the written task. Tests should accept alternate valid solutions and reject deliberately invalid certificates, while reviewers examine the specification and construction separately. Synthetic benchmark compliance cannot establish general source trust, practical authorization security or agent containment.

The running examples have executable exhaustive checks over their stated finite domains. This establishes the illustrated consequences under the chosen contracts, not external validation of those contracts. The related-work comparison identifies the established theories being instantiated; independent specialist review is still needed to assess the synthesis and formal presentation. Its conceptual argument does not depend on a benchmark beating a particular model, and perfect performance on one finite task does not invalidate the distinction.

## 8. Conclusion

Semantic and epistemic governance can be expressed as different task-relative obligations: preserve the permitted consequences of a change, and use claims only as the evidence contract warrants. Their interaction helps explain why a model may reach a plausible answer without satisfying the whole task. Explicit contracts make those errors assessable while preserving legitimate alternative solutions. They also make the limits of an empirical claim visible.

## Data and code availability

This conceptual paper introduces no new model measurements. The executable examples and recorded results accompany the manuscript in the [foundations supplementary package](https://github.com/prosessleder/semantic-epistemic-governance-foundations-preprint). The checker enumerates closures, disjoint-origin report sets, repairs, worlds, decisions and tied optimal observations. The preserved original fixtures are accompanied by a separately versioned supplemental checker for the four-cell answer construction, the removal-of-report case, observation branches and the nonempty-world guard. These fixtures do not add to or alter a benchmark.

## Author contributions and AI assistance

Timothy O'Brien is the sole author and conducted this work independently, without institutional affiliation. OpenAI Codex assisted literature discovery, implementation, checking and manuscript drafting. The author is responsible for the specification, interpretation, references and conclusions. Automated checking of examples does not replace independent scientific review.

## Funding

This research received no external funding.

## Competing interests

The author declares no competing interests.

## References

<a id="ref-calvanese"></a>
[1] D. Calvanese, G. De Giacomo, D. Lembo, M. Montali and A. Santoso. Ontology-Based Governance of Data-Aware Processes. In *Web Reasoning and Rule Systems (RR 2012)*, LNCS 7497, pp. 25-41, 2012. [Source](https://www.inf.unibz.it/~calvanese/papers/calv-etal-RR-2012.pdf).

<a id="ref-botoeva"></a>
[2] E. Botoeva, B. Konev, C. Lutz, V. Ryzhikov, F. Wolter and M. Zakharyaschev. Inseparability and Conservative Extensions of Description Logic Ontologies: A Survey. arXiv:1804.07805v1, 2018. [Source](https://arxiv.org/abs/1804.07805v1).

<a id="ref-green"></a>
[3] T. J. Green, G. Karvounarakis and V. Tannen. Provenance Semirings. In *Proceedings of PODS*, pp. 31-40, 2007. doi:10.1145/1265530.1265535. [Source](https://www.cs.ucdavis.edu/~green/papers/pods07.pdf).

<a id="ref-provo"></a>
[4] T. Lebo, S. Sahoo and D. McGuinness (eds.). PROV-O: The PROV Ontology. W3C Recommendation, 30 April 2013. [Source](https://www.w3.org/TR/2013/REC-prov-o-20130430/).

<a id="ref-arenas"></a>
[5] M. Arenas, L. Bertossi and J. Chomicki. Answer Sets for Consistent Query Answering in Inconsistent Databases. *Theory and Practice of Logic Programming* 3(4-5), pp. 393-424, 2003. doi:10.1017/S1471068403001832. Author preprint: arXiv:cs/0207094, 2002. [Source](https://arxiv.org/abs/cs/0207094).

<a id="ref-proofwriter"></a>
[6] O. Tafjord, B. Dalvi and P. Clark. ProofWriter: Generating Implications, Proofs, and Abductive Statements over Natural Language. In *Findings of ACL-IJCNLP*, pp. 3621-3634, 2021. doi:10.18653/v1/2021.findings-acl.317. [Source](https://aclanthology.org/2021.findings-acl.317/).

<a id="ref-checklist"></a>
[7] M. T. Ribeiro, T. Wu, C. Guestrin and S. Singh. Beyond Accuracy: Behavioral Testing of NLP Models with CheckList. In *Proceedings of ACL*, pp. 4902-4912, 2020. doi:10.18653/v1/2020.acl-main.442. [Source](https://aclanthology.org/2020.acl-main.442/).

<a id="ref-critic"></a>
[8] Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, N. Duan and W. Chen. CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing. *ICLR*, 2024. Author preprint: arXiv:2305.11738v4. [Source](https://arxiv.org/abs/2305.11738v4).

<a id="ref-huang"></a>
[9] J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. Yu, X. Song and D. Zhou. Large Language Models Cannot Self-Correct Reasoning Yet. *ICLR*, 2024. [Source](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html).
