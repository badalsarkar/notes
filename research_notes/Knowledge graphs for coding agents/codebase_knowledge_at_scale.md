# Codebase knowledge at scale: how coding agents represent, index, and retrieve large codebases

Research date: 2026-10-29. Items dated before 2025 are marked **[pre-2025]**. Items marked **[prior knowledge, not re-fetched]** come from the researcher's background knowledge with a primary-source URL that was not re-opened in this session; the report writer should treat them as lower confidence.

## What are the main approaches and how does each work?

### Takeaway
Production agents use five families of technique: embedding retrieval over code chunks, lexical or agentic search with grep-style tools, compressed repository maps, precise symbol indexes (SCIP, LSIF, Glean, Kythe), and code or knowledge graphs. Most serious systems by 2026 are hybrids, and the main differences between vendors are about which of these is the default and whether an index is built ahead of time.

### Cited Findings

**Embedding / vector RAG over chunks**
- Cursor trains its own embedding model on agent session traces: an LLM ranks which content would have been most helpful at each step of a trace, and the embedding model is trained so that its similarity scores match those rankings (Nov 6, 2025). — [Cursor, Improving agent with semantic search](https://cursor.com/blog/semsearch)
- Cursor's docs say semantic search becomes available once indexing reaches 80%, the index re-syncs every 5 minutes processing only changed files, and excluding large generated or content files improves accuracy. — [Cursor docs mirror (search tool)](https://techdevnotes.com/releases/cursor-docs/20260626-202020Z-6c7064724f5e/content/pages/agent/tools/search.txt) (third-party mirror of Cursor docs)
- Greptile argues that natural-language queries and code do not land near each other in embedding space, and reports that translating code to natural language before embedding works better; its pipeline parses the AST, recursively generates docstrings per node, and embeds the docstrings, treating the codebase as a graph rather than a list of files. — [Greptile, Codebases are uniquely hard to search semantically](https://www.greptile.com/blog/semantic-codebase-search)
- Cognition summarises the weakness of embedding search as being fast after indexing but inaccurate on multi-hop queries, and able to inject irrelevant content that the agent overweights. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)

**Lexical / agentic search (grep, glob, read)**
- Claude Code's creator Boris Cherny said early versions used RAG with a local vector database, and the team switched to agentic search (grep, glob, file reads) because it worked better; his stated evidence was mainly qualitative ("vibes"), plus index staleness and security/privacy concerns, with the trade-off being latency and tokens (Latent Space podcast, May 2025, reported secondhand). — [OfficeChai summary](https://officechai.com/ai/claude-researcher-explains-how-agentic-search-performed-better-than-rag-for-code-generation/); [dev.to summary](https://dev.to/chen115y/the-representation-problem-why-rag-vs-agentic-search-is-the-wrong-debate-4j8f)
- Cognition describes agentic search as flexible but slow, often needing dozens of sequential round trips, and as flooding the agent with irrelevant tokens. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)
- Sourcegraph's BM25F work ranks matches in file names and symbol definitions above comments; it reports a roughly 20% improvement in code search relevance and says BM25 held up against modern embeddings in internal evaluations. — [Sourcegraph, Keeping it boring (and relevant) with BM25F (mirror)](https://www.plushcap.com/content/sourcegraph/blog/sourcegraph-keeping-it-boring-and-relevant-with-bm25f)

**RL-trained retrieval subagents (a variant of agentic search)**
- Cognition's SWE-grep and SWE-grep-mini (Oct 16, 2025) are small models trained with multi-turn RL to retrieve files and line ranges, used as Windsurf's "Fast Context" subagent. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)
- The reward is the average of weighted F1 over file retrieval and line retrieval, using F-beta with beta = 0.5 to favour precision, because context pollution is judged more harmful than missing context. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)
- The models issue up to 8 parallel tool calls per turn for at most 4 turns (3 exploration, 1 answer), compared with 10 to 20 serial turns for typical agentic search; going from 4 to 8 parallel calls reduced turns from 6 to 4 at equal performance. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)
- The tool set is restricted to grep, read, glob and similar, and the subagent returns file and line lists rather than summaries so that results are verifiable and the reward is deterministic. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)

