# Practical techniques for efficient context management in production LLM agents

Research date: 26 October 2026. Each source carries its publication date where the page states one. "Measured" means a number from a stated evaluation, and "vendor claim" means a figure reported by the party selling the technique without an independent replication. Almost every number in this note is a vendor-reported internal evaluation; the only peer-review-style study with full tables is the JetBrains paper.

## Compaction and summarisation (Claude Code compaction, Anthropic context editing and memory tool, OpenAI Agents SDK sessions, Manus file system as context, observation masking versus LLM summarisation)

### Takeaway
Cheap, deterministic removal of old tool outputs (observation masking or tool-result clearing) delivers most of the cost benefit of LLM summarisation at lower cost and complexity, and summarisation adds a real risk of drift and longer trajectories. The strongest production pattern combines light clearing, occasional summarisation, and externalising state to files so that compression is restorable.

### Cited Findings
- Anthropic describes compaction in Claude Code as summarising the message history and starting a new context window with that summary, preserving architectural decisions, unresolved bugs and implementation details while discarding redundant tool outputs, and continuing with the five most recently accessed files (29 September 2025) — [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- The same post calls tool-result clearing "one of the lightest forms of compaction", because a raw tool result deep in the history is usually no longer needed (29 September 2025) — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic defines "context rot" as decreasing recall accuracy as the context window fills, a pattern it says appears across all models, and frames context as an "attention budget" that every token depletes (29 September 2025) — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic's context editing feature automatically clears stale tool calls and results when the conversation approaches token limits, and the memory tool lets Claude create, read, update and delete files in a client-side memory directory that persists across conversations; both launched in public beta on 29 September 2025 alongside Claude Sonnet 4.5's built-in context awareness — [Claude blog, Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)
- Vendor claim (internal evaluation): on an internal agentic search evaluation, memory tool plus context editing improved performance by 39% over baseline and context editing alone by 29%; on a 100-turn web search evaluation, context editing let agents finish workflows that otherwise failed from context exhaustion while cutting token consumption by 84% — [Claude blog, context management](https://claude.com/blog/context-management)
- The OpenAI Agents SDK cookbook presents two session strategies: `TrimmingSession` keeps the last `max_turns` user turns verbatim and drops older ones, which is deterministic, adds no latency and causes no summary drift, but can drop older constraints and IDs abruptly; `SummarizingSession` compresses older turns into a synthetic user/assistant pair once `context_limit` is exceeded while keeping `keep_last_n_turns` verbatim (default 3), which preserves long-range decisions but adds latency and cost and can lose or misweight details (page undated) — [OpenAI Cookbook, Session memory](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory)
- The cookbook lists the failure modes as context poisoning (an incorrect fact carried forward in a summary), summary drift, context amnesia under trimming, token spikes from large recent tool outputs, and compounding errors — [OpenAI Cookbook, Session memory](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory)
- Manus treats the sandbox file system as unlimited, persistent external memory and uses "restorable" compression: a web page's contents can be dropped from context as long as its URL is kept, and a document's contents as long as its file path is kept (18 July 2025, Yichao "Peak" Ji) — [Manus, Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Measured (JetBrains Research, "The Complexity Trap", Lindenbauer et al., arXiv 2508.21433, v1 29 August 2025, v3 27 October 2025): within SWE-agent on SWE-bench Verified across five model configurations, observation masking (rolling window of the last M=10 turns, older observations replaced with a placeholder) roughly halved cost relative to the raw agent and matched or slightly exceeded LLM summarisation (summarise N=21 turns at a time, keep last M=10 verbatim) on solve rate — [arXiv 2508.21433](https://arxiv.org/abs/2508.21433)
- Measured per-model results from that paper's Table 1 (solve rate, cost per instance): Qwen3-Coder 480B raw 53.4% / $1.29, masking 54.8% / $0.61, summary 53.8% / $0.64; Gemini 2.5 Flash raw 32.8% / $0.41, masking 35.6% / $0.18, summary 36.0% / $0.24; Gemini 2.5 Flash thinking raw 40.4% / $0.56, masking 36.4% / $0.24, summary 31.4% / $0.25; Qwen3-32B raw 17.0% / $1.12, masking 15.0% / $0.55, summary 16.0% / $0.50 — [arXiv 2508.21433v3 HTML](https://arxiv.org/html/2508.21433v3)
- Measured: LLM summarisation lengthened trajectories, with Qwen3-Coder 480B runs about 15% longer than the raw agent and 13% longer than masking, and Gemini 2.5 Flash summary runs averaging 52 turns versus 44 for masking; the authors attribute this to summaries hiding signals that would otherwise prompt the agent to stop — [arXiv 2508.21433v3 HTML](https://arxiv.org/html/2508.21433v3)
- Measured: the summariser's own API calls accounted for 0.65% to 7.20% of per-instance cost depending on the model (7.20% for Qwen3-Coder 480B) — [arXiv 2508.21433v3 HTML](https://arxiv.org/html/2508.21433v3)
- Measured: a tuned hybrid (masking with window 10, plus summarisation with N=43, M=10) on Qwen3-Coder 480B reached a solve rate 2.6 points above the raw agent and cost 7% less than masking and 11% less than summarisation, but with untuned settings the hybrid was less cost-efficient; on OpenHands the masking window had to be retuned before masking matched summarisation — [arXiv 2508.21433v3 HTML](https://arxiv.org/html/2508.21433v3)
- Cognition argues for a dedicated compression model that distils action history into key details, events and decisions, describes it as "hard to get right", and says it has fine-tuned smaller models for the task (12 June 2025) — [Cognition, Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents)

### Inferences
- The JetBrains results suggest that teams should start with observation masking or tool-result clearing as the default and add LLM summarisation only when long-range continuity is demonstrably lost, because summarisation costs a model call, lengthens runs and can introduce poisoned facts.
- Gains from both techniques are model-dependent; Gemini 2.5 Flash thinking lost solve rate under both strategies, so any adoption should be re-evaluated per model rather than assumed.
- Restorable compression (keeping a URL or file path in place of content) is a cheap way to make masking lossless in principle, since the agent can re-fetch what it needs.

### Gaps
- I did not find an official Anthropic document giving the exact auto-compact trigger threshold in Claude Code for current versions, so no threshold percentage is reported here.
- Anthropic's 29%, 39% and 84% figures come from undisclosed internal evaluations; I found no independent replication.
- The OpenAI cookbook page carries no publication date.

## Just-in-time retrieval versus up-front retrieval (agentic search versus vector RAG in coding agents)

### Takeaway
Coding agents have split into two camps: Claude Code and Cline rely on just-in-time agentic search (grep, glob, file reads), while Cursor indexes the codebase and reports that semantic search added to grep improves accuracy. The evidence favours a hybrid, with the caveat that every number is a vendor-internal benchmark.

### Cited Findings
- Anthropic distinguishes pre-inference embedding retrieval from just-in-time retrieval, in which the agent holds lightweight identifiers such as file paths, stored queries and links and loads data at runtime with tools (29 September 2025) — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Claude Code uses a hybrid model in which `CLAUDE.md` files are loaded up front and glob and grep retrieve other files just in time — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Cline states that it deliberately does not index codebases with embeddings, arguing that chunking code breaks its logic, that indexing creates secondary copies of code that widen the security surface, and that agentic exploration mirrors how a senior engineer reads a repository — [Cline blog, Why Cline doesn't index your codebase](https://cline.bot/blog/why-cline-doesnt-index-your-codebase-and-why-thats-a-good-thing)
- Vendor claim (internal benchmark): Cursor reports that adding its own trained embedding model and semantic search alongside grep gave on average 12.5% higher accuracy on Cursor Context Bench (6.5% to 23.5% depending on the model), plus improved code retention in an online A/B test (11 November 2025) — [Cursor, Improving agent with semantic search](https://cursor.com/blog/semsearch)
- Critics of the "no RAG" position point out that agentic search is itself a form of retrieval-augmented generation and that vector indexes still perform well on heterogeneous prose, where exact-match grep is weak — [jacar.es, Why many code agents use agentic search instead of a vector database](https://jacar.es/en/code-agents-without-vector-search/) (secondary commentary)

### Inferences
- Agentic search costs more turns and tokens per lookup but needs no index maintenance and avoids stale embeddings, which matters in fast-changing repositories.
- Vector retrieval appears most useful for conceptual queries where the agent does not know the identifier to grep for, which is consistent with Cursor's choice to add semantic search to grep rather than replace it.

### Gaps
- I found no independent, public benchmark that compares agentic search, vector RAG and a hybrid on the same coding tasks with token and latency costs.

## Memory (short-term versus long-term, Letta/MemGPT, Mem0, Zep/Graphiti, LangGraph, ChatGPT memory, instruction files, Agent Skills)

### Takeaway
Long-term memory systems replace full-history replay with selective retrieval and report large latency and token savings, but the benchmarks (LOCOMO, DMR, LongMemEval) are run by the vendors themselves. File-based instruction memory (CLAUDE.md, AGENTS.md) and progressively disclosed Skills are the simplest form and trade precision for transparency.

### Cited Findings
- Vendor-authored paper (Mem0, arXiv 2504.19413, 28 April 2025): on the LOCOMO benchmark Mem0 reports a 26% relative improvement in LLM-as-a-Judge score over OpenAI's memory, 91% lower p95 latency and more than 90% token-cost savings compared with full-context replay, and the graph-memory variant scores about 2% higher overall than the base configuration — [arXiv 2504.19413](https://arxiv.org/abs/2504.19413)
- The Mem0 paper reports a median total response time of 0.708 s and p95 of 1.440 s for Mem0, versus a median of 9.870 s and p95 of 17.117 s for a full-context baseline sending about 26,000 tokens per call — [arXiv 2504.19413 PDF](https://arxiv.org/pdf/2504.19413)
- Vendor-authored paper (Zep, arXiv 2501.13956, 20 January 2025): Zep's core engine Graphiti is a temporally aware knowledge graph; Zep reports 94.8% versus MemGPT's 93.4% on Deep Memory Retrieval, accuracy gains of up to 18.5% on LongMemEval, and 90% lower response latency than baseline implementations — [arXiv 2501.13956](https://arxiv.org/abs/2501.13956)
- The Mem0 and Zep claims are not mutually consistent as a leaderboard, because each paper selects its own baselines and benchmark; Mem0's marketing pages add further figures (for example 92.5% accuracy at about 6,956 tokens per retrieval) that do not appear in the paper — [Mem0 guide page](https://mem0.ai/guide/benchmarking-cost-difference-full-llm-context-compressed-memory)
- Anthropic's memory tool is file-based and client-side, so the developer controls the storage backend, and it is intended for building knowledge bases and maintaining project state across sessions (29 September 2025) — [Claude blog, context management](https://claude.com/blog/context-management)
- Anthropic describes structured note-taking with a Pokémon-playing agent that kept maps, progress counts and combat notes across thousands of game steps and resumed from those notes after context resets — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic Agent Skills (16 October 2025) use three levels of progressive disclosure: the skill's name and description are loaded into the system prompt at startup, the full `SKILL.md` is read only when the skill is judged relevant, and linked files are read only when needed, so the bundled context is "effectively unbounded"; the post warns that malicious skills can exfiltrate data and should be installed only from trusted sources — [Anthropic, Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### Inferences
- The memory products all solve the same problem as compaction (not replaying full history) but at the cross-session level, and their headline savings are measured against a full-context baseline, which is the weakest possible comparator.
- Instruction files and Skills give predictable, auditable context at the cost of manual curation; vector or graph memory gives automatic recall at the cost of opacity and retrieval errors.

### Gaps
- I did not fetch primary sources for Letta/MemGPT (the original MemGPT paper is arXiv 2310.08560, October 2023), LangGraph's short-term (thread checkpointer) and long-term (store) memory documentation, or ChatGPT's memory feature, so their mechanics and numbers are not reported here.
- I found no independent benchmark that evaluates Mem0, Zep and Letta under identical conditions.

## Tool design for context efficiency (tool count, descriptions, token-efficient outputs, MCP bloat, code execution with MCP, tool search, Cloudflare Code Mode)

### Takeaway
Tool definitions alone can consume tens of thousands of tokens before an agent starts work, and the two main remedies are deferred loading through tool search and letting the model write code against tools so that intermediate results never enter context. Both report large token reductions but add infrastructure, and code execution requires a secure sandbox.

### Cited Findings
- Vendor measurement: a five-server MCP setup (GitHub, Slack, Sentry, Grafana, Splunk) exposes 58 tools costing about 55K tokens before the conversation starts, GitHub alone costing about 26K tokens for 35 tools, and Anthropic observed tool definitions consuming 134K tokens before optimisation (24 November 2025) — [Anthropic, Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- Vendor claim: the Tool Search Tool cut context use from about 77K tokens to about 8.7K, which Anthropic calls an 85% reduction (the arithmetic is closer to 89%), and raised MCP evaluation accuracy with large tool libraries from 49% to 74% for Opus 4 and from 79.5% to 88.1% for Opus 4.5 — [Anthropic, advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- Vendor claim: Programmatic Tool Calling reduced average token usage on complex research tasks from 43,588 to 27,297 (37%) and improved GIA benchmark accuracy from 46.5% to 51.2%; tool use examples improved accuracy on complex parameter handling from 72% to 90% in internal tests — [Anthropic, advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- Anthropic's "code execution with MCP" (4 November 2025) presents MCP servers as a file tree of code APIs that the agent explores and imports on demand, filters large results in code before they reach the model, and keeps intermediate results in the execution environment; its Google Drive to Salesforce example drops from about 150,000 tokens to about 2,000 (98.7%) — [Anthropic, Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- The same post states that running agent-generated code requires sandboxing, resource limits and monitoring, which adds operational overhead and security considerations that direct tool calls avoid — [Anthropic, Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- Cloudflare Code Mode (26 September 2025, Kenton Varda and Sunil Pai) converts an MCP server's schema into a TypeScript API, gives the agent a single tool that runs TypeScript in a fresh V8 isolate with no internet access, and routes calls through bindings so that generated code never handles API keys; the authors argue that models have seen far more real TypeScript than synthetic tool-call examples, but the post reports no benchmarks, and the full TypeScript API is still loaded into context — [Cloudflare, Code Mode](https://blog.cloudflare.com/code-mode/)
- Anthropic names bloated tool sets as a common failure mode and recommends tools that are self-contained, robust to errors, minimally overlapping and clear about their intended use — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Inferences
- Tool search addresses the cost of tool definitions, while code execution addresses the cost of tool results; the two are complementary rather than alternatives.
- Dynamically loading tool definitions interacts with prompt caching, because tool definitions sit at the front of the cache prefix (see the caching section), so deferred loading must append definitions rather than rewrite the tool list.

### Gaps
- None of the token-reduction figures in this section were independently replicated, and Cloudflare published no quantitative results.

## Sub-agents and multi-agent context isolation

### Takeaway
Sub-agents help when work is genuinely parallel and read-heavy, such as breadth-first research, because each sub-agent explores in its own window and returns a short summary. They cost many more tokens and fail when sub-tasks share hidden decisions, which is the core of Cognition's counter-argument.

### Cited Findings
- Vendor claim (internal research evaluation): a multi-agent system with Claude Opus 4 as lead and Claude Sonnet 4 sub-agents outperformed single-agent Claude Opus 4 by 90.2% (13 June 2025) — [Anthropic, How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Anthropic reports that agents use about 4 times the tokens of chat and multi-agent systems about 15 times, and that on BrowseComp token usage alone explains about 80% of performance variance (95% with tool-call count and model choice), concluding that multi-agent systems "work mainly because they help spend enough tokens to solve the problem" — [Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Anthropic states that multi-agent designs fit poorly when all agents need the same context or have many dependencies, including most coding tasks, and lists early failures such as spawning 50 sub-agents for simple queries — [Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Anthropic describes sub-agents that may spend tens of thousands of tokens exploring but return a condensed summary of often 1,000 to 2,000 tokens to the lead agent — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Cognition (Walden Yan, 12 June 2025) argues for two principles, "share context, and share full agent traces, not just individual messages" and "actions carry implicit decisions", illustrated by a Flappy Bird task split between sub-agents that produced a Mario-style background and a mismatched bird; it recommends a single-threaded linear agent, optionally with a compression model, while saying it is optimistic about multi-agent collaboration in the long term — [Cognition, Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents)

### Inferences
- The two positions are compatible: isolation helps for read-only, parallelisable exploration whose output is a summary, and hurts for write-heavy work where sub-agents make conflicting decisions.
- Because the 90.2% gain coincides with roughly 15 times the token spend, it should be read as evidence that spending more tokens in parallel helps on research, not as a free efficiency gain.

### Gaps
- I found no independent replication of the 90.2% figure, and the internal evaluation set is not public.

## Prompt and KV caching (pricing, KV-cache hit rate, stable prefix, append-only context, tool masking)

### Takeaway
Caching is the largest single cost lever for agents because agent input-to-output ratios are extreme, and it works only if the context prefix is stable and append-only. Providers now discount cached reads by roughly 90% or more, with write premiums on Anthropic and newer OpenAI models.

### Cited Findings
- Manus calls KV-cache hit rate "the single most important metric" for a production agent, reports an average input-to-output ratio of about 100:1, and cites Claude Sonnet cached input at $0.30 per million tokens versus $3 uncached (18 July 2025) — [Manus, Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Manus recommends keeping the prompt prefix stable (no second-precision timestamps at the start), making context append-only, serialising deterministically because JSON key order may vary, marking cache breakpoints explicitly, and enabling vLLM prefix caching with session-ID routing when self-hosting — [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Manus masks tool availability by constraining token logits through a state machine instead of removing tool definitions, which would break the cache and confuse the model, and gives tools shared prefixes such as `browser_` and `shell_` so groups can be constrained together — [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Anthropic's current pricing charges 1.25 times base input for a 5-minute cache write and 2 times for a 1-hour write, and 0.1 times for reads on most models (0.05 times for Opus 5.5 and Sonnet 5.5); it allows up to four breakpoints, and the prefix order is tools, then system, then messages, so changing tool definitions invalidates the whole cache (accessed 26 October 2026) — [Claude docs, Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- OpenAI caching is automatic for prefixes of at least 1,024 tokens, with discounts on cached input of up to 95%; for GPT-5.6 and later a 30-minute write costs 1.25 times and a 12-hour write 2.5 times the uncached rate, with reads at 0.1 times, while earlier models had no write charge (accessed 26 October 2026) — [OpenAI docs, Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
- Gemini implicit caching is on by default for Gemini 2.5 and newer models with a minimum of 2,048 input tokens for 2.5 Flash and Pro, but the caching page I read does not state the discount rate — [Google, Gemini API context caching](https://ai.google.dev/gemini-api/docs/caching)

### Inferences
- Any context-editing technique that rewrites earlier messages (summarisation, clearing, tool removal) invalidates the cache from that point, so its token savings must be weighed against the loss of cached-read discounts; this is a likely reason Manus prefers append-only context and logit masking.

### Gaps
- I could not verify the current Gemini cached-token discount from the official page, and third-party pricing comparisons I found contradicted each other, so I have excluded them.

## Structured note-taking, todo-list recitation and keeping errors in context

### Takeaway
Agents that rewrite a todo list keep goals in recent attention, and agents that see their own failures avoid repeating them; both are supported by practitioner reports rather than controlled measurements.

### Cited Findings
- Manus has the agent continually rewrite a `todo.md` file so that goals stay in the most recent part of the context, noting that a typical task needs about 50 tool calls — [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Manus leaves failed actions and stack traces in context so that the model can update its beliefs, and adds controlled variation in serialisation and phrasing to stop the agent imitating repetitive action patterns (for example when reviewing 20 resumes) — [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Anthropic's structured note-taking example (the Pokémon agent) shows notes surviving context resets and being read back to continue work — [Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Inferences
- Keeping errors in context sits in tension with observation masking; a practical compromise is to mask bulky successful outputs while retaining short error summaries.

### Gaps
- I found no controlled study that quantifies the benefit of todo recitation or of retaining errors.

## Evaluation and observability of context (token budgets, context tracing)

### Takeaway
The available guidance points to a small set of metrics, namely cache hit rate, tokens per task, trajectory length and solve rate, but I found little published tooling-specific evidence within the call budget.

### Cited Findings
- Anthropic's API exposes `cache_creation_input_tokens` and `cache_read_input_tokens` on each response so that teams can confirm whether caching occurred — [Claude docs, Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- Anthropic's finding that token usage explains about 80% of BrowseComp performance variance implies that token spend per task should be tracked alongside quality — [Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- The JetBrains study shows that trajectory length and summariser cost share are necessary metrics, because a technique can lower per-turn cost while lengthening runs — [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)
- The OpenAI cookbook notes that summarisation makes observability harder because summary prompts and outputs must be logged to debug drift — [OpenAI Cookbook, Session memory](https://developers.openai.com/cookbook/examples/agents_sdk/session_memory)

### Inferences
- A minimal context dashboard would track tokens per task, cached-read share, context-window fill at each turn, number of compaction events and task success, broken down by model.

### Gaps
- I did not research tracing products such as LangSmith, Langfuse or OpenTelemetry GenAI conventions within the call budget, so their capabilities are not covered here.
