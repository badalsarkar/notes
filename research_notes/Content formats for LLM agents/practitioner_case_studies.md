# Practitioner case studies: how organisations structure documentation and internal knowledge for LLMs and agents

Evidence labels used throughout these notes:

- **[Read]** means the page itself was fetched and read.
- **[Search only]** means the claim comes from a search-result extract of that URL, and the full page was not read. Verify before quoting.
- **[Self-reported]** means the organisation is reporting on itself with no independent verification.
- **[Vendor marketing]** means the publisher sells the product or approach under discussion.

## Developer documentation publishers: how do they expose docs to agents, and is there usage data?

### Takeaway
Serving the same content as Markdown is close to universal among large documentation publishers, usually with an index file, and several add an MCP server. The usage evidence splits by audience: llms.txt is almost never fetched across the general web, while Mintlify reports heavy machine-route traffic on developer docs, though from its own hosted sites and its own benchmark.

### Cited Findings
**What each publisher does**
- **Stripe (undated current docs):** Appending `.md` to a docs URL returns Markdown, an llms.txt file is published, a hosted MCP server at mcp.stripe.com can search documentation and call the API with OAuth, and agent skills install through `npx skills add https://docs.stripe.com`. [Search only] — [Build on Stripe with AI](https://docs.stripe.com/building-with-ai); [Agents and AI on Stripe](https://docs.stripe.com/agents.md)
- **Cloudflare (12 February 2026, modified 15 July 2026):** Markdown for Agents converts HTML to Markdown at the edge when a client sends `Accept: text/markdown`, returns an estimated `x-markdown-tokens` header and a `content-signal` header, and is in beta for Pro, Business and Enterprise zones. [Read] [Vendor marketing] — [Cloudflare blog](https://blog.cloudflare.com/markdown-for-agents/)
- **Cloudflare's reported saving:** The post itself dropped from 16,180 tokens as HTML to 3,150 as Markdown, about 80%, but this is one example page. [Read] [Self-reported] — [Cloudflare blog](https://blog.cloudflare.com/markdown-for-agents/)
- **Cloudflare's client claim:** Cloudflare states that Claude Code and OpenCode already send these Accept headers, and I did not verify this independently. [Read] — [Cloudflare blog](https://blog.cloudflare.com/markdown-for-agents/)
- **Vercel (14 January 2026, updated 17 January 2026):** A guide describes serving Markdown and HTML from one URL through a Next.js rewrite keyed on the Accept header, with a generated `sitemap.md` as the discovery point. It reports no measurements. [Read] — [Vercel guide](https://vercel.com/kb/guide/how-to-serve-documentation-for-agents)
- **Vercel's own docs:** Vercel's documentation pages respond to `Accept: text/markdown`. [Search only] — [Vercel changelog](https://vercel.com/changelog/docs-pages-support-markdown-responses)
- **Google (4 February 2026):** The Developer Knowledge API and MCP server, in public preview, provide search and retrieval of public developer documentation as "unstructured Markdown", with re-indexing within 24 hours of an update during the preview. [Read] — [Google Developers Blog](https://developers.googleblog.com/introducing-the-developer-knowledge-api-and-mcp-server/)
- **Google's stated next step:** Google plans to add structured content, such as code sample objects and API reference entities, before general availability. This suggests that Markdown alone was treated as a first stage and not an end state. [Read] — [Google Developers Blog](https://developers.googleblog.com/introducing-the-developer-knowledge-api-and-mcp-server/)
- **Google Search's separate position (guide updated 10 July 2026):** Google Search states that it ignores llms.txt. This was taken from a secondary table and the Google page was not read directly. [Search only] — [Google Search Central](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide), via [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)
- **Microsoft Learn (undated current docs):** A remote unauthenticated MCP endpoint at `learn.microsoft.com/api/mcp` exposes search, fetch and code-sample search tools. Microsoft warns that it is not a traditional API and that tools and request formats may change. [Search only] — [Microsoft developer reference](https://learn.microsoft.com/en-us/training/support/mcp-developer-reference)
- **GitHub Docs (undated current docs):** GitHub publishes an llms.txt index and a Docs API whose article endpoint returns Markdown and metadata. [Search only] — [docs.github.com/llms.txt](https://docs.github.com/llms.txt); [GitHub Docs API](https://docs.github.com/en/get-started/using-github-docs/github-docs-api)
- **Anthropic (observed 2 November 2026):** Claude Code's best-practices page, when fetched, is returned as Markdown beginning with a pointer to `code.claude.com/docs/llms.txt`, so the index is advertised inside each page. Its internal links also use `.md` URLs. This is my direct observation of one page and not a statement by Anthropic. [Read] — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- **Fern (2026):** Fern publishes guidance on llms.txt and LLM-friendly documentation, which I did not read in full. [Search only] [Vendor marketing] — [Fern guide](https://buildwithfern.com/post/optimizing-api-docs-ai-agents-llms-txt-guide)

**Traffic and adoption data**
- **Ahrefs (15 June 2026, May 2026 data):** About 28% of 137,210 domains (38,360) had an llms.txt file, and 97% of those files received zero requests in May 2026. Ahrefs treats 28% as an upper bound because its customers skew technical and SEO-aware. It also notes that a fetch does not prove the file was used. [Search only] — [Ahrefs study](https://ahrefs.com/blog/llmstxt-study/)
- **Ahrefs on who fetches:** About 96% of requests came from bots, 77% of those bots were not AI tools, and no AI bot requests were seen for llms.txt paths that returned 404. A secondary summary adds that Claude Code out-fetched AI retrieval bots. [Search only] — [Ahrefs study](https://ahrefs.com/blog/llmstxt-study/); [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)
- **Other adoption counts disagree because their denominators differ:**
  - SE Ranking reported 10.13% of about 300,000 domains in November 2025. — [SE Ranking](https://seranking.com/blog/llms-txt/), via [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)
  - An HTTP Archive analysis reported 5.61% of the top 10,000 sites in June 2026, up from 1.04% in July 2025. — [Casey Burridge](https://caseyrb.com/blog/state-of-llms-txt-adoption/), via [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)
  - The same analysis found that 78.1% of Shopify sites in the top 10,000 carry the file after an automatic rollout, against 8.7% of WordPress sites, so adoption counts partly measure platform defaults. — [Casey Burridge](https://caseyrb.com/blog/state-of-llms-txt-adoption/), via [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)
- **SE Ranking on effect:** The study found no significant correlation between llms.txt and AI citation frequency. This measures citations in AI search and not coding-agent success. — [Search Engine Journal](https://www.searchenginejournal.com/llms-txt-shows-no-clear-effect-on-ai-citations-based-on-300k-domains/561542/), via [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)
- **Mintlify (29 July 2026):** Agents were 66% of measured web traffic on Mintlify-hosted docs in July so far, with 213M+ agent requests against 105M human page loads, up from 15.2% at the start of 2026. [Read] [Vendor marketing] [Self-reported] — [Mintlify midyear report](https://mintlify.com/blog/state-of-docs-traffic)
- **Mintlify route mix:** Among explicit machine routes between February and July, direct `.md` rose from 25.1% to 54.4%, `text/markdown` negotiation fell from 25.2% to 8.3%, and plain text fell from 47.2% to 34.5%. [Read] [Self-reported] — [Mintlify midyear report](https://mintlify.com/blog/state-of-docs-traffic)
- **Mintlify MCP activity:** Mintlify counted 1.42M MCP tool calls, of which 56.57% were search and 43.30% were filesystem retrieval. MCP is tracked separately from the web totals. [Read] [Self-reported] — [Mintlify midyear report](https://mintlify.com/blog/state-of-docs-traffic)
- **Mintlify benchmark:** Across 2,400 runs on 20 docs sites with Claude Code and Codex, average 404 errors per retrieval request were 2.23 for HTML, 1.42 for plain Markdown and 0.11 for the llms.txt variants. [Read] [Vendor marketing] — [Mintlify midyear report](https://mintlify.com/blog/state-of-docs-traffic)
- **Limits of the Mintlify data, some stated by Mintlify:**
  - A known signature does not prove the origin of a request, and agents with browser user agents may be counted as human.
  - Switching to `.md` can raise the measured agent share without any change in task volume.
  - Better agent accuracy would lower request volume, so request counts are a weak success measure.
  - The article's "almost 90%" error reduction does not match its own chart, which implies about 92% to 95%.
  - The 66% and the projected "nearly 90%" by year-end should not be read as an industry figure. — [Mintlify midyear report](https://mintlify.com/blog/state-of-docs-traffic)
- **Earlier Mintlify figure:** A February 2026 post put AI at almost half of docs traffic. [Search only] — [Mintlify post](https://mintlify-landing-page.vercel.app/blog/ai-traffic)

### Inferences
- The Ahrefs and Mintlify results are compatible and should not be presented as a contradiction. Ahrefs measures largely non-documentation sites and direct requests for one file, while Mintlify measures developer documentation and all machine routes.
- llms.txt seems to act as a navigation aid when a coding agent is given it or directed to it, and it does not act as something crawlers discover by themselves. The Mintlify benchmark, the absence of 404 probes in Ahrefs, and Anthropic's in-page pointer are all consistent with this, but none of them proves it.
- The convergent publisher pattern is one source of truth with three access levels: a per-page Markdown rendition, an index file, and an MCP search and fetch tool.
- The direct `.md` route is growing faster than content negotiation on Mintlify, although Vercel and Cloudflare both promote negotiation. This could reflect how agents discover links, and it may also be an artefact of Mintlify's own routing.

### Gaps
- I found no traffic data published by Stripe, Vercel, Google, Microsoft, GitHub or Anthropic about their own documentation.
- I found no independent replication of the Mintlify benchmark, and its full methodology and raw data are not published.
- One search summary stated that Profound found llms-full.txt receives more agent traffic than llms.txt. I could not trace it to a primary source, so it should not be used.
- A secondary blog reports that Anthropic, OpenAI and Perplexity publish llms.txt without publicly committing to consume it in crawling, but it links no source.

## Internal engineering knowledge: how do companies organise standards, architecture docs and ADRs for coding agents?

### Takeaway
The best-documented large deployments combine a short file in the repository with a platform that holds cross-repository facts, and they rely on linters and CI for enforcement. Controlled research is much less favourable to context files than these self-reported accounts, so the contrast should be stated explicitly.

### Cited Findings
**OpenAI, harness engineering (date unconfirmed; an earlier summary gives 11 February 2026)**
- A team of three engineers, later seven, built a repository of "on the order of a million lines" with about 1,500 merged pull requests over five months, and estimates this took one-tenth of the hand-coding time. [Read from a third-party reproduction] [Self-reported] — [Reproduction on BitTide](https://bittide.aicompass.dev/article/3c74af4d-2842-4a43-8daf-ec9d37b2e1ba); original at [openai.com/index/harness-engineering](https://openai.com/index/harness-engineering/), which returned HTTP 403 to my fetch
- The giant AGENTS.md approach failed for four stated reasons: context is scarce, marking everything as important removes priority, the file goes stale, and a single blob cannot be checked mechanically for coverage, freshness or ownership. — [Reproduction on BitTide](https://bittide.aicompass.dev/article/3c74af4d-2842-4a43-8daf-ec9d37b2e1ba)
- The replacement is an AGENTS.md of about 100 lines acting as a table of contents, pointing to a `docs/` system of record that holds design docs with verification status, an architecture map, a quality grading document, versioned execution plans, and known technical debt. — [Reproduction on BitTide](https://bittide.aicompass.dev/article/3c74af4d-2842-4a43-8daf-ec9d37b2e1ba)
- Dedicated linters and CI jobs check that docs are current and cross-linked, custom linters enforce the layering Types → Config → Repo → Service → Runtime → UI with remediation steps in the error messages, and a recurring agent opens pull requests to correct documentation that no longer matches the code. — [Reproduction on BitTide](https://bittide.aicompass.dev/article/3c74af4d-2842-4a43-8daf-ec9d37b2e1ba)

**Cloudflare (20 April 2026)** [Read] [Self-reported]
- A pipeline pulls ownership and dependency metadata from Backstage, detects each repository's stack, maps it to Engineering Codex standards, drafts an AGENTS.md with a model, and opens a merge request for the owning team. About 3,900 repositories have been processed. — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- Each file is short and covers runtime, test and lint commands, navigation, conventions with rule references, boundaries, and dependencies. Standards are cited by ID, such as RFC 021 and API-REST-01, and the AI code reviewer cites the same IDs in its findings. — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- The Engineering Codex is distilled into "If you need X, use Y" rules and packaged as an agent skill with progressive disclosure across linked Markdown files. — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- Cross-repository facts stay on the platform. Backstage tracks 2,055 services, 228 APIs, 544 systems, 1,302 databases and 375 teams, among other entities, and is exposed through an MCP server with 13 tools. — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- Reported outcomes are 93% R&D adoption and a four-week average of merge requests rising from about 5,600 to over 8,700 per week. There is no controlled comparison, and adoption of these files cannot be isolated as the cause. — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- Reported problems are plausible but wrong changes caused by missing local context, less accurate first-pass files for polyglot repositories and unusual builds, and the warning that a stale file can be worse than no file. The AI reviewer flags changes that suggest the file needs updating. — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)

**Spotify (3 June 2026)** [Read] [Self-reported]
- Spotify exposes Backstage through MCP and command-line tools so that Claude can find a component's owner and documentation. "Golden state" defines recommended technology per component type, Soundcheck supports self-assessment against it, and lint and static analysis provide the feedback that lets the agent correct itself. — [Spotify Engineering](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint)
- Spotify reports that Claude performs measurably worse in fragmented codebases, which treats code consistency itself as a form of agent context. It does not publish the measurement. — [Spotify Engineering](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint)
- Reported outcomes are a 76% rise in pull request frequency and over 2.5 million merged automated maintenance PRs, and the reported cost is more review load. — [Spotify Engineering](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint)
- A separate Spotify post describes institutional knowledge as fragmented across CLAUDE.md files, bespoke MCP setups and personal prompt libraries, and it promotes Spotify's Portal product as the remedy. [Search only] [Vendor marketing] — [Spotify Portal blog](https://portal.spotify.com/blog/introducing-xirp)

**Uber (reported 24 August 2026, from a talk by Uday Kiran Medisetty and Adam Huda)** [Read through a vendor summary, not first-party]
- Agents were wasting tokens finding service information spread across 20 to 30 systems, so Uber built a context graph of about 40 million entries across 150 kinds of nodes and edges, covering code, design docs, Jira, incidents and bugs. Large reductions in tokens, turns and latency are reported without figures. — [Port newsletter](https://newsletter.port.io/p/how-uber-built-a-software-factory)
- An MCP gateway reaches over 1,000 tools and reduced tokens by over 40%, by replacing many tools with a single discovery-and-call tool and compacting responses. — [Port newsletter](https://newsletter.port.io/p/how-uber-built-a-software-factory)
- A registry of 2,500 skills with automated lint and review runs over 20,000 skill runs a day, and usage traces and evals go back to authors. The problems it addresses are duplicate skills, hard-to-find skills and uneven quality. — [Port newsletter](https://newsletter.port.io/p/how-uber-built-a-software-factory)
- Port sells a competing platform and the post ends with a pitch, so Uber's numbers should be checked against the talk if they are to be relied on. — [Port newsletter](https://newsletter.port.io/p/how-uber-built-a-software-factory)
- Simple CI checks were moved into an inner-loop validate command that agents run before opening a pull request. [Search only] — [The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development)

**Anthropic's product guidance (undated current docs)** [Read]
- CLAUDE.md is loaded into every session, so Anthropic advises keeping it short and limited to what Claude cannot work out from the code. — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- Instructions are described as non-deterministic and hooks, deny rules and managed settings as deterministic: "If something has to happen every time, make it a hook, a deny rule, or a managed setting." — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- Skills are recommended for long procedures because only the name and description are present in every session. Anthropic also says a line may be ignored because the file has grown long enough for it to get lost. — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- Anthropic is a vendor describing its own product, and its claims about attention are not accompanied by data on that page. — [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

**Thoughtworks Technology Radar**
- AGENTS.md was rated Trial in November 2025, described as a README for agents with no required structure, and is no longer on the current Radar edition. Thoughtworks warns that older blips may be out of date. A related context engineering blip is listed as Adopt in April 2026. [Read] — [Thoughtworks Radar](https://www.thoughtworks.com/en-au/radar/techniques/agents-md)
- A community digest of Vol. 34 (April 2026) says that "Curated shared instructions for software teams" recommends anchoring guidance in service templates, and that agent skills reduce instruction bloat. [Search only, not first-party] — [Vol. 34 digest](https://agentic-ai.readthedocs.io/en/latest/AgenticTechStack/thoughtworks-radar-vol34/)

**Cross-company**
- A May 2026 roundup of the Background Agents Summit states that every organisation built a tool and context integration layer. [Search only] [Vendor marketing] — [Ona guide](https://ona.com/guides/background-agents)

**Controlled evidence that complicates these accounts**
- **Gloaguen et al., listed by ETH Zurich's SRI Lab (arXiv 2602.11988, v1 12 February 2026, v3 29 September 2026):** Tested with Claude Code, Codex and Qwen Code on SWE-bench Lite (300 tasks) and CTXbench (138 instances). [Read] — [arXiv HTML](https://arxiv.org/html/2602.11988); [abstract](https://arxiv.org/abs/2602.11988)
  - LLM-generated files changed resolution rate by −0.5% and −2%, which was not significant, and raised cost by about 20% and 23%, which was significant.
  - Developer-written files improved resolution by 2.4% on average, which was not significant (p = 21%), and raised cost by up to 19%. They did significantly outperform LLM-generated files.
  - When all existing documentation was removed, LLM-generated files improved performance by 2.7%, which suggests that they mainly duplicate existing docs.
  - Repository overviews did not reduce the steps needed to reach the relevant file, but instructions were followed. For example, `uv` was used 1.6 times per instance when named and under 0.01 times when not.
  - The authors recommend omitting LLM-generated files for now and limiting human-written files to what the README does not already contain.
- **A version conflict on these figures:** Secondary write-ups of the earlier version quote +4% for developer files and −2% or −3% for generated files. Use the current version's figures. — [DAIR.AI summary](https://academy.dair.ai/blog/agents-md-evaluation); [Hacker News thread](https://news.ycombinator.com/item?id=47034087)
- **Author affiliation caveat:** The ETH label comes from the search listing of the SRI Lab publication page, and individual author affiliations were not checked. [Search only] — [ETH SRI Lab](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd)
- **McMillan factorial study (arXiv 2605.10039, 11 May 2026):** Across 1,650 Claude Code sessions and 16,050 function-level observations, file size, instruction position, file architecture and adjacent-file conflict showed no detectable effect on adherence to a trivial annotation. The largest effect was within a session, with about 5.6% lower odds of compliance per additional generated function. [Read, abstract only] — [arXiv](https://arxiv.org/abs/2605.10039)
- **An empirical study of 2,303 context files:** The study found that these files are actively maintained and evolve like configuration. [Search only] — [arXiv 2511.12884](https://arxiv.org/pdf/2511.12884)

### Inferences
- A recurring split separates what belongs in the repository from what belongs on a platform. Repository-local commands, conventions and rule references stay in the repository, because they must version with the code. Facts spanning many repositories, such as ownership, dependencies and API catalogues, stay on a platform and are reached through MCP.
- Cloudflare's generated-then-reviewed files look at first like a counterexample to the ETH recommendation. They differ in that they inject information absent from the repository, namely Backstage metadata and Codex rule IDs. This matches the ETH result that generated files helped once they were no longer duplicating documentation, although Cloudflare has not published a controlled test of this.
- The organisations reporting success all pair documents with mechanical enforcement, so their outcomes cannot be attributed to document format alone.
- The size-related guidance from OpenAI and Anthropic and the McMillan null result address different outcomes. McMillan measures adherence to one trivial instruction and does not measure crowding out of the task, so it weakens the claim that long files cause lost rules but does not address cost or task success.

### Gaps
- I found no first-party Shopify or Airbnb account of how they organise knowledge for coding agents. Shopify's automatic llms.txt for merchants is a different topic.
- I could not fetch OpenAI's original post, so its text and date rest on a third-party reproduction that I could not compare with the original.
- I found no first-party Uber written account. The available one is a competitor's summary of a talk.
- One blog reports that an Anthropic evaluation on SWE-bench Verified raised Claude's resolve rate from 54.3% to 61.3% with AGENTS.md files. I could not find the primary source, so it should not be cited as Anthropic's result. — [Secondary blog](https://luonghongthuan.com/en/blog/agents-md-context-file-design-ai-agents-2026/)
- No account located states what happens to ADRs specifically in large monorepos, or provides a published AGENTS.md hierarchy design with results.

## ADRs and agents: are there published practices for agents reading, writing or enforcing decision records?

### Takeaway
AWS, Microsoft and Google all publish ADR guidance that recommends close-to-code or repository storage and immutable records, but none of the pages read mention agents. Agent-oriented ADR practice exists mostly as small open-source tools and proposals, and I found no large organisation reporting measured results from it.

### Cited Findings
**Cloud vendor guidance, none of it agent-specific**
- **AWS Prescriptive Guidance (undated):** An accepted ADR is immutable and a new ADR supersedes it. ADRs move through Proposed, Accepted, Rejected and Superseded states, and code reviewers link to an ADR when a change violates it. Enforcement is therefore described as human review. [Read] — [AWS ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- **Microsoft Azure Well-Architected (10 April 2026):** The ADR is an append-only log, and each record has a status and a recorded confidence level. Records should be "pithy, assertive, on-topic, and factual" and should not become design guides, and supplementary material is linked. The page says that brownfield workloads can have ADRs retroactively generated from known decisions. [Read] — [Microsoft Learn](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- **Google Cloud (undated):** Google recommends storing ADRs "close to your application code, ideally in the same version control system" as lightweight Markdown, optionally mirroring key decisions to a wiki for people outside the team. [Read] — [Google Cloud](https://docs.cloud.google.com/architecture/architecture-decision-records)

**Agent-oriented proposals and tools**
- **InfoQ, "Agentic Fitness Functions" (17 August 2026):** Hemant Kumar Mahato, Łukasz Sieczkowski and Vijayasenthilkumar Kuppusamy propose running deterministic checks first and then a calibrated agent with a versioned rubric and a small evidence pack. It returns a structured verdict with score, confidence, rationale and recommended action. One example is an ADR Drift Monitor. [Read] — [InfoQ](https://www.infoq.com/articles/agentic-fitness-functions-evolutionary-architecture/)
- **Status of that proposal:** It has a reference implementation and no production deployment or measured precision. The authors treat agentic checks as advisory and list position bias, non-determinism, prompt injection and rubric drift as failure modes. — [InfoQ](https://www.infoq.com/articles/agentic-fitness-functions-evolutionary-architecture/)
- **Archgate:** The tool pairs ADRs with companion rule files, and its checks report the file, line and broken ADR. Maturity is unverified. [Search only] [Vendor or author self-description] — [Archgate on PyPI](https://pypi.org/project/archgate/)
- **ADR Kit:** The tool targets MADR-format ADRs, supports a policy block in ADR front matter, and exposes MCP tools to agents. Maturity is unverified. [Search only] [Author self-description] — [ADR Kit](https://github.com/kschlt/adr-kit)
- **ADR Guard and kgai:** One is a GitHub Action failing a pull request when watched code changes without a matching ADR, and the other is an append-only decision log for agents. Both are listed in a community list. [Search only] — [ADR GitHub list](https://github.com/architecture-decision-record/architecture-decision-record)
- **Microsoft-hosted project use:** The agent-governance-toolkit repository keeps ADRs with accepted, proposed, deprecated and superseded statuses. This shows ADR use in an agent project and does not show agents consuming them. [Search only] — [Microsoft Agent Governance Toolkit](https://microsoft.github.io/agent-governance-toolkit/adr/)

**Closest large-scale analogues, without ADRs**
- OpenAI enforces layering through custom linters and structural tests, with remediation text aimed at the agent. — [Reproduction on BitTide](https://bittide.aicompass.dev/article/3c74af4d-2842-4a43-8daf-ec9d37b2e1ba)
- Cloudflare's AI reviewer cites rule IDs from the Engineering Codex and RFCs, and the sample AGENTS.md references the same IDs. — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- Morgan Stanley validates CALM documents at build time with Spectral rulesets. — [InfoQ, QCon London 2026](https://www.infoq.com/news/2026/03/morgan-stanley-apis-mcp-calm/)

### Inferences
- The vendor guidance happens to suit agents well, since immutable records, explicit statuses and a repository location are what would let an agent filter out superseded decisions. This is my inference, and none of the vendors claims it.
- The status field and supersession links are the most important machine-readable elements of an ADR, because without them an agent cannot tell that a decision is no longer current. OpenAI's complaint that agents cannot tell what is still true is the same problem at file level.
- A reasonable working pattern is a decision record in prose, a rule ID, and a deterministic check that cites that ID. This pattern is assembled from Cloudflare and OpenAI practice and is not a practice any of them documents under the name ADR.

### Gaps
- I found no first-party report from a large organisation about agents writing ADRs or about rules generated automatically from ADRs at scale, with results.
- I found no evidence on whether a specific machine-readable ADR schema improves agent compliance compared with plain MADR Markdown.
- ArchUnit's role was only seen in search results and a sample project's issue, and I found no published agent-specific case. — [Sample issue](https://github.com/aanbrn/axon-showcase/issues/262)

## Security policy and compliance: how do organisations make policy agent-readable?

### Takeaway
The clearest public case is FedRAMP, which moved towards mandatory machine-readable authorisation data and then narrowed the requirement after public comment. I found no first-party account of compliance vendors or large companies measuring results from agent access to policy libraries.

### Cited Findings
- **FedRAMP RFC-0024 (2026):** The original proposal for Rev5 machine-readable packages named OSCAL as the approved format, with a proposed effective date of 30 September 2026. [Search only] — [RFC-0024](https://www.fedramp.gov/rfcs/0024/)
- **FedRAMP's narrowing, Notice 0009 (25 March 2026):** Comprehensive machine-readable data is now required only for Class D (High), while Classes A to C provide some machine-readable data and mostly semi-structured text, with DOCX and XLSX being retired. [Read] — [FedRAMP NTC-0009](https://www.fedramp.gov/notices/0009/)
- **Reasons for the narrowing:** A "significant majority" of commenters raised concern about complexity, and they "nearly universally" asked for more time. FedRAMP also said that building its own tooling would need a 3 to 5 times budget increase and several years. The notice gives no comment counts. [Read] — [FedRAMP NTC-0009](https://www.fedramp.gov/notices/0009/)
- **Deadlines in the notice:** Active certifications must meet the 2027-11-01 milestone, and new Class D submissions must meet 2027-05-01. [Read] — [FedRAMP NTC-0009](https://www.fedramp.gov/notices/0009/)
- **Generation direction:** All providers must generate human-readable materials from the machine-readable ones. The notice names the OSCAL Foundation as an industry partner and does not require OSCAL by name. [Read] — [FedRAMP NTC-0009](https://www.fedramp.gov/notices/0009/)
- **CR26 (mid-2026):** Secondary sources say the Consolidated Rules were published around 25 June 2026 and replace narrative guidance with MUST and MUST NOT requirements published as structured data on GitHub. They disagree on the effective date and on the Rev5 and Class D detail. I did not read the primary text. [Search only] — [CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-fedramp-20x-consolidated-rules-transition/); [Kiteworks preview](https://www.kiteworks.com/regulatory-compliance/fedramp-cr26-authorization-changes/)
- **Vanta (4 August 2025):** Vanta's FedRAMP 20x pilot write-up says machine-readable formats are required and that teams should involve product teams early, and it does not mention OSCAL. It says Key Security Indicators need interpretation because no definitive guidebook exists. [Read] [Vendor marketing] [Self-reported] — [Vanta](https://www.vanta.com/resources/lessons-learned-from-vantas-fedramp-20x-pilot)
- **Vanta and Drata status conflicts:** Competitor and aggregator pages disagree on which products hold which authorisation. Treat these as unresolved and check the FedRAMP Marketplace. [Search only] [Competitor content] — [Paramify comparison](https://www.paramify.com/blog/paramify-vs-vanta); [Axipro on Drata](https://axipro.co/drata-fedramp-authorization/)
- **Cloudflare, policy compliance by agents (20 April 2026):** The Network Firewall team audited `rampartd` with a multi-agent consensus process that scored each requirement as COMPLIANT, PARTIAL or NON-COMPLIANT and gave remediation steps. Cloudflare says this turned weeks of work into a repeatable process, without published accuracy figures. [Read] [Self-reported] — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- **FINOS to the Financial Stability Board (5 August 2026):** FINOS asks the FSB to recognise open "machine-readable control libraries ('governance as code')" as a legitimate way to operationalise its sound practices. This is advocacy by a project steward. [Read] — [FINOS response to FSB](https://www.fsb.org/uploads/FINOS.pdf)

### Inferences
- FedRAMP's narrowing is the most useful retreat in this section. A regulator with the authority to mandate a structured format chose semi-structured text for most classes after providers objected to the transition cost. The decision concerns the cost of migration and does not show that structured data has no value.
- The requirement to generate human-readable output from a machine-readable source inverts the usual approach of extracting structure from prose. CALM's Markdown generation follows the same direction.

### Gaps
- I found no first-party statement about Vanta or Drata MCP servers or agent access to their policy libraries in this research, although such products may exist.
- A vendor blog extract said no formal 20x Phase 1 participant used OSCAL for its machine-readable materials. I could not identify a primary source, so this should not be used without verification.
- I found no first-party case with measured results for RAG over a policy library. GitHub's own policy-as-code practice for agents was not found either.
- The final CR26 text on OSCAL was not read, so the current requirement should be confirmed at [fedramp.gov](https://www.fedramp.gov/notices/).

## Hybrid patterns: who uses frontmatter, sidecars, generated documents, knowledge graphs and enterprise platforms?

### Takeaway
The strongest named cases generate documents from a structured source or use a graph or catalogue beside Markdown. Published results on the commercial enterprise platforms were not found in this research, and the security record of Atlassian Rovo is better documented than any productivity result.

### Cited Findings
**Documents generated from a structured source**
- **Morgan Stanley with CALM (14 December 2025):** Lead architect Khal Elsawaf generates block and sequence diagrams and tables from one model, and writes Markdown Solution Architecture Descriptions that pull in live architecture data, replacing static PowerPoint decks. He said he had used CALM for about six weeks. [Read] [Self-reported, published by the project's foundation] — [FINOS blog](https://www.finos.org/blog/confessions-of-a-calm-aholic-how-morgan-stanley-automates-architecture-without-writing-json)
- **Limits shown in that demo:** The AI copilot misclassified a service and one relationship needed re-prompting, the extension host needed a restart, the system was simplified, and Elsawaf said he did not know the JSON schema. — [FINOS blog](https://www.finos.org/blog/confessions-of-a-calm-aholic-how-morgan-stanley-automates-architecture-without-writing-json)
- **Cloudflare (20 April 2026):** AGENTS.md is generated from Backstage metadata and repository analysis and then reviewed by the owning team. [Read] [Self-reported] — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- **FedRAMP (25 March 2026):** Human-readable materials must be generated from the machine-readable materials. [Read] — [FedRAMP NTC-0009](https://www.fedramp.gov/notices/0009/)

**Markdown with frontmatter or an inline rule block**
- **ADR Kit:** It places a policy block in ADR front matter. This is a small open-source example, and I found no large-organisation adopter. [Search only] — [ADR Kit](https://github.com/kschlt/adr-kit)
- **Agent skills:** Stripe, Cloudflare and Uber all package knowledge as skills, which agents discover through a name and description before reading the full Markdown. [Search only for Stripe] — [Stripe skills](https://docs.stripe.com/skills); [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/); [Port newsletter on Uber](https://newsletter.port.io/p/how-uber-built-a-software-factory)

**Knowledge graphs and catalogues over documents**
- **Uber:** About 40 million entries across 150 kinds of nodes and edges, as reported above. — [Port newsletter](https://newsletter.port.io/p/how-uber-built-a-software-factory)
- **Cloudflare:** The post describes a 16K+ entity knowledge graph on Backstage. [Search only for the 16K+ figure] — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- **Backstage TechDocs gap:** A Medium author states that the TechDocs plugin had no native MCP tool support at the time of writing. [Search only, single author, undated here] — [Medium post](https://nitin15j.medium.com/turning-backstage-into-an-ai-ready-platform-with-mcp-2412bf744a64)
- **data.world benchmark, reported by a vendor:** A 2026 article cites GPT-4 scoring 54% with a knowledge graph against 16% over raw SQL. This concerns SQL question answering and not documentation, and it comes through a vendor-hosted article. [Search only] [Vendor marketing] — [Galaxy](https://www.getgalaxy.io/articles/enterprise-context-management-ai-agents)

**Enterprise platforms**
- **Atlassian Rovo and MCP:** The available evidence concerns security, covered in the failures section below. — [PromptArmor](https://www.promptarmor.com/resources/atlassian-rovo-exfiltrates-data)

### Inferences
- The projection-from-structure pattern is common to the most credible cases, with Markdown serving as the delivery format and not necessarily the system of record.
- JSON sidecars as a named pattern did not appear in any first-party case I found. CALM's JSON is the source and not a sidecar.

### Gaps
- I found no first-party results for Glean, the Notion MCP server or the Confluence MCP server, despite targeted searches. This absence is a limit of this search and does not prove that no such results exist.
- I found no controlled comparison of Markdown with frontmatter against plain Markdown or JSON from a named organisation.

## Regulated and financial sector: what have banks, exchanges, asset managers and FINOS published?

### Takeaway
Morgan Stanley and FINOS's CALM is the only substantial first-party financial sector case I found, and it graduated at FINOS in October 2026. Evidence from other institutions is thin, with Fidelity as the only other named adopter, and its promised account was still under review at that time.

### Cited Findings
**CALM and Morgan Stanley**
- **Release (August 2025):** Morgan Stanley open-sourced CALM v1.0 through FINOS. [Search only] — [Banking Dive](https://www.bankingdive.com/news/morgan-stanley-open-source-software-development-finos-calm/758406/); [DevOps.com](https://devops.com/morgan-stanley-open-sources-calm-the-architecture-as-code-solution-transforming-enterprise-devops)
- **Graduation (issue opened 2 October 2026, approved 7 October, closed 8 October):** The proposal claims five or more adopting organisations, at least three of them in financial services, with Morgan Stanley and Fidelity Investments agreeing to be named. It cites about 28,000 CalmHub Docker pulls, 49,000 CLI npm downloads over a year, and 19 maintainers from 6 organisations. [Read] [Self-reported] — [FINOS issue 455](https://github.com/finos/community/issues/455)
- **Deployment figures to quote with care:** The same issue cites more than 1,400 internal deployments and more than 2,000 application deployments across several firms, drawing on an August 2025 CIO Dive article. The checklist boxes appear unchecked in the page I read, so graduation rests on the closing comment. [Read] — [FINOS issue 455](https://github.com/finos/community/issues/455)
- **QCon London 2026, Jim Gough and Andreea Niculcea (reported 19 March 2026):** CALM documents describe intended state as JSON. Patterns are organisational templates, deployment artefacts are generated from the single source, and the CALM CLI validates with Spectral rulesets, flagging such issues as missing security controls on relationships. CALM Hub is the "golden source" for deployments. [Read] — [InfoQ](https://www.infoq.com/news/2026/03/morgan-stanley-apis-mcp-calm/)
- **Reported result:** The first API took about two years to reach production, and with CALM and automated security approvals this drops to one or two weeks. The team manages more than a hundred deployments. [Read] [Self-reported at a conference] — [InfoQ](https://www.infoq.com/news/2026/03/morgan-stanley-apis-mcp-calm/)
- **Control enforced against an agent:** In a demo, a denied-symbols list was defined in CALM configuration and enforced at deployment, and Claude received a hard rejection when it queried a restricted symbol. This was a demo and not a production measurement. [Read] — [InfoQ](https://www.infoq.com/news/2026/03/morgan-stanley-apis-mcp-calm/)
- **Reported costs:** Overlapping tool descriptions cause retries and wasted tokens as tools grow to dozens, chatty agents raise costs, and developers give up some flexibility in wiring systems together. [Read] — [InfoQ](https://www.infoq.com/news/2026/03/morgan-stanley-apis-mcp-calm/)

**FINOS AI governance**
- **AIGF v2.0 (12 November 2025):** The framework adds a dedicated agentic risk catalogue covering prompt injection and memory poisoning, persistent agent compromise, chain-of-thought leakage and supply-chain tampering, and is cross-referenced to OWASP, MITRE and the EU AI Act. [Read] — [FINOS blog](https://www.finos.org/blog/finos-ai-governance-framework-v2.0-addressing-agentic-ai-risks-in-a-rapidly-evolving-landscape)
- **Inconsistent counts:** The post gives 30 risks in v1.0, 46 in v2.0 and six new pairs, and these do not reconcile. It names no banks. CALM integration for machine-readable control mappings was described as planned. — [FINOS blog](https://www.finos.org/blog/finos-ai-governance-framework-v2.0-addressing-agentic-ai-risks-in-a-rapidly-evolving-landscape)
- **Governance as code:** FINOS's page lists machine-readable compliance specifications and automated policy validation as components, but it does not name a format or an adopter. It reports training for "100+ FSI AI Leaders" in 2026. [Read] — [FINOS governance as code](https://ai.finos.org/governance-as-code/)
- **AIGF certification pipeline:** A FINOS Labs project describes turning mitigations into machine-configurable controls with predefined success criteria. [Search only] — [FINOS Labs](https://github.com/finos-labs/aigf-certification-pipeline)
- **FSB submission (5 August 2026):** FINOS says deployed systems often diverge from approved designs and that coding agents amplify this risk. It says CALM's versioned patterns let firms validate deployed code against approved architecture, and that its AI Reference Architecture working group has codified AI architectures in CALM with AIGF risks and mitigations. It names Moderne's Prethink as a vendor use of CALM. [Read] [Advocacy] — [FINOS response to FSB](https://www.fsb.org/uploads/FINOS.pdf)

### Inferences
- The financial sector case differs from the developer tool cases because the structured artefact is the object that receives approval. Format is driven by audit and governance needs, and agent readability is a secondary benefit.
- The denied-symbols demo illustrates a useful distinction. The control is enforced at the deployed gateway and not by asking the model to obey a document.
- Adoption beyond Morgan Stanley remains largely unproven in public, since the "five or more" figure includes unnamed organisations and the evidence is private to the FINOS Technical Oversight Committee.

### Gaps
- I found no first-party publications from exchanges or asset managers on machine-readable controls for agents, other than Fidelity's being named. Its blog was still pending as of the issue.
- I found no published per-bank accounts of AIGF use, and no named bank contributors in the pages read.
- I found no production results for AIGF controls deployed as runtime defences.
- I did not investigate regulators' own machine-readable rulebook projects.

## What are the reported failures and retreats?

### Takeaway
The clearest documented retreats are OpenAI's abandoned giant AGENTS.md and FedRAMP's narrowed mandate, and the strongest empirical challenge is the ETH finding on cost without success gains. Prompt injection through documents has gone from a research concern to documented attacks on mainstream tools, and I found no documented retreat from llms.txt despite its weak traffic evidence.

### Cited Findings
**Overly long or redundant context**
- OpenAI tried a single large AGENTS.md and replaced it, for the reasons listed earlier. [Read through reproduction] — [Reproduction on BitTide](https://bittide.aicompass.dev/article/3c74af4d-2842-4a43-8daf-ec9d37b2e1ba)
- ETH found that context files add about 20% or more inference cost with no significant success gain, and that repository overviews do not help navigation. [Read] — [arXiv HTML](https://arxiv.org/html/2602.11988)
- A contrary result comes from McMillan's factorial study, which found no detectable effect of file size on adherence to a trivial annotation. [Read, abstract only] — [arXiv](https://arxiv.org/abs/2605.10039)
- Uber reports tool sprawl consuming context before agents do any work, and duplication among skills. [Vendor summary] — [Port newsletter](https://newsletter.port.io/p/how-uber-built-a-software-factory)
- Morgan Stanley reports tool disambiguation problems beyond a handful of tools. [Read] — [InfoQ](https://www.infoq.com/news/2026/03/morgan-stanley-apis-mcp-calm/)

**Stale documents**
- OpenAI reports that outdated rules accumulate and that agents cannot tell which remain true. — [Reproduction on BitTide](https://bittide.aicompass.dev/article/3c74af4d-2842-4a43-8daf-ec9d37b2e1ba)
- Cloudflare warns that a stale AGENTS.md can be worse than none. This is a statement of judgement, and no measurement is attached. [Read] — [Cloudflare blog](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- Morgan Stanley's speakers present stale architecture diagrams as a problem CALM addresses by reporting what is actually deployed. [Read] — [InfoQ](https://www.infoq.com/news/2026/03/morgan-stanley-apis-mcp-calm/)

**Prompt injection through documents**
- **Atlassian Rovo, PromptArmor (5 August 2026):** A hidden injection in an uploaded file such as a "Backlog Guide" could cause Rovo to append Jira and Confluence data to an attacker URL without human approval. Disabling web search did not remove the URL tool, and Markdown image rendering provided a second channel. [Read] [Security vendor research] — [PromptArmor](https://www.promptarmor.com/resources/atlassian-rovo-exfiltrates-data)
- **Disclosure status in that report:** PromptArmor disclosed on 23 May 2026 and reported no fix at publication. Other sources report that Atlassian fixed a separate Varonis-reported issue, "RovoBlast", on 8 July 2026, so the two should not be merged. [Search only for the second] — [PromptArmor](https://www.promptarmor.com/resources/atlassian-rovo-exfiltrates-data); [CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-atlassian-rovo-prompt-injection-20260814-c/)
- **Atlassian MCP (June 2025):** Simon Willison describes an attack in which a malicious support ticket is processed with internal privileges and data leaves through a public reply, an instance of private data, untrusted content and external communication combined. [Search only] — [Simon Willison](https://simonwillison.net/2025/Jun/19/atlassian-prompt-injection-mcp)
- **OpenAI Codex CLI, Backslash Security (6 July 2026):** A malicious AGENTS.md could direct Codex in non-interactive `exec` mode to copy credential files. Backslash reports that the specific payload is now blocked, and argues the underlying mode-dependent gating remains. No disclosure timeline or OpenAI response is given. [Read] [Security vendor research] — [Backslash](https://www.backslash.security/blog/openai-codex-injection-in-agents-md-exfiltrating-credentials)
- **Cloud Security Alliance (17 March 2026):** A research note covers repository files hijacking coding assistants, including that GitHub Copilot includes AGENTS.md automatically. [Search only] — [CSA note](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/03/CSA_research_note_readme_instruction_injection_ai_coding_agents_20260317-csa-styled.pdf)
- **Rules File Backdoor (2025):** Pillar Security's hidden-Unicode attack on Cursor and Copilot rule files is known here only through secondary compilations, one of which says GitHub added hidden-Unicode warnings in May 2025. [Search only] — [Compiled reference](https://gist.github.com/kibotu/c06f54d6fbc4705e886a50fb2e59e6ae)

**Abandoned or narrowed formats and mandates**
- FedRAMP narrowed its machine-readable mandate and moved dates to 2027, as described above, and retired DOCX and XLSX at the same time. [Read] — [FedRAMP NTC-0009](https://www.fedramp.gov/notices/0009/)
- Google Search ignores llms.txt, and John Mueller reportedly compared the file to the keywords meta tag. [Secondary] — [Ahrefs](https://ahrefs.com/blog/what-is-llms-txt/), via [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)
- Chrome's Lighthouse audit does check for llms.txt but treats a 404 as not applicable. This keeps the format in use while not requiring it. [Secondary] — [Chrome for Developers](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt), via [agentexperience.tech](https://agentexperience.tech/insights/state-of-llms-txt/)

### Inferences
- Agents following instructions well is both the benefit and the attack surface. ETH shows strong adherence to named tools, and the Backslash result depends on that same adherence.
- Knowledge platforms widen the exposure compared with a reviewed repository file, because they mix untrusted content with broad read access. The Rovo case demonstrates this, while the repository cases need a malicious file to reach a clone.
- Vendor security research should be treated as credible but incomplete, since these publishers sell defences and report only their own side of the disclosure.

### Gaps
- I found no measured study showing how often stale documents mislead agents in production. The available statements are expert judgement.
- I found no organisation publicly announcing that it removed llms.txt or an MCP documentation server.
- The 90%+ success figure for a malicious AGENTS.md attributed to Forever Security reached me only through a DEV Community article, so it should not be used without the primary source.
- I did not confirm CVE details for any issue in this section, and CVE claims should be checked at NVD.
- Mintlify's security incidents (March 2024 and November 2025) were seen in search results but concern platform security and not document-borne injection, so they are out of scope. — [Mintlify incident post](https://mintlify.com/blog/incident-march-13)
