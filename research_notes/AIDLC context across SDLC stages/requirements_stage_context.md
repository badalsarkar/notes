# Requirements-Stage Context for an AI-DLC

Research date: 2026-11-01. These notes do not repeat the general context engineering or the tool overviews in `aidlc-context-management.md` and `specification-driven-development.md`.

**Evidence labels.** [Vendor] is a tool's own documentation or template, and shows what the tool is designed to do rather than whether it works. [Independent] is research by authors with no stake in the tool discussed. [Author-tool] is research in which the authors evaluate their own method or framework. [Practitioner] is one person's reported experience.

**Publication status.** Most papers cited here are arXiv preprints. They have not necessarily been peer reviewed, and exceptions are noted where known.

**How the sources were read.**
- WebFetch was unavailable, so pages were downloaded with curl.
- Tool templates were read closely from the `main` branch on the research date.
- Papers were read through keyword-targeted excerpts, not from start to finish. Figures are quoted from those excerpts.
- Items marked [snippet] rest only on a search-result summary and should be verified before they are relied on.

**Contents**
1. What requirements artefacts need to contain, and what the tools record
2. Which notations work best with LLMs
3. Research on elicitation, ambiguity, clarifying questions and requirement quality
4. Recording source material, provenance, open questions and assumptions
5. Failure modes

## 1. What do requirements artefacts need to contain, and what do the tools record?

### Takeaway
The tools now broadly agree on intent, functional requirements with stable identifiers, testable acceptance conditions, scope exclusions, assumptions and open questions. None of the templates reviewed records a per-requirement link to a stakeholder source, a confidence value or a named approver, and regulatory obligations are at most an optional section or a checklist category.

### Cited Findings

**Comparison of current artefacts (all [Vendor] unless noted)**

| Content | Spec Kit | AWS AI-DLC | BMAD | OpenSpec | Kiro | Tessl |
|---|---|---|---|---|---|---|
| Main file | `spec.md` | `requirements.md`, questions file, `traceability.json` | PRD | `proposal.md`, delta `spec.md` | `requirements.md` | `*.spec.md` |
| Intent or goals | User stories and measurable success criteria | Intent analysis | Vision, jobs to be done | Intent section | User stories | Not confirmed |
| Requirement form | `FR-001: System MUST` | `FR{n}`, `FR{n}.{m}`, `NFR{n}` | `FR-n` with testable consequences | `### Requirement` with RFC 2119 keywords | EARS | Requirements linked to tests |
| Acceptance form | Given/When/Then | Not fixed by the stage rule | "Consequences (testable)" | `#### Scenario` | EARS criteria | `[@test]` links |
| Non-goals | No template section; `/clarify` checks for them | Out of scope | Non-Goals section, and per FR | In and out of scope | Not confirmed | Not confirmed |
| Assumptions | Assumptions section | Assumptions with rationale | Inline `[ASSUMPTION]` tags and an index | Not seen in the concepts document | Not confirmed | Not confirmed |
| Open questions | `[NEEDS CLARIFICATION]`, at most 3 | Open questions section | Open Questions section | Not seen in the concepts document | Not confirmed | Not confirmed |
| Glossary | No template section; `/clarify` checks terminology | No required section | Mandatory, with synonyms prohibited | Not seen in the concepts document | Not confirmed | Not confirmed |
| Regulatory content | `/clarify` category | Not a required section; constraints only | Optional compliance section | Not seen in the concepts document | Not confirmed | Not confirmed |

"Not confirmed" means that I did not read enough of the source to say the item is absent.