**Repository maps (Aider)** **[pre-2025]**
- Aider (Oct 2023) sends the model a concise map of the git repository listing files, key symbols, and the critical lines of each definition, built from tree-sitter ASTs that show where symbols are defined and referenced. — [Aider, Building a better repository map with tree-sitter](https://aider.chat/2023/10/22/repomap.html)
- Files are nodes in a dependency graph which is ranked by a graph-ranking algorithm, and only the highest-ranked identifiers that fit in the budget are kept; the default budget is 1k tokens via `--map-tokens`. — [Aider repomap post](https://aider.chat/2023/10/22/repomap.html)
- An analysis of Aider's `repomap.py` reports the ranking is PageRank personalised toward the files being edited, the budget formula is max(1024, min(max_input_tokens/8, 4096)), and a binary search stops once output is within 15% of the target. — [NousResearch hermes-agent issue #535](https://github.com/NousResearch/hermes-agent/issues/535); [agentpatterns.ai, Repository Map Pattern](https://www.agentpatterns.ai/context-engineering/repository-map-pattern/)
- The map is selective: it omits many symbols and keeps only the most-referenced ones, and in 2023 the user still had to choose which files to edit. — [Aider repomap post](https://aider.chat/2023/10/22/repomap.html)

**Precise symbol indexes (SCIP, LSIF, Glean, Kythe)**
- Sourcegraph built SCIP to replace LSIF because LSIF was hard to debug and incremental indexing was complex for large codebases; with SCIP the backend only needs to reindex changed files. **[pre-2025]** — [Sourcegraph, Announcing SCIP](https://sourcegraph.com/blog/announcing-scip)
- Sourcegraph uses precise (SCIP-based) code navigation when an index exists and falls back to search-based navigation otherwise. — [Sourcegraph docs, Precise code navigation](https://sourcegraph.com/docs/user/code_intelligence/lsif)
- Meta's Glean stores facts in RocksDB, is queried with the logic language Angle, and targets incremental indexing cost of O(changes) rather than O(repository), with a practical bound of O(fanout) for C++ headers; immutable databases are stacked so clients can view several revisions without full copies (Dec 2024). **[pre-2025]** — [Meta Engineering, Glean open source code indexing](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)
- A simple Glean declaration lookup returns in about a millisecond, and a complex inheritance-and-override query returns first results in a few milliseconds. — [Meta Engineering, Glean](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)
- Glean powers Meta's Glass symbol server (definitions, references, and cross-language jumps across RPC and FFI), and Meta states it supports RAG in AI coding assistants, without further detail. — [Meta Engineering, Glean](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)
- A former Kythe engineer describes Kythe as separating the physical code representation from an abstract semantic graph, and notes that it relies heavily on a unified build system (Blaze/Bazel). — [Hacker News comment](https://hn.jakechampion.name/item/30854916) (secondary, forum comment)

**Code graphs and knowledge graphs**
- RepoGraph (ICLR 2025) builds a line-level graph where each node is a code line and edges represent dependencies, and it is designed as a plug-in to existing agent and procedural frameworks. — [RepoGraph, arXiv 2410.14684](https://arxiv.org/abs/2410.14684)
- CodexGraph lets LLM agents write queries against a graph database built from the repository, evaluated on CrossCodeEval, SWE-bench, and EvoCodeBench. **[pre-2025, Aug 2024]** — [CodexGraph, arXiv 2408.03910](https://arxiv.org/abs/2408.03910)
- LocAgent builds a heterogeneous graph of directories, files, classes and functions with containment, import, invocation and inheritance edges, and gives the agent graph-traversal tools for localization (Mar 2025). — [LocAgent, arXiv 2503.09089](https://arxiv.org/abs/2503.09089)
- KGCompass builds a repository-aware knowledge graph linking issues and pull requests to files, classes and functions. — [KGCompass, arXiv 2503.21710](https://arxiv.org/abs/2503.21710)
- CodeCompass (Feb 2026) exposes dependency graphs to agents as an MCP server. — [CodeCompass, arXiv 2602.20048](https://arxiv.org/abs/2602.20048)

**Hybrid systems**
- Cursor's agent uses grep and semantic search together and states that the combination produces the best results. — [Cursor, semsearch](https://cursor.com/blog/semsearch)
- Sourcegraph describes a two-stage retrieve-then-rank pipeline that combines keyword search, embeddings, and graph-based analysis. — [Sourcegraph, Lessons from building AI coding assistants (mirror)](https://www.plushcap.com/content/sourcegraph/blog/sourcegraph-lessons-from-building-ai-coding-assistants-context-retrieval-and-evaluation)
- Agentless uses a fixed hierarchical localization pipeline (repository tree to files, then classes/functions, then edit locations), combined with embedding retrieval, instead of a free-running agent. **[pre-2025, Jul 2024] [prior knowledge, not re-fetched]** — [Agentless, arXiv 2407.01489](https://arxiv.org/abs/2407.01489)
- RepoCoder iterates retrieval and generation, using the previous generated draft as the next retrieval query. **[pre-2025, 2023] [prior knowledge, not re-fetched]** — [RepoCoder, arXiv 2303.12570](https://arxiv.org/abs/2303.12570)
- GraphCoder uses a statement-level code context graph (control flow plus data and control dependence) for coarse-to-fine retrieval in repository-level completion. **[pre-2025, 2024] [prior knowledge, not re-fetched]** — [GraphCoder, arXiv 2406.07003](https://arxiv.org/abs/2406.07003)

### Inferences
- The approaches differ mainly in when the work is done: indexes (embeddings, SCIP, Glean, graphs) pay cost up front and need a freshness pipeline, while agentic search pays at query time in latency and tokens.
- Precise symbol indexes are the only approach with sub-millisecond, exact answers for "where is this defined / who calls this", but they depend on per-language indexers and often on a build system, which is the main operational burden at 1M+ LOC.
- Repository maps are a cheap middle ground (no external service, tree-sitter only), but a 1k to 4k token budget cannot represent a 1M-LOC codebase meaningfully, so they act as orientation rather than retrieval at that scale.

### Gaps
- No primary source for Claude Code's switch away from RAG was fetched; the Latent Space podcast itself was not reviewed and the claims are reported through secondary summaries.
- No primary data on Windsurf's own indexing (Codemaps, embeddings) was gathered in this session.
- CodeRAG (several papers share the name) was not located; its details are missing.
- GitHub Copilot's indexing approach (remote code search index, embeddings) was not researched in this session.

## What does the research literature show?

### Takeaway
Graph-structured retrieval consistently improves localization and resolve rates on SWE-bench-family benchmarks, often by large relative margins, and the 2026 literature argues that the bottleneck is navigation and the agent's willingness to use structural tools rather than context window size. Most results are on Python-only benchmarks (SWE-bench Lite/Verified) with repositories far smaller than 1M LOC.

### Cited Findings
- RepoGraph, added to four methods across agent and procedural frameworks, substantially boosted all of them and set a new open-source state of the art on SWE-bench; secondary summaries report an average relative improvement of 32.8% in resolve rate on SWE-bench Lite, which was not confirmed in the primary text in this session. — [RepoGraph, arXiv 2410.14684](https://arxiv.org/abs/2410.14684); [ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4a4a3c197deac042461c677219efd36c-Abstract-Conference.html); 32.8% figure via [Liner review](https://liner.com/review/repograph-enhancing-ai-software-engineering-with-repositorylevel-code-graph)
- LocAgent reports up to 92.7% file-level localization accuracy with a fine-tuned Qwen-2.5-Coder-32B at lower cost than proprietary agents; a review of its Table 3 reports Claude-3.5 with LocAgent at 94.16% file-level Acc@5, 87.59% module-level Acc@10 and 77.37% function-level Acc@10 on SWE-bench Lite. Secondary sources disagree on some numbers, so the PDF should be checked. — [LocAgent, arXiv 2503.09089](https://arxiv.org/pdf/2503.09089); [Liner review](https://liner.com/review/locagent-graphguided-llm-agents-for-code-localization)
- KGCompass v1 reported 45.67% repair and 51.33% function-level localization on SWE-bench Lite at about $0.20 per repair; the later journal version reports 58.3% repair and 56.0% localization, and states that 69.7% of successfully localized bugs required multi-hop graph traversal. — [KGCompass, arXiv 2503.21710](https://arxiv.org/abs/2503.21710)
- CodeCompass (Feb 2026, single author, 258 trials, 30 tasks, one production FastAPI repository): on hidden-dependency tasks graph navigation reached 99.4% completion versus 76.2% for vanilla agents and 78.2% for BM25 retrieval; 58% of trials with graph access made zero calls to the graph tool, and agents needed explicit prompting to use it. The author calls this the "navigation paradox": agents miss architecturally critical files despite context windows over 1M tokens. — [CodeCompass, arXiv 2602.20048](https://arxiv.org/abs/2602.20048)
- Agentless reported 32.00% on SWE-bench Lite at about $0.70 per issue with GPT-4o, showing that a simple fixed localization pipeline could rival agent frameworks at the time. **[pre-2025] [prior knowledge, not re-fetched]** — [Agentless, arXiv 2407.01489](https://arxiv.org/abs/2407.01489)
- SWE-bench Pro (Scale AI, Sept 2025) contains 1,865 problems from 41 repositories, including commercial codebases held out from the public set, with tasks requiring multi-file, long-horizon changes; at launch frontier models scored roughly 23% on the public set. **[prior knowledge, not re-fetched]** — [SWE-bench Pro, arXiv 2509.16941](https://arxiv.org/abs/2509.16941)
- 2026 SWE-bench Pro leaderboard figures differ widely between aggregators (for example one lists the top model at 80.3% in July 2026, another at 84.8% in Sept 2026), and several model names appear only on aggregators, so these are unreliable. — [BenchLM](https://benchlm.ai/benchmarks/swe-bench-pro); [AnotherWrapper](https://anotherwrapper.com/tools/llm-pricing/evals/swe-bench-pro)
- Augment ran Auggie and other agents on the 731 public SWE-bench Pro problems and reported Auggie at 51.80% versus Claude Opus 4.5 at 45.89% through SWE-Agent on Scale's leaderboard (Feb 4, 2026); this was Augment's own run, not Scale's. — [Augment, Auggie tops SWE-bench Pro](https://www.augmentcode.com/blog/auggie-tops-swe-bench-pro)

### Inferences
- The academic evidence favours explicit structure (dependency or call graphs) mainly for localization of multi-hop or hidden-dependency issues; the KGCompass 69.7% multi-hop figure and the CodeCompass hidden-dependency gap point in the same direction.
- The CodeCompass adoption finding suggests that adding a graph tool does not help unless the agent is prompted or trained to use it, which may explain why vendor A/B tests of extra tools show small average effects.
- Agent scaffolding and retrieval now visibly move scores on the same model (Augment's 51.8% vs 45.9% with Opus 4.5), but vendor-run comparisons are not controlled for other scaffold differences.

### Gaps
- No direct, controlled study comparing long-context stuffing against retrieval for 1M+ LOC codebases was found in this session.
- No peer-reviewed benchmark was found that uses repositories at the 1M LOC scale; SWE-bench Lite/Verified repositories are mostly far smaller.
- Multi-repo benchmarks were not located in this session.

## Why do some vendors argue against vector indexes while others invest in indexing, and what evidence does each side give?

### Takeaway
The anti-index camp (Anthropic for Claude Code, Cline) argues from freshness, security, and chunking damage, but has published no quantitative evidence. The pro-index camp (Cursor, Augment, Sourcegraph, Greptile) has published vendor-run numbers showing gains that grow with codebase size, while also adopting grep; Cognition took a third route by training fast agentic-search models.

### Cited Findings
**Against indexing**
- Cline (May 27, 2025) argues that chunking code for embeddings tears apart its logic, that an index is a snapshot that drifts with every merge and needs a continuous refresh pipeline, and that embeddings create a second copy of sensitive IP; it concedes RAG can save tokens. The post contains no benchmarks or measurements. — [Cline, Why Cline doesn't index your codebase](https://cline.bot/blog/why-cline-doesnt-index-your-codebase-and-why-thats-a-good-thing)
- Claude Code's switch away from a local vector database was justified by qualitative performance, staleness, and security/privacy, per secondary summaries of Boris Cherny's remarks. — [OfficeChai](https://officechai.com/ai/claude-researcher-explains-how-agentic-search-performed-better-than-rag-for-code-generation/)
- Sourcegraph removed embeddings from Cody Enterprise and replaced them with Sourcegraph Search, citing scale across more and larger repositories and not sending code to a third-party embedding API; local embeddings remained only as a backup in VS Code. — [Sourcegraph Cody FAQ](https://sourcegraph.com/docs/cody/faq)

**For indexing**
- Cursor (Nov 2025): on its internal Cursor Context Bench, semantic search raised accuracy by 12.5% on average (6.5% to 23.5% by model) across all tested models; in an online A/B test with the same model, code retention rose 0.3% overall and 2.6% on codebases with 1,000+ files, and dissatisfied follow-up requests were 2.2% higher without semantic search. Cursor says semantic search is "currently necessary" for best results in large codebases. — [Cursor, semsearch](https://cursor.com/blog/semsearch)
- Augment (Feb 6, 2026) reports that adding its Context Engine via MCP improved agent output quality by 70%+ across Claude Code, Cursor and Codex, measured on 300 Elasticsearch PRs with 900 attempts, scored on correctness, completeness, best practices, code reuse and unsolicited documentation; it lists Claude Code + Opus 4.5 at +80% and Cursor + Opus 4.5 at +71%, and says runs used fewer tool calls and turns. These are vendor-run evaluations with no independent replication found. — [Augment, Context Engine MCP now live](https://www.augmentcode.com/blog/context-engine-mcp-now-live); [SiliconANGLE](https://siliconangle.com/2026/02/06/augment-code-makes-semantic-coding-capability-available-ai-agent/)
- Greptile's position is that semantic search over code works when code is first translated to natural language. — [Greptile blog](https://www.greptile.com/blog/semantic-codebase-search)

**Third route**
- Cognition found that agent trajectories in Windsurf and Devin often spent over 60% of the first turn retrieving context, and reports that SWE-grep matches or beats frontier models on retrieval at about an order of magnitude lower latency, and that on a hard subset of SWE-bench Verified, Fast Context with Sonnet 4.5 solved the same number of tasks in significantly less time. Results use the internal Cognition CodeSearch Eval and the CLI latency comparison was described as an informal demo. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)
- A talk summary from AI Engineer Europe 2026 notes that Cursor's 12.5% figure comes from an internal benchmark and is not an independent evaluation. — [AI Engineer Europe 2026 talk page](https://www.ai.engineer/talks/UM6sFg_jdlE-rag-is-dead-right-kuba-rogut)

### Inferences
- The two camps measure different things: Cursor and Augment report gains concentrated in large codebases, while the anti-index arguments are mostly about operational risk (staleness, IP copies) rather than accuracy.
- Cursor's own data shows the benefit of semantic search is small on average (+0.3% retention) and larger on bigger repositories (+2.6% at 1,000+ files), which is consistent with grep being adequate for small and medium repositories and insufficient for vocabulary-mismatch queries in large ones.
- Sourcegraph's move from embeddings to tuned lexical search shows that "indexing" and "embeddings" are not the same position: a large index can be lexical and symbolic.
- No side has published an independent, controlled comparison at 1M+ LOC.

### Gaps
- No Anthropic primary post quantifying the RAG versus agentic-search decision was found.
- GitHub Copilot and Windsurf's own embedding-index positions were not researched in this session.

## How do these systems handle multi-repo/monorepo scale, polyglot code, generated code, and cross-service dependencies?

### Takeaway
Monorepo and polyglot scale is handled best by industrial symbol indexes (Glean, Kythe, SCIP) which are incremental and support cross-language edges, at the cost of per-language indexers and build integration. AI-tool indexes handle scale mainly through incremental sync and exclusion of generated files, and there is little public evidence on cross-service dependency resolution.

### Cited Findings
- Glean supports per-language schemas plus language-neutral abstraction layers, covers C++, Python, PHP, JavaScript, Rust, Erlang, Thrift and Haskell for diff-level features, and handles cross-language jumps across RPC (Thrift) and FFI boundaries. — [Meta Engineering, Glean](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)
- Glean's stacked immutable databases let clients view multiple repository revisions without full copies, with incremental cost proportional to changes (O(fanout) for C++). — [Meta Engineering, Glean](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)
- Kythe's reliance on a unified build system (Blaze/Bazel) is a constraint for codebases that lack one. — [Hacker News comment](https://hn.jakechampion.name/item/30854916) (secondary)
- SCIP indexes only changed files, which Sourcegraph cites as the reason it replaced LSIF for large codebases. — [Sourcegraph, Announcing SCIP](https://sourcegraph.com/blog/announcing-scip)
- Sourcegraph moved Cody Enterprise from embeddings to search to scale across more repositories and larger repositories. — [Sourcegraph Cody FAQ](https://sourcegraph.com/docs/cody/faq)
- Cursor syncs its index every 5 minutes processing only changed files and recommends ignoring large generated or content files to improve accuracy. — [Cursor docs mirror](https://techdevnotes.com/releases/cursor-docs/20260626-202020Z-6c7064724f5e/content/pages/agent/tools/search.txt)
- A secondary report says Cursor reduced indexing time for a large repository from about four hours to 21 seconds in January 2026 by reusing teammates' indexes via Merkle-tree synchronization; this was not confirmed from a Cursor primary source. — [Pulse.bot news summary](https://www.pulse.bot/ai/news/cursor-slashes-codebase-indexing-from-four-hours-to-21-seconds-543a7632-a105-4df1-b4ab-346a47a83fbd)
- Cline concedes that without an index the agent must run local filesystem searches, which can be slow on repositories with thousands of folders (third-party analysis). — [fast.io, How Cline reads files without indexing](https://fast.io/resources/how-cline-reads-files-without-indexing/)

### Inferences
- For cross-service dependencies (RPC, message schemas), only systems that index the interface definition language and link it to generated stubs (as Glean does for Thrift) can follow the edge precisely; grep can follow it only if names are shared textually.
- Generated code is a known source of retrieval noise for both embedding and grep approaches, and the common mitigation is exclusion via ignore files.

### Gaps
- No public data was found on how Augment, Greptile or Cursor resolve cross-repository or cross-service edges.
- No benchmark specific to polyglot or multi-repo retrieval was found in this session.

## What are the concrete numbers?

### Takeaway
Hard numbers are sparse and mostly vendor-reported; the table below collects the ones found, with their provenance.

### Cited Findings
- Aider repo map: default 1k tokens; formula max(1024, min(max_input_tokens/8, 4096)); binary search tolerance 15%. — [Aider](https://aider.chat/2023/10/22/repomap.html); [hermes-agent #535](https://github.com/NousResearch/hermes-agent/issues/535)
- Glean query latency: about 1 ms for a simple declaration lookup, a few ms to first results for complex inheritance queries. — [Meta Engineering, Glean](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)
- SWE-grep: over 650 tokens/s; SWE-grep-mini: over 2,800 tokens/s (Cerebras), about 4.5x and 20x faster than Haiku 4.5 at 140 tokens/s; max 8 parallel calls x 4 turns; more than 60% of first-turn time previously spent on retrieval. — [Cognition, SWE-grep](https://cognition.com/blog/swe-grep)
- Cursor: +12.5% average offline accuracy (6.5% to 23.5%); +0.3% code retention overall, +2.6% at 1,000+ files; 2.2% more dissatisfied follow-ups without semantic search; 5-minute index sync; semantic search available at 80% indexed. — [Cursor, semsearch](https://cursor.com/blog/semsearch); [Cursor docs mirror](https://techdevnotes.com/releases/cursor-docs/20260626-202020Z-6c7064724f5e/content/pages/agent/tools/search.txt)
- Augment Context Engine MCP: +70%+ quality across agents (300 PRs, 900 attempts); Auggie 51.80% on SWE-bench Pro public (731 problems) vs Opus 4.5 at 45.89% via SWE-Agent. — [Augment MCP post](https://www.augmentcode.com/blog/context-engine-mcp-now-live); [Augment SWE-bench Pro post](https://www.augmentcode.com/blog/auggie-tops-swe-bench-pro)
- Sourcegraph BM25F: about 20% improvement in code search relevance. — [Sourcegraph BM25F (mirror)](https://www.plushcap.com/content/sourcegraph/blog/sourcegraph-keeping-it-boring-and-relevant-with-bm25f)
- LocAgent: up to 92.7% file-level accuracy (fine-tuned Qwen-2.5-Coder-32B); 94.16% file Acc@5 with Claude-3.5. — [LocAgent](https://arxiv.org/pdf/2503.09089); [Liner review](https://liner.com/review/locagent-graphguided-llm-agents-for-code-localization)
- KGCompass: 58.3% repair, 56.0% localization on SWE-bench Lite (v2); about $0.20 per repair (v1). — [KGCompass](https://arxiv.org/abs/2503.21710)
- CodeCompass: 99.4% vs 76.2% (vanilla) vs 78.2% (BM25) on hidden-dependency tasks. — [CodeCompass](https://arxiv.org/abs/2602.20048)

### Inferences
- Precision/recall figures for production retrievers (Cursor, Cognition, Augment) exist only in unpublished charts or internal benchmarks, so cross-vendor comparison of retrieval quality is not currently possible from public data.

### Gaps
- No published index build time, index size, or storage cost figures were found for Cursor, Augment, Greptile or Sourcegraph at 1M+ LOC scale (beyond the unconfirmed Cursor 4h-to-21s report).
- No published token-budget figures were found for Claude Code's agentic search on large repositories.
- Per-model figures in the Cursor and Cognition posts appear only in charts and were not extractable.
