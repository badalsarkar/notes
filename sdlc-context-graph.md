# Context Graphs in the Software Delivery Lifecycle

Research report, September 2026. Related notes: [ai-dlc.md](ai-dlc.md),
[specification-driven-development.md](specification-driven-development.md),
[agentic-ai.md](agentic-ai.md), [software-dev-with-gen-ai.md](software-dev-with-gen-ai.md),
[ai-security.md](ai-security.md).

## 1. What this report covers

Coding agents need to know things that are not in the file they are editing: what calls this
function, which team owns that service, what the last incident on it was, and which client
restrictions the change has to respect. Several organisations have answered this by building a
graph and letting agents query it. This report covers what goes into such a graph, who has built
one, what it measurably buys, why most of them go stale, and how this relates to the methodology
described in [ai-dlc.md](ai-dlc.md).

It does not cover graph retrieval as a general technique. [agentic-ai.md](agentic-ai.md) already
covers GraphRAG, temporal knowledge graphs, ontologies and semantic layers as retrieval methods,
including the GraphRAG-Bench results and the change in indexing cost, and that material is not
repeated here. This note is about the software delivery application specifically.

## 2. Summary

Three different things are called graphs in this area, and conflating them is the main source of
confusion. A **code graph** holds symbols, calls and types, and is derived mechanically from
source. A **work or context graph** holds services, teams, incidents, pull requests, deploys and
tickets, and has to be fed from the systems that own them. A **business ontology** holds products,
clients, policies and the rules the firm operates by, and is a data modelling programme rather
than a build. They have different costs, different refresh mechanics and different failure modes.

AI-DLC builds none of them, although its own output is graph-shaped: intent, units of work,
stories, designs, code, tests and timestamped approvals are nodes and edges persisted as markdown
in a repository directory. That keeps the method portable across agent harnesses and is also what
limits it, because nothing can be queried, only read. AWS sells graph products, but they are a
separate product line that the methodology does not reference.

The measurable benefit of a code graph is efficiency rather than correctness. Published results
show large reductions in tokens, tool calls and latency, and small single-digit improvements in
task resolution. At the scale where an organisation runs agents continuously, efficiency is the
thing that matters, which is why the clearest public results come from the largest adopters.

The binding constraint is staleness. A stale graph returns a confident structured answer with no
timestamp, and agents do not reliably notice. The rule that has emerged from practice is to build
the graph on top of systems that are already continuously updated, rather than running a separate
extraction pipeline that has to be maintained.

## 3. Three different graphs

### 3.0 The two terms

A **knowledge graph** stores facts as nodes with typed, named relationships between them rather
than as prose. "Restriction R-14 applies to account A and supersedes R-09" becomes two labelled
edges instead of a sentence. The relationships are data that can be queried and traversed, which
is the entire difference from a document that states the same thing.

A **context graph** is a knowledge graph that also carries the process history: decisions, who
made them, when, and what they touched. Gartner uses the term this way, and
[agentic-ai.md](agentic-ai.md) section 3.7 covers it alongside semantic layers. A knowledge graph
says what is true. A context graph also says how the organisation came to believe it and who
signed it off.

A context graph is therefore a kind of knowledge graph, and the part that distinguishes it —
decision traces and workflow history — is exactly what a delivery method like AI-DLC spends its
whole process producing. The three sections below separate the graphs by what they hold and what
they cost, which is the distinction that matters when deciding whether to build one.

### 3.1 The code graph

**What is in it.** Functions, methods, classes, interfaces, types and modules as nodes, with
calls, imports, inheritance, implementation and type usage as edges. Open implementations
typically carry around 14 node types and 15 or more edge types, plus derived structure such as
module boundaries and community detection over the call graph.

**Where it comes from.** Static analysis of the source, either through the Language Server
Protocol, an indexing format such as SCIP, or a parser such as tree-sitter. No human authors it.

**How it stays fresh.** It is recomputed from the code, and incremental re-indexing is fast
enough to run on every commit. Because the source is its own record, this graph requires no
separate maintenance process, which is what distinguishes it from the other two.

