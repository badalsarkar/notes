# Context Management Across the AI-DLC Stages

Research report, November 2026. Related notes:
[aidlc-context-management.md](aidlc-context-management.md),
[sdlc-context-graph.md](sdlc-context-graph.md), [ai-dlc.md](ai-dlc.md),
[specification-driven-development.md](specification-driven-development.md), [Knowledge graphs for
coding agents](knowledge-graphs-for-coding-agents.md).

## Contents

- [1. What this report covers](#1-what-this-report-covers)
- [2. Summary](#2-summary)
- [3. Evidence labels and source limits](#3-evidence-labels-and-source-limits)
    - [3.1 Evidence labels](#31-evidence-labels)
    - [3.2 How the sources were read](#32-how-the-sources-were-read)
    - [3.3 Corrections carried forward](#33-corrections-carried-forward)
- [4. Coverage review](#4-coverage-review)
- [5. Changes to the existing notes](#5-changes-to-the-existing-notes)
- [6. Stage-by-stage specification](#6-stage-by-stage-specification)
    - [6.1 Requirements stage context](#61-requirements-stage-context)
    - [6.2 Design stage context](#62-design-stage-context)
    - [6.3 Implementation stage context](#63-implementation-stage-context)
    - [6.4 Test and review stage context](#64-test-and-review-stage-context)
    - [6.5 Operations feedback context](#65-operations-feedback-context)
    - [6.6 Side-by-side summary of the stages](#66-side-by-side-summary-of-the-stages)
- [7. Cross-stage model](#7-cross-stage-model)
    - [7.1 Evidence on stage handoffs](#71-evidence-on-stage-handoffs)
    - [7.2 Artefact identity and versioning](#72-artefact-identity-and-versioning)
    - [7.3 Lineage links](#73-lineage-links)
    - [7.4 Supersession](#74-supersession)
    - [7.5 Staleness propagation](#75-staleness-propagation)
    - [7.6 Where artefacts live](#76-where-artefacts-live)
- [8. Retrieval design](#8-retrieval-design)
    - [8.1 Context assembly per stage](#81-context-assembly-per-stage)
    - [8.2 Validity filtering](#82-validity-filtering)
    - [8.3 Source precedence](#83-source-precedence)
    - [8.4 Conflict handling](#84-conflict-handling)
- [9. Option comparisons](#9-option-comparisons)
    - [9.1 Requirement record format](#91-requirement-record-format)
    - [9.2 Artefact storage](#92-artefact-storage)
    - [9.3 Specification lifecycle](#93-specification-lifecycle)
    - [9.4 Retrieval mechanism](#94-retrieval-mechanism)
    - [9.5 Implementation session record](#95-implementation-session-record)
    - [9.6 Conflict policy](#96-conflict-policy)
- [10. Capital markets illustrations](#10-capital-markets-illustrations)
- [11. Regulatory position](#11-regulatory-position)
- [12. Measurement plan](#12-measurement-plan)
- [13. Build order](#13-build-order)
- [14. Open decisions](#14-open-decisions)
- [Resources](#resources)

## 1. What this report covers

- The question is what an AI-DLC platform should record as context at each stage of the software
  development lifecycle, how it should record that context, and how later stages should retrieve it
  so that quality stays high.
- The report also states whether the earlier research covered this problem and what it missed.
  Section 4 answers that question, and section 5 lists the places where the new evidence changes the
  existing notes.
- The report rests on four new research notes:
  [requirements](research_notes/AIDLC%20context%20across%20SDLC%20stages/requirements_stage_context.md),
  [design](research_notes/AIDLC%20context%20across%20SDLC%20stages/design_stage_context.md),
  [handoffs, traceability and
  drift](research_notes/AIDLC%20context%20across%20SDLC%20stages/handoffs_traceability_drift.md),
  and [stage retrieval, feedback and
  evaluation](research_notes/AIDLC%20context%20across%20SDLC%20stages/stage_retrieval_feedback_evaluation.md).
- It does not repeat three bodies of existing material, and it links to them instead.
    - [aidlc-context-management.md](aidlc-context-management.md) covers the stores, the context
      patterns and the resume protocol around AWS AI-DLC.
    - [sdlc-context-graph.md](sdlc-context-graph.md) covers code graphs, work graphs and business
      ontologies.
    - [Knowledge graphs for coding agents](knowledge-graphs-for-coding-agents.md) covers
      code retrieval at the scale of one million lines and the commercial context engines.

## 2. Summary

- **Coverage.** The earlier research covered the system around the stores well, but it did not
  specify stage-by-stage content, and it did not cover requirement quality, per-artefact identity,
  validity filtering, implementation outputs or the promotion of learned rules in any depth.
- **What to record.** Later stages depend most on material that they cannot reconstruct from code.
  This conclusion is an inference, because no study ranks these items by value.
    - Requirements should record normative statements, acceptance conditions, exclusions,
      assumptions, open questions, regulatory interpretations and verbatim sources.
    - Design should record decisions, rejected alternatives, constraints and revisit conditions,
      together with machine-checkable contracts.
    - Implementation should record decisions, deviations and machine-produced test evidence, and it
      should retain raw transcripts as evidence that later stages do not load by default.
    - Test and review should record which tests fail when a requirement is violated, and what each
      reviewer actually saw.
    - Operations should record observations that are routed to a test, a requirement or a candidate
      rule, and that do not become instructions without review.
- **How to record it.** The recommended design gives each artefact a stable identifier, a content
  digest, an origin, an approval bound to that digest, and links that name the upstream digest from
  which it was derived. This entire model is a proposal, because no tool reviewed implements it and
  no study has tested it.
- **How to retrieve it.** The recommended design applies deterministic filters for entitlement,
  validity and scope before any relevance ranking, pushes the items linked by identifier, and offers
  search only for optional material.
    - The evidence for this design is indirect. Re-rankers prefer older and richer documents ([An et
      al.](https://arxiv.org/abs/2604.14227), abstract), and the best model reached 55.2% accuracy
      at recognising stale memories ([STALE](https://arxiv.org/abs/2605.06527), as recorded in
      [sdlc-context-graph.md](sdlc-context-graph.md) section 7).
    - In a preprint with synthetic conflicts, 90.1% of agent choices followed a stale instruction
      file. Claude Code flagged the conflict in 79 of 80 runs and still followed the file ([Xu and
      Wu](https://arxiv.org/abs/2610.30571)). A flag from the agent therefore cannot serve as the
      control, and the engine must act on the conflict.
- **Where the evidence is strongest.** Two results have the most direct bearing on quality, and both
  come from small tasks.
    - Defective requirements reduce generated-code correctness. Injected ambiguity reduced Pass@1 by
      an average of 7.22 points and at most 32.35 points on function-level tasks
      ([Orchid](https://arxiv.org/html/2604.21505v2)).
    - Giving a test-writing agent the specification produced correct code 36 to 38 points more often
      on Claude models, while doubling the test budget barely helped ([Haeri and
      Ghelichi](https://arxiv.org/abs/2607.06636), abstract). The benefit disappeared on
      well-specified algorithmic problems.
- **Where evidence is absent.** No study was found on any of the following points, so every related
  recommendation in this report is a proposal.
    - No study compares EARS, Gherkin, user stories and structured data as inputs to code
      generation.
    - No controlled study compares stage-scoped context with unscoped context.
    - No study measures information loss per handoff, or how often specifications go stale.
    - No controlled study covers approval gate placement or reviewer fatigue over generated
      artefacts.
    - No evidence specific to capital markets was found, and no published outcome study of AI-DLC
      was found.
- **Regulation.** No text read in this research sets a rule specific to AI-generated code. Section
  11 states which texts were confirmed and which need compliance review.
- **Recommended first steps.** The state-model and loaded-context fixes from
  [aidlc-context-management.md](aidlc-context-management.md) section 11 should come first.
  Identifiers and digests should follow on one bounded domain, and then the requirement-to-test
  link, because it is the point where the published evidence suggests that assembly may pay back
  most. Section 13 gives the full order.

## 3. Evidence labels and source limits

### 3.1 Evidence labels

- This report separates three kinds of statement, and every substantive claim carries one of the
  labels below.

| Group | Label | Meaning |
|---|---|---|
| Independent evidence | **[Independent]** | Research by authors with no stake in the tool under study. Most of these papers are unreplicated preprints. |
| Vendor-reported or self-reported claims | **[Vendor]** | A party reporting on its own product, documentation or template, including research by a company's own staff (shown as Vendor-affiliated). A template shows what a tool is designed to do and does not show that it works. |
| Vendor-reported or self-reported claims | **[Own-method]** | Research in which authors evaluate their own method or framework, including peer-reviewed work. |
| Vendor-reported or self-reported claims | **[Practitioner]** | An individual or project account, usually without measured outcomes. |
| Design proposals and inferences | **[Proposal]** | A schema, matrix, ladder, ordering or inference made by the researchers or by this report. None of these has been tested unless the text says so. |

- Reading depth appears in parentheses where it is limited. "Abstract" means that only the abstract
  or landing page was read, "excerpt" means that keyword-targeted passages were read, "snippet"
  means that the claim rests on a search-result summary and should be verified before it is relied
  on, and "secondary" means that a write-up was read rather than the primary source.

### 3.2 How the sources were read

- **Requirements note.** Pages were downloaded with curl because WebFetch was unavailable. Tool
  templates were read closely from their `main` branches, and papers were read through
  keyword-targeted excerpts rather than from start to finish.
- **Design note.** WebFetch failed on every domain tried, and no full paper or documentation page
  was read. Every finding in that note rests on an arXiv abstract or a search summary, and the
  primary templates for Kiro, Spec Kit and AI-DLC's design outputs remain unconfirmed.
- **Handoffs note.** Some primary pages were read directly, including MAST, SR 26-2 and RTS 6, but
  EUR-Lex returned empty responses and PCAOB refused the request. The official BMAD repository was
  not read, so BMAD details come from third-party mirrors and may differ by version.
- **Retrieval and evaluation note.** Many studies were read only as abstracts or search excerpts.
  The longitudinal ESEM 2026 study of 669 developers could not be fetched, so its findings are
  unknown. The full DORA 2025 report was not read, and the note did not re-read the Khatri ablation
  (arXiv 2607.27250).
- **Limits that apply to the whole evidence base.**
    - Most papers are preprints, and several evaluate models that are no longer current.
    - Most requirement-quality tasks are function-level or small applications, and their defects are
      usually injected rather than naturally occurring.
    - All temporal retrieval benchmarks derive from Wikipedia, Wikidata or general knowledge, and
      none uses requirements, ADRs or firm policy.
    - The memory studies use puzzle, web and application tasks, and none uses coding-agent
      transcripts in a delivery workflow.

### 3.3 Corrections carried forward

The research notes corrected several circulating figures. These corrections should apply wherever
the figures are reused.

| Item | Correct reading | Do not use |
|---|---|---|
| MAST inter-agent misalignment share | Summing the published modes gives about 32.4%, with about 44.2% for system design and 23.5% for verification ([MAST](https://arxiv.org/html/2503.13657v3)). A search summary gives 32.3%. | The secondary figures of 31% and about 37%. |
| MAST failure rates | The 41% to 86.7% range is not comparable across systems, because the benchmarks differ. | The range as a cross-system ranking. |
| "61% of agent PRs unreviewed" | 61.38% applies to 33,596 agent PRs in repositories with 100 or more stars. In repositories with both kinds of PR, 28.92% of agent PRs and 34.52% of human PRs had no recorded review, and human-only review was 8.08% against 25.21% ([Duma et al.](https://arxiv.org/html/2605.02273)). PRs without comments count as unreviewed, and size and complexity are not controlled. | The 61% figure as a contrast with human work. |
| Mixed review share in Duma et al. | The table and arithmetic give 31.09%. | The 40.34% in the paper's text. |
| LiSSA requirements-to-code output | The figures of about 0.18 precision and 0.38 recall are a sample output in its documentation ([LiSSA](https://helmholtz.software/software/lissa)). | Those figures as a benchmark result. |
| Orchid maximum Pass@1 drop | The v2 paper gives 32.35 points ([v2](https://arxiv.org/html/2604.21505v2)), and v1 reportedly gives 31.10 (snippet). | An unversioned maximum. |
| Contradictory requirements in arXiv 2507.20439 | The paper reports GPT-4 falling from 73.8% to 6.7% on contradictory HumanEval tasks, which is larger than its own summary figure ([paper](https://arxiv.org/html/2507.20439)). | "Up to 40%" as the upper bound. |
| Larsen and Moghaddam | The paper is at SEAA 2026. The 6.7% fall in smell density is a denominator effect, because raw smell counts were flat and lines of code grew 12.8% ([record](https://arxiv.org/abs/2606.13298)). | "MSR 2026", or the density fall as an improvement. |
| Faros figures | The incidents-per-PR figure comes from [Faros](https://faros.ai/blog/ai-acceleration-whiplash-takeaways), which publishes no baselines or statistical tests and sells this kind of measurement. | The attribution of that figure to DORA 2025. |
| RTS 6 Article 28 | Article 28(3) sets a five-year period for high-frequency trading order records ([text](https://www.legislation.gov.uk/eur/2017/589/article/28/adopted)). | Article 28 as a general algorithm record rule. |
| Figures without a traceable source | The LinearB merge-rate figures, the KushoAI drift figures and the Medium post's 88% C4 accuracy could not be traced to a method or primary report. | All three of these figures. |
| AI-DLC requirements path | The path `aidlc-rules/aws-aidlc-rule-details/...` now returns 404, and the current rule is under [core/aidlc-common](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md). | Write-ups that describe the old layout as current. |

## 4. Coverage review

The earlier research did not answer this question directly. It described how context reaches an
agent and how stores should be governed, but it treated a stage mainly as a loading scope and did
not specify what each stage must produce for the next one.

| Problem area | Earlier research and user notes | Status | What this round added |
|---|---|---|---|
| Categories of context, stores and owners | [aidlc-context-management.md](aidlc-context-management.md) sections 3 and 9.2 | Covered | No change to the categories, and a resolved storage proposal in section 7.6. |
| Code retrieval at scale | [Knowledge graphs for coding agents](knowledge-graphs-for-coding-agents.md) and [sdlc-context-graph.md](sdlc-context-graph.md) section 6 | Covered | Nothing new. This report reuses those findings. |
| Workflow state and resume | [aidlc-context-management.md](aidlc-context-management.md) sections 4.5 and 9.6 | Covered | Nothing new. Approval binding to a digest extends the state split. |
| What each stage must record | Lists of AI-DLC artefacts and specification contents only | Missed as a per-stage specification | Section 6, including a comparison of tool templates. |
| Requirement quality and code correctness | [specification-driven-development.md](specification-driven-development.md) section 7.1 cites survey results | Partly covered | Orchid, arXiv 2507.20439 and the requirement smell study. |
| Clarification and ambiguity detection | Elaboration treated as valuable, without evaluation | Missed | ClarifyGPT, ClarifyCodeBench, and detection limits of about 47% recall and 50% precision. |
| Requirement notation | EARS described as the highest-value technique | Covered with unsupported confidence | No comparative study exists. See section 5. |
| Source-to-requirement provenance | Named as a need in general terms | Missed | LENS, Inter2US, and the separation of faithfulness from coverage. |
| Design rationale and capture | ADRs recommended without evidence | Partly covered | Rule study by Cai et al., Zhou et al. on LLM rationale, and GADR on transcript extraction. |
| Conformance and drift | Drift named as the main failure, with a hook example | Partly covered | Layered enforcement, Xu and Wu, and the distinction among reference, structural and behavioural checks. |
| Artefact identity and versioning | ReqToCode and the graph-shaped reading of AI-DLC | Partly covered | A survey of tool identifiers and the digest-link proposal. |
| Handoff loss and contracts | Cognition and Anthropic positions on subagents | Partly covered | MAST, MetaGPT, and a statement that no direct measurement exists. |
| Stage-specific denial | Per-stage allow-list manifest in section 9.3 of the context note | Missed | A deny matrix, of which only a few cells have support. |
| Validity against relevance | Freshness metadata and a date shown to the agent | Partly covered | Re-ranker bias, HoH, and validity as a hard filter with an as-of date. |
| Agent behaviour under conflict | STALE recorded | Partly covered | Xu and Wu, and an explicit precedence design. |
| Implementation outputs for later stages | Decision log and AI-DLC diary | Partly covered | Raw retention with target-bound delivery, deviations as records, and agent claims separated from evidence. |
| Feedback and promotion | AI-DLC learning loop and Copilot memory | Partly covered | A promotion ladder, mining conventions, poisoning evidence, and incident routing. |
| Per-stage evaluation | Section 9.9 of the context note, covering efficiency measures | Partly covered | ID-based retrieval metrics, seeded faults, and randomisation of context configuration. |
| Human review placement | Review named as the constraint | Partly covered | Anchoring evidence, a gate priority proposal, and a statement that no controlled study exists. |
| Regulation | Brief treatment, with SR 26-2 unconfirmed in the earlier report | Partly covered and partly unverified | Primary confirmation of SR 26-2 and of RTS 6 through UK copies, and an explicit list of unconfirmed texts. |

## 5. Changes to the existing notes

The existing notes were treated as read-only and were not edited. The table lists changes the user
may wish to make. "Contradicted" means the new evidence conflicts with the statement, "qualified"
means the statement needs a limit, and "to check" means that the writer could not settle the point.

| Location | Current statement | New evidence or finding | Status |
|---|---|---|---|
| [specification-driven-development.md](specification-driven-development.md) sections 3.3 and 7.1 | EARS is "the single highest-value technique", and "constrained requirement syntax works". | Two targeted searches found no LLM evaluation of EARS, and no study compares notations ([requirements note](research_notes/AIDLC%20context%20across%20SDLC%20stages/requirements_stage_context.md) section 2). EARS remains a reasonable default, but its adoption by Kiro is a product decision. | Contradicted as a ranking |
| [specification-driven-development.md](specification-driven-development.md) section 8 | An agent executes a stale document "and does not flag the mismatch". | Claude Code flagged the conflict in 79 of 80 runs and still followed the file ([Xu and Wu](https://arxiv.org/abs/2610.30571)). Agents may flag the conflict, and the harm arises because they proceed. | Contradicted in detail |
| [specification-driven-development.md](specification-driven-development.md) section 8 | Reviewer fatigue leads to rubber-stamping. | The notes found no controlled study of fatigue over generated artefacts, so this remains a practitioner report. | Qualified |
| [specification-driven-development.md](specification-driven-development.md) section 7.3 | The arXiv 2606.30689 trade-off is presented as a main result. | The figures match, but the study is the framework's own evaluation, reportedly by a single author, and it was read only as an abstract. | Qualified |
| [aidlc-context-management.md](aidlc-context-management.md) section 9.5 | A verification date lets the agent treat older items with caution. | STALE, Xu and Wu, and the re-ranker results show that agent caution is not a reliable control. The date remains useful to reviewers, and validity should be filtered before the agent sees the item. | Qualified |
| [aidlc-context-management.md](aidlc-context-management.md) section 9.5 | Agent memories expire if unused, following Copilot. | This suits agent memories but not approved controls, because an absence of failures may mean that a rule is working ([BMAD](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/), Practitioner). | Qualified |
| [aidlc-context-management.md](aidlc-context-management.md) section 9.3 | Each manifest carries a token budget per tier. | No published stage budget was found, so any figure is a starting assumption. The manifest also needs mandatory and optional classes and a deny list. | Qualified and extended |
| [aidlc-context-management.md](aidlc-context-management.md) section 9.4 | Elaboration answers are extracted into knowledge items. | Oracle clarification falls slightly below a complete requirement ([ClarifyCodeBench](https://arxiv.org/html/2607.00711v2)), which suggests that answers should also be merged into the normative requirement. This reading is indirect. | Extended |
| [aidlc-context-management.md](aidlc-context-management.md) section 9.9 | Cited or used items estimate precision. | Without-reference measures do not penalise an agent that ignored a key policy, so they are online proxies only. ID-based precision and recall should be primary. | Qualified |
| [aidlc-context-management.md](aidlc-context-management.md) sections 4.3 and 4.5 | AI-DLC has 126 event types and 32 stages. | The README at badge version 2.11.2 advertises a 131-event audit trail and 33 stages ([aidlc-workflows](https://github.com/awslabs/aidlc-workflows), Vendor). The version has moved since October. | To update |
| [aidlc-context-management.md](aidlc-context-management.md) section 7.1 | Developer-written files add about four points, Lulla reports 20.1% fewer mean output tokens, and the ablation had 288 runs. | The [earlier report](knowledge-graphs-for-coding-agents.md) gives a non-significant +2.4 points from Gloaguen v3, 16.58% fewer output tokens from Lulla, and 291 runs from Khatri. The new notes did not re-read these papers, so the writer cannot say which is correct. | To check |
| [sdlc-context-graph.md](sdlc-context-graph.md) section 7 | A stale graph is worse than no graph. | Outdated passages do mislead models ([HoH](https://aclanthology.org/people/jie-ouyang/), snippet), but no study compares a stale artefact with a missing one. The vendor statement on ADRs is also unmeasured. | Qualified |
| [sdlc-context-graph.md](sdlc-context-graph.md) section 8 | EU AI Act high-risk obligations under Annexes I and II take effect on 2 August 2026. | The new research did not investigate this claim, and it remains unverified. See section 11. | To check |
| [ai-dlc.md](ai-dlc.md) section 7.3 | METR's follow-up estimated "18% slower" on an interval "from 38% slower to 9% faster", and "4% slower" for new recruits. | The research note records these as −18% time (CI −38% to +9%) and −4% time (CI −15% to +9%), meaning less time taken, and METR believes developers are probably faster, on very weak evidence ([METR](https://metr.org/blog/2026-02-24-uplift-update/)). The direction in the note appears reversed. Both intervals include zero. | Contradicted, and to check against METR |
| [Knowledge graphs for coding agents](knowledge-graphs-for-coding-agents.md), persistent context section | SR 26-2's treatment of generative AI was not checked in primary form. | Footnote 3 is now confirmed from the primary text. The inference about SDLC controls remains an inference. See section 11. | Updated |
| [ai-dlc.md](ai-dlc.md) section 8.3 | Expect model risk questions. | This remains sensible, but SR 26-2 excludes generative and agentic models from its scope and addresses a bank's models rather than change control for a coding tool. | Qualified |

## 6. Stage-by-stage specification

- Each stage below uses the same ten items. The first nine are the specification, and the tenth
  states what supports it.
- **The specification as a whole is a [Proposal].** Individual findings cited within it carry their
  own labels, and the stage matrices and record schemas are the researchers' untested designs.
- The fields shared by all artefacts are defined once, in section 7.2.

### 6.1 Requirements stage context

- **What to record.**
    - The stage should record each normative requirement with a permanent identifier and a testable
      acceptance condition.
    - It should record scope exclusions and glossary terms. Where a term differs by desk or system,
      the entry should name the owning system or policy.
    - It should record assumptions with their rationale, and open questions with an owner, the
      affected requirements, a blocking flag, a due date and any provisional default. No template
      reviewed has an owner field on open questions.
    - It should record regulatory obligations as a first-class type, holding the instrument, clause,
      version date, interpretation and interpreting owner. No reviewed tool models this.
    - It should keep verbatim sources in immutable storage, segmented so that a requirement can cite
      a span, and it should merge clarification answers into the normative statement as well as
      retaining the question and answer.
- **Recommended format.**
    - The record should have two layers: machine-validated metadata in YAML or JSON, and normative
      content in constrained natural language. RFC 2119 or EARS can carry the statement, and
      Given/When/Then can carry the examples. Section 9.1 compares this with the alternatives.
    - The agent-facing artefact should show only current wording, and an append-only record should
      retain superseded wording.
- **Identifiers and provenance fields.** The record below is taken from the requirements note and is
  a [Proposal], with the digest and link fields added from section 7.

```yaml
id: REQ-142                 # permanent, never renumbered
digest: "sha256:..."        # of the canonicalised content
type: functional            # functional | nfr | constraint | regulatory | non-goal
statement: "When ..., the system shall ..."
acceptance: [AC-142-1]
origin: stated              # stated | inferred | agent-assumed
sources:
  - ref: "transcript/2026-10-14-ops#t112-t114"
    quote: "verbatim excerpt"
    captured_hash: "sha256:..."
    authority: stakeholder  # regulation | policy | stakeholder | ticket | agent
status: approved            # draft | needs-confirmation | approved | superseded
approved_by: "named accountable person"
approved_digest: "sha256:..."
approved_at: 2026-10-20
supersedes: REQ-097
```

- **What the stage consumes.** It consumes the source request, stakeholder records, applicable
  policy and regulation with effective dates, prior decisions and glossary terms.
- **What it must not consume.**
    - It must not consume technology stack, API or code structure material. This item has tool
      support in Spec Kit's instruction to avoid "HOW to implement"
      ([specify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/specify.md),
      Vendor).
    - It should not take current code as a default input, because code anchors requirements on what
      already exists. This item is a [Proposal].
    - It must not treat instruction-shaped text in documents, emails or tickets as direction,
      following AI-DLC's handling of source documents as untrusted data
      ([requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md),
      Vendor).
    - A requirement quote must not expose source material that later readers are not entitled to
      see, such as client email or restricted-list content.
- **Retrieval method.** Policies should be retrieved as section-level chunks with citation anchors,
  jurisdiction and effective dates, and with hybrid search because exact rule numbers favour keyword
  matching. Hybrid search also serves duplicate and precedent discovery. Linked prior decisions
  should be fetched by identifier.
- **Approval gate.**
    - The researchers rank requirement approval first among gates, because a wrong requirement
      passes every later check. This ranking is a [Proposal].
    - Approval should attach to a versioned set by digest, and any change should invalidate it.
    - The gate should require no blocking questions and a decision on every `agent-assumed` item.
    - A named compliance owner should approve regulatory interpretations rather than the engineer
      running the workflow.
    - The reviewer should first see the delta, the inferred items and the regulatory items.
- **Quality measures.**
    - The primary retrieval measures are recall of must-retrieve policies and decisions against
      labelled identifiers, and the share of retrieved items in force.
    - Task measures are faithfulness and coverage reported separately, unresolved markers, and
      testability of acceptance conditions.
    - Outcome measures are requirement changes after design approval and incidents traced to
      requirement gaps.
    - Automated scanners should prompt reviewers and should not certify quality. The best of ten
      models detected a median 47% of expert-identified issues and false-flagged 11% ([arXiv
      2609.03230](https://arxiv.org/abs/2609.03230), Independent, abstract), and LLMs in Orchid
      showed precision around 50% when finding ambiguity.
- **Failure modes.**
    - Fabrication can occur when descriptions of current practice become requirements. These
      accounted for 66% of false positives in LENS on twelve transcripts ([arXiv
      2606.25867](https://arxiv.org/abs/2606.25867), Own-method, preliminary).
    - Omission is the expected pattern when individual requirements are faithful but coverage is low
      ([Inter2US](https://arxiv.org/pdf/2510.08622), Own-method). A low faithfulness score does not
      by itself identify fabrication, because humans may use sources beyond the transcript.
    - Silent assumption is documented in ClarifyCodeBench, and Spec Kit's `/specify` instructs the
      agent to guess beyond three open markers
      ([specify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/specify.md),
      Vendor).
    - Ordering, atomicity, comparison rules and collection semantics are resolved poorly by models.
      Collection semantics stayed at or below 16.7%, comparison rules at or below 12.5%, and
      ordering and atomicity were resolved by only two models
      ([ClarifyCodeBench](https://arxiv.org/html/2607.00711v2), Independent).
    - Over-specification adds review burden. In a test from September 2025, Kiro turned a small bug
      into four user stories with 16 acceptance criteria
      ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html),
      Practitioner), and tools have since added lighter options.
    - Over-questioning follows from a precision near 50%. Spec Kit's cap of five questions with
      impact ranking is one response, and no evaluation of it was found.
- **Evidence status.**
    - Independent benchmark evidence shows that requirement defects reduce correctness
      ([Orchid](https://arxiv.org/html/2604.21505v2); [arXiv
      2507.20439](https://arxiv.org/html/2507.20439)). In the second study, the
      runnable-but-incorrect rate exceeded 80% for GPT-4 and several other models on contradictory
      descriptions.
    - A further study on requirement smells is exploratory, and its strong GPT-4o correlations did
      not survive Bonferroni correction ([arXiv 2609.29208](https://arxiv.org/html/2609.29208)).
    - Clarification helps but remains limited. Even after the pipeline, Pass@1 stayed 7.8 to 19.8
      points below complete requirements, and the best early-key-question score was 0.30
      ([ClarifyCodeBench](https://arxiv.org/html/2607.00711v2)). ClarifyGPT improved GPT-4 from
      70.96% to 80.80% with ten participants by asking only when sampled solutions diverged ([arXiv
      2310.10996](https://arxiv.org/abs/2310.10996), Own-method, 2023).
    - No evidence was found on which fields most affect downstream accuracy, whether provenance
      links improve agent accuracy, or whether extraction confidence is calibrated. This is why the
      record uses a categorical `origin` rather than a percentage.

### 6.2 Design stage context

- **What to record.**
    - Capture effort should favour what code cannot show: rejected alternatives with reasons, the
      constraints behind a choice, accepted trade-offs and revisit conditions.
    - Interfaces, data models and boundaries should be held in checkable artefacts rather than
      prose.
    - A decision record should also hold the enforcement reference, status, owner, and links to
      affected contracts and threat-model entries.
    - The template could ask directly whether familiarity or schedule influenced the decision,
      because a questionnaire of 63 participants and 13 interviews found that architects prefer
      familiar or fast options ([Borowa et al.](https://arxiv.org/abs/2309.14164), Independent,
      abstract).
- **Recommended format.**
    - Prose should hold the reasons and checkable artefacts should hold the obligations, with each
      ADR pointing to the test or contract that enforces it. MADR is a common structure, but its
      current version and the exact verification heading could not be confirmed.
    - OpenAPI, Protobuf and similar contracts should be used wherever a tool can validate them. A
      valid file can still describe the wrong contract, so validation does not replace human
      acceptance.
    - Structurizr's text model is a candidate for architecture views, and its claims are vendor
      claims about model consistency that say nothing about whether the model matches the code
      ([Structurizr](https://docs.structurizr.com/ai/dsl-generation), Vendor, snippet). Mermaid
      should be generated from a model or treated as non-authoritative.
    - Formal specifications should be reserved for a few concurrency-critical or state-critical
      areas with expert owners.
- **Identifiers and provenance fields.** In addition to the shared fields, the stage should record
  `id` such as `ADR-SETTLE-031`, `status` (proposed, accepted, rejected, deprecated or superseded),
  `decider`, `derived_from` with upstream digests, `enforced_by`, `revisit_when`, `supersedes`,
  `superseded_by` and `rationale_origin` (human-stated or agent-stated). Agent drafts should
  separate facts observed in a source from inferred rationale.
- **What the stage consumes.** It consumes approved requirements by identifier, ADRs in force,
  code-graph expansion from impacted components, constraints and non-functional requirements, and
  exact names of services, topics, fields and states. Supplying interface names raised the strongest
  TLA+ model from 16% to 26% correct, although that result has been measured only for TLA+
  ([TLA+-Bench](https://arxiv.org/abs/2607.23425), Own-method, abstract).
- **What it must not consume.** It must not consume superseded ADRs unless they are explicitly
  marked and requested, and it should not consume raw elaboration transcripts. Transcript enrichment
  can add unfaithful content, as GADR's RAG variant showed
  ([GADR](https://arxiv.org/abs/2608.17694), Own-method, abstract).
- **Retrieval method.**
    - Requirements are fetched by identifier, and ADRs by status and component with supersession
      chains followed to the head.
    - Code-graph expansion from the work item should be limited to one or two hops as a starting
      assumption.
    - For drafting a new ADR, a recency window of typically three to five prior records gave the
      best balance in one study, and retrieval helped only marginally, mainly for cross-cutting
      decisions ([Gupta et al.](https://arxiv.org/abs/2604.03826), Independent, abstract). That
      study measures ADR writing on automatic fidelity metrics, so it says nothing about whether an
      agent complies with an ADR.
- **Approval gate.**
    - Human approval should apply to decisions that are hard to reverse: architecture, schema and
      data contracts, and interfaces on which other systems or counterparties depend.
    - Agent decisions should be tiered. Local reversible choices can go to a session or pull-request
      log, and decisions that add a dependency, change a boundary, alter a data contract or affect a
      control should create a Proposed ADR and stop.
    - Changes to architecture tests, contracts and fitness functions should need independent
      approval, so that the authoring agent cannot weaken its own guardrail in one change.
- **Quality measures.**
    - The retrieval measures are recall of impacted components against what the merged change
      touched, and recall of in-force ADRs.
    - The task measure is the number of conflicts with in-force ADRs that are found at review.
    - The outcome measures are unplanned components changed and rework at gates.
    - Structural metrics should be reported as raw counts as well as density, and drift measurement
      needs a declared intended architecture because smell metrics are only a proxy.
- **Failure modes.**
    - Implicit design decisions may go unreviewed, because agents choose frameworks and integrations
      that almost no one reviews as architecture ([Konrad et al.](https://arxiv.org/abs/2604.04990),
      conceptual preprint, abstract).
    - Artefacts can be valid yet wrong. Every model in TLA+-Bench writes valid TLA+ far more often
      than correct TLA+, and an evaluation of 30 LLMs found up to 26.6% syntactic and 8.6% semantic
      correctness ([Bisharat et al.](https://arxiv.org/abs/2606.05792), Independent, abstract).
      Rates across these benchmarks are not directly comparable.
    - Rationale volume can overwhelm reviewers. Measured against human experts, LLM arguments had
      precision of 0.267 to 0.278, but 64.45% to 69.42% of arguments that experts did not mention
      were also helpful, and 1.59% to 3.24% were potentially misleading ([Zhou et
      al.](https://arxiv.org/abs/2504.20781), Independent, abstract). The resulting cost is volume,
      with a reported 4.55 to 5.77 arguments per decision against 1.98 for humans (snippet).
    - Rules may conflict or accumulate. Developers tend to add negative constraints rather than edit
      rules, and practitioners rate architectural constraints highly while rule files mainly hold
      low-level workflow and formatting constraints ([Cai et al.](https://arxiv.org/abs/2606.12231),
      Independent, abstract).
    - Generated-code exclusions in architecture tests can be too broad, and could exempt
      agent-written code from the rule. This risk is a [Proposal] extending
      [Loiane](https://loiane.com/2026/07/architecture-testing-java-archunit/) (Practitioner,
      snippet).
- **Evidence status.**
    - This stage has the weakest reading depth, because the note rests on abstracts and search
      summaries.
    - No head-to-head study of design formats as agent input was found, and no study ranks design
      content by value or loss rate. The survey evidence on rationale is old, for example [Tang et
      al.](https://figshare.swinburne.edu.au/articles/report/A_survey_of_architecture_design_rationale/26269849)
      from 2006.
    - No study measures whether ArchUnit-style rules or Pact improve agent-written code, and no
      false-positive rate for LLM architecture judges was found. Thoughtworks and Codesai recommend
      deterministic checks first
      ([Radar](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms);
      [Codesai](https://codesai.com/en/posts/2026/04/minimal-architecture-constrainsts-in-agentic-world),
      both Practitioner, snippet).
    - Empirical support exists for the value of updating rules, since artefact compliance rose from
      49.14% to 72.13% after a rule update across 160 events ([Cai et
      al.](https://arxiv.org/abs/2606.12231)).
    - Zhu et al. report decay in generated systems that detailed prompting does not mitigate ([Zhu
      et al.](https://arxiv.org/abs/2605.02741), abstract), while Larsen and Moghaddam found flat
      smell counts across 74 adopters and 77 matched controls. Their designs differ, and neither
      compares code with an intended architecture.

### 6.3 Implementation stage context

- **What to record.** The retention table below is a [Proposal] from the retrieval note.

| Artefact | Retain | Serve to later stages by default | Reason |
|---|---|---|---|
| Raw session transcript | Yes, in immutable storage under a retention schedule | No, only for audit, investigation and evaluation | It is primary evidence, and it cannot be reconstructed. |
| Decision log | Yes | Yes, by identifier | A diff cannot show what was rejected or why. |
| Specification deviations | Yes, as first-class records | Yes, and mandatory for test and review | A diff conceals them, and review needs them most. |
| Pull request description | Yes | Yes, as a lead-in that is marked as agent claims | The author wrote it, so it is not independent. |
| Test evidence from CI | Yes | Yes, as evidence | It is machine-produced and verifiable. |
| Rolling LLM summary | Only as a disposable index | Only for navigation | It is lossy and depends on the update schedule. |
| Distilled lesson | Only as a candidate linked to source episodes | Only after promotion (section 6.5) | Otherwise an unverified generalisation can become an instruction. |

- **Recommended format.**
    - Decisions and deviations should be captured through small structured tool calls during the
      work, because this is cheaper than reconstructing them from a transcript. This is a
      [Proposal].
    - Line attribution could use [Agent Trace](https://agent-trace.dev/) or
      [git-ai](https://github.com/git-ai-project/git-ai), but neither has an independent accuracy
      evaluation. Agent Trace is an RFC whose schema's version pattern would reject the three-part
      version in its own examples, and git-ai's claims are vendor claims.
    - Commit trailers such as `Assisted-by` suit disclosure and can index stronger records
      ([LLVM](https://llvm.org/docs/AIToolPolicy.html)). They are self-asserted, and a squash merge
      can alter them.
- **Identifiers and provenance fields.** In addition to the shared fields, the stage should record
  `task_id`, `implements` with requirement identifiers and digests, `commit`, `model_id` and
  version, `context_manifest_digest`, `tool_actions_ref` and `session_ref`. A deviation record
  should hold the requirement, what differs, why, and who approved it.
- **What the stage consumes.** It consumes the single task with its acceptance criteria, relevant
  design decisions by identifier, scoped rules and a limited tool set, assembled into a pack by the
  previous stage. It uses just-in-time code search for the rest, with the code retrieval options in
  [Knowledge graphs for coding agents](knowledge-graphs-for-coding-agents.md).
- **What it must not consume.**
    - It must not reach production data, production credentials or the wider tool catalogue. Stripe
      enforces this through its environment: minions run in QA devboxes with no access to real user
      data or production services, and receive a small default subset of nearly 500 tools
      ([Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2),
      Vendor).
    - It should not load other units' tasks or full requirements documents. This item is a
      [Proposal], because no controlled study of denial was found.
    - It should not treat raw transcripts from earlier sessions as direct input, or rolling
      summaries as authority.
- **Retrieval method.** The engine should push the mandatory items by identifier. Agents should use
  on-demand tools only for optional material, because availability alone does not produce use: in
  CodeCompass, 58% of trials with graph access made no call to the graph tool
  ([CodeCompass](https://arxiv.org/abs/2602.20048), Own-method, single author).
- **Approval gate.**
    - Each deviation from the approved specification should be individually approved, and each
      decision crossing the materiality tier in section 6.2 should stop for a Proposed ADR.
    - Plan and task documents can be sampled rather than approved one by one, if they trace to an
      approved requirement and deviations are surfaced.
    - Deterministic checks should run before a person sees the work. Stripe runs linters locally and
      allows at most two CI rounds before handing a branch to a human
      ([Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2),
      Vendor).
- **Quality measures.** The retrieval measures are the used-to-loaded ratio and missing-context
  events, meaning that the agent searched for something a pack should have held. The task measures
  are spec-conformance by an independent check, golden-task success, and tokens and tool calls to
  the first passing build. The outcome measures are rework commits within a set period and
  deviations per task.
- **Failure modes.**
    - Agents may follow stale files. See section 8.4 for the result and the design response.
    - Agents may skip or over-apply instructions, and in one test an agent treated research notes on
      existing classes as a new specification and generated duplicates
      ([Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html),
      Practitioner, 2025).
    - Consolidation can degrade memory. It rises in utility and can then fall below a no-memory
      baseline, and GPT-5.4 failed on 54% of ARC-AGI problems it had solved without memory even when
      consolidating from ground-truth solutions ([Zhang et al.](https://arxiv.org/abs/2605.12978),
      Independent, abstract).
    - Raw injection also performs poorly, because a trajectory exposes both useful procedure and
      obsolete state ([Li et al.](https://arxiv.org/abs/2608.12847), Independent, abstract).
    - Citation discipline has a cost. In the framework's own evaluation over 840 implementations,
      per-line requirement citations enabled automated hallucination detection at 86.4% and 88.0%,
      and they significantly reduced output determinism ([arXiv
      2606.30689](https://arxiv.org/abs/2606.30689), Own-method, abstract).
    - Agents may fix the wrong thing. Codex rewrote existing code in 20 of 80 runs in Xu and Wu, and
      tests failed in 17 of those.
- **Evidence status.**
    - No study was found of coding-agent transcripts, or of whether PR descriptions, decision logs
      or deviation logs reduce rework or review time. All memory evidence transfers from puzzle, web
      or application benchmarks.
    - The storage and delivery results can be reconciled by storing raw material and producing a
      target-bound brief at read time, which is a [Proposal]. Section 9.5 compares the options.
    - Stored transcripts may contain client or material non-public information. Retention and access
      rules were not researched and need the firm's records and compliance functions.

### 6.4 Test and review stage context

- **What to record.**
    - Test artefacts should link to requirement identifiers and digests, and they should record the
      pre-conditions, post-conditions and undefined behaviours written before test generation.
    - The record should show which tests fail when a requirement is violated, established by
      mutation or seeded faults, because a trace link only shows that a mapping exists.
    - CI evidence should hold the command, commit, result and requirement identifiers.
    - Each review should record findings with severity and disposition, the artefact versions and
      evidence seen, the context the agent loaded, and whether the finding came from a person or an
      agent.
    - Tests that assert behaviour outside the specification should be recorded as
      invented-requirement candidates rather than silently accepted.
- **Recommended format.** Test evidence should be machine-produced structured records from CI, not
  agent narrative. Review records should be structured events linked to a reviewed digest, and an
  approval should fail if the digest differs from what is released.
- **Identifiers and provenance fields.** In addition to the shared fields, the stage should record
  `verifies` with requirement identifiers and digests, `fails_when_violated` with the method and
  date, `run_id`, `commit`, `reviewer`, `reviewer_role`, `independence`, `reviewed_digest`,
  `evidence_seen` and `finding_origin` (human or agent).
- **What the stage consumes.**
    - Test agents consume requirements and acceptance criteria, contracts and relevant past
      incidents.
    - Review consumes the diff, linked requirements, scoped standards, test evidence and the
      deviation log.
- **What it must not consume.**
    - A test agent should not take the implementer's account of what the code does as its basis.
      Whether hiding the code itself helps is untested, and it would be costly for white-box
      coverage, so only the narrative is deferred.
    - A first-pass reviewer should not see the author's rationale, the agent's claim that the change
      is safe, or the implementation transcript. This item rests on one study of framing effects
      read only through search excerpts ([arXiv 2603.18740](https://arxiv.org/html/2603.18740v1))
      and on a reported Cognition position that a reviewer works best from a clean context ([Latent
      Space wiki](https://latent.space/wiki/walden-yan-7c572c23/), secondary snippet).
    - On high-risk changes, a human should form a view before seeing AI comments, or the comments
      should be presented separately. In a controlled experiment, reviewers starting from an
      automated review found more low-severity but no more high-severity issues, focused on the
      locations the LLM indicated, and saved no time ([Tufano et
      al.](https://arxiv.org/abs/2411.11401), Independent, abstract, 2024, not replicated with
      current agents).
- **Retrieval method.** Requirement content is fetched by identifier, and a required step writes
  pre-conditions and post-conditions before test generation. Review runs an independent first pass
  in a clean context and reveals the rationale for a second pass. Past incidents can be found
  through graph or search from the component.
- **Approval gate.**
    - All deterministic checks should run before a person sees anything.
    - Risk tiers should be set by rule rather than by the agent. Changes to order routing, risk
      limits, regulatory reporting, entitlements and calculations with financial effects should keep
      mandatory independent human review.
    - An AI reviewer's pass must not reduce the human reviewer's scope on high-risk work.
    - Review should show the delta against the approved upstream artefact and the deviation list,
      and a limit on queue depth should slow generation when reviewers fall behind.
    - The whole gate design is a [Proposal], because no controlled study of placement or gate count
      was found.
- **Quality measures.**
    - Test measures are requirement-to-test coverage counting only tests that fail on violation,
      mutation score or seeded-bug detection, false-alarm rate, and invented-requirement rate.
    - Review measures are precision and recall on a known-issue benchmark, addressed rate,
      high-severity finding rate, and escaped defects by requirement.
    - Review health can be sampled through seeded-fault audits on non-production paths. No published
      use was found for generated artefacts, so this would be an experiment. Approval time against
      size and the proportion of approvals without comment are only indicators.
- **Failure modes.**
    - Verification may be superficial. MAST reports that many verifiers check only whether code
      compiles, and that adding a high-level objective check raised ChatDev's success on ProgramDev
      by 15.6% ([MAST](https://arxiv.org/html/2503.13657v3), Independent).
    - Test generators can invent requirements. A property-based generator caught 28 of 30 bugs but
      invented requirements outside the specification ([Haeri and
      Ghelichi](https://arxiv.org/abs/2607.06636)).
    - Coverage can mislead. In a Google-authored study, a spec-first step gained 9.8 points in bug
      detection and 2.5 points in branch coverage on production bugs ([Tufano et
      al.](https://arxiv.org/abs/2608.17177), Vendor-affiliated, abstract).
    - Passing tests only shows that code matches the specification, as
      [specification-driven-development.md](specification-driven-development.md) section 7.1
      records.
    - Review capacity can be exceeded. Faros reports median review time up 441.5% between low and
      high adoption periods, with the caveats in section 3.3
      ([Faros](https://faros.ai/blog/ai-acceleration-whiplash-takeaways), Vendor).
    - AI reviewer noise can cause engineers to ignore the tool, which is why Uber filters categories
      that draw negative feedback ([uReview](https://www.uber.com/us/en/blog/ureview/), Vendor,
      2025).
- **Evidence status.**
    - The test-grounding result is the strongest stage-specific evidence in this research. Supplying
      the specification gained 36 to 38 points on Claude models, 28 on GPT-5.3-codex and 19 on
      Gemini 3.5 Flash, and the tester found 27 of 30 bugs with the specification against 2 of 30
      without it. The false-alarm rate fell from 33% to 0% ([Haeri and
      Ghelichi](https://arxiv.org/abs/2607.06636), Independent, abstract). The tasks are small.
    - The Google-authored study has a 77.8% and 56.7% LLM-judge comparison, which is weaker evidence
      than its bug-detection result.
    - Atlassian reports that 38.70% of generated comments led to code changes and median cycle time
      fell 30.8% ([RovoDev](https://arxiv.org/abs/2601.01129), Vendor, peer-reviewed, abstract). A
      search summary indicates that the result is not causal.
    - Uber reports that engineers mark about 75% of comments useful, and that 65% are addressed
      against 51% for human comments. These are vendor figures, and the post gives no thresholds.

### 6.5 Operations feedback context

- **What to record.**
    - Each observation should record its source (incident, settlement break, failed test or review
      comment), a link to the evidence, the affected component, and the change and deployment
      references.
    - An incident analysis should route to three separate places: a regression test against the
      affected requirement, a change or gap recorded against the requirement, and a candidate rule.
      Each destination has a different owner.
    - Lessons should be recorded as candidates with verbatim citations and source episodes, and they
      should not take effect as instructions until promoted.
- **Recommended format.** Observations should be append-only event records, and promoted rules
  should live in the reviewed rule repository. Telemetry and reference data should be read live
  rather than copied. The preferred target for a lesson is, in order, a deterministic check, a test,
  a scoped rule, and only then an always-loaded instruction, because each later step costs context
  and is enforced less reliably. This ordering is a [Proposal].
- **Identifiers and provenance fields.** In addition to the shared fields, the stage should record
  `observation_id`, `source_ref`, `occurrences` excluding bots and agent reviewers, `quote`,
  `as_of`, `routed_to`, `promotion_level`, `promotion_approver`, `replay_result` and `subject_ref`,
  which is the thing a rule is about.
- **What the stage consumes.** It consumes runbooks, deployment and change records, read-only
  telemetry and past incidents, and it uses requirement lineage to find what the failing code was
  meant to do.
- **What it must not consume.**
    - It must not have write access to production without approval.
    - It must not use unverified agent memory as a basis for action.
    - It must not treat mined comments or tickets as instructions. These inputs are untrusted, as
      the Snyk audit of a rule extraction skill indicates
      ([skills.sh](https://www.skills.sh/hiroro-work/claude-plugins/extract-rules/security/snyk),
      Vendor, snippet).
    - It should not copy break samples or client data into a knowledge store.
- **Retrieval method.** Graph expansion should run from the alert or service to recent changes and
  past incidents. Queries should carry an as-of date, so that an investigation of a past settlement
  break retrieves the rule in force on the trade date. Live systems should be read through read-only
  tools.
- **Approval gate.** Each promotion level needs its own evidence and approver, as the ladder below
  shows, and production change remains a separate gate.

| Level | Content | Evidence required | Approver |
|---|---|---|---|
| 1. Observation | An event with a source link, never loaded as an instruction | Link to the source | None, stored automatically |
| 2. Candidate | A clustered lesson with verbatim citations | N independent human occurrences or one severe incident | Triage by the area's owner |
| 3. Scoped rule | Applied to one repository or component | Replay on golden tasks shows benefit without harm | Component owner |
| 4. Team or domain standard | A pull request to the rule repository | Evidence from the scoped period | The standard's named owner |
| 5. Firm policy | Owned by an existing policy function | That function's process | Risk or compliance. Agents may propose but may not author. |

- **The ladder above is a [Proposal]**. The occurrence threshold is unset because no evidence
  supports a value. Community skills use three or more occurrences
  ([learn-from-prs](https://claudskills.com/skills/learn-from-prs/SKILL.md), Practitioner, snippet),
  and no outcomes are reported.
- **Quality measures.** The retrieval measure is recall of relevant change and incident records. The
  task measures are time to correct cause on replayed incidents, and replay results for each
  promoted rule. The outcome measures are change failure rate, time to restore, and repeat incidents
  of the same class.
- **Failure modes.**
    - Memory and rule files can be poisoned. Cisco demonstrated a compromise in which an npm
      postinstall hook overwrote `MEMORY.md` files across projects and modified hook settings, and
      the poisoned agent recommended storing an API key in a committed file
      ([Cisco](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code),
      Vendor security research). Cisco reports that version 2.1.50 removed user memories from the
      system prompt.
    - Agents can validate one another. Occurrence counts must exclude agent reviewers, because
      agent-only review is common in agent PRs ([Duma et al.](https://arxiv.org/html/2605.02273)).
    - An LLM rewriting lessons can degrade performance even from correct inputs ([Zhang et
      al.](https://arxiv.org/abs/2605.12978)).
    - Rules can be overfitted. The dotnet/fsharp project dropped rules fitted to single PRs when
      mining about 695 comments ([PR 19451](https://github.com/dotnet/fsharp/pull/19451),
      Practitioner, snippet), and a pytest discussion describes demoting rules without a verified
      quote ([discussion 14685](https://github.com/pytest-dev/pytest/discussions/14685),
      Practitioner, snippet).
    - Rules may expire incorrectly if they are removed because failures stopped. BMAD removes a
      policy only when its subject is gone or a human removes it
      ([BMAD](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/),
      Practitioner).
    - A misclassified incident can hide its actual cause. A cut-off misunderstanding treated as a
      coding rule leaves the requirement gap in place, and this example is a [Proposal].
- **Evidence status.**
    - This stage has the least empirical support. No measured study of learned rules reports later
      defect or review outcomes, no empirical study of postmortems feeding rules or requirements was
      found, and no large organisation has published a promotion model.
    - The available incident material is prescriptive practitioner writing. The primary papers for
      MemoryGraft and MINJA were not located.

### 6.6 Side-by-side summary of the stages

The table below is a [Proposal] that condenses sections 6.1 to 6.5.

| Stage | Main output | Authoritative form | Mandatory input | Denied input | Main gate | Primary measure |
|---|---|---|---|---|---|---|
| Requirements | Requirement, obligation, assumption, question | Metadata and constrained text | Sources and in-force policy | Stack and code by default | Requirement approval by digest | Must-retrieve recall, faithfulness and coverage |
| Design | Decision and contract | ADR and checkable contract | Approved requirements and in-force ADRs | Superseded ADRs and raw transcripts | Hard-to-reverse decisions | Impacted-component recall |
| Implementation | Code, decision log, deviations | Git and structured events | One task pack | Production access and other tasks | Deviation approval | Spec-conformance by independent check |
| Test and review | Failing-on-violation tests and findings | CI evidence and review events | Requirements and deviation log | Author narrative on first pass | Independent review on regulated scope | Seeded-fault detection |
| Operations feedback | Observation and routed changes | Event record and rule repository | Change records and live telemetry | Unverified memory and production write | Promotion and production change | Time to correct cause and repeat incidents |

## 7. Cross-stage model

Sections 7.2 to 7.6 are a [Proposal]. No tool found implements the whole model, and no study has
compared it with alternatives.

### 7.1 Evidence on stage handoffs

- No source measures information lost per handoff, and no controlled study compares typed schemas,
  handoff documents, blackboards and gates under the same conditions.
- MAST is the closest evidence ([MAST](https://arxiv.org/html/2503.13657v3), Independent, preprint
  v3 of October 2025). It annotated more than 1,600 traces across seven frameworks and found 14
  failure modes.
    - Its explicit handoff modes have small shares, such as ignored input at 1.9% and information
      withholding at 0.85%, while disobeying the task specification is 11.8% and failure to ask for
      clarification is 6.8%.
    - These small shares do not show that handoffs are safe, because a downstream agent that
      silently acts on an incomplete artefact may be labelled as derailment or as a reasoning-action
      mismatch.
- MetaGPT has agents exchange role-specific documents through a publish-subscribe pool. Its authors
  report executability of 3.75 against 2.25 and human revision cost of 0.83 against 2.5 compared
  with ChatDev, at 31,255 tokens against 19,292 ([Hong et al.](https://arxiv.org/html/2308.00352),
  Own-method, 2023). This compares whole systems and does not isolate the schema.
- Cognition asks teams to share full traces
  ([Cognition](https://cognition.com/blog/dont-build-multi-agents), Vendor), while Anthropic passes
  lightweight references to durable artefacts and reports about 15 times the tokens of chat for
  multi-agent work ([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system),
  Vendor). Both reject a lossy summary as the carrier of context, so a platform can pass artefact
  references between stages and use clean contexts for independent review. This reconciliation is a
  [Proposal].
- A preprint reports that handoff count alone accounts for failures in ChatDev and Magentic, but it
  was seen only as an unverified snippet ([arXiv 2609.17464](https://arxiv.org/pdf/2609.17464)).
- Typed schemas address missing fields and do not address wrong content. A gate must therefore check
  meaning as well as form, which is why section 6 pairs each schema with a test or a named reviewer.

### 7.2 Artefact identity and versioning

- Current tools identify artefacts by path, feature number or naming convention, and none of the
  documentation read specifies per-requirement content hashes, supersession records or event
  sourcing.
    - Spec Kit uses numbered feature directories
      ([spec-driven.md](https://raw.githubusercontent.com/github/spec-kit/main/spec-driven.md),
      Vendor).
    - OpenSpec separates live specs from dated change folders, which is the closest found to a
      supersession model
      ([OpenSpec](https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/README.md), Vendor).
    - AWS AI-DLC declares FR and NFR identifiers to be permanent keys
      ([requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md),
      Vendor), but its `traceability.json` holds only `id`, `kind` and `of`.
- The proposed model separates a stable logical identifier from a version digest, for example
  `REQ-RESTRICT-014` plus a SHA-256 of the canonicalised content.
- Each artefact would carry the shared fields below.

| Field | Purpose |
|---|---|
| `id` | A permanent logical identifier that is never renumbered or reused. |
| `digest` | A cryptographic hash of the canonical content, which provides the version. |
| `type` and `stage` | The record type and the stage that produced it. |
| `status` | The lifecycle state. Generation and approval must be separate fields, to avoid the failure in AI-DLC issue #249. |
| `origin` | Whether the content was stated, inferred or agent-assumed. |
| `sources` | The upstream references and verbatim spans. |
| `owner` | The accountable person or role. |
| `effective_from`, `effective_to`, `jurisdiction` | The validity fields used by the filter in section 8.2. |
| `approved_by`, `approved_digest`, `approved_at` | The approval bound to exact content. |
| `supersedes`, `superseded_by` | The replacement chain. |
| `entitlement` | The access class that derived artefacts inherit. |

- A cryptographic hash matters for tamper evidence. Agent Trace's Murmur3 example is suitable for
  relocating moved code, but Murmur3 is not a cryptographic hash.

### 7.3 Lineage links

- A link is a record with `from`, `to`, `type`, `to_digest`, `link_status`, `created_by` and
  `created_at`. The types are `derives_from`, `constrains`, `implements`, `verifies`,
  `deviates_from`, `approves`, `supersedes` and `caused_by`.
- Links should be recorded when the work happens, rather than recovered later. LLM recovery is
  suited to proposing candidates for review.
    - On CM1, TraceLLM's best configuration reached precision 0.45, recall 0.67 and F2 0.61
      ([TraceLLM](https://arxiv.org/html/2602.01253), Own-method, peer-reviewed per its listed
      reference). Figures for its other datasets were not read.
    - An LLM ensemble reached F2 comparable to information retrieval methods with lower precision
      ([Fuchß et al.](https://fuchss.org/conferences/aire25/), workshop paper, 2025), and a 2025 KIT
      thesis reports that an agentic approach fell short of traditional retrieval (snippet).
- Recovered links should keep a `proposed` status until a named person confirms them, because at a
  precision near 0.5 about one proposed link in two would be wrong.
- [sdlc-context-graph.md](sdlc-context-graph.md) section 8 records ReqToCode, in which code
  references typed trace elements so that a broken trace breaks the build. This round found no
  outcome evidence for that approach, and it remains a candidate for the `implements` link.

### 7.4 Supersession

- A decision can change in three ways, following the distinction described by
  [Repowise](https://repowise.dev/blog/guides/use-git-history-to-catch-stale-adrs-before-they-mislead-agents)
  (Vendor, snippet): amend for corrected context, supersede for a replacement decision, and archive
  for a record that no longer guides work.
- The two published positions on records can coexist. Append-only guidance is common among
  practitioners
  ([example](https://dev.to/naman_here/adrs-for-ai-coding-agents-how-to-make-every-agent-read-architecture-decisions-3he4),
  snippet), while [Davidson](https://duncandavidson.com/agents-love-decisions) (Practitioner,
  snippet) argues that agents need the ruling that governs today and that Git can carry the history.
  An append-only audit store and a current-only agent view satisfy both.
- No controlled study shows that agents obey status fields or supersession markers, so status text
  alone is a weak control. The stronger design has five parts.
    1. Superseded records are excluded from default retrieval.
    2. They remain reachable only on explicit request.
    3. Any direct read shows a superseded-by banner.
    4. The enforcing test is replaced or retired in the same change.
    5. Derived rules, skills and examples are searched for and removed, because developers tend to
       add a negative rule beside the old instruction ([Cai et
       al.](https://arxiv.org/abs/2606.12231)).
- Supersession should be tested with a fresh agent that asks for the governing decision, as one
  practitioner guide suggests.

### 7.5 Staleness propagation

- When an upstream digest changes, every artefact whose link names the earlier digest becomes
  `suspect`, and its approval is marked as no longer current. This is the established "suspect link"
  idea from requirements management tools, although its use in the tools covered here was not
  confirmed.
- Propagation should be transitive but triaged. A material change to a requirement marks its design,
  tests and task packs as suspect, and the owner either confirms the link against the new digest or
  opens a change. An editorial change can be declared non-material only by the owner.
- Drift detection operates at three levels, and each catches different faults.

| Level | Check | Catches | Misses |
|---|---|---|---|
| Reference | Cited symbols, files and identifiers exist, and orphan citations are rejected | Removed code and fabricated identifiers | Behaviour that changed under the same name |
| Structural | The declared graph is compared with the import graph, and contracts are diffed | Boundary and interface violations | Logic errors inside a permitted structure |
| Behavioural | Tests derived from requirements are run | A precedence rule that compiles but behaves differently | Whatever the tests do not state |

- Automatic bidirectional synchronisation should be avoided, because editing a specification to
  match code could legitimise a defect. A difference found by a check should open a proposed change
  that requires approval, which is partly what Tessl's "update the spec first" guidance implies
  ([Tessl
  skill](https://tessl.io/registry/tessl-labs/spec-driven-development/files/skills/spec-verification/SKILL.md),
  Vendor).
- The drift gates proposed by the Spec Growth Engine report no outcome figures in the abstracts read
  ([arXiv 2606.27045](https://arxiv.org/abs/2606.27045); [arXiv
  2610.11725](https://arxiv.org/abs/2610.11725), single author). Spec Kit's claim that
  specifications stay in sync because they generate code does not explain how hand-edited code is
  handled, and Böckeler classes the tool as spec-first.

### 7.6 Where artefacts live

- The recommendation is both: Git for authored artefacts, an append-only event store for gates and
  links, and a graph or index rebuilt from those two. Section 9.2 gives the comparison.

| Artefact class | Authoritative store | Derived copies |
|---|---|---|
| Requirements, ADRs, contracts, tests, rules | Git, reviewed by pull request | Search index and graph |
| Verbatim sources and raw transcripts | Immutable object storage with entitlements and a retention schedule | Span references only |
| Gates, approvals, link events, context manifests, deviations | Append-only event store | Graph and dashboards |
| Workflow state | Engine-owned schema, as in [aidlc-context-management.md](aidlc-context-management.md) section 9.6 | None |
| Test evidence | CI system, exported as events | Requirement coverage views |
| Telemetry, restrictions, reference data, tickets | The owning systems, read live | Identifiers and links, without content |

- A signed attestation could bind the model, context manifest digest, artefact digests and approver,
  using an in-toto custom predicate. This would be an in-house convention, because no predicate for
  agent-generated code was found, and a 2026 conference abstract says that AI models remain outside
  established provenance frameworks ([OpenSSF
  abstract](https://openssfcdeu2026.sched.com/event/2RA4B)).
- No single standard covers the chain from requirement to approval. Agent Trace treats quality
  assessment and code ownership as non-goals, and the [SPDX 3 AI
  profile](https://github.com/spdx/spdx-3-model/blob/main/model/AI/AI.md) describes a component
  rather than one generated change.

## 8. Retrieval design

The pipeline and matrices in this section are a [Proposal]. The evidence cited motivates them, but
none of it tests them on delivery artefacts.

### 8.1 Context assembly per stage

- The engine should build each pack from a declared manifest in the following order. Stable content
  should come first to preserve the prompt cache, as
  [aidlc-context-management.md](aidlc-context-management.md) section 9.3 describes.
    1. **Entitlement filter.** Enforced by the retrieval layer, this step removes what the requester
       and task may not see.
    2. **Validity filter.** This step applies status, effective dates and supersession, as section
       8.2 describes.
    3. **Scope filter.** This step applies jurisdiction, component and stage, including the deny
       list for the stage.
    4. **Mandatory items.** The engine pushes identifier-linked items. An expected item that cannot
       be supplied stops the stage.
    5. **Optional retrieval.** Hybrid search, graph expansion or agent tools then find optional
       items.
    6. **Re-ranking and budget.** Only optional items are ranked and trimmed, and overflow is
       offered as references.
    7. **Manifest record.** The engine logs each artefact identifier and digest loaded, with the
       stage, work item and pack version.
- The stage matrix below is the researchers' synthesis. Direct support exists only for the cells
  marked (a) Spec Kit, (b) arXiv 2607.06636 and 2608.17177, (c) arXiv 2603.18740, and (d) Stripe.
  All other cells are reasoned design choices.

| Stage | Should receive | Denied or deferred | Assembly mechanism |
|---|---|---|---|
| Requirements | Source request, stakeholder records, in-force policy and regulation, prior decisions, glossary | Stack, API and code structure (a); current code by default | Retrieval by policy and domain tag, plus a clarification marker rule |
| Design | Approved requirements by identifier, in-force ADRs, code-graph expansion, constraints | Superseded ADRs unless marked; raw transcripts | Graph expansion from the work item, one or two hops |
| Implementation | One task and its acceptance criteria, relevant decisions, scoped rules, tools | Other units' tasks; production data and credentials (d); wider tool catalogue (d); full requirement documents | Task pack plus just-in-time code search |
| Test | Requirements and acceptance criteria (b), contracts, past incidents | The implementer's account of the code | Retrieval by requirement identifier, plus a required conditions step (b) |
| Review | Diff, linked requirements, standards, test evidence, deviation log | Author rationale and agent claims on first pass (c); transcript | Independent first pass, then rationale revealed |
| Operations | Runbooks, change records, read-only telemetry | Unapproved production write; unverified memory | Graph expansion from the alert to changes and incidents |

- Denial is more reliable when the tool or environment enforces it, because agents both skip and
  over-apply prompt instructions. A prompt rule can remain as an explanation of the boundary. For
  example, a development agent should have no route to client positions or restricted lists,
  whatever its instructions say. (Illustration.)
- Each stage should also keep a token budget per tier, and no published figures exist to set it.
  Starting values should be treated as assumptions and adjusted through the ablation method in
  section 12.
- BMAD's statement that "an index the agent must choose to fetch gets skipped" has no published data
  ([BMAD](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/),
  Practitioner), but it is consistent with the CodeCompass result. This is the main reason for
  pushing mandatory items.

### 8.2 Validity filtering

- Validity should be established before relevance ranking, for four reasons.
    - Re-rankers show "a strong bias toward older, semantically rich documents, even when they are
      factually obsolete", and optimised instructions improved evolving-knowledge performance by up
      to 27% ([An et al.](https://arxiv.org/abs/2604.14227), own benchmark, abstract).
    - Outdated passages reduce accuracy and can mislead even when current information is available
      ([HoH](https://aclanthology.org/people/jie-ouyang/), Independent, snippet, 2025).
    - Under 75% synthetic distractors, an unbounded memory had the highest mean similarity (0.87)
      and the lowest precision, so a high similarity score does not indicate good retrieval
      ([Reddy](https://arxiv.org/abs/2606.29178), Independent, abstract).
    - Re3 reports a 9.7% average generation gain on its own benchmark from a conflict-aware recency
      filter ([Cao et al.](https://aclanthology.org/2026.acl-long.1180/), own benchmark, snippet).
- None of these benchmarks uses requirements, ADRs or policies, so their transfer to governed
  artefacts is an inference.
- Recency decay is unsuitable for governed artefacts, because an old policy in force outranks a
  recent draft. The filter should be `status = in-force AND effective_from <= as_of < effective_to
  AND superseded_by IS NULL`. Decay is reasonable only for tickets and informal discussion.
- Every query should carry an `as_of` date.
    - A change built for a future regulatory date needs the rule that will apply on that date.
      (Illustration.)
    - An investigation of a past settlement break needs the rule in force on the trade date.
      (Illustration.)
    - The term "current" would give the wrong answer in both cases.
- Citations should name the identifier and digest, and a gate should machine-check them. Every
  generated requirement, decision and test must resolve to a real in-force source, and an orphan
  citation should be rejected before a person reads it. The orphan approach comes from a study seen
  through a search excerpt, and no measurement shows that citations improve accuracy or reviewer
  speed.
- Retrieval should vary by artefact type.

| Artefact | Primary method | Secondary method | Ranking signal |
|---|---|---|---|
| Requirements | Identifier and trace link | Hybrid search for duplicates and precedent | None for linked items |
| ADRs | Status and component, following the chain to the head | Hybrid search for precedent | None for in-force items |
| Policies | Section chunks with anchors, jurisdiction and dates | Keyword match on rule numbers | Relevance after validity |
| Tickets and chat | Link from the work item | Permission-trimmed search | Recency decay and low authority |
| Lessons | Promotion level and scope | None | Never searched as authority below level 3 |
| Summaries | Navigation only | None | BMAD's argument favours retrieving the source instead |

### 8.3 Source precedence

- A single global order is not sufficient, because the correct winner depends on what the conflict
  concerns. Xu and Wu make the authority order an explicit design decision: for an instruction about
  code conventions the code may be the better evidence, while for a client mandate rule the approved
  requirement should prevail and the conflict should stop the work.
- The table below is a [Proposal] that separates normative questions from descriptive ones.

| Question type | Precedence | When the sources disagree |
|---|---|---|
| What must the system do? | Regulation or legal text, then approved firm policy, then in-force ADR, then approved requirement, then ticket, then chat | Stop and route to the owner of the higher source. |
| What does the system do now? | Executing code and tests, then generated code knowledge, then documentation | Use the code, and mark the document as suspect. |
| What convention applies here? | Existing code in the module, unless an in-force standard names a migration | Follow the code, and raise a candidate if a standard is breached. |
| What is the current business data? | The owning system, read live | Never resolve this from a document or a memory. |
| Which item applies within one level? | The later effective date | Same level with overlapping validity: stop and route to the owner. |

- A desk head's recent statement in a meeting should not override a compliance interpretation of a
  clause. The `authority` field in the requirement record exists so that a more recent statement
  does not override a higher source. (Illustration.)

### 8.4 Conflict handling

- **The Xu and Wu result.** The authors built 40 Python projects in which an instruction file
  conflicted with the code, and ran Claude Code and Codex CLI for 320 runs ([arXiv
  2610.30571](https://arxiv.org/abs/2610.30571), Independent, preprint of 22 October 2026).
    - Without intervention, 90.1% of choices followed the stale file.
    - Claude Code flagged the conflict in 79 of 80 runs and still followed the file.
    - Codex rewrote existing code in 20 of 80 runs, and tests failed in 17 of those.
    - One sentence giving existing code precedence raised code-following choices from 4.2% to 91.4%,
      and test pass rates from 89.4% to 100%.
    - The conflicts are synthetic and concern coding conventions, so the result may not transfer to
      business rules. It measures the consequence of staleness and does not measure how often
      staleness occurs.
- **Design consequences.** The following points are a [Proposal].
    - Agents should emit a structured conflict record, naming both artefacts and digests. The
      engine, not the agent, should then move the work to a blocked state when the conflict concerns
      a normative question.
    - The stage prompt should contain explicit precedence for descriptive conflicts, since that
      sentence was cheap and effective in the study. The sentence should follow the table in section
      8.3, because the same rule applied to a mandate could override an approved restriction.
    - Models should not arbitrate conflicts between normative sources at the same level. The
      conflict should go to the owner of the higher source.
    - Pre-flight checks should detect known conflicts between in-force artefacts before an agent
      starts. Cai et al. also call for automated conflict detection in rule sets.
    - Each conflict and its resolution should be recorded, and a repeated conflict type should
      create an observation under section 6.5.
- **Testing the design.** Golden tasks should include stale-context traps, conflicting-source traps
  and must-refuse cases, and fresh-agent probes should confirm that the governing record is
  returned.
- **What remains unknown.** No study compares the harm of a stale artefact with that of a missing
  one, and no independent evaluation of any tool's drift detector was found.

## 9. Option comparisons

Each option uses the same five items. Costs are qualitative because no source publishes comparable
figures. The capital markets worked examples are illustrations and are not sourced findings.

### 9.1 Requirement record format

#### Option A: Markdown with a constrained notation

- **How it works.** Requirements live in Markdown with light conventions, such as EARS in Kiro,
  `MUST` statements with Given/When/Then in Spec Kit, and RFC 2119 keywords with scenarios in
  OpenSpec.
- **Strengths.** It is readable, reviewable in a pull request and portable across harnesses, and
  every reviewed tool already works this way.
- **Weaknesses.** Metadata such as source, approver and status cannot be validated reliably, and
  prose status has been misread at a gate in AI-DLC issue #249. No study shows that any notation
  improves generation.
- **Cost.** Authoring and tooling costs are low, and audit reconstruction costs are high later.
- **Worked example (illustration).** It fits a small internal change to a trade blotter filter,
  where a reviewed scenario is sufficient. It does not fit a client mandate precedence rule, where
  an auditor must establish the source, the interpretation owner and the approved version of each
  clause.

#### Option B: Structured metadata with a constrained text body

- **How it works.** A YAML or JSON layer holds identifiers, type, status, sources and approver, and
  the normative statement remains constrained natural language. AI-DLC's JSON sidecar is a partial
  precedent, and the full design is a [Proposal].
- **Strengths.** Machines can validate gate-controlling fields, reviewers can read the text, and
  staleness can be computed from digests.
- **Weaknesses.** Its benefit has not been tested against plain Markdown. Authors need tooling, or
  the metadata will be neglected, and origin labels depend on honest capture.
- **Cost.** A schema, validators and gate integration are moderate one-time costs, and each
  requirement needs a small additional authoring effort.
- **Worked example (illustration).** It fits a T+1 settlement change that spans several services,
  because each affected test and design can be marked suspect when a requirement changes. It does
  not fit a one-line defect fix, where a ticket link and a regression test are sufficient and the
  record would add review burden.

#### Option C: External requirements management tool

- **How it works.** A governed tool such as Jama holds requirements, and agents reach it through an
  MCP server or an interchange format such as ReqIF. Jama says that existing permissions, lifecycle
  workflows and audit trails apply ([release
  notes](https://support.jamasoftware.com/hc/en-us/articles/45837542601229-Version-9-35-Customer-Validated-Cloud),
  Vendor).
- **Strengths.** It reuses an existing audited process and suspect-link style workflows, and this
  may matter where such a tool already holds the record.
- **Weaknesses.** Its review path is separate from code review, and the MCP server is a separately
  purchased add-on. No official DOORS Next or Polarion MCP server was found, and the Polarion
  package found is not established as a Siemens product. No study evaluates agent use of these
  tools.
- **Cost.** Licences and integration are high unless the firm already owns them.
- **Worked example (illustration).** It fits a firm whose regulatory reporting requirements are
  already governed in such a tool, because a second store would create a conflict over authority. It
  does not fit a new internal analytics service with no existing record, where a licence and
  integration add cost without a control benefit.

| | A: Markdown | B: Metadata and text | C: External tool |
|---|---|---|---|
| Machine validation | Weak | Strong | Strong |
| Review path | Pull request | Pull request | Tool workflow |
| Audit fields | Manual | Schema-enforced | Tool-enforced |
| Evidence of agent benefit | None comparative | None | None |
| Cost | Low | Moderate | High unless owned |
| Main limitation | Unverifiable metadata | Tooling required | Separate from code review |

- **Trade-off.** Option B gives up some simplicity to make staleness and approval computable. The
  recommendation is Option B for material or regulated requirements, Option A or a ticket for small
  changes, and Option C where such a tool is already authoritative. This is a [Proposal], and the
  user's own tasks should test it.

### 9.2 Artefact storage

#### Option A: Git only

- **How it works.** All artefacts, events and links are files in a repository, as in AWS AI-DLC's
  `aidlc/` directory.
- **Strengths.** It has a natural review path, it needs no new infrastructure, and it is portable
  across harnesses.
- **Weaknesses.** Files cannot be queried, only read, as
  [sdlc-context-graph.md](sdlc-context-graph.md) section 4 records. History can be rewritten, and
  a path or branch-scoped folder is a weak audit identifier.
- **Cost.** Infrastructure cost is low, and cost rises with audit reconstruction and multi-team use.
- **Worked example (illustration).** It fits a single team running a pilot on a trade enrichment
  service. It does not fit the question "which released code derives from a superseded version of
  restriction R-14 across twelve repositories?"

#### Option B: Database or graph only

- **How it works.** Artefacts are typed records in a database or graph, and agents write them
  through tools. The AIDLC Collaborative sample moves in this direction, while its engine still owns
  Git operations.
- **Strengths.** Lineage and impact queries are direct, and identity and access control are central.
- **Weaknesses.** It loses the pull request review path, requires a migration and creates a new
  critical system. A graph may also look authoritative when its feeds are stale, as
  [sdlc-context-graph.md](sdlc-context-graph.md) section 7 describes.
- **Cost.** Build and operating costs are high.
- **Worked example (illustration).** It fits lineage data for a counterparty hierarchy, which is
  relational by nature and has a system of record. It does not fit architectural decisions that
  engineers review alongside the code they constrain.

#### Option C: Git, an append-only event store and a derived graph

- **How it works.** Git holds authored artefacts, an append-only store holds gates, approvals, links
  and manifests, and a queryable graph is rebuilt from both.
- **Strengths.** It keeps the review path, supports immutable approvals, and allows the graph to be
  discarded and rebuilt.
- **Weaknesses.** It has three components to synchronise, and no primary evidence compares it with
  the alternatives. Rebuild logic can itself have defects, and Git history still needs protection
  against rewriting.
- **Cost.** The cost is moderate to high, and it can be phased by starting with event records in a
  simple table and adding a graph only when queries need it.
- **Worked example (illustration).** It fits a mandate engine change, where a person can read the
  requirement in a pull request while an auditor queries who approved which digest. It does not fit
  a two-person team on a low-risk reporting tool, where the operating cost exceeds the benefit.

| | A: Git only | B: Database or graph | C: Hybrid |
|---|---|---|---|
| Human review | Strong | Weak | Strong |
| Lineage queries | Weak | Strong | Strong |
| Tamper evidence | Needs protection | Depends on design | Strong for events |
| Operating burden | Low | High | Moderate to high |
| Evidence | Vendor use | Vendor use | Proposal only |

- **Trade-off.** Option C accepts synchronisation work in exchange for keeping both review and
  query. It is recommended where audit reconstruction matters, starting from Option A with event
  records added first.

### 9.3 Specification lifecycle

The three levels come from
[Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) (Practitioner,
October 2025), and the tools may have moved since then.

#### Option A: Spec-first

- **How it works.** A specification is written for the task, used to generate the work, and not
  necessarily maintained afterwards. Böckeler classes Kiro and Spec Kit here.
- **Strengths.** It has low maintenance cost, and it supplies a reviewed intent.
- **Weaknesses.** The specification stops describing the system, so a later agent may follow it if
  it remains retrievable.
- **Cost.** It has a low ongoing cost, with a retrieval risk if old specifications are not excluded.
- **Worked example (illustration).** It fits a one-off migration script for a retired counterparty
  field. It does not fit a restriction engine, whose rules outlive any change.

#### Option B: Spec-anchored with drift gates

- **How it works.** The specification is kept for the feature's life, and the three levels of check
  in section 7.5 block or flag differences.
- **Strengths.** It provides a durable record that can be checked, and it keeps code as a separately
  reviewed artefact.
- **Weaknesses.** Maintenance is an ongoing cost, and no independent precision or recall figures
  exist for drift detectors. Behavioural checks catch only what tests state.
- **Cost.** It has a moderate build cost and an ongoing maintenance cost.
  [aidlc-context-management.md](aidlc-context-management.md) section 7.4 records one project
  spending one to two hours per week, from a single developer's observational account.
- **Worked example (illustration).** It fits regulatory reporting field mappings, where each rule
  needs a durable requirement and a test. It does not fit an exploratory analytics prototype that
  may be discarded within weeks.

#### Option C: Spec-as-source

- **How it works.** The specification is the main edited file, and code is regenerated from it.
  Tessl explores this, and a third-party review says that its regeneration remains in closed beta
  (snippet).
- **Strengths.** It avoids duplicate maintenance in principle, and a change is expressed at the
  level of intent.
- **Weaknesses.** Regeneration showed non-determinism even at a low abstraction level in Böckeler's
  test, and citation discipline further trades against determinism. The approach depends on
  regeneration being deterministic enough to review.
- **Cost.** The product risk is high, and adoption costs are unknown.
- **Worked example (illustration).** It may fit a generated adapter from a schema where the output
  is fully testable. It does not fit a production trading change, where a reviewer must be able to
  approve exact code.

| | A: Spec-first | B: Spec-anchored | C: Spec-as-source |
|---|---|---|---|
| Durable record | No | Yes | Yes |
| Maintenance | Low | Moderate | Unknown |
| Reviewable code | Yes | Yes | Regeneration dependent |
| Main risk | Stale spec retrieved | Maintenance loss | Non-determinism |
| Suitability for regulated change | Low | High | Low at present |

- **Trade-off.** Option B accepts maintenance cost for a durable and checkable record. The
  recommendation is Option B for long-lived or regulated rules and Option A for one-off work, with
  completed Option A specifications excluded from default retrieval.

### 9.4 Retrieval mechanism

#### Option A: Identifier and lineage pack

- **How it works.** The engine fetches artefacts named by the work item and its links, and it pushes
  them into the context.
- **Strengths.** It is deterministic, auditable and easy to measure, and it does not depend on the
  agent choosing to search.
- **Weaknesses.** It cannot find anything that has not been linked, and it inherits any wrong or
  missing link.
- **Cost.** It is low once identifiers exist, and it depends on link discipline.
- **Worked example (illustration).** It fits supplying the approved restriction requirement to a
  test agent. It does not fit finding that a similar mandate rule was decided two years ago under a
  different identifier.

#### Option B: Filtered hybrid search

- **How it works.** Keyword and vector search run after deterministic validity and scope filters.
- **Strengths.** It discovers unlinked precedent and policy, and exact rule identifiers favour its
  keyword component.
- **Weaknesses.** Similarity is not validity, and distractors reduce accuracy. No measured
  comparison exists for these artefacts.
- **Cost.** An index, chunking and metadata maintenance are moderate costs.
- **Worked example (illustration).** It fits locating a clause in a settlement policy from a
  description. It does not fit the current restricted list, which must come from the system of
  record.

#### Option C: Graph expansion

- **How it works.** Traversal starts from a node such as a component or alert and follows typed
  edges for one or two hops. The [earlier report](knowledge-graphs-for-coding-agents.md) and
  [sdlc-context-graph.md](sdlc-context-graph.md) section 6 record the code graph evidence.
- **Strengths.** It answers multi-hop dependency questions directly, and structural questions are
  where graphs help most.
- **Weaknesses.** Answers look authoritative when feeds are stale, agents underuse optional graph
  tools, and no stage-level evaluation exists.
- **Cost.** It is low for a code graph, and high for a work graph with many feeds.
- **Worked example (illustration).** It fits tracing a field from trade enrichment through a topic
  to a transaction report mapper. It does not fit a question about why a business owner prefers one
  exception flow, which appears in a source record rather than a structural edge.

#### Option D: Agent-driven just-in-time tools

- **How it works.** The agent holds references and searches or reads what it decides it needs.
- **Strengths.** It reads current content and loads only what it uses, which suits source code well.
- **Weaknesses.** Retrieval can only answer questions that the agent thinks to ask, and tools may
  not be called at all. It is unsuitable for a control that must always apply.
- **Cost.** It has low infrastructure cost and higher token and latency cost.
- **Worked example (illustration).** It fits finding the callers of a settlement date function
  during implementation. It does not fit ensuring that a best-execution record-keeping obligation is
  seen on an order routing change.

| | A: Identifier pack | B: Filtered hybrid | C: Graph expansion | D: Agent tools |
|---|---|---|---|---|
| Finds unlinked items | No | Yes | Only through edges | If sought |
| Determinism | High | Medium | High on a fixed graph | Low |
| Suitable for mandatory context | Yes | No | Partly | No |
| Audit clarity | High | Medium | High | Medium |
| Main failure | Missing link | Valid-looking stale or distractor text | Stale graph | Item never sought |

- **Trade-off.** These options complement one another. The recommendation is Option A for mandatory
  items, followed by B, C or D for optional discovery, with a design that records which mechanism
  supplied each item. This is a [Proposal] that extends the manifest in
  [aidlc-context-management.md](aidlc-context-management.md) section 9.3.

### 9.5 Implementation session record

#### Option A: Retained raw transcript

- **How it works.** The full session is stored unchanged and is read for audit or investigation.
  Entire is described as capturing prompts, tool calls and diffs on an orphan branch (Secondary).
- **Strengths.** It is primary evidence that cannot be reconstructed, and episodic retention stayed
  competitive with consolidators ([Zhang et al.](https://arxiv.org/abs/2605.12978)).
- **Weaknesses.** Direct injection performs poorly, sensitive content needs controls, and storage
  cost at enterprise scale was not established.
- **Cost.** It has storage, access control and retention review costs.
- **Worked example (illustration).** It fits reconstructing how a regulatory reporting change was
  produced. It does not fit direct loading into the next unit's context, where obsolete state would
  come with it.

#### Option B: Rolling LLM summary

- **How it works.** A model repeatedly condenses the session or its memory.
- **Strengths.** It is compact and cheap to load, and it helps with navigation.
- **Weaknesses.** Consolidation can fall below a no-memory baseline, and the same trajectories give
  different memories under different schedules. AMA-Bench's authors report a related gain from
  bypassing an extraction layer (Secondary).
- **Cost.** Each update is a model call, and undetected loss adds a hidden cost.
- **Worked example (illustration).** It fits a navigation index over a long margin calculation
  debugging session. It does not fit a record of an agreed settlement exception.

#### Option C: Structured decision and deviation records

- **How it works.** The agent records decisions and deviations through small tool calls, each linked
  to requirement identifiers.
- **Strengths.** Records are queryable and reviewable, and they supply what a diff conceals.
- **Weaknesses.** Agent-stated rationale may be reconstructed after the event, and agents may
  under-report. No study measures its effect on rework or review.
- **Cost.** It has a low runtime cost, and a schema and enforcement cost.
- **Worked example (illustration).** It fits an agent that implements a cut-off differently from a
  requirement and needs approval. It does not fit capture of every minor local naming choice, which
  would add noise.

#### Option D: Target-bound brief at read time

- **How it works.** When a later stage reads earlier work, a note is produced for that target,
  holding the reusable procedure, bindings to recover, applicability conditions and verification
  requirements.
- **Strengths.** One study reported 62.3% success over 2,391 instances, which is 10.7 points above
  raw injection with 48.9% fewer online tokens ([Li et al.](https://arxiv.org/abs/2608.12847),
  Independent, abstract).
- **Weaknesses.** The environments are web and application tasks rather than software delivery, and
  the comparison is with raw injection rather than generic summaries. Each brief must be generated
  and is itself an unverified derivative.
- **Cost.** It adds a model call at read time and needs the raw store to exist.
- **Worked example (illustration).** It fits briefing a test agent on how an earlier unit handled a
  counterparty hierarchy edge case. It does not fit an audit answer, which should cite primary
  records.

| | A: Raw | B: Rolling summary | C: Structured records | D: Target-bound brief |
|---|---|---|---|---|
| Role | Evidence | Navigation | Durable decision record | Delivery |
| Default use in later stages | No | Navigation only | Yes | Yes, on demand |
| Main evidence | Zhang et al., abstract | Negative in Zhang et al. | None on outcomes | Li et al., abstract |
| Main failure | Sensitive and noisy if loaded | Silent loss | Under-reporting | Stale binding |

- **Trade-off.** The recommendation combines A for storage, C for durable decisions and D for
  delivery, with B limited to navigation. The added storage and generation cost buys the ability to
  trace a later decision back to its evidence. This combination is a [Proposal] and has not been
  tested on coding transcripts.

### 9.6 Conflict policy

#### Option A: Model arbitration

- **How it works.** The agent or a re-ranker chooses among conflicting sources, as listwise
  arbitration does in Re3.
- **Strengths.** It is automatic, and it does not interrupt the work.
- **Weaknesses.** Xu and Wu show agents following stale files after flagging them, STALE shows weak
  recognition of outdated state, and the outcome is hard to defend in audit.
- **Cost.** Its direct cost is low, and errors are found late.
- **Worked example (illustration).** It may fit ranking two informal tickets about a test
  environment. It does not fit two versions of a client restriction.

#### Option B: Single global precedence

- **How it works.** One rule applies, such as "existing code wins".
- **Strengths.** It is simple, and one sentence of this kind raised code-following choices from 4.2%
  to 91.4% in Xu and Wu.
- **Weaknesses.** Code is the wrong authority for a business rule. The same sentence could cause an
  agent to preserve a defect against an approved requirement.
- **Cost.** It is very low to implement, with a high cost for a wrong outcome on regulated logic.
- **Worked example (illustration).** It fits a code formatting convention. It does not fit a mandate
  precedence rule where the code is the defect.

#### Option C: Typed precedence with an engine-enforced stop

- **How it works.** Conflicts are classified as in section 8.3. Descriptive conflicts resolve by
  rule, and normative conflicts move the work to a blocked state and route to an owner. This option
  is a [Proposal].
- **Strengths.** It separates easy conflicts from those that need a person, and it leaves an
  auditable record.
- **Weaknesses.** It depends on correct classification, it can create too many stops, and it is
  untested.
- **Cost.** It has moderate engine and taxonomy costs, and it consumes owner time.
- **Worked example (illustration).** It fits a stale settlement cut-off in a document that disagrees
  with an approved requirement, which stops the work. It does not fit a low-risk prototype, where
  the stop would add delay without a control benefit, so a tier rule should disable it there.

| | A: Model arbitration | B: Global rule | C: Typed with stop |
|---|---|---|---|
| Interruption | None | None | Moderate |
| Regulated suitability | Low | Low | High |
| Evidence | Negative for agents | Positive on synthetic convention conflicts | Proposal only |
| Main failure | Confident wrong choice | Wrong authority | Stop fatigue or misclassification |

- **Trade-off.** Option C accepts interruption in exchange for a defensible outcome on normative
  conflicts, and it uses Option B's sentence within its descriptive class.

## 10. Capital markets illustrations

All cases in this section are illustrations written for this report. They are not sourced findings,
and no capital markets evidence on these methods was found.

### 10.1 Client mandate restrictions: a case where the model fits

- A change adds a restriction type to a pre-trade compliance engine.
- **Requirements.** The record cites the mandate clause, the compliance interpretation and a named
  owner, and the precedence between exclusions and concentration limits is stated explicitly. The
  ambiguity checklist covers ordering and tie-breaking, because models resolve those categories
  poorly.
- **Design.** An ADR records the evaluation order and the rejected alternative, and it points to a
  golden-file test that enforces the order.
- **Implementation.** The pack holds one task and the relevant identifiers. The current restriction
  list comes from the system of record through a read-only tool, and the agent has no other route to
  client data.
- **Test and review.** A test agent works from the requirement, and seeded violations establish
  which tests fail. An independent compliance technology reviewer sees the deviation list first.
- **Later change.** When the interpretation changes, the digest changes, and the affected design,
  tests and approvals become suspect.
- **Limit.** A schema can require a precedence rule to exist, but only a test or reviewer can
  establish that the rule is correct.

### 10.2 Client mandate restrictions: a case where the model does not fit

- A portfolio manager asks whether a specific trade is permitted today under a client's mandate.
- This is a runtime question for the restriction engine and its data, and it does not belong in
  delivery context. Answering it from a stored requirement or memory could give an outdated answer
  and could breach entitlements.

### 10.3 Settlement breaks: a case where the model partly fits

- Cross-border breaks increase after a change to instruction enrichment.
- **Where it fits.** Graph expansion finds recent changes, lineage identifies the requirement behind
  the changed code, and an `as_of` query retrieves the rule in force on each trade date.
- **Where it does not fit.** Break samples should stay in the live system, and a knowledge item
  written before a move to T+1 should not be served as current.
- **Routing.** If the cause is a misunderstood affirmation cut-off, the record should go to the
  requirement owner as a gap, with a regression test. Adding a coding rule alone would hide the
  cause.

### 10.4 Regulatory reporting: a case where the model fits with review limits

- A new reporting field depends on a future regulatory effective date.
- **Where it fits.** The obligation record holds the instrument, clause, version date and
  interpretation, and the `as_of` date retrieves the future rule. A schema compatibility check
  blocks the removal of a field used by a downstream reporting consumer.
- **Where it does not fit.** The platform cannot decide what a rule means. Generated regulatory text
  can contain omissions and fabrication, as legal-text Gherkin evaluations found in another domain
  ([arXiv 2508.20744](https://arxiv.org/pdf/2508.20744), Independent), so a named owner must approve
  the interpretation.

### 10.5 Counterparty hierarchies: a case for reading live data rather than storing it

- A change to credit exposure aggregation depends on how ultimate parent is resolved.
- **Where it fits.** The decision on cache tolerance belongs in an ADR, with a contract test on the
  hierarchy service, and code-graph expansion finds the callers.
- **Where it does not fit.** The hierarchy itself is relational data with a system of record, and it
  should be queried under entitlements. A hierarchy copied into a requirement would go stale without
  any digest changing.

### 10.6 Low-risk reporting utility: a case where the full model should not be applied

- A team fixes a formatting defect in an internal operations report.
- Full requirement records, ADRs and lineage would add review burden without a control benefit. A
  ticket, a regression test and a normal review are sufficient. The tier rule should be set in
  advance, so that the agent cannot choose the lighter path for a change in regulated scope.

## 11. Regulatory position

This section follows the confirmation status in the [handoffs
note](research_notes/AIDLC%20context%20across%20SDLC%20stages/handoffs_traceability_drift.md). It
is not legal advice, and all interpretations need review by compliance or legal staff.

- **No text read in this research sets a rule specific to AI-generated code.** Existing change rules
  already require evidence about who changed and who approved. The recommendation to record model
  and context is a reasoned control design, and it must not be presented to auditors as a quoted
  regulatory obligation.

| Text | Status | What was found | Limit |
|---|---|---|---|
| Federal Reserve SR 26-2 | Confirmed from primary text | Footnote 3 places generative and agentic AI models outside the guidance, and adds that risk management and governance practices should guide controls for tools not covered. It supersedes SR 11-7 and SR 21-8 ([letter](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm)). | It addresses model risk in a bank's models and is not the main control text for AI-assisted delivery. |
| OCC Bulletin 2026-13 | Confirmed from primary text | It issues the same guidance on 17 April 2026, and it says that the agencies plan a request for information on AI use ([bulletin](https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html)). | A request for information is planned, so the position may develop. |
| RTS 6 Article 5 (Regulation (EU) 2017/589) | Read in the UK legislation copy; EUR-Lex original not accessible | Firms must keep records of material changes to algorithmic trading software showing when a change was made, who made it, who approved it and its nature, and senior management designates a person to authorise deployment ([Article 5](https://www.legislation.gov.uk/eur/2017/589/article/5)). | It applies to algorithmic trading software. EU text should be confirmed. |
| RTS 6 Article 9 | Read in the UK copy | It requires annual self-assessment and validation. The UK page marks it as revoked under the Financial Services and Markets Act 2023 ([Article 9](https://www.legislation.gov.uk/eur/2017/589/article/9)). | UK applicability needs checking. |
| RTS 6 Article 28(3) | Read in the UK copy as adopted | It sets a five-year period for high-frequency trading order records ([Article 28](https://www.legislation.gov.uk/eur/2017/589/article/28/adopted)). | It does not establish a retention period for change records. |
| Delegated Regulation 2017/565 Article 72(1) | Read in the UK copy as adopted | Records must allow corrections to be identified with earlier contents retained, and must allow IT-based analysis ([Article 72](https://www.legislation.gov.uk/eur/2017/565/article/72/adopted)). | Its application to software change records is an interpretation. The retention period was not on the page read. |
| Digital Operational Resilience Act RTS 2024/1774 Article 17 and the Level 1 text | Not confirmed; needs compliance review | Secondary mirrors indicate requirements for independent change approval, documentation, fall-back procedures and emergency change handling ([mirror](https://www.springlex.eu/en/packages/dora/rts-rmf-regulation/article-17/)). | EUR-Lex returned empty responses. |
| SOX sections 302 and 404, PCAOB AS 2201 and AS 1105, SEC rules | Not confirmed; needs compliance review | Only secondary vendor material was available, describing program change as an IT general control domain. | Nothing specific to AI-generated code was found. |
| MiFID II Directive Article 16(6) and 16(7), and the retention period for algorithm change records | Not confirmed; needs compliance review | These texts were not read. | A five-year period should not be assumed from Article 28. |
| FCA review of algorithmic trading controls | Secondary snippet only; needs compliance review | A law firm report notes weak documentation of development and testing as a concern ([Reed Smith](https://www.reedsmith.com/articles/fca-multi-firm-review-of-algorithmic-trading-controls/)). | The FCA text was not read. |
| EU AI Act | Not researched; needs compliance review | See the item below. | No statement in this report relies on it. |

- **Recheck of [sdlc-context-graph.md](sdlc-context-graph.md) section 8.** That note says the
  Act's high-risk obligations under Annexes I and II take effect on 2 August 2026.
    - The research notes record that this claim was not researched in this round, so it is
      unverified. **The user should check it against the Act and any later amendment before reusing
      it.**
    - The writer's general recollection, which is not supported by any note and was not verified
      here, is that the Act's high-risk categories are set by Annexes I and III rather than I and
      II, and that the application dates differ between those categories. This is an additional
      reason to check both the annex references and the date.
    - Whether a coding tool or generated code falls within high-risk scope at all is a separate
      question, and no source read addresses it.
- **Proposed minimum change record.** The record below is a [Proposal], and only the first group has
  a textual basis, in RTS 6 Article 5 for algorithmic trading software.
    - **Fields traceable to a text:** when the change was made, who made it, who approved it and its
      nature.
    - **Fields recommended for reconstruction:** artefact identifiers and digests, approver role and
      independence, evidence reviewed, model identifier and version, context manifest digest, tool
      actions, test results, deployment and rollback references, and whether approval was granted
      against the final digest.
- **Attribution.** Treating the human submitter as the accountable author, with the agent recorded
  as a tool, fits [LLVM's policy](https://llvm.org/docs/AIToolPolicy.html) and the [Linux kernel's
  rule](https://docs.kernel.org/process/coding-assistants.html) that agents must not add
  `Signed-off-by` tags. A compliance owner should confirm whether this meets the "who made it" field
  in RTS 6 Article 5.
- **Independence.** A clean-context reviewer agent is closer to segregation of functions than a
  self-review, but no regulator text found says that an agent can meet such a requirement. Regulated
  scope should keep an independent human approver.

## 12. Measurement plan

The stage table and experiment designs below are a [Proposal]. Published use exists for the metric
families, but no one was found using this per-stage design, and no published target values exist for
these artefacts.

- **Three layers of measurement** are needed, because no single published measure of context quality
  exists across delivery stages.

| Stage | Retrieval metric | Task metric | Outcome that reveals poor context |
|---|---|---|---|
| Requirements | Recall of applicable policies and decisions against labelled identifiers; share in force | Markers resolved; faithfulness and coverage; testability | Changes after design approval; incidents from requirement gaps |
| Design | Recall of impacted components against the merged change; in-force ADR recall | ADR conflicts found at review | Unplanned components; rework at gates |
| Implementation | Used-to-loaded ratio; missing-context events | Spec-conformance; golden-task success; tokens and calls to first passing build | Rework commits; deviations per task |
| Test | Share of requirements supplied; recall of past incidents | Tests failing on violation; seeded-bug detection; false alarms; invented requirements | Escaped defects by requirement |
| Review | Availability of linked requirements and standards | Known-issue precision and recall; addressed rate; high-severity rate | Defects that passed review; median human time |
| Operations | Recall of change and incident records | Time to correct cause on replay | Change failure rate; time to restore |

- **Primary metric.** ID-based precision and recall should be primary, because artefacts have stable
  identifiers and labelling is therefore cheap. Ragas documents an ID-based variant
  ([Ragas](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/),
  Practitioner). The merged change provides ground truth for design, and the requirement trace
  provides it for test.
- **Recall floor.** Must-retrieve policy items should have a recall floor, and precision should be
  tracked as a cost measure, because missing a restriction is much worse than loading one irrelevant
  document. The floor value is an open decision.
- **Without-reference metrics.** These should serve only as online proxies, because they measure
  whether the output used the context rather than whether the context was right.
- **Golden task suite.** Tasks should come from the firm's own history for each stage, and they
  should include stale-context traps, conflicting-source traps and must-refuse cases. Each change to
  a rule, pack or retriever should run against the suite, in the same way as a code regression test.
  Uber's curated benchmark of commits with human labels is a vendor precedent
  ([uReview](https://www.uber.com/us/en/blog/ureview/)).
- **Ablation.** Items should be removed from stage packs to see whether results change, which is
  cheaper than a field experiment.
- **Field experiment.** The platform should randomise the context configuration by work item, and it
  should not randomise the presence of AI. METR's follow-up found that developers increasingly
  refused to work without AI and that 30% to 50% withheld tasks
  ([METR](https://metr.org/blog/2026-02-24-uplift-update/)), and developers have less reason to
  refuse a comparison between two packs.
- **Paired delivery metrics.** Throughput should be read together with change failure rate, rework,
  review time and the share of changes merged without human review. This follows from the conclusion
  of the DORA 2025 DevOps research report, which is unrelated to the Digital Operational Resilience
  Act, that AI amplifies an organisation's existing strengths and weaknesses
  ([DORA](https://dora.dev/research/2025/dora-report/)). Incident attribution must be defined before
  a baseline is taken, given Faros's caveat that one PR may link to several incidents.
- **Perception.** Self-reported improvement should not be used as evidence of speed, as
  [ai-dlc.md](ai-dlc.md) section 7.3 already notes.
- **Review effectiveness.** Seeded-fault audits should run periodically on non-production paths.
  Reviewer time and silent approvals are indicators only, since the EASE study's treatment of PRs
  without comments shows the limits of such signals.
- **Instrumentation.**
    - Raw traces should use OpenTelemetry with a thin firm-owned attribute layer holding stage, work
      item, pack version, and artefact identifiers and digests.
    - The upstream GenAI conventions appear to be unstable. The repository README shows no tagged
      releases as fetched in November 2026
      ([repository](https://github.com/open-telemetry/semantic-conventions-genai)), so attributes
      should be mapped at the collector.
    - Golden datasets and evaluators should stay in the firm's own repository, because Langfuse's
      migration guide states that scores do not carry across and experiments must be re-run
      ([Langfuse](https://langfuse.com/resources/engineering/migrate-from-langsmith.md), Vendor,
      secondary).
- **Decision rule.** A context item, rule or stage artefact should stay only if the measurements
  show a benefit or if it serves a stated audit need. A requirement-to-test link may have audit
  value regardless of its effect on delivery, and the record should state which reason applies.

## 13. Build order

This order is a [Proposal]. It extends [aidlc-context-management.md](aidlc-context-management.md)
section 11, and it differs from [sdlc-context-graph.md](sdlc-context-graph.md) section 9, which
starts with the code graph because its objective is retrieval efficiency rather than stage quality.
The recommendation assumes one bounded domain for the first pass.

1. **Fix the state model and record what was loaded.** These are items 1 and 2 in the earlier build
   order, and every later measurement depends on them.
2. **Create the baseline and a small golden suite.** Baseline metrics must exist before any stage
   artefact changes, and incident attribution should be defined here.
3. **Add identity and digests on one domain.** This step covers permanent identifiers, canonical
   digests, typed links and approval bound to a digest, and it adds event records in a simple
   append-only table.
4. **Implement the requirements record and gate.** This step covers origin labels, source spans,
   open question ownership, obligation records, and separate faithfulness and coverage reports.
   Scanners remain advisory.
5. **Build the requirement-to-test link.** This step adds the required conditions step, mutation or
   seeded checks, and evidence from CI. It comes early because it has the strongest stage-specific
   evidence, and it should be confirmed on real financial rules since the published tasks are small.
6. **Add validity filtering and typed conflict handling.** This step covers `as_of` queries, default
   exclusion of superseded items, the precedence sentence, engine-enforced stops, and fresh-agent
   probes.
7. **Add deterministic design conformance.** This step covers decision records for hard-to-reverse
   choices, contract and architecture checks, protected guardrail files, and detection of new
   dependencies and contract changes.
8. **Add implementation records.** This step covers structured deviations and decisions, transcript
   retention after a records decision, and first-pass review without the author's narrative.
9. **Add stage deny rules in the environment and suspect-link propagation.** Scope should be
   enforced through tools, tokens and environments, and any stale state should become visible to
   reviewers.
10. **Run the feedback ladder at levels 1 to 3.** Levels 4 and 5 should follow only after the scoped
    period produces evidence, and write access to the rule store should be monitored from the start.
11. **Add a derived graph and target-bound briefs.** A graph should be built only when measured
    queries need it and can be rebuilt from the stores. Briefs should be tested with ablation before
    wider use.

The following items should be deferred until evidence or a clear need exists: a broad business
ontology, numeric confidence on requirements, spec-as-source for production logic, automatic
bidirectional synchronisation, and automatic promotion of learned rules.

## 14. Open decisions

| Decision | Options | What the choice depends on | Who should decide |
|---|---|---|---|
| Engine base | Extend AWS AI-DLC, adopt a hosted variant, or build a separate engine | How much of the stage rules and audit taxonomy is reusable, and whether the file layout supports the multi-user requirement | Platform owner |
| First domain | Mandates, reporting, settlement or a low-risk internal service | The balance between learning value and regulatory exposure | Platform owner with the domain lead |
| Change tiers | Which changes require the full record and which remain light | Risk appetite, and who owns the tier rule | Engineering and risk |
| Requirement notation | EARS, RFC 2119 with scenarios, or an internal convention | A comparison on the firm's own tasks, because no external evidence selects one | Platform owner |
| Requirement store | Git, an existing management tool, or both with one authority | Whether a governed tool already holds these records | Platform owner and compliance |
| Precedence table | The order in section 8.3 and the exceptions to it | Firm policy, because the order expresses authority | Compliance, risk and architecture |
| Must-retrieve recall floor | A value and the item classes it covers | Baseline measurements and risk appetite | Risk and platform owner |
| Transcript retention | Duration, access and redaction | Records rules that were not researched here | Records and compliance |
| Approver independence | Whether an agent reviewer can count toward any control, and which roles can approve | A compliance reading of change rules | Compliance and internal audit |
| Tester visibility | Whether test agents see the implementation code, or only requirements and contracts | An internal experiment, because this is untested | Platform owner |
| Promotion thresholds | The occurrence count, replay requirement and owner at each ladder level | Evidence from the scoped period | Standards owners |
| Token budgets | Starting values per stage and tier | Ablation results | Platform owner |
| Attribution method | Trailers, Agent Trace, git-ai or an in-house record | An evaluation of attribution accuracy, and squash-merge handling | Platform owner and audit |
| Regulatory scope | Which jurisdictions and regimes apply | The texts listed as not confirmed in section 11 | Legal and compliance |

## Resources

### Existing notes and earlier research

- [aidlc-context-management.md](aidlc-context-management.md) describes stores, patterns, resume
  protocol and the first build order.
- [sdlc-context-graph.md](sdlc-context-graph.md) describes code graphs, work graphs, ontologies
  and traceability as a graph.
- [ai-dlc.md](ai-dlc.md) describes the method and adoption considerations.
- [specification-driven-development.md](specification-driven-development.md) describes the tool
  landscape and specification practice.
- [Knowledge graphs for coding agents](knowledge-graphs-for-coding-agents.md) describes code
  retrieval families and commercial context engines.
- [The research notes for this report](research_notes/AIDLC%20context%20across%20SDLC%20stages/)
  contain the full findings, gaps and source lists, including sources not cited here.

### Requirements

- [Orchid](https://arxiv.org/html/2604.21505v2), [arXiv
  2507.20439](https://arxiv.org/html/2507.20439) and [arXiv
  2609.29208](https://arxiv.org/html/2609.29208) measure requirement defects against code
  correctness.
- [ClarifyCodeBench](https://arxiv.org/html/2607.00711v2) and
  [ClarifyGPT](https://arxiv.org/abs/2310.10996) cover clarification.
- [arXiv 2609.03230](https://arxiv.org/abs/2609.03230) covers LLM detection of requirement issues
  against an INCOSE-based ground truth.
- [LENS](https://arxiv.org/abs/2606.25867) and [Inter2US](https://arxiv.org/pdf/2510.08622) cover
  extraction from transcripts and traceability to source.
- [arXiv 2508.20744](https://arxiv.org/pdf/2508.20744) evaluates Gherkin generated from regulation.
- [Spec Kit
  templates](https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md),
  [AWS AI-DLC requirements
  analysis](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md),
  [BMAD PRD
  template](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-prd/assets/prd-template.md),
  [OpenSpec concepts](https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md)
  and [Kiro feature specs](https://kiro.dev/docs/specs/feature-specs/) are the tool sources.

### Design and conformance

- [Zhou et al.](https://arxiv.org/abs/2504.20781), [Gupta et al.](https://arxiv.org/abs/2604.03826)
  and [GADR](https://arxiv.org/abs/2608.17694) cover LLM rationale and ADR generation.
- [Cai et al.](https://arxiv.org/abs/2606.12231) studies rule files and rule evolution.
- [Konrad et al.](https://arxiv.org/abs/2604.04990), [Larsen and
  Moghaddam](https://arxiv.org/abs/2606.13298) and [Zhu et al.](https://arxiv.org/abs/2605.02741)
  cover implicit architecture and erosion.
- [TLA+-Bench](https://arxiv.org/abs/2607.23425) and [Bisharat et
  al.](https://arxiv.org/abs/2606.05792) cover formal specification generation.
- [Thoughtworks Radar on architecture drift
  reduction](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)
  describes the combination of deterministic checks and LLM evaluation.

### Handoffs, traceability and drift

- [MAST](https://arxiv.org/html/2503.13657v3) and [MetaGPT](https://arxiv.org/html/2308.00352) cover
  multi-agent failure and structured communication.
- [Xu and Wu](https://arxiv.org/abs/2610.30571) test stale instruction files against code.
- [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) provides the
  spec-first, spec-anchored and spec-as-source taxonomy, and practitioner tests of the tools.
- [TraceLLM](https://arxiv.org/html/2602.01253) and
  [LiSSA](https://helmholtz.software/software/lissa) cover link recovery. The LiSSA figures are
  sample output.
- [Agent Trace](https://agent-trace.dev/), [git-ai](https://github.com/git-ai-project/git-ai), [LLVM
  AI tool policy](https://llvm.org/docs/AIToolPolicy.html) and [Linux kernel coding assistants
  guidance](https://docs.kernel.org/process/coding-assistants.html) cover attribution.

### Retrieval, memory and feedback

- [An et al.](https://arxiv.org/abs/2604.14227), [Re3](https://aclanthology.org/2026.acl-long.1180/)
  and [Reddy](https://arxiv.org/abs/2606.29178) cover temporal retrieval and noise.
- [STALE](https://arxiv.org/abs/2605.06527) tests recognition of outdated memories.
- [Zhang et al.](https://arxiv.org/abs/2605.12978), [Li et al.](https://arxiv.org/abs/2608.12847)
  and [AMA-Bench](https://arxiv.org/abs/2602.22769) cover consolidation, target-bound reuse and raw
  retention.
- [CodeCompass](https://arxiv.org/abs/2602.20048) records agent underuse of optional graph tools.
- [Stripe Minions part
  2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) and [BMAD
  theory of project
  context](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/) describe
  scoped context in practice.
- [Cisco on persistent memory
  compromise](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code)
  covers the promotion risk.

### Test, review and evaluation

- [Haeri and Ghelichi](https://arxiv.org/abs/2607.06636) and [Tufano et al.,
  2026](https://arxiv.org/abs/2608.17177) cover specification-grounded testing.
- [Tufano et al., 2024](https://arxiv.org/abs/2411.11401) and [Duma et
  al.](https://arxiv.org/html/2605.02273) cover review anchoring and agent PR review.
- [Uber uReview](https://www.uber.com/us/en/blog/ureview/) and [Atlassian
  RovoDev](https://arxiv.org/abs/2601.01129) are vendor accounts of AI review.
- [METR update](https://metr.org/blog/2026-02-24-uplift-update/), [DORA
  2025](https://dora.dev/research/2025/dora-report/) and
  [Faros](https://faros.ai/blog/ai-acceleration-whiplash-takeaways) cover outcomes, with the limits
  stated in section 3.3.
- [Ragas context
  precision](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/)
  and [OpenTelemetry GenAI
  conventions](https://github.com/open-telemetry/semantic-conventions-genai) cover instrumentation.

### Regulation

- [Federal Reserve SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm) and
  [OCC Bulletin 2026-13](https://www.occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html)
  were read in primary form.
- [RTS 6 Article 5](https://www.legislation.gov.uk/eur/2017/589/article/5), [Article
  9](https://www.legislation.gov.uk/eur/2017/589/article/9), [Article
  28](https://www.legislation.gov.uk/eur/2017/589/article/28/adopted) and [Regulation 2017/565
  Article 72](https://www.legislation.gov.uk/eur/2017/565/article/72/adopted) were read in UK
  legislation copies.
- [The Digital Operational Resilience Act Article 17
  mirror](https://www.springlex.eu/en/packages/dora/rts-rmf-regulation/article-17/) is a secondary
  source, and its content should be confirmed against the Official Journal.
