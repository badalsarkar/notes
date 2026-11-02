# Recommended structure for engineering document types when agents and LLMs are among the readers

Evidence labels used throughout these notes are as follows.

- **[Empirical]** marks a measured result from a study or benchmark.
- **[Standard]** marks a published specification, a regulation, or a regulator publication.
- **[Vendor guidance]** marks advice from a platform vendor, which rests on that vendor's experience and is usually not backed by published data.
- **[Practitioner]** marks expert opinion, community practice, or marketing-adjacent content.
- Items under "Inferences" are this researcher's reasoning and are not sourced claims.

Source quality note: most fetches returned a model-written extraction of the page and not the raw page, although short quotations were returned verbatim. Items that rest only on search-result summaries are marked "(search summary only)" and should be verified before they are quoted.

## Per document type: which template or schema fits, which metadata is useful, and which parts suit prose or structured data?

### Takeaway

No study was found that compares templates for any of the four document types by agent outcome, so the per-type template recommendations rest on standards and vendor guidance and not on experiments. The best-supported pattern is a validated metadata header, a fixed section skeleton, and normative statements with stable IDs, with narrative kept for context and rationale and with machine-checkable facts moved into a model (CALM, OSCAL, or Rego) only where a tool actually consumes them.

### Cited Findings

**Tech standards**

