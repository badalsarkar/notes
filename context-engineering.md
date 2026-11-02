# Context Engineering for Agents and Enterprise Data

Research report, October 2026. Related notes: [agentic-ai.md](agentic-ai.md),
[sdlc-context-graph.md](sdlc-context-graph.md), [genai-architecture.md](genai-architecture.md),
[ai-security.md](ai-security.md), [ai-dlc.md](ai-dlc.md),
[coding-agents-in-large-codebases.md](coding-agents-in-large-codebases.md).

## Contents

- [1. What this report covers](#1-what-this-report-covers)
- [2. Summary](#2-summary)
- [3. Definitions and the evidence for keeping context small](#3-definitions-and-the-evidence-for-keeping-context-small)
  - [3.1 What context engineering means](#31-what-context-engineering-means)
  - [3.2 Measured evidence on long-context degradation](#32-measured-evidence-on-long-context-degradation)
  - [3.3 Named failure modes](#33-named-failure-modes)
- [4. Techniques inside the agent](#4-techniques-inside-the-agent)
  - [4.0 How the options are compared](#40-how-the-options-are-compared)
  - [4.1 Observation masking and tool-result clearing](#41-observation-masking-and-tool-result-clearing)
  - [4.2 Compaction and summarisation](#42-compaction-and-summarisation)
  - [4.3 Just-in-time retrieval](#43-just-in-time-retrieval)
  - [4.4 Structured notes, instruction files and Skills](#44-structured-notes-instruction-files-and-skills)
  - [4.5 Long-term memory systems](#45-long-term-memory-systems)
  - [4.6 Tool loadout, tool search and code execution](#46-tool-loadout-tool-search-and-code-execution)
  - [4.7 Sub-agents and context isolation](#47-sub-agents-and-context-isolation)
  - [4.8 Prompt and KV caching](#48-prompt-and-kv-caching)
  - [4.9 Side by side](#49-side-by-side)
- [5. Measuring context](#5-measuring-context)
- [6. The enterprise context layer](#6-the-enterprise-context-layer)
  - [6.1 What the term means](#61-what-the-term-means)
  - [6.2 Reference architecture](#62-reference-architecture)
  - [6.3 Semantic layers and metrics layers](#63-semantic-layers-and-metrics-layers)
  - [6.4 Ontologies and knowledge graphs](#64-ontologies-and-knowledge-graphs)
  - [6.5 Catalogs, lineage and usage-derived metadata](#65-catalogs-lineage-and-usage-derived-metadata)
  - [6.6 Permission-aware enterprise search](#66-permission-aware-enterprise-search)
  - [6.7 Decision traces and context graphs](#67-decision-traces-and-context-graphs)
  - [6.8 Side by side](#68-side-by-side)
- [7. Vendor platforms and standards](#7-vendor-platforms-and-standards)
  - [7.1 Four vendor families](#71-four-vendor-families)
  - [7.2 Interoperability standards](#72-interoperability-standards)
  - [7.3 Lock-in](#73-lock-in)
- [8. Governance and regulation in capital markets](#8-governance-and-regulation-in-capital-markets)
  - [8.1 Regulatory expectations](#81-regulatory-expectations)
  - [8.2 Information barriers, MNPI and entitlements](#82-information-barriers-mnpi-and-entitlements)
  - [8.3 What banks have published](#83-what-banks-have-published)
- [9. Worked capital markets scenarios](#9-worked-capital-markets-scenarios)
- [10. Practical build order](#10-practical-build-order)
- [11. Failure modes to watch for](#11-failure-modes-to-watch-for)
- [12. Open questions and gaps in the evidence](#12-open-questions-and-gaps-in-the-evidence)
- [Resources](#resources)

## 1. What this report covers

An agent can only use what is in its context window on a given call, and everything else it knows
comes from its weights. Context engineering is the work of deciding which tokens reach the model at
each step, and it has two halves that are usually discussed separately. The first half happens
inside the agent: how instructions, tool definitions, tool results, history and memory are selected,
compressed and arranged during a long task. The second half happens inside the organisation: how
business meaning, provenance, permissions and accumulated knowledge about the firm's data are made
available to agents in a governed way, which vendors and analysts now call a context layer.

This report covers both halves. For the agent side, it compares the main techniques (observation
masking, compaction, just-in-time retrieval, file-based and long-term memory, tool search and code
execution, sub-agents and prompt caching) on the same structure: how each works, its strengths, its
weaknesses, its cost, and a capital markets example of where it fits and where it does not. For the
enterprise side, it compares semantic layers, ontologies and knowledge graphs, catalogs and usage
metadata, permission-aware enterprise search and the vendor platforms that package them, and then
covers the governance and regulatory expectations that apply in financial services.

It does not repeat material covered elsewhere. [agentic-ai.md](agentic-ai.md) covers vector RAG,
hybrid search, agentic file search, GraphRAG, temporal knowledge graphs, ontologies and semantic
layers as retrieval methods, with its section 3.7 describing the ontology pattern and its section 5
giving retrieval scenarios. [sdlc-context-graph.md](sdlc-context-graph.md) covers code graphs and
work graphs for software delivery, including how such graphs go stale. Those topics are recapped
here only where a sentence of background is needed to make a comparison.

Most of the numbers in this field come from the organisations that sell the technique being
measured. The report labels figures as measured when they come from a published evaluation with a
stated method, and as vendor claims when they come from an internal evaluation without independent
replication. Analyst figures attributed to Gartner reached this research second-hand, through vendor
blogs and conference recaps, and are labelled as forecasts.

## 2. Summary

The central finding on the agent side is that model accuracy falls as the context grows, well before
the advertised window is full, so the main design goal is to keep the working context small and high
in signal. Independent benchmarks (RULER, NoLiMa, the Databricks long-context RAG study and Chroma's
context rot report) place the first significant drop for many 2024 and 2025 models at around 32,000
tokens. Anthropic's guiding principle, to find "the smallest possible set of high-signal tokens that
maximize the likelihood of some desired outcome", follows from that evidence rather than from taste.

The techniques that achieve this are now fairly stable. The cheapest and best-evidenced is
observation masking, which replaces old tool outputs with placeholders, and the one peer-reviewed
comparison found it roughly halved cost and matched LLM summarisation on solve rate. Summarisation,
memory products, sub-agents and code execution all add capability for specific situations, and each
brings a cost, either in extra model calls, in opacity, in tokens or in infrastructure. Prompt
caching is the largest single cost lever for agents, because agents read far more than they write,
but it rewards an append-only context and so conflicts with any technique that rewrites earlier
messages. A team has to choose its compression strategy and its caching strategy together.

The central finding on the enterprise side is that agents fail on enterprise data mainly because the
meaning of the data is missing, and that model capability is the smaller constraint. Two
near-identical tables can differ in whether they include logged-out users, a revenue question can
match two competing "authoritative" tables, and a schema alone cannot tell an agent which one
finance uses. The organisations that have published working systems (OpenAI, LinkedIn, Uber,
Pinterest, BlackRock) all solve this the same way. They rank and annotate tables using query logs
and owner input, narrow the schema and the tool set before the model sees them, enforce permissions
at retrieval time, and keep a human confirmation step. Their reported production accuracy is
moderate, with LinkedIn reporting 53% correct or nearly correct on an internal benchmark.

A semantic layer gives the most reliable answers within the scope that has been modelled, and its
most useful property for regulated work is that it fails visibly by refusing rather than returning a
plausible wrong number. Outside that scope it answers nothing, so the recommended pattern is a
router that tries the semantic layer first and falls back to governed text-to-SQL. Ontologies add
typed entities and governed write actions, which matter once agents do more than read. Every vendor
now exposes its context over MCP, so MCP access no longer distinguishes products, and the
differences lie in the depth of the semantics, the permission model and the degree of lock-in.

In capital markets the context layer is also a control. Information barriers, MNPI handling and
licensed-data entitlements require that permissions are enforced before content enters the context,
that agents retrieve with the user's identity rather than a shared service account, and that the
retrieved context is logged alongside the prompt so that an agent's decision can be reconstructed.
FINRA's 2026 oversight report names these concerns directly.

## 3. Definitions and the evidence for keeping context small

### 3.1 What context engineering means

The term became common in June 2025. Tobi Lutke described it as "the art of providing all the
context for the task to be plausibly solvable by the LLM", and Andrej Karpathy called it "the
delicate art and science of filling the context window with just the right information for the next
step" ([Simon Willison](https://simonwillison.net/2025/jun/27/context-engineering/)). Anthropic
defines context as "the set of tokens included when sampling from an LLM" and context engineering as
"curating and maintaining the optimal set of tokens (information) during LLM inference", with prompt
engineering as the part of it that writes the instructions ([Anthropic, Effective context
engineering for AI
agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

Google's ADK team frames the same idea as a compiler problem. Sessions, memory and artifacts are
source state, an ordered pipeline of named processors compiles them, and the working context is the
per-call view sent to the model, with the rule that "every model call and sub-agent sees the minimum
context required" ([Google Developers
Blog](https://developers.googleblog.com/en/architecting-efficient-context-aware-multi-agent-framework-for-production/)).
The value of this framing is that it separates storage from presentation, so the full record can be
kept while the model sees only a scoped view of it. Google reports no benchmark numbers for the
design.

LangChain groups the techniques into four operations, which are useful as a vocabulary for the rest
of this report ([LangChain, Context Engineering for
Agents](https://www.langchain.com/blog/context-engineering-for-agents)). Write means saving
information outside the window, such as notes or memory. Select means pulling relevant information
into the window, such as retrieval or loading an instruction file. Compress means keeping only the
tokens the task needs, such as summarisation or trimming. Isolate means splitting work across
separate windows, such as sub-agents or a sandbox that holds large objects as variables.

By late 2026 the discussion had moved towards what Drew Breunig calls harness engineering, meaning
the design of the scaffold, orchestration and tooling around the model, with models increasingly
trained to manage their own context through tools such as memory files, compaction and sub-agents
([Breunig, The State of Context
Engineering](https://www.dbreunig.com/2026/10/24/the-state-of-context-engineering.html)). The
tactics have not changed much since mid-2025, but more of them are now applied by the model rather
than by deterministic code in the harness.

### 3.2 Measured evidence on long-context degradation

The case for keeping context small rests on several independent measurements, and they agree in
direction even though they differ in method.

The "Lost in the Middle" study found that question-answering performance is highest when the
relevant information is at the beginning or end of the input and drops when it sits in the middle,
including in models built for long contexts ([arXiv 2307.03172](https://arxiv.org/abs/2307.03172)).
RULER tested 17 long-context models on 13 tasks covering retrieval, multi-hop tracing and
aggregation, and found that although all claimed 32,000 tokens or more, only half maintained
satisfactory performance at 32,000 ([arXiv 2404.06654](https://arxiv.org/abs/2404.06654)). The
Databricks long-context RAG study ran more than 2,000 experiments on 13 models and found that
Llama-3.1-405b began to decline at about 32,000 tokens and GPT-4-0125-preview at about 64,000
([Databricks](https://www.databricks.com/blog/long-context-rag-performance-llms)). NoLiMa removed
the lexical overlap between the question and the answer, so the model had to infer the link, and
found that 11 of 13 models claiming at least 128,000 tokens fell below half their short-context
score at 32,000, with GPT-4o falling from 99.3% to 69.7% ([arXiv
2502.05167](https://arxiv.org/abs/2502.05167)).

Chroma's context rot report tested 18 models from four providers and is the most directly relevant
to agent design ([Chroma Research](https://www.trychroma.com/research/context-rot)). Even a single
topically related distractor reduced accuracy, and the effect differed by provider, with Claude
models tending to abstain and GPT models producing the most confident hallucinations. On
LongMemEval, focused prompts of about 300 tokens scored significantly higher than full prompts of
about 113,000 tokens for every model tested. The authors concluded that how information is presented
matters as much as whether it is present.

The top frontier models have narrowed the gap on some tasks, and o3 was reported at 100% on
Fiction.LiveBench at 128,000 tokens in 2025 ([The
Decoder](https://the-decoder.com/openais-o3-achieves-near-perfect-performance-on-long-context-benchmark/)).
No source found in this research shows that degradation has disappeared, and no 2026 replication of
the Chroma study on current-generation models was found. Breunig's practical rule of thumb is to
start resetting context at about 200,000 tokens, which is a practitioner heuristic rather than a
measurement ([Breunig,
2026](https://www.dbreunig.com/2026/10/24/the-state-of-context-engineering.html)).

Anthropic's explanation is that attention relationships grow quadratically with length and that
training data is dominated by shorter sequences, so the model's attention is "stretched thin" as
context grows, producing a gradient rather than a cliff
([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
This is a vendor explanation rather than a measured result, but it is consistent with the
benchmarks.

### 3.3 Named failure modes

Breunig's June 2025 taxonomy gives names to the ways a context goes wrong, and each name points to a
mitigation ([Breunig, How Long Contexts
Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html); [How to Fix
Your Context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html)).

| Failure mode | What happens | Measured or reported example | Mitigation |
|---|---|---|---|
| Poisoning | An error enters the context and is referenced repeatedly. | A Gemini 2.5 Pokémon agent pursued impossible goals after its goals section was corrupted. | Validation, pruning, quarantine. |
| Distraction | The model over-focuses on a long history and neglects its training. | The same agent repeated past actions beyond about 100,000 tokens. | Compaction, resets. |
| Confusion | Superfluous content, often too many tools, degrades the answer. | A quantised Llama 3.1 8b failed with 46 tools and succeeded with 19, both well inside its window (measured). | Tool loadout, retrieval. |
| Clash | New information conflicts with earlier content. | Splitting prompts across turns caused an average 39% drop, with o3 falling from 98.1 to 64.1 (measured). | Pruning stale turns, isolation. |
| Inertia | The model keeps pursuing a hypothesis after it should stop. | Agents with forgetting outperformed agents without it on AHC014 (measured, cited by Breunig). | Periodic resets, planned forgetting. |
| Fighting the weights | The instruction works against what the model was trained to do. | Repeated capitalised pleas for parallel tool calls in a system prompt. | Change the harness rather than the wording. |

The last two were added in October 2026 ([Context
Inertia](https://www.dbreunig.com/2026/10/14/context-inertia.html); [Don't Fight the
Weights](https://www.dbreunig.com/2025/11/11/don-t-fight-the-weights.html)). Breunig expects
long-running agents to accumulate conflicting memories and skills and regards strategic forgetting
as an unsolved problem.

There is an apparent tension between Manus's advice to keep failed actions in context and the
poisoning evidence, which suggests removing wrong content. Both hold when the distinction is drawn
carefully. A recorded failure with its error message helps the model avoid repeating a mistake,
while an unflagged wrong conclusion presented as fact poisons later reasoning.

## 4. Techniques inside the agent

### 4.0 How the options are compared

Each technique below is described under the same five headings, followed by a capital markets case
where it fits and a case where it does not. Section 4.9 puts them side by side. Prompt structure is
treated briefly first, because it underlies all of them.

Anthropic's guidance for system prompts is to write at the "right altitude", which sits between
hard-coded if-then logic that makes the agent brittle and vague guidance that assumes shared context
the model does not have
([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). It
recommends starting with a minimal prompt on the best available model and adding instructions and
examples only in response to observed failures, using a small set of diverse, canonical examples
rather than a long list of edge-case rules. Minimal here refers to signal density, not length.
OpenAI's data agent team reported the same lesson from production, where prescriptive step-by-step
prompts produced worse answers than stating the goal ([ByteByteGo
summary](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)). This guidance is
qualitative, and no controlled study of prompt altitude was found.

### 4.1 Observation masking and tool-result clearing

**How it works.** Old tool outputs are removed from the history and replaced with a short
placeholder, while the agent's own reasoning and actions are kept. In the JetBrains study the agent
kept the last ten turns verbatim and masked observations older than that ([arXiv
2508.21433](https://arxiv.org/abs/2508.21433)). Anthropic calls tool-result clearing "one of the
lightest forms of compaction" and offers it as an API feature, context editing, which clears stale
tool calls and results as the conversation approaches its token limit ([Claude blog, context
management](https://claude.com/blog/context-management)). Manus makes the removal restorable by
keeping the URL or file path in place of the content, so the agent can fetch it again if needed
([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).

**Strengths.** It is deterministic, adds no model call and no latency, and cannot introduce a
hallucinated fact, because it only removes content. It has the strongest independent evidence of any
technique in this report. On SWE-bench Verified across five model configurations, masking roughly
halved cost relative to the unmanaged agent and matched or slightly exceeded LLM summarisation on
solve rate (measured). For Qwen3-Coder 480B, the raw agent solved 53.4% at $1.29 per instance,
masking solved 54.8% at $0.61, and summarisation solved 53.8% at $0.64 ([arXiv
2508.21433v3](https://arxiv.org/html/2508.21433v3)).

**Weaknesses.** The benefit depends on the model and the agent framework. Gemini 2.5 Flash in
thinking mode lost solve rate under masking, falling from 40.4% to 36.4%, and on OpenHands the
masking window had to be retuned before masking matched summarisation (measured). A masked
observation is gone unless the agent kept a handle to it, so constraints that appeared only in a
tool result can be lost. Any rewrite of earlier messages also invalidates the prompt cache from that
point onwards (see section 4.8).

**Cost.** The engineering cost is low, since it is a filter over the message list or an API flag.
The runtime cost is negative, because it reduces input tokens on every subsequent turn. Anthropic
reports that context editing cut token consumption by 84% on a 100-turn web search evaluation and
allowed agents to finish workflows that otherwise failed from context exhaustion, which is a vendor
claim from an internal evaluation ([Claude blog](https://claude.com/blog/context-management)).

**Capital markets example where it fits.** A settlement-break investigation agent works through a
failed trade by pulling custodian status messages, standing settlement instructions, the
confirmation and the counterparty's affirmation history. Most of these outputs are bulky and are
only needed for the step that read them. Masking them after use, while keeping the message
references and a one-line note of what each showed, keeps the window small across a long
investigation, and the agent can re-fetch a message by its reference if a later step needs it.

**Where it does not fit.** A trade surveillance analyst agent that is assembling a case file for a
spoofing alert needs to quote the specific orders, cancellations and communications it reviewed
earlier. If those raw observations are masked without restorable references, the agent will
summarise evidence from memory, which is the opposite of what a case file requires. In that workflow
the evidence should be written to a case store as it is read, and masking applied only to
observations that are already recorded there.

### 4.2 Compaction and summarisation

**How it works.** When the window nears its limit, a model summarises the history and a new window
starts from that summary. Claude Code's compaction keeps architectural decisions, unresolved bugs
and implementation details, discards redundant tool outputs, and continues with the five most
recently accessed files
([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
LangChain reported in July 2025 that Claude Code auto-compacted at 95% of the window
([LangChain](https://www.langchain.com/blog/context-engineering-for-agents)), and no current
official threshold was found. The OpenAI Agents SDK offers two session strategies, one that trims to
the last N turns and one that summarises older turns into a synthetic pair while keeping the last
few verbatim ([OpenAI Cookbook, Session
memory](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory)). Cognition uses
a dedicated, fine-tuned compression model at agent handoffs and describes the task as "hard to get
right" ([Cognition, Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents)).

A related practice is the full context reset, in which the agent writes notes to durable storage and
the window is then cleared while the environment persists. Breunig describes an Anthropic setup in
which the agent writes notes about every 90 minutes before the context is cleared ([Breunig,
2026](https://www.dbreunig.com/2026/10/24/the-state-of-context-engineering.html)). Resetting differs
from compaction in that the agent chooses what to write down, rather than a summariser choosing what
to keep.

**Strengths.** Summarisation preserves long-range decisions and constraints that trimming would drop
abruptly, and it lets a task continue past the size of one window. A tuned hybrid of masking and
occasional summarisation on Qwen3-Coder 480B reached a solve rate 2.6 points above the raw agent at
7% lower cost than masking alone (measured, [arXiv
2508.21433v3](https://arxiv.org/html/2508.21433v3)).

**Weaknesses.** A summary can carry an incorrect fact forward, which the OpenAI cookbook calls
context poisoning, and it can drift or misweight details over repeated rounds ([OpenAI
Cookbook](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory)). In the
JetBrains study, summarisation lengthened trajectories, with Gemini 2.5 Flash summary runs averaging
52 turns against 44 for masking, and the authors attribute this to summaries hiding the signals that
would otherwise tell the agent to stop (measured). With untuned settings the hybrid was less
cost-efficient than masking alone. Summaries also make debugging harder, because the summary prompts
and outputs have to be logged before drift can be investigated.

**Cost.** Each summarisation is an extra model call, which accounted for between 0.65% and 7.20% of
per-instance cost in the JetBrains study, plus the cost of the longer trajectories it caused.
Summarisation also rewrites history, so it forfeits cached-read discounts on everything after the
rewritten point.

**Capital markets example where it fits.** A sector research agent works through a quarter's
earnings-call transcripts for thirty issuers and builds a thesis over several hours. The individual
transcript passages matter less as the work progresses than the conclusions drawn from them, such as
which issuers guided margins down and which cited the same supplier. Compaction that keeps those
conclusions and drops the raw passages fits the task, provided the agent has also written its
findings to a notes file that does not depend on the summariser.

**Where it does not fit.** A portfolio rebalancing agent operating under a client mandate must
respect restrictions such as an exclusion list, a maximum issuer weight and a prohibition on a
specific sector. If those restrictions entered the context through an early tool call and are later
summarised, a single dropped clause produces a breach. Hard constraints of this kind should be
pinned in the system prompt or re-read from the mandate store at each decision point, so that they
never depend on a summary being faithful.

### 4.3 Just-in-time retrieval

**How it works.** Instead of retrieving content before inference and placing it in the prompt, the
agent holds lightweight identifiers such as file paths, stored queries and links, and loads data
through tools when it needs it
([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
Claude Code is a hybrid, loading `CLAUDE.md` up front and using glob and grep for everything else.
Cline deliberately does not index codebases, arguing that chunking breaks code logic and that an
index is a second copy of the code that widens the security surface
([Cline](https://cline.bot/blog/why-cline-doesnt-index-your-codebase-and-why-thats-a-good-thing)).
The retrieval methods themselves, including agentic file search and hybrid search, are compared in
[agentic-ai.md](agentic-ai.md) sections 3.2 and 3.3.

**Strengths.** Only what the current step needs enters the window, which follows directly from the
degradation evidence in section 3.2. There is no index to maintain, so there are no stale embeddings
in fast-changing content, and no secondary copy of sensitive data.

**Weaknesses.** Each lookup costs turns and tokens, and the agent must know or guess what to search
for. Exact-match tools such as grep are weak on paraphrase-heavy prose. Cursor reports that adding
its own semantic search alongside grep gave on average 12.5% higher accuracy on its internal
benchmark, which is a vendor claim ([Cursor](https://cursor.com/blog/semsearch)). No independent
benchmark comparing agentic search, vector retrieval and a hybrid on the same tasks with cost and
latency was found.

**Cost.** There is no build or index cost. The runtime cost is higher per question than a single
retrieval call, because the agent explores in several steps.

**Capital markets example where it fits.** A post-trade exception agent handles one break at a time.
The relevant records (the trade, its allocations, the confirmation, the custodian message and the
SSI) are known in advance and identified by keys. The agent can hold the trade ID and fetch each
record as it needs it, with no index required.

**Where it does not fit.** An analyst asks which issuers in a coverage universe have discussed
supply-chain exposure to a particular region over the last five years of filings. The agent does not
know which documents or terms to search for, and grep over thousands of filings will miss
paraphrases. This question needs an index with hybrid retrieval, as described in
[agentic-ai.md](agentic-ai.md) section 5, with just-in-time loading reserved for opening the
specific documents the index returns.

### 4.4 Structured notes, instruction files and Skills

**How it works.** The agent writes its plan, progress and findings to files outside the window and
reads them back when needed. Manus has the agent continually rewrite a `todo.md` file so that the
current goals sit in the most recent part of the context, which counters goal drift over a typical
task of about 50 tool calls
([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
Anthropic's Pokémon-playing agent kept maps, progress counts and combat notes that survived context
resets across thousands of steps
([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
Anthropic's memory tool gives the model create, read, update and delete operations over a
client-side memory directory, so the developer controls where the data lives ([Claude
blog](https://claude.com/blog/context-management)). Instruction files such as `CLAUDE.md` and
`AGENTS.md` are the static form of this, and Agent Skills add progressive disclosure, in which only
a skill's name and description are loaded at start-up, the full `SKILL.md` is read when the skill is
judged relevant, and linked files are read only when needed ([Anthropic, Agent
Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)).

**Strengths.** File-based memory is transparent and auditable, because a person can read and correct
exactly what the agent will see. It makes compression restorable and survives resets. Progressive
disclosure allows a large library of procedures to be available while costing only a line per skill
until one is used. Anthropic reports that memory plus context editing improved an internal agentic
search evaluation by 39% over baseline, which is a vendor claim ([Claude
blog](https://claude.com/blog/context-management)).

**Weaknesses.** Static instruction files need manual curation and go stale. A search result
attributed a 2026 study to Gloaguen et al. reporting that LLM-generated context files lowered task
success while raising cost, but the primary paper was not found, so that claim is unverified.
Breunig reports an enterprise team loading 600 skills per engineer, which turns progressive
disclosure back into a tool-loadout problem ([Breunig,
2026](https://www.dbreunig.com/2026/10/24/the-state-of-context-engineering.html)). Anthropic warns
that malicious skills can exfiltrate data and should be installed only from trusted sources. No
controlled study quantifies the benefit of todo recitation.

**Cost.** The engineering cost is low. The ongoing cost is human curation time for instruction files
and skills, which scales with the number of teams and procedures.

**Capital markets example where it fits.** A risk technology team maintains a skill that describes
how to produce the daily VaR back-testing exception report, including which data sources are
authoritative, which adjustments are permitted and how exceptions are classified. The procedure
changes rarely, it is reviewed by the team that owns it, and it is loaded only when an agent is
asked for that report.

**Where it does not fit.** Client restrictions that change daily, such as a newly added
restricted-list entry following a wall-crossing, should not live in an instruction file or skill. A
static file will be out of date between edits, and the authoritative source is the compliance
system, which the agent should query at the point of decision.

### 4.5 Long-term memory systems

**How it works.** A memory service extracts facts from conversations, stores them in a vector store,
a graph or both, and retrieves the relevant ones into later sessions instead of replaying full
history. Mem0 uses extracted memories with an optional graph variant ([arXiv
2504.19413](https://arxiv.org/abs/2504.19413)). Zep's engine, Graphiti, is a temporally aware
knowledge graph that records when facts became true and stopped being true ([arXiv
2501.13956](https://arxiv.org/abs/2501.13956)). Temporal graph memory as a retrieval method is
covered in [agentic-ai.md](agentic-ai.md) section 3.6.

**Strengths.** It solves the same problem as compaction at the cross-session level, and it can
recall a preference stated weeks earlier without carrying the whole history. Mem0 reports a median
response time of 0.708 seconds against 9.870 seconds for a full-context baseline sending about
26,000 tokens per call, and more than 90% token-cost savings. Zep reports 94.8% against MemGPT's
93.4% on Deep Memory Retrieval and up to 18.5% higher accuracy on LongMemEval. All of these are
figures from vendor-authored papers.

**Weaknesses.** The headline savings are measured against full-context replay, which is the weakest
possible comparator, and each paper chooses its own baselines and benchmark, so the results do not
form a leaderboard. No independent benchmark evaluating Mem0, Zep and Letta under identical
conditions was found. Recall is probabilistic and opaque, so a wrong or outdated memory can be
retrieved with no indication that it is wrong, and bad facts persist until something removes them.
Memory that is shared across users is a leakage channel. OpenAI's data agent scopes corrections
globally or personally ([OpenAI](https://openai.com/index/inside-our-in-house-data-agent/)), and a
global scope crosses users unless writes are reviewed or scoped by entitlement.

**Cost.** It adds a stateful service to operate, an extraction model call per conversation, and
storage, in exchange for lower per-call token counts.

**Capital markets example where it fits.** A client coverage assistant for a salesperson remembers
that a particular pension fund client prefers a weekly summary rather than daily calls, follows
emerging-market credit and dislikes long documents. These are soft preferences, an occasional recall
error is low-cost, and the memory is scoped to the salesperson's own book.

**Where it does not fit.** A memory system should not be the record of a client's investment
restrictions or of who has been wall-crossed on a deal. A probabilistic recall layer is not an
acceptable control for either, and a memory written while a banker was on the private side of an
information barrier could later be retrieved for a public-side user if scoping is wrong. Those facts
belong in systems of record that the agent queries with the user's entitlements.

### 4.6 Tool loadout, tool search and code execution

**How it works.** There are two separate problems with tools, and each has its own remedy. The first
is that tool definitions consume context before any work starts. Anthropic measured a five-server
MCP setup at 58 tools costing about 55,000 tokens, with GitHub alone at about 26,000 tokens for 35
tools ([Anthropic, advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)).
Tool search addresses this by deferring definitions until the agent searches for a tool it needs.
The second problem is that tool results consume context, and code execution addresses it by letting
the agent write code against tools so that intermediate results stay in the execution environment
and only filtered output reaches the model ([Anthropic, Code execution with
MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)). Cloudflare's Code Mode
converts an MCP server's schema into a TypeScript API and runs agent-written code in an isolate with
no internet access, routing calls through bindings so that the code never handles API keys
([Cloudflare](https://blog.cloudflare.com/code-mode/)). Manus takes a third approach and keeps all
tool definitions in place while constraining which tools can be chosen by masking token logits
through a state machine, which avoids invalidating the cache
([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).

**Strengths.** Fewer visible tools reduce confusion as well as cost. The measured evidence on tool
count is consistent: in the RAG-MCP study with DeepSeek-v3, tool descriptions began to overlap above
30 tools and the model almost always failed above 100, while retrieving fewer than 30 tools tripled
selection accuracy ([Breunig
summary](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html)). Anthropic reports that
tool search cut context use from about 77,000 to about 8,700 tokens and raised accuracy with large
tool libraries from 49% to 74% for Opus 4, and that its code-execution example dropped from about
150,000 tokens to about 2,000. These are vendor claims, and the first reduction, described as 85%,
is closer to 89% by the published figures. Production teams report the same ceiling. BlackRock
narrows thousands of Aladdin Copilot tools to about 20 to 30 per query because planning degraded
beyond about 40 to 50 ([ZenML summary of BlackRock
talk](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)),
and OpenAI cut its data agent from about 40 tools to 13 after overlapping tools produced conflicting
answers ([ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)).

**Weaknesses.** Tool search adds a retrieval step that can miss the right tool, and loading
definitions mid-task changes the context prefix. Tool definitions sit at the front of the cache
prefix, so rewriting the tool list invalidates the whole cache, and deferred definitions must be
appended rather than inserted. Code execution requires a sandbox with resource limits and
monitoring, which adds operational and security overhead that direct tool calls avoid. Cloudflare
published no quantitative results, and Code Mode still loads the full TypeScript API into context.
Tool descriptions are also an attack surface, because a poisoned description loads into context at
initialisation and persists across sessions
([Speakeasy](https://www.speakeasy.com/resources/mcp-tool-poisoning)).

**Cost.** Tool search is a moderate engineering cost and is now an API feature. Code execution is a
higher cost, because it requires an approved, monitored sandbox, which in a bank means a technology
risk review.

**Capital markets example where it fits.** An agent asked to find all positions where a
counterparty's exposure exceeds its limit after a downgrade can call a positions API that returns
200,000 rows. With code execution, the agent writes a filter that joins positions to limits and
returns the twelve breaches, and only those twelve rows enter the context. Without it, the full
result either floods the window or has to be truncated arbitrarily.

**Where it does not fit.** A narrow agent with eight well-designed tools, such as one that drafts
trade confirmations, gains nothing from tool search, which would add latency and a retrieval failure
mode. Code execution is also a poor fit where the firm cannot approve a sandbox for agent-written
code against production data, in which case narrower tools that return pre-filtered, token-efficient
results are the alternative.

### 4.7 Sub-agents and context isolation

**How it works.** A lead agent delegates sub-tasks to sub-agents, each with a clean window. A
sub-agent may spend tens of thousands of tokens exploring and returns a condensed summary of often
1,000 to 2,000 tokens
([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

**Strengths.** It keeps investigative work out of the main agent's history and lets read-heavy work
run in parallel. Anthropic reports that a lead Opus 4 agent with Sonnet 4 sub-agents outperformed
single-agent Opus 4 by 90.2% on an internal research evaluation, which is a vendor claim
([Anthropic, multi-agent research
system](https://www.anthropic.com/engineering/multi-agent-research-system)).

**Weaknesses.** The same post reports that agents use about four times the tokens of chat and
multi-agent systems about fifteen times, and that token usage alone explained about 80% of
performance variance on BrowseComp. Anthropic concludes that multi-agent systems "work mainly
because they help spend enough tokens to solve the problem", so the 90.2% gain should be read as the
effect of spending more tokens in parallel. Sub-agents also lose shared context. Cognition's
principles are to "share context, and share full agent traces, not just individual messages" and
that "actions carry implicit decisions", illustrated by two sub-agents that built a Mario-style
background and a mismatched bird for the same Flappy Bird task
([Cognition](https://cognition.com/blog/dont-build-multi-agents)). Anthropic itself states that
multi-agent designs fit poorly when agents need the same context or have many dependencies,
including most coding tasks.

**Cost.** Token spend rises by roughly an order of magnitude over a single agent, according to
Anthropic's own figures. The two positions are compatible: isolation helps for parallel, read-only
exploration that returns a summary, and hurts for write-heavy work where sub-agents make conflicting
decisions.

**Capital markets example where it fits.** A credit analyst asks for a comparison of covenant terms
and refinancing risk across thirty high-yield issuers. Each issuer's filings and transcripts can be
read by a separate sub-agent that returns a fixed-format summary, and the lead agent compares the
summaries. The sub-tasks are independent and read-only, and the extra token spend buys coverage.

**Where it does not fit.** Repairing a misbooked trade involves amending the trade, re-allocating it
across funds and re-issuing the confirmation. Each step depends on decisions made in the previous
one, such as which allocation method applies, so splitting the work across sub-agents produces the
conflicting-decision failure that Cognition describes. A single agent with full context should do
this work.

### 4.8 Prompt and KV caching

**How it works.** Providers cache the processed prefix of a prompt and charge much less to reuse it.
Anthropic charges 1.25 times base input for a five-minute cache write and 2 times for a one-hour
write, and 0.1 times for reads on most models, with up to four breakpoints and a prefix order of
tools, then system, then messages ([Claude docs, Prompt
caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)). OpenAI caches
prefixes of at least 1,024 tokens automatically, with discounts on cached input of up to 95%, and
for GPT-5.6 and later charges a write premium ([OpenAI
docs](https://developers.openai.com/api/docs/guides/prompt-caching)). Gemini implicit caching is on
by default for 2.5 and newer models ([Google](https://ai.google.dev/gemini-api/docs/caching)).
Pricing details were current at 26 October 2026 and change often.

**Strengths.** Manus calls KV-cache hit rate "the single most important metric for a
production-stage AI agent", because its agents have an input-to-output ratio of about 100 to 1 and
cached input on Claude Sonnet cost a tenth of uncached input
([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)).
Because agents re-read their whole history on every turn, caching reduces cost on almost every call
without changing what the model sees.

**Weaknesses.** It works only if the prefix is stable and the context is append-only. A
second-precision timestamp at the start of the system prompt, non-deterministic JSON key order or a
change to the tool list each invalidates the cache. This conflicts with masking, summarisation and
dynamic tool loading, all of which rewrite earlier content. The MCP revision of 28 July 2026 asks
servers to return `tools/list` in deterministic order for this reason ([MCP changelog
2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)). Cache lifetimes
are short, so low-volume workloads pay the write premium without enough reads to recover it.

**Cost.** The engineering cost is the discipline of prompt layout, and the runtime effect is a large
reduction in input cost when hit rates are high. Teams can confirm hits through the
`cache_creation_input_tokens` and `cache_read_input_tokens` fields on each Anthropic response.

**Capital markets example where it fits.** A surveillance triage agent reviews hundreds of alerts a
day against the same long prefix containing the firm's market abuse policy, the alert typology
definitions and the tool definitions. Each alert is appended after the stable prefix, so almost
every call reads the policy from cache.

**Where it does not fit.** An agent that places per-user entitlement data or the current timestamp
at the top of its system prompt, or that is used only a few times an hour, will see few cache hits.
In the first case the fix is to move variable content after the cached prefix. In the second case
the write premium can make caching more expensive than not caching.

### 4.9 Side by side

| Technique | LangChain operation | Main benefit | Main weakness | Runtime cost effect | Evidence quality |
|---|---|---|---|---|---|
| Observation masking | Compress | Halves cost with no loss of solve rate in one study | Model-dependent; drops unreferenced constraints | Large saving | Measured, peer-review style (JetBrains) |
| Compaction and summarisation | Compress | Keeps long-range decisions | Poisoning, drift, longer runs, cache loss | Saving, minus summariser calls | Measured (JetBrains) plus vendor claims |
| Just-in-time retrieval | Select | Only current-step data enters context | More turns; weak on paraphrase | Higher per question, no index | Vendor and practitioner reports |
| Notes, instruction files, Skills | Write, Select | Transparent, auditable, restorable | Manual curation; staleness; skill sprawl | Low | Vendor claims and anecdotes |
| Long-term memory services | Write, Select | Cross-session recall | Opaque recall; persistent bad facts; leakage | Saving against full replay | Vendor-authored papers only |
| Tool search | Select | Fewer definitions in context | Retrieval miss; cache churn | Saving | Vendor claims plus measured tool-count studies |
| Code execution | Isolate | Large results never enter context | Sandbox and security overhead | Large saving on data-heavy tasks | Vendor claims |
| Sub-agents | Isolate | Parallel read-heavy coverage | About 15 times the tokens; conflicting decisions | Large increase | Vendor claim (internal evaluation) |
| Prompt caching | (Layout) | Cuts input cost on every turn | Requires stable, append-only prefix | Large saving at high hit rates | Published pricing |

The practical reading of this table is that masking and caching should be the defaults, because they
are cheap and well supported, and that the other techniques should be added when a specific failure
appears. The main interaction to design for is between compression and caching, since every
technique that rewrites history gives up cached reads after the rewrite.

## 5. Measuring context

A technique can lower per-turn cost while lengthening the run, as summarisation did in the JetBrains
study, so the measure has to be per task rather than per call. The metrics that appear across the
sources are tokens per task, the cached-read share of input tokens, context-window fill at each
turn, the number of compaction events, trajectory length, summariser cost share and task success,
all broken down by model, since the JetBrains results showed that the same technique helped one
model and hurt another ([arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)). Anthropic's
finding that token usage explained about 80% of BrowseComp performance variance means that quality
results reported without token spend are hard to interpret
([Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)).

For agents over enterprise data, Uber's evaluation is a usable template. It scores a golden set of
real questions with verified intent, tables and reference SQL on intent accuracy, table overlap,
successful execution, non-empty results and LLM-judged similarity, and it treats run-to-run
variation of about 5% as noise ([Uber Engineering,
QueryGPT](https://www.uber.com/en-us/blog/query-gpt/)). BlackRock describes "evaluation-driven
development", in which each system-prompt behaviour becomes a test case written with subject-matter
experts and run daily and on every pull request ([ZenML
summary](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)).
Morgan Stanley built its assistant rollout on evaluations graded by advisors for accuracy and
coherence ([OpenAI customer story](https://openai.com/index/morgan-stanley/)). Tracing products such
as LangSmith, Langfuse and the OpenTelemetry GenAI conventions were not researched for this report.

## 6. The enterprise context layer

### 6.1 What the term means

There is no standard definition. a16z describes the context layer as a superset of the traditional
semantic layer, adding access to tribal knowledge in documents, canonical entities and identity
resolution, governance guidance and natural-language rules, and it states that the market is early
and that where the layer should live is still open ([a16z, Your Data Agents Need
Context](https://a16z.com/your-data-agents-need-context/)). Atlan attributes to Gartner a structure
of three components, semantics, operational state and provenance, which is a vendor's account of an
analyst framework ([Atlan](https://atlan.com/know/core-components-context-layer/)). Alation
distinguishes the semantic layer, which standardises metric definitions, from a context layer that
adds ownership, lineage and machine-readable delivery
([Alation](https://www.alation.com/blog/what-is-an-enterprise-context-layer/)).

Across these sources the working definition has four parts. The first is meaning, supplied by a
semantic layer or an ontology. The second is provenance and trust, supplied by a catalog with
lineage and certification. The third is accumulated knowledge, meaning documents, tribal rules,
corrections and decision history. The fourth is delivery, meaning an API or MCP endpoint that
enforces access control. The terms used by vendors differ mainly in which of these parts the vendor
sells.

The term "context graph" is narrower. Foundation Capital's late-2025 essay argues that systems of
record keep outcomes but not reasoning, and defines a context graph as an accumulated record of
decision traces, meaning what context was used, which policy applied, which exception was granted
and who approved it, linked across entities and time ([Ashu
Garg](https://ashugarg.substack.com/p/ais-trillion-dollar-opportunity-context)).
[sdlc-context-graph.md](sdlc-context-graph.md) section 3 covers this distinction and its application
to software delivery.

The motivating failure in a16z's essay shows why the layer is needed. An agent asked "what was
revenue growth last quarter?" does not know which revenue definition or fiscal quarter applies, the
semantic-layer YAML is outdated and missing two product lines, and finance's `fct_revenue` table
competes with a materialised view called `mv_revenue_monthly`. In capital markets the same problem
appears with "notional", "exposure", "position" (trade-date or settlement-date) and "counterparty"
(legal entity or parent group), each of which has several legitimate definitions, so the context
layer must carry the definition and its owner as well as the column.

### 6.2 Reference architecture

The architecture that the sources converge on has five tiers.

| Tier | What it holds | Typical components | Who builds it |
|---|---|---|---|
| Sources | Systems of record | Trading, risk, reference data, CRM, document stores | Existing |
| Ingestion | Unified data with lineage | Lakehouse, pipelines, lineage capture | Data platform team, often bought |
| Meaning | Definitions, entities, trust signals | Semantic layer, ontology or knowledge graph, catalog | Bought engine, firm-modelled content |
| Serving | Retrieval and routing with entitlements | MCP servers, gateway, permission-aware search | Usually built |
| Agents | Task logic, memory, feedback | Agent runtime, memory scopes, evaluation suites | Built |

a16z's build sequence follows the same order. It makes sources reachable, generates first-draft
context automatically from query frequency, common joins and existing dbt or LookML definitions, has
human experts add implicit and conditional knowledge, exposes the result through an API or MCP, and
keeps it self-updating as upstream data changes and agent errors are corrected
([a16z](https://a16z.com/your-data-agents-need-context/)).

OpenAI's in-house data agent is the most detailed public example and uses six context sources
([OpenAI, Inside our in-house data
agent](https://openai.com/index/inside-our-in-house-data-agent/)). They are table usage metadata
with queries from popular dashboards ranked above one-off queries, human annotations from owners,
Codex enrichment that reads pipeline code to infer derivation and freshness, institutional knowledge
from Slack, Google Docs and Notion through an access-controlled retrieval service, memory of
corrections, and live queries to the warehouse when offline context is stale. Secondary coverage
reports that the first three sources are merged nightly into one description per table, that
retrieving all historical queries hurt because most were one-offs, and that the team found the
foundation of unified data and strong annotations mattered more than the agent itself
([ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)). OpenAI published no
accuracy figures.

The build-versus-buy pattern that emerges is to buy the engines (catalog, semantic layer runtime,
lakehouse) and to build the retrieval, routing and memory logic, because that is where firm-specific
knowledge lives. No published total-cost-of-ownership comparison was found.

### 6.3 Semantic layers and metrics layers

**How it works.** Metrics, dimensions and the joins between them are defined once in a governed
model, usually YAML, and an engine compiles a request for "net revenue by region last quarter" into
SQL. The agent asks the semantic layer for a metric rather than writing SQL against raw tables.
Examples include the dbt Semantic Layer on MetricFlow, Snowflake semantic views, Databricks Metrics,
Looker's LookML and Tableau Semantics (section 7).

**Strengths.** Within the modelled scope, accuracy is very high and consistent. dbt Labs reran the
data.world insurance benchmark in April 2026 on a modelled project with 11 questions run 20 times
each, and found Claude Sonnet 4.6 scored 90.0% through text-to-SQL and 98.2% through the Semantic
Layer, while GPT-5.3 Codex scored 84.1% and 100.0% ([dbt
Labs](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)). The most useful property
for regulated reporting is the failure behaviour. dbt Labs reports that text-to-SQL fails silently
with plausible wrong answers, while the semantic layer fails visibly by erroring or declining. A
semantic layer also gives every tool and every agent the same definition, which is why BlackRock
co-leads the Open Semantic Interchange (section 7.2).

**Weaknesses.** Coverage is limited to what has been modelled. On questions that needed more entity
hops than the model supported, the Semantic Layer scored 0% in every run, while text-to-SQL scored
70% to 100%. The headline results rest on 11 questions on one dataset, the benchmark is vendor-run,
and dbt Labs notes that it gave text-to-SQL the full schema, which is impractical for a large
warehouse. Third parties report 100% on the same 11 questions, and one analysis argues that these
numbers mostly measure how much modelling work was already done
([HackerNoon](https://hackernoon.com/why-better-schema-modeling-beats-better-text-to-sql-models)).
Semantic definitions also go stale, as in a16z's example of a YAML file missing two product lines.
No public benchmark on a financial-services schema of trades, positions and reference data was
found.

**Cost.** The engines are increasingly open source (MetricFlow was relicensed under Apache 2.0 in
October 2025, and Databricks Metrics ships in Apache Spark), so the main cost is human modelling
effort that scales with the number of governed metrics, plus ongoing upkeep. No source quantified
that effort in person-hours.

**Capital markets example where it fits.** A finance agent answers questions about desk P&L,
risk-weighted assets and regulatory capital by business line. These numbers have one approved
definition each, are reported externally and are reconciled by product control. A semantic layer
that either returns the governed figure or refuses is the right behaviour, and a plausible wrong
number from free-form SQL is the worst outcome.

**Where it does not fit.** A credit officer asks which positions are held against counterparties
whose ultimate parent has a netting agreement without a collateral threshold. The question joins
positions to a counterparty hierarchy and to CSA terms in a way the metrics model was never designed
for, and a semantic layer would return nothing. dbt Labs' own recommendation is to route such
questions to governed text-to-SQL or to consider whether a small modelling change would close the
gap ([dbt Labs](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)).

### 6.4 Ontologies and knowledge graphs

[agentic-ai.md](agentic-ai.md) sections 3.4 to 3.7 cover GraphRAG, temporal graphs and the ontology
pattern as retrieval methods, and this section adds only what matters for an enterprise context
layer.

**How it works.** The firm models its business objects (instruments, legal entities, accounts,
positions, agreements) as typed entities with named relationships, and binds them to the underlying
data. Palantir's Ontology adds kinetic elements, meaning actions and functions with the same
granular access controls as data, so that human and agent actions are staged and written back to
enterprise systems ([Palantir docs](https://www.palantir.com/docs/foundry/ontology/why-ontology)).
FIBO, maintained by the EDM Council, is an open OWL ontology of financial concepts that maps
"counterparty", "client" and "customer" onto a shared legal entity or party concept with explicit
ownership and contract relationships ([EDM
Council](https://edmcouncil.org/frameworks/industry-models/fibo/)).

**Strengths.** This pattern has the oldest measured evidence for structured data. In the original
data.world benchmark, GPT-4 answered 16% of questions correctly over raw SQL and 54% over a
knowledge-graph representation of the same database ([arXiv
2311.07509](https://arxiv.org/pdf/2311.07509)). It handles multi-hop questions that a metrics model
cannot, and it is the only pattern of those compared here that offers governed write actions, which
matters once an agent books an amendment or raises a break rather than only describing one.

**Weaknesses.** It is a long programme of modelling and organisational agreement rather than an
installable component. RDF and OWL suit shared, standards-aligned vocabularies but have scarce
tooling skills, while property graphs are easier for engineering teams but lack formal semantics,
and no measured comparison of the two for LLM accuracy was found. The 2023 gap has narrowed as
models improved, with dbt Labs reporting raw-schema text-to-SQL accuracy rising from 32.7% in 2023
to 64.5% in 2026. No independent study of Palantir's Ontology effect on agent accuracy was found.

**Cost.** This is the highest human cost of any option here, because domain experts must agree on
the model. Graph construction over documents is a compute cost that has fallen sharply. Microsoft
reports that LazyGraphRAG indexing costs 0.1% of full GraphRAG ([Microsoft
Research](https://www.microsoft.com/en-us/research/blog/lazygraphrag/)), against one practitioner's
anecdote of a $33,000 GraphRAG indexing bill in early 2024. Palantir deployments involve embedded
engineers, and commentary questions whether such builds scale beyond resource-intensive engagements
([Foreign Policy
Journal](https://www.foreignpolicyjournal.com/2026/10/16/palantir-technologies-nasdaq-pltr-deploys-foundry-and-aip-platforms-inside-commercial-banking-with-customers-bank-deal/)).

**Capital markets example where it fits.** Counterparty and beneficial ownership analysis is
relational by nature. A graph keyed on LEIs, with parent, subsidiary, guarantor and ultimate
beneficial owner relationships, lets an agent aggregate exposure to a group after one subsidiary is
downgraded, which neither a metrics layer nor document retrieval can do.

**Where it does not fit.** Research question answering over earnings-call transcripts is
paraphrase-heavy and mostly needs single passages, so building an ontology for it would be expensive
and add little. Hybrid retrieval with a reranker, as described in [agentic-ai.md](agentic-ai.md)
section 5, is the better fit, with graph retrieval reserved for questions that span issuers.

### 6.5 Catalogs, lineage and usage-derived metadata

**How it works.** A data catalog holds schemas, descriptions, owners, classifications, certification
status and lineage, and agents query it before choosing tables. The production text-to-SQL systems
add usage signals from query logs. LinkedIn's SQL Bot draws on DataHub metadata including top values
for categorical fields and partition keys, ingests popular tables automatically and uses deprecation
signals to retire datasets ([arXiv 2507.14372](https://arxiv.org/pdf/2507.14372)). Uber's QueryGPT
routes a question to a curated domain workspace, lets the user edit the selected tables, and prunes
columns because its largest tables exceed 200 columns or 40,000 to 60,000 tokens ([Uber
Engineering](https://www.uber.com/en-us/blog/query-gpt/)). Pinterest indexes summaries of top-tier
tables only and has a model re-select from retrieved candidates.

**Strengths.** It uses metadata the firm already has, and usage signals are cheap and reflect how
people actually query. Certification and tiering act as the trust filter in every published system.
Uber reports that 78% of users said QueryGPT saved time and estimates query authoring falling from
about 10 minutes to about 3, and Pinterest's first-shot acceptance reportedly rose from about 20% to
over 40% ([ZenML
summary](https://www.zenml.io/llmops-database/text-to-sql-system-with-rag-enhanced-table-selection)).
Both are self-reported or second-hand.

**Weaknesses.** Schema and descriptions alone are insufficient, since OpenAI found that
near-identical tables differ in meaning. Query logs encode wrong and one-off queries along with good
ones, so they need ranking by author, frequency and dashboard use. Similarity retrieval over tables
degrades with scale, and Uber's first version lost accuracy as more tables were onboarded. Reported
production accuracy is moderate, with LinkedIn at 53% correct or nearly correct by expert review,
which supports keeping a human confirmation step.

**Cost.** The catalog is usually bought. Enrichment can turn documentation effort into batch
compute, and secondary coverage of OpenAI reports Codex enrichment running in batches of 100 to 200
tables taking 5 to 10 minutes each
([ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)). Owner annotation
remains a human cost.

**Capital markets example where it fits.** A bank has several copies of position data: the
books-and-records store, a risk-system copy and a finance reporting mart. A catalog attribute that
marks the books-and-records store as the golden source for end-of-day positions, combined with usage
ranking from the queries behind approved regulatory reports, lets the agent choose the right table
and explain why.

**Where it does not fit.** Catalog metadata should not be treated as a guarantee of correctness for
numbers that are reported externally. A catalog can tell an agent which table is certified, but it
cannot stop the agent writing an incorrect aggregation over it, so regulated figures should come
from the semantic layer rather than from catalog-guided SQL.

### 6.6 Permission-aware enterprise search

**How it works.** Documents are indexed with their access-control lists attached to each chunk, and
the retriever filters by the requesting user's entitlements before similarity search, so restricted
content never enters the context. Elasticsearch document-level security, Azure AI Search security
filters, Weaviate multi-tenancy and Pinecone metadata filters implement variants ([DEV
Community](https://dev.to/venkathub/permission-aware-rag-enforcing-document-acls-at-retrieval-time-54a7)).
Glean, Microsoft Work IQ and Foundry IQ sell this as a managed service (section 7).

**Strengths.** It is the only pattern here that covers unstructured knowledge such as policies,
procedures, research and agreements while respecting existing permissions. Pre-filtering is also
more efficient than post-filtering, which wastes compute and can return sparse results.

**Weaknesses.** Filtering after generation is insufficient, because the model may already have seen
restricted facts and can leak them through paraphrase or through a refusal
([tianpan.co](https://tianpan.co/blog/2026-04-19-pii-leak-rag-pipeline-access-control)). The main
operational failure is ACL drift between the source and the index. Microsoft's ISE team notes that a
revoked user may still see content until the next ingestion run, and recommends re-indexing on
permission-change events ([Microsoft
ISE](https://devblogs.microsoft.com/ise/sharepoint-doc-level-access/)). Leakage paths also include
caches, rerankers, summaries, tool outputs and agent memory, which sit outside the index's
authorisation boundary. No measured study of ACL drift or leakage rates in production was found.

**Cost.** Managed offerings are priced per seat with consumption credits. Glean publishes no price
list, and Vendr reports a buyer-reported median contract of about $98,890 a year
([Vendr](https://www.vendr.com/marketplace/glean)). A self-built index carries the ongoing cost of
permission synchronisation.

**Capital markets example where it fits.** A research and policy assistant serves analysts on the
public side of the information barrier. The index carries entitlements from the document management
system, so research reports, compliance manuals and published filings are searchable, while deal
team folders on the private side are excluded before retrieval for any public-side user.

**Where it does not fit.** Corpus-wide summaries, such as GraphRAG community summaries or a cached
daily digest, built across documents with different entitlements inherit no single document's ACL,
so they can expose private-side information to public-side users. Any derived artefact of that kind
has to be built per entitlement group, or not built at all over mixed-permission content.

### 6.7 Decision traces and context graphs

A context graph records why decisions were made, such as why a limit breach was approved or why an
exception was granted on a client onboarding, and Foundation Capital argues that capturing these
traces requires sitting in the execution path at commit time ([Ashu
Garg](https://ashugarg.substack.com/p/ais-trillion-dollar-opportunity-context)). Palantir describes
its Ontology as designed to represent decisions as well as data ([Palantir
blog](https://blog.palantir.com/connecting-agents-to-decisions-277dee8ddb40)), and Sequeda's recap
of Gartner's March 2026 conference reports that decision governance was called the most underrated
trend ([Sequeda](https://juansequeda.substack.com/p/gartner-data-and-analytics-march)). Its strength
is that precedent becomes searchable, and its weakness is that it only exists where a workflow
system already captures approvals, so it cannot be reconstructed after the fact.
[sdlc-context-graph.md](sdlc-context-graph.md) sections 3.2 and 7 cover how such graphs are fed and
how they go stale.

### 6.8 Side by side

| Option | Answers | Strength | Weakness | Main cost | Fits in capital markets | Does not fit |
|---|---|---|---|---|---|---|
| Semantic layer | Governed metrics | Very high in-scope accuracy; fails visibly | 0% outside modelled scope | Human modelling | P&L, RWA, regulatory figures | Ad hoc multi-hop joins |
| Ontology or knowledge graph | Entities, relationships, actions | Multi-hop; governed writes | Long programme; skills scarce | Domain expert agreement | Counterparty and ownership hierarchies | Transcript and filing Q&A |
| Catalog and usage metadata | Which table, owner, freshness | Uses existing metadata; trust tiers | Moderate accuracy; noisy logs | Owner annotation | Golden-source selection | Sole guarantee for reported numbers |
| Permission-aware search | Unstructured knowledge | Respects existing ACLs | ACL drift; derived-artefact leakage | Seats or sync pipeline | Policies, research, agreements | Mixed-entitlement summaries |
| Decision traces | Why something was decided | Searchable precedent | Needs execution-path capture | Workflow integration | Limit breach and exception approvals | Decisions made outside systems |

These options are layers rather than alternatives. A reasonable financial-services arrangement is
golden-source reference data (instruments, legal entities with LEIs, counterparties, books) as the
ontology core, trade, position and risk metrics in a semantic layer, policies, ISDA and CSA terms
and procedures in a permission-aware document index, and approval history in a decision-trace store,
all reached through one gateway that enforces the user's entitlements.

## 7. Vendor platforms and standards

### 7.1 Four vendor families

By 2026 almost every data vendor markets a context layer, and TechTarget described Neo4j's October
2026 launch as joining a "context cavalcade"
([TechTarget](https://www.techtarget.com/data-technologies/news/366652383/Neo4j-joins-the-context-cavalcade-with-suite-for-informing-AI-agents)).
Joe Reis argues that vendors are renaming active-metadata products as context products ([Joe
Reis](https://joereis.substack.com/p/gartner-declares-2026-the-year-of)). The products fall into
four families.

| Family | Vendors | Mechanism | How agents consume it | Strength | Weakness |
|---|---|---|---|---|---|
| Warehouse and lakehouse semantics | Snowflake semantic views and Horizon Context; Databricks Unity Catalog Metrics and Genie Ontology; Google Looker (LookML); Salesforce Tableau Semantics | Governed metric and dimension objects stored next to the data | MCP servers, native agents, A2A for Looker | Deep integration with the platform's security and agents | Semantics tied to one platform raise switching costs |
| Catalog-based context | Atlan, Collibra, Alation, DataHub; Google Knowledge Catalog | Glossaries, lineage, certification and ownership | MCP servers within the caller's permissions | Neutral across platforms; governance depth | An extra layer to operate; no execution engine |
| Work and document graphs | Glean; Microsoft Work IQ and Foundry IQ | Permission-aware index of documents, people and activity | Native agents and MCP | Covers unstructured knowledge with ACLs | Seat pricing; little structured-data semantics |
| Ontology and graph | Palantir Foundry and AIP; Microsoft Fabric IQ; Neo4j Context Engine | Typed entities, links and actions | Platform agents and APIs | Multi-hop reasoning and governed actions | Heaviest build; several products still in preview |

Some details matter for evaluation. Snowflake announced Cortex Sense at its June 2026 Summit, and
recaps cite accuracy of 83% with it against 24% without it and, elsewhere, "up to 3x to 4x" better
accuracy, which are inconsistent vendor claims
([Flexera](https://www.flexera.com/blog/perspectives/snowflake-summit-2026/);
[Revefi](https://www.revefi.com/blog/key-takeaways-snowflake-summit-2026)). Databricks added a
business-semantics pillar to Unity Catalog in June 2026, with several parts in preview, and states
that Metrics is open source and "OSI ready"
([Databricks](https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026)). Its
Unity AI Gateway governs MCP services, agents and tools with hard spend caps. Microsoft's Fabric IQ
ontology is labelled preview on Microsoft Learn, although one source reports a general-availability
announcement ([Microsoft
Learn](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/fabric-iq)). Neo4j's
Context Engine entered private preview on 20 October 2026. No retrieved source described an
AWS-native business semantic layer comparable to semantic views or metric views.

Named financial-services references are scarce. Google cites PayPal scaling conversational analytics
to more than 3,000 users through Claude Desktop and the Looker MCP server, which is a vendor claim
([Google
Cloud](https://cloud.google.com/blog/products/business-intelligence/looker-in-2026-gartner-analytics-and-bi-platforms-mq)).
Customers Bank announced on 15 October 2026 that it is deploying Palantir Foundry and AIP for
deposit account onboarding, and states that "their data and their ontology remain theirs" ([Palantir
IR](https://investors.palantir.com/news-details/2026/Customers-Bank-and-Palantir-Collaborate-to-Build-an-AI-Native-Future-for-Banking)).
No retrieved source named a financial-services customer for the context features of Snowflake,
Databricks, dbt, Atlan, Collibra, Alation, Glean, Microsoft, AWS or Salesforce.

### 7.2 Interoperability standards

The Open Semantic Interchange was launched by Snowflake in September 2025 with Salesforce, dbt Labs,
BlackRock and RelationalAI, and its first specification was published under Apache 2.0 on 27 January
2026, covering datasets, metrics, dimensions, relationships and AI context such as synonyms and
usage instructions
([Snowflake](https://www.snowflake.com/en/blog/open-semantic-interchanges-specs-finalized/)).
Secondary sources report that it entered the Apache Incubator in July 2026 as Apache Ossie, which
was not confirmed on an Apache page. Round trips are lossy in practice. Snowflake-only features are
written as vendor extensions and non-equi joins can be dropped, so portability applies to the common
core ([Datus.ai](https://datus.ai/blog/what-is-snowflake-osi/)). Sequeda argues that OSI covers only
BI semantics and recommends RDF and OWL for ontologies, which is his opinion
([Sequeda](https://juansequeda.substack.com/p/gartner-data-and-analytics-march)).

MCP is the access protocol that every vendor in section 7.1 supports, and it moved to the Linux
Foundation's Agentic AI Foundation in December 2025 alongside AGENTS.md and goose ([IT
Brief](https://itbrief.com.au/story/linux-foundation-launches-agentic-ai-open-standards-hub)). Its
revision of 28 July 2026 removed protocol-level sessions, added OpenTelemetry trace propagation,
required routing headers so intermediaries can filter without parsing bodies, required cache
lifetime and scope fields on list and read results, and deprecated OAuth Dynamic Client Registration
in favour of Client ID Metadata Documents ([MCP changelog
2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)). These changes suit
a model in which an enterprise gateway routes, caches, audits and traces all context delivery, and
in which the firm's identity provider controls which agent clients may obtain tokens. MCP
standardises how an agent reaches context but says nothing about what the context means, which is
why vendors pair it with OSI-style semantics. A2A, a separate Linux Foundation project since June
2025, covers delegation between agents and complements MCP ([Help Net
Security](https://www.helpnetsecurity.com/2025/06/24/the-linux-foundation-agent2agent/)).

A Gartner forecast repeated in vendor blogs predicts that by 2028, 60% of agentic analytics projects
relying solely on MCP will fail for lack of a consistent semantic layer ([CTO
Magazine](https://ctomagazine.com/semantic-layer-ai-agents-iceberg-mcp/)). The original was not
available, the timeframes differ between retellings, and it should be read as a forecast.

### 7.3 Lock-in

The lock-in risk has moved from storage, where open table formats are now common, to business
semantics and agent runtime. Each platform's agent works best on its own semantic objects even when
those objects can be exported, and competitors critique LookML and Tableau Semantics as vendor-bound
([Strategy](https://software.strategy.com/blog/google-next-26-just-validated-agentic-bi-needs-a-semantic-layer);
[SoftwareReviews](https://www.softwarereviews.com/vendor-technology-notes/dreamforce-2026-data-360-tableau-informatica)).
Most of this commentary comes from vendors with a stake in the outcome. For a regulated firm the
trade-off is between deep platform-native governance and agent integration (Snowflake, Databricks,
Palantir) and portability through a neutral catalog and OSI-based definitions (Atlan, Collibra,
dbt), which costs an extra layer to operate. Keeping metric definitions in an open format such as
MetricFlow YAML, even when a platform runtime serves them, preserves the option to move.

## 8. Governance and regulation in capital markets

### 8.1 Regulatory expectations

FINRA's 2026 Annual Regulatory Oversight Report, released on 9 December 2025, is the first FINRA
report to discuss AI agents
([Debevoise](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)).
It states that agents "may take actions that exceed the user's actual or intended scope or
authority", that "complex chains of agent actions may be difficult to reconstruct", and that agents
working with sensitive data "may unintentionally retain or reveal that information". Its guidance
includes "maintaining prompt and output logs for accountability and troubleshooting" and "tracking
which model version was used and when". FINRA treats its rules as technology-neutral and expects
written supervisory procedures to be updated ([DLA
Piper](https://www.dlapiper.com/insights/publications/2025/12/finra-flags-generative-ai-risks-and-governance-expectations)).
A prompt log alone cannot reconstruct an agent's decision, because the decision depended on
retrieved context and tool results, so a firm that wants to meet the intent of this guidance should
log those as well. That last point is an inference rather than FINRA's wording.

Other frameworks apply in parallel. The Federal Reserve's SR 11-7 sets model risk management
expectations that banks apply to AI models ([Federal
Reserve](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm)). DORA has applied ICT
risk and third-party risk requirements to EU financial entities since 17 January 2025, which covers
LLM and MCP providers as ICT third parties
([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)). Under the EU Digital Omnibus
provisional agreement of 7 May 2026, AI Act high-risk obligations for stand-alone Annex III systems
are deferred to 2 December 2027
([Sidley](https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/)).
The deferral reduces near-term AI Act pressure, but DORA and SR 11-7 already apply. No regulator
publication was found that addresses information barriers or MNPI in the context of LLM retrieval
specifically.

OWASP's Top 10 for Agentic Applications, published on 9 December 2025, lists memory and context
poisoning, tool misuse, and identity and privilege abuse among its risks ([OWASP
GenAI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)).
[ai-security.md](ai-security.md) covers prompt injection, tool poisoning and MCP security in detail.

### 8.2 Information barriers, MNPI and entitlements

Information barriers map onto permission-aware retrieval, provided that the agent retrieves with the
requesting user's identity. An agent that retrieves through a shared service account can cross a
barrier that the user could not, because the service account's entitlements are the union of
everyone's. The same applies to licensed market data. S&P Global's Kensho-built MCP server for
Capital IQ data has users connect by logging in to their own authorised S&P account ([S&P
Global](https://press.spglobal.com/2025-07-15-S-P-Global-and-Anthropic-Announce-Integration-of-S-P-Globals-Trusted-Financial-Data-into-Claude)),
which preserves existing licence entitlements and audit, and Anthropic describes similar connectors
for LSEG and Moody's data
([Anthropic](https://www.anthropic.com/news/advancing-claude-for-financial-services)).

The derived-artefact risk from section 6.6 is specific to this industry. Summaries, caches, memory
and graph community reports built across mixed-entitlement content inherit no single document's
permissions, and a memory written by a private-side banker and later retrieved for a public-side
user is an information barrier breach. Memory, caches and derived indexes therefore need to be
scoped by entitlement group, and the agent's identity at each step needs to be the user's. No
published technical account of row-level or column-level security passthrough from a warehouse to an
agent at a named bank was found.

### 8.3 What banks have published

The published deployments share a pattern of a firm-controlled gateway in front of several models,
retrieval over curated internal content, and evaluation suites built with domain experts. Goldman
Sachs routes GS AI Assistant prompts through an internal compliance gateway that selects among
vetted models ([Fox
Business](https://foxbusiness.com/technology/goldman-sachs-announces-firmwide-launch-ai-assistant)).
JPMorgan's LLM Suite is a portal over external models that the bank updates roughly every eight
weeks as it connects business-unit data, and its chief analytics officer has said that much of the
work is connecting the "thousands of different applications" the firm runs
([CeFPro](https://connect.cefpro.com/article/view/inside-jpmorgan-llm-suite-as-ai-agents-spread-across-the-bank);
[McKinsey](https://www.mckinsey.com.br/industries/financial-services/our-insights/jpmorgan-chases-derek-waldron-on-building-an-ai-first-bank-culture)).
BlackRock's Aladdin Copilot uses a plugin registry to which 50 to 60 domain teams contribute tools,
passes application context (which screen is open and what is on it) with each query, filters
thousands of tools to 20 to 30, and governs plugin access by environment, user group and application
([ZenML
summary](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)).
Morgan Stanley's assistant is used by over 98% of advisor teams according to OpenAI's customer
story, and the firm keeps advisor review of meeting summaries before they enter the CRM
([OpenAI](https://openai.com/index/morgan-stanley/)). All usage and productivity figures from these
firms are self-reported, and no independent measurement of outcomes at any bank was found.

The common design treats the gateway, tool registry, context layer and evaluation suite as the
durable asset and the model as replaceable. This matches the broader survey evidence, where the most
cited causes of failed pilots are cost, unclear value, risk controls and integration with workflows
and data. Gartner's prediction that over 40% of agentic AI projects will be cancelled by the end of
2027 is a forecast based on a webinar poll
([Gartner](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)),
and MIT NANDA's finding that 95% of organisations saw no measurable return rests on about 150 survey
responses and 52 interviews ([AI
Realist](https://msukhareva.substack.com/p/genai-has-little-to-no-return-on)). Both should be read
as weak evidence.

## 9. Worked capital markets scenarios

The table maps common capital markets workloads to the agent-side and enterprise-side techniques
that fit them, drawing on the per-option examples above.

| Workload | Context layer components | Agent-side techniques | Main control |
|---|---|---|---|
| Settlement break investigation | Catalog for golden-source trade and SSI data; just-in-time record lookup | Observation masking with restorable references; single agent | Agent acts with operations user's entitlements; amendments through governed actions |
| Counterparty and beneficial ownership exposure | Ontology keyed on LEIs; semantic layer for exposure metrics | Code execution to aggregate large position sets | Exposure definitions owned by credit risk |
| Trade surveillance triage | Graph of orders, executions and communications over time; permission-aware search over communications | Prompt caching of policy prefix; evidence written to a case store | Full retrieved-context logging for the case file |
| Client mandate and restriction checks | Systems of record for mandates and restricted lists, queried at decision time | Constraints pinned in prompt or re-read each step, never left to summaries | No memory system as the record of restrictions |
| Research over filings and transcripts | Permission-aware hybrid index of research, filings and licensed data via per-user MCP | Sub-agents per issuer; compaction of long runs | Public-side scoping; licensed-data entitlements |
| Regulatory and management reporting | Semantic layer with router to governed text-to-SQL | Small tool set; refusal over guessing | Product control ownership of metric definitions |

## 10. Practical build order

1. **Measure before optimising.** Record tokens per task, cache hit rate, window fill per turn,
   trajectory length and task success by model on a golden set of real questions, following Uber's
   pattern, because several techniques trade per-call savings against longer runs.
2. **Lay out prompts for caching and turn on observation masking.** Put stable content (tools,
   policy, instructions) first, append everything else, serialise deterministically, and mask old
   tool outputs while keeping references. These two steps are cheap and have the best evidence.
3. **Cut the tool set.** Remove overlapping tools, keep the visible set below about 20 to 30, and
   design tools to return filtered, token-efficient results. Add tool search only when the library
   is genuinely large, and add code execution only when the firm can approve a sandbox.
4. **Externalise state to files.** Have long-running agents keep a plan and notes outside the
   window, and move stable procedures into reviewed instruction files or skills with an owner. Add
   summarisation or resets only when a demonstrated loss of long-range continuity appears.
5. **Stand up the gateway and identity model before connecting data.** Route all model and MCP
   traffic through a firm-controlled gateway, pass the user's identity to every data source, and log
   prompts, retrieved context, tool calls and model versions. This is the step that information
   barriers and FINRA's guidance depend on.
6. **Use the metadata you already have.** Mark golden sources, certification and ownership in the
   catalog, rank tables by usage from approved reports, and deprecate copies. Build a domain-scoped
   table-selection step with human confirmation before trying free-form SQL across the estate.
7. **Model the metrics that are reported externally.** Put P&L, exposure, capital and other governed
   figures in a semantic layer kept in an open format, and route questions to it first with governed
   text-to-SQL as the fallback.
8. **Build permission-aware search over documents with event-driven ACL refresh.** Re-index on
   permission change rather than on a schedule, and scope any derived summaries, caches and memory
   by entitlement group.
9. **Take on the ontology last and narrowly.** Start with the relational domain where the semantic
   layer fails, usually counterparty and legal-entity hierarchies, align it with FIBO where
   practical, and add governed write actions only when agents need to act rather than report.
10. **Add sub-agents and long-term memory only for the workloads that need them.** Use sub-agents
    for parallel, read-only research, and memory services for soft preferences, and keep both out of
    anything that serves as a control.

## 11. Failure modes to watch for

- A hard constraint, such as a client restriction or an account identifier, enters the context once
  through a tool result and is later masked or summarised away, so the agent proceeds without it.
- A summary carries a wrong fact forward and later steps treat it as established, which the OpenAI
  cookbook calls context poisoning and which is hard to debug if summaries are not logged.
- A compression technique lowers per-call cost but lengthens the run, or rewrites the history and
  destroys cache hits, so total cost rises while the per-call metric improves.
- The tool list grows with each team's contribution until planning degrades, which BlackRock
  observed beyond about 40 to 50 tools and OpenAI resolved by cutting from about 40 to 13.
- A tool description from a third-party MCP server contains injected instructions that load into
  every session, as described in [ai-security.md](ai-security.md).
- Sub-agents make conflicting implicit decisions on interdependent work, and the lead agent
  reconciles them incorrectly.
- The semantic layer goes stale or misses product lines, as in a16z's example, and continues to
  return confident governed answers for an incomplete scope.
- Text-to-SQL returns a plausible wrong number with no warning, which dbt Labs identifies as its
  characteristic failure, and the number reaches a report.
- Two tables both appear authoritative during a migration, and the agent picks the wrong one, which
  OpenAI addressed by tracking explicitly which copy was authoritative.
- Index ACLs lag the source after a revocation or a wall-crossing change, so a user can retrieve
  content they are no longer entitled to see.
- A summary, cache, digest or shared memory built across mixed-entitlement content exposes
  private-side information to public-side users.
- An agent retrieves with a shared service account rather than the user's identity, so its effective
  entitlements are broader than any individual user's.
- Logs capture the prompt and the output but not the retrieved context, so a supervisor cannot
  reconstruct why the agent acted as it did.
- Vendor accuracy claims from 11-question benchmarks or internal evaluations are used to justify a
  platform choice, without a firm-specific golden set to confirm them.

## 12. Open questions and gaps in the evidence

Several questions remain open on the available evidence. No independent benchmark compares agentic
search, vector retrieval and hybrids on the same tasks with cost and latency, and no independent
benchmark compares the long-term memory products under identical conditions. The multi-agent, tool
search, context editing and memory gains reported by Anthropic come from internal evaluations that
have not been replicated. No 2026 replication of the context rot studies on current-generation
models was found, so how much smaller the degradation has become is unknown.

On the enterprise side, no public text-to-SQL or semantic-layer benchmark exists on a
financial-services schema of trades, positions and reference data, no source quantified the human
cost of curating a governed metric or entity, and no source measured how quickly context accuracy
decays without refresh. Gartner and Forrester material reached this research only second-hand.
Regulators have not addressed information barriers or MNPI in LLM retrieval directly, so firms are
applying existing supervisory rules by analogy.

## Resources

Agent-side context engineering:

- [Effective context engineering for AI
  agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) —
  Anthropic, September 2025, the attention-budget principle, compaction, note-taking and sub-agents.
- [Managing context on the Claude Developer Platform](https://claude.com/blog/context-management) —
  context editing and the memory tool, with Anthropic's internal results.
- [Context Engineering for AI Agents: Lessons from Building
  Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) —
  KV-cache hit rate, logit masking, restorable compression and todo recitation.
- [The Complexity Trap](https://arxiv.org/abs/2508.21433) — JetBrains Research, observation masking
  compared with LLM summarisation on SWE-bench Verified.
- [Context Engineering for Agents](https://www.langchain.com/blog/context-engineering-for-agents) —
  LangChain, the Write, Select, Compress and Isolate taxonomy.
- [Architecting efficient context-aware multi-agent framework for
  production](https://developers.googleblog.com/en/architecting-efficient-context-aware-multi-agent-framework-for-production/)
  — Google ADK, context as a compiled view.
- [Session memory](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory) —
  OpenAI Cookbook, trimming and summarising sessions and their failure modes.
- [Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) — Cognition, the
  case for single-threaded agents.
- [How we built our multi-agent research
  system](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic, the
  token-spend findings.
- [Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) and [Code
  execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) — tool search,
  programmatic tool calling and code execution.
- [Code Mode](https://blog.cloudflare.com/code-mode/) — Cloudflare, MCP tools as a TypeScript API in
  an isolate.
- [Equipping agents for the real world with Agent
  Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
  — progressive disclosure.
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) (Anthropic)
  and [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) (OpenAI) —
  current pricing and mechanics.
- [Mem0](https://arxiv.org/abs/2504.19413) and [Zep](https://arxiv.org/abs/2501.13956) —
  vendor-authored memory papers.

Long-context evidence and failure modes:

- [Context Rot](https://www.trychroma.com/research/context-rot) — Chroma, 18 models, distractors and
  focused prompts.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172), [RULER](https://arxiv.org/abs/2404.06654),
  [NoLiMa](https://arxiv.org/abs/2502.05167) and [Databricks long-context
  RAG](https://www.databricks.com/blog/long-context-rag-performance-llms) — measured degradation.
- [How Long Contexts
  Fail](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html), [How to Fix
  Your Context](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html) and [The State of
  Context Engineering](https://www.dbreunig.com/2026/10/24/the-state-of-context-engineering.html) —
  Drew Breunig, the failure-mode taxonomy and its 2026 update.

Enterprise context layer:

- [Your Data Agents Need Context](https://a16z.com/your-data-agents-need-context/) — a16z, the
  definition and build sequence.
- [Inside our in-house data agent](https://openai.com/index/inside-our-in-house-data-agent/) —
  OpenAI, six context sources.
- [Semantic Layer vs. Text-to-SQL
  2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026) — dbt Labs benchmark rerun
  and routing advice.
- [A Benchmark to Understand the Role of Knowledge Graphs on LLM
  Accuracy](https://arxiv.org/pdf/2311.07509) — data.world, the 16% to 54% result.
- [Spider 2.0](https://arxiv.org/abs/2411.07763) and [its annotation
  audit](https://arxiv.org/html/2601.08778v3) — enterprise-scale text-to-SQL and its benchmark
  caveats.
- [QueryGPT](https://www.uber.com/en-us/blog/query-gpt/) (Uber) and [Text-to-SQL for Enterprise Data
  Analytics](https://arxiv.org/pdf/2507.14372) (LinkedIn) — production text-to-SQL.
- [SharePoint document-level access in
  RAG](https://devblogs.microsoft.com/ise/sharepoint-doc-level-access/) — Microsoft ISE, ACL drift
  and re-indexing.
- [FIBO](https://edmcouncil.org/frameworks/industry-models/fibo/) — EDM Council financial industry
  ontology.
- [Palantir Ontology](https://www.palantir.com/docs/foundry/ontology/why-ontology) — semantic and
  kinetic elements.
- [LazyGraphRAG](https://www.microsoft.com/en-us/research/blog/lazygraphrag/) — the graph indexing
  cost change.
- [Open Semantic Interchange
  specification](https://www.snowflake.com/en/blog/open-semantic-interchanges-specs-finalized/) —
  the portable semantic model.
- [What's new in Unity Catalog, Data + AI Summit
  2026](https://www.databricks.com/blog/whats-new-unity-catalog-data-ai-summit-2026) — Databricks
  business semantics and AI Gateway.
- [AI's trillion-dollar opportunity: context
  graphs](https://ashugarg.substack.com/p/ais-trillion-dollar-opportunity-context) — Foundation
  Capital, decision traces.

Protocols, governance and financial services:

- [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog) —
  stateless protocol, gateway headers, caching fields and authorization changes.
- [FINRA 2026 oversight report
  summary](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)
  — Debevoise, agent risks and logging expectations.
- [OWASP Top 10 for Agentic Applications for
  2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026).
- [EU AI Act Digital Omnibus
  agreement](https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/)
  — Sidley, deferred high-risk deadlines.
- [SR 11-7](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm) and
  [DORA](https://eur-lex.europa.eu/eli/reg/2022/2554/oj) — model risk and ICT third-party risk
  baselines.
- [BlackRock Aladdin Copilot
  architecture](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)
  — plugin registry, tool filtering and evaluation-driven development.
- [Morgan Stanley customer story](https://openai.com/index/morgan-stanley/) — evaluation-led
  rollout.
- [S&P Global and Anthropic
  integration](https://press.spglobal.com/2025-07-15-S-P-Global-and-Anthropic-Announce-Integration-of-S-P-Globals-Trusted-Financial-Data-into-Claude)
  — per-user authenticated MCP access to licensed data.
- [Advancing Claude for Financial
  Services](https://www.anthropic.com/news/advancing-claude-for-financial-services) — LSEG, Moody's
  and other data connectors.
