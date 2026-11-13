# Commercial AI Context Engines and Codebase-Understanding Products for Coding Agents (as of November 2026)

Research date: 2026-11-12. All performance figures are vendor claims unless explicitly marked otherwise. Items not re-verified against a primary source in this session are flagged. Several searches were rate-limited, so coverage of Poolside, Tessl, Swimm, Potpie, Kiro, and Amazon Q indexing is thin and listed under Gaps.

## How does each product index code, docs, tickets and PRs, and how does it build and refresh the index for a large multi-repo estate?

### Takeaway
The market has split into three retrieval styles: hosted semantic indexes with incremental sync (Augment, Cursor, Qodo, Greptile, Factory, Zencoder), knowledge graphs that also ingest tickets and operational history (Tabnine Enterprise Context Engine, Bito AI Architect, Unblocked, Glean, Atlassian Rovo), and index-free agentic search (Claude Code), with Cognition's SWE-grep and Sourcegraph Deep Search sitting between them as fast agentic search over a code-search backend. Vendors rarely publish concrete refresh latencies or maximum estate sizes, so "enterprise monorepo scale" claims are mostly unquantified.

### Cited Findings

**Augment Code (Context Engine)**
- Augment describes the Context Engine as semantic search that "understands relationships, dependencies, and architectural patterns", not just text matching, and says it works "with codebases of any size, from side projects to enterprise monorepos" without stating limits (vendor claim; post published 2026-02-06, updated 2026-06-18) — [Augment blog](https://www.augmentcode.com/blog/context-engine-mcp-now-live)
- A related Augment post is titled "Context Engine. Now with full Commit history", which indicates commit history is indexed; the MCP launch page itself does not list indexed sources — [Augment blog](https://www.augmentcode.com/blog/context-engine-mcp-now-live)
- A third-party review headlines "500K-file context" for Augment (unverified secondary claim) — [baeseokjae review](https://baeseokjae.github.io/posts/augment-code-review-2026/)

**Cursor**
- Cursor builds a Merkle tree of file hashes on the client so it can detect exactly which files changed and re-embed only those; for a new team member, the client computes a simhash from the Merkle tree so Cursor can reuse an existing team index, and the hash structure is used to avoid leaking files the user does not have locally — [Cursor blog: secure codebase indexing](https://cursor.com/blog/secure-codebase-indexing)
- Secondary sources report AST-aware chunking (tree-sitter), embeddings cached by chunk hash, storage in Turbopuffer (vector plus full-text), re-sync of modified files roughly every 10 minutes, and obfuscated file paths with no plaintext code stored server-side — [Engineer's Codex](https://read.engineerscodex.com/p/how-cursor-indexes-codebases-fast); [Bito guide](https://bito.ai/blog/how-cursors-codebase-indexing-works-2026-guide/)
- Cursor combines semantic and lexical search because each finds results the other misses (secondary summary) — [morphllm](https://morphllm.com/codebase-indexing)
- A January 2026 report says index reuse cut time-to-first-index for a large repo from about four hours to 21 seconds (Cursor-reported figure via secondary coverage) — [pulse.bot](https://www.pulse.bot/ai/news/cursor-slashes-codebase-indexing-from-four-hours-to-21-seconds-543a7632-a105-4df1-b4ab-346a47a83fbd)

**Qodo (formerly CodiumAI) Context Engine / Qodo Aware**
- The on-prem Context Engine consists of three services installed in order (metadata-service, rag-indexer, context-retriever) backed by PostgreSQL, and connects to GitHub (Cloud or Enterprise), GitLab, and Bitbucket Data Center — [Qodo docs: setup Context Engine](https://docs.qodo.ai/on-prem/context-engine/setup-context-engine); [Qodo on-prem architecture](https://docs.qodo.ai/on-prem/qodo-on-premise/architecture.md)
- The on-prem Context Engine requires access to gpt-5 and claude-4.1-opus, and customers with a custom LLM gateway must contact support — [Qodo docs](https://docs.qodo.ai/on-prem/context-engine/setup-context-engine)
- Repositories are added explicitly to a "Context Engine RAG index" — [Qodo docs](https://docs.qodo.ai/on-prem/ide-plugin/how-to-add-repositories-to-the-context-engine-rag-index)
- Qodo announced cross-repo review and "mined rules" (rules inferred from the codebase) and markets "Qodo 3.0" as quality control for an "agentic software factory" — [Qodo blog](https://www.qodo.ai/?p=15395); [Qodo 3.0](https://www.qodo.ai/?p=22520)

**Tabnine Enterprise Context Engine (now Tricentis)**
- The engine builds a continuously updated knowledge graph that extracts entities, relationships, dependencies and architectural patterns from repositories, documentation, tickets, APIs and infrastructure metadata — [Business Wire](https://www.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise); [Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)

**Bito AI Architect**
- AI Architect builds a knowledge graph from repositories down to modules, APIs and libraries, plus operational history from issue trackers such as Jira; Bito-hosted setup involves connecting a Git provider and a repo list, after which Bito indexes and returns an MCP URL and token — [Bito docs: AI Architect overview](https://docs.bito.ai/ai-architect/overview); [Bito docs](https://docs.bito.ai/ai-architect)
- The same graph feeds Bito's AI Code Review Agent; Slack, Jira and Linear integrations are documented — [Bito docs: key features](https://docs.bito.ai/ai-architect/key-features)

**Greptile**
- A review describes Greptile as building a repository-wide semantic graph index and using "swarm" agents for review (secondary, single source) — [WeavAI](https://weavai.app/blog/en/2026/05/12/greptile-2026-review-ai-code-review-pricing-debate/); [cubic review](https://www.cubic.dev/blog/greptile-review)

**Cognition (Windsurf, now Devin Desktop; DeepWiki; SWE-grep; Codemaps)**
- SWE-grep is the retrieval subagent behind Windsurf "Fast Context"; Cognition claims it is about 10x faster than standard agentic search (vendor claim) — [nxcode](https://www.nxcode.io/resources/news/cognition-windsurf-acquisition-swe-1-5-codemaps-2026); primary post (not re-fetched this session): [Cognition: SWE-grep](https://cognition.ai/blog/swe-grep)
- Codemaps (launched around late October / 4 November 2025; sources disagree on the date) generates AI-annotated structural maps of code using SWE-1.5 and Claude Sonnet 4.5 and links to DeepWiki — [testingcatalog](https://www.testingcatalog.com/windsurf-is-getting-codemaps-for-ai-assisted-coding/); [windowsforum](https://windowsforum.com/news/codemaps-on-windsurf-ai-driven-codebase-maps-for-faster-onboarding.388036/)
- Windsurf 2.0 (15 April 2026) added Devin integration and an Agent Command Center; one review reports Windsurf was rebranded "Devin Desktop" on 2 June 2026 and SWE-1.6 succeeded SWE-1.5 (lower-confidence secondary sources) — [codepick](https://codepick.dev/en/guides/windsurf-2-new-features/); [vibecoding.app](https://vibecoding.app/blog/windsurf-review); [chatforest](https://chatforest.com/reviews/windsurf-2-0-cognition-devin-agent-command-center-ide-review/)

**Sourcegraph (Code Search, Deep Search, MCP) and Amp**
- Sourcegraph's MCP server exposes cross-repo search, navigation, history and Deep Search over its existing code-search index; Deep Search can run as a sub-agent via MCP so the calling agent's context window is not filled with raw results — [Sourcegraph MCP](https://sourcegraph.com/mcp); [MCP GA changelog](https://sourcegraph.com/changelog/mcp-ga)
- The 3 August 2026 changelog added more exhaustive Deep Search with downloadable reports and customisation through guidance and skills — [Sourcegraph changelog](https://sourcegraph.com/changelog/2026-08-03)

**Factory**
- Factory's "Knowledge" droid builds and maintains an index over the repo, internal docs and ticket history so other droids query it instead of re-reading code; repositories are synced to Chroma Cloud, and droids select the index matching the current branch and commit — [digitalapplied review](https://www.digitalapplied.com/blog/factory-ai-multi-agent-coding-platform-review); [Chroma case study](https://www.trychroma.com/customers/factory-ai-case-study)

**Zencoder (Repo Grokking)**
- Repo Grokking embeds whole repositories into a vector database for RAG and also builds a graph representation; a 2025 review says scans are re-triggered when code changes (dated February 2025) — [InfoWorld](https://www.infoworld.com/article/3820199/review-zencoder-has-a-vision-for-ai-coding.html)

**Unblocked**
- Unblocked positions itself as a context engine that synthesises across code, docs, chat and tickets, arguing that "MCP is a transport protocol, not a context engine" and that a pile of MCP connectors does not resolve conflicting or stale sources (vendor positioning) — [Unblocked: context for agents](https://getunblocked.com/blog/unblocked-context-engine-for-agents/index.md); [Unblocked: connectors are not a context engine](https://getunblocked.com/blog/mcp-connectors-are-not-a-context-engine/index.md); [Inside the Unblocked context engine](https://getunblocked.com/blog/inside-the-unblocked-context-engine/index.md)

**Glean and Atlassian Rovo (packaged knowledge platforms)**
- Glean Code Search returns code files, snippets, commits, PR/MR diffs and references from connected repositories, permission-trimmed to what the running user can access in the code host — [Glean docs: code search](https://docs.glean.com/tools/glean/code-search)
- Atlassian Rovo "code context" searches connected GitHub and Bitbucket Cloud repositories with combined lexical and semantic search, and is rolling out to paid customers through open beta — [Atlassian support](https://support.atlassian.com/rovo/docs/what-is-code-context/)

**Claude Code (contrast: no index)**
- Claude Code uses LLM-driven grep, glob and file reads at runtime instead of a vector index; secondary accounts attribute to Boris Cherny the statement that an early local vector-DB RAG version was dropped because agentic search worked better and avoided staleness, security and reliability problems — [smartscope](https://smartscope.blog/en/ai-development/practices/rag-debate-agentic-search-code-exploration/); [vadim blog](https://vadim-blog.vercel.app/2026/claude-code-no-indexing)
- Secondary accounts disagree on whether agentic search was more accurate or merely acceptable for simplicity; the original podcast was not reached in this session — [yage.ai](https://yage.ai/share/why-coding-agents-still-use-grep-en-20260327.html); [smartscope](https://smartscope.blog/en/ai-development/practices/rag-debate-agentic-search-code-exploration/)

### Inferences
- For a multi-million-line, multi-repo estate, the products with the clearest documented refresh mechanics are Cursor (Merkle-tree diff plus shared team index) and Factory (branch/commit-aware index); others describe "continuous" indexing without stating latency.
- Graph-plus-tickets products (Tabnine, Bito, Unblocked, Glean, Rovo) are better suited to questions about why code exists and who owns it, while embedding-only indexes mainly help locate code.
- Agentic search avoids index staleness and data duplication, which matters for regulated estates, but it costs more tokens and tool calls per query on very large codebases; this trade-off is the main argument context-engine vendors use against it.

### Gaps
- No vendor published a verified maximum repository count, line count, or reindex latency for multi-million-line estates.
- Poolside, Tessl, Swimm, Potpie, Kiro and Amazon Q Developer workspace indexing were not covered in fetched sources (searches rate-limited or returned nothing). From prior knowledge, Amazon Q Developer built a local workspace index in the IDE and Kiro relies on spec documents and steering files, but this was not verified for November 2026.
- CodeRabbit's code-graph retrieval mechanics were not covered by any fetched source.

## What do these products expose via MCP so other agents can use the context?

### Takeaway
By late 2026 nearly every vendor ships an MCP server, and the competitive pitch has shifted from "our IDE" to "our context inside your agent" (Augment, Bito, Sourcegraph, Unblocked, Glean, Atlassian, Qodo Aware, DeepWiki). Tool lists are rarely documented on marketing pages, and some MCP usage is metered separately.

### Cited Findings
- Augment Context Engine MCP became generally available on 6 February 2026 in two modes: local (Auggie CLI as a stdio MCP server over the working directory) and remote (hosted endpoint `api.augmentcode.com/mcp` for context across all repositories); it lists Claude Code, Codex, Gemini CLI and others as clients, and every Augment user got 1,000 free requests in February 2026 — [Augment blog](https://www.augmentcode.com/blog/context-engine-mcp-now-live); [Augment docs](https://docs.augmentcode.com/context-services/overview); [Augment on X](https://x.com/augmentcode/status/2019840972805533994)
- The Augment launch page does not name the specific MCP tools exposed — [Augment blog](https://www.augmentcode.com/blog/context-engine-mcp-now-live)
- Bito AI Architect runs as an MCP server for Claude Code, Cursor, Windsurf, GitHub Copilot in VS Code and Codex, with a one-command installer — [Bito docs](https://docs.bito.ai/ai-architect); [Bito platform](https://bito.ai/platform/)
- Sourcegraph's default `/.api/mcp` endpoint moved to a curated context-gathering toolset from the 30 March 2026 release, with the full toolset at `/.api/mcp/all` — [Sourcegraph changelog](https://sourcegraph.com/changelog/mcp-all)
- Unblocked's MCP server reached GA in April 2026 alongside a CLI, with consolidated tools tuned for Cursor, Claude, Codex and Copilot — [Unblocked MCP](https://getunblocked.com/blog/mcp-beta/index.md); [Unblocked blog index](https://getunblocked.com/blog/index.md)
- Glean exposes Code Search through the Glean MCP Server, and introduced enterprise MCP "actions" in March 2026 — [Glean docs](https://docs.glean.com/tools/glean/code-search); [Glean blog Mar 2026](https://www.glean.com/blog/mcp-mar-drop-2026); [Glean blog Sep 2025](https://www.glean.com/blog/mcp-servers-septdrop-2025)
- The Atlassian Rovo MCP server exposes code search, and use through MCP consumes Rovo credits — [Atlassian Rovo MCP](https://developer.atlassian.com/cloud/rovo-mcp/); [Atlassian support](https://support.atlassian.com/rovo/docs/what-is-code-context/)
- Qodo Aware has documented enterprise self-hosted deployment (Qodo's context product exposed to agents) — [Qodo Aware docs](https://docs.qodo.ai/qodo-aware/getting-started/enterprise-self-hosted)
- Cognition's DeepWiki offers a public MCP server for wiki-style repository Q&A (not re-fetched this session) — [DeepWiki MCP docs](https://docs.devin.ai/work-with-devin/deepwiki-mcp)

### Inferences
- MCP makes context engines interchangeable at the protocol level, so differentiation now rests on retrieval quality, permissions and deployment model rather than on the IDE.
- Credit-metered MCP access (Rovo, Augment) means agent loops that call context tools heavily can create unpredictable cost, which should be modelled before rollout.

### Gaps
- Exact MCP tool schemas for Augment, Bito, Qodo Aware and Glean were not retrieved.
- Whether Tabnine's Context Engine remains available via MCP to non-Tricentis agents after the acquisition is unknown.

## What data-residency and self-hosting options exist, and what security certifications are claimed?

### Takeaway
Fully self-hosted or air-gapped options are offered by Tabnine (now with roadmap risk), Qodo, Sourcegraph, Poolside and Factory (on-prem options), with Greptile offering self-hosting at enterprise tier; Augment, Cursor and Bito's default offerings are SaaS, and Qodo's on-prem Context Engine still depends on frontier models (gpt-5, claude-4.1-opus) being reachable.

### Cited Findings
- Tabnine lists SaaS, VPC, on-premises and fully air-gapped deployment, states it does not retain code or train on customer code, and lists Code Assistant at $39/user/month and Agentic at $59/user/month (annual); no post-acquisition commitment to these deployment modes has been published — [Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)
- Qodo markets air-gapped/on-prem deployment, scoped context access and auditability; a Qodo page says air-gapped installs support GitHub Enterprise, GitLab Self-Managed, Bitbucket Data Center and Gerrit (date unverified) — [Qodo enterprise](https://www.qodo.ai/enterprise/); [Qodo on-prem code review](https://www.qodo.ai/glossary/what-is-on-prem-code-review/)
- Augment's security page lists SOC 2 Type II (attested), ISO/IEC 42001 (certified), GDPR, CCPA and HIPAA with BAA; Coalfire issued the ISO/IEC 42001 certification (press release dated 5 August 2025, while Augment's blog claiming "first certified" is dated 29 May 2025) — [Augment security](https://augmentcode.com/security); [Coalfire press release](https://coalfire.com/insights/news-and-events/press-releases/augment-ai-achieves-iso-iec-42001-certification-from-coalfire-certification-marking-a-milestone-in-responsible-ai-governance); [Augment blog](https://www.augmentcode.com/blog/augment-code-is-the-first-ai-coding-assistant-to-be-iso-iec-42001-certified)
- Cursor stores embeddings and obfuscated metadata in the cloud rather than plaintext code (secondary description; check Cursor's security docs for compliance use) — [Cursor blog](https://cursor.com/blog/secure-codebase-indexing); [Bito guide](https://bito.ai/blog/how-cursors-codebase-indexing-works-2026-guide/)
- Factory lists SSO, SAML/SCIM, zero data retention, audit logging, on-prem options, customer-managed keys and data-residency controls — [digitalapplied](https://www.digitalapplied.com/blog/factory-ai-multi-agent-coding-platform-review)
- Poolside deploys inside the customer boundary, including air-gapped, and records every agent action as a searchable trajectory (third-party ranking site) — [Agentic Index](https://agenticindex.io/rankings/coding-agents)
- Greptile offers custom enterprise pricing with self-hosting and SSO/SAML — [llms.blog](https://www.llms.blog/posts/greptile-raises-50m-at-a-750m-valuation-what-the-ai-code-reviewer-does-and-what-it-costs)
- Glean and Rovo code search are permission-trimmed to the user's code-host access — [Glean docs](https://docs.glean.com/tools/glean/code-search)
- Tabnine was named a Visionary in the May 2026 Gartner Magic Quadrant for Enterprise AI Coding Agents — [Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)

### Inferences
- For a bank needing air-gapped deployment, the realistic shortlist is Tabnine (contract protections needed), Qodo, Sourcegraph and Poolside; Qodo's model dependency must be checked against the bank's approved model gateway.
- ISO/IEC 42001 is becoming a differentiating certification for AI coding vendors, but SOC 2 Type II remains the baseline.

### Gaps
- SOC 2 / ISO 27001 status for Bito, Greptile, Unblocked, Zencoder and Qodo was not verified in this session.
- Regional data residency (EU, UK) options for Augment and Cursor were not confirmed.
- No financial-services customer names were found for any context-engine vendor except Tricentis's broader customer list (Experian, Allianz) — [Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)

## Which benchmark claims are vendor-only versus independently replicated?

### Takeaway
Every headline improvement number for a named commercial context engine found in this research is vendor-run and unreplicated. Independent academic benchmarks (ContextBench, Agent Retrieval Bench) exist but evaluate generic retrieval methods and open agents, not named commercial products, and they suggest scaffolding adds only marginal retrieval gains.

### Cited Findings
- Augment (vendor): adding Context Engine MCP improved agent output by 71% for Cursor + Opus 4.5, 80% for Claude Code + Opus 4.5 and 30% for Cursor + Composer-1, measured on 300 Elasticsearch PRs × 3 prompts (900 attempts) across correctness, completeness, best practices, code reuse and unsolicited documentation; no variance or per-agent sample size published — [Augment blog](https://www.augmentcode.com/blog/context-engine-mcp-now-live)
- Augment has only two G2 reviews averaging 2.8 stars, so there is little independent user feedback — [G2](https://www.g2.com/sellers/augment-code)
- Tabnine/Tricentis (vendor, unaudited): up to 2x AI accuracy, up to 80% token reduction and up to 50% faster complex tasks — [Business Wire](https://www.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise)
- Bito (vendor): 70.1% task success with AI Architect versus 51.9% without, on Claude Opus 4.6 — [Bito grounded coding](https://bito.ai/product/grounded-coding/)
- Unblocked (vendor): curated context used 42% fewer tokens and 64% fewer tool calls than raw context dumping — [Unblocked blog](https://getunblocked.com/blog/why-mcp-isnt-enough-enhancing-agent-capabilities-with-a-context-engine/index.md)
- Cognition (vendor): SWE-grep about 10x faster than standard agentic search; SWE-1.5 at 950 tokens/second — [nxcode](https://www.nxcode.io/resources/news/cognition-windsurf-acquisition-swe-1-5-codemaps-2026); [chatforest](https://chatforest.com/reviews/windsurf-2-0-cognition-devin-agent-command-center-ide-review/)
- Greptile: an 82% bug-detection rate is reported by a single blog, not independently verified — [WeavAI](https://weavai.app/blog/en/2026/05/12/greptile-2026-review-ai-code-review-pricing-debate/)
- Independent: ContextBench (arXiv:2602.05892, Feb 2026) has 1,136 issue-resolution tasks from 66 repos with human-annotated gold context, evaluates four LLMs and five coding agents, and finds scaffolding adds only marginal gains in context retrieval and that models favour recall over precision — [arXiv](https://arxiv.org/abs/2602.05892); [GitHub](https://github.com/EuniAI/ContextBench)
- Independent: Agent Retrieval Bench (arXiv:2607.24882, July 2026) evaluates lexical retrieval, RepoMap, open embeddings and logged agent context selection at file level; its pilot is only 45 samples in a single run and shows large headroom versus oracle context — [arXiv](https://arxiv.org/abs/2607.24882)
- A third-party comparison headlined a "15-problem gap" between Augment and Cursor on the same model (methodology not reviewed; the site sells a competing retrieval product) — [morphllm](https://www.morphllm.com/comparisons/augment-code-vs-cursor)

### Inferences
- Vendor benchmarks use the vendor's chosen repos and graders, so they show direction but not magnitude; buyers should run a bake-off on their own repositories.
- ContextBench's finding that scaffolding adds little retrieval gain is in tension with vendor claims of 30-80% improvement, though the two measure different things (retrieval precision versus end-task quality).

### Gaps
- No independent replication of any named vendor's benchmark (Augment, Bito, Tabnine, Unblocked, Cognition, Greptile) was found.

## What acquisitions, shutdowns and pricing changes occurred in 2025-2026?

### Takeaway
The main structural events are Cognition's acquisition of Windsurf (July 2025) and its later rebrand toward Devin, Tricentis's acquisition of Tabnine (30 July 2026), large rounds for CodeRabbit, Factory and Greptile, the reported end-of-life of standalone Atlassian Rovo Dev, and a move from flat seats to usage-based pricing at Augment and Greptile.

### Cited Findings
- Tricentis acquired Tabnine on 30 July 2026 (terms undisclosed; Calcalist estimated tens of millions of dollars against $55M raised); only "support" was promised to existing customers, no roadmap; a review site reports tabnine.com redirected to tricentis.com from 3 October 2026 while docs.tabnine.com stays live (single source) — [Business Wire](https://www.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise); [Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk); [javisreview](https://javisreview.com/review/tabnine-review-2026/)
- Tricentis precedent: Flood.io was acquired in 2017 and shut down on 30 June 2024 with 20 days' notice — [Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)
- Cognition acquired Windsurf in July 2025 after Google hired Windsurf's leadership; some 2026 secondary sources wrongly date the acquisition to December 2025 — primary (not re-fetched this session): [Cognition blog](https://cognition.ai/blog/windsurf); conflicting secondary: [nxcode](https://www.nxcode.io/resources/news/cognition-windsurf-acquisition-swe-1-5-codemaps-2026); [Wikipedia](https://en.wikipedia.org/wiki/Cognition_AI)
- CodeRabbit raised a $143M Series C at a $1.5B valuation in August 2026 (Atomico and Smash Capital), reports over 2 million reviews per week, and its CEO said proceeds may fund acquisitions — [Reuters via CodeRabbit](https://www.coderabbit.ai/newsroom/reuters-coderabbit-valued-at-1-5-billion); [Axios Pro](https://www.axios.com/pro/enterprise-software-deals/2026/08/12/coderabbit-raise-acquisitions-ai-code-review); [FinSMEs](https://www.finsmes.com/2026/08/coderabbit-raises-143m-in-series-c-funding.html)
- Factory raised a reported $150M Series C at $1.5B led by Khosla Ventures on 16 April 2026 — [idlen](https://www.idlen.io/news/factory-ai-150-million-1-5-billion-droids-coding-agents-enterprise-april-2026/)
- Greptile reportedly raised $50M at a $750M valuation and moved in March 2026 from a flat $30/seat to $30/seat with 50 credits plus $1 per extra credit, where review depth costs 1, 3 or 10 credits; the change drew community criticism — [llms.blog](https://www.llms.blog/posts/greptile-raises-50m-at-a-750m-valuation-what-the-ai-code-reviewer-does-and-what-it-costs); [Agent Wars](https://www.agent-wars.com/news/2026-05-01-greptile-per-review-pricing)
- Augment moved to credit-based pricing on 20 October 2025 (criticised by users); trackers report a further shift to dollar/token usage billing in mid-2026 and rate changes in August-September 2026 (not confirmed against a primary pricing page) — [Augment blog](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing); [The Register](https://www.theregister.com/2025/10/15/augment_pricing_model/); [Augment docs](https://docs.augmentcode.com/models/credit-based-pricing); [usagepricing](https://usagepricing.com/blueprint/activity/augment-code-2026-08-11-price-change)
- Atlassian has reportedly announced end-of-life for standalone Rovo Dev with no final date, while pushing Jira/Confluence/Bitbucket context into third-party agents through MCP (third-party source) — [crosstowntech](https://crosstowntech.com/apps/rovo-dev-guide/)
- Sourcegraph's coding agent moved from Cody to Amp, and Sourcegraph and Amp are reported to be separating into different companies; third-party sites cite a $16,000/year minimum for Sourcegraph (unverified) — [Sourcegraph: a note from Dan](https://sourcegraph.com/blog/a-note-from-dan); [aitoolsatlas](https://aitoolsatlas.ai/tools/sourcegraph-deep-search)
- Tricentis is backed by GTCR ($1.33B at a $4.5B valuation, November 2024) and Insight Partners — [Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)

### Inferences
- Consolidation risk is real: Tabnine (now inside a testing company) and Windsurf (absorbed into Devin) both show that a standalone coding-context product can be repurposed after acquisition, so multi-year contracts need end-of-life notice and escrow clauses.
- Usage-based pricing for context and review makes agent-heavy workflows harder to budget than seat licences.

### Gaps
- Pricing for Cursor Enterprise, Bito AI Architect, Unblocked, Qodo Enterprise and Glean was not retrieved.
- No reliable 2026 information was found for Swimm, Potpie, Tessl or Poolside funding or product changes.