**What it costs.** Very little. One open implementation indexes Django at 49,000 nodes and
196,000 edges in about six seconds, and the Linux kernel at 2.1 million nodes and 4.9 million
edges in about three minutes, with incremental re-indexing at roughly 1.2 seconds.

**What it answers.** Symbol lookup, call graphs, type hierarchies and impact radius, in one query
rather than a sequence of greps.

**Limitations.** It is static, so runtime behaviour, reflection and dynamic dispatch are not
represented. Language features that a parser does not model are simply absent, and macro-heavy C
is the reported worst case. It also does not hold source lines, so an agent that needs to read
the actual implementation still has to open the file.

**Capital markets example.** Changing the format of a settlement instruction field, and needing
to know every service, batch job and report that reads it before deciding whether the change is
one release or four.

### 3.2 The work or context graph

**What is in it.** Services, engineering teams, ownership, incidents, pull requests,
architectural design documents, deployments, datasets and query history. Uber's public example
runs to 86 node types and 117 edge types.

**Where it comes from.** Existing internal systems, typically dozens of them, joined on shared
identifiers.

**How it stays fresh.** Only by being fed continuously from those systems. This is where most
implementations fail, and section 7 covers it.

**What it costs.** Substantial platform work, and the cost is ongoing rather than one-off. It is
an integration programme, not an indexing job.

**What it answers.** Questions that cross system boundaries, which is most of what a developer
actually asks: who owns this, what changed recently, what broke last time, what depends on it
operationally rather than syntactically.

**Limitations.** It inherits the quality of the systems feeding it. If service ownership is wrong
in the source of record, the graph makes that wrong answer faster and more confident.

**Capital markets example.** A surveillance feed stops producing alerts overnight. The useful
question is which deployment touched the upstream topic, who approved it, which team owns the
consumer, and whether the same change went to any other environment.

### 3.3 The business ontology

**What is in it.** The firm's business objects and the rules that relate them: what an instrument
is, what a mandate is, what a restriction is, and which takes precedence when two conflict.

**Where it comes from.** Domain experts, with tooling now able to draft a first version from
existing data for experts to review rather than starting from a blank page.

**How it stays fresh.** Governance. There is no mechanical refresh, because the source of truth
is organisational agreement.

**What it costs.** The most of the three, and the cost is mostly people's time rather than
compute. [agentic-ai.md](agentic-ai.md) section 3.7 treats this as a programme with its own
timeline, and that framing holds here.

**What it answers.** What "correct" means, which is exactly what a coding agent needs and what a
specification written in prose only approximates.

**Limitations.** It does not help with unstructured text, and it cannot be installed. An ontology
that does not reflect how the business actually decides things is worse than none, because it
will be treated as authoritative.

**Capital markets example.** The precedence rules for client mandates and restrictions, which in
most firms exist as folklore spread across operations and compliance, and which AI-DLC's
elaboration ceremony is designed to extract.

## 4. What AI-DLC actually has

### 4.1 Its output is already graph-shaped

The method produces the material a context graph holds, and persists it as markdown. Read the
phases described in [ai-dlc.md](ai-dlc.md) section 5 as nodes and edges and the structure is
plain:

| AI-DLC artifact | Graph role |
|---|---|
| Business intent | Root node |
| Unit of Work | `decomposes_from` the intent |
| User story | `derives_from` a unit |
| Domain model | An ontology fragment: the business objects and how they relate |
| Design | `designs` a story |
| Code, tests | `implements`, `tested_by` |
| Infrastructure, deployment, monitoring | `deploys`, `observed_by` |
| Audit file entries | Edge properties: `approved_by`, `generated_by`, `at`, and the raw input |

The nodes exist, the edges exist as prose references inside documents, and none of it is
queryable. This is the sense in which AI-DLC has a context graph written down as files rather
than no context graph at all.

### 4.2 Two graphs, treated as one

Separating them matters, because they have opposite economics.

- **The traceability graph** runs intent to unit of work to story to design to code to test to
  approval. It is vertical, scoped to one initiative, and **created by the method itself**. This
  is what [ai-dlc.md](ai-dlc.md) section 5.4 calls the paper trail and what section 8.3 needs in
  order to answer an auditor.