**GitHub Spec Kit**
- The spec template's headings are User Scenarios & Testing, Edge Cases, Requirements, Functional Requirements, Key Entities, Success Criteria and Assumptions, with acceptance scenarios written as Given/When/Then. There is no glossary or non-goals heading, and the template's own example places "Mobile support is out of scope" under Assumptions. — [spec-template.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md)
- `/specify` instructs the agent to "make informed guesses", to use reasonable defaults documented under Assumptions, and to keep at most 3 `[NEEDS CLARIFICATION]` markers. If there are more, it keeps the 3 most critical and guesses the rest. It also tells the agent to avoid "HOW to implement". — [specify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/specify.md)
- `/clarify` scans the spec against a taxonomy and marks each category Clear, Partial or Missing. The categories are functional scope (including out-of-scope declarations), domain and data model, UX flow, non-functional attributes (including compliance and regulatory constraints), integrations, edge cases, constraints and trade-offs, terminology (canonical glossary terms and avoided synonyms), completion signals, and placeholders. — [clarify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/clarify.md)
- `/clarify` asks at most 5 questions in a session. Each is multiple choice or answerable in five words or fewer, and the agent presents a recommended option. Candidates are ranked by an Impact × Uncertainty heuristic. — [clarify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/clarify.md)
- Current `main` says to present exactly one question at a time. A diff in PR #1962 shows a variant that batches questions when an ask-user tool is available, so the behaviour may differ by version. — [clarify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/clarify.md); [PR #1962](https://github.com/github/spec-kit/pull/1962/files) [snippet]

