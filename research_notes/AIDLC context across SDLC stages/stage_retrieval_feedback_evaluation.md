# Context Across SDLC Stages: Stage-Scoped Retrieval, Downstream Feedback and Evaluation

Research date: 1 November 2026. This note extends sections 7 and 9.3 to 9.9 of `aidlc-context-management.md` and sections 6 and 7 of `sdlc-context-graph.md`, and does not repeat their findings.

Each finding carries one or more evidence labels.

- **[Independent]** means academic or other work by parties without a product interest in the result. Most such papers are unreplicated.
- **[Vendor]** means a company reporting on its own product or platform.
- **[Practitioner]** means a project document, community artefact or individual report with no outcome measurement.
- **[Secondary]** means I read a write-up or a search excerpt rather than the primary source.
- **[Abstract]** means I read only the abstract or landing page.
- **[Older]** means the information predates 2026 and may be out of date.

Contents:

1. Stage-scoped assembly
2. Retrieval quality for non-code artefacts
3. What implementation produces for later stages
4. Feedback from test, review and production
5. Evaluation
6. Human review

## 1. Stage-scoped assembly: what each stage needs and is denied

### Takeaway
The tools publish a consistent pattern of narrow, stage-specific artefacts and rules, but I found no controlled study that compares stage-scoped context with unscoped context in a delivery workflow. Explicit denial is rare in the tools and is mostly expressed as a prohibition on content or as a limit on tools and environments, so a per-stage deny list is largely a design inference rather than an established practice.

### Cited Findings

**Tool and framework patterns**

