# Code intelligence tools market: evidence, analyst coverage, pricing, security and financial-services adoption (as of November 2026)

Labelling convention used below: **[Vendor claim]** means the statement comes from the vendor or its marketing; **[Independent]** means peer-reviewed or preprint research, analyst work reported by a third party, or established press; **[Aggregator]** means a low-authority secondary site whose figure should be checked before reuse.

## 1. Independent benchmarks: embeddings vs symbol/graph indexes vs agentic grep

### Takeaway
The only large, vendor-neutral benchmark that measures retrieval quality inside coding agents (ContextBench, Feb 2026) finds that elaborate retrieval scaffolding gives marginal gains over a plain bash/grep agent, that all agents favour recall over precision, and that the backbone model matters as much as the retrieval method. Evidence on embeddings vs grep is mixed: grep is competitive on small-to-medium repositories with distinctive identifiers, while embeddings help with natural-language queries; most "grep wins" and "embeddings win" claims come from vendors or small experiments.

### Cited Findings
- **ContextBench** (arXiv 2602.05892, submitted 5 Feb 2026, v3 11 Feb 2026) contains 1,136 issue-resolution tasks from 66 repositories in 8 languages, and measures recall, precision and F1 of retrieved context at file, block and line granularity, plus redundancy and efficiency. [Independent] — [arXiv](https://arxiv.org/html/2602.05892); [GitHub/leaderboard](https://github.com/euniai/contextbench)
- ContextBench evaluates four LLMs (GPT-5, Claude Sonnet 4.5, Gemini 2.5 Pro, Devstral 2) and five agents (mini-SWE-agent, SWE-agent, OpenHands, Agentless, Prometheus). The agents represent distinct retrieval styles: mini-SWE-agent uses plain bash commands, Agentless uses embedding-based semantic retrieval, SWE-agent and OpenHands use file-navigation interfaces, and Prometheus uses graph-based repository retrieval. [Independent] — [arXiv](https://arxiv.org/html/2602.05892)
- On ContextBench Lite (500 tasks, GPT-5 backbone), the simplest agent, mini-SWE-agent (bash only), had the highest file-level F1 (0.634) and block-level F1 (0.375) and the highest line-level recall (0.606), with Pass@1 0.472. [Independent] — [arXiv](https://arxiv.org/html/2602.05892)
- On the same setup, the graph-based Prometheus had the highest Pass@1 (0.512) but low file-level precision (0.336); SWE-agent and OpenHands had the highest file recall (0.726 and 0.733) at much lower precision (0.537 and 0.400). [Independent] — [arXiv](https://arxiv.org/html/2602.05892)
- The embedding-based Agentless had the lowest file-level recall (0.609) but the highest line-level F1 (0.376), and Pass@1 0.452. The paper does not isolate retrieval method as a variable beyond these numbers. [Independent] — [arXiv](https://arxiv.org/html/2602.05892)
- Holding the agent fixed (mini-SWE-agent), changing the model moved Pass@1 from 0.364 (Gemini 2.5 Pro) to 0.530 (Claude Sonnet 4.5). Claude Sonnet 4.5 took 14.38 steps per task at about $0.76; GPT-5 took 5.87 steps at about $0.45 while reading about 119 lines per step. [Independent] — [arXiv](https://arxiv.org/html/2602.05892)
- The authors report that agents frequently inspect relevant code but do not use it in the final patch, and that LLMs favour recall over precision, pulling in noise. [Independent] — [arXiv](https://arxiv.org/html/2602.05892)
- "Is Grep All You Need? How Agent Harnesses Reshape Agentic Search" (arXiv 2605.15184, May 2026) finds that with inline delivery, grep beat vector retrieval for every harness–model pair tested, but the crossover depended on harness and backbone, and delivering results via files or some vendor CLIs erased or reversed the lead. The corpus was LongMemEval conversational memory, not code. [Independent] — [arXiv](https://arxiv.org/html/2605.15184v1)
- "Deep Agentic Search for Repository-Level Code Question Answering: An Empirical Study" (arXiv 2608.01507, 2026) exists as a further code-specific study; I did not read its results. [Independent] — [arXiv](https://arxiv.org/pdf/2608.01507)
- An account of Augment's SWE-bench agent work reports that "grep and find were sufficient" for SWE-bench, attributing this to small repositories and distinctive keywords, which limits transfer to large enterprise monorepos. [Vendor-adjacent practitioner write-up, Sept 2025] — [Jason Liu](https://jxnl.co/writing/2025/09/11/why-grep-beat-embeddings-in-our-swe-bench-agent-lessons-from-augment/)
- Cursor has reported that its agents answered 12.5% more questions correctly with an embedding (semantic) index than without it. [Vendor claim, reported secondhand] — [Dbggr summary](https://dbggr.dev/articles/embeddings-vs-grep-agentic-search/)
- A practitioner replay on Django commits found grep located the right file within three rounds 75% of the time when the request named the code and 45% when it was plain English; a small embedding model did better on both, the two missed different files, and combining them reached 94% and 87%. [Practitioner experiment, not peer reviewed] — [DEV Community](https://dev.to/theaicommit/how-a-coding-agent-finds-code-grep-versus-an-embedding-index-2cpl)
- A small GitHub experiment claims embeddings were about 35% cheaper than grep for agent memory because of fewer round trips. [Unreviewed experiment] — [GitHub](https://github.com/henry-dowling/embedding-vs-grep-experiment)
- Background benchmarks that pre-date agentic retrieval and are commonly cited: SWE-bench (end-to-end issue resolution, 2023) — [arXiv 2310.06770](https://arxiv.org/abs/2310.06770); RepoBench (repository-level completion with a retrieval sub-task, 2023) — [arXiv 2306.03091](https://arxiv.org/abs/2306.03091); CodeRAG-Bench (retrieval-augmented code generation, 2024) — [arXiv 2406.14497](https://arxiv.org/abs/2406.14497). [Independent; not re-read for this note]

### Inferences
- No independent benchmark directly compares commercial code-intelligence products (Sourcegraph, Augment Context Engine, Copilot indexing, Greptile, Tabnine Context Engine) on the same tasks; vendor comparisons of these products should be treated as marketing.
- ContextBench suggests that, for SWE-bench-scale repositories, retrieval architecture is a second-order variable behind model choice. Whether that holds for multi-million-line enterprise monorepos is untested by independent work.
- The most defensible position for a buyer is that grep and embeddings are complementary, which matches the hybrid designs most vendors now ship.

### Gaps
- I found no vendor-neutral bake-off of commercial context engines on enterprise-scale (multi-repo, >10M LOC) codebases.
- I did not verify LongCodeBench, CTXbench or SWE-bench Pro/Multi details in this pass; they should be checked by another source before citing.
- No independent study evaluates SCIP/LSIF-style symbol indexes (Sourcegraph, Serena via LSP) against grep for agents; Prometheus (graph retrieval) is the closest proxy.

## 2. Analyst coverage (Gartner, Forrester, IDC)

### Takeaway
Gartner renamed its category from "AI Code Assistants" (2024, 2025) to "Enterprise AI Coding Agents" (May 2026). The 2026 Leaders are Anthropic, Cursor, GitHub and OpenAI; AWS, Google and Cognition fell to Challengers, Tabnine was the only Visionary, and GitLab was not placed. Pure code-intelligence vendors (Sourcegraph, Augment, Qodo, Greptile, Moderne) do not appear in either Magic Quadrant according to the coverage found.

### Cited Findings
- 2025 Gartner Magic Quadrant for AI Code Assistants (published around 17 Sept 2025): Leaders were GitHub (second year), Amazon, Cognition (Windsurf), GitLab (second year) and Google Cloud. [Vendor announcements and trade press] — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/gartner-positions-github-as-a-leader-in-the-2025-magic-quadrant-for-ai-code-assistants-for-the-second-year-in-a-row/); [GitLab press release](https://about.gitlab.com/press/releases/2025-09-17-gitlab-named-a-leader-in-gartner-magic-quadrant-ai-code-assistants/); [Cognition](https://devin.ai/blog/gartner-windsurf-cognition-magic-quadrant-ai-coding-assistants); [AWS Insider](https://awsinsider.net/articles/2025/09/22/amazon-repeats-as-a-leader-in-ai-code-assistants-report.aspx)
- Secondary coverage of the 2025 report places Anysphere (Cursor), Alibaba, Tabnine, IBM and JetBrains outside the Leaders quadrant; exact quadrants were not confirmed from Gartner. [Secondary] — [search coverage via AWS Insider](https://awsinsider.net/articles/2025/09/22/amazon-repeats-as-a-leader-in-ai-code-assistants-report.aspx)
- 2026 Gartner Magic Quadrant for Enterprise AI Coding Agents (published 20 May 2026): Leaders Anthropic, Cursor, GitHub, OpenAI; Challengers AWS, Google, Alibaba Cloud, Cognition; Visionary Tabnine (only one); Niche Players Atlassian, BytePlus, JetBrains. GitLab was not placed. [Trade press] — [Virtualization Review, 5 Jun 2026](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)
- Gartner's 2026 mandatory features reportedly include native MCP support, human review and approval of changes, traceability and auditability, and enterprise data protection; evaluation emphasised autonomous task execution, context awareness, verification and governed operation. [Trade press] — [Virtualization Review](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)
- GitHub says it was a Leader for the third consecutive year and placed highest on Ability to Execute; Cursor says it was placed furthest on Completeness of Vision. [Vendor claims] — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/github-recognized-as-a-leader-in-the-gartner-magic-quadrant-for-enterprise-ai-coding-agents-for-the-third-year-in-a-row/); [Cursor blog](https://cursor.com/blog/cursor-leads-gartner-mq-2026); [OpenAI](https://openai.com/index/gartner-2026-agentic-coding-leader/)

### Inferences
- The category shift from "assistants" to "agents" means Gartner now scores agent execution and governance rather than retrieval quality; code-intelligence depth (cross-repo search, symbol graphs) is assessed only indirectly under "context awareness".
- Tabnine's Visionary placement in May 2026 preceded its acquisition by Tricentis in July 2026, which may change its roadmap (see section 3).

### Gaps
- I found no Forrester Wave or IDC MarketScape specific to code intelligence or AI coding agents in 2025–2026 in this pass.
- The Gartner reports themselves were not accessed; placements rely on vendor posts and trade press.

## 3. Market events 2025–2026

### Takeaway
The market consolidated around agent vendors: Google licensed Windsurf technology and hired its CEO, Cognition bought the rest of Windsurf and later retired the brand, Tricentis bought Tabnine, Sourcegraph shut down self-serve Cody in favour of Amp, and valuations for Cursor, Cognition and Greptile rose sharply.

### Cited Findings
- **Windsurf / Google / Cognition (July 2025):** Google hired Windsurf's CEO in a reported $2.4B licensing deal; days later Cognition agreed to acquire Windsurf's IP, product, brand and remaining team, terms undisclosed. [Independent press] — [CNBC, 14 Jul 2025](https://www.cnbc.com/2025/07/14/cognition-to-buy-ai-startup-windsurf-days-after-google-poached-ceo.html)
- **Cognition funding:** Cognition raised $400M at a $10.2B valuation in September 2025, led by Founders Fund. [Independent press] — [CNBC, 8 Sep 2025](https://www.cnbc.com/2025/09/08/cognition-valued-at-10point2-billion-two-months-after-windsurf-.html); [VentureBeat](https://venturebeat.com/programming-development/cognition-follows-windsurf-acquisition-with-usd400m-fundraise-showing-strong). A later $1B Series D (27 May 2026) is reported only by an aggregator. [Aggregator] — [Tracxn](https://tracxn.com/d/companies/cognition/__A-LTT9JRh_QNtJP-fH1fyGNlIUA_Bt9UIx3qnfFr1w0)
- **Windsurf brand retired:** From 2 June 2026 the Windsurf editor was renamed Devin Desktop, and the old Windsurf version reached end of life on 1 July 2026. [Aggregator; verify with Cognition] — [webauditos](https://webauditos.com/guides/windsurf)
- **Tabnine acquired by Tricentis (30 July 2026):** Tricentis will fold Tabnine's Enterprise Context Engine into its agentic quality engineering platform; terms were not disclosed. Calcalist reports a price in the tens of millions of dollars, while one aggregator claims $500M, which is unverified. [Independent press + conflict] — [Business Wire](https://secure.businesswire.com/news/home/20260730388427/en/Tricentis-Acquires-Tabnine-to-Further-Scale-Agentic-Quality-Engineering-for-the-Enterprise); [Calcalist](https://www.calcalistech.com/ctechnews/article/1o1nf7vd3); [Futurum](https://futurumgroup.com/insights/tabnines-acquisition-by-tricentis-a-strategic-move-for-agentic-quality-engineering/); [BriefGlance ($500M claim)](https://briefglance.com/companies/tricentis/pulses/64176)
- Commentary notes that buyers who chose Tabnine for its air-gapped coding assistant face roadmap risk, because Tricentis bought the context engine for testing agents. [Opinion] — [beri.net](https://www.beri.net/article/tricentis-tabnine-acquisition-air-gapped-coding-assistant-roadmap-risk)
- **Sourcegraph Cody (July 2025):** Cody Free, Cody Pro and Enterprise Starter were discontinued effective 23 July 2025, with Sourcegraph's agentic product Amp as the successor; only Cody Enterprise remains for existing enterprise customers. [Encyclopedic secondary] — [Wikipedia](https://en.wikipedia.org/wiki/Sourcegraph)
- **Cursor (Anysphere):** $900M Series C at $9.9B post-money (June 2025), then $2.3B at $29.3B post-money (November 2025); later reports say it sought about $2B at a pre-money valuation above $50B. [Encyclopedic + press] — [Wikipedia](https://en.wikipedia.org/wiki/Cursor_(company)); [Yahoo Finance](https://finance.yahoo.com/sectors/technology/articles/ai-coding-startup-cursor-seeks-115735149.html)
- **Qodo:** $70M Series B in March 2026 led by Qumra Capital, total funding $120M. [Encyclopedic secondary] — [Wikipedia](https://en.wikipedia.org/wiki/Qodo)
- **Greptile:** $50M Series B at a $750M valuation led by Menlo Ventures, announced 19 Oct 2026, after a Benchmark-led Series A (~$25M, reported $180M valuation; dating conflicts between 2025 and 2026). [Secondary; vendor announcement on X] — [llms.blog](https://www.llms.blog/posts/greptile-raises-50m-at-a-750m-valuation-what-the-ai-code-reviewer-does-and-what-it-costs); [AGTP on X](https://x.com/AGTPinsights/status/2112238859761463510)
- **Moderne:** $30M Series B in February 2025 led by Acrew Capital, with Morgan Stanley, Amex Ventures and TIAA Ventures participating; total raised $50M; customer base grew 250% in 2024. [Vendor press release] — [fintech.global](https://fintech.global/2025/02/12/moderne-raises-30m-series-b-to-accelerate-ai-powered-code-transformation/); [Intel Capital](https://www.intelcapital.com/moderne-secures-30m-to-drive-billions-in-enterprise-code-modernization-savings-based-on-its-innovative-tech-used-by-aws-microsoft-and-broadcom-ai-assistants/)
- **Augment:** An aggregator lists Augment as Series B with about $252M raised; I found no confirmed 2025–2026 round. [Aggregator] — [Tracxn via search](https://tracxn.com/d/companies/cognition/__A-LTT9JRh_QNtJP-fH1fyGNlIUA_Bt9UIx3qnfFr1w0)

### Inferences
- Standalone code-intelligence vendors are being absorbed or repositioned: Tabnine into testing, Windsurf into Devin, Sourcegraph from Cody to Amp. Buyers should treat roadmap continuity as a selection criterion.
- Financial-institution venture arms (Morgan Stanley, Amex Ventures, TIAA) investing in Moderne is a signal of interest in large-scale code migration in the sector.

### Gaps
- Augment funding, Serena (open-source, no company funding events found) and any shutdowns beyond Cody self-serve were not confirmed.

## 4. Pricing models with real numbers

### Takeaway
The market moved from flat per-seat pricing to per-seat plus metered usage during 2025–2026. GitHub moved Copilot from premium-request allowances (June 2025) to token-priced AI Credits (June 2026), Augment moved to credit pools (October 2025), and Cursor moved to usage-based pricing (June 2025). Code-modernisation and code-search platforms (Sourcegraph, Moderne) remain sales-led enterprise contracts with little public pricing.

### Cited Findings
- **GitHub Copilot (2025):** Business $19 per user per month with 300 premium requests; Enterprise $39 per user per month with 1,000; overage $0.04 per premium request, enforcement starting June 2025. [Independent press] — [The Register, 20 Jun 2025](https://www.theregister.com/2025/06/20/github_begins_enforcing_premium_request/); [ITPro](https://www.itpro.com/software/development/github-copilot-pricing-changes-premium-requests)
- **GitHub Copilot (June 2026):** Premium requests were replaced by token-priced GitHub AI Credits on 1 June 2026, with 1 credit = $0.01 and Business reportedly receiving 1,900 pooled credits per user; the change drew developer complaints about cost predictability and annual-plan refunds. [Aggregators; verify on GitHub pricing page] — [tech-insider](https://tech-insider.org/ie/github-copilot-ai-credits-pricing-2026/); [letsdatascience](https://letsdatascience.com/blog/github-copilot-usage-based-billing-developer-backlash); [heise](https://heise.de/-10511480)
- **Augment Code (20 Oct 2025):** Moved from message limits to monthly credit pools: 40,000 credits (Indie), 130,000 (Standard), 450,000 (Max), custom Enterprise; new Enterprise customers and renewals move to credits. Third parties report $20, $60 and $200 per month for Indie/Standard/Max. [Vendor announcement; prices from third parties] — [Augment blog](https://www.augmentcode.com/blog/augment-codes-pricing-is-changing)
- **Cursor:** Dropped flat-rate plans for usage-based pricing in June 2025. [Secondary] — [heise](https://heise.de/-10511480)
- **Sourcegraph:** Cody Enterprise is reported at $59 per user per month on annual contract, while other sources say Sourcegraph Enterprise is sales-only from about $16K with AI credits; the figures conflict. [Aggregators] — [usagepricing](https://www.usagepricing.com/blueprint/sourcegraph-cody); [devtune](https://devtune.ai/verticals/ai-code-review-and-code-quality/sourcegraph/pricing)
- **AI code review (Greptile, Qodo, CodeRabbit):** Seat prices are reported in the range of $24 to $72 per seat per month across CodeRabbit and rivals. [Aggregator] — [shattered.io](https://shattered.io/coderabbit-pricing-vs-greptile-qodo-bugbot-copilot-2026/)

### Inferences
- For a bank with thousands of developers, metered credits make total cost dependent on agent usage patterns; budget controls and per-user caps become procurement requirements.
- Per-repo or per-LOC pricing is not visible publicly for any vendor found; Moderne and Sourcegraph pricing is negotiated.

### Gaps
- No official current list prices were retrieved for Sourcegraph, Moderne, Tabnine (post-acquisition), Qodo, Greptile or Devin; aggregator numbers should be checked against vendor pages.

## 5. Security and compliance

### Takeaway
Certification claims (SOC 2 Type II, ISO 42001, CMEK, air-gap) are mostly vendor-asserted and should be verified against reports. The material incident class in 2025–2026 is MCP and agent configuration abuse: repo-controlled MCP configs that auto-execute, and prompt injection that exfiltrates private repository content through connected tools.

### Cited Findings
- **Augment:** Claims ISO/IEC 42001 certification (August 2025, via Coalfire) as the first AI coding assistant, SOC 2 Type II (July 2024) and customer-managed encryption keys. [Vendor claim] — [Augment blog](https://www.augmentcode.com/blog/augment-code-is-the-first-ai-coding-assistant-to-be-iso-iec-42001-certified); [Augment security](https://augmentcode.com/security)
- **Cursor CVE-2025-54136 ("MCPoison", CVSS 7.2):** An attacker could modify an MCP configuration after a user had approved it, so a benign config in a shared repo could later run malicious commands; fixed in Cursor 1.3. [Independent security research, Check Point] — [The Hacker News, Aug 2025](https://thehackernews.com/2025/08/cursor-ai-code-editor-vulnerability.html); [Tenable](https://www.tenable.com/cve/CVE-2025-54136)
- **Cursor CVE-2025-54135 ("CurXecute"):** Prompt injection via a connected Slack MCP server could create a sensitive MCP file without approval and achieve code execution; fixed in Cursor 1.3 (29 Jul 2025). [Independent] — [SC World](https://www.scworld.com/news/cursor-flaw-risks-rce-from-prompt-injections-on-mcp-server-researchers-say); [SecurityWeek](https://www.securityweek.com/several-vulnerabilities-patched-in-ai-code-editor-cursor/)
- **Cursor CLI CVE-2025-64109:** Opening a cloned project in the Cursor CLI beta immediately ran a malicious MCP server command without warning. [CVE database] — [ocve](https://ocve.arawa.fr/cve/CVE-2025-64109)
- **GitHub MCP private-repo leak (May 2025, Invariant Labs):** A malicious issue on a public repository could steer an agent using the GitHub MCP server to copy private-repository data into a public pull request; this is an architecture-level data-leak pattern rather than a single patched bug. [Independent research, secondary coverage] — [Tessl](https://tessl.io/blog/malicious-github-issue-ai-agent-leak/); [HackerNoon](https://hackernoon.com/the-github-issue-that-could-hijack-your-ai-agent)
- A Cloud Security Alliance research note (29 Jun 2026) lists repo-controlled MCP auto-execution issues across assistants, including CVE-2025-59536 (CVSS 8.7) and CVE-2026-21852 (CVSS 5.3) in Claude Code and CVE-2026-12957 (CVSS 8.5) in Amazon Q Developer, all reported as patched. [Independent] — [CSA note (PDF)](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/06/CSA_research_note_mcp_ai_coding_assistant_credential_theft_20260629-csa-styled.pdf)
- Gartner made native MCP support, human approval of changes, auditability and enterprise data protection mandatory for its 2026 Magic Quadrant. [Trade press] — [Virtualization Review](https://virtualizationreview.com/articles/2026/06/05/ai-firms-push-cloud-giants-from-leaders-quadrant-in-gartner-ai-coding-report.aspx)

### Inferences
- The risk surface of a code-intelligence tool is now the agent plus its connectors, not only the index; controls such as MCP allow-lists, read-only tokens scoped per repository, and disabling workspace-level MCP auto-load matter more than the vendor's certificate list.
- No public incident was found in which a vendor's hosted code index itself leaked customer code.

### Gaps
- I did not retrieve trust-centre pages for Sourcegraph, Qodo, Greptile, Moderne, Tabnine or Cognition, nor training/retention policies; these need direct verification.
- On-prem/air-gap availability was not verified per vendor in this pass beyond commentary on Tabnine.

## 6. Adoption in banks, exchanges and asset managers; regulatory considerations

### Takeaway
Large banks publicly report broad rollouts of coding assistants (Citi with GitHub Copilot to 30,000–40,000 developers, JPMorgan with an in-house assistant, Goldman with its own Developer Copilot plus Cognition's Devin), with self-reported productivity gains of 5–20%. Dedicated code-intelligence vendors are visible mainly through fintech case studies (Sourcegraph at SoFi, Coinbase, FactSet, Neo Financial) and Moderne's unnamed "five leading North American banks". Regulators treat AI coding vendors under existing third-party and ICT risk frameworks rather than specific rules.

### Cited Findings
- **Citi:** CEO Jane Fraser described equipping 30,000 developers with generative AI coding tools (early 2025); later coverage describes agentic AI rolling out to 40,000 developers. CTO David Griffiths estimated that regular GitHub Copilot users gain 5–15% productivity. [Independent press, executive claims] — [Yahoo Finance](https://finance.yahoo.com/news/citi-deploys-ai-coding-tools-152606091.html); [American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers); [American Banker (earlier)](https://americanbanker.com/news/why-citi-is-rolling-out-generative-ai-to-all-its-developers)
- **JPMorgan:** Tens of thousands of engineers raised productivity 10–20% using a coding assistant developed by the bank, per global CIO Lori Beer (Reuters, 14 Mar 2025). This is an in-house tool, not Copilot. [Independent press, executive claim] — [Yahoo Finance/Reuters](https://finance.yahoo.com/news/jpmorgan-engineers-efficiency-jumps-much-190410471.html)
- **Goldman Sachs:** Deployed Cognition's Devin in 2025 alongside its roughly 12,000 developers, with the CIO describing plans to scale to hundreds or thousands of instances; Goldman also runs an internal AI Developer Copilot in VS Code and JetBrains. [Press; some figures from single sources] — [Quartz](https://qz.com/goldman-sachs-ai-coder-devin-cognition); [NCFA](https://ncfacanada.org/goldman-sachs-deploys-agentic-ai-engineer-devin/)
- **Bank of America:** Reported 18,000 developers using coding agents with about 20% gains. [Consultancy compilation; text partly garbled] — [Keyhole Software PDF](https://keyholesoftware.com/wp-content/uploads/Keyhole-Guide-Coding-Faster-Wont-Save-the-Bank.pdf)
- **Sourcegraph in financial services:** Case studies cover SoFi (hundreds of microservices), Coinbase, Neo Financial and FactSet (code search across 12,000+ repositories during a Perforce-to-GitHub migration). [Vendor case studies] — [Sourcegraph case studies](https://sourcegraph.com/case-studies); [SoFi](https://testwww.sourcegraph.com/case-studies/sofi-moves-fast-on-hundreds-of-microservices)
- **Moderne:** Serves five leading North American banks (unnamed) alongside Allstate, Choice Hotels and Walmart; Morgan Stanley, Amex Ventures and TIAA Ventures invested. [Vendor press release] — [fintech.global](https://fintech.global/2025/02/12/moderne-raises-30m-series-b-to-accelerate-ai-powered-code-transformation/)
- **EU DORA:** Guidance commentary treats LLM and model vendors as ICT third-party service providers under DORA; BaFin's non-binding January 2026 guidance places generative AI inside existing DORA governance and third-party frameworks; an ESA joint statement on frontier AI cyber risk (31 Jul 2026) reportedly asks firms to keep asset inventories that include AI/ML components. [Secondary summaries; primary texts not verified] — [bankingnewsai DORA](https://www.bankingnewsai.com/ai-regulation/guides/dora-explained); [airiskaware](https://airiskaware.com/insights/eu-banks-ai-governance-eba); [bankingnewsai regulation](https://www.bankingnewsai.com/agentic-banking/regulation)
- **US:** A summary states that the 2026 interagency model-risk guidance (SR 26-2 / OCC Bulletin 2026-13 / FDIC FIL-15-2026) carves generative and agentic AI out of scope, and that no US banking regulator had issued agent-specific rules by September 2026; a vendor blog contradicts this by claiming SR 11-7 was clarified to cover AI-generated code. NYDFS reportedly asked for human review of AI-generated code in May 2026. [Secondary, conflicting; verify primary documents] — [bankingnewsai](https://www.bankingnewsai.com/agentic-banking/regulation); contradicted by [IAN blog](https://iancloud.ai/blog/ai-code-remediation-financial-services-compliance-2026)

### Inferences
- In banks, the procurement path for code-intelligence tools runs through third-party risk management (DORA register of information in the EU, vendor due diligence in the US) rather than model-risk validation, unless the tool is used to generate code for models in scope.
- The concentration of public bank deployments on GitHub Copilot, in-house assistants and Devin suggests that specialist context engines are usually bought as add-ons to an approved assistant rather than as the primary tool.
- Acquisition events (Tabnine, Windsurf) are directly relevant to DORA exit-strategy and concentration-risk requirements.

### Gaps
- I found no public confirmation of which banks use Sourcegraph, Augment, Qodo, Greptile, Tabnine or Moderne by name, and no exchange or asset-manager deployments.
- Risk.net, Waters Technology and PRA/FINRA material on AI coding tools was not found in this pass.
- JPMorgan's use of GitHub Copilot is asserted only by a low-authority blog.