**AWS AI-DLC**
- The stage produces `requirements.md`, `requirements-analysis-questions.md` and optionally `traceability.json`. The requirements file contains intent analysis, functional requirements, non-functional requirements, constraints, assumptions with rationale, out of scope and open questions. — [requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)
- FR and NFR identifiers are declared "permanent traceability keys" that later stages must not renumber. The JSON list holds `id`, `kind` and, for sub-requirements, `of`. — [requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)
- Completeness is assessed across six dimensions: functional, non-functional, user scenarios, business context, technical context and quality attributes. Depth is set to Minimal, Standard or Comprehensive. — [requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)
- The older path `aidlc-rules/aws-aidlc-rule-details/inception/requirements-analysis.md` now returns 404, so write-ups that cite it describe an earlier repository layout. — verified against the [repository tree](https://api.github.com/repos/awslabs/aidlc-workflows/git/trees/main?recursive=1)

**BMAD**
- The PRD's essential spine includes a purpose statement, vision, target users and numbered journeys (`UJ-n`), a glossary, features with nested `FR-n`, explicit non-goals, MVP scope, open questions and an assumptions index. — [prd-template.md](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-prd/assets/prd-template.md)
- The glossary rule says downstream workflows must use its terms exactly, and that introducing a synonym is "a discipline violation". The template says non-goals prevent the "let me also add this nearby thing" failure mode. — [prd-template.md](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-prd/assets/prd-template.md)
- Optional clusters for enterprise and regulated work include Stakeholders and Approvals, Risk and Mitigations, Data Governance, Audit Trail / Decision Provenance, and Compliance and Regulatory. — [prd-template.md](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-prd/assets/prd-template.md)

**OpenSpec**
- `proposal.md` captures Intent, Scope (in and out) and Approach. Requirements live in spec files under `### Requirement` headings with RFC 2119 keywords and `#### Scenario` examples, and changes are expressed as deltas such as `## ADDED Requirements`. — [concepts.md](https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md)

**Kiro**
- `requirements.md` "uses EARS (Easy Approach to Requirements Syntax) notation to provide structured, testable requirements". The current documentation offers Requirements-First, Design-First and Quick Spec feature workflows, and its navigation also lists Bugfix Specs. — [Kiro feature specs](https://kiro.dev/docs/specs/feature-specs/)
- Older information: in September 2025 Böckeler observed requirements written as "As a…" user stories with GIVEN/WHEN/THEN acceptance criteria, which differs from the current documentation's EARS description. — [Böckeler, 15 Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

**Tessl**
- Spec files end in `.spec.md`, carry a `targets` list in frontmatter, and interleave requirements with `[@test]` links. Registry pages show differing versions of the format. — [Tessl spec format](https://tessl.io/registry/tessl-labs/spec-driven-development/files/spec-format.md) [snippet]
- Tessl's specs sit close to code rather than at the stakeholder level. In September 2025 Böckeler saw a 1:1 mapping between spec and code file. A 2026 third-party review says regeneration is still closed beta and JavaScript-only, which I could not confirm from Tessl. — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html); [CodeMySpec review](https://codemyspec.com/blog/tessl-review) [snippet]

### Inferences
- A practical minimum for later agents is a stable ID, normative statement, testable condition, scope exclusion, glossary term, assumption with rationale, and open question with an owner. The first six fields are already present in at least one tool. The owner field on open questions is not in the templates I read.
- BMAD's mandatory glossary is the best fit for capital markets because terms such as "settlement date", "position" and "client" can differ by desk or system. A glossary entry should name the owning system or policy where definitions differ.
- Regulatory obligations should be a first-class record type rather than a constraint bullet. Each record should hold the instrument, clause, version date, interpretation and interpreting owner, because no reviewed tool models this.
- A typed store is preferable to one long document, because design and implementation agents need different slices. This is my design judgement and I found no comparative study.

### Gaps
- I found no controlled study showing which fields of a requirements artefact most affect downstream agent accuracy.
- I did not read Kiro's or Tessl's full templates, so the "Not confirmed" cells are open.

## 2. Which notations work best with LLMs?

### Takeaway
I found no study that directly compares EARS, Gherkin, user stories and structured YAML or JSON as inputs to code generation, so no notation can be called best on current evidence. The tools' choices reflect design preference, and the better-supported finding is that unambiguous, complete content matters and that Gherkin can be generated usefully with human review.

### Cited Findings
- **EARS:** I found no LLM evaluation of EARS in two targeted searches. Kiro has adopted it as its native notation, which is a product decision rather than evidence of accuracy. — [Wikipedia on EARS](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax) [snippet]; [Kiro docs](https://kiro.dev/docs/specs/feature-specs/) [Vendor]
- **Gherkin from regulation** [Independent; published version on [ScienceDirect](https://sciencedirect.com/science/article/pii/S0950584926001114?via=ihub%3D)]: 10 participants assessed 60 specifications from food-safety regulations generated by Claude and Llama, producing 120 assessments. Top-two ratings were relevance 95%, clarity 100%, completeness 94.2%, singularity 93.4% and time savings 91.7%. Participants still noted omissions, hallucinations and mixed intents. The time-savings figure is self-reported rather than measured. — [arXiv 2508.20744](https://arxiv.org/pdf/2508.20744)
- **Gherkin then executable tests** [Author-tool, industrial]: at an automotive partner, users rated 95% of generated scenarios helpful. Of the generated test scripts, 60% were usable as generated, 8% needed minor fixes, 24% needed regeneration with added input and 8% were discarded. — [arXiv 2504.07244](https://arxiv.org/html/2504.07244v1)
- **Gherkin generation strategy** [Author-tool; accepted at SEET 2026]: on 107 requirements from four documents, four expert raters scored an epic-organised pipeline above a requirement-aligned baseline on completeness (4.31 against 3.50). Its scenario density was also higher (1.12 against 0.60 per requirement), and the authors partly attribute the completeness rating to that density. — [arXiv 2607.01980](https://arxiv.org/html/2607.01980v1)
- **Citation annotations in specs** [Author-tool; the framework's own evaluation, per the indexed record a single-author preprint]: on 840 implementations across two models, a condition with per-line requirement citations enabled automated hallucination detection at 86.4% and 88.0%, against 0% for the alternatives, with a 0% false-positive rate. It also produced significantly lower output determinism than the uncited condition (d=-0.76 and d=-0.72). I read only the abstract. — [arXiv 2606.30689](https://arxiv.org/abs/2606.30689)
- **Format conventions in tools** [Vendor]: Spec Kit combines Given/When/Then with `MUST` statements, OpenSpec combines RFC 2119 with scenarios, Kiro uses EARS, and BMAD uses an actor-capability sentence with testable consequences. All are Markdown with light conventions, and AI-DLC is the only one of these where I saw a JSON sidecar for identifiers. — [Spec Kit](https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md); [OpenSpec](https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md); [Kiro](https://kiro.dev/docs/specs/feature-specs/); [BMAD](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-prd/assets/prd-template.md); [AI-DLC](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)
- **Practitioner caution:** Böckeler reports that Kiro produced "Given/When/Then"-style documents too verbose for a small bug, and notes that natural-language specs lose the parseable-structure benefits of model-driven development. — [Böckeler, Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [Practitioner]

### Inferences
- A sensible design separates two layers: machine-validated metadata (IDs, type, status, source links, approver) in YAML or JSON, and normative content in constrained natural language. This follows from what each form does well, and has not been tested as a comparison.
- A team can choose EARS or RFC 2119 for the normative statement and Given/When/Then for examples, because they serve different functions. Consistency is likely to matter more than the choice. This should be tested on the platform's own tasks by comparing pass rates and review time across notations.
- Example for a trade-affirmation feature: "When an allocation is received after the affirmation cut-off, the system shall flag it for manual review", with a Given/When/Then scenario that fixes the cut-off time and time zone. The notation forces a trigger to be stated, but does not resolve which cut-off applies, so a glossary or policy link remains necessary.

### Gaps
- There is no direct comparison of notations for code-generation accuracy, and this is the largest evidence gap in the question set.
- I found no study of structured YAML or JSON requirements against natural language for coding agents.

## 3. What does research show about elicitation, ambiguity detection, clarifying questions and requirement quality?

### Takeaway
Requirement defects measurably reduce generated-code correctness, with benchmark effects from about 7 points to more than 30 points of Pass@1 depending on model and defect type. Clarification helps, but models are poor at finding the ambiguity and asking the right question themselves, so the stage cannot rely on LLM self-assessment.

### Cited Findings

**Effect of requirement quality on code generation**
- **Orchid** [Independent benchmark]: 1,304 function-level tasks and 5,216 variants covering lexical, syntactic, semantic and vagueness ambiguity. Ambiguity reduced Pass@1 by an average of 7.22 points and at most 32.35 points, with a relative decline of 16.25%. The maximum is reported as 31.10 in v1 [snippet]. — [arXiv 2604.21505v2](https://arxiv.org/html/2604.21505v2)
- In the same study, ambiguity raised GPT-4's intra-model conflict rate from 14.09% to 28.29% and DeepSeek-V3's from 6.83% to 17.45%. The inter-model conflict rate rose from 51.04% to 57.28%. — [arXiv 2604.21505v2](https://arxiv.org/html/2604.21505v2)
- **Mutated prompts** [Independent]: drops of 25–30% for ambiguous and 20–25% for incomplete descriptions, on HumanEval and MBPP. Contradictory descriptions are summarised as "up to 40%", yet the same paper reports GPT-4 falling from 73.8% to 6.7% on contradictory HumanEval tasks, which is larger than that summary. The flaws were GPT-4-generated and then manually checked. — [arXiv 2507.20439](https://arxiv.org/html/2507.20439)
- In that study execution rates stayed high while the runnable-but-incorrect rate exceeded 80% for GPT-4 and several other models on contradictory descriptions. Defective requirements therefore tend to produce code that runs but is wrong. — [arXiv 2507.20439](https://arxiv.org/html/2507.20439)
- **Requirement smells** [Independent, described by its authors as exploratory]: on four game applications with GPT-4o and DeepSeek-V3, higher smell density was generally associated with lower correctness, but effects varied. DeepSeek-V3 on Dice fell from 88.0% to 77.6%, GPT-4o on Dice fluctuated between 74.4% and 80.0%, and both stayed high on Arkanoid. The strong correlations reported for GPT-4o did not survive Bonferroni correction, and statistical power was limited. — [arXiv 2609.29208](https://arxiv.org/html/2609.29208)
- Limits on these figures: most tasks are function-level or small applications, ambiguity is usually injected rather than naturally occurring, and several tested models are no longer current.

**Clarifying questions**
- **ClarifyGPT** (older, 2023 preprint; [ACM version](https://dl.acm.org/doi/10.1145/3660810)) [Author-tool]: detects ambiguity by sampling several solutions and checking whether they behave consistently, and asks questions only when they diverge. With ten participants, GPT-4 improved from 70.96% to 80.80% on MBPP-sanitized. With simulated users across four benchmarks, GPT-4 improved from 68.02% to 75.75% and ChatGPT from 58.55% to 67.22%. — [arXiv 2310.10996](https://arxiv.org/abs/2310.10996)
- **ClarifyCodeBench** [Independent benchmark]: 419 annotated ambiguous tasks, evaluated on GPT-4o, GPT-5, Gemini 2.5 Flash, Claude Sonnet 4.5, DeepSeek-V3.2 and Qwen3. The best early-key-question score (TKQR) was 0.30 and the best round-adherence score (ORA) was 0.50. — [arXiv 2607.00711v2](https://arxiv.org/html/2607.00711v2)
- Even after the clarification pipeline, Pass@1 stayed 7.8 to 19.8 points below complete requirements. When two key questions were needed, the best rate of asking both was 0.08. — [arXiv 2607.00711v2](https://arxiv.org/html/2607.00711v2)
- Reasoning modes improved code under complete requirements more than they improved clarification. Claude Sonnet 4.5's Pass@1 under complete requirements rose from 48.8 to 50.0, while its Pass@1 under ambiguity fell from 38.2 to 34.3. — [arXiv 2607.00711v2](https://arxiv.org/html/2607.00711v2)
- Resolution varied by ambiguity type. Units reached 66.7% and numerical precision 100% for each of DeepSeek-V3.2, Gemini 2.5 Flash and GPT-4o, whereas collection semantics stayed at or below 16.7% and comparison rules at or below 12.5%. Ordering and atomicity were resolved by only two models. — [arXiv 2607.00711v2](https://arxiv.org/html/2607.00711v2)
- Oracle clarification, where the annotated questions and answers were given as dialogue context, improved results but remained slightly below receiving the complete requirement. — [arXiv 2607.00711v2](https://arxiv.org/html/2607.00711v2)
- **HumanEvalComm** (older, 2024) [Independent]: introduced the Communication Rate and Good Question Rate metrics. ClarifyCodeBench's authors argue that it does not support precise evaluation of clarification quality [snippet]. — [arXiv 2406.00215](https://arxiv.org/pdf/2406.00215); [arXiv 2607.00711v2](https://arxiv.org/html/2607.00711v2)
- **ClarifyCoder** [Author-tool]: fine-tunes a code model with synthetic data to seek clarification, motivated by the observation that earlier methods force interaction even on clear tasks. I did not extract its numeric results. — [arXiv 2504.16331](https://arxiv.org/pdf/2504.16331)

**Ambiguity and quality detection**
- Orchid found that LLMs tend to treat most requirements as ambiguous, with precision around 50%. Localisation rarely exceeded 23% and resolution stayed below 64%. — [arXiv 2604.21505v2](https://arxiv.org/html/2604.21505v2)
- Code models classified clear and unclear descriptions with an MCC of only -0.1 to 0.55. — [arXiv 2507.20439](https://arxiv.org/html/2507.20439)
- Against an INCOSE-based expert ground truth, across ten OpenAI and Anthropic models, the best model detected a median 47% of issues and false-flagged 11%. Necessity and correctness issues were almost always missed, and newer models were not reliably better. I read only the abstract. — [arXiv 2609.03230](https://arxiv.org/abs/2609.03230) [Independent]
- In a requirements-from-code study, generated requirements had a 24.5% smell rate. Neither an LLM nor a single human reviewer detected smells reliably, and inter-rater agreement was fair at best. — [arXiv 2606.25550](https://arxiv.org/html/2606.25550)

**Elicitation from conversations**
- **LENS** [Author-tool, industrial, preliminary]: on twelve transcripts from a security operations centre, best extraction of explicit requirements reached precision 73%, recall 100% and F1 84.4%. 66% of false positives came from mentions of manual work being read as requirements. The first author built the ground truth, which domain experts validated. — [arXiv 2606.25867](https://arxiv.org/abs/2606.25867)
- **LLMREI** [Author-tool]: across 33 simulated interviews, the bot made a similar number of common interview mistakes to a human and elicited up to 73.7% of requirements. The authors had to instruct it to ask one question at a time. Stakeholders were simulated, so this may not carry over to real interviews. — [arXiv 2507.02564](https://arxiv.org/html/2507.02564v1)

### Inferences
- Execution-based divergence, as in ClarifyGPT, may be a stronger ambiguity signal than asking a model whether a requirement is clear. Orchid's conflict-rate data support the principle, but multi-solution sampling is costly and has been shown mainly at function level.
- The weak results for ordering, atomicity, comparison rules and collection semantics matter for capital markets. Examples include event ordering in order books, tie-breaking in allocation, and whether corporate-action adjustments apply before or after netting. A platform should ask about these with domain checklists rather than relying on model initiative.
- Numbers and units appear easier for models to resolve, but this does not establish that domain conventions such as day-count or rounding rules are safe. Those should be stated explicitly.
- Oracle clarification falling short of a complete requirement suggests that answers should be merged into the normative requirement, not merely stored as a transcript. The evidence is indirect and the gap is described as slight.
- A precision near 50% implies that an unfiltered ambiguity scanner would generate many unnecessary questions. Spec Kit's impact ranking and capped question count is one way to manage this, though I found no evaluation of it.

### Gaps
- I found no independent study measuring requirement quality against code accuracy for multi-file enterprise work or for capital markets.
- I found no independent evaluation of Spec Kit `/clarify`, or of any tool's clarification step, on outcomes.
- I did not retrieve a dedicated recent survey of requirements engineering for LLMs. A 2026 systematic review exists on [AI agents for RE automation](https://doi.org/10.3390/automation7050169), and I did not read it.

## 4. How should raw source material, provenance, open questions and assumptions be recorded?

### Takeaway
Research prototypes link each derived requirement to transcript excerpts, and AI-DLC treats raw input as separate, untrusted, verbatim data, but no reviewed tool stores a claim-level source link with an approver. The platform will have to design that record itself, and the evidence supports keeping the source immutable and the distilled requirement separately editable.

### Cited Findings

**Linking requirements to source**
- LENS represents extracted and inferred requirements as user stories linked to transcript excerpts for traceability, and gives a rationale for inferred requirements. — [arXiv 2606.25867](https://arxiv.org/abs/2606.25867) [Author-tool]
- Inter2US defines two metrics: requirements faithfulness (the share of stories supported by a transcript segment) and interview coverage (the share of segments supported by a story). An LLM matcher achieved 0.86 macro-F1 across four annotated datasets. It uses overlapping three-turn chunks, and each positive match is concrete evidence that can be shown during review. — [arXiv 2510.08622](https://arxiv.org/pdf/2510.08622) [Author-tool]
- In that study faithfulness was consistently high except for the smallest generator, and coverage increased with generator size. The authors note that this asymmetry reflects a familiar pattern in which requirements are individually valid but incomplete. Coverage is not the same as completeness. — [arXiv 2510.08622](https://arxiv.org/pdf/2510.08622)
- Human-written stories scored lower on faithfulness than most LLM sets because students could use sources beyond the transcript. A low faithfulness score therefore does not by itself identify a fabrication. — [arXiv 2510.08622](https://arxiv.org/pdf/2510.08622)

**How tools treat raw input and answers** [Vendor]
- AI-DLC retrieves the project description through a fixed command and uses it verbatim as the authoritative request, and forbids reconstructing it from the audit log. Pasted `<document>` blocks are split from the user's directions. Document content is treated as untrusted data that cannot redirect the workflow. — [requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)
- AI-DLC stores answers in a questions file using `[Answer]:` tags and refuses to proceed with partial answers. It scans for vague language such as "mix of", "not sure" and "depends", checks for contradictions, and asks follow-up questions. — [requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)
- AI-DLC can require a consolidated summary confirmation before generation, with a logged decision and a receipt, followed by an Approve or Request Changes gate. Its reviewer is `advisory` with at most 2 iterations. — [requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)
- Spec Kit records each answer as `- Q: <question> → A: <answer>` under `## Clarifications` and `### Session YYYY-MM-DD`, and applies it to the relevant section. If an answer invalidates an earlier statement, the statement is replaced with "no obsolete contradictory text" left behind. Unasked high-impact items are flagged as Deferred in the completion report, which is not necessarily persisted to the spec. — [clarify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/clarify.md)
- BMAD requires inline `[ASSUMPTION: ...]` tags wherever the agent inferred without confirmation, with an index "surfaced for explicit confirmation". Open questions are recorded so they become "future tickets or follow-up research, not silent gaps". — [prd-template.md](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-prd/assets/prd-template.md)
- The AI-DLC `traceability.json` schema shown holds `id`, `kind` and `of`, with no source, confidence or approver field. — [requirements-analysis.md](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)

### Inferences

**Recommended record, as a design proposal rather than a tested standard:**

```yaml
id: REQ-142                 # permanent, never renumbered
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
approved_at: 2026-10-20
supersedes: REQ-097
```

- **Verbatim retention:** source material should be stored immutably with a capture date and hash, and transcripts should be segmented so that requirements can cite a span. Spec Kit's replacement rule keeps the current spec clean, but history then relies entirely on version control and the Q/A bullet.
- **Separate current state from history:** the agent-facing artefact should show only the current requirement, while an append-only record retains superseded wording. This preserves Spec Kit's benefit of having no contradictory text, while adding the audit trail a regulated firm needs.
- **Origin rather than numeric confidence:** a categorical `stated`, `inferred` or `agent-assumed` field is more defensible than a model-reported percentage, because I found no evidence that such confidence values are calibrated for requirements. Reviewers can then concentrate on inferred items, and implementation agents can be told not to treat assumptions as confirmed.
- **Unresolved questions** need an ID, the question, the affected requirements, the owner, a blocking flag, a due date and the provisional default if there is one. A blocking question should stop the handoff, and a non-blocking one should travel into design.
- **Authority hierarchy:** the record should state which source prevails. For example, a desk head's statement in a meeting should not override a compliance interpretation of a clause, even when it is more recent. Source documents should remain untrusted data, following AI-DLC's approach, since emails and tickets can contain instruction-shaped text.
- **Approval scope:** approval should attach to individual requirements or a versioned set, and changes should invalidate it. A regulatory interpretation should be approved by the named compliance owner rather than by the engineer running the workflow. Entitlements on sources such as client emails or restricted-list material also carry over to derived requirements, and a requirement quote should not expose them.

### Gaps
- I found no study of the best granularity for provenance links, or of whether provenance links improve downstream agent accuracy as distinct from reviewer efficiency.
- I found no empirical evidence on calibrated confidence for extracted requirements.
- I found no capital-markets case study showing transcript-to-requirement provenance in production, nor regulatory guidance specific to AI-generated requirements. I did not search regulator sources in depth.

## 5. Failure modes

### Takeaway
The documented risks are omission and hallucination in generated specifications, assumptions made silently, verbose output that reviewers cannot absorb, and agents that do not follow the spec. Fabrication appears lower-rate than omission in the limited evidence available, though measurements are small and most drift evidence is anecdotal.

### Cited Findings

**Fabricated requirements**
- Legal-text Gherkin evaluations reported occasional omissions and hallucinations, and concluded that systematic human review is required. — [arXiv 2508.20744](https://arxiv.org/pdf/2508.20744)
- A requirements-from-code study measured a 6.1% hallucination rate (1.8% on one project and 10.3% on another). There were only 7 hallucinations in total, so the authors limit generalisation. The direction here is code to requirements, not stakeholder input to requirements. — [arXiv 2606.25550](https://arxiv.org/html/2606.25550)
- LENS false positives show one specific form of fabrication: descriptions of current practice being turned into requirements. — [arXiv 2606.25867](https://arxiv.org/abs/2606.25867)
- LLMREI reports that interview bots can hallucinate, carrying errors into summaries [snippet]. — [arXiv 2507.02564](https://arxiv.org/pdf/2507.02564)

**Silent assumption**
- ClarifyCodeBench's authors state that when details are missing, LLMs "often make implicit assumptions and produce code that does not match the intended behavior", and its models tended to ask fewer questions than annotated. — [arXiv 2607.00711v2](https://arxiv.org/html/2607.00711v2)
- Spec Kit's `/specify` instructs guessing beyond 3 open markers. The guesses are meant to be documented, but compliance is not guaranteed since checklists are interpreted by AI. — [specify.md](https://raw.githubusercontent.com/github/spec-kit/main/templates/commands/specify.md) [Vendor]; [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [Practitioner]

**Over-specification and review burden**
- Kiro turned a small bug into 4 user stories with 16 acceptance criteria. — [Böckeler, Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [Practitioner; tools have since changed, and Kiro now offers Quick Spec and Bugfix options]
- On a 3–5 point feature, Spec Kit created many repetitive markdown files, and Böckeler wrote "I'd rather review code than all these markdown files". — [Böckeler, Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [Practitioner]
- AI-DLC's scaling by depth and BMAD's "scope dial" are vendor responses to this problem, and I found no evaluation of either. — [AI-DLC](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md); [BMAD](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/skills/bmad-prd/assets/prd-template.md)

**Agents not honouring the record, and false control**
- Böckeler saw agents ignore instructions despite the files and checklists. In one case an agent treated research notes describing existing classes as a new specification and duplicated them. In others it followed a constitution article too eagerly. — [Böckeler, Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [Practitioner]

**Requirement drift**
- Böckeler observes that Spec Kit's per-spec branch suggests the spec lives for the change request rather than the feature, and that maintenance strategy is often left vague. — [Böckeler, Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [Practitioner]
- Regenerating from the same spec showed non-determinism even at a low abstraction level. — [Böckeler, Oct 2025](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) [Practitioner]
- OpenSpec's delta model and AI-DLC's permanent IDs are vendor mechanisms for controlling drift. — [OpenSpec](https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md); [AI-DLC](https://raw.githubusercontent.com/awslabs/aidlc-workflows/main/core/aidlc-common/stages/inception/requirements-analysis.md)

**Over-reliance on automated quality gates**
- The best model detected a median of only 47% of expert-identified requirement issues, and the authors warn that orchestrating such modules in agentic architectures may compound the deficiencies. — [arXiv 2609.03230](https://arxiv.org/abs/2609.03230) [Independent]

### Inferences

| Failure mode | Control proposed | Evidence basis |
|---|---|---|
| Fabricated requirement | Require a source span for `stated` items, and run a faithfulness check | Inter2US and citation studies; effect in production untested |
| Omission | Report uncovered transcript segments and clause coverage to reviewers | Inter2US coverage; coverage is not completeness |
| Silent assumption | Tag `agent-assumed`, block approval until confirmed or rejected, and count them per spec | BMAD and AI-DLC conventions; no outcome evidence |
| Over-questioning | Rank questions by impact, cap them per session and batch the rest as non-blocking | Orchid's precision near 50%; Spec Kit design |
| Over-specification | Scale artefacts by change type, and do not generate criteria without a source | Böckeler anecdote; AI-DLC and BMAD design |
| Review burden | Show reviewers a diff, the inferred items and the regulatory items first, instead of the whole document | My judgement; no study found |
| Drift | Use permanent IDs, deltas, supersession links and approval invalidation on change | Vendor mechanisms; no outcome evidence |
| Agent ignores record | Check code and tests against requirement IDs deterministically, rather than relying on instructions | Böckeler's observations; citation study supports verifiability, at a cost to determinism |

- Faithfulness checks and coverage checks answer different questions, and a platform needs both. High faithfulness with low coverage is the expected pattern, so a capital-markets team should worry at least as much about a missed requirement, such as an omitted exception flow for failed settlements, as about an invented one.
- Automated scanners should be presented as prompts to human reviewers rather than as gates that certify quality, because a clean scan misses about half of expert-identified issues in the best reported case.

### Gaps
- I found no direct measurement of fabricated requirement rates in tool-generated specs from Kiro, Spec Kit, BMAD, OpenSpec or AI-DLC.
- I found no controlled study of review time, or of defect escape, for long generated specs. The evidence is practitioner anecdote, and the main account dates from October 2025 and reflects tool versions from September 2025.
- I found no longitudinal measurement of requirement drift across agent-driven delivery.
