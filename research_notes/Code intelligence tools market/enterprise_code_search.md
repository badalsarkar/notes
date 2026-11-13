# Enterprise Code Search and Precise Code Navigation Platforms (state as of November 2026)

Scope: Sourcegraph, GitHub, GitLab, Google (internal Code Search, Kythe, Gemini Code Assist), Meta Glean, open-source engines (Zoekt, OpenGrok, livegrep, Sourcebot, Hound), JetBrains, and Atlassian (Bitbucket, Rovo). Research date: 2026-11-12. Statements marked "vendor claim" come from the vendor's own material. Most third-party "review" sites found in search were low-quality aggregators, and they are flagged where used.

## 1. What does each platform index, how does it index, and how fresh is the index?

### Takeaway
The market has split into three indexing layers that are increasingly combined: trigram or regex text indexes (Zoekt, Blackbird, livegrep, OpenGrok), compiler-accurate symbol indexes (SCIP, Kythe, Glean), and embedding or graph indexes built for AI agents (Copilot semantic index, Gemini code customization, GitLab Orbit, Atlassian code context). Freshness ranges from seconds (GitHub Copilot semantic index, GitLab Orbit updates) to roughly 24 hours (Gemini Code Assist code customization) to up to 48 hours for an initial Atlassian index.

### Cited Findings