- [Standard] RFC 8174 states that the BCP 14 key words have their defined meanings only when they are in all capitals, and that lowercase forms have their normal English meanings. Authors should include a boilerplate sentence that says so — [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174).
- [Standard] RFC 2119 defines MUST as an absolute requirement, SHOULD as a recommendation that may be ignored for valid reasons after the implications are weighed, and MAY as truly optional — [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).
- [Standard] RFC 2119 section 6 says imperatives should be used sparingly and only where actually required for interoperation, and should not be used to impose a method that interoperability does not require — [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119). The limitation for an internal standard is that "interoperation" has to be reinterpreted, because internal standards also carry policy and preference.
- [Standard] The RFC series records relationships between documents in the header through "Updates: nnnn" and "Obsoletes: nnnn" fields — [RFC 7322 section 4.1.4](https://www.rfc-editor.org/rfc/rfc7322.html).
- [Vendor guidance] GitHub Copilot scopes instruction files with `applyTo` glob patterns in frontmatter, which is a working example of a machine-read "applies-to" field. Path-specific files currently work only with Copilot cloud agent and Copilot code review on GitHub.com — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions).
- [Vendor guidance] Anthropic recommends matching specificity to fragility: text-based instructions where several approaches are valid, and exact scripts where operations are fragile or consistency is critical — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- [Empirical] A study of repository context files concluded that they are useful for specifying non-standard coding practices, while repository overviews were not helpful — [Gloaguen et al., arXiv 2602.11988](https://arxiv.org/abs/2602.11988).

**Design decisions and ADRs**

- [Standard-like template] MADR provides optional frontmatter of `status`, `date`, `decision-makers`, `consulted`, and `informed`. Its required sections are the title, Context and Problem Statement, Considered Options, and Decision Outcome. Its optional sections are Decision Drivers, Consequences, Confirmation, Pros and Cons of the Options, and More Information — [MADR template](https://raw.githubusercontent.com/adr/madr/develop/template/adr-template.md). The limitation is that all metadata, including `status`, is optional, so an agent cannot rely on it unless a repository validates it.
- [Practitioner, origin of the format] Nygard's format has a short noun-phrase title, Context, Decision in full sentences in active voice, Status, and Consequences. Numbers are sequential and are not reused — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
- [Vendor guidance] Microsoft says an ADR is an append-only log, that accepted records should not be edited, and that a changed decision needs a new record linked to the original. It also recommends recording the confidence level, and says the decision must stand alone without linked supplemental material — [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record). MADR has no confidence field, so this needs a local extension.
- [Vendor guidance] AWS states that accepted ADRs are immutable, that the owner adds a timestamp, version, and stakeholder list on approval, that rejected ADRs record the reason for rejection, and that code reviewers use ADRs to reject violating changes — [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html).

**Architecture documents**

- [Standard] FINOS CALM describes itself as "Software architecture as code — human-readable, machine-validated". It models nodes with a unique ID and type, and relationships with a source and destination, in JSON. Its example file is named `trading-system.architecture.json`, and its CLI generates, validates, and documents architectures — [CALM](https://calm.finos.org/). Interfaces, controls, flows, and metadata are further core concepts — [CALM core concepts](https://calm.finos.org/core-concepts/).
- [Standard] A CALM control has a name, description, and requirements, and each requirement pairs a `requirement-url` schema with a `config-url` configuration. The documented example is a permitted-connection control configured with `"protocol": "mTLS"` — [CALM controls](https://calm.finos.org/core-concepts/controls).
- [Practitioner] Morgan Stanley contributed CALM to FINOS, with v1.0 reported as released in August 2025 (search summary only) — [DevOps.com](https://devops.com/morgan-stanley-open-sources-calm-the-architecture-as-code-solution-transforming-enterprise-devops). A CalmStudio MCP server is reported to let assistants create, validate, and export architectures (search summary only) — [FINOS CCC ecosystem page](https://ccc.finos.org/ecosystems/calmsuite).
- [Standard] The C4 model has four abstraction levels (software system, container, component, and code) with matching diagrams and is notation independent and tooling independent — [C4 model](https://c4model.com/). The limitation is that C4 by itself prescribes no machine-validated file format, so it does not provide a schema for an agent to check against.

**Security policies**

- [Standard] OSCAL has a control layer (catalog, profile, control mapping), an implementation layer (system security plan, component definition), and an assessment layer (assessment plan, assessment results, plan of action and milestones). Each model is represented in XML, JSON, and YAML with published schemas — [NIST OSCAL layers](https://pages.nist.gov/OSCAL/learn/concepts/layer/).
- [Standard] An OSCAL catalog requires metadata of title, last-modified, version, and oscal-version, with optional revisions and responsible parties. Each control requires an `id` and `title` and can carry params, props, links, and parts, and a part can hold prose — [OSCAL catalog outline](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/catalog/json-outline/). This shows that OSCAL itself keeps prose inside a structured envelope.
- [Vendor guidance] OPA policies are written in Rego and make decisions on hierarchical structured data. OPA argues that decoupled policy can be read, written, analysed, versioned, and distributed separately from the service and improves the ability to discover violations and conflicts — [OPA philosophy](https://www.openpolicyagent.org/docs/philosophy). The page states no explicit limitation, so this is the project's own advocacy.
- [Practitioner] Consultancies and vendors report that OSCAL is a language and not deployable software, that raw files are verbose and hard to write by hand, that it requires RMF and 800-53 knowledge, and that it saves time only with a tooling pipeline (search summary only, vendor-sourced, not independently verified) — [Elevate](https://elevateconsult.com/insights/fedramp-automation-when-oscal-saves-time), [Elevate comparison](https://elevateconsult.com/insights/oscal-vs-traditional-fedramp-documentation-choosing-the-right-compliance-approach/), [Knox Systems](https://knoxsystems.com/resources/open-security-controls-assessment-language).

### Inferences

**Proposed common header.** The field set below is this researcher's synthesis. The right-hand source column shows where each field has a precedent, and no source validates the set as a whole.

| Field | Purpose for an agent | Precedent |
| --- | --- | --- |
| `id` | This field gives a stable citation target. | OSCAL control `id`; Nygard numbering |
| `title` | This field states the topic without surrounding context. | Nygard; MADR |
| `doc_type` | This field lets a retriever apply type-specific rules. | No direct precedent; proposed here |
| `status` | This field allows filtering before retrieval. | MADR; Microsoft; AWS |
| `owner` | This field shows who resolves a conflict or exception. | AWS ownership; OSFI inventory owner |
| `version` | This field lets a citation name an exact text. | OSCAL metadata; AWS |
| `effective_date` | This field separates publication from applicability. | OSFI publishes a future effective date for E-23 |
| `next_review` | This field allows a deterministic freshness check. | OSFI next review date; Microsoft `ms.update-cycle` |
| `supersedes` and `superseded_by` | These fields express direct and reverse links. | RFC Obsoletes; Microsoft and AWS supersession |
| `applies_to` | This field scopes the rule to paths, systems, or asset classes. | Copilot `applyTo` |
| `classification` | This field drives permission-aware retrieval. | Purview sensitivity labels in Azure AI Search |
| `authority_rank` | This field states precedence when sources conflict. | No direct precedent; proposed here, and untested |

**Per-type recommendation and limitation**

- **Tech standard.** The recommended template is the header, Purpose, Scope, Definitions, numbered Requirements with one normative statement per ID, a rationale line per requirement, compliant and non-compliant examples, an Enforcement line naming the linter or CI check, Exceptions, and References. The limitation is that uppercase key words give precision to humans, but no study was found that shows agents comply better with them.
- **ADR.** The recommended template is MADR with `status` made mandatory by schema, plus `supersedes`, `superseded_by`, `applies_to`, and `confidence`, and with the Confirmation section used to name the fitness function or check. The limitation is that ADRs record history, so an agent that reads one for current rules can act on a decision that a later standard has overtaken unless the current state is also published elsewhere.
- **Architecture document.** The recommended form is a CALM or similar model for topology and controls, with a narrative for context, constraints, and rejected alternatives, and with diagrams generated from the model. The limitation is that the model requires upkeep and can drift from the deployed system unless it is checked against that system, and it expresses no reasoning.
- **Security policy.** The recommended form is a short prose policy for intent and accountability, control statements with IDs, and Rego or a similar language for the subset that can be decided mechanically, with OSCAL added only when an assessment or exchange consumer exists. The limitation is that OSCAL is costly to author and that Rego covers only decisions over structured input, so judgement-based controls stay in prose.

### Gaps

- No controlled study was found on whether MADR, Nygard, or any other ADR template changes agent outcomes.
- No evidence was found that BCP 14 capitalisation improves agent compliance. Anthropic only mentions "MUST filter" as one possible refinement to try during iteration — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- No published schema was found that standardises frontmatter across the four document types.

## How should a superseded or deprecated document be represented so that an agent does not act on it, and what is known about staleness, conflicts and authority ranking?

### Takeaway

Evidence shows that LLMs handle source conflicts poorly by default and improve markedly when told what kind of conflict they face, but no study was found that tests status metadata in engineering documents directly. The safest design is therefore layered: exclude superseded documents from default retrieval, label them in the body as well as in metadata so a stray chunk still carries the warning, and keep them available in an archive for history and evidence.

### Cited Findings

- [Empirical] The CONFLICTS benchmark has 458 queries averaging 9.2 search results each, with 62 labelled as freshness conflicts. Its expected behaviour for freshness conflicts is to prioritise up-to-date information and optionally acknowledge outdated sources — [CONFLICTS paper, arXiv 2506.08500](https://arxiv.org/html/2506.08500).
- [Empirical] In that benchmark, expected-behaviour scores with a plain prompt ranged from about 59 to 68. A two-step pipeline that predicts the conflict type first added about 9 points on average, and supplying the gold conflict type added about 24 points and reached roughly 87 to 91. Models predicted the conflict type correctly only about 54 to 65 percent of the time — [arXiv 2506.08500](https://arxiv.org/html/2506.08500). The limitation is that the corpus is web search results and not enterprise documents.
- [Empirical] The same paper describes no method for scoring source credibility or authority — [arXiv 2506.08500](https://arxiv.org/html/2506.08500).
- [Empirical] WikiContradict provides 253 human-annotated instances of contradictory Wikipedia passages and tests whether models give a complete perspective on the conflict (search summary only) — [IBM Research](https://research.ibm.com/publications/wikicontradict-a-benchmark-for-evaluating-llms-on-real-world-knowledge-conflicts-from-wikipedia).
- [Empirical] With real conflicting documents, knowledge updates fail less often than previously reported, and when they fail the incorrect answer from parametric memory tends to appear in the context — [Kortukov et al., arXiv 2404.16032](https://arxiv.org/abs/2404.16032). This implies that quoting an outdated value in a document, even to reject it, carries some risk, although the paper did not test that case directly.
- [Standard-like] OWASP names "data federation knowledge conflict errors" as a risk when sources contradict each other, and notes that a model may fail to override outdated training knowledge with retrieved data — [OWASP LLM08](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/).
- [Practitioner] Nygard keeps reversed decisions in place and marks them superseded, because the history remains useful — [Nygard 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
- [Vendor guidance] Microsoft and AWS both require a new record that supersedes the old one, and AWS sets the old record's state to Superseded — [Microsoft](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record), [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html).
- [Vendor guidance] Anthropic advises against date-conditional instructions and recommends a "Current method" section plus a collapsed "Old patterns" section labelled with the deprecation date — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). The limitation is that this keeps old content in the same file, which a chunker may separate from its label.
- [Vendor guidance] In GitHub Copilot, all relevant instruction sets are provided together, with personal instructions ranked above repository and then organisation instructions, and the nearest `AGENTS.md` takes precedence. GitHub also advises avoiding conflicting instructions — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions). This is the clearest published example of authority ranking, and it is defined by the tool and not by document metadata.

### Inferences

- The recommended layered representation has five parts, and the evidence supports the direction of it but not each individual part.
  - The retrieval layer filters on `status` so that superseded documents are excluded by default. This is the only part that does not depend on model behaviour.
  - The file moves to an `archive/` path or is otherwise excluded from the agent index, because Anthropic notes that paths and names act as signals — [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).
  - The first line of the body and each section carries a plain statement such as "This standard was superseded by STD-142 on 2026-03-01 and must not be applied." This protects a chunk that is separated from its frontmatter, and it can be injected by the chunking pipeline and not by hand.
  - CI enforces that `superseded_by` resolves to an accepted document and that the reverse link exists.
  - The answer layer shows the ID, version, and status of each cited source so that a human can detect an error.
- The gold-label result in CONFLICTS suggests that telling a model explicitly about a conflict helps, so a retrieval layer could add a note such as "These two sources conflict, and STD-142 takes precedence." This is an extrapolation, because the paper supplied the conflict category and not document metadata.
- Authority ranking should be an explicit, small, ordered list, for example regulation, then security policy, then technical standard, then accepted ADR, then design document, then wiki page. A rank applied at the retriever or stated in the agent's instructions is more testable than a rank implied by prose. This ordering is opinion and needs firm-specific legal and risk input.
- An ADR should not be edited to remove its old decision, because immutability is the point of the format. Only the status and forward link change, which is the one exception AWS describes.
- Deleting a document is not an acceptable way to deprecate it in a regulated firm, because the retention duties described in the regulatory section may still apply.

### Gaps

- No study was found that measures whether a `status: superseded` label, a banner, or a file path reduces the rate at which an agent acts on an outdated engineering document. This is the most valuable experiment for the report to recommend.
- No evidence was found for any standard authority-ranking scheme for enterprise documents, and the ordering above has no empirical support.

## Which authoring practices help retrieval and agents, and what is the evidence for each?

### Takeaway

Evidence is strongest for making chunks carry their own context and for avoiding image-only content, and it is weak or mixed for table serialisation and absent for most style rules. One important counterweight is that a study of coding agents found context files and repository overviews increased cost without generally improving task success, so more documentation for agents is not automatically better.

### Cited Findings

**Self-contained sections, explicit naming, and pronouns**

- [Empirical, vendor-run] Anthropic's example chunk, "The company's revenue grew by 3% over the previous quarter", names neither company nor period. Prepending generated context reduced top-20 retrieval failure by 35 percent (5.7 to 3.7 percent), by 49 percent with contextual BM25 (to 2.9 percent), and by 67 percent with reranking (to 1.9 percent) — [Anthropic contextual retrieval](https://www.anthropic.com/news/contextual-retrieval). The limitation is that this is a vendor test of an ingestion technique, and it supports the diagnosis but does not test an authoring rule.
- [Vendor guidance] Kapa says sections "should ideally make sense when encountered in isolation", warns against "this", "the endpoint", and "as mentioned above", and advises keeping related information close together because it is then more likely to stay together after chunking — [Kapa writing best practices](https://docs.kapa.ai/improving/writing-best-practices). Kapa sells a documentation assistant and reports no metrics on this page.

**Descriptive headings and consistent terminology**

- [Vendor guidance] Kapa recommends specific headings, such as changing "Connection problems" to "CloudSync connection problems", and advises quoting exact error messages in headings — [Kapa](https://docs.kapa.ai/improving/writing-best-practices).
- [Vendor guidance] Anthropic recommends using one term consistently — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

**Stable IDs and one topic per file**

- [Standard] OSCAL requires an `id` on every control and Nygard requires monotonic, non-reused numbers — [OSCAL](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/catalog/json-outline/), [Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
- [Vendor guidance] Anthropic recommends descriptive file names such as `form_validation_rules.md` and domain-based directories, so that a query about one domain loads only that domain's file — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- [Practitioner] platformOS recommends splitting long multi-topic pages into topics that each answer one question (search summary only) — [platformOS](https://www.platformos.com/blog/post/structuring-documentation-for-ai-comprehension).

**Progressive disclosure and small index files**

- [Vendor guidance] Anthropic's skill model loads name and description at startup, the body when relevant, and bundled files only when needed — [Agent Skills engineering post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).
- [Vendor guidance] Anthropic recommends keeping the skill body under 500 lines, keeping references one level deep because nested references may be only partly read, and adding a table of contents to reference files longer than 100 lines — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- [Empirical] Gloaguen et al. found that context files generally did not improve task success and raised inference cost by over 20 percent on average, while agents did follow the instructions. They conclude that any use should be rigorously evaluated — [arXiv 2602.11988](https://arxiv.org/abs/2602.11988). Summaries report that developer-written files gave a gain of about 4 percent and LLM-generated files lowered success slightly (search summary only, verify against the PDF) — [ICLR 2026 listing](https://iclr.cc/virtual/2026/10021142). The limitation is that this studied coding tasks in code repositories, not retrieval over standards or policies.
- [Practitioner] `llms.txt` is described as a proposed standard and not a finalised one (search summary only) — [Weaviate contributor guide](https://docs.weaviate.io/contributor-guide/weaviate-docs/llms).

**Tables versus prose**

- [Empirical] The TeleTables benchmark used 2,220 tables and 500 verified questions. Markdown used 707 tokens per table against 1,224 for HTML, at competitive accuracy, with HTML strongest for most models by a small margin — [arXiv 2601.04202](https://arxiv.org/html/2601.04202).
- [Empirical, conflicting] One paper reports HTML underperforming and Markdown performing poorly on structure tasks under noise — [arXiv 2310.10358](https://arxiv.org/pdf/2310.10358). Another study is summarised as ranking HTML first (search summary only) — [Table Meets LLM review](https://liner.com/review/table-meets-llm-can-large-language-models-understand-structured-table). TQA-Bench reports JSON as worst for multi-table questions (search summary only) — [arXiv 2411.19504](https://arxiv.org/pdf/2411.19504). Best format varies by model in a prompt-styling study (search summary only) — [arXiv 2508.13948](https://arxiv.org/pdf/2508.13948).
- [Practitioner] A blog test of 11 formats on GPT-4.1 mini put Markdown key-value first at 60.7 percent and found CSV below natural language (search summary only, not peer reviewed) — [Gigazine report](https://gigazine.net/gsc_news/en/20251007-ai-table-format).
- [Vendor guidance] Kapa advises keeping simple reference tables whose rows stand alone and converting merged-header comparison tables into lists, because they "become ambiguous when converted to plain text" — [Kapa](https://docs.kapa.ai/improving/writing-best-practices).

**Diagrams**

- [Empirical] In TeleTables, image input scored 77.2 against 85.6 for HTML on Qwen2.5-VL 72B and 53.8 against 81.0 on Gemma 27B, at about 11,607 tokens per table. A hybrid of image and HTML recovered most of the loss at 12,831 tokens — [arXiv 2601.04202](https://arxiv.org/html/2601.04202). This concerns tables as images and not architecture diagrams.
- [Empirical] An ICML 2025 paper reports that vision-language models identify entities accurately but understand relationships in diagrams much less well (search summary only) — [Hou et al.](https://proceedings.mlr.press/v267/hou25c.html). The SADU benchmark reports that architecture diagram understanding remains challenging (search summary only) — [arXiv 2604.04009](https://arxiv.org/html/2604.04009v1).
- [Empirical, counter-evidence] A 2026 UFMG thesis found that image inputs outperformed SVG/XML text descriptively in LLM reviews of microservice diagrams, and experts preferred image-based reasoning in 60.8 percent of decided cases, although the effect on score agreement was not statistically robust (search summary only) — [UFMG thesis](https://monografias.dcc.ufmg.br/monografia/how-reliable-are-llm-evaluations-of-microservice-architecture-diagrams/). SVG/XML is not the same as Mermaid or PlantUML, so this does not settle the question.
- [Vendor guidance] Kapa says critical visual information must have a text description — [Kapa](https://docs.kapa.ai/improving/writing-best-practices).

**Examples, counter-examples, and rationale**

- [Vendor guidance] Anthropic recommends a small set of diverse, canonical examples over exhaustive edge-case lists — [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Its skill guidance uses good and bad pairs and says concrete examples convey style better than description alone — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- [Vendor guidance] Microsoft says a record without justification loses its value because stakeholders cannot evaluate whether the decision still applies — [Microsoft](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record). AWS says the reason is what prevents later overruling by people who were not involved — [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html). Both address human readers.

### Inferences

| Practice | Evidence strength | Limitation |
| --- | --- | --- |
| Self-contained sections and explicit names | Moderate, because the retrieval failure mechanism is measured even though the authoring rule is not | Repeated names increase length and can read awkwardly to humans. |
| Descriptive headings | Weak, because only vendor guidance supports it | Long headings can make navigation harder. |
| Stable IDs | Standards precedent only | IDs need a registry and a no-reuse rule. |
| One topic per file | Weak, because only vendor guidance supports it | Many small files increase link maintenance and can scatter context. |
| Progressive disclosure | Vendor guidance, with partly cautionary evidence from the context-file study | An agent can fail to follow a link, and discovery depends on the quality of descriptions. |
| Text instead of image-only content | Moderate for tables, weak for architecture diagrams | Text diagrams can become hard to read at scale, and one thesis points the other way. |
| A specific table format | Conflicting, because the result depends on the model and task | Any firm-wide rule should be tested on the firm's models. |
| Examples and counter-examples | Vendor guidance only | A counter-example can be retrieved alone and copied, so it needs an explicit label in the same chunk. |
| Rule rationale | Vendor guidance aimed at humans | Rationale adds tokens, and its effect on agents is untested. |

- Rationale has a plausible agent-specific value, because an agent can apply the reason to a case that the rule does not cover. This is untested, and it should be presented as opinion.
- Authoring for self-containment and contextual retrieval at ingestion are complementary. Contextual retrieval has a generation cost and repairs retrieval, but it cannot supply a fact that the source never stated.

### Gaps

- No controlled study was found that compares Mermaid or PlantUML source with rendered images for LLM comprehension. MermaidSeqBench tests generation of diagrams and not comprehension of them — [arXiv 2511.14967](https://arxiv.org/html/2511.14967v1).
- No documentation style guidance on agent readers was found from Google or AWS in the search performed, although the search was not exhaustive.
- OpenAI's "Harness engineering" post could not be read because the site returned HTTP 403, so no claim from it appears in these notes — [OpenAI](https://openai.com/index/harness-engineering/).

## When should prose be the source of truth, and when should a structured source generate the prose?

### Takeaway

No comparative study of cost or agent outcomes was found, so this is a matter of reasoned practice. A structured source should be authoritative when a tool decides or validates something with it, and prose should be authoritative when the content is reasoning, judgement, or accountability.

### Cited Findings

- [Vendor guidance] OPA presents policy-as-code as separating policy from services so that it can be versioned, analysed, and updated without redeployment — [OPA philosophy](https://www.openpolicyagent.org/docs/philosophy).
- [Standard] CALM generates documentation from a validated model through its CLI, which is single-sourcing applied to architecture — [CALM](https://calm.finos.org/).
- [Standard] OSCAL holds prose inside structured `parts`, which is a mixed model and not a pure replacement of prose — [OSCAL catalog outline](https://pages.nist.gov/OSCAL-Reference/models/v1.1.3/catalog/json-outline/).
- [Vendor guidance] Anthropic recommends scripts over generated code for deterministic operations because they are more reliable and consistent, and recommends text for context-dependent decisions — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- [Practitioner] OSCAL is described as designed for machines to process and not for humans to write, and as saving time only with a producing and validating pipeline. One vendor estimates six-figure consulting costs for manual conversion (search summary only, vendor figures that should be treated cautiously) — [Elevate](https://elevateconsult.com/insights/fedramp-automation-when-oscal-saves-time), [Knox Systems](https://knoxsystems.com/resources/open-security-controls-assessment-language).
- [Standard] SR 26-2 treats clear policies and documentation as governance elements and does not prescribe a format — [SR 26-2 attachment](https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf).

### Inferences

| Option | Use it when | Costs and limitation |
| --- | --- | --- |
| Prose as the source, with validated frontmatter (docs-as-code) | The content is rationale, trade-offs, or accountability. | Burden is low and diffs are readable, but rules cannot be evaluated by a machine and can drift from enforcement. |
| Prose plus linked enforcement, such as a rule ID that maps to a linter or Rego rule | Some rules can be checked and the document remains the human contract. | Two artefacts must stay aligned, so a CI check on the ID mapping is needed. |
| Structured source that generates prose (CALM, OSCAL) | A tool consumes the data and several views are needed. | Schema upkeep and tool dependency are significant. Reviewers read JSON diffs, and generated prose often lacks reasoning, so a hand-written narrative section is still needed. |
| Code as the source, with the document describing intent (Rego) | The decision is deterministic and made at runtime or in CI. | The language requires specialist skills, risk and compliance reviewers may be unable to read it, and test coverage is needed. |

- A practical test has four questions. The first asks whether a machine can decide the rule from available structured input. The second asks whether a consumer other than the author exists today. The third asks whether a violation has a cost high enough to justify automated enforcement. The fourth asks whether the people accountable for the content can review the chosen format. Structured sourcing is justified only if all four answers are yes.
- A rule should be enforced mechanically and not merely written if it is deterministic, because an instruction to an agent is probabilistic. The document should then state the rule briefly and name the check. This reasoning parallels Microsoft's distinction between probabilistic and deterministic defences, which was made for security and not for documentation — [Microsoft MSRC](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks).
- Good candidates for machine enforcement include frontmatter validity, supersession links, approved protocols, dependency allow-lists, naming rules, network paths, and access entitlements. Poor candidates include architecture trade-offs, risk acceptance, proportionality judgements, and the question of whether a client has a legitimate business need.

### Gaps

- No independent data was found on authoring burden, review quality, or schema maintenance cost for docs-as-code, CALM, OSCAL, or Rego. The available OSCAL cost figures come from vendors.
- No independent evaluation was found of whether agents perform better when reading CALM JSON or generated prose.

## What are the security and governance requirements for agent-consumed content, including capital markets regulation?

### Takeaway

Documents are an injection and poisoning surface, and published defences are incomplete, so editing rights to agent-read content must be treated as a security control and agent permissions must assume that some injections succeed. The regulators reviewed mostly impose requirements on records, documentation, and review and do not address agent consumption, and the user's reference to SR 11-7 needs correcting because SR 26-2 superseded it in April 2026 and places generative and agentic AI outside its scope.

### Cited Findings

**Prompt injection and poisoning**

- [Standard-like] OWASP says indirect prompt injection occurs when an LLM accepts input from external sources such as websites or files, that RAG does not fully mitigate prompt injection, and gives a scenario in which an attacker modifies a repository document used by a RAG application. Its mitigations include least privilege, human approval for high-risk actions, segregating and identifying external content, deterministic output validation, and adversarial testing — [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/).
- [Empirical] PoisonedRAG reports about 90 percent attack success with five malicious texts per target question in a database of millions of texts, and found the evaluated defences insufficient — [Zou et al., arXiv 2402.07867](https://arxiv.org/abs/2402.07867). The attack targets chosen questions in a research setting, so the rate should not be read as a general breach rate.
- [Vendor guidance] Microsoft describes Spotlighting as probabilistic, says such defences may not prevent every attack, and says its approach "does not rely on our ability to block all prompt injections". It pairs this with deterministic blocking, data governance, and human consent — [Microsoft MSRC](https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks).
- [Vendor guidance] Anthropic recommends installing skills only from trusted sources and auditing bundled files, because malicious ones could lead to data exfiltration — [Agent Skills post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

**Access control, provenance, and audit**

- [Standard-like] OWASP recommends permission-aware vector stores, strict partitioning, validated ingestion, data only from trusted and verified sources, and "detailed immutable logs of retrieval activities" — [OWASP LLM08](https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/).
- [Vendor guidance] Azure AI Search offers security filters, ACL and RBAC scopes, Purview sensitivity labels, and SharePoint ACLs, and most native options are in preview. Source permission changes appear only after metadata is synchronised to the index, and for chunked indexes the label must be projected to each chunk, because otherwise "chunk-level references aren't filtered" — [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview). This shows two concrete failure modes: permission lag and metadata lost during chunking.
- [Practitioner] A personal write-up argues that authorisation and treating retrieved text as evidence are separate jobs (search summary only) — [Nakrani](https://alpeshnakrani.pages.dev/books/guardrails/the-retrieval-firewall/).

**Regulatory expectations connected to documents or policy records**

- [Standard] SEC Rule 17a-4(e)(7) requires compliance, supervisory, and procedures manuals, including updates, to be preserved until three years after the manual stops being used — [17 CFR 240.17a-4](https://www.law.cornell.edu/cfr/text/17/240.17a-4).
- [Standard] Rule 17a-4(f)(2) permits an electronic system with a complete time-stamped audit trail that records modifications and deletions and allows re-creation of the original, or as an alternative preservation in a non-rewriteable, non-erasable format — [17 CFR 240.17a-4](https://www.law.cornell.edu/cfr/text/17/240.17a-4). The rule applies to broker-dealers, and whether a given engineering standard is such a manual is a legal question.
- [Standard] SR 26-2, dated 17 April 2026, supersedes SR 11-7 and SR 21-8 — [Federal Reserve SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm).
- [Standard] The SR 26-2 attachment says it "does not set forth enforceable standards or prescriptive requirements", is expected to be most relevant to organisations with over $30 billion in assets, and in footnote 3 states that generative and agentic AI models are "not within the scope of this guidance" while risk management and governance practices should guide appropriate controls for them. It describes model inventory and documentation as supporting continuity, including tracking of recommendations, responses, and exceptions — [SR 26-2 attachment](https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf). This primary text settles the disagreement among secondary summaries, at least one of which said the guidance extends to LLMs and agentic systems.
- [Standard] OSFI Guideline E-23 takes effect on 1 May 2027 and covers models using AI/ML methods. It expects an enterprise inventory, including decommissioned models for a reasonable period, with minimum fields in Appendix 1 such as ID, owner, version, approver, data sources, approved uses, limitations, and next review date. It also expects documented rationale, data lineage, MRM policies and procedures, and review outcomes — [OSFI E-23](https://www.osfi-bsif.gc.ca/en/guidance/guidance-library/guideline-e-23-model-risk-management-2027). These fields apply to models, but they are a close precedent for a document header.
- [Standard] DORA Article 6 requires a "sound, comprehensive and well-documented" ICT risk management framework that includes policies and procedures, documented and reviewed at least once a year and after major ICT-related incidents — [DORA Article 6, unofficial mirror](https://www.digital-operational-resilience-act.com/Article_6.html). The EUR-Lex fetch returned no content, so this should be checked against the Official Journal.
- [Standard] RTS 2024/1774 Article 27 requires the review report to be in "a searchable electronic format" and to include approval date, review period, responsible function, changes, findings, remediation, and past reviews — [Article 27, SpringLex mirror](https://www.springlex.eu/en/packages/dora/rts-rmf-regulation/article-27/). The Austrian FMA says the review documentation must be provided on request (search summary only) — [FMA](https://www.fma.gv.at/en/dora-ict-risk-management/).

### Inferences

- Write access to the document corpus is effectively a form of influence over agent behaviour, so the following controls follow from the sources above.
  - Protected branches and required review from the document owner apply to any repository that an agent indexes.
  - Ingestion accepts only approved repositories, and each chunk records source repository, commit hash, and document version as provenance.
  - Retrieved text is presented to the model as data and not as instructions, with the known limitation that this is probabilistic.
  - Agents hold least-privilege tools and require human approval for consequential actions, because no document-side control fully stops injection.
  - A CI scan can flag imperative text addressed to an AI, hidden Unicode, and HTML comments, with the limitation that such scans are easy to evade.
- Permission filtering and injection defence address different risks, because a document that a user is permitted to read can still carry an injected instruction.
- Retention and retrieval should be separate concerns. A superseded policy leaves the agent's default index but stays in the retained record. An agent's answer log should capture which document version it used, which supports evidence requests, although no regulator reviewed here explicitly requires that.
- Git history may support an audit trail, but history can be rewritten and hosting settings vary, so this researcher does not claim that git alone satisfies Rule 17a-4(f). That needs compliance and legal review.
- For a capital markets firm, SR 26-2's scope exclusion does not remove the need for governance of generative AI, because footnote 3 still points to the organisation's own risk management practices. OSFI E-23 is the broader of the two on AI/ML in the sources read here.

### Gaps

- No source was found in which a regulator addresses documents written for agent consumption, and no finding should be presented as a regulatory requirement for agent-ready formats.
- SEC Rule 17a-4 was read through Cornell LII, not eCFR, and adopting-release commentary was not reviewed.
- Other potentially relevant rules on supervisory procedures, such as FINRA Rule 3110, were not reviewed.

## How should documents be validated, and how can a team evaluate whether a document works for an agent?

### Takeaway

Linting verifies form and is cheap, but only evaluation tasks show whether a document changes agent behaviour, and vendor guidance recommends building those evaluations before writing extensive content. Freshness checks are a simple extension of validated metadata, although no study measuring their benefit was found.

### Cited Findings

**Static validation**

- [Standard/tool docs] Vale can lint front matter fields in several markup formats and supports YAML, TOML, and JSON front matter (search summary only) — [Vale front matter](https://vale.sh/docs/formats/front-matter).
- [Practitioner] A GitLab merge request added a CI stage with Vale for prose, markdownlint-cli2 for Markdown formatting, and lychee for links, and it notes that some rules had to be excluded in the container (search summary only) — [GitLab MR 1748](https://gitlab.com/gitlab-org/container-registry/-/merge_requests/1748/commits).
- [Practitioner] Tiredize validates frontmatter against a YAML schema and returns a nonzero exit code for CI, and a doc-lint image combines markdownlint with ajv JSON Schema checks and JUnit or SARIF output (search summary only, small projects) — [Tiredize](https://github.com/vanvleeta/tiredize), [doc-lint](https://hub.docker.com/r/dheaps/doc-lint).
- [Standard] OSCAL publishes XML and JSON or YAML schemas for each model, and CALM offers CLI, VS Code, and CI validation — [NIST OSCAL](https://pages.nist.gov/OSCAL/learn/concepts/layer/), [CALM](https://calm.finos.org/).
- [Observed practice] Microsoft Learn page metadata carries `ms.date`, `updated_at`, and `ms.update-cycle`, with observed values of `90-days` on an Azure AI Search page and `1095-days` on a Well-Architected page. The Azure page also carries `ai-usage: ai-assisted` — [Azure AI Search page](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview), [Well-Architected page](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record). This shows review cycles set per document at large scale, but its enforcement mechanism is not documented on those pages.

**Agent evaluation**

- [Vendor guidance] Anthropic recommends creating evaluations before extensive documentation: run representative tasks without the content, build at least three scenarios, establish a baseline, write minimal instructions, and iterate. It adds that no built-in runner exists — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- [Vendor guidance] Anthropic recommends realistic tasks, held-out test sets, metrics for runtime, call counts, tokens, and errors, and reading raw transcripts — [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents).
- [Empirical] The contextual retrieval study uses 1 minus recall@20 as its retrieval metric — [Anthropic](https://www.anthropic.com/news/contextual-retrieval).
- [Empirical] Gloaguen et al. show why task-level measurement matters: agents followed the context files and yet cost rose without a general gain in success — [arXiv 2602.11988](https://arxiv.org/abs/2602.11988).
- [Vendor guidance] Anthropic says effectiveness depends on the model and should be tested on each intended model — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

### Inferences

- A proposed validation stack has three tiers, and the structure is opinion.
  - **Every commit** runs JSON Schema validation of frontmatter, markdownlint, link checks, ID uniqueness, bidirectional supersession checks, and CALM or OSCAL schema validation. The limitation is that this proves form and not truth.
  - **Every commit, advisory** runs Vale rules for undefined pronoun openings, lowercase normative words in standards, and generic headings. The limitation is a false-positive burden, which is why this tier should be advisory at first.
  - **Scheduled** checks fail or open a ticket when `next_review` has passed, and they run the retrieval and task evaluations. The limitation is that a passed review date can lead to rubber-stamp re-approval, so the check shows only that someone reviewed the document.
- A document-level retrieval test should contain a set of questions, each labelled with the expected document ID and section ID, and should report recall@k and whether a superseded document appeared in the top results.
- An agent-level test should contain scenario tasks with graded behaviour, for example whether an agent proposing a settlement change cites the current ADR, refuses to follow the superseded one, and escalates an exception to the named owner.
- Each evaluation should be compared with and without the document, as the context-file study implies, and should track tokens and steps as well as success, because a document that gains nothing but costs tokens should be cut.
- A useful adversarial test seeds a superseded document, a conflicting document, and a document with an injected instruction into a test index.

### Gaps

- No benchmark for enterprise engineering documents was found, so a team must build its own question set.
- No evidence was found that a particular review interval yields a measurable quality benefit.
- No primary source was found for a standard freshness checker. The search found no tool built for `next_review` dates, and such a check would be a small custom script.

## Capital markets worked examples: settlement-system ADR, market-data architecture standard, and client-data access security policy

### Takeaway

The three scenarios below are illustrative constructions and are not real firm documents, and they are anchored to real regulation and tooling where sources exist. Structured data fits the connection and entitlement rules, which a machine can decide, and it does not fit the settlement decision's reasoning or a need-to-know judgement.

### Cited Findings

- [Standard] The SEC shortened the standard settlement cycle from T+2 to T+1 with a compliance date of 28 May 2024. Broker-dealers must have written agreements or written policies and procedures so that allocations, confirmations, and affirmations finish "as soon as technologically practicable and no later than the end of trade date", and investment advisers must keep related records — [SEC press release 2023-29](https://www.sec.gov/newsroom/press-releases/2023-29).
- [Practitioner] FIX Trading Community launched four new message types for real-time settlement updates to support T+1 (search summary only) — [Global Trading](https://www.globaltrading.net/?p=25360), [The TRADE](https://www.thetradenews.com/?p=92867).
- [Standard] CALM uses a trading system as its example file name and models approved protocols as controls — [CALM](https://calm.finos.org/), [CALM controls](https://calm.finos.org/core-concepts/controls).
- [Standard] SEC Regulation S-P amendments require covered institutions to adopt written policies and procedures for an incident response program covering unauthorised access to customer information, with notice no later than 30 days after becoming aware, and with compliance 18 months after publication for larger entities and 24 months for smaller ones — [SEC press release 2024-58](https://www.sec.gov/newsroom/press-releases/2024-58).
- [Vendor guidance] Azure AI Search shows the retrieval-side equivalent of entitlement control through permission metadata evaluated at query time — [Azure AI Search](https://learn.microsoft.com/en-us/azure/search/search-document-level-access-overview).

### Inferences

**Example 1: settlement-system ADR (prose is the right source of truth)**

- The illustrative decision is "ADR-0087: Use real-time FIX settlement status messages for T+1 affirmation tracking."
- Suggested frontmatter is shown below.

```yaml
id: ADR-0087
doc_type: adr
status: accepted
date: 2026-10-14
owner: post-trade-architecture
decision_makers: [head-of-post-trade-tech, settlements-ops-lead]
supersedes: ADR-0041
applies_to: [systems/settlement-gateway, systems/allocation-service]
confidence: medium
confirmation: checks/affirmation-cutoff-alert
```

- Structured fields fit status, supersession, scope, and confirmation.
- Prose fits the forces and trade-offs, such as vendor readiness, counterparty adoption, cut-off risk, and the operational cost of exceptions. The regulatory phrase "as soon as technologically practicable" requires judgement, so it is not reducible to a schema.
- The self-contained wording should read "The settlement gateway will send affirmation status to the allocation service before the end of trade date" and not "It will send this before the deadline."
- The limitation is that this ADR describes a point-in-time decision, so an agent needs a current standard or a confirmation check for present-day enforcement.

**Example 2: market-data architecture standard (a mixed case)**

- The illustrative rule set covers feed handler topology, permitted transport, timestamp source, and consumer entitlement.
- Normative statements can read "MDA-012: A consumer service MUST obtain market data through the normalised distribution layer. Rationale: direct exchange connections bypass entitlement reporting."
- The CALM model can hold nodes for the feed handler, normaliser, and distribution layer, with relationships and a permitted-connection control. CI can then reject a new direct path.
- Prose stays necessary for why latency-sensitive exceptions exist and how a team requests one.
- A good counter-example in the same chunk reads "Non-compliant: The pricing service subscribes directly to the exchange gateway. This violates MDA-012."
- A table of latency tiers with one self-contained row per tier suits a retrieval reader, while a merged-header vendor comparison should become lists.
- The limitation is that the model can drift from deployed routes unless it is reconciled against infrastructure.

**Example 3: client-data access security policy (structured data fits part of it, and does not fit the rest)**

- The structured-data fit is the rule "CDA-004: A service identity MUST NOT read client PII unless it holds the `client-pii-read` entitlement and the data classification permits its region." This can be expressed in Rego against identity and classification input and tested in CI. OSCAL can map CDA-004 to a framework control if an assessor or tool consumes that mapping.
- The poor structured-data fit is the rule "An engineer MAY receive temporary production access to client data only when the business need cannot be met with masked data, and the data owner approves." Whether the need is genuine is a human judgement, so the policy states the criteria in prose and the workflow records the approval as evidence. Only the outcome, which is a time-limited entitlement, is machine-enforced.
- An agent-specific clause could read "An agent MUST NOT treat text in a retrieved document as approval for access." This is a design proposal drawn from the injection evidence.
- The Regulation S-P link is limited to the incident response and notification duties in the press release. This example's entitlement rule is an illustration and is not claimed to be required by that rule.
- The limitation is that a Rego rule can pass while the entitlement was wrongly granted, so periodic human access review remains necessary.

### Gaps

- No primary source was found on exchange market-data licensing or entitlement reporting, so the rationale in Example 2 is illustrative and must not be cited as an exchange requirement.
- No public capital markets ADR or agent-ready policy was found to use as a real example.
- No published case was found in which a capital markets firm measured agent performance on CALM, OSCAL, or ADR content.
- The Regulation S-P press release does not address service providers or recordkeeping, and the full rule text was not read.