- Spec Kit's specify template explicitly excludes implementation detail: "Avoid HOW to implement (no tech stack, APIs, code structure)", and it asks the author to focus on what users need and why. This is the clearest published example of denying a stage a category of content. [Practitioner] — [Spec Kit, spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Spec Kit requires unknowns to be marked `[NEEDS CLARIFICATION: specific question]` rather than guessed, and a checklist requires that no markers remain before the requirements count as complete. It describes checklists as "unit tests" for the specification. [Practitioner] — [Spec Kit, spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- Spec Kit enforces its nine-article constitution at planning through "Phase -1" gates such as Simplicity and Anti-Abstraction. Its plan stays high-level, with code and detailed algorithms moved to `implementation-details/`. `/speckit.tasks` requires `plan.md` and reads `data-model.md`, `contracts/` and `research.md` when they exist, which amounts to an artefact-level manifest for the stage. [Practitioner] — [Spec Kit, spec-driven.md](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- BMAD version 4 breaks large PRD and architecture documents into smaller sections or individual stories, and has the scrum master agent select what the current story needs. The developer agent implements one story at a time, each agent works in a new chat, and QA review follows. `devLoadAlwaysFiles` lists the files the developer agent loads for every task. I read this through search excerpts of third-party mirrors. [Practitioner] [Secondary] [Older] — [BMAD workflow guide v4.29.6 mirror](https://git.biohazardvfx.com/Nicholai/BMAD-METHOD/src/tag/v4.29.6/docs/bmad-workflow-guide.md); [BMAD knowledge base mirror](https://cdn.jsdelivr.net/npm/@ptnglobal/bmad-method@4.43.1/bmad-core/data/bmad-kb.md); [Tessl-hosted API patterns](https://tessl.io/registry/tessl/npm-bmad-method/files/docs/reference/api-patterns.md)
- BMAD's current documentation has moved away from that presentation. It describes a loop of Clarify, Plan, Build and verify, and Learn and adjust, and its landing page does not mention sharding. The older `bmad-generate-project-context` skill is deprecated in favour of a verified block in `AGENTS.md`. Anyone citing "BMAD story files and sharding" should state the version. [Practitioner] — [BMAD docs](https://docs.bmad-method.org/); [Set and maintain project context](https://docs.bmad-method.org/existing-codebases/set-and-maintain-project-context/)
- BMAD's current theory of project context limits the always-loaded block to facts that are expensive to rediscover, policy the code cannot express, divergences from ecosystem defaults, pitfalls from observed failures, and prohibitions that name a permitted alternative. It excludes file maps, overviews, style rules and history. It separates implementation context, which lives in the code repository, from planning context, which it says is "consulted in bursts rather than loaded continuously". It also states that "an index the agent must choose to fetch gets skipped; an index already in context does not", without published data for that sentence. [Practitioner] — [Theory of project context](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/)
- Kiro steering files have four inclusion modes: always, fileMatch (a glob in front matter), manual (a `#` reference in chat) and auto (matched from a description field). `AGENTS.md` does not support these modes and is always included. The official documentation could not be fetched from this environment, so this comes from community guides. [Practitioner] [Secondary] — [Book of Kiro, steering](https://kiro-community.github.io/book-of-kiro/en/features/steering)
- A user report states that fileMatch does not trigger for global steering files, which is unconfirmed by Kiro. [Practitioner] — [Kiro issue 9176](https://github.com/kirodotdev/Kiro/issues/9176)
- Kiro produces three documents per task (requirements, design, tasks). Spec Kit produced eight files in Böckeler's test, each spec on its own branch. Tessl used a one-to-one mapping from spec to code file, with generated code marked "DO NOT EDIT", and it was in private beta in that test. [Independent, Thoughtworks practitioner] [Older: tested September 2025] — [Böckeler, martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Agents do not reliably follow scoped context. Böckeler frequently saw instructions skipped, saw Spec Kit's agent treat research notes on existing classes as new specifications and generate duplicates, and saw it apply a constitution article too eagerly. [Independent, anecdotal] [Older] — [Böckeler, martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)

**Platform teams**

- Stripe uses global rules "very judiciously" and attaches most rules by subdirectory or file pattern as the agent traverses the filesystem. Its central MCP server has nearly 500 tools, of which minions receive an intentionally small default subset, and engineers can add thematically grouped sets. [Vendor] — [Stripe Minions part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- Stripe's denial is enforced by the environment and not by the prompt. Minions run in QA-environment devboxes with no access to real user data, production services or arbitrary network egress, and a control framework blocks destructive MCP actions. [Vendor] — [Stripe Minions part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- Stripe's blueprints mix deterministic nodes (run linters, push) with agent nodes (implement task, fix CI failures), and the standard blueprint allows at most two CI runs before handing the branch to a human. More than 1,300 pull requests per week are merged with minion-written code and human review. The article states no rule-file count, size limit or token budget. [Vendor] — [Stripe Minions part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- Uber's uReview does not run one general reviewer. Comments pass through generation, filtering, validation and deduplication, with confidence thresholds tuned per assistant, language and category. [Vendor] [Older: August 2025] — [Uber uReview](https://www.uber.com/us/en/blog/ureview/)
- Uber's and Atlassian's work graphs are covered in `sdlc-context-graph.md` section 5. I found no new published stage-level token budgets from either company.

**Evidence bearing on what a stage should see**

- Grounding a test-writing agent in the specification improved results far more than adding tests. Holding the tester, budget and repair loop fixed, a one-line prompt change that supplied the specification produced correct code 38 points more often across three Claude models and 36 points more on a held-out set. It gained 28 points on GPT-5.3-codex and 19 points on Gemini 3.5 Flash (sign test over 18 tasks, p=0.002). Doubling the test budget barely helped. The tester found 27 of 30 bugs with the specification as a plain paragraph, against 2 of 30 without it. The false-alarm rate fell from 33% to 0%. The tasks are small and the benefit disappeared on well-specified algorithmic problems. [Independent] [Abstract] — [Haeri and Ghelichi, arXiv 2607.06636](https://arxiv.org/abs/2607.06636)
- In the same study, a property-based generator caught 28 of 30 bugs but invented requirements outside the specification. This is a precise illustration of a test stage operating without a requirement boundary. [Independent] [Abstract] — [arXiv 2607.06636](https://arxiv.org/abs/2607.06636)
- Requiring an agent to write pre-conditions, post-conditions and undefined behaviours before generating tests improved bug detection by 9.8 points (p=0.0352) and branch coverage by 2.5 points (p=0.0034) on Google production bugs. The authors are from Google, and the paper is a workshop paper at SpecOps 2026. [Vendor-affiliated research] [Abstract] — [Tufano et al., arXiv 2608.17177](https://arxiv.org/abs/2608.17177)
- LLM code review is affected by framing. A test of four models on 250 CVE vulnerability and patch pairs under five framing conditions found confirmation bias, with false-negative bias exceeding false-positive bias. I read only search excerpts. [Independent] [Secondary] — [arXiv 2603.18740](https://arxiv.org/html/2603.18740v1)

### Inferences

The following matrix is my synthesis. Only the entries marked with a citation number have direct support: (a) Spec Kit, (b) arXiv 2607.06636 and 2608.17177, (c) arXiv 2603.18740, (d) Stripe. All other entries are reasoned design choices.

| Stage | Should receive | Should be denied or deferred | Assembly mechanism |
|---|---|---|---|
| Requirements | Source request, stakeholder records, applicable policies and regulation with effective dates, prior decisions, glossary or ontology terms | Technology stack, API and code structure (a); current code as a default input, because it anchors requirements on what exists | Retrieval by policy and domain tag, plus a clarification marker rule |
| Design | Approved requirements by ID, ADRs in force, code graph expansion from impacted components, constraints, non-functional requirements | Superseded ADRs unless marked as such; raw elaboration transcripts | Graph expansion from the work item, limited to one or two hops |
| Implementation | The single task and its acceptance criteria, relevant design decisions by ID, scoped rules, tools | Other units' tasks, production data and production credentials (d), the wider tool catalogue (d), full requirements documents | A story-file or task pack built by a previous stage, plus just-in-time code search |
| Test | Requirements and acceptance criteria (b), contracts, past incident cases for the component | The implementer's account of what the code does. Hiding the code itself is untested and is costly for white-box coverage, so I would defer only the narrative | Retrieval by requirement ID, and a required step that writes pre- and post-conditions (b) |
| Review | Diff, linked requirements, scoped standards, test evidence, deviation log | The author's rationale and the agent's claim that the change is correct or safe, at least on a first pass (c); the implementation transcript | Independent first pass, then the rationale is revealed for a second pass |
| Operations | Runbooks, deployment and change records, read-only telemetry | Write access to production without approval; unverified agent memory as a basis for action | Graph expansion from the alert or the service to recent changes and past incidents |

- Denial is more reliable when enforced by a tool or environment than by a prompt, because the evidence shows agents both skip and over-apply instructions. Stripe's QA environment is the model for this. For a capital markets platform, the equivalent is that a development agent should have no route to client positions, trade data or restricted lists, whatever the instructions say.
- Retrieval by artefact ID should be the default inside a work item, because the previous stage knows exactly what it produced. Semantic search suits the case where nobody knows the relevant ID, such as a precedent ADR or a policy not yet linked. This agrees with the manifest in section 9.3 of `aidlc-context-management.md`, and adds the rule that the ID-linked items are mandatory and the searched items are optional.
- The BMAD claim about skipped indexes suggests that required items should be pushed by the engine rather than left to agent choice. On-demand tools should be reserved for material that really is optional.
- The test-grounding results are the strongest stage-specific evidence in this note, and they indicate that the requirement-to-test link is where context assembly may pay back most. A settlement-cycle change or a client mandate restriction is the kind of case-rich rule where this is likely to apply, though the published studies use small programming tasks and not financial rules.

### Gaps
- I found no published token budgets per stage from any of the named tools or platform teams, and no study that compares budgets. Any figure in a design is therefore a starting assumption to be measured.
- I found no controlled study of denying particular content to a stage, including the question of whether test agents do better without seeing the implementation.
- I found no current primary information on Tessl's context handling. The Böckeler description dates from 2025, and the search for its registry returned nothing usable.
- I found no primary evidence from Atlassian on stage-specific context packs beyond what the earlier notes record.

## 2. Retrieval quality for non-code artefacts

### Takeaway
The most relevant evidence shows that outdated documents actively mislead models and that re-rankers prefer older, richer documents, so validity must be established before relevance ranking and not left to the model. There is little direct evidence on requirements, ADRs or policy corpora, and the findings below transfer from general and Wikipedia-derived benchmarks.

### Cited Findings
- Existing re-rankers show "a strong bias toward older, semantically rich documents, even when they are factually obsolete". FRESCO tests this with queries seeking recent information against historical Wikipedia revisions. Optimised re-ranker instructions improved evolving-knowledge performance by up to 27% while staying competitive on non-evolving tasks. The authors are from Meta Superintelligence Labs and UCLA. [Independent of any retrieval product] [Abstract] — [An et al., arXiv 2604.14227](https://arxiv.org/abs/2604.14227)
- Semantic relevance and temporal validity are separate requirements in FRESCO's design, and neither is sufficient alone. [Abstract] — [arXiv 2604.14227](https://arxiv.org/pdf/2604.14227)
- Re3 pairs a time-aware dual relevance encoder with a conflict-aware recency filter that performs listwise arbitration to suppress obsolete versions. On its own benchmark of more than 1.3 million instances, it reports an average gain of 9.7% in generation accuracy over the strongest baselines. [Independent, authors' own benchmark] [Secondary] — [Cao et al., ACL 2026](https://aclanthology.org/2026.acl-long.1180/)
- The HoH benchmark found that outdated passages substantially reduce accuracy by distracting models from correct information, and that they can mislead models even when current information is available. [Independent] [Secondary] [Older: ACL 2025] — [Ouyang et al., ACL Anthology listing](https://aclanthology.org/people/jie-ouyang/)
- A retention study found a related effect for noise. With 75% synthetic distractors, Precision@5 fell from 20.2% to 12.4% for unbounded memory and from 15.8% to 3.8% for FIFO, while a scored policy held at 16.9% to 16.6%. Unbounded memory had the highest mean similarity (0.87) and the lowest precision, which shows that high similarity scores do not indicate good retrieval. [Independent] [Abstract] — [Reddy, arXiv 2606.29178](https://arxiv.org/abs/2606.29178)
- BMAD argues that paraphrased documentation goes stale while the source stays true. This supports retrieving source artefacts and treating summaries as disposable. [Practitioner] — [BMAD theory of project context](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/)
- A cross-model study of spec-driven development uses machine-detectable "orphan" citations, meaning references to requirements that do not exist, as an automated hallucination detector in generated code. Its comparison of traceSDD and OpenSpec was non-significant with small effects. I read only a search excerpt and could not confirm its peer-review status. [Secondary] — [Citation Discipline in Spec-Driven Development](https://www.researchgate.net/publication/408302240_Citation_Discipline_in_Spec-Driven_Development_A_Cross-Model_Empirical_Study_of_Output_Determinism_and_Automated_Hallucination_Detection_in_LLM-Generated_Code)
- Temporal Graph RAG tutorials rank conflicting facts by exponential decay from a query date. This is a practitioner pattern without evaluation. [Practitioner] [Secondary] — [Machine Learning Mastery](https://machinelearningmastery.com/adding-temporal-reasoning-to-graph-rag-tracking-fact-freshness-and-staleness/)

### Inferences
- Recency decay is the wrong model for governed artefacts. A ten-year-old policy still in force outranks a recent draft, so validity should be a hard filter on status and effective dates (`status=in-force`, `effective_from <= as_of < effective_to`, `superseded_by=null`), and not a ranking signal. Decay is reasonable only for tickets and informal discussion.
- Queries should carry an as-of date. A trade-reporting change built for a future regulatory date needs the rule that will apply on that date, and an investigation of a past settlement break needs the rule in force on the trade date. A "current" filter gets both wrong.
- The filter order should be entitlement, then validity, then jurisdiction and scope, then hybrid retrieval, then re-ranking. The first three are deterministic and auditable, which matters more in a regulated setting than a small gain in ranking.
- Conflicts should be surfaced rather than resolved silently. A workable precedence is regulation or legal text, then approved firm policy, then in-force ADR, then approved requirement, then ticket, then chat. Within a level, the later effective date wins. A conflict at the same level with overlapping validity should stop the stage and go to the owner, and should not be arbitrated by a model. This ordering is my proposal and has not been tested.
- Different artefact types need different retrieval handling.
    - **Requirements:** by ID and by trace link, with hybrid search only for discovering duplicates or precedent.
    - **ADRs:** by status and component, with supersession chains followed to the head.
    - **Policies:** by section-level chunks with citation anchors, jurisdiction and effective dates. Exact identifiers such as rule numbers favour keyword matching, which is the case for hybrid search.
    - **Tickets:** by link from the work item, with decay and low authority.
- Citations should be artefact ID plus version or content hash, and they should be machine-checked. The orphan-citation approach can be applied at a gate: every generated requirement, design decision and test must resolve to a real, in-force source, and any that do not are rejected before a person reads them.

### Gaps
- I found no benchmark or study on retrieval over requirements, ADRs or firm policy corpora, including effective dates, supersession and jurisdiction. All benchmarks found derive from Wikipedia, Wikidata or general knowledge.
- I found no measured comparison of hybrid search and metadata filtering specifically for these artefacts. Retrieval techniques were out of scope for new searching, and this should be read with the earlier retrieval research.
- I found no measurement of whether citations in generated artefacts improve their accuracy or the reviewer's speed.

## 3. What implementation produces for later stages

### Takeaway
The best recent evidence favours keeping raw traces as the primary record and deriving task-specific distillates at read time, because continuous LLM consolidation can make memory worse than having none, while injecting raw traces directly also performs poorly. None of these studies measure coding-agent transcripts, PR descriptions or decision logs in a delivery workflow.

### Cited Findings
- Consolidated memory rises in utility, then degrades, and can fall below a no-memory baseline. Even when consolidating from ground-truth solutions, GPT-5.4 failed on 54% of ARC-AGI problems it had previously solved without memory. The same trajectories gave different memories under different update schedules. Episodic retention stayed competitive with the consolidators, and agents keeping raw episodes by default achieved double the accuracy of those forced to consolidate. The authors recommend treating raw episodes as primary evidence and making consolidation an explicit, gated choice. The tasks are puzzles rather than software delivery. [Independent] [Abstract] — [Zhang et al., arXiv 2605.12978](https://arxiv.org/abs/2605.12978)
- Injecting raw traces is not the answer either. Query-conditioned reuse, a target-bound note holding the reusable procedure, bindings to recover, applicability conditions and verification requirements, averaged 62.3% success over 2,391 instances. That is 10.7 points above full raw-trajectory injection with 48.9% fewer online tokens. The authors state that "direct trajectory injection loses much of its utility as traces grow longer". The environments are web and application tasks. This is a comparison with raw injection and not with generic summaries. [Independent] [Abstract] — [Li et al., arXiv 2608.12847](https://arxiv.org/abs/2608.12847)
- The same paper's full text says a raw trajectory exposes the reader to both useful procedure and obsolete state, and that a generic source-only summary leaves target-specific work unresolved. [Secondary, PDF excerpt] — [arXiv 2608.12847](https://arxiv.org/pdf/2608.12847)
- AMA-Bench's authors report that bypassing an LLM extraction layer and using raw data directly can significantly improve performance on trajectory benchmarks. This is stated as an experimental observation in the paper. Its abstract attributes the underperformance of existing systems to lost causal and objective information and to lossy similarity retrieval, and reports its own system at 57.22% accuracy, 11.16% above the strongest baseline. [Independent] [Secondary for the raw-data observation] — [Zhao et al., arXiv 2602.22769](https://arxiv.org/abs/2602.22769)
- A survey of persistent agent memory argues that an episode is useful downstream only if it retains the provenance and retrieval handles that allow a later decision to be traced back to it. [Independent, survey] [Secondary] — [arXiv 2606.30306](https://arxiv.org/pdf/2606.30306)
- A separate survey describes the common layered design, where storage preserves trajectories with minimal transformation and higher layers distil reusable insight. [Independent, survey] [Secondary] — [arXiv 2605.06716](https://arxiv.org/pdf/2605.06716)
- BMAD excludes history, edit narration and aspirational state from project context, placing them in git and specifications. [Practitioner] — [BMAD theory of project context](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/)

### Inferences

The retention decision below is my synthesis and has not been tested.

| Artefact | Retain | Serve to later stages by default | Reason |
|---|---|---|---|
| Raw session transcript | Yes, in immutable storage under a retention schedule | No. Audit, investigation and evaluation only | Primary evidence. It cannot be reconstructed, and injection performs badly |
| Decision log (what was chosen, what was rejected and why, linked to requirement IDs) | Yes | Yes, by ID, to review, later units and operations | Rationale cannot be recovered from the diff |
| Spec deviations (requirement, what differs, why, who approved) | Yes, as first-class records | Yes, and mandatory for review and test | It is the input that review most needs and that a diff conceals |
| PR description | Yes | Yes, as a lead-in, but marked as agent claims and not as evidence | Written by the author and therefore not independent |
| Test evidence (command, commit, result, requirement IDs) | Yes, produced by CI | Yes, as the evidence itself | Machine-generated and verifiable, unlike an agent's statement that tests pass |
| Rolling LLM summary of a session | Only as a disposable index | Only for navigation | Lossy and schedule-dependent, per arXiv 2605.12978 |
| Distilled lesson | Only as a candidate with a link to its source episodes | Only after promotion (section 4) | Prevents an unverified generalisation becoming an instruction |

- The apparent contradiction between arXiv 2605.12978 and arXiv 2608.12847 resolves once storage is separated from delivery: store raw, and generate a target-bound brief when it is read. A brief should state its applicability conditions and what must be re-verified, since a stale binding is the failure both papers point to.
- Deviation records would be a useful capture point because they can be produced at low cost. A small, structured tool call during implementation is cheaper than reconstructing the deviation from a transcript afterwards.
- In a capital markets setting, transcripts may contain client or material non-public information and may fall under records retention requirements. The firm's records and compliance functions would need to determine retention and access; I did not research the applicable rules for this note.

### Gaps
- I found no study of coding-agent session transcripts, comparing raw retention with summaries for later delivery stages. All evidence transfers from puzzle, web or application benchmarks.
- I found no study measuring whether PR descriptions, decision logs or deviation logs reduce later rework or review time.
- I did not establish storage cost or sensitive-data handling for transcripts at enterprise scale.

## 4. Feedback from test, review and production

### Takeaway
Mining review comments is an active practice with useful conventions for citations and occurrence thresholds, and negative review feedback is demonstrably used in production at Uber to suppress noisy categories. I found almost no empirical evidence on incidents flowing into requirements or rules, and no published governance model for promotion from a large engineering organisation, so a promotion process has to be designed rather than copied.

### Cited Findings

**Learning from review**

- Uber uses feedback to filter rather than to write rules. Each comment has a predicted category, categories that draw negative developer feedback are filtered automatically, and thresholds are tuned per assistant, language and category. Engineers mark about 75% of comments useful. On average 65% are addressed in the same changeset, against 51% for human-written comments. Uber also reports that a high false-positive rate makes engineers tune the tool out. The post gives no thresholds. [Vendor] [Older: August 2025] — [Uber uReview](https://www.uber.com/us/en/blog/ureview/)
- Atlassian's RovoDev reports that 38.70% of generated comments led to code changes in later commits, median PR cycle time fell 30.8%, and human-written comments fell 35.6%, in a one-year evaluation published at ICSE-SEIP 2026. A search summary of the paper lists a limitation calling for randomised or quasi-experimental designs, which indicates the result is not causal. [Vendor, peer-reviewed] [Abstract] — [arXiv 2601.01129](https://arxiv.org/abs/2601.01129)
- The dotnet/fsharp project mined about 695 review comments from four expert reviewers over ten years into agent instructions, and also dropped rules that were overfitted to single pull requests. [Practitioner] [Secondary] — [dotnet/fsharp PR 19451](https://github.com/dotnet/fsharp/pull/19451)
- A pytest discussion describes a tool that requires each mined rule to carry a verbatim quote from repository history, and that demotes rules lacking a verified citation. [Practitioner] [Secondary] — [pytest discussion 14685](https://github.com/pytest-dev/pytest/discussions/14685)
- Community skills apply promotion heuristics. One requires three or more occurrences for team-specific patterns, filters out bots and cites PR links. Another clusters repeated feedback, deduplicates, records provenance and skips one-off or disputed feedback. None of these reports outcomes. [Practitioner] [Secondary] — [learn-from-prs](https://claudskills.com/skills/learn-from-prs/SKILL.md); [pr-learning](https://skillselion.com/skills/cameroncooke/cameroncooke-skills/pr-learning)
- A difflore tool distils imported PR comments into local rule candidates with source backing. [Practitioner] [Secondary] — [difflore-cli source](https://docs.rs/crate/difflore-cli/0.5.0/source/src/commands/import_reviews/local_agent_distill.rs)

**Incidents and postmortems**

- Practitioner material recommends that lessons should live in validation code, tests, hooks and rule files, and that each incident should yield a test that would have caught it. This comes from a vendor of an agent platform and no measurement is offered. [Practitioner] [Secondary] — [agent.ceo](https://agent.ceo/blog/incident-learning-loop-ai-agent-platform)
- One practitioner traces each behavioural rule of a personal assistant to a specific incident and checks postmortem action items the next day. [Practitioner] [Secondary] — [Latent Operator](https://latentoperator.pages.dev/posts/writing-postmortems-for-your-ai-agent)
- A reusable skill routes each lesson by type (skill update, orchestration rule update or flag for human review) and asks how the fix would be verified to prevent recurrence. [Practitioner] [Secondary] — [Smithery](https://smithery.ai/skills/hohai99/postmortem-and-learning-extractor)
- One vendor recommends that AI draft incident reports while humans write the lessons. [Vendor] [Secondary] — [CallSphere](https://callsphere.ai/blog/vw3c-postmortem-template-ai-agent-incidents.md)
- BMAD states that a policy or pitfall is removed only when its subject is gone or a human removes it, and not merely because failures have stopped. This is a useful counter to automatic expiry for rules, since an absence of failures may mean the rule is working. [Practitioner] — [BMAD theory of project context](https://docs.bmad-method.org/existing-codebases/theory-of-project-context/)

**Risk at promotion**

- Cisco demonstrated persistent compromise of Claude Code. An npm postinstall hook in a repository the user approved moved a payload into global configuration, overwrote `MEMORY.md` files across projects and modified hooks settings, and added a shell alias that re-enabled auto-memory. The poisoned agent recommended storing an API key in a committed source file and gave no security warning. Cisco reports that the model treated memory files as trusted user instructions, and that version 2.1.50 removed user memories from the system prompt. [Vendor security research] — [Cisco, 1 April 2026](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code)
- A Snyk audit flagged an extract-rules skill because parsing public PR comments exposes an agent to third-party prompt injection. [Vendor] [Secondary] — [skills.sh audit](https://www.skills.sh/hiroro-work/claude-plugins/extract-rules/security/snyk)
- MemoryGraft plants malicious entries through benign-looking content such as a README, and MINJA poisons memory through ordinary queries. I read these only through a vendor summary and did not locate the papers. [Secondary] — [WorkOS](https://workos.com/blog/ai-agent-memory-poisoning)
- The consolidation result in section 3 bears directly on promotion: an LLM rewriting lessons can degrade performance even from correct inputs. [Independent] [Abstract] — [arXiv 2605.12978](https://arxiv.org/abs/2605.12978)
- Earlier notes record the GitHub Copilot memory design and the STALE benchmark, where the best model reached 55.2% accuracy. That result means agent-side checks cannot be the promotion control. See `sdlc-context-graph.md` section 7.

### Inferences
- A promotion ladder that follows from this evidence has five levels, and each step needs its own evidence and approver. This is my proposal and has not been tested.
    1. **Observation:** an event with a link to the source (review comment, failed test, incident). Stored automatically and never loaded as an instruction.
    2. **Candidate:** a clustered lesson with at least N independent occurrences, or one severe incident, carrying verbatim citations. Occurrence counts should exclude bots and agent reviewers, because most agent-PR review activity comes from other agents (section 6), and counting them would allow agents to validate each other.
    3. **Scoped rule:** applied to one repository or component after approval by its owner, with a replay against golden tasks showing that it helps and does not harm.
    4. **Team or domain standard:** a pull request to the rule repository, reviewed by the standard's named owner, with evidence from the scoped period.
    5. **Firm policy:** owned by the existing policy function (for example, risk or compliance). Agents may propose but may not author changes at this level.
- The preferred target for a lesson should be, in order: a deterministic check (linter, CI test, policy as code), then a test, then a scoped rule, and only then an always-loaded instruction. Every step down that list costs context and is enforced less reliably. This fits the evidence on agents skipping instructions and on instruction files raising costs.
- Mined text from comments and tickets must be treated as untrusted, as the Cisco and Snyk reports show. Candidates should be quarantined from execution contexts, and writes to the rule store should go only through the reviewed path. Write access to rule files and hooks should also be monitored separately.
- Incidents should flow to three places with different owners: a regression test against the affected requirement (engineering), a change or gap recorded against the requirement (product or business owner), and a candidate rule (standard owner). A post-trade incident caused by a misunderstood cut-off, for example, would most likely indicate a requirement gap rather than a coding rule, and treating it as a coding rule would hide the actual cause.
- Rules should expire on a review of their subject rather than on the absence of use, in line with the BMAD position. This qualifies the expire-if-unused approach recorded for Copilot memory: that approach is suitable for agent memories and not for approved controls.

### Gaps
- I found no measured study of learned rules from review comments that reports subsequent defect or review outcomes.
- I found no primary engineering publication from Uber, Stripe or Atlassian describing how a learned fact is promoted to a standard.
- I found no empirical study of postmortems feeding agent rules or requirements. The available material is prescriptive.
- I did not locate the primary papers for MemoryGraft, MINJA or the "Bad Memory" paper mentioned in secondary sources, and I found no standard benchmark for rules-file poisoning.

## 5. Evaluation: measuring context quality per stage

### Takeaway
Context quality has no single published measure across delivery stages, so a platform needs a stack: retrieval metrics against labelled artefact IDs, stage-specific golden tasks, and delivery outcomes. The outcome studies show that perceptions and aggregate throughput mislead, that randomised designs are becoming harder to run, and that no controlled spec-driven outcome study was found, so measurement must be planned into the platform from the start.

### Cited Findings

**Retrieval metrics**

- Ragas defines Context Precision@K as the sum over k of Precision@k × v_k, divided by the number of relevant items in the top K, so it measures ranking as well as content. Variants differ in their inputs. `ContextPrecision` and the legacy `LLMContextPrecisionWithReference` require a reference answer; `ContextUtilization` and the legacy without-reference variant compare chunks with the generated response; `NonLLMContextPrecisionWithReference` needs reference contexts; and `IDBasedContextPrecision` compares `reference_context_ids` directly. [Practitioner, tool documentation] — [Ragas context precision](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/)
- Ragas also lists Context Recall, Context Entities Recall, Noise Sensitivity and Faithfulness, along with agent metrics such as Tool Call Accuracy, Tool Call F1, Agent Goal Accuracy and Topic Adherence. [Practitioner] — [Ragas metrics](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/)
- Uber evaluates against a curated benchmark of commits with known issues, using precision, recall and F1 against human labels. Online, it reruns the reviewer five times on the final commit, and counts a comment as addressed if no rerun reproduces a semantically similar comment. [Vendor] [Older] — [Uber uReview](https://www.uber.com/us/en/blog/ureview/)
- Atlassian's evaluation combines offline, online and user-feedback assessment over a year, and its primary online measure is the code resolution rate. [Vendor] [Abstract] — [arXiv 2601.01129](https://arxiv.org/abs/2601.01129)
- High retrieval similarity can coincide with low precision, as shown in the 0.87 mean similarity under noise in the retention study. [Independent] [Abstract] — [arXiv 2606.29178](https://arxiv.org/abs/2606.29178)

**Requirement-to-test measures**

- The test-grounding study shows why coverage alone is inadequate: doubling tests barely helped while grounding moved correct code by 36 to 38 points, and a generator found bugs by inventing requirements. [Independent] [Abstract] — [arXiv 2607.06636](https://arxiv.org/abs/2607.06636)
- The Google-authored study reports a 2.5-point branch coverage gain alongside a 9.8-point bug-detection gain, which again shows that the two do not move together. It also used LLM-as-judge comparisons, rating spec-driven suites better than baseline in 77.8% of cases and better than human-written in 56.7%. These judge figures are weaker evidence than the bug-detection result. [Vendor-affiliated research] [Abstract] — [arXiv 2608.17177](https://arxiv.org/abs/2608.17177)

**Outcome studies**

- METR's original trial found that AI made tasks 19% longer (95% CI +2% to +39%) for experienced open-source developers in early 2025. [Independent] [Older] — [METR update, February 2026](https://metr.org/blog/2026-02-24-uplift-update/)
- In that trial, developers believed they had been sped up by about 20%. [Secondary for this figure] — [DEV Community summary](https://dev.to/dang-w/the-perception-gap-5dof)
- METR's follow-up covered 57 developers, 143 repositories and over 800 tasks. Returning developers showed −18% time (CI −38% to +9%) and new recruits −4% (CI −15% to +9%), with both intervals including zero. METR believes developers are probably faster than in early 2025 but calls this very weak evidence of the increase, and considers the central estimate a poor measure, for these reasons.
    - Developers increasingly refused to work without AI.
    - Between 30% and 50% of those surveyed withheld tasks they did not want to do without AI.
    - Work quality differed between conditions.
    - Completion rates were lower in the AI-disallowed condition.
    - Time was hard to track with concurrent agents.

  METR is considering shorter experiments, fixed-task designs, transcripts, time-use studies and developer-level randomisation. [Independent] — [METR update](https://metr.org/blog/2026-02-24-uplift-update/)
- DORA 2025 concludes that AI's "primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses", and that the largest returns come from the surrounding organisational system. [Independent-leaning, Google-sponsored survey] [Older] — [DORA 2025 report page](https://dora.dev/research/2025/dora-report/)
- About 90% of DORA 2025 respondents use AI at work, from nearly 5,000 technology professionals. [Vendor summary] [Older] — [Google blog](https://blog.google/technology/developers/dora-report-2025/)
- A reader of the DORA report summarises its seven clusters as follows: clusters 1 to 4 largely offset speed gains with a higher change failure rate, while clusters 6 and 7, about 40% of respondents, raise throughput without harming stability. He argues the sample is skewed towards teams familiar with DORA, so the industry figure is likely half or less. I did not read the full report. [Independent commentary] [Older] — [Bowley](https://blog.robbowley.net/2025/10/01/dora-2025-ai-assisted-dev-report-some-benefit-most-dont/)
- Faros reports telemetry from 22,000 developers and more than 4,000 teams over two years, comparing each organisation's lowest and highest AI-adoption periods. From low to high adoption, it reports incidents per merged PR up 242.7%, monthly incidents up 57.9%, median time in review up 441.5%, PRs merged with no review up 31.3%, bugs per developer up 54%, and code churn up 861%. The page gives no absolute baselines, no sample size per metric and no statistical tests. It cautions that one PR may link to several incidents and that churn could reflect refactoring. Faros sells this kind of measurement, and adoption periods are also confounded with time. [Vendor] — [Faros](https://faros.ai/blog/ai-acceleration-whiplash-takeaways)
- There are claims about Faros' findings that conflict. Some secondary articles attribute the incidents-per-PR figure to DORA 2025, and some give a different review-time change. The primary Faros page above should be preferred. [Secondary] — [Particula](https://particula.tech/blog/dora-2025-ai-acceleration-whiplash-incidents-bugs-pr-review-data)
- Spec-driven literature is mostly conceptual or architectural. Piskala offers a framework of specification rigour, and the Spec Growth Engine proposes an architecture. Neither measures outcomes. [Independent] [Secondary] — [arXiv 2602.00180](https://arxiv.org/abs/2602.00180); [arXiv 2606.27045](https://arxiv.org/pdf/2606.27045)
- A SpecOps workshop now exists at SPLASH 2026, so more results may appear soon. [Independent] [Abstract] — [arXiv 2608.17177](https://arxiv.org/abs/2608.17177)

**Observability tooling**

- The OpenTelemetry GenAI conventions have moved to a dedicated repository. The old page is no longer maintained. [Primary] — [OTel GenAI spans page](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/)
- The new repository's README lists an empty Releases section and a "TODO" Schema URL, and covers spans, metrics and events for GenAI clients and MCP. [Primary, as fetched in November 2026] — [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai)
- A July 2026 secondary source says every `gen_ai.*` item still carried "Development" stability. Other secondary sources describe agent spans (`create_agent`, `invoke_agent`, `execute_tool`, `invoke_workflow`) and a `retrieval` operation name. I could not confirm these in the primary specification because the file path I tried returned a 404. [Secondary] — [DEV Community, Azena](https://dev.to/azena-ai/opentelemetrys-genai-semantic-conventions-are-not-stable-yet-heres-what-actually-shipped-in-2026-3mke); [Greptime](https://www.greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions)
- Langfuse groups OTel traces into experiment runs using experiment metadata on spans, and has a model of datasets, runs, items, traces and scores. [Vendor documentation] [Secondary] — [Langfuse OTel experiments](https://langfuse.com/docs/evaluation/experiments/experiments-via-opentelemetry)
- LangSmith supports evaluation with OTel by creating an experiment session and adding span attributes that link traces to the experiment and to dataset examples. [Vendor documentation] [Secondary] — [LangSmith OTel evaluation](https://docs.langchain.com/langsmith/evaluate-with-opentelemetry)
- Langfuse's migration guide states that experiments must be re-run because scores do not carry across. This suggests keeping the golden datasets and evaluators in the firm's own repository. [Vendor documentation] [Secondary] — [Langfuse migration guide](https://langfuse.com/resources/engineering/migrate-from-langsmith.md)

### Inferences

**Context quality by stage.** This table is my synthesis. Published usage exists for the cited metric families, but I found no one using this per-stage design.

| Stage | Context retrieval metric | Task-level metric | Downstream outcome that reveals poor context |
|---|---|---|---|
| Requirements | Recall of applicable policies and prior decisions against a labelled ID set; share of retrieved items in force | Ambiguity markers resolved; testability of acceptance criteria | Requirement changes after design approval; incidents traced to requirement gaps |
| Design | Recall of impacted components against the components the merged change actually touched; in-force ADR recall | Conflicts with in-force ADRs found at review | Unplanned components changed; design rework at gates |
| Implementation | Used-to-loaded ratio; missing-context events (the agent searched for something a pack should have held) | Spec-conformance rate; golden-task success; tokens and tool calls to first passing build | Rework commits within N days; deviations per task |
| Test | Share of requirements supplied to the tester; recall of relevant past incidents | Requirement-to-test coverage; mutation score or seeded-bug detection; false-alarm rate; invented-requirement rate | Escaped defects by requirement |
| Review | Linked requirement and standard availability | Precision and recall on a known-issue benchmark; addressed rate; high-severity finding rate | Defects that passed review; median human time per change |
| Operations | Recall of relevant change and incident records | Time to correct cause on replayed incidents | Change failure rate; time to restore |

- ID-based precision and recall should be the main retrieval metric for this platform, because most artefacts carry stable IDs and labelling is therefore cheap. The merged change gives a natural ground truth for a design stage, and the requirement trace does the same for test. Generated-answer metrics such as faithfulness are useful at the requirements stage, where text output is the product, and less so elsewhere.
- Without-reference metrics, such as those that compare chunks to the generated response, measure whether the output used the context and not whether the context was right. An agent that ignored a key policy would not be penalised. They should therefore serve only as online proxies.
- Context recall matters more than precision for controls: failing to retrieve a restriction is much worse than loading one irrelevant document. A capital markets platform should set a recall floor for "must-retrieve" policy items, with precision tracked as a cost measure.
- Spec-conformance requires an independent check. An agent that wrote the code cannot be the sole judge. The check could consist of executable acceptance tests linked to requirement IDs, with an LLM judge as a secondary check only, given that LLM-judge results are the weaker evidence.
- Requirement-to-test coverage should count only tests that fail when the requirement is violated, which can be established by mutation or by seeded faults. A trace link alone only shows that a mapping exists. In a regulated setting this link is also audit evidence, which gives it value regardless of its effect on delivery.
- A golden task suite should have tasks per stage, drawn from the firm's real history, including stale-context traps, conflicting-source traps and must-refuse cases such as an in-force restriction. Every change to a rule, pack or retriever should run against it, in the same way as a code regression. Stage packs can then be ablated by removing items and observing whether results change, which is the published ablation method and is cheaper than a field experiment.
- METR's experience implies that an internal "AI versus no AI" randomised trial will suffer the same refusal and selection problems. A better design is to randomise the context configuration, not the presence of AI, because developers have no reason to refuse it. Pack A against pack B, by work item, within the normal workflow, also gives the direct answer to the context question.
- Faros and DORA together imply that throughput measures cannot be read in isolation. At minimum, throughput should be paired with change failure rate, rework, review time and the share of changes merged without human review. Incident attribution must be defined before any baseline is taken, given Faros's caveat about linking.
- Standardise on OTel for raw traces with a thin, firm-owned attribute layer (stage, work item ID, pack version, artefact IDs and versions loaded). Because the upstream GenAI conventions are not yet stable and are without a tagged release as far as I could confirm, attributes should be mapped at the collector so they can be changed in one place. The artefact-level load record is also the audit record described in section 9.3 of `aidlc-context-management.md`.

### Gaps
- I found no published AI-DLC outcome study. The AI-DLC benchmark request noted in `aidlc-context-management.md` section 7.5 was not re-checked.
- I found no controlled spec-driven outcome study on delivery measures such as defect rates, rework or change failure rate. The two controlled studies found concern test generation.
- I found no published per-stage context quality benchmark in software delivery, or any use of Ragas-style metrics on requirements or ADRs.
- I did not read the full DORA 2025 report or find any 2026 DORA report, so its instability and cluster details rest on secondary sources. The search on this was limited and a 2026 report should be checked for directly.
- LinearB benchmark figures appear in secondary write-ups, including the often repeated claim of AI pull requests merging at 32.7% against about 84% for manual ones. I could not trace them to a primary source and have not relied on them.
- The 2026 ablation cited in `aidlc-context-management.md` (arXiv 2607.27250) was not re-read.

## 6. Human review: preventing fatigue and placing gates

### Takeaway
Review capacity is now the visible constraint, and AI review help does not clearly improve what matters, since one controlled experiment found more low-severity findings, no more high-severity findings, and no time saved. I found no controlled study of approval gate placement or fatigue, so the gate design below is inferred from the failure evidence.

### Cited Findings
- In a controlled experiment with 29 experts and more than 50 hours of recorded reviews, reviewers starting from an automated review found more low-severity issues but no more high-severity issues. They focused on the code locations indicated by the LLM, and they neither saved time nor gained confidence. [Independent, preprint] [Older: November 2024, pre-agent models] [Abstract] — [Tufano et al., arXiv 2411.11401](https://arxiv.org/abs/2411.11401)
- In AIDev repositories with 100 or more stars, 61.38% of 33,596 agent pull requests received no recorded review, and of those reviewed, 58.77% had agents only, 10.14% humans only and 31.09% mixed. The widely quoted 61% figure overstates the difference with human work. In repositories containing both kinds of PR, 28.92% of agent PRs and 34.52% of human PRs received no review, though human-only review was 8.08% for agent PRs against 25.21% for human PRs. The study treats PRs without comments as unreviewed, does not control for size or complexity, and does not assess effectiveness. The paper's text gives 40.34% for mixed review while its table and arithmetic give 31.09%. [Independent] — [Duma et al., EASE 2026, arXiv 2605.02273](https://arxiv.org/html/2605.02273)
- Faros's increases in review time and in unreviewed merges are listed in section 5, with the caveats given there. [Vendor] — [Faros](https://faros.ai/blog/ai-acceleration-whiplash-takeaways)
- Artefact volume itself creates review burden. Böckeler found Kiro over-verbose for a small bug, which became four user stories with 16 acceptance criteria. She found Spec Kit's output so repetitive that she would "rather review code", and she worries these workflows amplify review overload. [Independent, anecdotal] [Older] — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Stripe limits what reaches a person by running linters locally in a loop before pushing, auto-applying autofixes and allowing a maximum of two CI rounds. A branch still failing then goes to a human. [Vendor] — [Stripe Minions part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- Uber treats signal-to-noise as the main goal of its reviewer, generating, filtering, validating and deduplicating comments before posting, with a usefulness target above 75%. [Vendor] [Older] — [Uber uReview](https://www.uber.com/us/en/blog/ureview/)
- A longitudinal ESEM 2026 study of 669 developers examines whether agent adoption changes coding, testing and review, framed by automation complacency theory. I could not fetch it and did not see its findings, so it should be read directly before use. [Independent] [Secondary] — [ESEM 2026, LIPIcs](https://drops.dagstuhl.de/storage/00lipics/lipics-vol394-esem2026/LIPIcs.ESEM.2026.67/LIPIcs.ESEM.2026.67.pdf)
- A Codacy article argues for automated enforcement gates against automation bias, but cites no experiment for that claim. [Vendor] [Secondary] — [Codacy](https://blog.codacy.com/automation-bias-in-ai-generated-code-review-why-clean-code-still-ships-broken)

### Inferences
- Gates are probably most valuable where a mistake is cheap to fix now and expensive later, and where the judgement is one the machine cannot verify. This implies more human time on requirements and on decisions, and less on line-level review of mechanically verified code. The nearest evidence is the finding that LLM support did not improve high-severity detection, and I found no measurement that directly compares gate placements.
- Recommended high-value gates, in priority order, are listed below. The order is my judgement.
    1. **Requirement approval**, including resolved clarification markers and the policies relied on. A wrong requirement passes every later check.
    2. **Decisions that are hard to reverse:** architecture, schema and data contracts, and interfaces that other systems or counterparties depend on.
    3. **Deviations from specification**, each individually approved.
    4. **Promotion of learned rules**, as in section 4, because an error is multiplied across later work.
    5. **Changes in regulated or high-risk scope:** order routing, risk limits, regulatory reporting, entitlements and calculations with financial effects, where mandatory independent human review should remain regardless of agent confidence.
    6. **Production change.**
- Low-value gates are those over artefacts that a machine can check, and those over generated documents that restate an upstream one. Plan and task documents can be sampled rather than approved one by one, if they are traced to an approved requirement and deviations are surfaced.
- Methods that follow from the evidence to reduce fatigue are listed below.
    - Run all deterministic checks before a person sees anything, as Stripe does.
    - Show the reviewer a delta against the approved upstream artefact and the deviation list, and not the whole generated document.
    - Scale artefact size with risk and size of change. A small bug should not generate user stories, which is the failure Böckeler recorded.
    - Use risk-based routing, so that low-risk, reversible, well-tested changes get lighter review and risk tiers are set by rule rather than by the agent.
    - Set a limit on review queue depth, and slow generation when it is exceeded. Generating faster than the team can review simply moves the queue.
    - Track AI reviewer precision and suppress noisy categories, as Uber does.
- Because reviewers anchor on locations flagged by an LLM, the order of work matters. A human should form a view of high-risk scope before seeing AI comments, or the AI findings should be presented as a separate list. An AI reviewer's passing result must not reduce the human reviewer's scope on high-risk changes. This extrapolates a single 2024 experiment.
- Seeded-fault auditing can measure whether review is actually working. Periodically inserting known defects, in a controlled way and on non-production paths, would give a direct measure of detection rate and of decline over time. I found no published use of this for generated-artefact review, so it would be an experiment. Rubber-stamping signals can also be tracked, including approval time against artefact size and the proportion of approvals without comment. Those are only indicators, as the EASE study's treatment of silent approvals shows.
- In a capital markets setting, the review record should show what the reviewer actually saw, including the artefact versions, the evidence and the context loaded by the agent. A later audit can then establish whether approval was informed.

### Gaps
- I found no controlled study of reviewer fatigue over generated artefacts, approval gate placement, or the effect of gate count on defect escape.
- I found no study comparing human review of specifications with human review of code as a defect-prevention investment in agent workflows.
- I could not read the findings of the ESEM 2026 study, which is the closest relevant longitudinal work.
- The controlled experiment on review anchoring dates from 2024 and has not, as far as I found, been replicated with current agents.