**Sourcegraph**
- Sourcegraph's Enterprise plan bundles Code Search, symbol search, code navigation, Deep Search (an AI agentic search), Batch Changes, Code Insights and Code Monitoring as of November 2026. — [Sourcegraph pricing](https://sourcegraph.com/pricing)
- Sourcegraph's text search uses Zoekt, a trigram-based engine that Sourcegraph took over maintaining from its creator Han-Wen Nienhuys in November 2021 and keeps under Apache 2.0. — [Sourcegraph blog, Zoekt maintainership](https://sourcegraph.com/blog/sourcegraph-accepting-zoekt-maintainership); [sourcegraph/zoekt repo](https://www.github.com/sourcegraph/zoekt)
- Precise code navigation in Sourcegraph uses SCIP, a Protobuf-based index format that Sourcegraph introduced to replace the JSON-based LSIF because it is more space-efficient and simpler; SCIP indexers exist for Go, Java, TypeScript, Python, Ruby, C++, C# and other languages. — [Sourcegraph blog, Announcing SCIP (2022)](https://sourcegraph.com/blog/announcing-scip)
- Sourcegraph 7.0 (announced 2026-02-25) improved Deep Search accuracy, added image support, embedded code navigation in a Deep Search sidebar, and began rolling out a new versioned API; it also deprecated Search Notebooks and removed Cody Web for Deep Search customers. — [Sourcegraph blog, A new era for Sourcegraph (2026-02-25)](https://sourcegraph.com/blog/a-new-era-for-sourcegraph-the-intelligence-layer-for-ai-coding-agents-and-developers)
- A Sourcegraph enterprise page claims "8+ terabytes of code" at an unnamed finance-industry customer (vendor claim, undated preview page). — [Sourcegraph enterprise page (preview deploy)](https://deploy-preview-7029--sourcegraph.netlify.app/enterprise)

**GitHub**
- GitHub Copilot builds a semantic code search index per repository; the first build can take up to 60 seconds for a large repository, and the index usually reflects recent changes within seconds of starting a new conversation. — [GitHub Docs, Repository indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)
- "Instant" semantic code search indexing became generally available on 2025-03-12. — [GitHub changelog 2025-03-12](https://github.blog/changelog/2025-03-12-instant-semantic-code-search-indexing-now-generally-available-for-github-copilot/)
- In VS Code, Copilot can index non-GitHub workspaces (for example GitLab or local repositories) by uploading the content to GitHub; this is available only on GitHub.com, not on GHE.com or GitHub Enterprise Server, and on Business or Enterprise plans an owner must enable the "Semantic indexing for non-GitHub repositories" policy, which is disabled by default. — [GitHub Docs, Repository indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)
- GitHub's April 2026 VS Code release notes (v1.116 to v1.119) state that semantic indexing now works in all workspaces and that agents can run grep-style searches across GitHub repositories and organizations. — [GitHub changelog 2026-05-06](https://github.blog/changelog/2026-05-06-github-copilot-in-visual-studio-code-april-releases/)
- On 2026-05-20 GitHub added semantic issue search in Copilot Chat, backed by a separate semantic issues index. — [GitHub changelog 2026-05-20](https://github.blog/changelog/2026-05-20-semantic-issue-search-in-copilot-chat/)
- On 2026-09-22 GitHub announced whole-codebase indexing for C++ code intelligence in Copilot CLI. — [GitHub changelog 2026-09-22](https://github.blog/changelog/2026-09-22-faster-c-code-intelligence-with-whole-codebase-indexing)
- GitHub's lexical code search engine (Blackbird, launched 2023) is a custom Rust engine using ngram indexes; GitHub's engineering post at launch described indexing about 45 million repositories and 115 TB of code (dated February 2023, vendor claim). — [GitHub engineering blog, The technology behind GitHub's new code search (2023)](https://github.blog/engineering/architecture-optimization/the-technology-behind-githubs-new-code-search/)

**GitLab**
- GitLab's "exact code search" is built on Zoekt; on GitLab Self-Managed an administrator must install Zoekt (Zoekt chart or GitLab Operator) and enable it. The documentation page found lists the feature status as "Limited availability"; the Zoekt search API became generally available in GitLab 18.4, and a Zoekt integration page says something reached general availability in GitLab 19.5, but the page does not clearly say whether that is the whole feature. — [GitLab Docs, Exact code search](https://docs.gitlab.com/user/search/exact_code_search)
- GitLab Orbit (previously named GitLab Knowledge Graph) was announced in public beta on 2026-06-10; it builds a single graph across code, work items, pipelines, deployments and production signals. — [GitLab blog, Introducing GitLab Orbit (2026-06-10)](https://about.gitlab.com/blog/introducing-gitlab-orbit/); [GitLab press release 2026-06-10](https://about.gitlab.com/press/releases/2026-06-10-gitlab-announces-new-capabilities-to-give-enterprises-speed-control-at-agentic-scale/)
- Orbit has two variants: Orbit Local is an embedded code-indexing engine that agents query on the developer machine, and Orbit Remote is a hosted service that combines code indexing with the wider SDLC data. — [GitLab Docs, Orbit Local](https://docs.gitlab.com/orbit/local/); [GitLab Docs, Orbit Remote](https://docs.gitlab.com/orbit/remote/)
- Orbit Remote indexes source code on the default branch of each project (files, directories, definitions, imports and calls); initial indexing usually takes minutes and up to a few hours for large codebases, and subsequent updates arrive within seconds to minutes; code on non-default branches must be queried through the local graph. — [GitLab Docs, What Orbit indexes](https://docs.gitlab.com/orbit/remote/indexing/)
- Orbit's architecture replicates GitLab Postgres through Siphon CDC into a ClickHouse data lake, and indexers write graph data through NATS, reading repository data from Gitaly. — [GitLab runbook, Orbit Service](https://runbooks.gitlab.com/orbit/)
- GitLab states that Orbit indexed over 40,000 of its own projects in under 45 minutes (vendor claim). — [GitLab blog, Introducing GitLab Orbit](https://about.gitlab.com/blog/introducing-gitlab-orbit/)

**Google**
- Gemini Code Assist "code customization" is available only in Gemini Code Assist Enterprise; it indexes private repositories connected through Developer Connect, refreshes the index every 24 hours, allows one index per project and per organization, and caps indexing at 20,000 repositories. — [Google Cloud docs, Code customization overview](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization-overview?hl=en); [Gemini Code Assist quotas](https://developers.google.com/gemini-code-assist/resources/quotas?authuser=0)
- Google's internal Code Search uses Kythe for cross-reference results, according to a 2020 report on Google making its Code Search available for open-source projects (dated April 2020). — [InfoQ, Google Code Search available (2020)](https://www.infoq.com/news/2020/04/google-code-search-available)
- Kythe is Google's open-source, language-agnostic graph schema and toolchain for code cross-references, announced in 2015. — [Google Open Source blog, Kythe (2015)](https://opensource.googleblog.com/2015/01/kythe-new-approach-to-making-developer.html)

**Meta Glean**
- Glean is Meta's open-source system (open-sourced in August 2021) for collecting, deriving and querying facts about source code through a declarative query language (Angle); Meta uses it internally for code browsing, code search and documentation generation. — [Meta Engineering, Indexing code at scale with Glean (2024-12-19)](https://engineering.fb.com/2024/12/19/developer-tools/glean-open-source-code-indexing/)
- Glean ships indexers for about ten languages and can ingest SCIP indexes, so Sourcegraph's SCIP indexers can feed a Glean database. — [Simon Marlow, Indexing Hackage: Glean vs. hiedb (2025-05-22)](https://scriptagc.wasmer.app/https_simonmar_github_io/posts/2025-05-22-Glean-Haskell_html)

**Open-source engines**
- Zoekt is an Apache 2.0, trigram-indexed code search engine; the Sourcegraph-maintained repository describes itself as the de facto source of Zoekt, and it powers Sourcegraph, GitLab exact code search and Sourcebot. — [sourcegraph/zoekt](https://www.github.com/sourcegraph/zoekt); [Sourcebot vs OpenGrok (vendor blog)](https://www.sourcebot.dev/blog/sourcebot-vs-opengrok)
- OpenGrok is an Oracle-maintained Java search and cross-reference engine under CDDL 1.0; a 2026 roundup reports release 1.14.17 on 2026-08-24. — [getunblocked, Sourcegraph alternatives 2026 (vendor blog)](https://getunblocked.com/blog/sourcegraph-alternatives/)
- livegrep provides interactive regex search over multi-gigabyte repositories and is inspired by the original Google Code Search; it requires running the backend and web interface separately. — [Slashdot comparison, Sourcebot vs livegrep](https://slashdot.org/software/comparison/Sourcebot-vs-livegrep/)

**Atlassian**
- Atlassian "code context" indexes Bitbucket repositories directly and mirrors GitHub repositories before indexing; pushes trigger incremental re-indexing, but recently pushed code may not appear immediately, and the initial index can take up to 48 hours (another Atlassian page says 24 hours). — [Atlassian support, What is code context?](https://support.atlassian.com/rovo/docs/what-is-code-context/); [Atlassian support, Set up code context](https://support.atlassian.com/rovo/docs/set-up-code-context-for-your-site/)
- Code context combines lexical and semantic (embedding) search; Atlassian recommends lexical search for exact function names because semantic ranking is based on conceptual similarity. — [Atlassian support, What is code context?](https://support.atlassian.com/rovo/docs/what-is-code-context/)

### Inferences
- Precise, compiler-accurate navigation (SCIP, Kythe, Glean) remains the differentiator for Sourcegraph and the hyperscaler internal tools, while GitHub, GitLab Orbit and Atlassian rely on lighter-weight parsing (definitions, imports, calls) plus embeddings; the lighter approach covers more languages cheaply but is likely less accurate for overloaded symbols and cross-repository references.
- GitHub's semantic index is optimised for freshness within a single repository conversation, whereas Gemini's 24-hour refresh means agents can reason over code that is up to a day stale, which matters for fast-moving trading codebases.
- GitLab Orbit's default-branch-only remote index is a design limitation that pushes branch-level questions to the local graph.

### Gaps
- No authoritative current figure was found for Sourcegraph's maximum scale (repositories or lines of code) or for GitHub Blackbird's 2026 corpus size; the 2023 GitHub numbers are from memory of GitHub's launch blog and should be re-checked.
- Whether GitLab exact code search as a whole is GA on Self-Managed in 19.x could not be confirmed from a primary release note.
- No 2025-2026 primary source was found on Google's internal Code Search or on Kythe's current internal role.
- Hound (originally Etsy) was not researched in detail; its current maintenance status is unverified.
- JetBrains IDE indexing (local PSI-based stubs and indexes, plus shared indexes) was not covered by any 2026 source found; it is a local, per-IDE index rather than an enterprise search service.

## 2. What does each platform expose to AI agents (MCP tools, APIs, agent products), and with what permission model?

### Takeaway
Every major vendor now ships an MCP endpoint, and all of them claim to enforce the caller's existing repository permissions. Sourcegraph exposes the richest code-specific toolset (keyword, natural-language, definition, reference, commit and diff search plus Deep Search), GitLab Orbit exposes a graph over code and lifecycle data, GitHub exposes code search through its broad MCP server and uses semantic search inside its own coding agent, and Atlassian meters code search through Rovo credits.

### Cited Findings

**Sourcegraph MCP server (v7.x)**
- Sourcegraph exposes three MCP endpoints: `/.api/mcp` (core search, repository, history and Deep Search reading tools), `/.api/mcp/all` (full suite) and `/.api/mcp/deepsearch` (Deep Search agent tools only). — [Sourcegraph docs v7.5, MCP server](https://7.5.sourcegraph.com/api/mcp)
- Tools include `read_file`, `list_files`, `list_repos`, `keyword_search`, `nls_search`, `evaluator` (sandboxed Lua), `go_to_definition`, `find_references`, `commit_search`, `diff_search`, `compare_revisions`, `get_contributor_repos`, a beta metered `code_finder` search agent, and `deepsearch` / `deepsearch_read`. — [Sourcegraph docs v7.5, MCP server](https://7.5.sourcegraph.com/api/mcp)
- Authentication is OAuth 2.0 (dynamic client registration or static clients) or Sourcegraph access tokens with an `mcp` scope; admins can disable MCP (`mcp.enabled`) or individual tools (`mcp.tools.disabled`); RBAC requires the `MCP#ACCESS` permission, and repository permissions still apply so users can only read repositories they can already access. — [Sourcegraph docs v7.5, MCP server](https://7.5.sourcegraph.com/api/mcp)
- From the 2026-03-30 release, the default `/.api/mcp` endpoint moved to a curated set of tools focused on context gathering. — [Sourcegraph docs changelog](https://sourcegraph.com/docs/CHANGELOG)
- Sourcegraph 7.0 positions the product as an "intelligence layer" for third-party agents and lets admins track MCP tool usage in Sourcegraph Analytics. — [Sourcegraph blog (2026-02-25)](https://sourcegraph.com/blog/a-new-era-for-sourcegraph-the-intelligence-layer-for-ai-coding-agents-and-developers)
- The pricing page lists integrations with Claude Code, Cursor, Codex and Amp, along with GraphQL and REST APIs and a CLI. — [Sourcegraph pricing](https://sourcegraph.com/pricing)

**Cody and Amp**
- Sourcegraph stopped new Cody Free and Pro sign-ups on 2025-06-25 and ended access on 2025-07-23; Enterprise Starter was also discontinued, and affected users were offered Amp credits. — [Sourcegraph blog, Changes to Cody Free, Pro and Enterprise Starter](https://sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans)
- Cody Enterprise remains available to existing enterprise customers according to secondary sources; the 2026 pricing page does not mention Cody at all. — [Wikipedia, Sourcegraph](https://en.wikipedia.org/wiki/Sourcegraph); [Sourcegraph pricing](https://sourcegraph.com/pricing)
- Amp, Sourcegraph's agentic coding product launched in 2025, was spun out as a separate company in December 2025; secondary sources disagree on the entity name ("Amp Frontier Corporation" or "Amp Inc."), and Amp bills separately at ampcode.com. — [Latent Space wiki, Amp](https://latent.space/wiki/amp-code/); [HackerNoon, Sourcegraph spins out Amp](https://hackernoon.com/sourcegraph-spins-out-amp-to-chase-the-ai-coding-frontier)

**GitHub**
- Copilot's cloud coding agent uses the semantic code search index automatically when it fits the task, with no configuration required. — [GitHub Docs, Repository indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)
- GitHub's 2026-03-17 changelog states that the Copilot coding agent works faster with semantic code search. — [GitHub changelog 2026-03-17](https://github.blog/changelog/2026-03-17-copilot-coding-agent-works-faster-with-semantic-code-search/)
- The remote GitHub MCP server became generally available on 2025-09-04; it exposes code search (`search_code`) alongside issues, pull requests, Actions, security and other toolsets. — [GitHub changelog 2025-09-04](https://github.blog/changelog/2025-09-04-remote-github-mcp-server-is-now-generally-available/); [github-mcp-server v1.5.0](https://pkg.go.dev/github.com/github/github-mcp-server@v1.5.0)
- GitHub Enterprise Server does not support the remote MCP server; GHES and GHE.com data-residency customers run the local server with a hostname setting, and Copilot Business/Enterprise organizations govern MCP use through the "MCP servers in Copilot" policy and allowlists. — [GitHub Docs, MCP overview](https://docs.github.com/en/copilot/concepts/customizations/mcp); [Portkey, GitHub MCP server](https://portkey.ai/docs/integrations/mcp-servers/github-mcp-server)
- Copilot Spaces reached GA on 2025-09-25 and grounds Copilot Chat in curated repositories, files and documents; secondary sources report that the MCP Spaces toolset is remote-only and read-only (list and load a space). — [GitHub changelog label, Copilot Enterprise](https://github.blog/changelog/label/copilot-enterprise); [skills.sh, copilot-spaces](https://www.skills.sh/github/awesome-copilot/copilot-spaces)
- Copilot does not use indexed repositories for model training, and content-exclusion policies filter data before it reaches Copilot Chat (Business and Enterprise). — [GitHub Docs, Repository indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing)

**GitLab**
- GitLab Orbit serves the graph to the GitLab CLI, an MCP endpoint, a REST API and the GitLab Duo Agent Platform, and GitLab authorizes each query so that every answer is filtered by the user's GitLab permissions. — [GitLab Docs, Orbit](https://docs.gitlab.com/orbit/); [GitLab runbook, Orbit](https://runbooks.gitlab.com/orbit/)
- GitLab claims that agents using Orbit answered up to 11x faster and used up to 4.5x fewer tokens in internal testing, and that Claude Code, Codex and OpenCode can connect through MCP (vendor claim). — [GitLab blog, Introducing GitLab Orbit](https://about.gitlab.com/blog/introducing-gitlab-orbit/)
- A GitLab issue on enterprise gaps in exact code search notes that exact code search has no MCP server and no `glab` CLI support (feature request, not a status statement). — [GitLab issue 624419](https://gitlab.com/gitlab-org/gitlab/-/work_items/624419)

**Atlassian**
- The Atlassian Rovo MCP Server is cloud-hosted at `mcp.atlassian.com/v2/mcp`, and its code search tool searches and reads code across connected code providers; search calls consume Rovo credits. — [Atlassian Rovo MCP developer docs](https://developer.atlassian.com/cloud/rovo-mcp/)
- Rovo MCP added Bitbucket Cloud tools (list and get repositories and workspaces, create commits, open pull requests), and a separate MCP for Bitbucket Data Center has been released. — [Atlassian blog, Rovo MCP supports Bitbucket Cloud](https://www.atlassian.com/blog/bitbucket/the-atlassian-rovo-mcp-server-now-supports-bitbucket-cloud); [Atlassian developer community, MCP for Bitbucket DC](https://community.developer.atlassian.com/t/mcp-for-bitbucket-dc-has-been-released/102963)
- Code context results are scoped to what each user or authorized agent is permitted to see. — [Atlassian support, What is code context?](https://support.atlassian.com/rovo/docs/what-is-code-context/)

**JetBrains**
- Junie, JetBrains' coding agent, can call tools exposed by configured MCP servers. — [JetBrains AI Assistant 2026.1 help, Junie](https://www.jetbrains.com/help/ai-assistant/junie-agent.html)
- JetBrains IDEs act as MCP servers for external agents, and a Debugger MCP toolset requires IntelliJ IDEA 2026.1.1 or newer; Junie reportedly left beta in June 2026 (secondary source). — [JetBrains AI Assistant 2026.2 help](https://www.jetbrains.com/help/ai-assistant/2026.2/junie-agent.html); [mcp.directory, Junie after GA](https://mcp.directory/blog/junie-jetbrains-coding-agent-2026)
- JetBrains launched "AI for Teams and Organizations" in July 2026 with governance, shared context and cost controls (secondary report). — [LeadDev, JetBrains AI agent strategy](https://leaddev.com/ai/breaking-down-jetbrains-complex-ai-agent-strategy)

**Sourcebot**
- Sourcebot's MCP server requires an active Enterprise license. — [Sourcebot docs, MCP server](https://docs.sourcebot.dev/docs/features/mcp-server)

### Inferences
- The permission model is converging on "OAuth as the user, then repository ACLs apply", which means agent access is only as safe as the underlying repository ACLs; none of the sources describe agent-specific scopes narrower than the user's own access, apart from Sourcegraph's per-tool disable list and GitHub's MCP allowlists.
- Sourcegraph is the only vendor exposing precise `go_to_definition` and `find_references` as MCP tools over a cross-repository index, which is its main differentiator against platform-native options.

### Gaps
- The exact list of Orbit MCP tools was not found in the docs pages fetched.
- Google Gemini Code Assist does not appear to expose its code customization index through MCP; no source confirmed either way.
- Meta Glean, Zoekt, OpenGrok, livegrep and Hound have no official MCP servers found in this research; community wrappers may exist.

## 3. What self-hosting and data-residency options exist?

### Takeaway
Sourcegraph, GitLab (including Orbit) and the open-source engines can run fully on customer infrastructure; GitHub's AI indexing features are largely tied to GitHub.com or GHE.com, and Atlassian code context stores indexes in the United States.

### Cited Findings
- Sourcegraph's Enterprise plan offers single-tenant cloud and self-hosted deployment; the pricing page does not mention air-gapped deployment. — [Sourcegraph pricing](https://sourcegraph.com/pricing)
- GitLab Orbit is offered on GitLab.com, GitLab Self-Managed (installed on Kubernetes) and GitLab Dedicated for Premium and Ultimate tiers; when Orbit is disabled for a group, indexed data is kept for 30 days. — [GitLab Docs, Orbit](https://docs.gitlab.com/orbit/); [GitLab Docs, What Orbit indexes](https://docs.gitlab.com/orbit/remote/indexing/)
- An October 2026 press report says Orbit GA started on GitLab.com; another source attributes an October 15, 2026 GA date to the 19.5 release notes, and these could not be reconciled. — [HPCwire, GitLab Orbit GA (2026-10-30)](https://www.hpcwire.com/aiwire/2026/10/30/gitlab-orbit-now-generally-available-makes-ai-agents-more-accurate-and-less-expensive-to-run/); [Forkast](https://forkast.news/?p=132990)
- GitLab exact code search on Self-Managed requires the administrator to deploy Zoekt nodes. — [GitLab Docs, Exact code search](https://docs.gitlab.com/user/search/exact_code_search)
- Non-GitHub semantic indexing is unavailable on GHE.com and GitHub Enterprise Server; GHES docs state that most Copilot features require a presence on GitHub Enterprise Cloud. — [GitHub Docs, Repository indexing](https://docs.github.com/en/copilot/concepts/prompting-and-context/repository-indexing); [GHES 3.17 Copilot docs](https://docs.github.com/en/enterprise-server@3.17/copilot)
- An archived March 2025 changelog said instant semantic indexing was expected on GHES 3.17; GHES 3.17 itself was discontinued on 2026-09-22. — [Archived GitHub changelog (March 2025)](https://web.lumintu.workers.dev/read-https-web.archive.org/web/20250314165533/https://github.blog/changelog/); [GHES 3.17 Copilot docs](https://docs.github.com/en/enterprise-server@3.17/copilot)
- Atlassian code context stores data in an isolated environment in the United States, and disabling the feature deletes embeddings, indices and code chunks. — [Atlassian support, What is code context?](https://support.atlassian.com/rovo/docs/what-is-code-context/)
- Gemini Code Assist code customization reads repositories through Google Cloud Developer Connect, so the index lives in Google Cloud. — [Google Cloud docs, Configure code customization](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization)
- Sourcebot is free to self-host in its community tier and offers an Enterprise tier with an offline license option. — [Sourcebot pricing](https://sourcebot.dev/pricing); [Sourcebot homepage](https://sourcebot.dev)
- Zoekt (Apache 2.0), OpenGrok (CDDL 1.0) and livegrep are self-hosted by design. — [sourcegraph/zoekt](https://www.github.com/sourcegraph/zoekt); [getunblocked roundup](https://getunblocked.com/blog/sourcegraph-alternatives/)

### Inferences
- For a bank that requires on-premises or air-gapped deployment, the realistic options with agent-facing APIs are Sourcegraph self-hosted, GitLab Self-Managed with Orbit and Zoekt, Sourcebot Enterprise with an offline license, or an in-house stack (Zoekt plus SCIP or Glean). GitHub Copilot's semantic indexing and Atlassian code context both require sending code to vendor cloud services.
- Atlassian's US-only storage statement is a likely blocker for EU or APAC data-residency requirements unless Atlassian has added regions not found here.

### Gaps
- Sourcegraph's air-gapped support was not confirmed in a current primary source.
- No source confirmed whether GHES in 2026 supports Copilot repository semantic indexing for GHES-hosted repositories.
- No information was found on regional (EU) hosting for Sourcegraph Cloud or GitLab Orbit on GitLab.com.

## 4. What are pricing and licensing as of 2026?

### Takeaway
Sourcegraph is now enterprise-only with a $16K minimum annual contract and proprietary core code; GitLab Orbit is bundled into Premium and Ultimate; Gemini code customization requires the Enterprise edition; Atlassian meters code search with Rovo credits; Sourcebot uses a Fair Source licence with paid tiers; Zoekt, OpenGrok, livegrep, Kythe and Glean are open source.

### Cited Findings
- Sourcegraph lists a single Enterprise plan "starting at $16K" with a minimum annual contract; it includes per-user AI credits that pool across the organization without monthly expiry, with paid volume credit buckets; support is 24x5. — [Sourcegraph pricing](https://sourcegraph.com/pricing)
- Third-party sites quoting Sourcegraph per-seat prices ($19 per user per month for Enterprise Starter) conflict with the official page and refer to a plan that was discontinued in 2025. — [usagepricing.com, Sourcegraph Cody](https://www.usagepricing.com/blueprint/sourcegraph-cody); [Sourcegraph blog, Cody plan changes](https://sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans)
- Sourcegraph relicensed its main code to the non-open-source "Sourcegraph Enterprise" licence on 2023-06-13 and made the core repository private in August 2024; co-founder Quinn Slack said open source added "extra work and risk". A public snapshot of the repository remains. — [DevClass (2024-08-21)](https://devclass.com/2024/08/21/sourcegraph-makes-core-repository-private-co-founder-complains-open-source-means-extra-work-and-risk/); [sourcegraph-public-snapshot](https://github.com/sourcegraph/sourcegraph-public-snapshot)
- Zoekt remains Apache 2.0 under Sourcegraph maintainership. — [Sourcegraph blog, Zoekt maintainership](https://sourcegraph.com/blog/sourcegraph-accepting-zoekt-maintainership)
- GitLab Orbit is available to Premium and Ultimate customers. — [GitLab Docs, Orbit](https://docs.gitlab.com/orbit/)
- Gemini Code Assist code customization is available only in the Enterprise edition. — [Google Cloud docs, Code customization overview](https://docs.cloud.google.com/gemini/docs/codeassist/code-customization-overview?hl=en)
- Atlassian Rovo MCP code search calls consume Rovo credits. — [Atlassian Rovo MCP developer docs](https://developer.atlassian.com/cloud/rovo-mcp/)
- Sourcebot is licensed under the Functional Source License (FSL), which forbids offering it as a competing hosted product until each version's change date; the pricing page shows a $25 per seat monthly tier and a custom Enterprise tier, while Sourcebot's own llms.txt lists a $20 per user per month Pro plan, so the exact price is inconsistent. — [Sourcebot blog, Fair source (2025-07-20)](https://sourcebot.dev/blog/fair-source); [Sourcebot pricing](https://sourcebot.dev/pricing); [Sourcebot llms.txt](https://www.sourcebot.dev/llms.txt)
- OpenGrok is CDDL 1.0. — [getunblocked roundup](https://getunblocked.com/blog/sourcegraph-alternatives/)

### Inferences
- Sourcegraph's minimum contract and closed core shift it from a developer-adopted tool to a procurement-led purchase, which favours large regulated buyers but raises the barrier for teams under about 50 developers.
- Credit-metered agent search (Sourcegraph AI credits, Atlassian Rovo credits, Sourcegraph `code_finder`) means agent-heavy usage turns code search into a variable cost line, which is a change from flat per-seat search licensing.

### Gaps
- GitHub Copilot Business and Enterprise list prices for 2026 and any premium-request charges for coding agent semantic search were not verified in this research.
- JetBrains AI Enterprise and Junie 2026 pricing were not verified from a primary source.
- GitLab Premium and Ultimate 2026 list prices and any Orbit-specific add-on charges were not found.

## 5. What independent evidence, criticism and notable customers exist (especially banks and capital markets)?

### Takeaway
Independent, head-to-head benchmarks of enterprise code search for agents were not found; almost all performance numbers (GitLab's 11x, GitHub's coding agent speedups, Sourcegraph scale) are vendor claims. Criticism centres on Sourcegraph's move away from open source and product churn (Cody, Amp), Kythe's reduced investment, GitLab's default-branch limitation and incomplete exact code search, and data-residency limits of cloud-only semantic indexes.

### Cited Findings

**Customers**
- Sourcegraph claims that "4 of the top 6 US banks" have standardized on Sourcegraph and elsewhere that more than half of the world's ten largest banks are customers; neither claim names the banks (vendor claims). — [Sourcegraph blog, code search at scale](https://sourcegraph.com/blog/why-code-search-at-scale-is-essential-when-you-grow-beyond-one-repository); [Contrary Research, Sourcegraph](https://research.contrary.com/company/sourcegraph)
- Sourcegraph's published case studies include FactSet (financial data) and Neo Financial (Canadian fintech), along with HashiCorp, Nutanix, Indeed, Cloudflare and Quantcast. — [Neo Financial case study](https://test-iubs.onrender.com/case-studies/neo-financial-improves-the-developer-experience-with-sourcegraph); [Cloudflare case study](https://working-group--sourcegraph.netlify.app/case-studies/cloudflare-accelerates-debugging-and-improves-security)
- Sourcegraph commissioned a Forrester Total Economic Impact study (a vendor-commissioned study rather than independent research). — [Sourcegraph, Forrester TEI](https://about.sourcegraph.com/forrester-total-economic-impact)
- No search result linked Capital One or Citi to Sourcegraph; one Capital One case study found concerned Stardog, a different vendor. — [Stardog Capital One case study](https://www.casestudies.com/company/stardog/case-study/capital-one-customer-case-study)

**Criticism and independent signals**
- DevClass reported critically on Sourcegraph making its core repository private in August 2024, and a former Sourcegraph engineer wrote a post titled "Sourcegraph went dark". — [DevClass (2024-08-21)](https://devclass.com/2024/08/21/sourcegraph-makes-core-repository-private-co-founder-complains-open-source-means-extra-work-and-risk/); [Eric Fritz, Sourcegraph went dark](https://hn.jakechampion.name/reader/https://eric-fritz.com/articles/sourcegraph-went-dark)
- At least one open-source project (TVL) tracked migrating from Sourcegraph to livegrep after the licence change. — [TVL issue 290](https://b.tvl.fyi/issues/290)
- Sourcegraph discontinued self-serve Cody plans in 2025 and spun Amp out in December 2025, and 7.0 deprecated further features, which shows repeated product churn for buyers. — [Sourcegraph blog, Cody plan changes](https://sourcegraph.com/blog/changes-to-cody-free-pro-and-enterprise-starter-plans); [Sourcegraph blog 7.0](https://sourcegraph.com/blog/a-new-era-for-sourcegraph-the-intelligence-layer-for-ai-coding-agents-and-developers)
- The Google team working on Kythe was reportedly laid off in April 2024 (secondary source). — [Wikipedia, Google Kythe](https://en.wikipedia.org/wiki/Google_Kythe)
- GitLab's own issue tracker documents enterprise-scale usability, operational visibility and programmatic access gaps in exact code search. — [GitLab issue 624419](https://gitlab.com/gitlab-org/gitlab/-/work_items/624419)
- A third-party blog attributes a 2% task-completion gain to the Copilot coding agent's use of semantic search; this figure was not verified against GitHub's text. — [digitalapplied.com](https://www.digitalapplied.com/blog/github-copilot-coding-agent-50-percent-faster-semantic-search)
- Competitor comparison pages (Sourcebot vs OpenGrok, Unblocked's Sourcegraph alternatives) are vendor-authored marketing and are not independent benchmarks. — [Sourcebot vs OpenGrok](https://www.sourcebot.dev/blog/sourcebot-vs-opengrok); [getunblocked, AI code search tools compared](https://getunblocked.com/blog/ai-code-search-tools-compared/)
- One secondary source says SCIP moved to open governance in March 2026; this was not verified. — [Sourcegraph context-compare page (as surfaced in search)](https://sourcegraph.com/resources/context-compare)

### Inferences
- Sourcegraph's banking penetration claims are plausible given its self-hosted model and precise cross-repository navigation, but they are unverifiable without named references; buyers should request named financial-services references.
- The absence of independent agent-retrieval benchmarks means evaluation in a bank should be done with an internal task set (for example, impact analysis for a change to a shared pricing library) comparing precise navigation against embedding search.

### Gaps
- No independent benchmark comparing Sourcegraph, GitHub, GitLab Orbit and Sourcebot on agent task success was found.
- No named bank or capital markets customer was found for GitLab Orbit, Gemini code customization, Atlassian code context or Sourcebot.
- No independent reviews of GitLab Orbit after GA were found; it had only been GA for a few weeks at research time.