- **The knowledge graph the method consumes** is the structure of the codebase plus the business
  ontology: approved dependencies, architectural rules, restriction precedence, regulatory
  obligations. It is horizontal, pre-existing, far larger than any one initiative, and it outlives
  every one of them. This is what [ai-dlc.md](ai-dlc.md) section 8.2 calls a codified definition
  of "correct", and what the steering files gesture at.

AI-DLC generates the first as files and assumes the second exists as prose in steering files. That
is the gap, and it is why the two halves fail differently: the traceability graph is merely
unqueryable, while the consumed knowledge graph silently drifts.

**A worked example.** A change to client restriction precedence, run through AI-DLC as published,
produces a handful of markdown files and an audit log. Asking which code implements restriction
rule R-14, which parts of it were generated rather than written, who approved them, and what else
that design decision affected requires a person to read the trail and reconstruct the answer. With
the same material held as a graph it is one traversal, and the last part of the question becomes
answerable at all rather than a matter of recollection. With a code graph underneath it also runs
in reverse: this function is changing, so which requirements does it trace back to.

### 4.3 Where the graphs physically exist today

- **Nothing in the published workflows is a graph.** The artifacts in
  [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) are markdown files in a
  documentation directory plus a timestamped audit file. This is what makes the method portable
  across seven agent harnesses, and it is also why the context does not survive contact with a
  large codebase: nothing can be queried, only read.
- **The ontology, such as it is, lives in two prose documents**: the domain model produced during
  Construction, and the steering files. In graph terms that is an ontology with no schema, no
  query interface and no way to detect drift, which is the failure described in section 7.
