# Design-Stage Context in an AI-Assisted Delivery Lifecycle

Contents:

1. What should be recorded, and what is most often lost
2. Formats, agent consumption, and machine-checkable artefacts
3. Research on LLMs for architecture and design
4. Enforcing design conformance and detecting drift
5. Capturing agent decisions and superseding old ones
6. What AI-DLC, Kiro, Spec Kit, Tessl and BMAD artefacts contain
7. Failure modes

**How these notes were researched.** WebFetch failed on every domain tried, including arxiv.org, kiro.dev, adr.github.io and GitHub, because its domain safety check could not complete. No full paper or documentation page was read. Each finding therefore carries one of two depth labels. "Abstract" means that the text came directly from the arXiv API record. "Snippet" means that the text came from a search-tool summary, which is secondary and can misattribute details. The report writer should confirm any figure marked "snippet" before relying on it.

**Source labels.** The labels are: Peer-reviewed (accepted at a named venue, according to the arXiv record), Preprint, Vendor (a claim by the party selling or maintaining the tool), Practitioner (an individual or consultancy report), and Community (a mirror, skill listing or template copy).

## 1. What should be recorded, and what is most often lost?

### Takeaway
The literature consistently shows that rationale is valued yet rarely captured, but this research found no study that ranks the listed content types by value. Prioritising alternatives, constraints and revisit conditions is therefore an inference from what code cannot show, and it is not an empirical result.

