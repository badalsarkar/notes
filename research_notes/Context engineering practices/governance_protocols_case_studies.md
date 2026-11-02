# Enterprise Context Engineering: Governance, Protocols and Case Studies (Financial Services Emphasis)

Research date: 2026-10-26. Sources are dated where the date was visible. Vendor case studies and press releases are labelled as claims; independently measured results are rare and are labelled when present.

## Model Context Protocol, A2A and governance bodies

### Takeaway
MCP has moved from a vendor protocol to a Linux Foundation project (under the Agentic AI Foundation, December 2025), and its 2026-07-28 revision makes the protocol stateless, deprecates Dynamic Client Registration in favour of Client ID Metadata Documents, and adds caching and tracing metadata that matter for enterprise gateways. A2A is a separate Linux Foundation project (since June 2025) for agent-to-agent delegation, and it is complementary to MCP's agent-to-tool/data role.

### Cited Findings
- The 2025-11-25 MCP revision added OpenID Connect Discovery 1.0 support for authorization server discovery, incremental scope consent via `WWW-Authenticate` (SEP-835), and Client ID Metadata Documents as a recommended client registration mechanism (SEP-991). — [MCP changelog 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/changelog)
- A later revision dated 2026-07-28 removed protocol-level sessions and the `Mcp-Session-Id` header from Streamable HTTP (SEP-2567), and removed the `initialize` handshake so that every request carries its protocol version and client capabilities in `_meta` (SEP-2575). — [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- The 2026-07-28 revision added a mandatory `server/discover` RPC, replaced server-initiated requests (sampling, elicitation, roots) with a Multi Round-Trip Request pattern (SEP-2322), and moved experimental tasks into an official extension `io.modelcontextprotocol/tasks` (SEP-2663). — [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- For enterprise operation, the same revision documented OpenTelemetry trace-context propagation in `_meta` (SEP-414), required `Mcp-Method` and `Mcp-Name` HTTP headers on POST requests so that intermediaries can route and filter without parsing bodies (SEP-2243), and required `ttlMs` and `cacheScope` (`public` or `private`) on list and read results (SEP-2549). — [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- The revision asks servers to return `tools/list` in deterministic order to improve LLM prompt-cache hit rates, which links protocol design directly to context-window cost. — [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- Authorization changes in 2026-07-28 include RFC 9207 `iss` validation in authorization responses (SEP-2468), binding persisted client credentials to the issuing authorization server (SEP-2352), and deprecation of OAuth 2.0 Dynamic Client Registration (RFC 7591) in favour of Client ID Metadata Documents (PR #2858). — [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- The 2026-07-28 revision deprecated the Roots, Sampling and Logging features (SEP-2577) and adopted a feature lifecycle policy with a minimum twelve-month deprecation window (SEP-2596). — [MCP changelog 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/changelog)
- Commentators disagree on the size of the 2026 authorization change: Descope describes it as mostly additive, while WorkOS describes it as a rewrite of how agent authentication works. — [Descope](https://www.descope.com/blog/post/july-2026-mcp-revision); [WorkOS](https://workos.com/blog/mcp-2026-spec-agent-authentication)
- The Linux Foundation announced the Agentic AI Foundation (AAIF) on 9 December 2025 with three founding projects: Anthropic's MCP, OpenAI's AGENTS.md and Block's goose. — [IT Brief](https://itbrief.com.au/story/linux-foundation-launches-agentic-ai-open-standards-hub); [Gend summary](https://www.gend.co/blog/openai-agentic-ai-foundation-linux)
- One secondary source reports that AAIF had more than 170 members by April 2026 and cites MCP at over 110 million monthly SDK downloads; I could not verify these figures against a primary source. — [IntuitionLabs](https://intuitionlabs.ai/articles/tags/aaif)
- The Linux Foundation launched the Agent2Agent (A2A) project on about 24–25 June 2025 after Google transferred the specification, SDKs and tooling, with AWS, Cisco, Google, Microsoft, Salesforce, SAP and ServiceNow as founding members. — [Help Net Security, 2025-06-24](https://www.helpnetsecurity.com/2025/06/24/the-linux-foundation-agent2agent/); [The Decoder](https://the-decoder.com/google-hands-off-agent2agent-protocol-to-linux-foundation-for-open-ai-agent-standard/)
- Secondary sources report that A2A reached v1.0 in April 2026 with Signed Agent Cards and an AP2 payments extension, and more than 150 supporting organizations; no primary release note was found. — [Alice Labs guide](https://alicelabs.ai/en/insights/a2a-protocol-guide-2026); [Let's Data Science](https://letsdatascience.com/news/a2a-solidifies-cross-vendor-agent-interoperability-53400ea4)
- Sources conflict on whether A2A sits inside AAIF or remains a separate Linux Foundation project; the AAIF launch list does not include A2A. — [Agentic AI docs](https://agentic-ai.readthedocs.io/en/latest/Standards/agentic-ai-foundation/); contradicted by [blckalpaca](https://blckalpaca.at/en/knowledge-base/ai-agents/a2a-protocol-basics/linux-foundation-aaif-bedeutung)
- MCP gateway vendors describe scanning tool descriptions at catalog time and holding flagged tools in a pending-review state until a human approves them; these are vendor claims without independent evaluation. — [TrueFoundry](https://truefoundry.com/blog/blog-mcp-tool-poisoning-gateway-defense)

### Inferences
- The stateless 2026-07-28 design, required routing headers, cache-scope fields and OpenTelemetry conventions are the protocol features an enterprise gateway needs to route, cache, audit and trace context delivery centrally, so the spec is converging on a gateway-mediated deployment model.
- Deprecating Dynamic Client Registration favours a model in which an enterprise identity provider controls which agent clients can obtain tokens, which suits banks that do not allow anonymous client registration.
- In practice, MCP covers how an agent obtains context and tools, while A2A covers how one agent delegates to another, so a bank would likely use both rather than choose between them.

### Gaps
- I did not fetch the official MCP Registry documentation, so its status (preview versus general availability), namespace verification and sub-registry model are not sourced here.
- I found no primary source on named enterprise MCP gateways from major vendors (for example Microsoft, AWS, Kong, Cloudflare) or their adoption in banks.
- The A2A v1.0 date and feature set need confirmation from the A2A project's own release notes.

## Security and governance of context, including financial services regulation

### Takeaway
Regulators have begun to address agents specifically: FINRA's 2026 oversight report (9 December 2025) names agent scope, auditability and sensitive-data retention as risks and expects prompt and output logs and model-version tracking. OWASP's Agentic Top 10 (9 December 2025) and the tool-poisoning literature show that retrieved context and tool metadata are an attack surface, and EU AI Act high-risk obligations have been provisionally deferred to December 2027.

### Cited Findings
- FINRA's 2026 Annual Regulatory Oversight Report, released 9 December 2025, contains a standalone generative AI section and is the first FINRA report to discuss AI agents. — [Debevoise, Dec 2025](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)
- FINRA states that agents "may take actions that exceed the user's actual or intended scope or authority," that "complex chains of agent actions may be difficult to reconstruct," and that "agents working with sensitive or proprietary data may unintentionally retain or reveal that information." — [Debevoise, Dec 2025](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)
- FINRA encourages firms to monitor agent system access and data handling, decide where human-in-the-loop review is required, track agent actions and decisions, and establish guardrails that constrain agent behaviour. — [Debevoise, Dec 2025](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)
- FINRA's monitoring guidance includes "maintaining prompt and output logs for accountability and troubleshooting" and "tracking which model version was used and when," and it reports that summarization remains the top observed GenAI use case among member firms. — [Debevoise, Dec 2025](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)
- FINRA treats its rules as technology-neutral and expects firms to update written supervisory procedures for their use of GenAI. — [DLA Piper, 19 Dec 2025](https://www.dlapiper.com/insights/publications/2025/12/finra-flags-generative-ai-risks-and-governance-expectations)
- OWASP published the Top 10 for Agentic Applications for 2026 on 9 December 2025, with risks labelled ASI01–ASI10 covering goal and planning manipulation, tool misuse, identity and privilege abuse, supply chain, code execution, memory and context poisoning, inter-agent communication, cascading failures, human–agent trust and rogue agents. — [OWASP GenAI](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026); [Modulos summary](https://docs.modulos.ai/frameworks/owasp-top-10-agentic)
- Cycode reports that the OWASP agentic list draws on 2025 incidents such as EchoLeak (CVE-2025-32711), a zero-click prompt injection in Microsoft 365 Copilot, and a coding agent deleting a production database during a code freeze. — [Cycode](https://cycode.com/blog/owasp-top-10-agentic-applications/)
- Tool poisoning places attacker instructions in an MCP tool's description rather than its output, and because descriptions load into context at initialization the injection persists across sessions until the server is removed. — [Speakeasy](https://www.speakeasy.com/resources/mcp-tool-poisoning); [Waxell, 2026](https://waxell.ai/blog/mcp-tool-description-poisoning-agent-data-leakage-2026)
- Under the EU Digital Omnibus provisional agreement of 7 May 2026, AI Act high-risk obligations for stand-alone Annex III systems are deferred to 2 December 2027 and those for Annex I product-embedded systems to 2 August 2028; Parliament voted to adopt on 16 June 2026, with Council approval still pending at the time of the source. — [Sidley, 22 Jun 2026](https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/); [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- If the Omnibus were not formally adopted before 2 August 2026, the original high-risk timeline would apply from that date as written. — [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)
- The Federal Reserve's SR 11-7 (4 April 2011) defines model risk management expectations covering development, validation and governance, and it is the US supervisory baseline banks apply to AI models; I did not fetch it in this session. — [Federal Reserve SR 11-7](https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm)
- DORA, Regulation (EU) 2022/2554, applies ICT risk-management and third-party-risk requirements to EU financial entities from 17 January 2025, which covers LLM and MCP providers as ICT third parties; I did not fetch it in this session. — [EUR-Lex DORA](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- BlackRock's Aladdin Copilot governs plugin access by environment, user group and application, and applies input guardrails for PII, toxicity and off-topic content and output guardrails for hallucination and domain moderation. — [ZenML summary of BlackRock talk, 2025](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)
- Goldman Sachs routes GS AI Assistant prompts through an internal compliance gateway that selects among several vetted models, according to press reports. — [Belitsoft, Jul 2025](https://belitsoft.com/news/goldman-sachs-ai-assistant-23072025); [Fox Business](https://foxbusiness.com/technology/goldman-sachs-announces-firmwide-launch-ai-assistant)

### Inferences
- FINRA's expectation of prompt and output logs implies that firms should also log the retrieved context and tool results the agent saw, because the prompt alone cannot reconstruct an agent's decision chain; this is an inference, and FINRA did not state it in these terms.
- Information barriers and MNPI controls map naturally onto permission-aware retrieval and per-user tokens passed through MCP, because an agent that retrieves with a shared service account can cross a Chinese wall that the user could not.
- The EU AI Act deferral reduces near-term legal pressure for credit-scoring style use cases, but DORA third-party risk and SR 11-7 validation already apply, so governance work cannot wait for 2027.

### Gaps
- I found no published technical account of row- or column-level security passthrough from a warehouse (for example Snowflake or Databricks Unity Catalog) to an agent at a named bank.
- I found no regulator publication (FINRA, Fed, EBA, ESMA, FCA) that explicitly addresses information barriers or MNPI in the context of LLM retrieval; this is a genuine gap rather than a search limitation that I could confirm.
- I did not fetch ESMA's 2024 statement on AI in investment services or EBA material, and I did not confirm whether the Digital Omnibus was published in the Official Journal.
- Creditworthiness assessment is an Annex III use case under the AI Act according to my background knowledge, but the searched sources did not confirm it.

## Financial services and capital markets case studies

### Takeaway
The published bank deployments share a pattern: a firm-controlled gateway or portal in front of several models, retrieval over curated internal content, and evaluation suites built with domain experts. Data vendors (S&P Global/Kensho, LSEG, Moody's, FactSet and others) now distribute licensed data to agents through MCP connectors with per-user authentication. Almost all outcome numbers come from the firms or their vendors.

### Cited Findings
- Morgan Stanley's AI @ Morgan Stanley Assistant is used by over 98% of advisor teams, according to OpenAI's customer story; this is a vendor-published figure. — [OpenAI customer story](https://openai.com/index/morgan-stanley/)
- Morgan Stanley built its rollout on an evaluation framework in which advisors and prompt engineers graded summarization outputs for accuracy and coherence, and it later added translation evals; for the Debrief meeting tool it built eval datasets across meeting types and kept advisor review of outputs before they enter the CRM. — [OpenAI customer story](https://openai.com/index/morgan-stanley/)
- Trade press reports that Morgan Stanley said document retrieval efficiency rose from 20% to 80%, which is a firm claim without a published method. — [CTO Magazine](https://ctomagazine.com/ai-in-morgan-stanley-shaping-the-future-of-financial-services/)
- A secondary summary reports that the Morgan Stanley assistant's corpus grew to about 100,000 documents; OpenAI's page does not state this figure. — [ZenML LLMOps database](https://www.zenml.io/llmops-database/enterprise-knowledge-management-with-llms-morgan-stanley-s-gpt-4-implementation)
- JPMorgan's LLM Suite is a portal over external models rather than an in-house model, and the bank updates it roughly every eight weeks as it connects data from business units. — [CeFPro](https://connect.cefpro.com/article/view/inside-jpmorgan-llm-suite-as-ai-agents-spread-across-the-bank); [Bernard Marr](https://bernardmarr.com/?p=17394)
- Reported JPMorgan usage figures differ: about 250,000 staff with access and roughly half using it daily (October 2025 reporting), versus more than 230,000 staff using the platform in an August 2026 piece. — [AI Magazine](https://aimagazine.com/news/jpmorgan-openai-anthropic-evolving-banking-operations); [CeFPro](https://connect.cefpro.com/article/view/inside-jpmorgan-llm-suite-as-ai-agents-spread-across-the-bank)
- JPMorgan's chief analytics officer Derek Waldron has said that firms "work in thousands of different applications" and that much of the work is connecting them into an AI ecosystem, which identifies integration rather than model capability as the bottleneck. — [McKinsey interview](https://www.mckinsey.com.br/industries/financial-services/our-insights/jpmorgan-chases-derek-waldron-on-building-an-ai-first-bank-culture)
- Goldman Sachs launched the GS AI Assistant firm-wide in mid-2025, using GPT, Gemini, Claude and vetted open-source models behind an internal gateway and combining proprietary and public data. — [Fox Business](https://foxbusiness.com/technology/goldman-sachs-announces-firmwide-launch-ai-assistant); [YourStory](https://yourstory.com/ai-story/goldman-sachs-ai-assistant-launch-2025)
- BlackRock's Aladdin Copilot uses a plugin registry to which 50–60 domain teams contribute, either by registering existing Aladdin APIs as tools or by building custom agents, while a central AI team owns the shared infrastructure. — [ZenML summary of BlackRock talk, 2025](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)
- Each Aladdin Copilot query carries application context (which app is open, what is on screen and user settings), and a filtering step narrows thousands of tools to about 20–30, because the presenters observed that planning quality degraded beyond about 40–50 tools. — [ZenML summary of BlackRock talk, 2025](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)
- BlackRock describes "evaluation-driven development" in which system-prompt behaviours become test cases built with subject-matter experts, synthetic data and LLM-as-judge scoring, run daily and on every pull request; the talk gave no quantified outcome metrics. — [ZenML summary of BlackRock talk, 2025](https://www.zenml.io/llmops-database/agentic-ai-architecture-for-investment-management-platform)
- S&P Global and Anthropic announced on 15 July 2025 that a Kensho-built MCP server would give Claude access to S&P Capital IQ Financials, earnings call transcripts and other datasets, with users connecting by logging in to their own authorized S&P account. — [S&P Global press release, 2025-07-15](https://press.spglobal.com/2025-07-15-S-P-Global-and-Anthropic-Announce-Integration-of-S-P-Globals-Trusted-Financial-Data-into-Claude); [Kensho](https://kensho.com/news/kensho-llm-ready-api-expands-mcp-server-access-dataset-support-integrations)
- S&P Global's marketplace page (updated 20 February 2026) says the connector also works in Claude add-ins for Excel and PowerPoint and lists an S&P Global plugin for Claude Cowork. — [S&P Global Marketplace](https://www.marketplace.spglobal.com/en/solutions/claude-(fced11f1-c791-436a-83d8-517c6f66f789))
- Anthropic's "Advancing Claude for Financial Services" post describes connectors for LSEG (fixed income pricing, equities, FX, macro indicators and analyst estimates), Moody's (ratings, research and data on more than 600 million companies) and MT Newswires. — [Anthropic](https://www.anthropic.com/news/advancing-claude-for-financial-services)
- A third-party summary dates a May 2026 Anthropic financial services release that included ten agent templates and 17 data-partner connectors including FactSet, S&P Capital IQ, MSCI, PitchBook, Morningstar and LSEG; this should be checked against Anthropic's own post. — [claudekit.io](https://claudekit.io/en/updates/claude-finance-agents/)

### Inferences
- The common architecture is a firm-owned control plane (gateway, registry, evals) with interchangeable models, which treats the context layer and its governance as the durable asset and the model as replaceable.
- Vendor MCP connectors that authenticate the individual user preserve existing data-licence entitlements, which addresses a licensing and audit problem that shared API keys would create.
- BlackRock's 40–50 tool ceiling is one of the few published, concrete limits on how much tool context can be placed in front of a planner.

### Gaps
- I found no primary architecture write-up from Goldman Sachs, Citi, Bridgewater, Bloomberg or Nasdaq in this session; Bloomberg's BloombergGPT paper and Bridgewater's AIA Labs fund were not researched here.
- I found no independent measurement of outcomes at any bank; all usage and productivity figures are self-reported.
- I did not confirm FactSet's MCP server from a FactSet source.

## Non-financial case studies with transferable lessons

### Takeaway
Text-to-SQL deployments at Uber, LinkedIn and Pinterest show that accuracy depends on narrowing the schema context (intent routing, table selection, column pruning) and on metadata drawn from query logs and documentation, and that measured accuracy remains moderate (LinkedIn reports 53% correct or nearly correct on an internal benchmark).

### Cited Findings
- Uber's QueryGPT began at a May 2023 hackathon and uses an intent agent that maps a question to business domains before retrieving tables and sample SQL. — [Maxim summary of Uber blog](https://getmaxim.ai/blog/nl-to-sql-uber)
- Uber reported that accuracy fell as more tables were added to context, and that it needed more than 20 algorithm iterations, with intent classification, table confirmation by the user and column pruning as the key fixes. — [Maxim summary of Uber blog](https://getmaxim.ai/blog/nl-to-sql-uber)
- Uber evaluates QueryGPT with a set built from real logs and manually verified golden SQL, tracking intent accuracy, table overlap, successful runs, output presence and query similarity. — [Maxim summary of Uber blog](https://getmaxim.ai/blog/nl-to-sql-uber)
- Uber's platform runs about 1.2 million interactive queries a month, and secondary sources report authoring time falling from about 10 minutes to about 3 minutes; the 140,000 hours-per-month figure is a vendor extrapolation rather than an Uber measurement. — [Wren AI](https://getwren.ai/post/how-uber-is-saving-140-000-hours-each-month-using-text-to-sql-and-how-you-can-harness-the-same-power)
- LinkedIn's SQL Bot, described in the arXiv paper "Text-to-SQL for Enterprise Data Analytics" (July 2025), builds a knowledge graph from database metadata, query logs, wikis and code, clusters tables by team or product area, has over 300 weekly users, and was judged 53% correct or close to correct by experts on an internal benchmark. — [arXiv 2507.14372](https://arxiv.org/html/2507.14372v1)
- Pinterest's text-to-SQL system reportedly raised first-shot acceptance from about 20% to over 40%, improved task completion speed by 35%, and raised table search hit rate from 40% to 90% after adding RAG-based table selection; these figures come from a secondary summary. — [ZenML summary](https://zenml.io/llmops-database/text-to-sql-system-with-rag-enhanced-table-selection)

### Inferences
- The transferable lesson for capital markets data (security masters, positions, risk) is that curated metadata and table-selection steps matter more than a larger context window, which is consistent with BlackRock's tool-filtering result.

### Gaps
- I did not research Shopify, Stripe or Klarna in this session; Klarna's published AI assistant figures and its later partial reversal toward human agents should be sourced separately.
- The Pinterest and Uber numbers should be checked against the original engineering blog posts.

## Surveys on why enterprise AI pilots fail

### Takeaway
The two most cited figures are weak evidence: MIT NANDA's "95% see no return" rests on about 150 survey responses and 52 interviews with a narrow six-month definition of success, and Gartner's "over 40% of agentic projects canceled by 2027" is a prediction based on a webinar poll. Both point to cost, unclear value, risk controls and integration with workflows and data rather than model quality.

### Cited Findings
- MIT NANDA's "The GenAI Divide: State of AI in Business 2025" (July 2025) reported that 95% of organizations saw no measurable return from generative AI initiatives. — [PureAI, 23 Sep 2025](https://pureai.com/Articles/2025/09/23/Most-GenAI-Investments-Fail.aspx)
- Critics note that the report is not peer reviewed, that it relied on about 150 survey responses and 52 interviews, and that it defined success as marked and sustained P&L impact within about six months. — [AI Realist](https://msukhareva.substack.com/p/genai-has-little-to-no-return-on); [CustomerThink](https://customerthink.com/the-great-genai-divide-debunking-the-myth-of-95-failure/)
- Gartner predicted on 25 June 2025 that over 40% of agentic AI projects will be canceled by the end of 2027 because of escalating costs, unclear business value or inadequate risk controls, and estimated that only about 130 of thousands of agentic AI vendors are genuine ("agent washing"). — [Gartner press release, 2025-06-25](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)
- The Gartner forecast draws on a January 2025 poll of 3,412 webinar attendees. — [Gartner press release, 2025-06-25](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027)

### Inferences
- The failure causes named in these surveys (integration with workflows, risk controls, unclear value) are context-engineering problems more than model problems, which matches JPMorgan's statement that connecting thousands of applications is the main work.

### Gaps
- I did not find a 2026 data-readiness survey (for example from Gartner on AI-ready data, or from Informatica or Cloudera) in this session, so data-readiness percentages are not sourced here.
- I did not obtain the MIT NANDA report itself and relied on secondary descriptions of its method.
