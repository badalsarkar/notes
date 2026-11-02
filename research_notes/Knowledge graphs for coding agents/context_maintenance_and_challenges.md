# Context Maintenance, Evaluation and Challenges for Agentic Code Generation

Research date: 2026-10-29. Items dated before 2026 are marked as older information. Numbers come from the cited source and were not independently replicated unless stated.

## Context engineering: definition, techniques, and context rot

### Takeaway
Vendors such as Anthropic, Manus and Cognition describe context engineering as curating the smallest high-signal set of tokens at every model call, using just-in-time retrieval, compaction, external notes and isolated sub-agents. Independent benchmarks (Chroma, NoLiMa, LongCodeBench, Lost in the Middle) consistently show that accuracy drops as input grows, even well below advertised window sizes, which is the main justification for these techniques.

### Cited Findings
- Anthropic defines context engineering as curating and maintaining the optimal set of tokens during inference, including everything beyond the prompt, and treats it as the successor to prompt engineering for multi-turn agents (published 2025-09-29, older info). — [Anthropic: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic describes "context rot" as the drop in a model's ability to recall information as the token count grows, and ties it to the n² pairwise attention relationships in transformers. Its framing is that context is a finite "attention budget" with diminishing returns. — [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Anthropic lists the following techniques. — [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  - In just-in-time retrieval, the agent holds lightweight identifiers such as file paths, queries or URLs and loads the data at runtime with tools. Claude Code does this with `grep`, `head` and `tail` instead of pre-indexing everything, and a hybrid of some up-front retrieval plus exploration is also described.
  - In progressive disclosure, the agent discovers context step by step, using signals such as file names, sizes and timestamps to decide what to read next.
  - In compaction, a conversation near the window limit is summarized and restarted from the summary. Claude Code keeps the summary plus the five most recently accessed files, and Anthropic advises tuning compaction for recall first and then precision.
  - Tool-result clearing removes old raw tool outputs and is described as the lightest-touch form of compaction. It shipped on the Claude Developer Platform.
  - In structured note-taking, the agent writes memory outside the window and reloads it later. A Claude Pokémon run tracked progress across 1,234 steps this way, and a memory tool entered public beta with Sonnet 4.5.
  - In sub-agent isolation, sub-agents may use tens of thousands of tokens each but return condensed summaries of about 1,000 to 2,000 tokens to a lead agent.
- Manus (2025-07-18, older info) names the KV-cache hit rate as the single most important production metric. Cached Claude Sonnet input costs $0.30 per million tokens versus $3 per million uncached, a 10x difference. — [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Manus reports an average input-to-output token ratio of about 100:1 and about 50 tool calls for a typical task. — [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Manus keeps prefixes stable and context append-only for cache reuse. It masks tool logits instead of adding or removing tools mid-task, uses the file system as restorable external memory (dropping a page but keeping its URL), and rewrites a `todo.md` file to put the plan at the end of the context to reduce goal drift. It also keeps failed actions and stack traces in context so the model avoids repeating them. Manus gives no effect sizes for these practices. — [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Cognition (Walden Yan, 2025-06-12, older info) calls context engineering "effectively the #1 job of engineers building AI agents." It argues that sub-agents should share full context and traces because "actions carry implicit decisions," and that parallel agents acting on conflicting assumptions produce inconsistent results. — [Cognition: Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents)
- Cognition proposes a dedicated, possibly fine-tuned compression model that summarizes history into key decisions and events, and says this is hard to get right. It also notes that Claude Code sub-agents (as of June 2025) answer narrow questions rather than write code and do not run in parallel with the main agent. — [Cognition](https://cognition.com/blog/dont-build-multi-agents)
- Chroma's "Context Rot" report (2025-07-14, older info) tested 18 LLMs and found that "model performance consistently degrades with increasing input length" across all experiments. — [Chroma: Context Rot](https://www.trychroma.com/research/context-rot)
  - Degradation was faster when the needle and the question had lower semantic similarity.
  - One distractor reduced accuracy relative to the needle-only baseline, and four distractors compounded the drop. GPT models hallucinated most often, while Claude models tended to abstain.
  - Counterintuitively, shuffled (incoherent) haystacks produced better performance than logically structured ones in all 18 models.
  - On LongMemEval (306 prompts), focused prompts of about 300 tokens beat full prompts of about 113k tokens for every model.
  - On a repeated-words task from 25 to 10,000 words, performance declined for all models.
- NoLiMa (ICML 2025, older info) evaluated 13 models that claim at least 128K context. They perform well below 1K tokens but degrade significantly as length grows when the needle requires a non-literal (latent) association. On the hard subset, Llama 3.3 70B fell from 98.3 to 8.9 at 32K tokens. — [NoLiMa arXiv](https://arxiv.org/html/2502.05167v3); [NoLiMa dataset README](https://huggingface.co/datasets/amodaresi/NoLiMa/blob/main/README.md?code=true)
- A secondary review of NoLiMa says many models fell below 50% of their short-context baseline at 32K tokens. This figure is from an aggregator and not verified against the paper table. — [ICML poster page](https://icml.cc/virtual/2025/poster/46685); [Moonlight review](https://themoonlight.io//fr/review/nolima-long-context-evaluation-beyond-literal-matching)
- LongCodeBench (2025, older info) tests code QA and bug fixing on real GitHub issues at up to 1M tokens. As reported, Claude 3.5 Sonnet fell from 29% to 3% and Qwen2.5 from 70.2% to 40% as context grew. These figures come from a secondary summary. — [sotaverified: LongCodeBench](https://sotaverified.org/papers/longcodebench-evaluating-coding-llms-at-1m)
- "Lost in the Middle" (Liu et al., TACL, 2023, older info) found a U-shaped curve in which models do best when the relevant document is at the start or end of the context. For GPT-3.5-Turbo, accuracy with the answer in the middle was below its closed-book accuracy with no documents. — [arXiv 2307.03172](https://arxiv.org/abs/2307.03172v3)
- Secondary posts put the mid-context drop at roughly 20 percentage points, but they do not cite a table. — [dev.to summary](https://dev.to/a3e_ecosystem/liu-et-al-2023-lost-in-the-middle-tacl-found-multi-document-qa-accuracy-drops-roughly-20-3l8f)
- Chroma found no notable needle-position effect on its basic NIAH task. This partly conflicts with the strong position effect in Lost in the Middle, and the likely cause is the newer models and the different task design. — [Chroma](https://www.trychroma.com/research/context-rot)

### Inferences
- The benchmark evidence suggests that adding more repository context to a prompt has a cost in accuracy as well as tokens. This supports retrieval-on-demand and summarization over "stuff the window" approaches, especially for code, where distractors (similar functions and older versions of APIs) are common.
- The Manus cost figures imply that the context layout (stable prefix, append-only history) affects cost as much as the content selection does. This creates a tension with tool-result clearing and compaction, which rewrite the history and break the cache.
- The Cognition and Anthropic positions differ in emphasis. Cognition favors a single agent with shared context, while Anthropic endorses sub-agents that return compressed summaries. Both agree that sub-agents lose context that the parent holds.

### Gaps
- I did not fetch RULER directly. Its widely cited conclusion, that the effective context length of most models is far below their claimed length, is not given a source here.
- No vendor publishes effect sizes for compaction or note-taking on coding benchmarks in the sources reviewed.

## Keeping knowledge fresh: re-indexing, sync, temporal graphs, generated docs, drift

### Takeaway
Cursor publishes the most concrete freshness mechanism, a Merkle tree of file hashes that re-embeds only changed chunks and reuses teammates' indexes. Temporal knowledge graphs (Zep/Graphiti) model when facts were valid. Auto-generated wikis such as DeepWiki have reported staleness and accuracy problems, and I found no public vendor statement on DeepWiki's refresh policy.

### Cited Findings
- Cursor (Jeremy Stribling, 2026-01-27) builds a semantic index when a project opens. Semantic search improved response accuracy by 12.5% on average in Cursor's evaluation, and the index is unusable until at least 80% of it is built. Large repositories can take hours to index. — [Cursor: Securely indexing large codebases](https://cursor.com/blog/secure-codebase-indexing)
- Cursor hashes every file and folder into a Merkle tree, compares trees, and syncs only the changed branches. For a 50,000-file workspace the hashes and names total about 3.2 MB. Changed files are split into syntactic chunks, and the embeddings are cached by chunk content so that unchanged chunks are not recomputed. — [Cursor](https://cursor.com/blog/secure-codebase-indexing)
- Cursor computes a simhash of the client's tree and copies an existing team index when the similarity exceeds a threshold. Clones within an organization average 92% similarity. — [Cursor](https://cursor.com/blog/secure-codebase-indexing)
  - The median time-to-first-query fell from 7.87 seconds to 525 milliseconds.
  - The 90th percentile fell from 2.82 minutes to 1.87 seconds.
  - The 99th percentile fell from 4.03 hours to 21 seconds.
- Cursor's sync is also an access control. A client can only produce a hash if it holds the file, and the server drops search results that the client cannot prove it has. The article does not describe branch handling or the sync interval. — [Cursor](https://cursor.com/blog/secure-codebase-indexing)
- Zep/Graphiti (arXiv 2501.13956, January 2025, older info) is a bi-temporal knowledge graph. It records when a fact was valid in the world and when the agent ingested it, so facts that have been superseded can be invalidated instead of deleted. — [Zep paper](https://arxiv.org/abs/2501.13956v1); [Zep blog](https://blog.getzep.com/zep-a-temporal-knowledge-graph-architecture-for-agent-memory)
- Zep reports the following vendor results. — [Zep: State of the Art in Agent Memory](https://blog.getzep.com/state-of-the-art-agent-memory/)
  - On DMR, Zep scored 94.8% against 93.4% for MemGPT.
  - On LongMemEval, Zep scored 71.2% and 63.8% (GPT-4o and GPT-4o-mini) against 60.2% and 55.4% for full context.
  - The headline claim is up to 18.5% better accuracy with 90% lower latency.
  - The authors concede that DMR is too easy for modern context windows, and I found no independent replication.
- An OpenWrt maintainer reported that DeepWiki pages are not regenerated after a repository changes, cannot be removed, and contained incorrect descriptions of configuration options. A vendor-style comparison claims that a "Last indexed" date stamp shows re-indexing. The two sources conflict. — [OpenWrt forum](https://forum.openwrt.org/t/important-consideration-deepwiki-ai-generated-docs-may-contain-inaccuracies/249471); [SSOJet comparison](https://ssojet.com/blog/ai-documentation-generators)
- A documentation practitioner argues that AI code wikis are useful for exploring poorly documented code but range from dry reference material to hallucinations on complex projects, and calls them "documentation theater." — [passo.uno](https://passo.uno/ai-wikis-docs-teather-as-a-service/)
- A community Claude Code plugin (driftwiki) adds a drift-check script because the DeepWiki-style generator it forked "only generates, never detects drift," and its citations had line numbers that did not match the code. — [driftwiki listing](https://www.remoteopenclaw.com/plugins/dpviivqb-driftwiki/driftwiki)
- An empirical study of 2,303 agent context files from 1,925 repositories (Claude Code, Codex, Copilot) examined their structure, content and maintenance. This is a descriptive study, not a performance study, and only the abstract-level facts were checked. — [Agent READMEs, arXiv 2511.12884](https://arxiv.org/pdf/2511.12884)

### Inferences
- Content-addressed hashing (Merkle trees and per-chunk embedding caches) is the established way to make re-indexing incremental, and the same mechanism doubles as proof of access.
- Generated prose artifacts (wikis and LLM-written AGENTS.md files) have no equivalent change detection unless a team adds a drift check, so they go stale silently. Temporal graphs address staleness for facts but add ingestion complexity.

### Gaps
- I found no primary source on branch-aware indexes, such as how Sourcegraph or Augment handle per-branch embeddings, within the tool-call budget.
- I found no published data on who owns rules files in organizations, or on how often they are updated. The Agent READMEs paper may contain this, but it was not read in full.
- I found no official DeepWiki documentation on its refresh cadence.

## Feedback loops, memory systems, and memory poisoning

### Takeaway
Review tools such as Greptile learn from which PR comments developers act on and from their reactions, and they report vendor-only gains in the share of comments that get addressed. Persistent context (rules files and memory) is also a persistence mechanism for attackers, as Pillar's "Rules File Backdoor" showed.

### Cited Findings
- Greptile infers which of its comments authors acted on by comparing a PR's first and last commits, and it learns from thumbs-up and thumbs-down reactions. — [Greptile docs: memory and learning](https://www.greptile.com/docs/how-greptile-works/memory-and-learning)
- Greptile claims an 80% reduction in ignored comments and a 3x higher adoption rate for suggestions. These are vendor numbers. — [Greptile learning page](https://www.greptile.com/learning)
- Third-party sites attribute v4 figures to Greptile: the share of comments addressed rose from 30% to 43%, and comments addressed per PR rose from 0.92 to 1.60. These figures were not verified at the primary source. — [aicodereview.cc Greptile review](https://aicodereview.cc/tool/greptile/)
- Comparative bug-catch benchmarks between CodeRabbit and Greptile conflict across secondary sources, with the 82% and 44% figures assigned to opposite tools. They should not be used. — [getpanto.ai](https://www.getpanto.ai/blogs/coderabbit-vs-greptile-ai-code-review-tools-compared); [aicodereview.cc](https://aicodereview.cc/blog/coderabbit-vs-greptile)
- Pillar Security (March 2025, older info) showed that hidden instructions in Cursor and Copilot rules files, using invisible Unicode and semantic hijacking, can make the agent insert malicious scripts and hide the change from the developer. — [Pillar Security](https://pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents)
  - Poisoned rules persist across all future generations and survive forking.
  - Poisoned rules can spread through project templates and shared internal rule repositories.
  - Cursor and GitHub responded that reviewing the output is the user's responsibility.
  - Pillar recommends treating AI config files like executable code and auditing them for invisible characters.

### Inferences
- Self-updating rules and memories create a write path from untrusted inputs (issues, PR comments, tool output) into persistent context. Any automated learning loop therefore needs review and provenance controls similar to those for code changes.

### Gaps
- I found no peer-reviewed study measuring accuracy gains from self-updating rules files or agent memory in coding specifically.
- I found no documented real-world incident of memory poisoning in a coding agent, as opposed to proof-of-concept research, within the budget.

## Evaluation: measuring whether context helps, and the AGENTS.md studies

### Takeaway
The 2026 controlled studies find that AGENTS.md-style context files do not reliably raise task success. LLM-generated files slightly hurt success and add about 20% to cost, while developer-written files give a small, non-significant gain. One study finds efficiency gains (28.6% faster median runtime). Organizations otherwise rely on internal evals, SWE-bench-style harnesses and adoption metrics such as acceptance rate and comments addressed.

### Cited Findings
- Gloaguen, Mündler, Müller, Raychev and Vechev ("Evaluating AGENTS.md", arXiv 2602.11988, v1 2026-02-12, v3 2026-09-29) found that context files "do not generally improve task success rates" and raise inference cost by over 20% on average across agents and models. — [arXiv abstract](https://arxiv.org/abs/2602.11988)
  - The settings were SWE-bench Lite (300 tasks, 11 repositories) with LLM-generated files and the new CTXbench (138 instances, 12 Python repositories) with developer-committed files. — [arXiv v3 HTML](https://arxiv.org/html/2602.11988v3)
  - The per-agent changes in resolution rate, in percentage points against no file, are shown below for SWE-bench with an LLM file, CTXbench with an LLM file, and CTXbench with a developer file. — [v3 HTML](https://arxiv.org/html/2602.11988v3)
    - Claude Code with Sonnet-4.5 scored −1.2, −8.0 and −2.9.
    - Codex with GPT-5.2 scored −2.2, +2.9 and +2.9.
    - Codex with GPT-5.1 mini scored −0.1, −3.6 and +1.5.
    - Qwen Code with Qwen3-30B scored +1.3, +1.4 and +7.9.
  - LLM-generated files reduced resolution by about 0.5 points on SWE-bench and 2 points on CTXbench, which is not significant. Developer files gave +2.4 points on CTXbench (p = 0.21), which is significantly better than the LLM-generated files (p = 0.038). LLM-generated files helped (+2.7 points) only when all other documentation was removed. — [v3 HTML](https://arxiv.org/html/2602.11988v3)
  - LLM-generated files added 2.45 to 3.92 steps and about 20 to 23% cost, and developer files added 3.34 steps and up to 19% cost. Reasoning tokens rose by up to 22% for GPT-5.2. — [v3 HTML](https://arxiv.org/html/2602.11988v3)
  - Codebase overviews appeared in 95 to 100% of files generated by the stronger models and in 8 of the 12 developer files, but they did not reduce the steps needed to reach the files the reference patch modified. — [v3 HTML](https://arxiv.org/html/2602.11988v3)
  - Agents obey the files. For example, `uv` was used 1.6 times per instance when mentioned versus fewer than 0.01 times when not. — [v3 HTML](https://arxiv.org/html/2602.11988v3)
  - The authors recommend omitting LLM-generated context files for now and limiting human-written files to non-obvious requirements such as conventions and non-functional constraints. — [v3 HTML](https://arxiv.org/html/2602.11988v3)
  - The v1 abstract wording was more negative (it said the files "tend to reduce" success), and the wording was softened in later versions. — [arXiv v1](https://arxiv.org/abs/2602.11988v1)
- Lulla, Mohsenimofidi, Galster, Zhang, Baltes and Treude (arXiv 2601.20404, January 2026, revised March 2026) studied 10 repositories and 124 PR tasks. AGENTS.md was associated with a 28.64% lower median runtime and 16.58% fewer output tokens, with comparable task completion. — [arXiv 2601.20404](https://arxiv.org/abs/2601.20404)
- The cost results conflict. Gloaguen et al. find that context files increase cost and steps, while Lulla et al. find that they reduce runtime and output tokens. The two studies differ in agents, metrics (total cost versus output tokens and wall-clock time) and tasks. — [Gloaguen](https://arxiv.org/abs/2602.11988); [Lulla](https://arxiv.org/abs/2601.20404)
- Khatri ("Do Context Files Help Coding Agents?", arXiv 2607.27250, 2026-07-28) ran Claude Code (sonnet-4-6) and Codex CLI (gpt-5.5) on real merged PRs from 3 Python repositories, with 291 runs in total. — [arXiv 2607.27250](https://arxiv.org/html/2607.27250v1)
  - Claude passed 53.3% with no file and 55.6% with both always-on and selective files. Codex passed 58.8%, 56.9% and 52.9%.
  - There was no strategy effect (p = 1.00 and 0.66), and the minimum detectable effect was above 30 percentage points.
  - Failures came from implementation skill (architectural choice, exact wiring and engineering precision) rather than missing repository knowledge.
  - The real AGENTS.md never turned a near-miss into a pass.
- Cursor measures its context subsystem through internal evals and reports a 12.5% average accuracy improvement from semantic search. — [Cursor](https://cursor.com/blog/secure-codebase-indexing)
- Greptile uses the share of comments addressed as its outcome metric for learned context. — [Greptile docs](https://www.greptile.com/docs/how-greptile-works/memory-and-learning)

### Inferences
- The small effects (a few points), the high variance and the underpowered samples mean that teams cannot judge the value of context files without their own repeated, task-level evals. Gloaguen's own recommendation is to evaluate rigorously before adoption.
- The evidence favors short, human-written files limited to non-obvious conventions and tooling. Those files demonstrably change agent behavior, while general overviews cost tokens without improving navigation.

### Gaps
- I found no published organizational data linking context quality to PR merge rate or post-merge defect rate.
- I found no public acceptance-rate breakdown by context source from GitHub Copilot or Sourcegraph within the budget.

## Challenges: hallucinated APIs and packages, conflicting knowledge, pipeline security, cost, boundaries, tacit knowledge

### Takeaway
Package hallucination is common and repeatable, which makes it exploitable (slopsquatting). Prompt injection through repository content, issues and MCP tool descriptions can exfiltrate private code, and the root cause is over-broad access. Cost and latency are driven by context size and cache behavior. Tacit knowledge remains largely unaddressed by context files, and implementation skill is a separate bottleneck.

### Cited Findings
- Spracklen et al. (USENIX Security 2025, older info) generated 576,000 Python and JavaScript samples across 16 models. — [Dark Reading](https://www.darkreading.com/application-security/ai-code-tools-widely-hallucinate-packages); [Socket](https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks)
  - 19.7% of the recommended packages did not exist, with 205,474 unique fake names.
  - Open-source models averaged 21.7% and commercial models about 5.2%. GPT-4 Turbo had the lowest rate at 3.59%, and CodeLlama was above 30%.
  - Across ten re-runs of the same prompt, 43% of hallucinated packages recurred every time and 39% never recurred.
  - Only 13% of the fake names were off-by-one typos.
  - Top models identified their own hallucinations with more than 80% accuracy.
- The Cloud Security Alliance frames slopsquatting as a supply-chain vector. Mitigations it discusses include retrieval augmentation, self-refinement and registry checks. — [CSA research note](https://labs.cloudsecurityalliance.org/research-rb/csa-research-note-slopsquatting-ai-coding-assistant-supply-c/)
- Invariant Labs (May 2025, older info) showed that a malicious public GitHub issue could hijack an agent using the official GitHub MCP server into leaking private repository data into a public PR. The attack needed no server bug and relied on prompt injection plus a broad personal access token. Invariant calls it a "toxic agent flow." — [Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability); [DevClass](https://devclass.com/2025/05/27/researchers-warn-of-prompt-injection-vulnerability-in-github-mcp-with-no-obvious-fix/)
- Invariant's April 2025 tool-poisoning research showed that a single poisoned MCP tool description could exfiltrate data. A 2025 scan cited by Wallarm found tool poisoning in about 5.5% of 1,899 public MCP servers. This figure is secondary. — [Wallarm](https://lab.wallarm.com/attacking-the-mcp-trust-boundary)
- The proposed mitigations are least-privilege, per-repository tokens, MCP traffic scanning, and limiting the agent to content from users with push access. Simon Willison is quoted as saying "we still don't have convincing mitigations." — [Docker blog](https://www.docker.com/blog/mcp-horror-stories-github-prompt-injection/); [DevClass](https://devclass.com/2025/05/27/researchers-warn-of-prompt-injection-vulnerability-in-github-mcp-with-no-obvious-fix/)
- Cursor's index is an example of permission-aware retrieval. Results are filtered to files that the client can prove it holds through content hashes. — [Cursor](https://cursor.com/blog/secure-codebase-indexing)
- Context files add 2.45 to 3.92 steps and about 20% cost per task. Manus reports a 10x price gap between cached and uncached tokens and a 100:1 input-to-output ratio, so input context dominates spend. — [Gloaguen v3](https://arxiv.org/html/2602.11988v3); [Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- Chroma's distractor results show that semantically similar but wrong content measurably lowers accuracy, which applies directly to outdated or conflicting docs that sit in context next to current ones. — [Chroma](https://www.trychroma.com/research/context-rot)
- Khatri attributes the remaining failures to design judgment and exact wiring, which are tacit, skill-type knowledge that static context files did not fix. — [arXiv 2607.27250](https://arxiv.org/html/2607.27250v1)
- Cognition argues that decisions made in one agent are invisible to parallel agents unless their full traces are shared. This failure mode also applies across repositories and teams. — [Cognition](https://cognition.com/blog/dont-build-multi-agents)

### Inferences
- Because 43% of hallucinated package names recur every time, attackers can predict and pre-register them. Registry existence checks and allow-lists in the agent loop are cheap defenses.
- Every retrieval source (issues, wikis, MCP tool metadata and rules files) is an injection surface. Scoping access per task and per repository is the most concrete mitigation documented.

### Gaps
- I did not fetch the OWASP LLM Top 10 (2025) or Trail of Bits MCP research directly, so their specific recommendations are not cited.
- I found no quantitative study of multi-repository boundary failures, such as cross-service API contract errors, for coding agents.
- I found no source quantifying hallucinated API usage (as distinct from package names) against fresh versus stale documentation within the budget.