### Cited Findings
- **Older (2006).** Tang, Babar, Gorton and Han surveyed practitioners and obtained 81 valid responses. Practitioners saw value in documenting rationale and often used it when reasoning about design choices, but they also named barriers to documenting and using it. Peer-reviewed, snippet; the barrier categories were not retrieved. — [Swinburne report record](https://figshare.swinburne.edu.au/articles/report/A_survey_of_architecture_design_rationale/26269849); [WICSA 2005 record](https://bibtex.github.io/WICSA-2005-TangBGH.html)
- **Older (2007).** Tang's thesis reports that current practice had no systematic approach to using and capturing design rationale, and it proposes a rationale-based model called AREL. Snippet. — [Tang thesis](https://researchbank.swinburne.edu.au/file/198ab8bf-fbaa-422b-bd24-2ecf7d23aa0c/1/Antony%20Tang%20Thesis.pdf)
- A search summary states that survey participants regard rationale as important but do not capture it, mainly because they lack appropriate tools. The summary did not clearly identify which of its returned documents made this statement, so the attribution is unconfirmed. Snippet. — [Candidate source, core.ac.uk](https://core.ac.uk/download/232485824.pdf)
- A search summary states that Tofan's thesis reports two practitioner surveys and concludes that architectural knowledge vaporization is a major issue, with consequences that include drift from the intended architecture and costly evolution. Snippet. — [Tofan thesis](https://core.ac.uk/download/518709314.pdf)
- A questionnaire of 63 participants and 13 interviews found that architects prefer solutions that are familiar to them or that guarantee fast implementation. Mid-career architects were more open to new solutions than senior and junior practitioners. Most practitioners were not concerned with compatibility or portability. Preprint, abstract, 2023. — [Borowa et al.](https://arxiv.org/abs/2309.14164)
- Interviews with 32 practitioners from 21 organisations found that most architecture challenges centre on management, documentation, tooling and process. Peer-reviewed (ESEC/FSE 2023), abstract. — [Wan et al.](https://arxiv.org/abs/2308.09978)
- A study of 7,310 rules from 83 open-source projects, combined with a survey of 99 practitioners, found a mismatch. Practitioners rate architectural constraints as highly important, but rule files mainly contain low-level workflow and formatting constraints. Preprint (submitted to a journal), abstract. — [Cai et al.](https://arxiv.org/abs/2606.12231)
- The AI-DLC, Spec Kit and Kiro templates capture components, data models and contracts more explicitly than rejected alternatives. Spec Kit records a rejected simpler alternative only when a constitution violation needs justifying. See question 6 for sources. Community and vendor, snippet. — [Spec Kit template copy](https://forge.alexselimov.com/aselimov/notex.nvim/src/branch/master/.specify/templates/plan-template.md)

### Inferences
- Content types differ in how recoverable they are from code. Interfaces, data models and component boundaries can usually be partly reconstructed from the code. Rejected alternatives, the constraints that motivated a choice, accepted trade-offs and conditions for revisiting a decision usually cannot. Capture effort should therefore favour the second group, and the first group should be held in checkable artefacts instead of prose.
- The Borowa result implies that a recorded rationale may hide the real driver. A record that says "chosen for scalability" may conceal familiarity or delivery speed. A design template could ask directly whether familiarity or schedule influenced the decision.
- Compatibility being a low concern among general practitioners should not transfer to capital markets. For example, a design for a post-trade service may have to preserve message compatibility with counterparties and regulators, so that constraint should be stated explicitly.
- A minimum design record for this platform could contain the following items: decision, drivers and hard constraints, alternatives with rejection reasons, accepted trade-offs, revisit conditions, enforcement reference, status and owner, and links to affected contracts and threat-model entries. This list is a proposal and has not been validated by any study found here.
- Capital markets illustration: a record for choosing an event log for order lifecycle events should state the audit-retention constraint, the rejected database-polling option and the sequencing guarantee on which downstream reconciliation depends. None of these can be reliably inferred from the consumer code.

### Gaps
- No study was found that ranks decisions, alternatives, constraints, trade-offs, NFRs and threat models by value or by loss rate.
- The survey evidence on rationale is old. A later study cited in search results described the Tang work as at least eight years old at its time of writing, and no recent replication was found. — [Secondary record](https://springerlink.bibliotecabuap.elogim.com/10.1007/978-3-031-42592-9_21)
- No evidence was found on threat models as design-stage context for agents.

## 2. Which formats do agents consume well, and what is the case for machine-checkable artefacts?

### Takeaway
No independent head-to-head study of design formats as agent input was found. The strongest argument for machine-checkable artefacts is that they can be validated. It is not that agents understand them better, and the TLA+ evidence shows that agents can write valid specifications far more often than correct ones.

### Cited Findings
**ADRs**
- ADR history improves generation. A corpus from 750 open-source repositories was used to compare five context strategies. A recency window of typically 3 to 5 prior records gave the best balance of quality and efficiency. Retrieval helped marginally, mainly for non-sequential or cross-cutting decisions, and had no statistically significant advantage in typical linear workflows. Peer-reviewed (EASE 2026), abstract. — [Gupta et al.](https://arxiv.org/abs/2604.03826). A search summary notes that this result depends on automatic fidelity metrics. — [Pith summary](https://pith.science/paper/2604.03826)
- This study measures ADR writing, not whether a coding agent complies with ADRs when reading them. It should not be used as evidence for the second question. (Reading of the [same abstract](https://arxiv.org/abs/2604.03826).)
- MADR status values are listed as proposed, accepted, rejected, deprecated and superseded. Community, snippet. — [Semantic Anchors](https://llm-coding.github.io/Semantic-Anchors/anchor/madr)
- Secondary commentary says that MADR 3.0 added optional metadata and a Confirmation section, and that 4.0 renamed elements and added a minimal variant. A skill guide lists 4.0.0 as current. These claims could not be checked against adr.github.io. Community, snippet. — [MADR skill guide](https://www.skills.lc/zircote/adr/zircote-adr-skills-adr-format-madr-skill-md); [Zimmermann MADR primer, 2022, older](https://ozimmer.ch/practices/2022/11/22/MADRTemplatePrimer.html)
- One project using MADR-style records names the verification section "Validation" where other sources say "Confirmation", so the exact heading needs checking. Community, snippet. — [Paxman ADR index](https://paxman.readthedocs.io/en/latest/adr/)

**C4, Structurizr and Mermaid**
- Structurizr's documentation argues that its text-based DSL suits LLM generation, is version-controllable and diff-friendly, and keeps views consistent through a shared model. It also says that PlantUML and Mermaid do not understand C4. Vendor claim, snippet. — [Structurizr DSL generation](https://docs.structurizr.com/ai/dsl-generation)
- The Structurizr MCP server is described as able to parse and validate DSL, export to PlantUML and Mermaid, and manage workspaces. Vendor, snippet. — [Structurizr AI + MCP](https://docs.structurizr.com/ai)
- A practitioner reports a workflow in which a Claude Code skill writes workspace.dsl from the code. It presents no controlled evaluation. Practitioner, snippet. — [Working Software](https://www.workingsoftware.dev/ai-assisted-software-architecture-generating-the-c4-model-and-views-directly-from-code/)
- A Medium post claims about 88% accuracy for a multi-agent C4 pipeline against manual work, but it does not describe the sample or method. The figure should be treated as anecdotal. Practitioner, snippet. — [Medium post](https://medium.com/@sauravskit749/architectural-intelligence-using-generative-ai-to-automatically-derive-c4-diagrams-from-source-6d908901af7a)

**Formal specifications**
- An evaluation of 30 LLMs on 205 TLA+ specifications found up to 26.6% syntactic correctness and only 8.6% semantic correctness. Successes occurred only with progressive prompting, and code-specialised models consistently underperformed. Peer-reviewed (ICSOFT 2026), abstract. — [Bisharat et al.](https://arxiv.org/abs/2606.05792)
- TLA+-Bench, with 403 model-checked gold and 897 parse-only silver specifications, reports that the strongest model is correct 16% of the time by default and 26% when given the interface names. Open models reach at most 1%. Varying grading choices alone moves the correct rate from 10.0% to 1.7% on fixed outputs. Preprint, abstract. — [TLA+-Bench](https://arxiv.org/abs/2607.23425)
- ALIAS cautions that rates across these benchmarks are not directly comparable, because prompts and generation settings differ. Preprint, snippet. — [ALIAS](https://arxiv.org/html/2610.29767)
- A case study on SysMoBench reports that the specification contract, not the language, dominated the outcome. It is a single case and only indirectly relevant. Preprint, snippet. — [JS-SAM](https://arxiv.org/pdf/2607.13092)

**Machine-checkable contracts**
- oasdiff compares two OpenAPI revisions, classifies differences as breaking or non-breaking, and can fail a CI job. Practitioner guide, snippet. — [SitePoint](https://www.sitepoint.com/detect-breaking-api-changes-typescript-openapi/)
- Augment Code argues that without explicit contract tooling there is no automatic means of enforcing API consistency, and it recommends separating spec generation from verification. It gives no quantitative results. Vendor, snippet. — [Augment guide](https://www.augmentcode.com/guides/api-contract-testing-agent-authored-specs)
- Thoughtworks Radar coverage flags handwritten specifications as outperforming LLM-generated ones on precision. This comes from a secondary digest, and the underlying evidence was not seen. Practitioner, snippet. — [Radar Vol. 34 digest](https://agentic-ai.readthedocs.io/en/latest/AgenticTechStack/thoughtworks-radar-vol34/)

### Inferences
- A useful division is that prose holds the reasons and checkable artefacts hold the obligations. Each ADR should point to the artefact or test that enforces it.
- The gap between valid and correct TLA+ means that a parser or model checker run alone is not sufficient acceptance for agent-written specifications. A human must confirm that the properties being checked are the right ones. This applies by analogy to OpenAPI and Protobuf, where a valid file can still describe the wrong contract.
- The 16% to 26% rise from supplying interface names suggests that exact identifiers are valuable context, although this was measured only for TLA+. Design artefacts should give exact names for services, topics, fields and states.
- Formal specifications should be reserved for a small number of concurrency-critical or state-critical areas, and experts should own them. In capital markets, order state transitions or settlement instruction idempotency are plausible candidates; ordinary CRUD services are not.
- Mermaid is reasonable for human-readable explanation, but it should be generated from a model or treated as non-authoritative when no checks tie it to the system.

### Gaps
- No empirical comparison was found of coding-agent accuracy given OpenAPI, AsyncAPI, JSON Schema, Protobuf, Structurizr, Mermaid or prose as input. The dedicated search returned only tooling and blog pages.
- No formal benchmark of LLM-generated Structurizr DSL was found.
- Nygard's original ADR format, AsyncAPI, JSON Schema compatibility tools and Buf were not supported by retrieved sources, so no claims are made about them here.

## 3. What does research say about LLMs for architecture and design?

### Takeaway
LLMs can produce plausible decisions and additional useful arguments, but they fall short of human performance, generate low precision against expert rationale, and increase review volume. No controlled study of LLM versus human end-to-end design quality was found.

### Cited Findings
- **ADR decisions.** Given the context of an ADR, GPT-4 in a zero-shot setting generated relevant and accurate decisions but fell short of human-level performance. GPT-3.5 reached similar outcomes with few-shot prompts, and fine-tuned Flan-T5 gave comparable results. Peer-reviewed (ICSA 2024), abstract; these models are now old. — [Dhar et al.](https://arxiv.org/abs/2403.01709)
- **Rationale.** On 100 architecture problems with five LLMs and three prompting strategies, precision was 0.267 to 0.278, recall 0.627 to 0.715 and F1 0.351 to 0.389 against human experts. Of the arguments that experts did not mention, 64.45% to 69.42% were also helpful, 4.12% to 4.87% had uncertain correctness and 1.59% to 3.24% were potentially misleading. Peer-reviewed (TOSEM), abstract. — [Zhou et al.](https://arxiv.org/abs/2504.20781)
- The same study is reported to show 1.98 arguments per decision from humans and 4.55 to 5.77 from LLMs. Snippet from version 1. — [Zhou et al., v1](https://arxiv.org/html/2504.20781v1)
- **Meetings as input.** GADR extracts Nygard-format ADRs from raw transcripts. A feasibility study with five transcripts, four senior architects and fifteen students found that the agentic workflow captured most expert-identified decisions and outperformed zero-shot and few-shot baselines in stability and structural adherence. RAG enrichment improved depth but risked content unfaithful to the transcript. Preprint, abstract. — [GADR](https://arxiv.org/abs/2608.17694). A search summary gives about 18 of 23 senior decisions as covered. Snippet. — [GADR full text](https://arxiv.org/html/2608.17694)
- **Practice.** A study of 291 developer-ChatGPT conversations and a survey of 65 practitioners found nine categories of design tasks, mostly at detailed-design level and used for knowledge acquisition and design-related code generation. Reported benefits include better technology selection and early detection of design flaws. Reported limitations include lengthy outputs, incorrect code and dependence on project context. Preprint (submitted to a journal), abstract. — [Wang et al.](https://arxiv.org/abs/2605.01392)
- **Implicit architecture.** Agents select frameworks, scaffold infrastructure and wire integrations, and almost no one reviews these as architectural decisions. The paper identifies five mechanisms and six prompt-architecture coupling patterns. Its illustrative demonstration shows that prompt wording alone yields structurally different systems. Preprint, abstract; this is conceptual work with a demonstration and not a large empirical study. — [Konrad et al.](https://arxiv.org/abs/2604.04990)
- **Erosion, causal evidence.** Across 151 Java repositories (74 adopters and 77 matched controls) and 1,811 monthly snapshots, total architectural smell counts were essentially unchanged (+1.1%, p = 0.82), and lines of code grew 12.8% (p = 0.003). The 6.7% fall in smell density (p = 0.004) is therefore a denominator effect and not an improvement. Peer-reviewed (SEAA 2026), abstract. — [Larsen and Moghaddam](https://arxiv.org/abs/2606.13298)
- A search summary incorrectly described this paper as accepted at MSR 2026. The arXiv record gives SEAA 2026. — [arXiv record](https://arxiv.org/abs/2606.13298)
- The same paper is reported to note that true erosion requires comparison with an intended architecture, which is rarely available at scale in open source, so smell density is only a proxy. Snippet. — [Full text](https://arxiv.org/html/2606.13298v1)
- **Erosion, generated systems.** A multi-scale audit reports that more capable models generate more bloated and coupled code, that code volume is a near-perfect predictor of structural degradation, and that neither functional correctness nor detailed prompting mitigates the decay. Preprint, abstract. — [Zhu et al.](https://arxiv.org/abs/2605.02741)
- **Counter-example.** One single-author case study reports that an agent, under a specification-first protocol, dismantled a core invariant across 189 files of a 717,725-line codebase with 31 audit passes, 201 corrected defects, a three-day duration and a USD 2,430 cost. No human reviewed the code. Success was assessed by the author, and later sessions showed no observed bug. Preprint, abstract; the evidence is self-reported, although the logs are published. — [Abenhaim](https://arxiv.org/abs/2608.12440)
- **Small models.** SLM-ArchBench benchmarks 10 small language models on ADR generation and reports that models above 3B parameters have robust zero-shot ability. Preprint, snippet. — [SLM-ArchBench](https://www.alphaxiv.org/abs/2603.07091)

### Inferences
- Zhou's low precision does not mean that most LLM arguments are wrong, because many arguments outside the expert set were judged helpful. The practical cost is volume. Taking the snippet figures, LLMs produce about 2.3 to 2.9 times as many arguments per decision, and a reviewer must locate the small misleading share among them.
- LLMs appear better suited to widening options and drafting records than to choosing the final decision. Decisions that carry regulatory or client-facing consequences should have a named human decision-maker.
- Zhu et al. and Larsen and Moghaddam are in partial tension. Zhu finds pronounced decay in generated systems, whereas Larsen finds flat smell counts in adopting repositories. The designs differ: generated systems versus adoption in maintained projects with humans present. Neither compares code against an intended architecture.
- Zhu's finding that detailed prompting does not mitigate decay, read alongside Abenhaim's case, suggests that audit loops against a frozen specification may matter more than prompt detail. One self-assessed case is too weak to establish this.

### Gaps
- No controlled study comparing complete LLM-generated and human-generated designs was found.
- No study was found on the calibration of LLM confidence in design rationale.
- No capital markets or other regulated-domain evidence on LLM design quality was found.
- The sample and metrics in Zhu et al. were not read, and a search summary states that the paper did not test self-correction under test feedback. — [Full text](https://arxiv.org/html/2605.02741v1)

## 4. How is design conformance enforced on generated code, and how is drift detected?

### Takeaway
Current practitioner guidance converges on deterministic checks first, with LLM judges added for semantic drift, but the evidence is practitioner-level. Empirical work supports the value of updating rules, not specifically of architecture tests on agent-written code.

### Cited Findings
- A Radar entry published on 15 April 2026 describes architecture drift reduction that combines deterministic tools such as Spectral, ArchUnit or Spring Modulith with LLM evaluation to detect structural and semantic violations, and uses LLMs to help fix them. It also notes that coding agents can accelerate drift. Practitioner, snippet. — [Thoughtworks Radar](https://www.thoughtworks.com/radar/techniques/architecture-drift-reduction-with-llms)
- Codesai reports adding ArchUnit and ArchUnitTS tests to guard design rules against agents, and argues that deterministic checks are cheaper and more reliable than guidelines or agentic review. Practitioner, snippet. — [Codesai](https://codesai.com/en/posts/2026/04/minimal-architecture-constrainsts-in-agentic-world)
- An ArchUnit article treats a layering test as a fitness function. It warns that generated code, such as MapStruct mappers or OpenAPI clients, can trip rules and should be excluded through an ImportOption or a Generated-annotation predicate. Practitioner, snippet. — [Loiane](https://loiane.com/2026/07/architecture-testing-java-archunit/)
- InfoQ describes agentic fitness functions, which use AI judges for boundary fidelity and semantic contract drift. It says that they do not replace deterministic fitness functions or architects, and it suggests isolating the judge model from the authoring agent. Practitioner, snippet. — [InfoQ](https://www.infoq.com/articles/agentic-fitness-functions-evolutionary-architecture/)
- Assessing 160 rule evolution events, one study found that artefact compliance rose from 49.14% to 72.13% after a rule update. Developers reported changing rules mainly to correct AI errors (77.78%), typically by adding negative constraints. Preprint, abstract. — [Cai et al.](https://arxiv.org/abs/2606.12231)
- archfit checks code against intended architecture and supplies structured repair tasks to agents. This is self-description by the tool. Vendor, snippet. — [archfit](https://pkg.go.dev/github.com/alexei-led/archfit@v0.9.0)
- PactFlow provides an MCP server and AI tooling for generating contract tests from OpenAPI specs, traffic or code. Vendor, snippet. — [PactFlow MCP](https://pactflow.io/blog/pactflow-mcp-server/)
- A community guide shows sample conventions that include a drift-detection skill comparing Pact contracts against the provider's current OpenAPI. Practitioner, snippet. — [Codex CLI contract testing](https://codex.danielvaughan.com/2026/05/17/codex-cli-contract-testing-pactflow-mcp-consumer-driven-verification/)
- A DEV post cites KushoAI as finding that 41% of public APIs show schema drift within 30 days and 63% within 90 days. The primary report was not seen, and the claim does not measure agent-written code. Weak source, snippet. — [DEV post](https://dev.to/deepaksatyam/your-api-has-thousands-of-llm-consumers-none-of-them-can-read-your-changelog-5c9e)
- Augment poses the open question of whether agents can reliably author and maintain contracts, and no independent benchmark was found. Vendor, snippet. — [Augment guide](https://www.augmentcode.com/guides/api-contract-testing-agent-authored-specs)

### Inferences
- A layered enforcement model follows from these sources. Compile-time and CI rules handle dependencies and layering. Contract and schema checks handle interfaces. LLM judges handle semantic drift and advise, without being the sole gate.
- The agent writing the code should not be able to change its own guardrail in the same unchecked change. Changes to architecture tests, contracts and fitness functions should require CODEOWNERS-style human approval. This is a design recommendation and is not an evidenced result.
- Measuring drift requires an explicit intended architecture, because smell metrics alone are a proxy. Density metrics must also be reported with raw counts, following the Larsen and Moghaddam denominator finding.
- Capital markets illustration: an ArchUnit rule could prevent order-routing code from importing a market-data vendor's client directly. A schema compatibility check could block removal of a field used by a downstream regulatory reporting consumer, and a contract test could verify that the consumer still receives the identifiers it needs.
- Generated-code exclusions are a possible blind spot. An exclusion pattern that is too broad could exempt agent-written code from rules, so the distinction between tool-generated and agent-generated code should be explicit.

### Gaps
- No primary or empirical evidence was retrieved for jMolecules or dependency-cruiser in agent workflows.
- No study was found that measures the effect of ArchUnit-style rules or Pact on agent-written code quality or defect rates.
- No published false-positive rate for LLM architecture judges was found.

## 5. How do agents capture their own decisions, and how is a decision superseded?

### Takeaway
Agent decision capture is an emerging practice without a standard, and the guidance comes almost entirely from practitioners. Marking a decision as superseded is widely recommended, but no experiment was found showing that this stops agents from following the old decision.

### Cited Findings
- The Agent Decision Record proposal adds a status field with values including proposed, executed and superseded, plus agent, model and trigger metadata. It is an individual proposal and not a standard. Practitioner, snippet. — [AgDR](https://www.me2resh.com/blog/agent-decision-records)
- One practitioner says that the decision log grows as a side effect of normal agent work, whereas a human-only process would go stale. The same author proposes a periodic agent task that re-checks revisit conditions against vendor changelogs and dependency releases. Practitioner, snippet. — [DEV, yureki_lab](https://dev.to/yureki_lab/how-i-taught-my-ai-coding-agent-to-stop-undoing-my-design-decisions-2o38)
- Actual AI describes an append-only approach and cites Microsoft's Azure guidance. Vendor, snippet. — [Actual AI](https://actual.ai/blog/agent-optimized-adrs)
- Another guide says that the old record is marked as superseded and links to its replacement, because deleting or rewriting it destroys history. It also recommends testing the setup with a fresh agent to confirm that it returns the current decision and status. Practitioner, snippet. — [DEV, naman_here](https://dev.to/naman_here/adrs-for-ai-coding-agents-how-to-make-every-agent-read-architecture-decisions-3he4)
- A related guide has the agent draft a new Proposed ADR that supersedes the old one and updates the index. Practitioner, snippet. — [DEV, soaresdiogo](https://dev.to/soaresdiogo/adrs-are-the-guardrails-your-ai-coding-agent-is-missing-459c)
- Repowise separates three outcomes: amend for corrected context, supersede for a replacement decision, and archive for records that no longer act as guidance. It argues that a stale ADR can mislead an agent more than a missing one, and that disagreement between code and decision should default to marking the ADR stale. Vendor, snippet. — [Repowise](https://repowise.dev/blog/guides/use-git-history-to-catch-stale-adrs-before-they-mislead-agents)
- Duncan Davidson takes a different position. Agents need the ruling that governs today, with explicit permission to stop when it no longer fits, and Git can carry the history while the record is updated in place. Practitioner, snippet. — [Davidson](https://duncandavidson.com/agents-love-decisions)
- Nimbalyst describes ADRs written by a coding agent. Vendor; content was not retrieved beyond the title and search context. — [Nimbalyst](https://nimbalyst.com/blog/architecture-decision-records-written-by-your-coding-agent/)
- Developers report adding new negative constraints instead of editing existing rules. The same study calls for automated conflict detection. Preprint, abstract. — [Cai et al.](https://arxiv.org/abs/2606.12231)
- GADR warns that RAG enrichment can add content that is unfaithful to the source, which raises traceability questions for automated documentation. Preprint, abstract. — [GADR](https://arxiv.org/abs/2608.17694)

### Inferences
- Immutable records and in-place updates do not need to conflict. The audit store can be append-only, while the view served to agents shows only the currently active decision. This also suits a regulated firm's need for history.
- Status text alone is a weak control, because an agent that retrieves an old file may still follow it. A stronger design has four parts: (1) exclude superseded records from default retrieval, (2) keep them reachable only on explicit request, (3) show a superseded-by banner on any direct read, and (4) replace or retire the enforcing test in the same change. These are proposals that need testing.
- Cai et al.'s additive pattern points to a specific supersession hazard. Old and new rules can coexist, and a new "do not" rule can sit beside the old instruction. Supersession should therefore search for and remove derived rules, skills and examples as well as change the ADR.
- Agent decisions should be tiered. Local reversible choices can go in a session or PR log. Decisions that add a dependency, change a boundary, alter a data contract or affect a control should create a Proposed ADR and stop for human acceptance. Agent drafts should separate facts observed in the source from inferred rationale and should cite the commit, ticket or transcript.
- Agent-written rationale may be reconstructed after the event and may not reflect what actually drove the choice. It should be labelled as agent-stated.
- Capital markets illustration: when a firm replaces its security master vendor, the old ADR should be superseded, the rule that bans direct use of the new vendor's API should be retired, and a fresh agent should be tested to confirm that it selects the new adapter.

### Gaps
- No controlled study was found on whether agents obey status fields or supersession markers.
- No formal standard for agent-written ADRs was found.
- The cited Microsoft guidance was seen only through Actual AI's reference to it.

## 6. What do AWS AI-DLC, Kiro, Spec Kit, Tessl and BMAD design artefacts contain?

### Takeaway
All five capture structural design, but they differ in how they treat rationale and enforcement. BMAD is the only one whose documented architecture output explicitly includes ADRs, and Spec Kit has the clearest documented gate.

### Cited Findings
| Framework | Design artefacts | Rationale and alternatives | Gate or enforcement | Evidence quality |
|---|---|---|---|---|
| AWS AI-DLC | Application Design produces `components.md`, `services.md`, `component-methods.md` and `component-dependency.md`. Functional Design produces `business-logic-model.md`, `business-rules.md`, `domain-entities.md` and, conditionally, `frontend-components.md` per unit. NFR Design and Infrastructure Design are conditional. | No dedicated ADR artefact was seen in the snippets. | Stages may be skipped with reasons recorded. | Official stage reference and repository summary, snippet |
| Kiro | `design.md` covers technical architecture, sequence diagrams and implementation considerations. Six headings are reported: Overview, Architecture, Components and Interfaces, Data Models, Error Handling, Testing Strategy. | No dedicated section is reported. | Not confirmed. | Official documents confirm the broad content; the exact headings come from an unofficial prompt archive |
| Spec Kit | `plan.md`, `research.md`, `data-model.md` and `contracts/`. | Complexity Tracking records a violation, why it is needed and the simpler alternative rejected. | Constitution Check runs before Phase 0 and again after Phase 1 design. Unresolved NEEDS CLARIFICATION items raise an error. | Community copies of the template; may lag the official version |
| Tessl | `.spec.md` with YAML frontmatter that targets files or globs, requirements and inline `[@test]` links. | None reported. | Requirement-to-test links. | Vendor registry page; other details are secondary |
| BMAD | `architecture.md` with ADRs, and optional `project-context.md` for implementation rules. | ADR entries reportedly cover context, options, trade-offs and rationale. | Implementation readiness check after epics, with PASS, CONCERNS or FAIL. | Official workflow map; ADR content detail is from a mirrored guide |

Sources:
- AI-DLC: [Construction stage reference](https://awslabs.github.io/aidlc-workflows/reference/04-stages/construction/); [repository summary](https://docsearch.algolia.com/mcp/docs/repo/awslabs/aidlc-workflows); [DZone write-up showing skipped stages](https://dzone.com/articles/using-aidlc-to-build-documents).
- Kiro: [Official specs documentation](https://kiro.dev/docs/specs/index); [unofficial archived system prompt](https://elifuzz.github.io/awesome-system-prompts/kiro); [community skill using the same headings](https://skills.cat/skills/jasonkneen/kiro/design-documentation). Another community skill adds Correctness Properties and property-based tests, and this is not confirmed as official Kiro behaviour — [Spec Creator](https://skills.lc/josfko/recordplus/josfko-recordplus-claude-skills-spec-creator-skill-md).
- Spec Kit: [Template copy in a third-party repository](https://forge.alexselimov.com/aselimov/notex.nvim/src/branch/master/.specify/templates/plan-template.md); [Mintlify template documentation](https://www.mintlify.com/github/spec-kit/advanced/templates).
- Tessl: [Tile files](https://tessl.io/registry/tessl-labs/spec-driven-development/files). A third-party summary describes three spec parts and `@generate` and `@describe`, with no primary source found — [Ry Walker](https://rywalker.com/research/tessl). A critical review says that the Registry entered open beta on 16 September 2025, that the regeneration Framework is in closed beta and JavaScript-only, and that the installable tile is spec-first — [CodeMySpec](https://codemyspec.com/blog/tessl-review).
- BMAD: [Workflow map, French edition](https://docs.bmad-method.org/fr/reference/workflow-map/); [Getting Started](https://docs.bmad-method.org/tutorials/getting-started); [mirrored solutioning guide, possibly older](https://git.biohazardvfx.com/Nicholai/united-tattoo/src/branch/UI-Overhaul/.bmad/bmm/docs/workflows-solutioning.md).

### Inferences
- No framework's documented artefacts, as seen here, provide a full model with threat-model linkage, supersession handling and executable design conformance.
- The AI-DLC artefact set separates structure, business rules and NFR design cleanly, but a platform built on it would need a place for decisions and rejected alternatives. BMAD's approach and Spec Kit's Complexity Tracking table offer patterns to borrow.
- Spec Kit's alternatives record only covers violations of the constitution. It would not capture an ordinary choice between two compliant options, such as choosing between two messaging technologies.

### Gaps
- Primary templates could not be fetched, so the Kiro headings, Spec Kit's current template and the contents of AI-DLC's `components.md` and NFR Design outputs remain unconfirmed.
- Security or threat-model artefacts in these frameworks were not confirmed.
- Current version numbers of each framework as of November 2026 were not confirmed.

## 7. What are the failure modes?

### Takeaway
The main documented failure modes are unreviewed implicit decisions, plausible output that is valid yet wrong, loss of the intended baseline, stale or conflicting guidance, and excess review volume. Evidence is strong for some of these and anecdotal for others.

### Cited Findings
- **Unreviewed implicit design.** Prompt wording alone produced structurally different systems, and agents make architecture decisions that almost no one reviews as such. Preprint, abstract. — [Konrad et al.](https://arxiv.org/abs/2604.04990)
- **Valid but wrong artefacts.** Every model in TLA+-Bench writes valid TLA+ far more often than correct TLA+. Preprint, abstract. — [TLA+-Bench](https://arxiv.org/abs/2607.23425). The ICSOFT evaluation also identifies five recurring hallucination categories. Peer-reviewed, abstract. — [Bisharat et al.](https://arxiv.org/abs/2606.05792)
- **Unjustified rationale.** Between 1.59% and 3.24% of LLM arguments not mentioned by experts were potentially misleading, and between 4.12% and 4.87% were of uncertain correctness. Peer-reviewed, abstract. — [Zhou et al.](https://arxiv.org/abs/2504.20781)
- **Unfaithful enrichment.** RAG can deepen an ADR while adding content not supported by the transcript. Preprint, abstract. — [GADR](https://arxiv.org/abs/2608.17694)
- **Lost rationale.** Rationale is documented inadequately because of low motivation and effort. Peer-reviewed, abstract. — [Zhou et al.](https://arxiv.org/abs/2504.20781). ADR adoption has also been slowed by time constraints and inconsistent uptake. Peer-reviewed, abstract, 2024. — [Dhar et al.](https://arxiv.org/abs/2403.01709)
- **Misleading metrics.** A falling smell density can reflect code growth and not any improvement. Peer-reviewed, abstract. — [Larsen and Moghaddam](https://arxiv.org/abs/2606.13298)
- **Stale ADRs.** A stale ADR can mislead an agent more than a missing one. This is an unmeasured vendor argument. Vendor, snippet. — [Repowise](https://repowise.dev/blog/guides/use-git-history-to-catch-stale-adrs-before-they-mislead-agents)
- **Stale diagrams.** Structurizr's vendor argument is that model-based views stay consistent where independently drawn diagrams do not. It says nothing about whether the model matches the code. Vendor, snippet. — [Structurizr](https://docs.structurizr.com/ai/dsl-generation)
- **Conflicting guidance.** Thoughtworks says that instructions accumulate organically and conflict, and it recommends minimal, coherent sets surfaced progressively. Practitioner, snippet. — [Radar Vol. 34 digest](https://agentic-ai.readthedocs.io/en/latest/AgenticTechStack/thoughtworks-radar-vol34/)
- **Priorities not reaching rule files.** Architectural constraints are rated as important but are under-represented in the rules. Preprint, abstract. — [Cai et al.](https://arxiv.org/abs/2606.12231)
- **Review burden.** Survey respondents list lengthy outputs as an LLM design limitation. Preprint, abstract. — [Wang et al.](https://arxiv.org/abs/2605.01392). LLMs also generate more arguments per decision than experts do. Snippet. — [Zhou et al., v1](https://arxiv.org/html/2504.20781v1)
- **Weak metrics for ADR generation.** The EASE ADR study is reported to rely on automatic fidelity metrics, which do not establish decision quality. Secondary, snippet. — [Pith summary](https://pith.science/paper/2604.03826)

### Inferences
| Failure mode | Possible detection | Possible control |
|---|---|---|
| Implicit decision made during coding | PR scan for new dependencies, new services or changed contracts | Require a linked Proposed ADR |
| Confident but unjustified design | Check that each claim cites a requirement, constraint or source | Separate sourced facts from inferred reasoning, and name a human decision-maker |
| Lost rationale | Check that accepted ADRs have alternatives, drivers and revisit conditions | Capture at the point of decision, including from reviewed meeting transcripts |
| Stale decision or diagram | Compare records against code and git history on a schedule | Mark as stale by default, and generate diagrams from a model where feasible |
| Superseded decision still followed | Run fresh-agent probes that ask for the governing decision | Exclude superseded records from default retrieval and retire linked rules |
| Excess review burden | Track reviewer time and ADR volume per change | Set materiality thresholds, cap draft length and auto-check the mechanical items |
| Agent weakens its own guardrail | Flag changes to architecture tests or contracts | Require independent approval for those files |

- This table is a synthesis and has not been validated as a set. In a capital markets firm, the first controls to pilot would plausibly be those on contract changes and new dependencies, because they can be detected deterministically and affect downstream settlement, risk and reporting consumers.

### Gaps
- No study was found that quantifies the review burden of agent-drafted ADRs or design documents.
- No study was found that measures diagram staleness in agent-maintained repositories.
- No study was found that compares the harm of a stale ADR with that of a missing one.
