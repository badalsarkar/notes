# Context Management for AI-DLC

Research report, October 2026. Related notes: [ai-dlc.md](ai-dlc.md),
[sdlc-context-graph.md](sdlc-context-graph.md), [agentic-ai.md](agentic-ai.md),
[ai-security.md](ai-security.md), [specification-driven-development.md](specification-driven-development.md).

## Contents

- [1. What this report covers](#1-what-this-report-covers)
- [2. Summary](#2-summary)
- [3. The kinds of context in an AI-DLC workflow](#3-the-kinds-of-context-in-an-ai-dlc-workflow)
- [4. How AI-DLC manages context today](#4-how-ai-dlc-manages-context-today)
- [5. Industry patterns](#5-industry-patterns)
- [6. Side-by-side comparison](#6-side-by-side-comparison)
- [7. What the evidence shows](#7-what-the-evidence-shows)
- [8. Lessons reported by teams that built these systems](#8-lessons-reported-by-teams-that-built-these-systems)
- [9. A reference design for an AI-DLC context management system](#9-a-reference-design-for-an-ai-dlc-context-management-system)
- [10. Capital markets scenarios](#10-capital-markets-scenarios)
- [11. Build order](#11-build-order)
- [12. Failure modes to watch for](#12-failure-modes-to-watch-for)
- [13. Open questions](#13-open-questions)
- [Resources](#resources)

## 1. What this report covers

- AI-DLC moves the drafting of requirements, designs, code and tests to agents, and every one of
  those agents works only from what is in its context window at the moment it acts.
    - The quality of the output therefore depends on which rules, knowledge, prior decisions and
      workflow state reach the agent, and on whether that material is current.
    - Context management is the system that decides what is stored, where it is stored, who may
      change it, how it is retrieved for a given stage, and how it survives the end of a session.
- This report describes the categories of context an AI-DLC workflow produces and consumes, how
  the AWS AI-DLC implementation handles them as of version 2 in October 2026, the patterns other
  organisations use, the published evidence for each, and a reference design for building one.
- It does not repeat the retrieval techniques covered in [agentic-ai.md](agentic-ai.md), such as
  vector search, hybrid search and GraphRAG, or the context graph material in
  [sdlc-context-graph.md](sdlc-context-graph.md). Those notes describe how to query a knowledge
  store, and this note describes the system around the stores.

## 2. Summary

- The industry has converged on a layered model in which a small amount of context is always
  loaded, a larger amount is loaded when a condition matches, and most of it is retrieved by the
  agent on demand.
    - Anthropic, Kiro, Cursor, Claude Code, the Agent Skills standard and the Codified Context
      paper all use some version of this, under different names.
    - The reason is that model accuracy degrades as input length grows, even on simple tasks, so
      loading everything that might be relevant makes the agent worse as well as more expensive.
- Workflow state must live outside the conversation, in files or a database that the harness
  treats as authoritative.
    - AI-DLC already does this with its state file and audit trail, and Anthropic's published
      harness for long-running agents does the same with a progress file and a JSON feature list.
    - The open AI-DLC issues show that the remaining problems are at the boundary between the
      conversation and the stored state, particularly after compaction, where a summary of the
      conversation can disagree with the state file and nothing reconciles the two.
- The evidence for always-loaded instruction files such as `AGENTS.md` is mixed.
    - A February 2026 study found that LLM-generated context files slightly reduced task success
      and raised inference cost by more than 20%, while developer-written files raised success by
      about four points on average.
    - A separate study found that `AGENTS.md` files reduced runtime and output tokens by about 20%
      to 29%, but it did not measure correctness.
    - The consistent recommendation is to keep these files short and limited to requirements the
      agent cannot discover for itself.
- Memory that agents write for themselves works when each entry carries a pointer to its evidence
  and is checked against that evidence before use.
    - GitHub's Copilot memory stores code citations with every memory and validates them at read
      time, and reports a merge rate of 90% with memory against 83% without it.
    - The alternative, an offline curation pipeline that deduplicates and expires memories, was
      rejected by GitHub as too expensive to run at its scale.
- Staleness is the main failure mode in every published account. The systems that hold up either
  derive their context from sources that are already maintained, or attach a freshness check to
  each item and refuse to serve items that fail it.
- For an organisation implementing context management around AI-DLC, the practical design is a
  small number of separate stores with different owners and lifetimes, a per-stage context
  manifest with an explicit token budget, a governed write path for anything that becomes a rule,
  and a resume protocol that treats stored state as authoritative and the conversation as a cache.

## 3. The kinds of context in an AI-DLC workflow

- Treating context as one undifferentiated pool is the most common design error, because the
  categories differ in who owns them, how often they change, how long they remain valid and how
  much damage a stale copy causes.
- The table below separates them. The terms used in the rest of this report refer to these rows.

| Category | Examples | Owner | Changes | Lifetime | Cost of a stale copy |
|---|---|---|---|---|---|
| Organisational rules | Approved libraries, security standards, logging policy | Architecture, security | Quarterly | Years | High, because it is applied everywhere |
| Domain knowledge | Settlement cycles, mandate precedence, product definitions | Business, domain experts | Monthly | Years | High, and hard to detect |
| Code knowledge | Component inventory, call graph, architecture notes | Derived from source | Every commit | Until the next commit | Medium, and detectable mechanically |
| Workflow state | Current intent, stage, pending approvals, unit progress | The engine | Every step | One intent | Very high, because it controls gates |
| Decisions and rationale | ADRs, design trade-offs, approvals, rejected options | The team | Per stage | Years | High for audit |
| Working context | Current conversation, tool outputs, scratch notes | The agent | Every turn | One session | Low if the session ends cleanly |
| Learnings | Corrections the agent should not repeat | The team, proposed by the agent | Ad hoc | Until contradicted | Medium |
| External system data | Tickets, incidents, deploys, ownership | Source systems | Continuously | Varies | Low if read live, high if copied |

- Two observations follow from the table.
    - Workflow state and decisions are produced by the method itself, while rules, domain
      knowledge and code knowledge exist before the method runs and outlive any single intent.
      [sdlc-context-graph.md](sdlc-context-graph.md) section 4.2 makes the same distinction
      between the traceability graph and the knowledge graph.
    - The categories that change most often should be derived or read live rather than authored,
      and the categories that change least often are the ones that justify human review on write.

## 4. How AI-DLC manages context today

### 4.1 Directory layout

- AI-DLC version 2 stores all of its context as files under an `aidlc/` directory at the
  workspace root, committed to git
  ([Spaces and Intents](https://awslabs.github.io/aidlc-workflows/guide/03-spaces-and-intents/)).
    - A **space** is one team's set of intents, rules and knowledge. Most users have a single
      `default` space, and separate spaces exist for the case where several teams share one
      project.
    - `aidlc/spaces/<space>/memory/` holds the rules: `org.md`, `team.md`, `project.md` and a
      `phases/` folder with one file per phase.
    - `aidlc/spaces/<space>/knowledge/` holds team domain knowledge as free-form Markdown, plus a
      DocumentKB catalogue for documents the team owns.
    - `aidlc/spaces/<space>/codekb/<repo>/` holds architecture notes, a component inventory and a
      freshness marker for each repository, produced by a scan and reused across intents.
    - `aidlc/spaces/<space>/intents/<YYMMDD>-<label>/` is the record directory for one intent,
      holding `aidlc-state.md`, an `audit/` folder and the generated artifacts.
- Methodology knowledge shipped with the framework lives separately in the harness folder, for
  example `.claude/knowledge/`, and is overwritten on upgrade. The documentation tells teams not to
  edit it ([Knowledge](https://awslabs.github.io/aidlc-workflows/guide/08-knowledge/)).
- Multiple repositories are handled by placing them as sibling folders beside `aidlc/`, so that one
  intent record covers work that spans several repositories.

### 4.2 How context is loaded

- Knowledge is loaded per agent at the start of each stage, in a fixed order: space rules, shared
  methodology, agent methodology, team shared knowledge, team agent knowledge, and then the
  artifacts produced by earlier stages.
    - Loading is by directory convention rather than by search. The loader walks directories named
      after each agent, so a misspelled directory is skipped without any warning.
    - There is no size limit and no retrieval index for team knowledge. The documentation
      recommends small single-topic files and a quarterly pruning review.
    - The audit trail records which agent started a stage but not which knowledge files it read,
      so the documented way to verify loading is to ask the agent at a gate.
- Rules resolve in the order org, team, project, phase, stage. The set of files that apply is
  compiled once per workflow and their text is re-read before every stage
  ([Rules and the Learning Loop](https://awslabs.github.io/aidlc-workflows/guide/09-rules-and-the-learning-loop/)).
- Rules are additive. Nothing overrides anything else at runtime, and conflicts are handled by an
  LLM check against `org.md` when a new learning is written, which the documentation describes as
  an audit aid rather than an enforcement boundary.

### 4.3 State and audit

- Each intent has an `aidlc-state.md` file that acts as a durable cursor: project information,
  scope configuration, phase and stage progress, runtime state and a session resume point
  ([State Tracking and Audit Trail](https://awslabs.github.io/aidlc-workflows/guide/10-state-and-audit/)).
- The audit trail is a folder of per-clone Markdown shards recording events from a taxonomy of
  126 event types, such as `STAGE_STARTED`, `GATE_APPROVED` and `SESSION_COMPACTED`.
    - Sharding by clone means concurrent writers do not produce merge conflicts, and events whose
      order across writers is unknown are marked as unordered.
    - The state file can be rebuilt from the stage start and completion events if it is
      corrupted, so the audit trail is the more authoritative of the two.
- On every session start the engine reads the state file to find what is complete and what comes
  next, and after compaction the agent's persona is reloaded from its agent file
  ([Session Management](https://awslabs.github.io/aidlc-workflows/guide/11-session-management/)).

### 4.4 The learning loop

- While a stage runs, the orchestrator keeps a per-stage diary of interpretations, deviations,
  trade-offs and open questions.
- When the user corrects the agent, the loop asks once whether to keep the correction for the
  project or for the team. One-off fixes such as a typo are not asked about.
- A kept learning is written to `project.md` or `team.md` and recorded as a `RULE_LEARNED` audit
  event with a content hash and source. There is deliberately no path from the learning loop to
  `org.md`, so organisational rules can only change through a separate process.
- Six deterministic sensors (`claim-sources`, `required-sections`, `upstream-coverage`,
  `traceability`, `linter` and `type-check`) run on writes and at gates. They are advisory unless
  configured as blocking.

### 4.5 Where the current design is under strain

- The open issues in the [aidlc-workflows repository](https://github.com/awslabs/aidlc-workflows/issues)
  show where file-based context management meets its limits in practice. All of the following were
  open in October 2026.
    - [#249](https://github.com/awslabs/aidlc-workflows/issues/249): after a session was cleared,
      a new session read a stage marked `COMPLETED` in the state file and moved past an approval
      gate that had not been passed, because the state did not distinguish an artifact that had
      been generated from one that had been approved.
    - [#2492](https://github.com/awslabs/aidlc-workflows/issues/2492): after Codex compacted its
      context, the recovery summary implied that later units had been completed while the state
      file still pointed to an earlier stage. Nothing detected the disagreement. The proposed fix
      is to carry a state revision or digest in the recovery summary and reconcile on resume.
    - [#2454](https://github.com/awslabs/aidlc-workflows/issues/2454): one run on GitHub Copilot
      recorded 99 compaction events in about 28 hours. After each one the model lost the CLI
      contract and issued malformed commands, while the compaction event still reported the state
      as valid.
    - [#421](https://github.com/awslabs/aidlc-workflows/issues/421): 30 of 32 stages run inline in
      the main agent's context, so the early phases fill the window and force repeated manual
      compaction. The proposal is for the main agent to track state only and for each stage to
      run in a subagent.
    - [#1330](https://github.com/awslabs/aidlc-workflows/issues/1330): a customer reported that
      version 2 uses materially more tokens than version 1 for equivalent output.
    - [#423](https://github.com/awslabs/aidlc-workflows/issues/423): when units of work are built
      in parallel by different people or sessions, their context drifts from the assumptions
      agreed during Inception. The issue notes that the audit log is a chronological record
      rather than a structured decision record that other units can consume.
    - [#1335](https://github.com/awslabs/aidlc-workflows/issues/1335): version 2 assumes local
      tooling per developer, and one customer scaling to thousands of developers built a hosted
      platform to get shared projects, identity and central governance.
- Taken together, these issues show that the storage model is sound and the problems are in
  three places: the handover between conversational memory and stored state, the size of what is
  loaded inline, and the absence of a shared, multi-user context store.

## 5. Industry patterns

Each pattern below is described with the same structure: how it works, where it is used, its
strengths and weaknesses, its cost, and an example of where it fits and where it does not.

### 5.1 Always-loaded instruction files

- **How it works.** A Markdown file at a known path is inserted into every session's context.
  Examples are `AGENTS.md`, `CLAUDE.md`, Kiro's foundation steering files (`product.md`,
  `tech.md`, `structure.md`) and Spec Kit's `.specify/memory/constitution.md`.
- **Who uses it.** Almost every coding agent supports it, and `AGENTS.md` is read by Codex,
  Cursor, Kiro, Copilot and others. AI-DLC's `memory/` rules are a variant of this pattern.
- **Strengths.** It is simple, portable across harnesses, versioned with the code and reviewable
  in a pull request. A short file costs little once it is in the prompt cache.
- **Weaknesses.** Every token is paid on every turn whether it is relevant or not. Agents follow
  the instructions closely, so an unnecessary requirement becomes unnecessary work. The study
  described in section 7.1 found that codebase overviews in these files did not help agents find
  relevant files sooner.
- **Cost.** Low to author, and moderate to keep accurate, since nothing detects when the file
  disagrees with the code.
- **Fits.** A rule that applies to every change and that the agent cannot discover for itself,
  such as "all monetary amounts use the `Money` type with an explicit currency" in a trade
  booking service.
- **Does not fit.** A description of the settlement reconciliation module's architecture, which
  is relevant to a small fraction of tasks and goes stale with each refactor.

### 5.2 Scoped and conditional rules

- **How it works.** Rules carry metadata that says when to load them.
    - Kiro steering supports four inclusion modes in YAML front matter: `always`, `fileMatch` with
      a glob, `manual` on explicit reference, and `auto` when the request matches a description
      ([Kiro steering](https://kiro.dev/docs/steering/)).
    - Cursor project rules have equivalent types: always applied, attached by glob, requested by
      the agent from a description, and manual.
    - Claude Code supports nested `CLAUDE.md` files that load when the agent works in that
      directory, and rule files scoped by path.
    - AI-DLC scopes rules by phase and stage rather than by file path.
- **Strengths.** Context is proportional to the work being done. Ownership can follow the
  scope, so the team that owns the risk engine owns the rules attached to its paths.
- **Weaknesses.** Glob scoping misses changes that matter to a module without touching its files,
  such as a change to a shared schema. Description-based loading depends on the model choosing
  correctly, and a rule that is not loaded fails silently.
- **Cost.** Low, but the number of rule files grows and needs an owner and a review cycle.
- **Fits.** Rules for the FIX gateway that should load whenever files under `gateway/fix/` change.
- **Does not fit.** A regulatory rule, such as a best-execution record-keeping requirement, that
  must apply to any change touching order routing regardless of which files it lives in. That
  belongs in an always-loaded rule or a deterministic check.

### 5.3 Progressive disclosure through skills

- **How it works.** The Agent Skills format, published by Anthropic as an open standard in
  December 2025, packages instructions as a folder with a `SKILL.md` file. Only the name and
  description, on the order of 100 tokens per skill, load at startup. The body loads when a task
  matches the description, and bundled reference files and scripts load only when the body points
  to them.
- **Who uses it.** Claude Code, Codex, Copilot, Cursor, Gemini CLI and a growing number of other
  harnesses. AI-DLC version 2 itself ships as skills and runner commands.
- **Strengths.** A large library of procedures costs almost nothing until one is needed. Scripts
  let deterministic work, such as validating a schema, run outside the model.
- **Weaknesses.** Activation depends on the quality of the description, and there is limited
  tooling to show which skills were loaded for a given task. Skills suit procedures better than
  facts, because facts change and a skill has no freshness mechanism.
- **Cost.** Low per skill. The governance cost is in curating a shared library so that two
  skills do not give conflicting instructions.
- **Fits.** A procedure for adding a new counterparty reference data field, which touches the
  schema, the static data loader, the reconciliation mapping and the tests in a fixed order.
- **Does not fit.** The current list of restricted securities, which changes daily and must come
  from the system of record.

### 5.4 Just-in-time retrieval by the agent

- **How it works.** The agent holds lightweight references, such as file paths, document
  identifiers or tool names, and uses tools to read the content when it needs it. Anthropic's
  guidance describes Claude Code loading `CLAUDE.md` up front and then using glob and grep for
  everything else, and calls this a hybrid strategy
  ([Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- **Who uses it.** Claude Code, Codex and most coding agents for source code. The Codified
  Context paper extends it to specification documents through an MCP server with five tools,
  including `find_relevant_context(task)` and `suggest_agent(task)`, backed by keyword matching
  ([Vasilopoulos, 2026](https://arxiv.org/abs/2602.20478)).
- **Strengths.** The agent reads the current version of the source, so code knowledge cannot be
  stale. The window holds only what the agent chose to read.
- **Weaknesses.** It is slower than pre-loaded context and spends tokens on exploration. The
  agent has to know that something exists before it can look for it, so undocumented subsystems
  stay invisible. Case study 3 in the Codified Context paper found one only because a search
  returned nothing.
- **Cost.** Low for code, since search tools already exist. Higher for documents, which need an
  index and an MCP server.
- **Fits.** Finding every caller of the trade enrichment function before changing its signature.
- **Does not fit.** Applying a firm-wide rule the agent does not know exists. Retrieval can only
  answer questions the agent thinks to ask.

### 5.5 Durable workflow state outside the conversation

- **How it works.** The harness writes progress, decisions and next steps to files or a database
  and reads them at the start of each session, so a new session can resume without the previous
  conversation.
    - Anthropic's long-running agent harness uses an initialiser session that creates an `init.sh`
      script, a `claude-progress.txt` log and a JSON feature list with a `passes` field per
      feature. Every later session reads the git log and the progress file before choosing work
      ([Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
    - Anthropic chose JSON for the feature list because the model was less likely to overwrite or
      edit it inappropriately than a Markdown file.
    - Manus rewrites a `todo.md` file throughout a task so that the objectives appear at the end of
      the context, which keeps the agent on goal across roughly 50 tool calls
      ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
    - AI-DLC uses `aidlc-state.md` and the audit trail, described in section 4.3.
- **Strengths.** Progress survives session loss, compaction and a change of harness. Git gives
  history and rollback at no extra cost.
- **Weaknesses.** Free-text state is interpreted by the model, which is how issue #249 arose.
  Two copies of the state, one in the file and one in a conversation summary, can diverge, which
  is issue #2492.
- **Cost.** Low to build. The real cost is defining the state precisely enough that it cannot be
  misread, which means a schema rather than prose for anything that controls a gate.
- **Fits.** Tracking which units of a multi-week settlement platform migration have passed review.
- **Does not fit.** Storing reasoning or domain knowledge. State files should record where the
  work is, and knowledge belongs in its own store.

### 5.6 Compaction and structured summarisation

- **How it works.** When the window approaches its limit, earlier conversation is summarised and
  the session continues with the summary.
    - The lightest form is clearing old tool results, which Anthropic describes as the safest
      first step.
    - Factory compared three approaches on real coding sessions and scored its own anchored
      iterative summarisation at 3.70, Anthropic's SDK compression at 3.44 and OpenAI's compact
      endpoint at 3.35 on probe questions about files, decisions and next steps
      ([Factory](https://factory.ai/news/evaluating-compression)). Factory keeps a sectioned
      summary of intent, file changes, decisions and next steps, and merges only the newly
      truncated span into it, rather than regenerating the whole summary each time. These are a
      vendor's results on its own method.
- **Strengths.** It extends a session without human intervention and keeps the reasoning that led
  to the current point.
- **Weaknesses.** Summaries lose detail, and repeated summaries drift. Compaction can drop the
  instructions that tell the agent how to operate the workflow, as issue #2454 shows.
- **Cost.** Moderate, since each compaction is a model call, and a cache miss on the next turn.
- **Fits.** A long debugging session on an intraday margin calculation where the history of
  failed hypotheses is still useful.
- **Does not fit.** Carrying workflow state. State should be re-read from the authoritative store
  after compaction, and the summary should only carry what is not stored anywhere else.

### 5.7 Context isolation with subagents

- **How it works.** A lead agent delegates a focused task to a subagent with a clean context, and
  the subagent returns a condensed result. Anthropic describes this as a way to keep the lead's
  context small.
- **Who uses it.** Claude Code, Anthropic's research system, and AI-DLC for reverse engineering
  and code generation. Issue #421 proposes extending it to every stage.
- **Strengths.** The lead's context grows with the number of tasks rather than with the full
  transcript of each task. Exploration can run in parallel.
- **Weaknesses.** The subagent does not see the decisions the lead has made, and Cognition's
  [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) argues that actions
  carry implicit decisions and that parallel agents working from partial context make conflicting
  ones. Anthropic reported that its multi-agent research system used about 15 times the tokens of
  a chat interaction.
- **Cost.** High in tokens, offset by fewer compactions and shorter wall-clock time.
- **Fits.** Reading through three years of incident reports for the clearing interface and
  returning the five failure patterns that matter for a redesign.
- **Does not fit.** Two subagents independently designing the two ends of a message contract
  between the order management system and the allocation service. The decision has to be made
  once and passed to both.

### 5.8 Agent-written memory with verification

- **How it works.** The agent stores facts it has learned during a task, and a later session
  retrieves and uses them.
    - GitHub's Copilot memory stores a subject, a fact, citations to specific code locations and a
      reason. At the start of a session the most recent memories for the repository are included,
      and before using one the agent reads the cited locations to confirm the fact still holds. A
      memory that fails validation is corrected or discarded, and unused memories expire after 28
      days ([GitHub engineering blog](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/),
      [Copilot Memory docs](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)).
    - The ACE paper from Stanford, SambaNova and Berkeley maintains an evolving playbook that a
      reflector and a curator update with small incremental edits rather than full rewrites,
      because full rewrites lose detail over time, which the authors call context collapse
      ([Zhang et al., 2025](https://arxiv.org/abs/2510.04618)).
    - AI-DLC's learning loop is a governed version of this pattern, in which a human approves
      each memory before it becomes a rule.
- **Strengths.** It captures conventions nobody wrote down. Citation checking makes a wrong
  memory cheap to detect, because verifying a fact against code is easier than finding it.
- **Weaknesses.** Memories without evidence pointers cannot be checked. Memory is a persistence
  surface for injected content, which OWASP lists as ASI06, memory and context poisoning.
  Facts that rest on business rules rather than code cannot be validated by reading code.
- **Cost.** Low at write time. GitHub reported that read-time verification added no significant
  latency.
- **Fits.** "API version strings must be changed in three files together", with citations to the
  three files.
- **Does not fit.** "Client X's mandate excludes tobacco issuers." That is a business fact with a
  system of record, and it should be read from that system rather than remembered.

### 5.9 Managed memory services

- **How it works.** A service extracts facts, summaries and preferences from agent interactions
  and stores them for retrieval, usually with vector search and namespaces.
    - Amazon Bedrock AgentCore Memory separates short-term memory per session from long-term
      memory produced by extraction strategies, and organises long-term records under
      hierarchical namespaces such as `/users/{actorId}/preferences`
      ([AgentCore namespaces](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/session-actor-namespace.html)).
    - Mem0, Zep and Letta offer similar services with different extraction and graph models.
- **Strengths.** Identity, tenancy, retention and access control are handled by the service.
  This addresses the multi-user gap that issue #1335 describes.
- **Weaknesses.** These services were built for conversational assistants that remember users,
  not for engineering knowledge that must be reviewed and versioned with code. Extracted memories
  are not reviewed in a pull request. The published benchmarks are disputed: Letta reported 74%
  on LoCoMo using plain files and grep, above Mem0's published 68.5%, and Zep disputed Mem0's
  implementation of the benchmark ([Letta](https://www.letta.com/blog/benchmarking-ai-agent-memory)).
  All of these figures are self-reported by vendors.
- **Cost.** A service fee and an integration, plus a second place where knowledge lives.
- **Fits.** Remembering a developer's preferences across sessions, or holding short-lived
  per-session state for a hosted AI-DLC platform.
- **Does not fit.** Holding the firm's architectural rules, which need review, versioning and an
  audit trail that a vector store does not provide.

### 5.10 Graph-backed context

- **How it works.** Code, work items and business entities are held as a graph and exposed to the
  agent through query tools.
- [sdlc-context-graph.md](sdlc-context-graph.md) covers this pattern in full, including Uber,
  Atlassian and Sourcegraph. The point relevant here is that a graph is a retrieval backend for
  the stores in this report, and the governance and freshness questions in section 9 apply to it
  in the same way.

## 6. Side-by-side comparison

| Pattern | Best for | Freshness | Token cost | Governance | Main failure |
|---|---|---|---|---|---|
| Always-loaded files | Short, universal rules | Manual | Paid every turn | Pull request review | Bloat and drift |
| Scoped rules | Module and stage rules | Manual | Proportional to scope | Pull request review | Rule silently not loaded |
| Skills | Procedures | Manual | Near zero until used | Library curation | Wrong skill chosen |
| Just-in-time retrieval | Code, large document sets | Current by construction | Exploration cost | Source system's own | Unknown items never sought |
| Durable state | Workflow position | Written each step | Small | Engine-owned | Misread or divergent state |
| Compaction | Long sessions | Not applicable | One call per compaction | None | Loss of operating instructions |
| Subagents | Exploration, parallel work | Not applicable | High | None | Conflicting implicit decisions |
| Verified agent memory | Undocumented code conventions | Checked at read | Small | Repository access rules | Unverifiable or poisoned entries |
| Managed memory service | Per-user and per-session memory | Extraction-dependent | Small | Service-level | Unreviewed facts |
| Graph-backed context | Relationships across systems | Depends on feed | Small per query | Entitlements at query | Stale graph trusted |

## 7. What the evidence shows

### 7.1 Instruction files

- Gloaguen and colleagues evaluated context files across Claude Code,
  Codex and Qwen Code on SWE-bench Lite and on AGENTbench, a new set of 138 tasks from 12
  repositories that already contain developer-written context files
  ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988)).
    - LLM-generated context files reduced success by between 0.5 and 2 points depending on the
      benchmark, and raised cost by about 20% to 23%.
    - Developer-written files raised success by about 4 points on average, but not for Claude
      Code, and raised cost by up to 19%.
    - Agents followed the instructions they were given, so tools named in a context file were
      used far more often. Codebase overviews did not help agents locate the relevant files.
    - The authors recommend omitting generated context files and keeping human-written ones to
      minimal requirements such as specific tooling.
- Lulla and colleagues ran Codex on 124 merged pull requests from 10 repositories with and without
  `AGENTS.md` ([arXiv 2601.20404](https://arxiv.org/abs/2601.20404)).
    - Median wall-clock time fell by 28.6% and mean output tokens by 20.1%, both statistically
      significant.
    - Correctness was not measured beyond a manual sanity check of 50 tasks, which the authors
      state is not a correctness evaluation.
- A July 2026 ablation across Claude Code and Codex, with 288 runs on 17 tasks, reported that the
  context strategy did not measurably change correctness for either agent
  ([arXiv 2607.27250](https://www.alphaxiv.org/abs/2607.27250)). I have read only the abstract of
  this paper.
- The combined reading is that a short, accurate instruction file makes an agent somewhat more
  efficient and has a small and inconsistent effect on correctness, and that a long or generated
  one increases cost without improving results.

### 7.2 Input length

- Chroma's July 2025 report tested 18 models, including GPT-4.1, Claude 4, Gemini 2.5 and Qwen3,
  and found that performance became less reliable as input length grew, even on tasks as simple
  as copying a sequence of repeated words ([Chroma](https://research.trychroma.com/context-rot)).
  Semantically similar distractors made the degradation worse.
- This is the main argument against loading all available knowledge at every stage, which is
  what AI-DLC's directory-based loader does for the folders that exist.

### 7.3 Agent memory

- GitHub's A/B tests of Copilot memory reported a merge rate of 90% with memory against 83% without
  it for the coding agent, and a 3% increase in precision and 4% increase in recall for code
  review, with p-values below 0.00001. GitHub also seeded repositories with false memories whose
  citations pointed at irrelevant code, and reported that agents detected and corrected them, but
  published no figures for that test. These are a vendor's results on its own product, though they
  come from production traffic rather than a benchmark.
- ACE reported improvements of 10.6% on agent benchmarks and 8.6% on finance tasks over strong
  baselines, using execution feedback rather than labelled data.
- The LoCoMo results for memory services disagree with each other by up to 24 points depending on
  who ran the benchmark, and no independent replication exists. Letta's conclusion, that how an
  agent manages its context matters more than which retrieval mechanism it uses, is consistent
  with the rest of this section.

### 7.4 Layered context in a real project

- The Codified Context paper reports 283 sessions over 70 days building a 108,000-line C# system
  with a 660-line constitution, 19 specialist agent definitions and 34 on-demand specification
  documents served over MCP.
    - The context infrastructure totalled about 26,200 lines, equal to 24% of the code.
    - Maintenance took one to two hours per week, including a biweekly review and about five
      minutes per spec update made in the same session as the code change.
    - Staleness was the main failure. On at least two occasions an outdated specification led
      the agent to write code that conflicted with a recent refactor.
- The evidence is observational, from one developer on one project, and the author makes no
  causal claims.

### 7.5 What is missing

- There is no published measurement of context management strategies within AI-DLC itself.
  Issue [#684](https://github.com/awslabs/aidlc-workflows/issues/684) requests benchmarks and is
  open.
- A secondary blog post attributes to Amazon a three-tier selective artifact loading strategy that
  reduces token usage by 40% to 60%. I could not find an Amazon source for that figure.

## 8. Lessons reported by teams that built these systems

- **Keep the prompt prefix stable and the context append-only.** Manus reports an input to output
  token ratio of about 100 to 1 and a tenfold price difference between cached and uncached input,
  which makes the cache hit rate its most important production metric. Inserting retrieved
  context near the start of the prompt, or reordering rules between turns, invalidates the cache.
- **Mask tools rather than removing them.** Manus constrains which tools can be called through
  logit masking instead of changing the tool list mid-task, for the same cache reason.
- **Make compression reversible.** A web page can be dropped from context as long as its URL is
  kept, and a file's contents can be dropped as long as its path is kept. This lets the agent
  reload the content if it turns out to matter.
- **Keep failures in the context.** Manus found that removing failed actions and error traces
  caused the model to repeat them.
- **Verify at read time rather than curating offline.** GitHub rejected an offline pipeline for
  deduplicating and expiring memories as too expensive in engineering and model cost, and relied
  on citation checks at the point of use.
- **Use structured formats for anything that controls the workflow.** Anthropic found that the
  model was less likely to overwrite a JSON feature list than a Markdown one, and AI-DLC issue
  #249 shows a prose status being misread at a gate.
- **Write a fact down the second time it has to be explained.** This is one of the Codified
  Context guidelines, and it gives a practical trigger for creating knowledge rather than trying
  to document everything up front.
- **Detect drift mechanically.** The Codified Context project ran a hook at session start that
  compared recent commits against the mapping from subsystems to specification documents and
  warned when code had changed without a matching spec change.
- **Keep instruction files to what the agent cannot discover.** Both the ETH study and practitioner
  write-ups conclude that directory overviews and general guidance add cost without helping.
- **Do not let the conversation be the only copy of anything that matters.** Every published
  harness for long-running work writes state, progress and decisions to files or git, and
  treats the conversation as disposable.

## 9. A reference design for an AI-DLC context management system

This section proposes a design for an organisation implementing context management around
AI-DLC. It assumes AI-DLC version 2 as the workflow engine and adds the parts that sections 4.5
and 7 show are missing.

### 9.1 Design principles

- Each category of context in section 3 has one authoritative store, one owner and a defined
  freshness mechanism. A copy in any other place is treated as a cache.
- Context that can be derived from a maintained source is derived or read live, and only context
  that cannot be derived is authored.
- The default for any knowledge item is to be retrievable on demand, and an item is loaded
  automatically only when there is evidence that agents need it on most tasks in its scope.
- Anything that controls a gate, an approval or a rule is stored in a structured format with a
  schema, and anything advisory can be prose.
- Every item that reaches an agent carries its source, version and last verification time, so the
  agent and the reviewer can judge whether to trust it.

### 9.2 Stores and their responsibilities

| Store | Holds | Format | Authoritative source | Write path |
|---|---|---|---|---|
| Rule store | Organisational, team and project rules | Markdown with front matter: scope, owner, review date | Git repository of rules, separate from application code for org rules | Pull request with owner approval |
| Knowledge store | Domain knowledge, specifications, ADRs | Markdown with front matter: owner, sources, last verified | Git, indexed for search | Pull request, or promotion from elaboration output |
| Code knowledge | Component inventory, dependency graph | Generated | Source code | Regenerated on merge, never edited by hand |
| Workflow state | Intent, stage, gate status, unit progress | JSON or a database table with a schema | AI-DLC engine | Engine only |
| Decision log | Decisions, rationale, approver, affected units | Structured records | Git or database | Written at the gate where the decision is made |
| Audit trail | Events | Append-only shards | AI-DLC audit folder, exported to a central log | Engine and hooks only |
| Agent memory | Learned conventions with citations | Subject, fact, citations, reason, timestamp | Repository-scoped store | Agent writes, verified on read, promoted to rules only by review |
| Live sources | Tickets, incidents, reference data, restrictions | Native | Owning systems | Not written by the context system |

- The rule store and the knowledge store map to AI-DLC's `memory/` and `knowledge/` folders. The
  additions are front matter that records ownership and freshness, and a separate repository for
  organisational rules so that a change to `org.md` follows the organisation's change process
  rather than an application team's.
- The decision log is the structured record that issue #423 says the audit trail does not
  provide. Each entry names the decision, the alternatives considered, the approver and the units
  it constrains, so that a unit built later can query the decisions that apply to it.

### 9.3 Assembling context for a stage

- Each stage declares a context manifest that lists what it needs: which rule scopes, which
  knowledge tags, which upstream artifacts and which live tools. The engine assembles the context
  from the manifest rather than by walking directories.
- The manifest carries a token budget for each tier.
    - The always-loaded tier holds the rule summary, the current state and the stage
      instructions, and should stay within a few thousand tokens.
    - The conditional tier holds rules and knowledge matched by scope and tag, up to its budget,
      with the overflow offered as references the agent can read.
    - The on-demand tier is exposed as tools: knowledge search, code search, decision log query,
      and read-only access to live systems.
- The order of assembly follows the cache. Stable content such as organisational rules and stage
  instructions comes first, and volatile content such as state and retrieved items comes last.
- The engine records in the audit trail which items were loaded, with their versions. AI-DLC
  currently records only the agent, which makes it impossible to establish afterwards what an
  agent was told when it produced a given artifact.
- Stages that produce large transcripts run in subagents and return a summary and the artifacts
  they wrote, as proposed in issue #421. Stages that make decisions affecting several units stay
  in the main context or write the decision to the decision log before returning.

### 9.4 The write path and governance

- Agents may propose rules and knowledge but may not write them directly to the authoritative
  stores. AI-DLC's learning loop already asks the human, and the addition is that a team-level or
  organisational rule becomes a pull request to the rule repository with an owner as reviewer.
- Elaboration sessions are the main source of domain knowledge. The clarifying questions and
  answers from Mob Elaboration are extracted into knowledge items with the elaboration session as
  their source, which is the point [ai-dlc.md](ai-dlc.md) section 7.1 makes about forcing folklore
  into the open.
- Every knowledge item has an owner. An item whose owner has left the team is flagged in the same
  way as an item past its review date.
- Write access to agent memory follows repository write access, and read access follows
  repository read access, which is the model GitHub uses.

### 9.5 Freshness and invalidation

- Code knowledge is regenerated on merge to the main branch and stamped with the commit it was
  generated from. AI-DLC's `codekb` already carries a freshness marker, and the engine should
  refuse to serve it, or label it, when the marker is older than the head of the branch.
- Knowledge items that cite code paths are checked by a drift hook of the kind described in the
  Codified Context paper. When a cited file changes, the item is flagged for review.
- Knowledge items that cite documents use the same invalidation that AI-DLC's DocumentKB applies
  to summaries, which are withheld rather than served once the source document changes.
- Agent memories are verified against their citations on read and expire if unused, following
  the Copilot model.
- Every item served to an agent includes its last verification date, so that the agent can be
  instructed to treat older items with caution and so that a reviewer can see what the agent
  relied on.

### 9.6 Compaction and the resume protocol

- The conversation is treated as a cache of the stored state. After a compaction, a clear or a
  harness restart, the engine re-injects the current state, the next directive and the stage's
  operating contract from the stores, which addresses issue #2454.
- Any recovery summary carries the state revision it was produced from. On resume the engine
  compares that revision with the stored one and, if they differ, states that the stored state is
  authoritative and discards the summary's claims about progress, which is the fix proposed in
  issue #2492.
- Gate status is a separate field from artifact status, with distinct values for generated,
  awaiting approval, approved and rejected, so that a resumed session cannot mistake a generated
  artifact for an approved one, which addresses issue #249.
- Compaction should preserve open questions, decisions not yet written to the decision log, and
  failed approaches. Everything that already exists in a store can be dropped and reloaded.

### 9.7 Multiple developers and multiple units

- Per-clone audit shards, which AI-DLC already uses, avoid merge conflicts for events. The same
  approach does not work for decisions, because two units can make conflicting decisions without
  any file conflict.
- Decisions that affect a unit boundary, such as a message contract or a shared schema, are
  written to the decision log at the moment they are made, and the engine checks each unit's
  context manifest against new decisions at the start of each stage.
- For organisations with many teams, the stores in section 9.2 move from a local `aidlc/` folder to
  a shared service with identity and access control, which is the direction issue #1335 describes.
  The Git repositories remain the authoritative source for rules and knowledge, and the service
  indexes and serves them.

### 9.8 Security and entitlements

- Retrieved context is untrusted input. Knowledge items, memories and live data are delimited in
  the prompt and labelled with their source, and they are never placed where the model treats
  them as system instructions. AI-DLC's DocumentKB already labels tags as untrusted.
- Entitlements are enforced when context is retrieved, not by instructions in the prompt. An
  agent working on an equities intent should not be able to retrieve fixed income client data
  through a shared knowledge index. [sdlc-context-graph.md](sdlc-context-graph.md) section 9 and
  [ai-security.md](ai-security.md) cover the same requirement.
- Writes to memory and knowledge are logged with their source, so that a poisoned entry can be
  traced and removed along with everything derived from it.
- Secrets never enter any store. AI-DLC already masks secret-shaped values in the project
  description, and the same scan should run on knowledge and memory writes.

### 9.9 Measurement

- The following measures should be recorded per stage from the first pilot, because the evidence
  in section 7 shows that self-reported improvements are unreliable.
    - Tokens loaded per tier, tokens consumed, cache hit rate and cost.
    - Number of compactions per intent and number of resumes that required manual correction.
    - Proportion of loaded items that the agent cited or used, as an estimate of precision.
    - Rework at gates attributed to missing or stale context, recorded by the reviewer.
    - Age distribution of the knowledge items served.
- AI-DLC issue [#1211](https://github.com/awslabs/aidlc-workflows/issues/1211) requests token
  consumption in the audit log, which would provide the first of these.

## 10. Capital markets scenarios

### 10.1 Client mandate and restriction changes: a case where the design fits

- A team is changing the pre-trade compliance engine so that a new class of ESG exclusion can be
  expressed in client mandates.
- The organisational rule store supplies the rule that every restriction change requires a
  regression run against the full mandate set and a second reviewer from compliance technology.
- The knowledge store supplies the precedence rules for conflicting restrictions, which were
  captured as knowledge items during Mob Elaboration with the compliance officer named as owner.
- The actual restriction lists are read live from the reference data system through a read-only
  tool, rather than from any document or memory, because they change daily.
- The decision log records the choice to evaluate exclusions before concentration limits, and the
  unit building the reporting view retrieves that decision when it starts.
- An auditor can later establish which rules and knowledge items, at which versions, were in the
  agent's context when it generated the evaluation code, because the stage recorded its loaded
  items.

### 10.2 Settlement break investigation: a case where it partly fits

- An agent is asked to find why a class of cross-border settlement breaks increased after a
  change to the instruction enrichment service.
- Code knowledge and just-in-time code search work well here, because the relevant facts are in
  the code and its history.
- Domain knowledge about market-specific settlement conventions is useful but has to be checked,
  because a knowledge item written before the move to T+1 settlement in the relevant market may
  still describe T+2 behaviour. The last verification date on the item is what lets the agent
  and the reviewer notice this.
- The incident and break data must come from the live systems. Copying break samples into the
  knowledge store would create a stale and possibly sensitive copy.

### 10.3 Research over filings and earnings call transcripts: a case where it does not fit

- A team builds a tool that summarises earnings call transcripts for analysts. The content the
  application processes at runtime is a retrieval problem for the product, and it is covered by
  [agentic-ai.md](agentic-ai.md).
- The AI-DLC context management system should hold the rules and decisions about how the
  application is built, not the corpus the application serves. Indexing filings into the
  development knowledge store would mix product data with engineering knowledge, enlarge every
  search and raise licensing questions about the data.

### 10.4 Beneficial ownership hierarchies: a case for a graph rather than documents

- A change to the know-your-customer service depends on how ownership chains are walked through
  intermediate holding companies.
- Documents describing the hierarchy logic are adequate for the agent, but the hierarchy data
  itself is relational and is better exposed as a graph query tool, as described in
  [sdlc-context-graph.md](sdlc-context-graph.md) section 3.3, with entitlements enforced on the
  query.

## 11. Build order

1. **Fix the state model.** Separate gate status from artifact status, move gate-controlling
   fields to a schema, and add the state revision check on resume. This addresses the issues
   that can let work pass an approval gate, and it is small.
2. **Record what was loaded.** Add the list of context items and versions to the stage start
   event. This is a prerequisite for measuring anything else and for audit.
3. **Add ownership and freshness metadata** to rules and knowledge, and a drift hook that flags
   items whose cited code has changed.
4. **Introduce stage manifests and token budgets,** starting with the stages that cause the most
   compactions, and move those stages into subagents.
5. **Add the decision log** and make units check it at stage start.
6. **Add retrieval tools** for knowledge, decisions and live systems, and reduce the always-loaded
   tier to what the measurements show agents use.
7. **Add verified agent memory** for code conventions, scoped to repositories.
8. **Move to a shared service** for the stores when more than a few teams need the same rules and
   knowledge, keeping Git as the source of truth.

## 12. Failure modes to watch for

- The knowledge store grows because adding a file is easy and removing one requires someone to
  decide it is no longer true. The cost appears as more tokens per stage and lower accuracy.
- A generated context file or knowledge item is accepted without review, and agents follow its
  inaccurate instructions closely.
- A conversation summary disagrees with stored state, and the agent acts on the summary.
- A team rule contradicts an organisational rule, and the additive model loads both without
  either the agent or the reviewer noticing.
- A knowledge item describes a business rule that has since changed, and nothing links the item
  to the system where the change was made.
- A memory written from an abandoned branch is retrieved on the main branch. GitHub tested for
  this specifically.
- Entitlements are enforced in the prompt, so a shared index becomes a route to data the user
  cannot otherwise read.
- Better context increases throughput into a review process that is already the constraint, as
  described in [ai-dlc.md](ai-dlc.md) section 7.3.

## 13. Open questions

- Whether always-loaded rules improve correctness at all, given the mixed results in section 7.1,
  or only efficiency. A pilot can answer this for one codebase by running a small number of
  intents with the rule tier reduced to a minimum.
- How to validate memories and knowledge that rest on business rules rather than code, since the
  citation approach depends on a cheap check against a source that is easy to read.
- How AI-DLC's additive rule model should handle genuine conflicts between team and organisational
  rules, since the current check is advisory.
- Whether a hosted AI-DLC deployment will be published by AWS, or whether each organisation will
  build its own service around the file layout.

## Resources

- AWS AI-DLC documentation:
  [Spaces and Intents](https://awslabs.github.io/aidlc-workflows/guide/03-spaces-and-intents/),
  [Knowledge](https://awslabs.github.io/aidlc-workflows/guide/08-knowledge/),
  [Rules and the Learning Loop](https://awslabs.github.io/aidlc-workflows/guide/09-rules-and-the-learning-loop/),
  [State Tracking and Audit Trail](https://awslabs.github.io/aidlc-workflows/guide/10-state-and-audit/),
  [Session Management](https://awslabs.github.io/aidlc-workflows/guide/11-session-management/).
- [awslabs/aidlc-workflows issues](https://github.com/awslabs/aidlc-workflows/issues), particularly
  #249, #421, #423, #1330, #1335, #2454 and #2492.
- Anthropic,
  [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents),
  September 2025.
- Anthropic,
  [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents),
  November 2025.
- Manus,
  [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus),
  July 2025.
- GitHub,
  [Building an agentic memory system for GitHub Copilot](https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot/),
  January 2026.
- Gloaguen et al.,
  [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988),
  February 2026.
- Lulla et al.,
  [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404),
  January 2026.
- Vasilopoulos,
  [Codified Context: Infrastructure for AI Agents in a Complex Codebase](https://arxiv.org/abs/2602.20478),
  February 2026.
- Zhang et al.,
  [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618),
  October 2025.
- Chroma, [Context Rot](https://research.trychroma.com/context-rot), July 2025.
- Factory, [Evaluating context compression](https://factory.ai/news/evaluating-compression),
  December 2025.
- Letta, [Benchmarking AI Agent Memory](https://www.letta.com/blog/benchmarking-ai-agent-memory),
  August 2025.
- Cognition, [Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents), June 2025.
- [Kiro steering documentation](https://kiro.dev/docs/steering/).
- [Agent Skills specification](https://agentskills.io/specification).
- [Amazon Bedrock AgentCore Memory: memory strategies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-strategies.html).
- OWASP, Top 10 for Agentic Applications 2026, entry ASI06 on memory and context poisoning.