- **A related AWS sample goes further.** The
  [AIDLC Collaborative](https://aws-samples.github.io/sample-collaborative-ai-dlc/) implementation
  holds requirements, user stories, designs, decisions and code as typed, linked items, with a
  traceability graph view and an intent workbench. Agents write artifacts through MCP tools while
  the platform engine owns all git operations. The stated goal is to trace from a business
  requirement to the code implementing it and back. It is still a conceptual graph over artifacts
  rather than a graph database, but it is the clearest acknowledgement from AWS that the
  methodology's audit trail requires graph structure to be useful.
- **AWS's actual graph products are a separate line.** AWS Context, announced at the New York
  Summit on 17 June 2026, builds a knowledge graph from an organisation's existing data, provides
  agentic search over it, and is described as improving itself from agent usage patterns rather
  than manual curation, extending the graph technology behind Amazon Quick. The
  [Context Ontology Accelerator](https://aws.amazon.com/about-aws/whats-new/2026/07/aws-context--ontology-accelarator-generally-available/)
  became generally available on 31 July 2026: it is open source under Apache 2.0, drafts a
  business ontology from connected data sources for domain experts to review and refine, stores
  the approved result in a knowledge graph using W3C standards on Amazon Neptune and OpenSearch
  Serverless, and exposes it to any agent over MCP. AWS claims this reduces months of manual
  ontology work to days. Neither product is referenced by the AI-DLC workflows.
- **Kiro, where AI-DLC most often runs, added an index rather than a graph.** Its Code
  Intelligence feature integrates the Language Server Protocol for go-to-definition, find
  references, hover information and diagnostics, and its Knowledge Index lets an agent
  configuration declare custom knowledge sources that stay in sync with the codebase. The
  community filled the remaining gap with
  [KiroGraph](https://github.com/davide-desio-eleva/kirograph), a local tree-sitter graph over 33
  or more languages stored in SQLite, answering symbol relationships, call graphs and impact
  radius in a single MCP call, and claiming up to a 90% reduction in tokens.

The practical conclusion is that adopting AI-DLC means adopting flat files. Any graph is something
the adopting organisation bolts on, and the methodology offers no guidance on doing so.

## 5. What other organisations have built

### 5.1 Uber

The most substantive public example. Uber's AI Context Graph holds 24 million nodes and 80 million
edges across 86 node types and 117 edge types, fed from more than 30 internal systems covering
services, engineering teams, incidents, pull requests, architecture documents, deployments,
datasets and historical table usage. Agents query it in natural language.

The published comparison is a single illustration rather than a measurement, but it is a useful
one: given an identical prompt and the same model, the graph-grounded agent answered in 38
seconds, while the ungrounded agent spent 20 minutes inspecting service code, spawned two
subagents, hit three errors and concluded incorrectly that the dataset was unqueryable.

The surrounding numbers matter more. More than 70% of pull requests now come from local or cloud
agents, engineers have built over 3,600 agent skills, and the platform runs more than 30,000 skill
executions a day. Total AI spend has been flat since April 2026 while weekly agentic requests grew
9.4 times in six months. The context to keep alongside this is that Uber reportedly consumed its
2026 AI budget within four months before that optimisation work, so the graph is partly a
cost-control response rather than purely a quality one.

### 5.2 Atlassian

The clearest commercial competitor to AI-DLC's pitch, and it competes on exactly the layer
[ai-dlc.md](ai-dlc.md) section 5.4 treats as the method's distinguishing feature.

At Team '26 on 6 May 2026 Atlassian opened its Teamwork Graph so that Rovo and third-party agents
can search, reason and act across it. Code Context, built on that graph, gives coding agents
intelligence across multi-repository codebases. A CLI gives any coding agent, including Claude
Code and Codex, a single way to reach that context. Agent Context Controls let platform teams
govern which agents may operate in a space and precisely what they may see. The framing is
"governed agent loops" for an AI-native SDLC, in which developers define intent and guardrails,
agents execute in parallel, and people review and approve what ships.

Atlassian's own position is that the bottleneck is organisational context rather than model
intelligence. The supporting claims are that 94% of engineering leaders report using AI while only
6% have the systems to scale it across the lifecycle, and that analysis by DX found teams whose AI
tools used the most Teamwork Graph context shipped roughly 64% more per developer. DX is owned by
Atlassian, so the second figure is vendor research and should be read as such.

The structural difference from AI-DLC is more important than the feature list. Atlassian's graph is
built on work items that already exist and are already maintained, so it inherits freshness.
AI-DLC generates new markdown that someone has to keep current by hand.

### 5.3 Sourcegraph

Repositioned with version 7.0 in February 2026 as a shared intelligence layer for both developers
and agents. Its MCP server, backed by SCIP indexing, exposes 13 tools to MCP-compatible agents
including Claude Code, Cursor, Amp and Codex. Agentic Batch Changes, built on the code graph,
picks an execution strategy per change: deterministic scripts for mechanical edits, and delegation
to a frontier agent where judgement is required. This is the most direct example of a code graph
being used to decide whether an agent is needed at all, which is a cheaper pattern than asking an
agent and hoping.

### 5.4 The rest of the market

- **Glean** sells an Enterprise Graph over people, projects, teams, products and processes, and
  positions itself as the entire context layer rather than a component in someone else's stack.
- **Harness** is pitching the same idea to CI customers under the heading that a repository is
  already a knowledge graph that nobody queries.
- **Google and Microsoft remain file-based at the methodology layer.** Antigravity's project
  constitution and Microsoft's repository-based context engineering are the same shape as AI-DLC's
  steering files. Microsoft's graph work is a separate research lineage, and the GraphRAG
  repository is now in maintenance mode with LazyGraphRAG as the cost answer.
- **MCP is the common interface**, having been donated to the Agentic AI Foundation under the
  Linux Foundation in December 2025. It has no authentication, rate limiting, audit logging or
  access control of its own, which is why a gateway market has grown up to enforce policy on tool
  calls. Anything exposing a context graph to agents in a regulated environment needs that layer.
- **Tool comparisons are mostly vendor-authored.** One widely cited comparison of five context
  graph tools scores Neo4j highest on developer ecosystem and its own publisher highest on
  enterprise governance, which is a fair summary of how this category is being written about.

### 5.5 Side by side

| | Code graph | Work / context graph | Business ontology |
|---|---|---|---|
| **Built by** | Anyone, in an afternoon | Platform teams | Domain experts with tooling |
| **Source of truth** | The repository | 20–30 internal systems | Organisational agreement |
| **Refresh** | Automatic, per commit | Continuous pipelines | Governance process |
| **Build cost** | Very low | High | Highest |
| **Main benefit** | Tokens, latency, impact analysis | Cross-system questions | A definition of correct |
| **Main risk** | Misses runtime behaviour | Goes stale invisibly | Models a business nobody runs |
| **Public examples** | Sourcegraph, KiroGraph, Codebase-Memory | Uber, Atlassian, Glean | AWS Context Ontology Accelerator, Palantir |

## 6. What the evidence shows

### 6.1 Measured effects of code graphs

- **RepoGraph** (ICLR 2025) represents a repository as a line-level graph from syntax trees and
  retrieves small ego-graphs around task-relevant symbols. Across four SWE-bench-Lite baselines it
  improves resolve rates by 2.00 to 2.66 absolute points, reported as a 32.8% average relative
  improvement. The relative figure flatters the result: it is 99.63% relative for the weak RAG
  baseline and 8.56% for Agentless. Agentless with RepoGraph reached a 29.67% resolve rate.
- **Codebase-Memory** (2026) is the clearest efficiency measurement. It builds a tree-sitter graph
  over 66 languages, exposed through MCP, and benchmarks against an agent that explores files
  directly across 31 languages. It reaches roughly 90% of the quality of file exploration, at 0.83
  against 0.92, while using about ten times fewer tokens, roughly 1,000 per query against 10,000,
  and 2.1 times fewer tool calls, at 2.3 against 4.8. Graph queries return in under a millisecond
  against 10 to 30 seconds of file exploration. The limitations are stated honestly: macro-heavy C
  scores worst at 0.58 because macros are not in tree-sitter syntax trees, the analysis is static
  so runtime behaviour and dynamic dispatch are absent, the file-exploring agent still wins where
  full source or exhaustive pattern matching is needed, and the evaluation used a single model and
  one repository per language.
- **CORE-Bench** (2026) compares graph-based, embedding-based and agentic search retrieval for
  code and finds that no single method dominates. The consistent recommendation across this
  literature is hybrid: vectors where semantic similarity matters, graph where the task is
  dependency navigation or low-latency relational lookup.
- **ARISE** (2026) applies repository-level graphs to fault localisation and agentic program
  repair with gains over non-graph baselines, and is explicit about the offsetting costs of graph
  construction, traversal overhead, memory and scaling on very large codebases.

The pattern is consistent with the GraphRAG evidence in [agentic-ai.md](agentic-ai.md) section
3.4. Graph retrieval helps where the question is structural, and it reduces the cost of reaching
an answer rather than improving the model's performance on the underlying task.

### 6.2 Evidence for the organisational graph comes mostly from its vendors

The Uber comparison and Atlassian's 64% figure are the two most quoted results, and both are
published by parties with an interest. The most useful independent-ish counterweight comes from
the same ecosystem. Atlassian's own research group coined the **AI efficiency paradox**:
individual output surges, then backs up at review, approval and other human-judgement gates,
cancelling out the flow.

DX's Q2 2026 data put numbers on it. Its aggregated Developer Experience Index fell for the first
time, from a median of 67 in Q3 2025 to 65 in Q2 2026, which it puts at roughly 20 lost hours per
engineer per year. Over the same period median quarterly AI spend rose from $1,500 to $44,000,
median pull request size went from 42 to 72 lines, and self-reported time saved rose from 3.3 to
6.1 hours a week. Code maintainability rose 3.8% while confidence in changes fell 6.1%. The causes
given are context-switching between multiple agents, larger and less testable batches, and
ordinary non-AI friction that nobody addressed.

The conclusion that matters for this note is that improving the context available to an agent
reduces the cost of the agent working out what is going on, and increases the volume of change
arriving at review. It does not address the verification tax described in
[ai-dlc.md](ai-dlc.md) section 7.3, and may enlarge it.

## 7. Staleness and how graphs are maintained

- **Staleness is difficult to observe.** A stale node returns a structured answer with no
  timestamp, and the agent treats it exactly as it treats a current one. A stale graph is worse
  than no graph, because it lends false confidence to impact analysis, which is both what graphs
  are best at and what people therefore rely on them for.
- **Agents do not reliably detect it.** The STALE benchmark (Chao et al., 2026) tests whether an
  agent notices that a stored memory is no longer valid, using 400 expert-validated conflict
  scenarios and 1,200 queries over more than 100 topics, with contexts up to 150,000 tokens. It
  probes three things: recognising that a prior belief is outdated, rejecting a question that
  presupposes a stale state, and applying an updated state in later behaviour. The best model
  evaluated reached 55.2% overall accuracy, so agent-side detection should not be treated as a
  control.
- **The common failure is treating construction as a project.** Teams populate a graph once from a
  snapshot, connect agents to it, and it is stale within weeks as services, schemas and ownership
  change. The graph then needs its own maintenance pipeline, which is the cost nobody budgeted.
- **The rule that follows.** Build the graph on top of a layer that is already continuously
  updated, so freshness is inherited rather than manufactured. This is why the code graph is easy,
  why Atlassian's approach of building on existing work items is structurally sound, and why a
  set of hand-written steering files is the weakest option available.
- **Indexing cost is no longer the main constraint.** Indexing a large corpus with the original
  GraphRAG design cost on the order of $33,000 in early 2024. LazyGraphRAG indexes at the same
  cost as vector RAG, around 0.1% of full GraphRAG, and matches or beats its global search quality
  at more than 700 times lower query cost. The constraint has moved to ongoing maintenance.
- **Put a freshness signal on every node.** If an agent can see when a fact was last confirmed, a
  prompt can at least instruct it to distrust old ones. This is a weak control, but it is better
  than the current default of presenting five-month-old and five-minute-old facts identically.

## 8. Traceability, audit and the regulated case

This is where the graph argument is strongest for a firm that has to defend its software
afterwards, and it is a direct extension of [ai-dlc.md](ai-dlc.md) section 8.3.

- **The questions audit asks are graph queries.** Which requirement produced this code, who
  approved it, was it generated or written, and what else did that decision touch. A timestamped
  markdown file records that a decision happened. It does not answer any of those questions
  without a person reading the whole trail.
- **Traceability can be made structural rather than documentary.** ReqToCode (2026) proposes
  generating language-native code elements, called Traceables, from requirements: enums, constants
  and typed definitions that code references as ordinary dependencies. A broken trace becomes a
  broken build, coverage is computable at any revision by static analysis, requirements move
  through an explicit active, deprecated and removed lifecycle so teams get warnings before
  enforcement, and traces are branch-scoped so parallel work does not collide. The same
  verification applies to generated and hand-written code, which is precisely the distinction
  auditors care about. It therefore functions as a control, whereas AI-DLC's audit file functions
  only as a record.
- **The regulatory timing is close.** The EU AI Act's high-risk obligations under Annexes I and II
  take effect on 2 August 2026, and the practitioner guidance being published for AI-generated
  code emphasises attribution at file and repository level rather than a general statement that
  the organisation uses AI somewhere.
- **The elaboration output belongs in the graph.** Section 7.1 of [ai-dlc.md](ai-dlc.md) argues
  that the valuable part of the method is forcing folklore into the open. Writing that into prose
  specifications makes it unqueryable and leaves it to drift. Writing it into an ontology makes it
  reusable by every later session, checkable against the code, and defensible in review. For a
  client mandate and restriction engine, the precedence rules are the durable artifact; the
  specification document that described them is not.

## 9. Practical build order

1. **Start with the code graph.** It is cheap, mechanical, refreshes from source, and the benefit
   shows up immediately as fewer tokens and tool calls. LSP or SCIP if the tooling already exists,
   tree-sitter over MCP if not.
2. **Wire the work you already have** — tickets, pull requests, incidents, deploys, ownership,
   design documents — rather than authoring a new graph. Inherited freshness is the only property
   that survives two years.
3. **Take on the business ontology last and narrowly**, for the one domain where the rules are
   genuinely folklore, and build it from elaboration sessions that were going to happen anyway.
   AWS's ontology accelerator, or an equivalent, makes the first draft cheap; the review is the
   real work.
4. **Expose each of these as a separate tool** and let the agent choose, rather than merging them.
   This mirrors the routing advice in [agentic-ai.md](agentic-ai.md) section 6.
5. **Enforce entitlements at query time**, behind a gateway, because MCP provides none of that
   itself. An agent reading a context graph can reach across everything the graph connects.
6. **Measure tokens and tool calls per task** alongside delivery metrics. That is where the effect
   appears first, and it is the number that justified the work at the only organisation publishing
   results at scale.

## 10. Failure modes to watch for

- The graph becomes the only copy of a control, and nobody notices when it drifts from the system
  it was derived from.
- A one-off extraction is treated as done, and the maintenance pipeline is never built.
- Impact analysis is trusted because it is structured, on a graph that has not been refreshed
  since the last reorganisation of service ownership.
- Better context increases throughput into a review process that was already the constraint, which
  is the efficiency paradox in section 6.2.
- The ontology models the business as the modelling team understands it rather than as the desk
  actually operates, and is then cited as authoritative in a control conversation.
- Entitlements are enforced in the prompt rather than at retrieval, so the graph becomes a way to
  read across permission boundaries. See [ai-security.md](ai-security.md).

## Resources

- [Running a Software Factory Efficiently at Uber Scale](https://www.uber.com/us/en/blog/efficient-software-factory/) — the AI Context Graph, with scale and adoption figures. [Pragmatic Engineer's account](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development) adds context.
- [Atlassian opens up its Teamwork Graph](https://secure.businesswire.com/news/home/20260506556902/en/Atlassian-Opens-Up-Its-Teamwork-Graph-to-Power-Agentic-Work-Across-the-Enterprise) — Team '26, May 2026.
- [We're bringing governed agent loops to the AI-native SDLC](https://www.atlassian.com/blog/jira/governed-agent-loops) — Code Context, Agent Context Controls and the 94% / 6% claim.
- [Atlassian research coined the AI efficiency paradox; DX's Q2 data now finds it inside engineering](https://diginomica.com/atlassian-research-ai-efficiency-paradox-dx-q2-data-engineering) — the Developer Experience Index decline.
- [AWS Context](https://venturebeat.com/data/aws-enters-the-context-layer-race-with-a-graph-that-learns-from-agents-not-manual-curation) — the graph that learns from agent usage rather than manual curation.
- [Context Ontology Accelerator now generally available](https://aws.amazon.com/about-aws/whats-new/2026/07/aws-context--ontology-accelarator-generally-available/) — Apache 2.0, W3C standards, Neptune and MCP.
- [AIDLC Collaborative](https://aws-samples.github.io/sample-collaborative-ai-dlc/) — typed linked artifacts and a traceability graph over AI-DLC's output.
- [Kiro Code Intelligence and Knowledge Index](https://kiro.dev/changelog/cli/1-22/) and [KiroGraph](https://github.com/davide-desio-eleva/kirograph) — an index from the vendor, a graph from the community.
- [Sourcegraph: context engineering for AI agents](https://sourcegraph.com/blog/context-engineering) and [agentic coding for big code](https://sourcegraph.com/blog/agentic-coding).
- [RepoGraph](https://arxiv.org/abs/2410.14684) — repository-level code graph, the SWE-bench-Lite numbers.
- [Codebase-Memory](https://arxiv.org/html/2603.27277v1) — tree-sitter knowledge graphs over MCP, the token and latency measurements.
- [CORE-Bench](https://arxiv.org/pdf/2606.11864) — code retrieval compared across graph, embedding and agentic search.
- [ARISE](https://arxiv.org/pdf/2605.03117) — repository-level graphs for fault localisation and agentic repair.
- [STALE: can LLM agents know when their memories are no longer valid?](https://arxiv.org/abs/2605.06527) — Chao et al., 2026, the 55.2% result.
- [ReqToCode](https://arxiv.org/html/2603.13999) — requirements traceability as a compile-time property of the codebase.
- [Harness Engineering for Agentic AI Coding Tools](https://arxiv.org/pdf/2602.14690) — exploratory study of what practitioners actually build around agents.
- [LazyGraphRAG](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/) — the indexing and query cost change.
- [What auditors will ask about AI-generated code in 2026](https://blog.codacy.com/what-auditors-will-ask-about-ai-generated-code-in-2026) — file and repository level attribution.
