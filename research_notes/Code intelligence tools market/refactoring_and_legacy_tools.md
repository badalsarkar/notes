# Code intelligence tools for large-scale refactoring, architecture analysis and legacy/mainframe modernization (as of November 2026)

Scope note: This research covered about 17 search and fetch calls. Vendor statements are labelled "(vendor claim)". Items older than 2026 carry their date. Products for which no reliable 2025-2026 source was found are listed under Gaps rather than described from memory.

## What is the code model each builds and how is it kept current?

### Takeaway
The tools split into three model families. Moderne builds compiler-accurate, type-attributed Lossless Semantic Trees (LSTs) per repository. AWS Transform, CAST Imaging, IBM ADDI and Google MAT build cross-program dependency or knowledge graphs over legacy estates (COBOL, PL/I, JCL, data). vFunction and developer portals (Backstage, Port, OpsLevel) build architecture-level or service-level models from runtime telemetry and catalog metadata. Most of these models are refreshed by re-running an analysis or build step rather than by continuous incremental updating; vFunction is the main exception because it uses OpenTelemetry for continuous updates.

### Cited Findings

**Moderne (OpenRewrite, LST, Moddy, Moderne CLI/MCP)**
- Moderne's LST preserves whitespace and formatting around every element so that the original source can be printed back unchanged, which is what "lossless" means. — [Moderne docs: Lossless Semantic Trees](https://docs.moderne.io/user-documentation/recipes/authoring-recipes/concepts/lossless-semantic-trees)
- The LST is produced by driving the compiler through syntactic and semantic analysis so that it has full type attribution (vendor description). — [Moderne docs: LST reference](https://docs.moderne.io/administrator-documentation/moderne-platform/references/lossless-semantic-trees); [Moderne technology page](https://moderne.io/technology)
- In the local MCP mode (`mod mcp`), a background thread detects the git root and builds the LST by invoking the repository's own build toolchain (Gradle, Maven or other configured tools), and stores it under `.moderne/mcp/lst/` inside the repository. The LST is therefore refreshed by rebuilding, which depends on the project building successfully. — [Moderne MCP security and architecture](https://docs.moderne.io/user-documentation/agent-tools/mcp/security)
- Moderne extended type-attributed refactoring to JavaScript/TypeScript so that frontend and backend upgrades can use the same approach (secondary coverage, undated in snippet). — [Efficiently Connected](https://www.efficientlyconnected.com/?p=5019)

**AWS Transform (mainframe, .NET, VMware)**
- AWS told Info-Tech that mainframe analysis produces a knowledge graph intended to represent components and execution flow, and that Blu Age technology supports parts of analysis and refactoring. — [Info-Tech SoftwareReviews note](https://www.softwarereviews.com/vendor-technology-notes/aws-transform-says-it-s-processed-10-billion-lines-of-legacy-code)
- AWS's ML blog describes a dependency graph that reflects compiler semantics and records cross-program dependencies and middleware behaviour before any generative AI is applied. — [AWS ML blog: Learnings from COBOL modernization in the real world](https://aws.amazon.com/blogs/machine-learning/learnings-from-cobol-modernization-in-the-real-world)
- AWS documentation for the mainframe workflow describes storing extracted job artifacts in an Amazon Neptune cluster that answers questions in the chat interface (as summarised by search; not fetched in full). — [AWS Transform mainframe workflow docs](https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe-workflow.md)
- The 2026 "reimagine" workflow covers COBOL and PL/I, extracting business rules, data lineage and domain structure, then producing specifications using Business Rule Extraction and Domain-Driven Design methods. — [AWS: Reimagining mainframe applications with AWS Transform and Claude Code (2026)](https://aws-news.com/article/2026-05-08-reimagining-mainframe-applications-with-aws-transform-and-claude-code)
- AWS published an "Assess and Reimagine" workflow in June 2026 focused on traceability from mainframe source to implementation-ready requirements. — [AWS news, 26 June 2026](https://aws-news.com/article/2026-06-26-reimagine-mainframe-applications-with-traceability-and-speed-using-aws-transform)

**CAST Imaging and CAST Highlight**
- CAST Imaging exposes application statistics, cross-application dependencies, internal architectural graphs, object details, interactions and call graphs, which indicates a whole-application object-and-dependency graph built by CAST's static analysers. — [CAST: AI can now understand and transform big enterprise codebases](https://www.castsoftware.com/news/ai-can-now-understand-and-transform-big-enterprise-codebases)
- The model is refreshed when an application is re-analysed in CAST Imaging; the MCP server reads results through the CAST Imaging API rather than analysing code itself. — [CAST docs: Getting started with CAST Imaging MCP Server](https://doc.castsoftware.com/mcp-server/)

**IBM watsonx Code Assistant for Z and IBM ADDI**
- IBM introduced watsonx Code Assistant for Z in August 2023 for COBOL-to-Java conversion on IBM Z and positioned it alongside ADDI, which performs inventory, discovery and dependency analysis. — [IBM newsroom, 22 Aug 2023](https://newsroom.ibm.com/2023-08-22-IBM-Unveils-watsonx-Generative-AI-Capabilities-to-Accelerate-Mainframe-Application-Modernization?_gl=1); [ADTmag, Aug 2023](https://adtmag.com/Articles/2023/08/29/Watsonx-Code-Assistant-for-Z-Announced.aspx)
- Futurum describes the product as an evolution in COBOL modernization combining ADDI analysis with generative conversion (analyst commentary, date not verified). — [Futurum Group](https://futurumgroup.com/insights/watsonx-code-assistant-for-z-the-next-evolution-in-cobol-modernization)

**Google Cloud Mainframe Assessment Tool (MAT) and Mainframe Modernization Agents**
- Google describes MAT as reverse-engineering legacy codebases at large scale to explain how current applications behave, powered by Gemini models and mainframe-specific agentic workflows, and as the first of four areas (assessment, application modernization, pre-production testing, data migration). — [Google Cloud Mainframe Modernization](https://cloud.google.com/solutions/mainframe-modernization); [IT Brief UK](https://itbrief.co.uk/story/google-cloud-launches-ai-tools-for-mainframe-migration)
- Business rules extracted by MAT feed Mainframe Modernization Agents, which produce target specifications, architecture designs, implementation plans and Java or C# code. — [Google Cloud Mainframe Modernization](https://cloud.google.com/solutions/mainframe-modernization)

**Rocket Enterprise Analyzer (formerly Micro Focus / OpenText)**
- Rocket completed integration of OpenText's Application Modernization and Connectivity (AMC) business, formerly Micro Focus, in May 2024, and Enterprise Analyzer is now a Rocket product. — [Futurum: Rocket acquires OpenText AMC](https://futurumgroup.com/insights/rocket-acquires-opentext-amc-a-new-era-in-mainframe-modernization)
- Rocket describes Enterprise Analyzer as helping engineers understand application logic and dependencies and providing "what if" impact analysis, with integration into Visual Studio, Eclipse and VS Code. — [Rocket: The role of AI in application modernization](https://www.rocketsoftware.com/en-us/insights/future-ai-application-modernization)
- Rocket agreed in February 2026 to acquire OpenText's Vertica analytics database, which shows Rocket continuing to consolidate former Micro Focus assets. — [GlobeNewswire, 2 Feb 2026](https://www.globenewswire.com/news-release/2026/02/02/3230355/0/en/rocket-software-to-acquire-vertica-analytics-database-platform-from-opentext.html)

**vFunction (architectural observability)**
- vFunction analyses architecture using AI-enabled dynamic and static analysis in test, staging or production, and in 2025 integrated OpenTelemetry data to provide continuously updated architectural observability and documentation, including drift detection for distributed applications. — [vFunction press release, 29 Apr 2025](https://www.businesswire.com/news/home/20250429830762/en/vFunction-Unveils-New-Advancements-to-Simplify-Complex-Applications-Closing-Gap-Between-AI-Accelerated-Development-and-Architectural-Integrity); [SDxCentral press release](https://www.sdxcentral.com/press-releases/vfunction-expands-ai-driven-architectural-observability-platform-to-solve-for-technical-debt-in-distributed-application-architectures/)

**Developer portals and catalogs (Backstage, Port, OpsLevel)**
- These tools model services, ownership, dependencies and custom properties as catalog entities rather than code-level structure; OpsLevel says its MCP returns the same ownership, dependency and custom property data engineers see in the catalog. — [OpsLevel: richer context for humans and AI agents](https://www.opslevel.com/resources/richer-context-for-humans-and-ai-agents)

### Inferences
- Moderne's model is the most precise at the code level (type-attributed, round-trippable) but is bounded by what can be built; legacy estates without a working build cannot easily produce LSTs.
- Mainframe tools (AWS Transform, MAT, ADDI, CAST, Enterprise Analyzer) model cross-program, JCL and data-access dependencies across a whole estate, which is closer to an enterprise knowledge graph than to a per-repository syntax tree.
- Freshness is a structural weakness for most of these products because the model is a snapshot from the last analysis run; only runtime-fed tools like vFunction claim continuous updating.

### Gaps
- I did not find a 2026 source on how IBM ADDI's model is stored or refreshed, nor any 2026 watsonx Code Assistant for Z release notes.
- I did not verify CAST Highlight's model (it is generally a portfolio-level survey tool), Structurizr, Snyk's code graph, Cortex or Sonar's internal model in this session.
- I did not find a primary AWS source confirming the Neptune detail beyond the documentation search summary.

## How do these tools expose their models to coding agents in 2026?

### Takeaway
MCP is now the default exposure mechanism. Moderne, CAST, Sonar, Backstage, Port, OpsLevel and Google MAT all ship MCP servers, and AWS Transform integrates with Claude Code, Cursor, Codex and Kiro through skills and context files rather than (as far as I could verify) a first-party MCP server. No MCP announcement was found for vFunction, IBM ADDI/watsonx Code Assistant for Z or Rocket Enterprise Analyzer.

### Cited Findings
- Moderne's `mod mcp` is a local tool server wrapping Moderne CLI code-intelligence features; the agent runs in the client (for example Claude Code, Copilot or Windsurf) as a separate process. — [Moderne MCP security and architecture](https://docs.moderne.io/user-documentation/agent-tools/mcp/security)
- The local Moderne MCP server does not contact the Moderne platform by default and only uploads tool-call telemetry if the CLI is connected and signed in to a tenant. — [Moderne MCP security and architecture](https://docs.moderne.io/user-documentation/agent-tools/mcp/security)
- Moddy Desktop runs an MCP server on localhost:4848 with eight tools to search the recipe catalog, run recipes across many repositories, query recipe data tables and apply resulting changes. — [Moderne docs: Moddy Desktop MCP tools reference](https://docs.moderne.io/user-documentation/moddy/mcp-tools-reference)
- Moderne's 2026 conference talk argued that deterministic LST-based tools are accurate, fast and token-cheap for agents, citing an upgrade done in about three minutes using roughly 30k tokens (vendor claim). — [Moderne, "DevTools or Agent Tools", OSFF Toronto 2026](https://hosted-files.sched.co/osfftoronto2026/d4/Moderne%20-%20DevTools%20or%20Agent%20Tools.pdf)
- AWS's 2026 workflow pairs AWS Transform for reverse engineering with Claude Code for forward engineering, using CLAUDE.md for persistent project context and Claude Code Skills to package repeatable workflows as slash commands, with human validation of specifications before code generation. The article does not mention MCP. — [AWS: Reimagining mainframe applications with AWS Transform and Claude Code](https://aws-news.com/article/2026-05-08-reimagining-mainframe-applications-with-aws-transform-and-claude-code)
- AWS Transform is also available through Kiro Powers and agent skills that work with Claude Code, Cursor and Codex (search summary of AWS docs). — [AWS Transform launch guide](https://docs.aws.amazon.com/transform/latest/launchguide/aws-transform.md)
- CAST launched an early-access MCP server for CAST Imaging on 1 August 2025, delivered as Docker for on-premises or cloud use, and later made it available to all CAST Imaging users. — [CAST press release, Aug 2025](https://www.castsoftware.com/news/cast-announces-early-access-to-cast-imaging-mcp-server); [CAST: AI can now understand and transform big enterprise codebases](https://www.castsoftware.com/news/ai-can-now-understand-and-transform-big-enterprise-codebases)
- CAST Imaging Express and Imaging on Cloud have their own MCP servers, name Claude Desktop and GitHub Copilot as supported clients, and authenticate with an API key. — [CAST Imaging Express MCP FAQ](https://doc.castsoftware.com/imagingexpress/mcp-server/faq/); [CAST Imaging on Cloud MCP](https://doc.castsoftware.com/imagingoncloud/mcp-server/)
- Google documents running Gemini CLI against an AGENTS.md exported from MAT, with a MAT MCP server giving the CLI access to assessment data. — [Google Cloud MAT docs: modernize and validate](https://docs.cloud.google.com/mainframe-assessment-tool/docs/modernize-validate)
- Sonar offers a free local SonarQube MCP Server and an embedded MCP server in SonarQube Cloud; SonarQube Server 2026.3 describes native MCP connectivity for AI coding assistants. — [Sonar MCP Server](https://www.sonarsource.com/products/sonarqube/mcp-server/); [Sonar: native MCP Server in SonarQube Cloud](https://www.sonarsource.com/de/blog/announcing-native-mcp-server-in-sonarqube-cloud/); [Sonar: SonarQube Server 2026.3](https://www.sonarsource.com/jp/blog/announcing-sonarqube-server-2026-3/)
- A UK government (Defra) assessment describes "AI Code Assurance" as the main use of the Sonar MCP server, with the agent checking its output against quality gates before committing, through tools such as `analyze_code_snippet`, `get_project_quality_gate_status` and `search_sonar_issues_in_projects`. — [Defra AI SDLC tool guidance: SonarQube MCP](https://defra.github.io/ai-sdlc-tool-guidance/tool-guidance/mcps/sonarqube-mcp-detailed)
- Backstage's MCP Actions backend serves an MCP server at `/api/mcp-actions/v1` that exposes registered actions, can be split into focused servers, and uses Streamable HTTP (SSE is deprecated). — [Backstage docs: MCP actions](https://backstage.io/docs/ai/mcp-actions)
- Red Hat Developer Hub adds `software-catalog-mcp-tool` and `techdocs-mcp-tool` plug-ins on top of the Backstage MCP server (November 2025). — [Red Hat Developers, 10 Nov 2025](https://developers.redhat.com/articles/2025/11/10/mcp-red-hat-developer-hub-chat-your-catalog); [Red Hat Developer Hub 1.8 docs](https://docs.redhat.com/en/documentation/red_hat_developer_hub/1.8/html/interacting_with_model_context_protocol_tools_for_red_hat_developer_hub/assembly-model-context-protocol-tools)
- Spotify Portal for Backstage supports connecting third-party MCP servers to its AiKA assistant. — [Spotify Portal: third-party MCP servers](https://backstage.spotify.com/docs/portal/core-features-and-plugins/mcp/third-party-servers)
- Port launched an MCP server in June 2025 so that Cursor, VS Code and Claude can query and build in the Port catalog in natural language. — [Port blog](https://www.port.io/blog/integrate-software-catalog-every-workflow-port-mcp-server/)
- OpsLevel demonstrated an MCP server in June 2025 for surfacing metadata, health status and runbooks and for automating campaigns and bulk actions. — [OpsLevel MCP demo](https://www.opslevel.com/resources/demo-the-opslevel-mcp)
- Microsoft's open-source Legacy Modernization Agents (originally "COBOL Agentic Migration Factory") orchestrate persona-based agents with Semantic Kernel to convert COBOL to Java Quarkus or C# .NET (July 2025). — [Microsoft DevBlogs, 9 Jul 2025](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/); [GitHub: Azure-Samples/Legacy-Modernization-Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents)
- Microsoft's broader offering is GitHub Copilot app modernization agents for making legacy applications cloud- and AI-ready. — [Azure blog: Many agents, one team](https://azure.microsoft.com/en-us/blog/many-agents-one-team-scaling-modernization-on-azure/)
- I found no evidence of a vFunction MCP server in 2025-2026 sources. — [vFunction 2025 release](https://vfunction.com/news/vfunction-unveils-new-advancements-to-simplify-complex-applications/)

### Inferences
- Two exposure patterns are emerging. One is "deterministic tool behind MCP" (Moderne recipes, Sonar quality gates, CAST graph queries), where the agent calls a precise engine. The other is "specification hand-off" (AWS Transform, Google MAT, Morgan Stanley DevGen.AI), where the analysis tool produces specs or AGENTS.md/CLAUDE.md context that a general coding agent then implements.
- Mainframe incumbents (IBM, Rocket) appear to lag in agent-facing interfaces compared with cloud providers and newer vendors, based on the absence of MCP announcements found.

### Gaps
- I could not confirm whether AWS Transform has a first-party MCP server or relies only on skills and Kiro Powers.
- I did not find a Cortex MCP server source, nor Snyk code graph or Structurizr agent integrations, in this session.
- Exact tool lists for the Moderne `mod mcp` server and the CAST Imaging MCP server were not captured.

## What independent evidence of outcomes exists, especially in financial services?

### Takeaway
Independent, quantified outcome evidence is thin. Most figures are vendor-reported (AWS line counts, Moderne case studies) or come from banks' own statements to the press (Morgan Stanley). Financial services is the most visible sector, with Morgan Stanley, Bankdata, BNY (as a listed Moderne customer) and anonymised banks and insurers, but none of the figures found are audited or independently benchmarked.

### Cited Findings
- Morgan Stanley's in-house DevGen.AI, built on OpenAI GPT models, translates legacy code such as COBOL into plain-English specifications for developers to rewrite; in June 2025 the firm said it had reviewed nine million lines in five months and saved its 15,000 developers about 280,000 hours (bank's own statement to WSJ). — [Slashdot summarising WSJ, 4 Jun 2025](https://tech.slashdot.org/story/25/06/04/1233253); [Business Insider NL](https://www.businessinsider.nl/a-team-of-engineers-saved-morgan-stanley-more-than-280000-hours-this-year-the-bank-says-their-tool-wont-take-jobs/)
- A later CIO Dive article says Morgan Stanley has modernized more than 17 million lines of COBOL, Software AG Natural and Perl into Java and Python using DevGen.AI (article date not confirmed). — [CIO Dive](https://www.ciodive.com/news/ai-shifts-mainframe-modernization-strategy/825677/)
- Bankdata, owned by a consortium of Danish banks representing over 30% of the Danish market, worked with Microsoft on a multi-agent COBOL migration framework; Bankdata initially provided only a small COBOL module for testing (July 2025). — [Microsoft DevBlogs, 9 Jul 2025](https://devblogs.microsoft.com/all-things-azure/how-we-use-ai-agents-for-cobol-migration-and-mainframe-modernization/)
- A secondary conference page says the framework targets Bankdata's 17 million lines of COBOL; I found no confirmation that it is in production. — [WeAreDevelopers talk page](https://platform-v2.wearedevelopers.com/videos/1531/migrating-from-cobol-with-ai-a-moonshot-demo)
- AWS says AWS Transform processed over 4.5 billion lines in its first year, and Info-Tech reports AWS's later claim of 10 billion lines (vendor claims, not independently audited). — [AWS Transform docs](https://docs.aws.amazon.com/transform/latest/launchguide/aws-transform.md); [Info-Tech SoftwareReviews](https://www.softwarereviews.com/vendor-technology-notes/aws-transform-says-it-s-processed-10-billion-lines-of-legacy-code)
- A FINOS blog by Moderne says a large banking customer faced upgrading more than 15,000 codebases to Java 21, estimated at over 50,000 hours manually (vendor-authored). — [FINOS community blog](https://www.finos.org/blog/open-source-auto-refactoring-meets-ai-agent-to-modernize-fintech-software-at-scale)
- Moderne reports a large financial services cooperative reaching a steady "green" state for security issues in one business unit with a "conservative" 74% time saving (vendor case study, customer anonymised). — [Moderne case study: financial services](https://moderne.io/blog/case-study-improving-risk-profile-and-devx-with-automated-code-remediation-in-financial-services)
- Moderne also publishes anonymised case studies for mid-sized US insurers using automated code migrations. — [casestudies.com: insurer](https://www.casestudies.com/company/moderne/case-study/insurer-improves-developer-productivity-with-code-migration-automation)
- CB Insights lists Bank of New York Mellon among Moderne's customers (third-party database, not a case study). — [CB Insights: Moderne customers](https://www.cbinsights.com/company/moderne/customers)
- Computer Weekly interviewed Moderne about a major bank needing to move off Java 8 tied to WebSphere. — [Computer Weekly](https://www.computerweekly.com/news/366627766/Interview-Is-there-an-easier-way-to-refactor-applications)
- Cognition (Devin) published an April 2026 post on COBOL modernization at Fortune 500 companies, which is a further vendor-reported data point rather than independent evidence. — [Cognition blog, 8 Apr 2026](https://cognition.ai/blog/how-devin-is-modernizing-cobol-at-fortune-500-companies)
- IBM's product page cites a 94% reduction in time to analyse superfluous COBOL code without naming a client or date (vendor claim). — [IBM watsonx Code Assistant for Z](https://www.ibm.com/products/watsonx-code-assistant-z/pricing)
- Analyst coverage exists from Omdia ("On the radar: Moderne") and Intellyx, which describe capability rather than measure outcomes. — [Omdia](https://omdia.tech.informa.com/om142903/on-the-radar-moderne-for-automated-code-migration); [Intellyx](https://intellyx.com/?p=46985)

### Inferences
- The strongest financial-services signal is that large banks are building in-house tooling (Morgan Stanley DevGen.AI) or co-developing with hyperscalers (Bankdata with Microsoft), which suggests packaged products did not fully meet their needs at the time.
- Productivity numbers are typically reported as "lines reviewed" or "hours saved", which measure throughput rather than defect rates, equivalence or production cut-over; this weakens comparability.

### Gaps
- I found no independent, peer-reviewed or analyst-measured outcome study for any of these tools in banking, insurance, exchanges or capital markets.
- I found no named exchange or capital-markets customer for CAST, vFunction, IBM ADDI, Rocket or Google MAT in this session (CAST and IBM are widely reported to have bank customers, but I did not retrieve a citable source).
- I did not verify the date of the 17-million-line Morgan Stanley figure.

## What are the pricing and deployment constraints for regulated firms?

### Takeaway
Deployment options vary from fully local (Moderne CLI/MCP, local SonarQube MCP, CAST Imaging MCP in Docker) to SaaS-only managed services (AWS Transform, Google MAT/agents run in the provider's cloud). Published pricing is scarce; most products are sold through enterprise contracts. Regulated firms need to check where source code is sent, since several MCP integrations route code or prompts to a backend.

### Cited Findings
- Moderne's local MCP server runs on the developer's machine, stores LSTs inside the repository and does not contact Moderne's platform unless the CLI is connected to a tenant, in which case it uploads tool-call telemetry. — [Moderne MCP security and architecture](https://docs.moderne.io/user-documentation/agent-tools/mcp/security)
- CAST Imaging MCP server is delivered as Docker and can run on corporate servers or in the cloud, with separate installation from CAST Imaging and API-key authentication. — [CAST press release, Aug 2025](https://www.globenewswire.com/de/news-release/2025/08/01/3126069/0/en/cast-announces-early-access-to-cast-imaging-mcp-server.html); [CAST MCP install guide](https://doc.castsoftware.com/install/mcp-server)
- Sonar's MCP server is free and local (Docker), with an alternative embedded server in SonarQube Cloud; a third-party study site says MCP integration in SonarQube Server 2026.1 is limited to Developer edition and above (not verified against Sonar). — [Sonar MCP Server](https://www.sonarsource.com/products/sonarqube/mcp-server/); [ai-study-roadmap](https://ai-study-roadmap.pages.dev/cloud-and-infrastructure/applied/code-quality)
- The UK Defra assessment flags a data-sovereignty concern with the Sonar MCP server: prompt content, which can include source code, flows from the IDE through the MCP server to the backend SonarQube instance. — [Defra AI SDLC tool guidance](https://defra.github.io/ai-sdlc-tool-guidance/tool-guidance/mcps/sonarqube-mcp-detailed)
- AWS's mainframe reimagine workflow requires human-in-the-loop validation of specifications before code generation. — [AWS: AWS Transform and Claude Code](https://aws-news.com/article/2026-05-08-reimagining-mainframe-applications-with-aws-transform-and-claude-code)
- IBM publishes a pricing page for watsonx Code Assistant for Z, but the retrieved content did not include specific prices. — [IBM watsonx Code Assistant for Z pricing](https://www.ibm.com/products/watsonx-code-assistant-z/pricing)
- Moderne raised a $30m Series B, according to a fintech news listing (date not shown in snippet). — [FinTech Global](https://fintech.global/category/sector-updates/infrastructure-enterprise-software/banking-infrastructure/page/9)
- Rocket's ownership of former Micro Focus tools follows OpenText's divestitures; a licensing details site is the only source I found for Enterprise Analyzer licensing and is less reliable than vendor material. — [Futurum](https://futurumgroup.com/insights/rocket-acquires-opentext-amc-a-new-era-in-mainframe-modernization); [mainframelicensingexperts (third party)](https://mainframelicensingexperts.pages.dev/products/rocket-software/rocket-enterprise-analyzer/)
- Microsoft's Legacy Modernization Agents are open source, so a bank can run them inside its own Azure tenant with its own model deployments. — [GitHub: Azure-Samples/Legacy-Modernization-Agents](https://github.com/Azure-Samples/Legacy-Modernization-Agents)

### Inferences
- For banks and exchanges with strict source-code residency rules, locally hosted deterministic engines (Moderne CLI, CAST on-premises, SonarQube Server) are easier to approve than cloud-hosted analysis services, although the coding agent that consumes their MCP output may itself send code to a model provider.
- Hyperscaler services (AWS Transform, Google MAT) tie analysis to the provider's cloud, which suits firms already committed to that cloud but creates a dependency for the knowledge graph and specifications.

### Gaps
- I found no published 2026 list prices for Moderne, CAST Imaging/Highlight, vFunction, Rocket Enterprise Analyzer, IBM ADDI, Google MAT or AWS Transform in this session.
- I did not find accelerator products from Accenture, Infosys or TCS with verifiable 2025-2026 product documentation in the searches run.
- I did not verify FedRAMP, SOC 2 or on-premises availability for AWS Transform, Google MAT or vFunction.
