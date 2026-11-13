# Choosing Code Intelligence Tools for Multi-Million-Line Codebases

Research report, November 2026. Related notes: [knowledge-graphs-for-coding-agents.md](knowledge-graphs-for-coding-agents.md),
[coding-agents-in-large-codebases.md](coding-agents-in-large-codebases.md),
[context-layer-databases.md](context-layer-databases.md), [context-engineering.md](context-engineering.md),
[agent-ready-content-formats.md](agent-ready-content-formats.md).

## Contents

- [1. What this report covers](#1-what-this-report-covers)
- [2. Summary](#2-summary)
- [3. Five tool families cover different parts of the problem](#3-five-tool-families-cover-different-parts-of-the-problem)
- [4. Enterprise code search and navigation platforms](#4-enterprise-code-search-and-navigation-platforms)
  - [4.1 Sourcegraph](#41-sourcegraph)
  - [4.2 GitHub Copilot indexing and the GitHub MCP server](#42-github-copilot-indexing-and-the-github-mcp-server)
  - [4.3 GitLab exact code search and GitLab Orbit](#43-gitlab-exact-code-search-and-gitlab-orbit)
  - [4.4 Atlassian Rovo code context](#44-atlassian-rovo-code-context)
  - [4.5 Google Gemini Code Assist code customization](#45-google-gemini-code-assist-code-customization)
  - [4.6 Sourcebot and the open-source search engines](#46-sourcebot-and-the-open-source-search-engines)
  - [4.7 Meta Glean and Google Kythe](#47-meta-glean-and-google-kythe)
- [5. AI context engines](#5-ai-context-engines)
  - [5.1 Augment Context Engine](#51-augment-context-engine)
  - [5.2 Cursor codebase indexing](#52-cursor-codebase-indexing)
  - [5.3 Qodo Context Engine and Qodo Aware](#53-qodo-context-engine-and-qodo-aware)
  - [5.4 Tabnine Enterprise Context Engine](#54-tabnine-enterprise-context-engine)
  - [5.5 Bito AI Architect](#55-bito-ai-architect)
  - [5.6 Other context engines and knowledge platforms](#56-other-context-engines-and-knowledge-platforms)
  - [5.7 Index-free agentic search as the baseline](#57-index-free-agentic-search-as-the-baseline)
- [6. Open-source and self-hostable agent tools](#6-open-source-and-self-hostable-agent-tools)
  - [6.1 Indexing foundations and their maintenance status](#61-indexing-foundations-and-their-maintenance-status)
  - [6.2 Serena and other LSP-based MCP servers](#62-serena-and-other-lsp-based-mcp-servers)
  - [6.3 Tree-sitter code-graph MCP servers](#63-tree-sitter-code-graph-mcp-servers)
  - [6.4 Embedding-based MCP servers](#64-embedding-based-mcp-servers)
  - [6.5 Structural search and code-as-database engines](#65-structural-search-and-code-as-database-engines)
- [7. Refactoring, architecture and legacy analysis tools](#7-refactoring-architecture-and-legacy-analysis-tools)
  - [7.1 Moderne and OpenRewrite](#71-moderne-and-openrewrite)
  - [7.2 AWS Transform](#72-aws-transform)
  - [7.3 Google Mainframe Assessment Tool](#73-google-mainframe-assessment-tool)
  - [7.4 CAST Imaging](#74-cast-imaging)
  - [7.5 IBM watsonx Code Assistant for Z and ADDI](#75-ibm-watsonx-code-assistant-for-z-and-addi)
  - [7.6 Rocket Enterprise Analyzer](#76-rocket-enterprise-analyzer)
  - [7.7 vFunction](#77-vfunction)
  - [7.8 Microsoft Legacy Modernization Agents](#78-microsoft-legacy-modernization-agents)
  - [7.9 Sonar and developer portals](#79-sonar-and-developer-portals)
- [8. What the evidence shows about retrieval methods](#8-what-the-evidence-shows-about-retrieval-methods)
  - [8.1 Independent studies](#81-independent-studies)
  - [8.2 Vendor-reported results](#82-vendor-reported-results)
  - [8.3 Analyst coverage](#83-analyst-coverage)
- [9. Side-by-side comparison](#9-side-by-side-comparison)
  - [9.1 Enterprise search platforms and context engines](#91-enterprise-search-platforms-and-context-engines)
  - [9.2 Open-source agent tools](#92-open-source-agent-tools)
  - [9.3 Refactoring and legacy tools](#93-refactoring-and-legacy-tools)
  - [9.4 Deployment options for regulated firms](#94-deployment-options-for-regulated-firms)
- [10. Pricing, licensing and vendor stability](#10-pricing-licensing-and-vendor-stability)
- [11. Security and regulatory considerations](#11-security-and-regulatory-considerations)
- [12. Worked capital markets scenarios](#12-worked-capital-markets-scenarios)
  - [12.1 Post-trade settlement platform](#121-post-trade-settlement-platform)
  - [12.2 Mandate rules engine](#122-mandate-rules-engine)
  - [12.3 COBOL general ledger on the mainframe](#123-cobol-general-ledger-on-the-mainframe)
  - [12.4 Regulated firm that requires on-premises or air-gapped deployment](#124-regulated-firm-that-requires-on-premises-or-air-gapped-deployment)
  - [12.5 Java upgrade across thousands of repositories](#125-java-upgrade-across-thousands-of-repositories)
  - [12.6 Fast-moving pricing library in C++ and Python](#126-fast-moving-pricing-library-in-c-and-python)
- [13. How a large organisation should choose](#13-how-a-large-organisation-should-choose)
  - [13.1 Decide by constraint before comparing features](#131-decide-by-constraint-before-comparing-features)
  - [13.2 A layered architecture rather than a single product](#132-a-layered-architecture-rather-than-a-single-product)
  - [13.3 Run a bake-off on your own code](#133-run-a-bake-off-on-your-own-code)
  - [13.4 Contract and governance checklist](#134-contract-and-governance-checklist)
- [14. Conclusion](#14-conclusion)
- [Resources](#resources)
  - [Related notes](#related-notes)

## 1. What this report covers

- This report surveys the code intelligence tools available in November 2026 and explains how a large organisation should choose among them.
  - Code intelligence here means products that index a large codebase and give developers and coding agents code search, symbol navigation, code graphs, semantic retrieval, refactoring or legacy analysis, and context through the Model Context Protocol (MCP).
  - The reader in mind is an engineering or platform leader at a bank, broker or asset manager with a multi-million-line, multi-repository, polyglot estate that includes Java, Python, TypeScript, C#, C++, SQL and COBOL.
- Every product is described with the same seven headings so that products can be compared directly.
  - **What it indexes and how** describes the index model, for example trigram text, compiler-accurate symbols, embeddings or a graph.
  - **Freshness** describes how quickly the index reflects new commits.
  - **Agent access** describes what the product exposes to coding agents, including MCP tools and the permission model.
  - **Deployment and data residency** describes where the index and the code live.
  - **Pricing and licence** describes the commercial and licensing terms that were found.
  - **Evidence and customers** describes outcome data and named customers, with each item labelled as a vendor claim or as independent evidence.
  - **Limitations** names the main drawbacks that a buyer should weigh against the benefits.
- Smaller or similar tools are grouped in tables that use the same seven columns.
- Evidence labels are used throughout.
  - **[Vendor claim]** marks a statement that comes from the vendor's own material or a vendor-commissioned study.
  - **[Independent]** marks peer-reviewed or preprint research, independent security research, or established press reporting.
  - **[Secondary]** marks aggregator sites, reviews and directory pages whose figures should be checked before reuse.
  - Anything published before 2026 carries its date.
- The report draws on the techniques described in [knowledge-graphs-for-coding-agents.md](knowledge-graphs-for-coding-agents.md) and [coding-agents-in-large-codebases.md](coding-agents-in-large-codebases.md), and it does not repeat their explanations of retrieval methods.

## 2. Summary

- The market has no single product that covers all five jobs of code intelligence, so a large organisation will end up combining two or three tools.
  - Enterprise code search platforms (Sourcegraph, GitHub, GitLab, Atlassian, Google) find code across thousands of repositories.
  - AI context engines (Augment, Cursor, Qodo, Tabnine, Bito, Unblocked and others) assemble relevant context for an agent, often including tickets and documentation.
  - Open-source agent tools (Serena, GitNexus, claude-context, ast-grep and others) give a single developer's agent symbol-level or graph-level access to a working copy.
  - Refactoring and legacy tools (Moderne, CAST, AWS Transform, Google MAT, IBM, Rocket) model code precisely enough to change it at scale or to explain COBOL estates.
  - Index-free agentic search, as used by Claude Code, Cline and OpenHands, is the baseline that every indexed product has to beat.
- Every serious vendor now exposes its index through MCP, so the decision is no longer about which IDE developers use.
  - Sourcegraph is the only vendor found that exposes compiler-accurate `go_to_definition` and `find_references` as MCP tools over a cross-repository index ([Sourcegraph MCP docs](https://7.5.sourcegraph.com/api/mcp)).
  - GitLab Orbit is the only platform found that joins code with pipelines, deployments and work items in one graph exposed to agents ([GitLab Orbit docs](https://docs.gitlab.com/orbit/)).
- Independent evidence that indexes improve agent outcomes is weak, and almost every headline improvement figure is a vendor claim.
  - The largest neutral benchmark, ContextBench (February 2026), found that a bash-only agent had the best file-level retrieval F1 and that changing the model mattered as much as changing the retrieval method ([arXiv 2602.05892](https://arxiv.org/html/2602.05892)).
  - Graph and symbol tools help most with structural questions such as "who calls this" and with weaker models, and their advantage shrinks as model strength rises ([nefayran/code-graph-vs-grep](https://github.com/nefayran/code-graph-vs-grep)).
  - No public benchmark tests any of these products on a multi-million-line enterprise estate, which is where indexes should help most.
- Deployment constraints narrow the field more than features do.
  - GitHub Copilot semantic indexing, Atlassian code context, Gemini code customization, Augment's remote engine, AWS Transform and Google MAT all require code to be processed in a vendor cloud.
  - Sourcegraph self-hosted, GitLab Self-Managed with Orbit and Zoekt, Sourcebot Enterprise with an offline licence, Qodo on-premises, Tabnine air-gapped, Moderne CLI, CAST Imaging and SonarQube Server can run inside a firm's own boundary, each with caveats described below.
- COBOL, JCL and stored-procedure SQL are the weakest area of the whole market.
  - No open-source agent-facing tool reviewed handles COBOL with semantic precision, and neither CodeQL nor Joern has a COBOL frontend ([CodeQL languages](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/)).
  - Mainframe estates are served by commercial analysers (CAST, IBM ADDI, Rocket Enterprise Analyzer) or by hyperscaler services (AWS Transform, Google MAT), and large banks such as Morgan Stanley have built their own tooling.
- The recommended approach for a large organisation is a layered architecture chosen by constraint, followed by a bake-off on the organisation's own code.
  - The layers are an estate-wide lexical index, a precise symbol layer for compiled languages, an optional semantic context engine, a deterministic transformation engine, and a legacy analyser where mainframe code exists.
  - Vendor stability is a selection criterion in its own right, because Tabnine, Windsurf and Sourcegraph's Cody all changed ownership or direction between July 2025 and July 2026.

## 3. Five tool families cover different parts of the problem

- The families differ mainly in their index model, and the index model determines what questions an agent can answer reliably.

| Family | Index model | Best at | Weak at | Examples |
|---|---|---|---|---|
| Enterprise code search | Trigram or n-gram text index, plus compiler-accurate symbols in some products | Finding every occurrence of an identifier across thousands of repositories | Answering conceptual questions phrased in plain English | Sourcegraph, GitHub Blackbird, GitLab exact code search, Sourcebot, OpenGrok |
| Precise symbol indexes | SCIP, Kythe or Glean facts produced by compilers, or live LSP queries | Definitions, references, implementations and impact analysis | Languages without a working build, and setup cost | Sourcegraph precise navigation, Meta Glean, Serena |
| AI context engines | Embeddings, often with a lightweight graph and ticket or document sources | Natural-language questions and "why does this exist" questions | Exact cross-repository references and auditable completeness | Augment, Cursor, Qodo, Tabnine, Bito, Unblocked |
| Code graphs for agents | Tree-sitter call and import graphs in an embedded graph store | Structural questions on one repository at low token cost | Overloaded, dynamic or dependency-injected code, and estate scale | GitNexus, Codanna, CodeGraphContext, codebase-memory |
| Refactoring and legacy analysis | Type-attributed lossless trees, or cross-program dependency graphs over COBOL, JCL and data | Deterministic large-scale change and mainframe understanding | Freshness, because most models are snapshots from the last analysis run | Moderne, CAST Imaging, AWS Transform, Google MAT, IBM ADDI |

- The families are converging, and most vendors now combine lexical and semantic retrieval.
  - Atlassian recommends lexical search for exact function names because its semantic ranking is based on conceptual similarity ([Atlassian code context](https://support.atlassian.com/rovo/docs/what-is-code-context/)).
  - Cursor combines semantic and lexical search because each finds results the other misses ([Morph summary, secondary](https://morphllm.com/codebase-indexing)).
  - A practitioner replay on Django found that grep and a small embedding model missed different files, and that combining them reached 94% and 87% file-location success compared with 75% and 45% for grep alone ([DEV Community, practitioner experiment](https://dev.to/theaicommit/how-a-coding-agent-finds-code-grep-versus-an-embedding-index-2cpl)).

## 4. Enterprise code search and navigation platforms

### 4.1 Sourcegraph

- **What it indexes and how.**
  - Text search uses Zoekt, a trigram engine that Sourcegraph has maintained under Apache 2.0 since November 2021 ([Sourcegraph blog, 2021](https://sourcegraph.com/blog/sourcegraph-accepting-zoekt-maintainership)).
  - Precise code navigation uses SCIP, a Protobuf index format introduced in 2022 to replace LSIF, with indexers for Go, Java, TypeScript, Python, Ruby, C++, C# and other languages ([Announcing SCIP, 2022](https://sourcegraph.com/blog/announcing-scip)).
  - The Enterprise plan bundles Code Search, symbol search, code navigation, Deep Search (an agentic search), Batch Changes, Code Insights and Code Monitoring ([Sourcegraph pricing](https://sourcegraph.com/pricing)).
  - Sourcegraph 7.0, announced on 25 February 2026, repositioned the product as an "intelligence layer" for third-party agents, improved Deep Search and began rolling out a versioned API ([Sourcegraph blog](https://sourcegraph.com/blog/a-new-era-for-sourcegraph-the-intelligence-layer-for-ai-coding-agents-and-developers)).
- **Freshness.**
  - The sources reviewed do not give a re-indexing latency for text search.
  - Precise navigation is only as current as the last SCIP upload, and SCIP indexers generally need a project that compiles, so each repository needs an indexing step in CI ([Announcing SCIP, 2022](https://sourcegraph.com/blog/announcing-scip)).
- **Agent access.**
  - Sourcegraph exposes three MCP endpoints: `/.api/mcp` for a curated context-gathering set, `/.api/mcp/all` for the full suite and `/.api/mcp/deepsearch` for Deep Search only ([Sourcegraph MCP docs](https://7.5.sourcegraph.com/api/mcp)).
  - The tools include `keyword_search`, `nls_search`, `go_to_definition`, `find_references`, `commit_search`, `diff_search`, `compare_revisions`, `read_file`, `list_repos`, a metered beta `code_finder` agent and `deepsearch` ([Sourcegraph MCP docs](https://7.5.sourcegraph.com/api/mcp)).
  - Deep Search can run as a sub-agent through MCP, so the calling agent's context window is not filled with raw search results ([Sourcegraph MCP](https://sourcegraph.com/mcp)).
  - Authentication uses OAuth 2.0 or access tokens with an `mcp` scope, administrators can disable MCP or individual tools, an `MCP#ACCESS` RBAC permission is required, and existing repository permissions still apply ([Sourcegraph MCP docs](https://7.5.sourcegraph.com/api/mcp)).
- **Deployment and data residency.**
  - The Enterprise plan offers single-tenant cloud and self-hosted deployment ([Sourcegraph pricing](https://sourcegraph.com/pricing)).
  - Air-gapped deployment is not mentioned on the pricing page, and it was not confirmed in a current primary source, so a regulated buyer must confirm it directly.
- **Pricing and licence.**
  - Sourcegraph sells one Enterprise plan "starting at $16K" per year with pooled AI credits and 24x5 support ([Sourcegraph pricing](https://sourcegraph.com/pricing)).
  - The core code moved to a non-open-source licence on 13 June 2023, and the core repository was made private in August 2024 ([DevClass, August 2024](https://devclass.com/2024/08/21/sourcegraph-makes-core-repository-private-co-founder-complains-open-source-means-extra-work-and-risk/)).
  - Aggregator sites quote $59 per user per month for Cody Enterprise, which conflicts with the official page and should not be relied on ([usagepricing, secondary](https://www.usagepricing.com/blueprint/sourcegraph-cody)).
- **Evidence and customers.**
  - [Vendor claim] Sourcegraph says that "4 of the top 6 US banks" have standardised on it, without naming them ([Sourcegraph blog](https://sourcegraph.com/blog/why-code-search-at-scale-is-essential-when-you-grow-beyond-one-repository)).
  - [Vendor claim] Published case studies include FactSet, which searched more than 12,000 repositories during a Perforce-to-GitHub migration, and SoFi, Coinbase and Neo Financial ([Sourcegraph case studies](https://sourcegraph.com/case-studies)).
  - [Vendor claim] A Forrester Total Economic Impact study exists but was commissioned by Sourcegraph ([Sourcegraph, Forrester TEI](https://about.sourcegraph.com/forrester-total-economic-impact)).
  - No independent benchmark of Sourcegraph's agent tools was found.
- **Limitations.**
  - The product has changed direction repeatedly: self-serve Cody plans ended on 23 July 2025, Amp was spun out as a separate company in December 2025, and 7.0 deprecated Search Notebooks ([Sourcegraph blog, 2025](https://sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans); [HackerNoon, 2025](https://hackernoon.com/sourcegraph-spins-out-amp-to-chase-the-ai-coding-frontier)).
  - The closed licence prompted at least one open-source project to migrate to livegrep ([TVL issue 290](https://b.tvl.fyi/issues/290)).
  - Precise navigation requires a per-language build pipeline, and no SCIP indexer for COBOL was identified in this research.
  - Deep Search and `code_finder` consume credits, which turns heavy agent use into a variable cost.

### 4.2 GitHub Copilot indexing and the GitHub MCP server

- **What it indexes and how.**
  - GitHub's lexical code search engine, Blackbird, is a Rust n-gram engine that indexed about 45 million repositories and 115 TB of code at launch ([GitHub engineering blog, February 2023, vendor claim](https://github.blog/engineering/architecture-optimization/the-technology-behind-githubs-new-code-search/)).
  - Copilot builds a separate semantic (embedding) index for each repository ([GitHub Docs, repository indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)).
  - A semantic issues index was added on 20 May 2026 ([GitHub changelog](https://github.blog/changelog/2026-05-20-semantic-issue-search-in-copilot-chat/)), and whole-codebase indexing for C++ in Copilot CLI was announced on 22 September 2026 ([GitHub changelog](https://github.blog/changelog/2026-09-22-faster-c-code-intelligence-with-whole-codebase-indexing)).
  - In VS Code, Copilot can index non-GitHub repositories by uploading their content to GitHub, which a Business or Enterprise owner must enable by policy ([GitHub Docs](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)).
- **Freshness.**
  - The first semantic index build takes up to 60 seconds for a large repository, and the index usually reflects recent changes within seconds ([GitHub Docs](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)).
  - This is the fastest documented refresh in the market, and it became generally available on 12 March 2025 ([GitHub changelog, 2025](https://github.blog/changelog/2025-03-12-instant-semantic-code-search-indexing-now-generally-available-for-github-copilot/)).
- **Agent access.**
  - The Copilot cloud coding agent uses the semantic index automatically, and GitHub says it works faster as a result ([GitHub changelog, 17 March 2026](https://github.blog/changelog/2026-03-17-copilot-coding-agent-works-faster-with-semantic-code-search/)).
  - The remote GitHub MCP server, generally available since 4 September 2025, exposes `search_code` alongside issue, pull request, Actions and security toolsets ([GitHub changelog, 2025](https://github.blog/changelog/2025-09-04-remote-github-mcp-server-is-now-generally-available/)).
  - Copilot Business and Enterprise organisations govern MCP use with an "MCP servers in Copilot" policy and allowlists ([GitHub Docs, MCP](https://docs.github.com/en/copilot/concepts/customizations/mcp)).
- **Deployment and data residency.**
  - The remote MCP server is not supported on GitHub Enterprise Server, and GHES and GHE.com data-residency customers must run the local server ([GitHub Docs, MCP](https://docs.github.com/en/copilot/concepts/customizations/mcp)).
  - Non-GitHub semantic indexing is unavailable on GHE.com and GHES, and GHES documentation states that most Copilot features require a presence on GitHub Enterprise Cloud ([GHES 3.17 docs](https://docs.github.com/en/enterprise-server@3.17/copilot)).
  - GitHub states that indexed repositories are not used for model training and that content-exclusion policies filter data before it reaches Copilot Chat ([GitHub Docs](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)).
- **Pricing and licence.**
  - [Independent] In 2025 Copilot Business cost $19 and Enterprise $39 per user per month with premium-request allowances ([The Register, June 2025](https://www.theregister.com/2025/06/20/github_begins_enforcing_premium_request/)).
  - [Secondary] Premium requests were reportedly replaced by token-priced GitHub AI Credits on 1 June 2026, which drew complaints about cost predictability ([heise](https://heise.de/-10511480); [letsdatascience](https://letsdatascience.com/blog/github-copilot-usage-based-billing-developer-backlash)).
- **Evidence and customers.**
  - [Independent] Citi has equipped 30,000 to 40,000 developers with AI coding tools, and its CTO estimated that regular Copilot users gain 5% to 15% productivity, which is an executive estimate rather than a measured study ([American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers); [Yahoo Finance](https://finance.yahoo.com/news/citi-deploys-ai-coding-tools-152606091.html)).
  - [Secondary] A third-party blog attributes a 2% task-completion gain to the coding agent's semantic search, but this was not verified against GitHub's own text ([digitalapplied](https://www.digitalapplied.com/blog/github-copilot-coding-agent-50-percent-faster-semantic-search)).
- **Limitations.**
  - The semantic index is per repository, and no compiler-accurate cross-repository reference tool is exposed through MCP in the sources reviewed.
  - Firms on GHES lose most of the indexing features, which is significant because many banks run GHES.
  - [Independent] In May 2025 Invariant Labs showed that a malicious public issue could steer an agent using the GitHub MCP server into copying private repository data into a public pull request ([Tessl, 2025](https://tessl.io/blog/malicious-github-issue-ai-agent-leak/)).

### 4.3 GitLab exact code search and GitLab Orbit

- **What it indexes and how.**
  - GitLab exact code search is built on Zoekt, and on Self-Managed an administrator must deploy Zoekt nodes ([GitLab Docs](https://docs.gitlab.com/user/search/exact_code_search)).
  - GitLab Orbit, previously called the GitLab Knowledge Graph, entered public beta on 10 June 2026 and builds one graph across code, work items, pipelines, deployments and production signals ([GitLab blog](https://about.gitlab.com/blog/introducing-gitlab-orbit/)).
  - Orbit Remote indexes files, directories, definitions, imports and calls on each project's default branch, and Orbit Local is an embedded engine that agents query on the developer's machine ([What Orbit indexes](https://docs.gitlab.com/orbit/remote/indexing/); [Orbit Local](https://docs.gitlab.com/orbit/local/)).
  - Orbit replicates GitLab's Postgres through change data capture into a ClickHouse data lake, with indexers reading from Gitaly and writing through NATS ([GitLab runbook](https://runbooks.gitlab.com/orbit/)).
- **Freshness.**
  - Initial indexing takes minutes and up to a few hours for large codebases, and later updates arrive within seconds to minutes ([GitLab Docs](https://docs.gitlab.com/orbit/remote/indexing/)).
  - Code on non-default branches must be queried through the local graph.
- **Agent access.**
  - Orbit serves the graph to the GitLab CLI, an MCP endpoint, a REST API and the GitLab Duo Agent Platform, and every query is filtered by the user's GitLab permissions ([GitLab Orbit docs](https://docs.gitlab.com/orbit/)).
  - GitLab names Claude Code, Codex and OpenCode as MCP clients ([GitLab blog](https://about.gitlab.com/blog/introducing-gitlab-orbit/)).
  - A GitLab issue notes that exact code search itself has no MCP server and no `glab` CLI support ([GitLab issue 624419](https://gitlab.com/gitlab-org/gitlab/-/work_items/624419)).
- **Deployment and data residency.**
  - Orbit runs on GitLab.com, GitLab Self-Managed on Kubernetes and GitLab Dedicated, which makes it one of the few graph products that can run fully on customer infrastructure ([GitLab Orbit docs](https://docs.gitlab.com/orbit/)).
  - When Orbit is disabled for a group, indexed data is kept for 30 days ([GitLab Docs](https://docs.gitlab.com/orbit/remote/indexing/)).
- **Pricing and licence.**
  - Orbit is included for Premium and Ultimate customers, and no Orbit-specific add-on price was found ([GitLab Orbit docs](https://docs.gitlab.com/orbit/)).
- **Evidence and customers.**
  - [Vendor claim] GitLab says Orbit indexed more than 40,000 of its own projects in under 45 minutes, and that agents using Orbit answered up to 11 times faster with up to 4.5 times fewer tokens ([GitLab blog](https://about.gitlab.com/blog/introducing-gitlab-orbit/)).
  - [Independent] General availability began in October 2026, although sources disagree on the exact date ([HPCwire, 30 October 2026](https://www.hpcwire.com/aiwire/2026/10/30/gitlab-orbit-now-generally-available-makes-ai-agents-more-accurate-and-less-expensive-to-run/)).
  - No independent review after general availability and no named bank customer were found.
- **Limitations.**
  - Orbit's code model records definitions, imports and calls rather than compiler-resolved references, so it is likely less accurate than SCIP for overloaded symbols and cross-repository references (inference).
  - The remote graph covers only the default branch.
  - The status of exact code search on Self-Managed is unclear, because its documentation page says "Limited availability" while a separate page mentions general availability in 19.5 ([GitLab Docs](https://docs.gitlab.com/user/search/exact_code_search)).
  - Orbit had been generally available for only a few weeks at the time of writing.

### 4.4 Atlassian Rovo code context

- **What it indexes and how.**
  - Code context indexes Bitbucket repositories directly and mirrors GitHub repositories before indexing, and it combines lexical and embedding search ([Atlassian support](https://support.atlassian.com/rovo/docs/what-is-code-context/)).
  - It was rolling out to paid customers through an open beta at the time of the sources reviewed.
- **Freshness.**
  - Pushes trigger incremental re-indexing, but recently pushed code may not appear immediately, and the initial index can take 24 to 48 hours depending on which Atlassian page is read ([Set up code context](https://support.atlassian.com/rovo/docs/set-up-code-context-for-your-site/)).
- **Agent access.**
  - The Rovo MCP Server is hosted at `mcp.atlassian.com/v2/mcp`, and its code search tool searches and reads code across connected providers ([Rovo MCP docs](https://developer.atlassian.com/cloud/rovo-mcp/)).
  - Rovo MCP added Bitbucket Cloud tools for repositories, commits and pull requests, and a separate MCP server for Bitbucket Data Center has been released ([Atlassian blog](https://www.atlassian.com/blog/bitbucket/the-atlassian-rovo-mcp-server-now-supports-bitbucket-cloud); [Atlassian community](https://community.developer.atlassian.com/t/mcp-for-bitbucket-dc-has-been-released/102963)).
  - Results are scoped to what each user or authorised agent is permitted to see.
- **Deployment and data residency.**
  - Atlassian stores code context data in an isolated environment in the United States, and disabling the feature deletes embeddings, indices and code chunks ([Atlassian support](https://support.atlassian.com/rovo/docs/what-is-code-context/)).
- **Pricing and licence.**
  - Code search calls through MCP consume Rovo credits ([Rovo MCP docs](https://developer.atlassian.com/cloud/rovo-mcp/)).
- **Evidence and customers.**
  - [Independent] Atlassian was placed as a Niche Player in the May 2026 Gartner Magic Quadrant for Enterprise AI Coding Agents ([Virtualization Review](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)).
  - No outcome data or named customers for code context were found.
- **Limitations.**
  - United States storage is likely to block firms with EU, UK or APAC residency requirements unless Atlassian has added regions not found in this research.
  - The feature is in beta, and a third-party source reports that standalone Rovo Dev is heading to end of life ([crosstowntech, secondary](https://crosstowntech.com/apps/rovo-dev-guide/)).

### 4.5 Google Gemini Code Assist code customization

- **What it indexes and how.**
  - Code customization indexes private repositories connected through Google Cloud Developer Connect and is available only in Gemini Code Assist Enterprise ([Google Cloud docs](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization-overview?hl=en)).
- **Freshness.**
  - The index refreshes every 24 hours, which is the slowest documented refresh among the major platforms ([Google Cloud docs](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization-overview?hl=en)).
- **Agent access.**
  - No source confirmed that the index is exposed through MCP.
- **Deployment and data residency.**
  - The index lives in Google Cloud ([Configure code customization](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization)).
- **Pricing and licence.**
  - The feature requires the Enterprise edition, and list prices were not retrieved.
- **Evidence and customers.**
  - [Independent] Google moved from Leader in 2025 to Challenger in the May 2026 Gartner Magic Quadrant ([Virtualization Review](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)).
- **Limitations.**
  - The service allows one index per project and per organisation and caps indexing at 20,000 repositories ([Gemini Code Assist quotas](https://developers.google.com/gemini-code-assist/resources/quotas?authuser=0)).
  - A 24-hour refresh means agents can reason over code that is up to a day old, which matters for fast-moving trading code.

### 4.6 Sourcebot and the open-source search engines

- **What it indexes and how.**
  - Sourcebot is a self-hostable code search product built on Zoekt ([Sourcebot vs OpenGrok, vendor blog](https://www.sourcebot.dev/blog/sourcebot-vs-opengrok)).
  - Zoekt is an Apache 2.0 trigram engine that also powers Sourcegraph and GitLab exact code search ([sourcegraph/zoekt](https://www.github.com/sourcegraph/zoekt)).
  - OpenGrok is an Oracle-maintained Java search and cross-reference engine under CDDL 1.0, with release 1.14.17 reported on 24 August 2026 ([Unblocked roundup, vendor blog](https://getunblocked.com/blog/sourcegraph-alternatives/)).
  - livegrep provides interactive regex search over multi-gigabyte repositories and requires running its backend and web interface separately ([Slashdot comparison, secondary](https://slashdot.org/software/comparison/Sourcebot-vs-livegrep/)).
- **Freshness.**
  - The sources reviewed do not document refresh latency, which in practice depends on how often the operator syncs repositories.
- **Agent access.**
  - Sourcebot has an MCP server that requires an active Enterprise licence ([Sourcebot docs](https://docs.sourcebot.dev/docs/features/mcp-server)).
  - No official MCP servers were found for Zoekt, OpenGrok or livegrep.
- **Deployment and data residency.**
  - All of these tools are self-hosted, and Sourcebot offers an offline licence option in its Enterprise tier ([Sourcebot pricing](https://sourcebot.dev/pricing)).
- **Pricing and licence.**
  - Sourcebot uses the Functional Source License, which forbids offering it as a competing hosted product until each version's change date ([Sourcebot blog, 2025](https://sourcebot.dev/blog/fair-source)).
  - Its pricing page shows a $25 per seat monthly tier, while its own llms.txt lists $20 per user per month, so the price must be confirmed ([Sourcebot pricing](https://sourcebot.dev/pricing); [Sourcebot llms.txt](https://www.sourcebot.dev/llms.txt)).
- **Evidence and customers.**
  - No named bank customers and no independent benchmarks were found, and the available comparisons are vendor-authored.
- **Limitations.**
  - The sources describe text search only, and they do not document compiler-accurate navigation for Sourcebot.
  - The open-source engines need in-house operation and have no agent interface without additional work.

### 4.7 Meta Glean and Google Kythe

- Meta's Glean is an open-source code fact store, and it is unrelated to Glean the enterprise search company described in section 5.6.
- **What it indexes and how.**
  - Glean collects, derives and queries facts about source code with a declarative query language called Angle, and Meta uses it internally for code browsing, search and documentation ([Meta Engineering, December 2024](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)).
  - Glean ingests SCIP indexes for Rust, Go, TypeScript, Java, Python and .NET, so SCIP indexers can feed it ([Glean README](https://hackage.haskell.org/package/glean-0.1.0.0/src/README.md)).
  - Kythe is Google's language-agnostic cross-reference graph schema and toolchain, announced in 2015, with indexers for C++, Java, Go, TypeScript and Protocol Buffers ([Google Open Source blog, 2015](https://opensource.googleblog.com/2015/01/kythe-new-approach-to-making-developer.html); [kythe.io](https://kythe.io/)).
- **Freshness.**
  - Freshness depends entirely on the indexing pipeline that the adopter builds.
- **Agent access.**
  - Neither project has an official MCP server, so an adopter must write one.
- **Deployment and data residency.**
  - Both are self-hosted open source.
- **Pricing and licence.**
  - Both are free open source, and the cost is engineering effort.
- **Evidence and customers.**
  - [Vendor claim] Meta built Glean to index its monorepo, which is the strongest open-source evidence of indexing at multi-million-line scale ([Meta Engineering, December 2024](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)).
  - [Independent] Google's internal Code Search used Kythe for cross-references according to a 2020 report ([InfoQ, April 2020](https://www.infoq.com/news/2020/04/google-code-search-available)).
- **Limitations.**
  - Some of Meta's production indexers are not part of the open-source release ([Glean README](https://hackage.haskell.org/package/glean-0.1.0.0/src/README.md)).
  - [Secondary] The Google team working on Kythe was reportedly laid off in April 2024 ([Wikipedia](https://en.wikipedia.org/wiki/Google_Kythe)).
  - These are building blocks for a platform team rather than products, and no published figures exist for the engineering effort needed to run them on a polyglot estate.

## 5. AI context engines

- AI context engines index code, and often tickets and documents, so that an agent receives a focused set of relevant material.
- Their pitch changed during 2026 from "use our IDE" to "use our context inside your agent", and most of them now ship an MCP server.
- Vendors rarely publish refresh latencies or maximum estate sizes, so claims of "enterprise monorepo scale" are mostly unquantified.

### 5.1 Augment Context Engine

- **What it indexes and how.**
  - [Vendor claim] Augment describes semantic search that "understands relationships, dependencies, and architectural patterns" and says it works with "codebases of any size", without stating limits ([Augment blog](https://www.augmentcode.com/blog/context-engine-mcp-now-live)).
  - A related Augment post indicates that commit history is indexed.
- **Freshness.**
  - No refresh latency is published.
- **Agent access.**
  - The Context Engine MCP became generally available on 6 February 2026 in a local mode (the Auggie CLI as a stdio MCP server over the working directory) and a remote mode (a hosted endpoint for context across all repositories) ([Augment docs](https://docs.augmentcode.com/context-services/overview)).
  - Augment lists Claude Code, Codex and Gemini CLI among supported clients, but the launch page does not name the MCP tools.
- **Deployment and data residency.**
  - The remote engine is a SaaS service, and regional data residency was not confirmed.
  - [Vendor claim] Augment lists SOC 2 Type II, ISO/IEC 42001 and customer-managed encryption keys, and the ISO/IEC 42001 certificate was issued by Coalfire in August 2025 ([Augment security](https://augmentcode.com/security); [Coalfire, 2025](https://coalfire.com/insights/news-and-events/press-releases/augment-ai-achieves-iso-iec-42001-certification-from-coalfire-certification-marking-a-milestone-in-responsible-ai-governance)).
- **Pricing and licence.**
  - Augment moved to monthly credit pools on 20 October 2025 (40,000, 130,000 and 450,000 credits, with custom Enterprise terms), which users criticised ([Augment blog, 2025](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing); [The Register, 2025](https://www.theregister.com/2025/10/15/augment_pricing_model/)).
  - [Secondary] Further shifts to usage billing in mid-2026 are reported by trackers but were not confirmed on a primary page.
- **Evidence and customers.**
  - [Vendor claim] Adding the Context Engine improved agent output by 71% for Cursor with Opus 4.5, 80% for Claude Code with Opus 4.5 and 30% for Cursor with Composer-1, measured on 300 Elasticsearch pull requests with three prompts each, with no variance published ([Augment blog](https://www.augmentcode.com/blog/context-engine-mcp-now-live)).
  - [Independent] Augment has only two G2 reviews averaging 2.8 stars, so independent user feedback is thin ([G2](https://www.g2.com/sellers/augment-code)).
  - No financial-services customers were named.
- **Limitations.**
  - Cross-repository context requires the hosted remote engine, which may conflict with source-code residency rules.
  - Credit pricing makes agent-heavy usage hard to budget.

### 5.2 Cursor codebase indexing

- **What it indexes and how.**
  - Cursor builds a Merkle tree of file hashes on the client so that only changed files are re-embedded, and it reuses an existing team index for new team members through a similarity hash ([Cursor blog](https://cursor.com/blog/secure-codebase-indexing)).
  - [Secondary] Reports describe AST-aware chunking with tree-sitter and storage in turbopuffer for vector and full-text search ([Engineer's Codex](https://read.engineerscodex.com/p/how-cursor-indexes-codebases-fast)).
- **Freshness.**
  - [Secondary] Modified files are reported to re-sync roughly every 10 minutes ([Bito guide](https://bito.ai/blog/how-cursors-codebase-indexing-works-2026-guide/)).
  - [Secondary] Index reuse reportedly cut time to first index for a large repository from about four hours to 21 seconds in January 2026 ([pulse.bot](https://www.pulse.bot/ai/news/cursor-slashes-codebase-indexing-from-four-hours-to-21-seconds-543a7632-a105-4df1-b4ab-346a47a83fbd)).
- **Agent access.**
  - The index serves Cursor's own agents, and the sources reviewed do not describe an MCP endpoint that exposes it to other agents.
- **Deployment and data residency.**
  - Embeddings and obfuscated file paths are stored in Cursor's cloud, and Cursor says plaintext code is not stored server-side ([Cursor blog](https://cursor.com/blog/secure-codebase-indexing)).
  - Regional residency options were not confirmed.
- **Pricing and licence.**
  - Cursor moved from flat-rate plans to usage-based pricing in June 2025 ([heise](https://heise.de/-10511480)), and enterprise prices were not retrieved.
- **Evidence and customers.**
  - [Vendor claim] Cursor reported that its agents answered 12.5% more questions correctly with the semantic index than without it ([Dbggr summary](https://dbggr.dev/articles/embeddings-vs-grep-agentic-search/)).
  - [Independent] Cursor was named a Leader in the May 2026 Gartner Magic Quadrant ([Virtualization Review](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)).
- **Limitations.**
  - The index is tied to the Cursor editor and its cloud.
  - [Independent] Cursor had several 2025 MCP-related vulnerabilities, including CVE-2025-54136, in which an approved MCP configuration could later be changed to run malicious commands ([The Hacker News, 2025](https://thehackernews.com/2025/08/cursor-ai-code-editor-vulnerability.html)).

### 5.3 Qodo Context Engine and Qodo Aware

- **What it indexes and how.**
  - The on-premises Context Engine consists of a metadata service, a RAG indexer and a context retriever backed by PostgreSQL, and repositories are added explicitly to its index ([Qodo docs](https://docs.qodo.ai/on-prem/context-engine/setup-context-engine)).
  - Qodo also markets cross-repository review and "mined rules" inferred from the codebase ([Qodo blog](https://www.qodo.ai/?p=15395)).
- **Freshness.**
  - No refresh latency was documented.
- **Agent access.**
  - Qodo Aware exposes Qodo's context to agents and has documented enterprise self-hosted deployment ([Qodo Aware docs](https://docs.qodo.ai/qodo-aware/getting-started/enterprise-self-hosted)).
  - The exact MCP tool schema was not retrieved.
- **Deployment and data residency.**
  - The engine connects to GitHub Cloud or Enterprise, GitLab and Bitbucket Data Center ([Qodo architecture](https://docs.qodo.ai/on-prem/qodo-on-premise/architecture.md)).
  - [Vendor claim] Qodo markets air-gapped installation with GitHub Enterprise, GitLab Self-Managed, Bitbucket Data Center and Gerrit ([Qodo enterprise](https://www.qodo.ai/enterprise/)).
- **Pricing and licence.**
  - Prices were not retrieved, and Qodo raised a $70M Series B in March 2026 ([Wikipedia](https://en.wikipedia.org/wiki/Qodo)).
- **Evidence and customers.**
  - No independent outcome data or named financial-services customers were found.
- **Limitations.**
  - The on-premises Context Engine requires access to gpt-5 and claude-4.1-opus, and a custom LLM gateway requires contacting support, so "on-premises" does not mean "no external model" ([Qodo docs](https://docs.qodo.ai/on-prem/context-engine/setup-context-engine)).
  - Security certifications were not verified in this research.

### 5.4 Tabnine Enterprise Context Engine

- **What it indexes and how.**
  - The engine builds a continuously updated knowledge graph of entities, relationships, dependencies and architectural patterns from repositories, documentation, tickets, APIs and infrastructure metadata ([Business Wire](https://www.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise)).
- **Freshness.**
  - The engine is described as continuously updated, but no latency is published.
- **Agent access.**
  - Whether the engine remains available through MCP to non-Tricentis agents after the acquisition is unknown.
- **Deployment and data residency.**
  - Tabnine lists SaaS, VPC, on-premises and fully air-gapped deployment, and it states that it does not retain or train on customer code ([Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)).
- **Pricing and licence.**
  - Pre-acquisition list prices were $39 per user per month for Code Assistant and $59 for Agentic on annual terms ([Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)).
- **Evidence and customers.**
  - [Vendor claim] Tricentis cites up to 2 times better AI accuracy, up to 80% fewer tokens and up to 50% faster complex tasks ([Business Wire](https://www.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise)).
  - [Independent] Tabnine was the only Visionary in the May 2026 Gartner Magic Quadrant ([Virtualization Review](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)).
- **Limitations.**
  - Tricentis acquired Tabnine on 30 July 2026 to fold the context engine into a testing platform, and only "support" was promised to existing customers ([Business Wire](https://www.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise)).
  - Tricentis shut down an earlier acquisition, Flood.io, on 30 June 2024 with 20 days' notice, which is a relevant precedent for contract terms ([Beri analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)).

### 5.5 Bito AI Architect

- **What it indexes and how.**
  - AI Architect builds a knowledge graph from repositories down to modules, APIs and libraries, and it adds operational history from issue trackers such as Jira ([Bito docs](https://docs.bito.ai/ai-architect/overview)).
- **Freshness.**
  - No refresh latency was documented.
- **Agent access.**
  - After indexing, Bito returns an MCP URL and token for Claude Code, Cursor, Windsurf, GitHub Copilot in VS Code and Codex, and the same graph feeds Bito's code review agent ([Bito docs](https://docs.bito.ai/ai-architect); [Bito key features](https://docs.bito.ai/ai-architect/key-features)).
- **Deployment and data residency.**
  - The documented setup is Bito-hosted, and self-hosting was not documented in the sources reviewed.
- **Pricing and licence.**
  - Prices were not retrieved.
- **Evidence and customers.**
  - [Vendor claim] Bito reports 70.1% task success with AI Architect versus 51.9% without it on Claude Opus 4.6 ([Bito](https://bito.ai/product/grounded-coding/)).
- **Limitations.**
  - Certifications, residency options and named financial-services customers were not found.

### 5.6 Other context engines and knowledge platforms

- Glean in this table is the enterprise search company, which is unrelated to Meta's Glean in section 4.7.

| Product | What it indexes and how | Freshness | Agent access | Deployment and residency | Pricing and licence | Evidence and customers | Limitations |
|---|---|---|---|---|---|---|---|
| Unblocked | Synthesises code, documents, chat and tickets into one context engine ([Unblocked](https://getunblocked.com/blog/inside-the-unblocked-context-engine/index.md)) | Not published | MCP server and CLI, generally available April 2026 ([Unblocked](https://getunblocked.com/blog/mcp-beta/index.md)) | Not confirmed | Not retrieved | [Vendor claim] 42% fewer tokens and 64% fewer tool calls than raw context dumping ([Unblocked](https://getunblocked.com/blog/why-mcp-isnt-enough-enhancing-agent-capabilities-with-a-context-engine/index.md)) | Certifications and residency were not verified |
| Glean (enterprise search) | Code files, snippets, commits and pull request diffs from connected repositories ([Glean docs](https://docs.glean.com/tools/glean/code-search)) | Not published | Glean MCP server, with enterprise MCP actions added March 2026 ([Glean blog](https://www.glean.com/blog/mcp-mar-drop-2026)) | SaaS | Not retrieved | No code-specific outcome data | Code is one connector among many, not a precise code index |
| Cognition (Devin, DeepWiki, SWE-grep, Codemaps) | SWE-grep is a fast agentic retrieval subagent, and Codemaps (late 2025) generates annotated structural maps ([testingcatalog, 2025](https://www.testingcatalog.com/windsurf-is-getting-codemaps-for-ai-assisted-coding/)) | Search is live, and wiki freshness is not documented | Public DeepWiki MCP server ([DeepWiki MCP](https://docs.devin.ai/work-with-devin/deepwiki-mcp)) | SaaS | Not retrieved | [Vendor claim] SWE-grep is about 10 times faster than standard agentic search; [Independent] Goldman Sachs deployed Devin in 2025 ([Quartz, 2025](https://qz.com/goldman-sachs-ai-coder-devin-cognition)) | Windsurf was reportedly renamed Devin Desktop in June 2026, which shows product churn ([webauditos, secondary](https://webauditos.com/guides/windsurf)) |
| Factory | Knowledge droid indexes repository, documents and ticket history in Chroma Cloud ([Chroma case study](https://www.trychroma.com/customers/factory-ai-case-study)) | Selects the index matching the current branch and commit | Used by Factory's own droids | [Secondary] On-premises options, customer-managed keys and residency controls ([digitalapplied](https://www.digitalapplied.com/blog/factory-ai-multi-agent-coding-platform-review)) | Not retrieved; $150M Series C in April 2026 ([idlen](https://www.idlen.io/news/factory-ai-150-million-1-5-billion-droids-coding-agents-enterprise-april-2026/)) | No independent outcome data | The index serves Factory's platform rather than arbitrary agents |
| Greptile | [Secondary] Repository-wide semantic graph used for code review ([cubic review](https://www.cubic.dev/blog/greptile-review)) | Not published | Review product rather than a general context API | Enterprise self-hosting with SSO ([llms.blog](https://www.llms.blog/posts/greptile-raises-50m-at-a-750m-valuation-what-the-ai-code-reviewer-does-and-what-it-costs)) | $30 per seat with 50 credits and $1 per extra credit since March 2026 | [Secondary] An 82% bug-detection rate is reported by a single blog | Per-review credit pricing drew criticism ([Agent Wars](https://www.agent-wars.com/news/2026-05-01-greptile-per-review-pricing)) |
| Zencoder | Embeds repositories into a vector database and builds a graph, called Repo Grokking ([InfoWorld, February 2025](https://www.infoworld.com/article/3820199/review-zencoder-has-a-vision-for-ai-coding.html)) | Re-scans when code changes (2025) | Not confirmed | Not confirmed | Not retrieved | No independent data | The most recent source found is from 2025 |

### 5.7 Index-free agentic search as the baseline

- **What it indexes and how.**
  - Claude Code uses model-driven grep, glob and file reads at runtime instead of a persistent index, and an early version with a local vector database was dropped ([Morph summary, secondary](https://morphllm.com/codebase-indexing)).
  - Cline deliberately does not index, arguing that chunking code for embeddings breaks code logic and that a fresh index needs a continuous pipeline ([Cline blog](https://cline.bot/blog/why-cline-doesnt-index-your-codebase-and-why-thats-a-good-thing)).
  - OpenHands relies on shell tools and a file editor inside a sandbox ([OpenHands](https://github.com/All-Hands-AI/OpenHands)).
- **Freshness.**
  - Results always reflect the current working copy, because nothing is indexed in advance.
- **Agent access.**
  - The agent's own file tools are the interface, so no MCP server is needed.
- **Deployment and data residency.**
  - Nothing is copied into a separate index, which removes one data store from a security review, although code still flows to whichever model provider the agent uses.
- **Pricing and licence.**
  - There is no index licence, and the cost is paid in tokens and tool calls.
- **Evidence and customers.**
  - [Independent] On ContextBench Lite, the bash-only mini-SWE-agent had the highest file-level F1 (0.634) and block-level F1 (0.375) of the five agents tested ([arXiv 2602.05892](https://arxiv.org/html/2602.05892)).
  - [Secondary] Anthropic's guidance, as reported secondhand, is to start with agentic search and add semantic search only when faster results are needed ([jacar.es](https://jacar.es/en/code-agents-without-vector-search/)).
- **Limitations.**
  - Agentic search costs more tokens and tool calls per question on very large codebases, and it cannot search repositories that are not checked out locally.
  - The supporting evidence comes from repositories far smaller than a multi-million-line estate.

## 6. Open-source and self-hostable agent tools

### 6.1 Indexing foundations and their maintenance status

- The safe foundations in late 2026 are tree-sitter, Language Server Protocol servers, SCIP and, for very large fact stores, Meta's Glean.
- Several earlier foundations are no longer viable, and tools built on them carry inherited abandonment risk.

| Foundation | Role | Status in November 2026 | Main limitation |
|---|---|---|---|
| SCIP | Compiler-accurate definitions and references | Active; scip-java shipped 0.12.0 to 0.12.3 in March and April 2026 ([Maven Central](https://repo1.maven.org/maven2/com/sourcegraph/scip-java_2.13/0.12.3)); a move to open governance is reported but unverified | Needs a compilable project; scip-python and scip-dotnet status not confirmed |
| tree-sitter | Incremental syntax parsing for hundreds of languages ([tree-sitter](https://tree-sitter.github.io/tree-sitter/)) | Active, and the parser under most agent graph tools | Syntax only, so call edges are name-matched heuristics |
| LSP servers | Live definitions, references, rename and diagnostics ([LSP specification](https://microsoft.github.io/language-server-protocol/)) | Active | One long-running process per language, and quality varies by server |
| LSIF | Older JSON index format | Superseded by SCIP since 2022 ([Announcing SCIP, 2022](https://sourcegraph.com/blog/announcing-scip)) | Not a foundation for new work |
| Stack Graphs | GitHub's tree-sitter name resolution | Archived on 9 September 2025 ([github/stack-graphs](https://github.com/github/stack-graphs)) | Read-only |
| Kuzu | Embedded graph database used by several code-graph tools | Archived on 10 October 2025; continued as the LadybugDB fork, which has no commercial backing ([OneUptime](https://oneuptime.com/blog/post/2026-08-12-kuzu-to-ladybugdb-packages-apis-extensions-database-files/markdown)) | Migration needs a logical export and package renames |

### 6.2 Serena and other LSP-based MCP servers

- **What it indexes and how.**
  - Serena (Oraios AI) is an MCP server that offers symbol-level retrieval and editing, including find symbol, find referencing symbols, find implementations, diagnostics, replace symbol body and rename, over language servers for more than 40 languages ([oraios/serena](https://github.com/oraios/serena)).
  - It keeps no persistent index of its own and can optionally use a paid JetBrains plugin as its backend.
  - mcp-language-server exposes definition, references, diagnostics, hover and rename from any stdio language server such as gopls, pyright or clangd ([mcp-language-server](https://github.com/isaacphi/mcp-language-server)), and multilspy is the Microsoft Research library from which Serena's language-server layer descends ([multilspy](https://github.com/microsoft/multilspy)).
- **Freshness.**
  - Queries run live against the language server, so results reflect the current working copy (inference from the LSP design).
- **Agent access.**
  - Serena is an MCP server, and version 2 adds a REPL-based agent interface.
- **Deployment and data residency.**
  - Serena runs locally on the developer's machine or in the agent's sandbox, so no code leaves that environment through Serena itself.
- **Pricing and licence.**
  - With version 2 (October 2026), the Serena application became GPL-3.0-or-later while the SolidLSP component stayed MIT, and many directory sites still incorrectly describe it as MIT ([oraios/serena](https://github.com/oraios/serena)).
- **Evidence and customers.**
  - Serena had about 31,300 GitHub stars in November 2026, which shows adoption but not outcomes.
  - The project reports an internal evaluation of about 20 tasks without formal figures.
  - [Independent] A 2026 preliminary study of whether a language server saves tokens found an LSP-only configuration reached 0.778 F1 but used 19% more tokens overall, with the largest gain on one repository ([ResearchGate preprint](https://www.researchgate.net/publication/412312362_Does_a_Language_Server_Save_Tokens_for_Coding_Agents_A_Measurement_Methodology_and_Preliminary_Study)).
- **Limitations.**
  - With the free backend, find-declaration generally fails for symbols in external dependencies, and move, inline and propagate-deletion need the paid JetBrains plugin ([oraios/serena](https://github.com/oraios/serena)).
  - It works on the checked-out workspace, so it does not answer estate-wide questions across thousands of repositories.
  - The GPL licence matters to firms that want to embed or redistribute it.

### 6.3 Tree-sitter code-graph MCP servers

- These tools parse code with tree-sitter into a graph and expose it through MCP, which makes their call and reference edges name-matched heuristics rather than compiler-resolved facts.
- The category is less than two years old and dominated by small teams, so maintenance should be checked at adoption time.

| Tool | What it indexes and how | Freshness | Agent access | Deployment and residency | Licence | Evidence | Limitations |
|---|---|---|---|---|---|---|---|
| GitNexus | Tree-sitter graph for 12 languages in KuzuDB ([GitNexus README](https://cdn.jsdelivr.net/npm/gitnexus@1.6.9/README.md)) | Re-run `analyze` | MCP server, CLI and browser UI | Local | Open source | Star counts conflict between 33,000 and 45,000 ([SourcePulse](https://www.sourcepulse.org/projects/22555251)) | Depends on archived Kuzu; known gaps in Swift |
| codebase-memory-mcp | Persistent tree-sitter graph for 66 languages ([arXiv 2603.27277](https://arxiv.org/abs/2603.27277)) | Incremental | MCP server | Local | Open source | [Independent preprint by the authors] 83% answer quality versus 92% for grep-and-read, with about 10 times fewer tokens | Lower answer quality than the file-reading baseline |
| Codanna | Rust call and type graph with local embeddings ([Kumanyaev comparison](https://zzet.org/gortex/local-code-graph-mcp-servers-compared/)) | Incremental | MCP server | Local, read-only | Apache 2.0 | [Vendor claim] Over 75,000 symbols indexed per second | 687 stars in June 2026, so a small community |
| CodeGraphContext | Tree-sitter graph optionally enriched with SCIP, in FalkorDB Lite, Kuzu, LadybugDB or Neo4j ([repowise](https://repowise.dev/blog/comparisons/best-code-graph-mcp-servers)) | Incremental | MCP server | Local or server store | Open source | [Vendor-run benchmark] Incremental updates missed up to 474 edges found by a fresh build ([PipesHub](https://pipeshub.com/blog/code-graph-benchmark)) | Graph drift, which implies periodic full rebuilds |
| Gortex | Graph with BM25, vectors and graph reranking for 257 languages | Incremental | MCP server | Local | Apache 2.0 | Described only by its own author | Self-reported comparison |
| code-graph-rag | Tree-sitter graph in Memgraph queried with generated Cypher ([code-graph-rag](https://github.com/vitali87/code-graph-rag)) | Re-run ingestion | Natural-language queries | Local or server | Open source | None found | Generated queries are hard to validate |
| Blarify and Potpie | Tree-sitter plus language-server references in Neo4j or FalkorDB ([Blarify](https://github.com/blarApp/blarify)); Potpie runs agents over a Neo4j graph ([Potpie](https://github.com/potpie-ai/potpie)) | Re-run ingestion | Library and agents | Local or server | Open source; Potpie is Apache 2.0 | None found | Neo4j Community is GPLv3 and single-instance |
| Aider repo map | Tree-sitter definitions and references ranked with a PageRank-style algorithm into a token-budgeted map of about 1,000 tokens ([Aider](https://aider.chat/docs/repomap.html)) | Rebuilt per session | Built into Aider | Local | Open source | None found | A summary map rather than a queryable graph |

- [Independent] The largest public test of these tools ran on Kubernetes (146,000 graph nodes) and VS Code (219,000 nodes), and no public test on a multi-million-line polyglot estate was found ([nefayran/code-graph-vs-grep](https://github.com/nefayran/code-graph-vs-grep)).

### 6.4 Embedding-based MCP servers

| Tool | What it indexes and how | Freshness | Agent access | Deployment and residency | Licence | Evidence | Limitations |
|---|---|---|---|---|---|---|---|
| claude-context (Zilliz) | Chunks and embeds code into Milvus or Zilliz Cloud with hybrid BM25 and vector search ([claude-context](https://github.com/zilliztech/claude-context)) | Merkle-tree incremental re-indexing | MCP server | Self-hosted Milvus or Zilliz Cloud | MIT | [Vendor claim] About 40% token reduction; a third party reproduced 39.4% on release 0.1.0 ([evaluation README](https://glama.ai/mcp/servers/@zilliztech/claude-context/blob/2484ae29b3a9c92815f1524cbb9924b3e241ec17/evaluation/README.md)) | The claim comes from a vector-database vendor, and an embedding model must be hosted or called |
| ChunkHound | AST-aware chunking and regex search without a graph | Incremental | MCP server | Local | MIT | [Author paper] +4.3 recall on RepoEval and +2.67 pass@1 on SWE-bench versus naive chunking ([Kumanyaev comparison](https://zzet.org/gortex/local-code-graph-mcp-servers-compared/)) | No structural relationships |
| Roo Code indexing | Tree-sitter chunks embedded into Qdrant ([Roo Code docs](https://docs.roocode.com/features/codebase-indexing)) | Incremental | Built into Roo Code | Local or self-hosted Qdrant, with Ollama possible | Open source | None found | Tied to one agent |

### 6.5 Structural search and code-as-database engines

| Tool | What it indexes and how | Freshness | Agent access | Deployment and residency | Licence | Evidence | Limitations |
|---|---|---|---|---|---|---|---|
| ast-grep | Tree-sitter structural search, lint and rewrite with code-like patterns ([ast-grep](https://github.com/ast-grep/ast-grep)) | No index, so always current | MCP server ([ast-grep-mcp](https://github.com/ast-grep/ast-grep-mcp)) | Local | MIT | None found | Syntax only, with no type information |
| Probe | ripgrep-speed search returning whole functions or classes ([Probe](https://github.com/probelabs/probe)) | No index | CLI and MCP server | Local | Open source | None found | No cross-file relationships |
| CodeQL | Relational database of ASTs, data flow, control flow and types extracted from a build ([comparison](https://elmanto.github.io/posts/sast_derby_joern_vs_codeql)) | Rebuilt per analysis | Query language; no agent server found | Local or GitHub | Free for open source and research; private commercial code needs GitHub Advanced Security ([licence](https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md)) | [Independent] Recommended for whole-codebase analysis | Needs a build for compiled languages; no COBOL or SQL ([CodeQL languages](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/)) |
| Joern | In-memory code property graph combining AST, control flow and program dependence ([joern.io](https://joern.io/)) | Rebuilt per analysis | Query shell | Local | Apache 2.0 | [Independent] Requires a lot of RAM on very large repositories ([arXiv 2603.24837](https://arxiv.org/html/2603.24837v1)) | No COBOL frontend |
| Semgrep and Opengrep | Pattern-based multi-language analysis | No index | CLI | Local | Semgrep moved some features out of open source in December 2024 and January 2025, which led to the LGPL Opengrep fork ([Opengrep](https://www.opengrep.dev/)) | None specific to agents | Pattern rules rather than a navigable model |

## 7. Refactoring, architecture and legacy analysis tools

- These tools build a model precise enough to change code safely or to explain a legacy estate.
- Most of them refresh by re-running an analysis or a build, so their models are snapshots rather than live indexes.

### 7.1 Moderne and OpenRewrite

- **What it indexes and how.**
  - Moderne builds Lossless Semantic Trees (LSTs), which are type-attributed syntax trees that preserve formatting so that source can be printed back unchanged ([Moderne docs](https://docs.moderne.io/user-documentation/recipes/authoring-recipes/concepts/lossless-semantic-trees)).
  - The LST is produced by driving the compiler, and support is strongest for Java and the JVM, with newer support for JavaScript, TypeScript, Python and C# ([OpenRewrite docs](https://docs.openrewrite.org/concepts-and-explanations/lossless-semantic-trees)).
  - Changes are expressed as deterministic recipes that run across many repositories.
- **Freshness.**
  - In local MCP mode, a background thread builds the LST with the repository's own Gradle or Maven build and stores it under `.moderne/mcp/lst/`, so freshness depends on a successful rebuild ([Moderne MCP security](https://docs.moderne.io/user-documentation/agent-tools/mcp/security)).
- **Agent access.**
  - `mod mcp` is a local MCP server that wraps the Moderne CLI for clients such as Claude Code, Copilot and Windsurf ([Moderne MCP security](https://docs.moderne.io/user-documentation/agent-tools/mcp/security)).
  - Moddy Desktop runs an MCP server with eight tools to search the recipe catalogue, run recipes across many repositories, query recipe data tables and apply changes ([Moddy MCP tools](https://docs.moderne.io/user-documentation/moddy/mcp-tools-reference)).
- **Deployment and data residency.**
  - The local MCP server does not contact the Moderne platform by default and uploads only tool-call telemetry when the CLI is signed in to a tenant ([Moderne MCP security](https://docs.moderne.io/user-documentation/agent-tools/mcp/security)).
- **Pricing and licence.**
  - OpenRewrite is open source, Moderne's platform is commercial, and no list prices were found.
  - Moderne raised a $30M Series B in February 2025 with Morgan Stanley, Amex Ventures and TIAA Ventures participating ([fintech.global, 2025](https://fintech.global/2025/02/12/moderne-raises-30m-series-b-to-accelerate-ai-powered-code-transformation/)).
- **Evidence and customers.**
  - [Vendor claim] Moderne says it serves five leading North American banks, which it does not name ([fintech.global, 2025](https://fintech.global/2025/02/12/moderne-raises-30m-series-b-to-accelerate-ai-powered-code-transformation/)).
  - [Vendor claim] A FINOS blog by Moderne describes a large bank facing an upgrade of more than 15,000 codebases to Java 21, estimated at over 50,000 hours by hand ([FINOS blog](https://www.finos.org/blog/open-source-auto-refactoring-meets-ai-agent-to-modernize-fintech-software-at-scale)).
  - [Vendor claim] An anonymised financial services cooperative reported a "conservative" 74% time saving on security remediation ([Moderne case study](https://moderne.io/blog/case-study-improving-risk-profile-and-devx-with-automated-code-remediation-in-financial-services)).
  - [Secondary] CB Insights lists BNY among Moderne's customers ([CB Insights](https://www.cbinsights.com/company/moderne/customers)).
- **Limitations.**
  - LSTs can only be produced for code that builds, so legacy repositories without a working build are excluded.
  - No COBOL support was found in the sources reviewed.
  - Recipes must exist or be authored for each kind of change, which is engineering work.

### 7.2 AWS Transform

- **What it indexes and how.**
  - Mainframe analysis produces a knowledge graph of components and execution flow, and AWS describes a dependency graph that reflects compiler semantics, cross-program dependencies and middleware behaviour before generative AI is applied ([AWS ML blog](https://aws.amazon.com/blogs/machine-learning/learnings-from-cobol-modernization-in-the-real-world)).
  - The 2026 "reimagine" workflow covers COBOL and PL/I and extracts business rules, data lineage and domain structure into specifications ([AWS news, May 2026](https://aws-news.com/article/2026-05-08-reimagining-mainframe-applications-with-aws-transform-and-claude-code)).
- **Freshness.**
  - The model is produced by an analysis run, so it is a snapshot (inference).
- **Agent access.**
  - AWS pairs Transform for reverse engineering with Claude Code for forward engineering, using CLAUDE.md for project context and Claude Code Skills for repeatable workflows, and the article does not mention MCP ([AWS news, May 2026](https://aws-news.com/article/2026-05-08-reimagining-mainframe-applications-with-aws-transform-and-claude-code)).
  - Transform is also available through Kiro Powers and agent skills for Claude Code, Cursor and Codex, and a first-party MCP server was not confirmed ([AWS Transform launch guide](https://docs.aws.amazon.com/transform/latest/launchguide/aws-transform.md)).
- **Deployment and data residency.**
  - It is an AWS-managed service, and FedRAMP, SOC 2 and on-premises availability were not verified.
- **Pricing and licence.**
  - No list prices were found.
- **Evidence and customers.**
  - [Vendor claim] AWS says Transform processed over 4.5 billion lines in its first year, and it later claimed 10 billion lines ([Info-Tech](https://www.softwarereviews.com/vendor-technology-notes/aws-transform-says-it-s-processed-10-billion-lines-of-legacy-code)).
- **Limitations.**
  - The knowledge graph and specifications live in AWS, which creates a dependency for firms not committed to that cloud.
  - The workflow requires human validation of specifications before code generation, which is a control as well as a cost.
  - Line counts measure throughput rather than functional equivalence or production cut-over.

### 7.3 Google Mainframe Assessment Tool

- **What it indexes and how.**
  - Google describes MAT as reverse-engineering legacy codebases at large scale with Gemini models and mainframe-specific agentic workflows ([Google Cloud](https://cloud.google.com/solutions/mainframe-modernization)).
  - Business rules extracted by MAT feed Mainframe Modernization Agents that produce target specifications, architecture designs, implementation plans and Java or C# code.
- **Freshness.**
  - No refresh mechanism was documented in the sources reviewed.
- **Agent access.**
  - Google documents running Gemini CLI against an AGENTS.md exported from MAT, with a MAT MCP server providing assessment data ([Google Cloud MAT docs](https://docs.cloud.google.com/mainframe-assessment-tool/docs/modernize-validate)).
- **Deployment and data residency.**
  - The tool runs in Google Cloud.
- **Pricing and licence.**
  - No list prices were found.
- **Evidence and customers.**
  - No named financial-services customer or outcome data was found.
- **Limitations.**
  - It ties legacy analysis to Google Cloud, and on-premises availability was not verified.

### 7.4 CAST Imaging

- **What it indexes and how.**
  - CAST's static analysers build a whole-application object and dependency graph, including call graphs, cross-application dependencies and architectural layers ([CAST](https://www.castsoftware.com/news/ai-can-now-understand-and-transform-big-enterprise-codebases)).
- **Freshness.**
  - The model is refreshed when an application is re-analysed, and the MCP server reads results through the Imaging API rather than analysing code itself ([CAST MCP docs](https://doc.castsoftware.com/mcp-server/)).
- **Agent access.**
  - CAST launched an early-access MCP server on 1 August 2025 and later made it available to all Imaging users, and the Express and Cloud editions have their own servers that name Claude Desktop and GitHub Copilot as clients ([CAST, 2025](https://www.castsoftware.com/news/cast-announces-early-access-to-cast-imaging-mcp-server); [CAST Imaging Express FAQ](https://doc.castsoftware.com/imagingexpress/mcp-server/faq/)).
- **Deployment and data residency.**
  - The MCP server is delivered as Docker and can run on corporate servers or in the cloud ([CAST install guide](https://doc.castsoftware.com/install/mcp-server)).
- **Pricing and licence.**
  - No list prices were found.
- **Evidence and customers.**
  - No citable bank or capital markets customer was retrieved, although CAST is widely reported to have them.
- **Limitations.**
  - The documentation describes API-key authentication, so a buyer should confirm whether results are trimmed to each user's entitlements.
  - The model is only as current as the last analysis.

### 7.5 IBM watsonx Code Assistant for Z and ADDI

- **What it indexes and how.**
  - IBM Application Discovery and Delivery Intelligence (ADDI) performs inventory, discovery and dependency analysis, and watsonx Code Assistant for Z, introduced in August 2023, converts COBOL to Java on IBM Z ([IBM newsroom, 2023](https://newsroom.ibm.com/2023-08-22-IBM-Unveils-watsonx-Generative-AI-Capabilities-to-Accelerate-Mainframe-Application-Modernization?_gl=1)).
- **Freshness.**
  - No 2026 source described how ADDI's model is stored or refreshed.
- **Agent access.**
  - No MCP announcement was found.
- **Deployment and data residency.**
  - Current deployment details were not retrieved.
- **Pricing and licence.**
  - IBM publishes a pricing page, but the retrieved content had no prices ([IBM](https://www.ibm.com/products/watsonx-code-assistant-z/pricing)).
- **Evidence and customers.**
  - [Vendor claim] IBM cites a 94% reduction in time to analyse superfluous COBOL code without naming a client or date ([IBM](https://www.ibm.com/products/watsonx-code-assistant-z/pricing)).
- **Limitations.**
  - The most recent primary sources found date from 2023, and no agent-facing interface was found.

### 7.6 Rocket Enterprise Analyzer

- **What it indexes and how.**
  - Enterprise Analyzer helps engineers understand application logic and dependencies and provides "what if" impact analysis, with integrations for Visual Studio, Eclipse and VS Code ([Rocket](https://www.rocketsoftware.com/en-us/insights/future-ai-application-modernization)).
- **Freshness.**
  - No refresh mechanism was documented.
- **Agent access.**
  - No MCP announcement was found.
- **Deployment and data residency.**
  - Details were not retrieved.
- **Pricing and licence.**
  - Only a third-party licensing site was found, which is less reliable than vendor material ([mainframelicensingexperts, secondary](https://mainframelicensingexperts.pages.dev/products/rocket-software/rocket-enterprise-analyzer/)).
- **Evidence and customers.**
  - No outcome data was found.
- **Limitations.**
  - The product has passed from Micro Focus to OpenText to Rocket, with Rocket completing integration in May 2024, so roadmap continuity should be checked ([Futurum, 2024](https://futurumgroup.com/insights/rocket-acquires-opentext-amc-a-new-era-in-mainframe-modernization)).

### 7.7 vFunction

- **What it indexes and how.**
  - vFunction analyses architecture with static and dynamic analysis in test, staging or production ([Business Wire, April 2025](https://www.businesswire.com/news/home/20250429830762/en/vFunction-Unveils-New-Advancements-to-Simplify-Complex-Applications-Closing-Gap-Between-AI-Accelerated-Development-and-Architectural-Integrity)).
- **Freshness.**
  - Since April 2025 it uses OpenTelemetry data for continuously updated architecture documentation and drift detection, which makes it the main exception to snapshot-based models.
- **Agent access.**
  - No MCP server was found ([vFunction, 2025](https://vfunction.com/news/vfunction-unveils-new-advancements-to-simplify-complex-applications/)).
- **Deployment and data residency.**
  - On-premises availability was not verified.
- **Pricing and licence.**
  - No list prices were found.
- **Evidence and customers.**
  - No named financial-services customer was found.
- **Limitations.**
  - It models services and architecture rather than code-level symbols, so it complements rather than replaces code navigation.

### 7.8 Microsoft Legacy Modernization Agents

- **What it indexes and how.**
  - This open-source project, originally called the COBOL Agentic Migration Factory, orchestrates persona-based agents with Semantic Kernel to convert COBOL to Java Quarkus or C# .NET ([Microsoft DevBlogs, July 2025](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/)).
- **Freshness.**
  - It processes code per run rather than maintaining an index.
- **Agent access.**
  - It is itself an agent framework, and Microsoft's broader offering is GitHub Copilot app modernization agents ([Azure blog](https://azure.microsoft.com/en-us/blog/many-agents-one-team-scaling-modernization-on-azure/)).
- **Deployment and data residency.**
  - Because it is open source, a bank can run it inside its own Azure tenant with its own model deployments ([GitHub](https://github.com/Azure-Samples/Legacy-Modernization-Agents)).
- **Pricing and licence.**
  - The code is open source, and model consumption is billed separately.
- **Evidence and customers.**
  - [Vendor claim] Bankdata, owned by Danish banks representing over 30% of that market, co-developed the framework but initially provided only a small COBOL module for testing (July 2025).
  - [Secondary] A conference page says the target is Bankdata's 17 million lines of COBOL, and no production use was confirmed ([WeAreDevelopers](https://platform-v2.wearedevelopers.com/videos/1531/migrating-from-cobol-with-ai-a-moonshot-demo)).
- **Limitations.**
  - It is a sample framework rather than a supported product, and it lacks the estate-wide dependency analysis of CAST or ADDI.

### 7.9 Sonar and developer portals

- These tools do not navigate code symbols, but they give agents quality gates, ownership and service dependencies that complement code intelligence.

| Tool | What it indexes and how | Freshness | Agent access | Deployment and residency | Licence | Evidence | Limitations |
|---|---|---|---|---|---|---|---|
| SonarQube | Static analysis issues and quality gates | Per analysis | Free local MCP server, an embedded server in SonarQube Cloud, and native MCP in Server 2026.3 ([Sonar](https://www.sonarsource.com/products/sonarqube/mcp-server/); [Sonar 2026.3](https://www.sonarsource.com/jp/blog/announcing-sonarqube-server-2026-3/)) | Local Docker, Server or Cloud | Commercial editions, free MCP | [Independent] UK Defra uses it for "AI Code Assurance", with the agent checking quality gates before committing ([Defra](https://defra.github.io/ai-sdlc-tool-guidance/tool-guidance/mcps/sonarqube-mcp-detailed)) | Defra flags that prompt content, which can include code, flows to the backend SonarQube instance |
| Backstage | Services, ownership and dependencies as catalogue entities | Catalogue sync | MCP Actions backend at `/api/mcp-actions/v1` ([Backstage docs](https://backstage.io/docs/ai/mcp-actions)); Red Hat Developer Hub adds catalogue and TechDocs tools (November 2025) | Self-hosted | Apache 2.0 | None specific | Service-level, not code-level |
| Port and OpsLevel | Catalogue metadata, health and runbooks | Catalogue sync | MCP servers launched in June 2025 ([Port](https://www.port.io/blog/integrate-software-catalog-every-workflow-port-mcp-server/); [OpsLevel](https://www.opslevel.com/resources/demo-the-opslevel-mcp)) | SaaS | Commercial | None specific | Service-level, not code-level |

## 8. What the evidence shows about retrieval methods

### 8.1 Independent studies

- [Independent] ContextBench (February 2026) has 1,136 issue-resolution tasks from 66 repositories in eight languages and measures the precision and recall of the context that agents retrieve ([arXiv 2602.05892](https://arxiv.org/html/2602.05892)).
  - With GPT-5, the bash-only mini-SWE-agent had the highest file-level F1 (0.634), while the graph-based Prometheus had the highest task success (Pass@1 0.512) but low file-level precision (0.336).
  - The embedding-based Agentless had the lowest file-level recall (0.609) but the highest line-level F1 (0.376).
  - Holding the agent fixed, changing the model moved Pass@1 from 0.364 to 0.530, which shows that model choice matters as much as retrieval architecture at this repository scale.
  - The authors found that agents often inspect relevant code without using it and favour recall over precision.
- [Independent] "Is Grep All You Need?" (May 2026) found that grep beat vector retrieval for every harness and model pair with inline delivery, but the result depended on the harness, and the corpus was conversational memory rather than code ([arXiv 2605.15184](https://arxiv.org/html/2605.15184v1)).
- [Independent] A benchmark of 252 headless Claude Code runs found that a graph server did not make Claude Code cheaper on repositories up to 25,000 nodes, and with Sonnet, Read and Grep were cheaper on 11 of 12 questions at equal accuracy ([nefayran/code-graph-vs-grep](https://github.com/nefayran/code-graph-vs-grep)).
  - In the same benchmark, Haiku answered structural questions correctly 12 of 12 times with the graph versus 8 of 12 with Read and Grep.
  - On Kubernetes and VS Code, the graph-to-grep token ratio for structural questions was 0.29 for Haiku, 0.74 for Sonnet and 0.97 for Opus, so the benefit shrank as the model became stronger.
  - Loading graph tool definitions without a routing rule cost 62,000 tokens per session against 30,000 with one, which is a recurring cost that many buyers overlook.
- [Independent] RepoGraph (ICLR 2025) raised SWE-bench Lite resolve rates by an average relative 32.8% across four frameworks, mainly through better file localisation ([arXiv 2410.14684, 2024](https://arxiv.org/abs/2410.14684)), and LocAgent (ACL 2025) reached up to 92.7% file-level localisation with graph tools ([arXiv 2503.09089, 2025](https://arxiv.org/html/2503.09089)).
  - Both were measured on weaker scaffolds and models than current agents, so their gains may not carry over to frontier models.
- [Independent] A 2026 paper on reliable coding agents argues that bounded graph operations such as "find definitions" and "list callers" are easier to validate than free-form generated graph queries ([arXiv 2608.13867](https://arxiv.org/pdf/2608.13867)).
- [Practitioner] The author of a symbol-graph MCP server found that tuned grep beat his own server by 9 F1 points overall across 60 tasks, while the graph still won on imports and symbol relationships ([DEV Community](https://dev.to/nike-17/i-benchmarked-code-retrieval-for-ai-coding-agents-on-60-tasks-f9h)).
- The pattern across these studies is consistent.
  - Structure helps localisation and impact questions, especially for weaker models.
  - Frontier models compensate with more grep turns, so the advantage of indexes is smaller than vendors suggest on small and medium repositories.
  - All public benchmarks use repositories far smaller than a multi-million-line estate, which is exactly where indexes should help most, so the main evidential gap sits where large organisations operate.

### 8.2 Vendor-reported results

- None of the following figures has been independently replicated, and each uses the vendor's chosen repositories and graders.

| Vendor | Claim | Measurement |
|---|---|---|
| Augment | 71%, 80% and 30% better agent output with the Context Engine | 300 Elasticsearch pull requests with three prompts each, no variance published |
| Bito | 70.1% versus 51.9% task success | Claude Opus 4.6, task set not public |
| Tabnine and Tricentis | Up to 2 times accuracy, 80% fewer tokens, 50% faster tasks | Not described |
| GitLab Orbit | Up to 11 times faster answers and 4.5 times fewer tokens | Internal testing |
| Unblocked | 42% fewer tokens and 64% fewer tool calls | Against raw context dumping |
| Cognition | SWE-grep about 10 times faster than standard agentic search | Not described |
| Cursor | 12.5% more questions answered correctly with semantic search | Reported secondhand |
| claude-context | About 40% token reduction | Reproduced at 39.4% by a third party on an older release |
| Moderne | A Java upgrade in about three minutes with roughly 30,000 tokens | Conference talk, 2026 ([Moderne](https://hosted-files.sched.co/osfftoronto2026/d4/Moderne%20-%20DevTools%20or%20Agent%20Tools.pdf)) |

- ContextBench's finding that scaffolding adds little retrieval gain is in tension with vendor claims of 30% to 80% improvement, although the two measure different things (retrieval precision versus end-task quality).

### 8.3 Analyst coverage

- [Independent] Gartner renamed its category from "AI Code Assistants" to "Enterprise AI Coding Agents" in May 2026 ([Virtualization Review](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)).
  - The 2026 Leaders are Anthropic, Cursor, GitHub and OpenAI, the Challengers are AWS, Google, Alibaba Cloud and Cognition, Tabnine is the only Visionary, and the Niche Players are Atlassian, BytePlus and JetBrains.
  - GitLab, which was a Leader in 2025, was not placed ([GitLab press release, 2025](https://about.gitlab.com/press/releases/2025-09-17-gitlab-named-a-leader-in-gartner-magic-quadrant-ai-code-assistants/)).
  - Gartner reportedly made native MCP support, human approval of changes, auditability and enterprise data protection mandatory features.
- Pure code intelligence vendors such as Sourcegraph, Augment, Qodo, Greptile and Moderne do not appear in the Magic Quadrant, so analyst rankings say little about retrieval quality.
- No Forrester Wave or IDC MarketScape specific to code intelligence was found for 2025 or 2026.

## 9. Side-by-side comparison

### 9.1 Enterprise search platforms and context engines

| Product | Index model | Freshness | Precise cross-repo references for agents | MCP | Self-hosted or air-gapped | Pricing model | Main limitation |
|---|---|---|---|---|---|---|---|
| Sourcegraph | Zoekt trigram plus SCIP | SCIP per CI upload | Yes | Yes, with per-tool controls | Self-hosted; air-gap unconfirmed | From $16K a year plus AI credits | Closed source and product churn |
| GitHub Copilot | Blackbird plus per-repository embeddings | Seconds | No | Yes, remote server not on GHES | No for semantic indexing | Per seat plus AI credits | GHES gap |
| GitLab Orbit | Graph of code and SDLC data | Seconds to minutes | Definitions, imports and calls, default branch only | Yes | Yes, Self-Managed | Bundled in Premium and Ultimate | New and default-branch only |
| Atlassian Rovo | Lexical plus embeddings | Incremental; 24 to 48 hours initially | No | Yes, cloud only | No; US storage | Rovo credits | US residency and beta |
| Gemini code customization | Embeddings | 24 hours | No | Not confirmed | No; Google Cloud | Enterprise edition | Staleness and repository cap |
| Sourcebot | Zoekt | Operator-defined | No | Yes, Enterprise only | Yes, with offline licence | $20 to $25 per seat, FSL | Text search only in sources |
| Augment | Semantic with relationships | Not published | Not documented | Yes, local and remote | Remote is SaaS | Credits | Residency and cost predictability |
| Cursor | Embeddings plus lexical | About 10 minutes | No | Not for its index | No | Usage-based | Tied to the editor |
| Qodo | RAG index | Not published | Not documented | Yes, through Qodo Aware | Yes, but needs frontier models | Not published | Model dependency |
| Tabnine | Knowledge graph | Continuous, unquantified | Not documented | Unknown after acquisition | Yes | $39 to $59 per user (pre-acquisition) | Roadmap risk |
| Bito | Knowledge graph plus tickets | Not published | Not documented | Yes | Not documented | Not published | Unverified certifications |

### 9.2 Open-source agent tools

| Tool | Paradigm | Precision | Scope | Licence | Maintenance signal | Main limitation |
|---|---|---|---|---|---|---|
| Serena | Live LSP | Compiler-grade where the language server is good | One workspace | GPL-3.0 (application) and MIT (SolidLSP) | About 31,300 stars; v2 in October 2026 | External dependencies and advanced refactors need the paid plugin |
| mcp-language-server | Live LSP | Compiler-grade | One workspace | Open source | Not verified for 2026 | Fewer tools than Serena |
| GitNexus | Tree-sitter graph | Heuristic | One repository | Open source | Active in 2026 | Built on archived Kuzu |
| codebase-memory-mcp | Tree-sitter graph | Heuristic | One repository | Open source | Preprint March 2026 | Lower answer quality than file reading |
| CodeGraphContext | Tree-sitter graph, optional SCIP | Heuristic, or precise with SCIP | One repository or more | Open source | Active | Incremental drift |
| claude-context | Embeddings plus BM25 | Semantic | One codebase | MIT | About 10,900 stars | Needs an embedding model and vector store |
| ast-grep and Probe | Structural search, no index | Syntactic | One working copy | MIT and open source | Active | No types |
| Zoekt plus SCIP plus Glean | Estate-wide build-your-own | Compiler-grade | Whole estate | Apache 2.0 and open source | Active | Platform-team effort and no MCP server |

### 9.3 Refactoring and legacy tools

| Tool | Model | COBOL and PL/I | MCP or agent interface | Runs on-premises | Freshness | Main limitation |
|---|---|---|---|---|---|---|
| Moderne | Lossless Semantic Trees | No evidence found | Yes, local `mod mcp` and Moddy | Yes | Rebuild per change | Needs a working build |
| AWS Transform | Mainframe knowledge graph | Yes | Skills, CLAUDE.md and Kiro Powers; MCP unconfirmed | No | Snapshot | AWS dependency |
| Google MAT | Gemini-based reverse engineering | Yes | MAT MCP server and AGENTS.md | No | Not documented | Google Cloud dependency |
| CAST Imaging | Whole-application dependency graph | Widely reported, not verified here | Yes, Docker MCP | Yes | Re-analysis | API-key authentication |
| IBM ADDI and WCA for Z | Inventory and dependency analysis | Yes | None found | Not verified | Not documented | No agent interface found |
| Rocket Enterprise Analyzer | Logic and dependency analysis | Yes | None found | Not verified | Not documented | Ownership changes |
| vFunction | Architecture from static and runtime analysis | No | None found | Not verified | Continuous through OpenTelemetry | Service-level only |
| Microsoft Legacy Modernization Agents | Agent pipeline | Yes | Is an agent framework | In the firm's Azure tenant | Per run | Sample code, not a product |

### 9.4 Deployment options for regulated firms

| Requirement | Products that fit | Products that do not fit |
|---|---|---|
| Code must not leave the firm's data centre | Sourcegraph self-hosted, GitLab Self-Managed with Orbit and Zoekt, Sourcebot Enterprise, Tabnine on-premises, Qodo on-premises, Moderne CLI, CAST Imaging, SonarQube Server, Serena and other local tools | GitHub Copilot semantic indexing, Atlassian code context, Gemini code customization, Augment remote, Cursor, AWS Transform, Google MAT |
| Fully air-gapped with no external model | Open-source stacks with a locally hosted model, Sourcebot with an offline licence, Tabnine air-gapped (with contract protections) | Qodo, whose Context Engine requires gpt-5 and claude-4.1-opus; Sourcegraph until air-gap support is confirmed |
| EU or UK residency in a vendor cloud | To be confirmed with each vendor, because no regional options were confirmed in this research | Atlassian code context, which stores data in the United States |
| Repositories on GitHub Enterprise Server | Sourcegraph, Sourcebot, Qodo, the local GitHub MCP server | Copilot semantic indexing and the remote GitHub MCP server |

## 10. Pricing, licensing and vendor stability

- Pricing moved from flat seats to seats plus metered usage during 2025 and 2026.
  - GitHub moved to token-priced AI Credits in June 2026, Augment moved to credit pools in October 2025, Cursor moved to usage pricing in June 2025, and Greptile moved to per-review credits in March 2026.
  - Sourcegraph's Deep Search, Sourcegraph's `code_finder` and Atlassian's Rovo MCP code search are also metered.
  - For a bank with thousands of developers, metered credits make total cost depend on agent behaviour, so per-user caps and budget alerts become procurement requirements.
- Code search and modernisation platforms remain sales-led, and no per-repository or per-line pricing is public for any vendor found.
- Licences have tightened in several places, which affects any firm that wants to embed or redistribute a tool.
  - Sourcegraph's core is proprietary since 2023, Sourcebot uses the Functional Source License, Serena v2 is GPL-3.0, and Semgrep moved features out of its open-source edition in late 2024 and early 2025.
  - Zoekt (Apache 2.0), OpenGrok (CDDL 1.0), Glean, Kythe, OpenRewrite, ast-grep (MIT), Codanna (Apache 2.0) and claude-context (MIT) remain permissively or openly licensed.
- Ownership and direction changed often between 2025 and 2026, so roadmap continuity is a selection criterion.

| Date | Event | Relevance to buyers |
|---|---|---|
| July 2025 | Google hired Windsurf's CEO in a reported $2.4B licensing deal, and Cognition acquired the rest of Windsurf ([CNBC, 2025](https://www.cnbc.com/2025/07/14/cognition-to-buy-ai-startup-windsurf-days-after-google-poached-ceo.html)) | A standalone product was absorbed into another vendor's agent |
| July 2025 | Sourcegraph ended Cody Free, Pro and Enterprise Starter | Self-serve users had to move to Amp |
| December 2025 | Amp was spun out of Sourcegraph as a separate company | Sourcegraph and its agent product now have separate roadmaps |
| March 2026 | Qodo raised a $70M Series B | Funding supports continued investment |
| April 2026 | Factory raised a reported $150M Series C | Funding supports continued investment |
| June 2026 | Windsurf was reportedly renamed Devin Desktop, with the old version reaching end of life on 1 July 2026 | Product names and contracts can change within a year |
| 30 July 2026 | Tricentis acquired Tabnine, promising support but no roadmap | Air-gapped customers face roadmap risk |
| August 2026 | CodeRabbit raised $143M and said proceeds may fund acquisitions ([Axios Pro](https://www.axios.com/pro/enterprise-software-deals/2026/08/12/coderabbit-raise-acquisitions-ai-code-review)) | Further consolidation is likely |
| October 2026 | Greptile raised $50M at a $750M valuation | Funding supports continued investment |

- These events matter directly to EU firms, because DORA requires exit strategies and concentration-risk analysis for ICT third-party providers (see section 11).

## 11. Security and regulatory considerations

- The main risk in 2025 and 2026 came from agents and their MCP connectors rather than from leaks of a vendor's hosted index.
  - [Independent] Cursor CVE-2025-54136 allowed an approved MCP configuration in a shared repository to be changed later to run malicious commands, and CVE-2025-54135 allowed prompt injection through a Slack MCP server to achieve code execution, both fixed in July 2025 ([Tenable](https://www.tenable.com/cve/CVE-2025-54136); [SecurityWeek, 2025](https://www.securityweek.com/several-vulnerabilities-patched-in-ai-code-editor-cursor/)).
  - [Independent] A Cloud Security Alliance note of 29 June 2026 lists repository-controlled MCP auto-execution issues across assistants, including Claude Code and Amazon Q Developer, all reported as patched ([CSA research note](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/06/CSA_research_note_mcp_ai_coding_assistant_credential_theft_20260629-csa-styled.pdf)).
  - [Independent] The May 2025 GitHub MCP private-repository leak is an architectural pattern in which any agent that can read untrusted text and write to a public location can be steered into leaking data ([Tessl, 2025](https://tessl.io/blog/malicious-github-issue-ai-agent-leak/)).
  - No public incident was found in which a vendor's hosted code index itself leaked customer code.
- The permission model across vendors is "authenticate as the user, then apply repository permissions".
  - Sourcegraph, GitLab Orbit, Atlassian, Glean and GitHub all state that agent results are filtered by the user's existing access.
  - This means agent access is only as safe as the underlying repository permissions, and none of the sources describe agent scopes narrower than the user's own access, apart from Sourcegraph's per-tool disable list and GitHub's MCP allowlists.
  - Practical controls are MCP allowlists, read-only tokens scoped per repository, disabling automatic loading of workspace MCP configurations, and separating agents that read untrusted content from agents that can push code.
- Certification claims are mostly vendor-asserted.
  - Augment's SOC 2 Type II and ISO/IEC 42001 claims are documented, with the ISO certificate issued by Coalfire, while certifications for Bito, Greptile, Unblocked, Zencoder and Qodo were not verified.
- Regulators treat these tools under existing third-party and ICT risk frameworks, and the sources on this point are secondary and partly conflicting.
  - [Secondary] Commentary treats AI coding vendors as ICT third-party service providers under the EU's DORA, BaFin's non-binding January 2026 guidance places generative AI inside existing DORA governance, and an ESA statement of 31 July 2026 reportedly asks firms to inventory AI components ([bankingnewsai](https://www.bankingnewsai.com/ai-regulation/guides/dora-explained); [airiskaware](https://airiskaware.com/insights/eu-banks-ai-governance-eba)).
  - [Secondary, conflicting] One summary states that the 2026 US interagency model-risk guidance carves generative and agentic AI out of scope, while a vendor blog claims SR 11-7 was clarified to cover AI-generated code, and NYDFS reportedly asked for human review of AI-generated code in May 2026 ([bankingnewsai](https://www.bankingnewsai.com/agentic-banking/regulation); [IAN blog](https://iancloud.ai/blog/ai-code-remediation-financial-services-compliance-2026)).
  - The primary regulatory texts should be checked before relying on any of these statements.
  - In practice, a bank's procurement path for code intelligence runs through third-party risk management, with the DORA register of information in the EU, rather than model-risk validation.
- Bank adoption evidence shows that specialist context tools are usually added to an approved assistant rather than bought as the primary tool.
  - [Independent] JPMorgan built its own coding assistant and reported 10% to 20% productivity gains (Reuters, March 2025) ([Yahoo Finance](https://finance.yahoo.com/news/jpmorgan-engineers-efficiency-jumps-much-190410471.html)).
  - [Independent] Morgan Stanley's in-house DevGen.AI reviewed nine million lines of legacy code in five months and saved about 280,000 hours by the bank's own account (June 2025) ([Business Insider, 2025](https://www.businessinsider.nl/a-team-of-engineers-saved-morgan-stanley-more-than-280000-hours-this-year-the-bank-says-their-tool-wont-take-jobs/)), and a later article puts the total at more than 17 million lines of COBOL, Natural and Perl ([CIO Dive](https://www.ciodive.com/news/ai-shifts-mainframe-modernization-strategy/825677/)).
  - These figures measure throughput rather than defect rates or functional equivalence.

## 12. Worked capital markets scenarios

- Each scenario names the question an agent must answer, the tools that fit, and a tool that would be a poor fit, with the reason.

### 12.1 Post-trade settlement platform

- A bank runs a post-trade settlement platform as about 400 Java and Kotlin microservices that exchange ISO 20022 and SWIFT messages, and an agent is asked which services break if a shared settlement-instruction enrichment library changes its method signature.
  - The agent needs a complete, compiler-accurate list of callers across repositories, because a missed caller becomes a failed settlement in production.
  - A good fit is Sourcegraph with SCIP indexes produced in CI, because its `find_references` MCP tool returns cross-repository references from a compiler-grade index.
  - If the estate is on GitLab Self-Managed, GitLab Orbit is a reasonable alternative for "what depends on this" questions, and it adds pipeline and deployment links, but its call edges are not compiler-resolved and it covers only the default branch.
  - Moderne is the right tool for making the change itself, because an OpenRewrite recipe can update every caller deterministically.
  - A poor fit is an embedding-only context engine, because semantic similarity can return the most relevant callers but cannot prove that it found all of them.

### 12.2 Mandate rules engine

- An asset manager's mandate rules engine encodes client investment restrictions in Java, a rules DSL and SQL reference tables, and an agent is asked why a particular restriction blocks emerging-market bonds for one client and who approved the change.
  - The agent needs code, the ticket and pull request history behind the rule, and the SQL reference data, which is a "why" question as much as a "where" question.
  - A good fit is a context engine that ingests tickets and documents alongside code, such as GitLab Orbit for work items and pipelines, or Unblocked, Bito or Tabnine for tickets and documents, combined with exact search for the rule identifier.
  - The agent should still treat the compliance system as the source of truth for the restriction, because an index of code and tickets is not an approved compliance record (see [context-layer-databases.md](context-layer-databases.md)).
  - A poor fit is a tree-sitter code graph, because the decisive logic lives in a DSL and SQL tables that these tools do not parse, and none of the reviewed open-source tools extracts stored-procedure call graphs.

### 12.3 COBOL general ledger on the mainframe

- A bank's general ledger runs as COBOL programs on z/OS with copybooks, JCL batch jobs and DB2 tables, and an agent is asked which batch jobs write to the end-of-day ledger balance table and which business rules apply.
  - The agent needs a cross-program dependency graph that includes JCL steps, copybook includes and DB2 table access, which is what mainframe analysers build.
  - A good fit for a firm that must stay on-premises is CAST Imaging with its Docker MCP server, or IBM ADDI and Rocket Enterprise Analyzer, although no MCP interface was found for the last two.
  - A good fit for a firm that accepts hyperscaler processing is AWS Transform or Google MAT, both of which extract business rules and data lineage into specifications for a coding agent.
  - Large banks have also built their own tools, as Morgan Stanley did with DevGen.AI, which shows that packaged tools did not fully meet their needs at the time.
  - A poor fit is an open-source code graph or CodeQL, because none of the reviewed open-source agent tools handles COBOL with semantic precision and CodeQL and Joern have no COBOL frontend.
  - Text search over COBOL in Sourcegraph or Zoekt remains useful for finding a field name, but it does not provide program-to-table lineage.

### 12.4 Regulated firm that requires on-premises or air-gapped deployment

- A broker-dealer's security policy forbids source code from leaving its data centres, and some trading systems sit on an air-gapped network.
  - For estate-wide search, the options are Sourcegraph self-hosted (with air-gap support confirmed in writing), GitLab Self-Managed with Orbit and Zoekt, or Sourcebot Enterprise with an offline licence.
  - For local agent tools, Serena, mcp-language-server, ast-grep and claude-context with a self-hosted Milvus instance and a locally hosted embedding model can run entirely inside the network.
  - For change at scale, the Moderne CLI and `mod mcp` run locally and do not contact the Moderne platform by default.
  - For quality gates, SonarQube Server runs on-premises, although Defra's note that prompt content flows to the SonarQube backend still applies inside the network.
  - The coding agent that consumes these MCP servers must also use an approved model endpoint, because an on-premises index does not help if the agent sends retrieved code to an external model.
  - A poor fit is Qodo's on-premises Context Engine, because it requires access to gpt-5 and claude-4.1-opus, and also any cloud-indexed product such as Copilot semantic indexing, Atlassian code context or Gemini code customization.
  - Tabnine's air-gapped product fits technically, but the contract should include end-of-life notice, source escrow and a defined exit plan because of its July 2026 acquisition.

### 12.5 Java upgrade across thousands of repositories

- A large bank must move more than 15,000 codebases off Java 8 and older application servers to Java 21, which the FINOS case estimated at over 50,000 hours by hand.
  - The work needs the same mechanical change applied consistently, with formatting preserved, so that reviewers can trust the diffs.
  - A good fit is Moderne with OpenRewrite recipes, invoked by a coding agent through MCP for the cases that recipes do not cover.
  - Sourcegraph Batch Changes is a complementary option for tracking and opening changes across many repositories.
  - A poor fit is a general coding agent editing each repository from scratch, because results vary from repository to repository and the token cost scales with the number of repositories.

### 12.6 Fast-moving pricing library in C++ and Python

- A front-office quant team maintains a derivatives pricing library in C++ with Python bindings that changes many times a day, and an agent is asked to find every place that uses a day-count convention before a change.
  - The agent needs an index that reflects commits from the last hour, because yesterday's index can miss the callers that matter.
  - If the code is on GitHub.com, Copilot's semantic index refreshes within seconds and GitHub added whole-codebase C++ indexing to Copilot CLI in September 2026.
  - If the code must stay local, an LSP-based tool such as Serena or mcp-language-server over clangd and pyright gives live, compiler-grade references within the checked-out workspace.
  - A poor fit is Gemini code customization, whose 24-hour refresh can return results that predate the morning's changes.

## 13. How a large organisation should choose

### 13.1 Decide by constraint before comparing features

- The following questions remove most options quickly, and they should be answered before any feature comparison.
  - **Where must code and indexes live?** If code cannot leave the data centre, the cloud-indexed products in section 9.4 are excluded.
  - **Which code host is used?** GitHub.com favours Copilot indexing, GHES pushes toward Sourcegraph or Sourcebot, GitLab Self-Managed makes Orbit and Zoekt the natural first choice, and Bitbucket Data Center points toward Sourcegraph or Qodo.
  - **Which languages dominate?** JVM, Go, TypeScript and C# estates can use SCIP and OpenRewrite, while COBOL, JCL and stored-procedure SQL need a mainframe analyser or custom extraction.
  - **What is the main job?** Finding code favours lexical search, impact analysis favours precise references, explaining intent favours ticket-aware context engines, and large mechanical change favours deterministic recipes.
  - **Which model endpoints are approved?** An on-premises index paired with an unapproved external model does not meet a residency requirement.
  - **How stable is the vendor?** Acquisitions in 2025 and 2026 show that a product can be repurposed within a year.

### 13.2 A layered architecture rather than a single product

- A large estate is best served by a small number of layers, each chosen for one job.
  - **Layer 1, estate-wide lexical search.** A Zoekt-based index (Sourcegraph, GitLab exact code search or Sourcebot) gives every agent and developer exact search across all repositories, which is the most reliable way to find identifiers and the base that other layers build on.
  - **Layer 2, precise symbols for compiled languages.** SCIP indexes produced in CI and served through Sourcegraph, or a self-built Zoekt, SCIP and Glean stack, provide compiler-accurate references for impact analysis, and local LSP tools such as Serena provide the same precision inside a working copy.
  - **Layer 3, optional semantic or ticket-aware context.** A context engine should be added only if a bake-off shows that it improves results on the organisation's own tasks, because independent evidence for this layer is weakest.
  - **Layer 4, deterministic transformation.** Moderne and OpenRewrite handle large mechanical changes on buildable JVM code, and agents should call recipes rather than edit thousands of files freehand.
  - **Layer 5, legacy analysis.** CAST, IBM ADDI, Rocket, AWS Transform or Google MAT provide COBOL and JCL dependency graphs, and their output should be exported into the same agent context through MCP or AGENTS.md files.
  - **Cross-cutting governance.** MCP allowlists, read-only scoped tokens, usage caps and audit logs apply to every layer.
- The main cost of the precise layers is not the database but making every repository build reproducibly in an indexing environment, which on a large estate is a platform-team effort measured in engineer-months (an estimate, since no published figures were found).
- Tool-definition overhead also matters, because loading many MCP tools can cost 30,000 to 62,000 tokens per session, so curated endpoints such as Sourcegraph's default `/.api/mcp` and routing rules should be preferred.

### 13.3 Run a bake-off on your own code

- Because no independent benchmark covers enterprise-scale estates, the organisation should build its own task set and measure candidates on it.
  - The task set should contain 50 to 100 real questions drawn from the estate, such as "list every caller of the settlement-instruction enrichment method", "which batch jobs write the ledger balance table" and "why does this mandate rule exclude this asset class".
  - Each task should have a human-annotated answer, so that file-level recall and precision can be measured in the way ContextBench measures them.
  - Each candidate should be tested with the same agent and model, and with at least one weaker and one stronger model, because the benefit of indexes changes with model strength.
  - The measurements should include answer correctness, recall of the complete answer set, tokens, tool calls, wall-clock time and metered credit cost.
  - Index-free agentic search should be included as the baseline, because a product that does not beat it on the organisation's own code is not worth its operating cost.

### 13.4 Contract and governance checklist

- The contract should state where code, embeddings and indexes are stored, how long they are retained, and how they are deleted at exit.
- The contract should include end-of-life notice, source or data escrow and a defined exit plan, which also supports DORA exit-strategy requirements in the EU.
- Metered usage should have per-user caps, budget alerts and reporting, because agent loops can call context tools many times per task.
- The vendor should provide named financial-services references, because Sourcegraph's and Moderne's bank customer claims are unnamed.
- The vendor should confirm in writing whether air-gapped deployment is supported and which external model endpoints are required.
- MCP servers should be allowlisted centrally, tokens should be read-only and scoped where possible, and workspace-level MCP configurations should not auto-load.
- Agent results should be filtered by repository permissions, and the firm should review whether its repository permissions are tight enough to be the only control.

## 14. Conclusion

- The market in November 2026 sells mostly retrieval, while the hard problems for a large bank are completeness, freshness and legacy coverage.
  - Completeness requires compiler-accurate references, which only Sourcegraph exposes to agents as a cross-repository product, and which otherwise require a self-built SCIP or Glean pipeline.
  - Freshness is solved well inside a single repository by GitHub and by local LSP tools, but is slower or undocumented for most estate-wide products.
  - Legacy coverage remains with mainframe specialists and hyperscalers, and the largest banks have still chosen to build their own tooling.
- MCP has made context engines interchangeable at the protocol level, which shifts negotiating power toward buyers.
  - A firm can keep its approved coding agent and swap the context layer behind it, so it should avoid contracts that tie the index to one IDE or one agent.
  - The same interchangeability means that vendor claims can be tested cheaply on the firm's own code, and the absence of independent enterprise-scale evidence makes that test necessary rather than optional.

## Resources

- [Sourcegraph MCP server documentation](https://7.5.sourcegraph.com/api/mcp) — the most detailed public list of code intelligence tools exposed to agents.
- [A new era for Sourcegraph](https://sourcegraph.com/blog/a-new-era-for-sourcegraph-the-intelligence-layer-for-ai-coding-agents-and-developers) — Sourcegraph 7.0 announcement, February 2026.
- [Announcing SCIP](https://sourcegraph.com/blog/announcing-scip) — Sourcegraph, 2022, the design of the main precise index format.
- [GitHub Copilot repository indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing) — GitHub Docs, including the limits on GHE.com and GHES.
- [Introducing GitLab Orbit](https://about.gitlab.com/blog/introducing-gitlab-orbit/) — GitLab, June 2026, with the [Orbit indexing documentation](https://docs.gitlab.com/orbit/remote/indexing/).
- [What is code context?](https://support.atlassian.com/rovo/docs/what-is-code-context/) — Atlassian support, including the United States storage statement.
- [Gemini Code Assist code customization](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization-overview?hl=en) — Google Cloud documentation.
- [Indexing code at scale with Glean](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/) — Meta Engineering, December 2024.
- [Augment Context Engine MCP](https://www.augmentcode.com/blog/context-engine-mcp-now-live) — Augment, February 2026, including its vendor benchmark.
- [Secure codebase indexing](https://cursor.com/blog/secure-codebase-indexing) — Cursor's description of Merkle-tree indexing.
- [Tricentis acquires Tabnine](https://www.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise) — Business Wire, July 2026, with [roadmap risk analysis](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk).
- [oraios/serena](https://github.com/oraios/serena) — the most widely adopted LSP-based MCP server.
- [ContextBench](https://arxiv.org/html/2602.05892) — the largest independent benchmark of context retrieval by coding agents, February 2026.
- [code-graph-vs-grep](https://github.com/nefayran/code-graph-vs-grep) — an independent benchmark of graph tools against Read and Grep in Claude Code, 2026.
- [Codebase-Memory preprint](https://arxiv.org/abs/2603.27277) — March 2026 evaluation of a tree-sitter graph MCP server across 31 repositories.
- [RepoGraph](https://arxiv.org/abs/2410.14684) and [LocAgent](https://arxiv.org/html/2503.09089) — 2024 and 2025 papers on graph-based localisation for SWE-bench.
- [Moderne MCP security and architecture](https://docs.moderne.io/user-documentation/agent-tools/mcp/security) — how the local MCP server builds and stores LSTs.
- [Open-source auto-refactoring meets AI agents](https://www.finos.org/blog/open-source-auto-refactoring-meets-ai-agent-to-modernize-fintech-software-at-scale) — FINOS blog by Moderne on bank-scale Java upgrades.
- [Learnings from COBOL modernization in the real world](https://aws.amazon.com/blogs/machine-learning/learnings-from-cobol-modernization-in-the-real-world) — AWS, and [AWS Transform with Claude Code](https://aws-news.com/article/2026-05-08-reimagining-mainframe-applications-with-aws-transform-and-claude-code), May 2026.
- [CAST Imaging MCP server](https://doc.castsoftware.com/mcp-server/) — CAST documentation.
- [How we use AI agents for COBOL migration](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/) — Microsoft and Bankdata, July 2025.
- [SonarQube MCP guidance](https://defra.github.io/ai-sdlc-tool-guidance/tool-guidance/mcps/sonarqube-mcp-detailed) — UK Defra's assessment, including the data-sovereignty concern.
- [Gartner 2026 Magic Quadrant coverage](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx) — Virtualization Review, June 2026.
- [CSA research note on MCP credential theft](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/06/CSA_research_note_mcp_ai_coding_assistant_credential_theft_20260629-csa-styled.pdf) — Cloud Security Alliance, June 2026.
- [Eclipse Che4z COBOL Language Support](https://github.com/eclipse-che4z/che-che4z-lsp-for-cobol) and [ProLeap COBOL parser](https://github.com/uwol/proleap-cobol-parser) — the main open-source building blocks for custom COBOL extraction.

### Related notes

- [knowledge-graphs-for-coding-agents.md](knowledge-graphs-for-coding-agents.md) — how code graphs are built and used by agents.
- [coding-agents-in-large-codebases.md](coding-agents-in-large-codebases.md) — practices for running coding agents on large estates.
- [context-layer-databases.md](context-layer-databases.md) — the databases and stores behind an enterprise context layer.
- [context-engineering.md](context-engineering.md) — techniques for deciding what goes into an agent's context window.
- [agent-ready-content-formats.md](agent-ready-content-formats.md) — formats such as AGENTS.md and CLAUDE.md that carry context to agents.
