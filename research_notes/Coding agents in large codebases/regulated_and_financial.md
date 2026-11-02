# AI coding agents in banks, capital markets, insurers and other regulated or legacy-heavy enterprises

Evidence labels used on each finding:

- **[Exec]** means a statement by an executive of the firm, with no published method.
- **[Vendor]** means a case study or claim published by the tool seller or a paid consultancy.
- **[Practitioner]** means a first-person engineering account, such as a conference talk or engineering blog.
- **[Measured]** means a published method and data, which is not necessarily independent.
- **[Press]** means reporting, and it usually relays an [Exec] claim.
- **(excerpt only)** means I saw only a search result excerpt or a search summary and did not read the full page, so the claim should be checked before it is relied on.
- **(secondary)** means I read a summary or an aggregator and not the original talk, transcript or article.

## Which firms use coding agents on large legacy estates, and how are the programmes implemented?

### Takeaway
Large banks have moved from copilots to supervised agents, and they aim those agents mainly at bounded maintenance work: upgrades, patches, language migration, test generation, documentation, and legacy comprehension. The best-documented production legacy results come from comprehension and spec extraction plus human-reviewed mechanical migration, while one-shot rewrites remain unreliable, as JPMorgan's finance chief acknowledged in October 2026.

### Cited Findings

#### Goldman Sachs
- [Press/Exec] On 11 July 2025, CNBC reported that Goldman was piloting Cognition's Devin alongside about 12,000 developers, and CTO/CIO Marco Argenti said "hundreds of Devins" could become thousands depending on use cases. — [CNBC](https://www.cnbc.com/2025/07/11/goldman-sachs-autonomous-coder-pilot-marks-major-ai-milestone.html)
- [Exec] Argenti said this form of AI could raise productivity three to four times compared with earlier AI tools, and this was a forecast at pilot stage and not a result. — [CNBC](https://www.cnbc.com/2025/07/11/goldman-sachs-autonomous-coder-pilot-marks-major-ai-milestone.html)
- [Press] Human employees supervise Devin, and its stated work includes tedious tasks such as moving internal code to newer languages. — [CNBC](https://www.cnbc.com/2025/07/11/goldman-sachs-autonomous-coder-pilot-marks-major-ai-milestone.html)
- [Exec] (secondary) In Fortune on 8 May 2026, Argenti reportedly said usage is a poor signal and that he tracks idea-to-production speed and backlog, but no figure was given. — [Lucidate, 28 Oct 2026](https://lucidate.substack.com/p/banks-have-counted-the-hours-their)

#### JPMorgan Chase
- [Exec/Press] On 13 March 2025, Reuters reported global CIO Lori Beer saying tens of thousands of engineers became 10% to 20% more efficient with an in-house coding assistant. — [Reuters via Yahoo Finance](https://finance.yahoo.com/news/jpmorgan-engineers-efficiency-jumps-much-190410445.html) (excerpt only)
- [Exec, earnings call] On the Q3 2026 call on 13 October 2026, CFO Jeremy Barnum said "the benefits aren't observable in our current quarterly earnings" and that some benefits will be offset by token costs. — [Transcript on Webull](https://www.webull.com/news/15741198075913216)
- [Exec, earnings call] On that call, Barnum described a personal experiment with minor legacy tools in the technology group supporting finance, "trying to see if we could essentially one-shot the rewrite in a couple weeks, and it didn't work perfectly", while still describing the opportunity as exciting. — [Transcript on Webull](https://www.webull.com/news/15741198075913216)
- [Press] (secondary) A Business Insider dashboard report from April 2026 reportedly showed about 70,000 people set up on GitHub Copilot and about 24,000 recent users, which is roughly one third. — [Lucidate](https://lucidate.substack.com/p/banks-have-counted-the-hours-their)

#### Morgan Stanley (DevGen.AI)
- [Exec/Press] The WSJ reported on 3 June 2025 that the bank built DevGen.AI in-house on OpenAI GPT models, launched it in January 2025, and made it available to about 15,000 developers. — [WSJ via Tiger Brokers](https://www-web.itiger.com/news/2540775365)
- [Exec] Mike Pizzi said the tool had reviewed 9 million lines of code and saved 280,000 hours that year, and the article does not explain how hours were calculated. — [WSJ via Tiger Brokers](https://www-web.itiger.com/news/2540775365)
- [Press] The primary use is translating legacy languages such as COBOL into plain-English specifications from which developers rewrite the code, and other uses include isolating code for regulatory inquiries and fully translating small sections. — [WSJ via Tiger Brokers](https://www-web.itiger.com/news/2540775365)
- [Press] Full translation was described as still maturing, because the tool can rewrite Perl as Python without using Python idiomatically, and this is one stated reason humans stay in the loop. — [WSJ via Tiger Brokers](https://www-web.itiger.com/news/2540775365)
- [Unverified] A LinkedIn post by a co-creator says American Banker noted about 16 million lines modernised as of February 2026, and this is secondhand. — [LinkedIn search result](https://hk.linkedin.com/in/kennant-tom-a269a57) (excerpt only)

#### Citi
- [Press/Exec] American Banker reported on 14 July 2025 that Citi had begun rolling out Devin to its 40,000 developers, starting with simple tasks such as patches and library upgrades. — [American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers)
- [Exec] CTO David Griffiths said Copilot boosted productivity by 5% to 15%, that agentic tasks may run from 2x to 20x as fast, and that complex end-to-end features are "nowhere near that level yet". — [American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers)
- [Exec] Citi Squad, launched in 2024, was reported to have completed 740,000 automated reviews and to save about 100,000 hours per week. — [American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers)
- [Exec, earnings call] (secondary) On the Q3 2026 call on 13 October 2026, CEO Jane Fraser reportedly said 14,000 engineers use Devin and that technology supplier spending fell 30% in a year, which the analysis treats as the only money figure visible in accounts. I did not check this against Citi's transcript. — [Lucidate](https://lucidate.substack.com/p/banks-have-counted-the-hours-their)

#### Bank of America
- [Exec/Press] Fortune reported on 5 November 2025 that AI coding assistants are used by 18,000 developers, with a 20% productivity lift in select parts of the development life cycle. — [Fortune](https://fortune.com/2025/11/05/bank-of-america-prioritizes-bigger-ai-initiatives-as-annual-spending-on-new-tech-increased-by-44-over-the-past-decade) (excerpt only)
- [Exec/Press] A November 2025 report says the developers had used agents for about a year and that some software test work was streamlined by 90%. — [The Star](https://www.thestar.com.my/tech/tech-news/2025/11/18/bofa-says-ai-is-boosting-bankers039-productivity-revenue) (excerpt only)
- [Exec] CTO Hari Gopalkrishnan is quoted saying the 20% gain is being reinvested in new initiatives. — [American Banker](https://www.americanbanker.com/news/bank-of-america-jpmorganchase-execs-report-returns-on-ai) (excerpt only)

#### Nubank (Devin ETL migration)
- [Vendor] Cognition's case study describes an eight-year-old ETL monolith with over 6 million lines of code, about 100,000 data class implementations, dependency chains up to 70 levels deep, more than 1,000 engineers involved, and an expected 18-month timeline in 2023-2024. — [Cognition/Devin](https://devin.ai/customers/nubank)
- [Vendor] The case study reports 8x to 12x efficiency, which compares typical hours per data class with the hours spent prompting and reviewing Devin on that task. — [Cognition/Devin](https://devin.ai/customers/nubank)
- [Vendor] The "20x" cost figure compares Devin's running cost with an engineer's hourly cost only for the scope delegated to Devin, so it is not a whole-project saving. — [Cognition/Devin](https://devin.ai/customers/nubank)
- [Vendor] Nubank fine-tuned Devin on earlier manual migrations and built a benchmark, which doubled task completion scores and cut sub-task time from about 40 to about 10 minutes, and humans approved and merged each change. — [Cognition/Devin](https://devin.ai/customers/nubank)
- The page carries no publication date, and the older URL `cognition.com/blog/nubank` now returns HTTP 404. — [Cognition/Devin](https://devin.ai/customers/nubank)

#### Itaú Unibanco (mainframe, AWS Transform and Kiro)
- [Vendor] AWS describes a five-decade estate of COBOL, IMS, CICS, Db2, TPF Assembler and PL/I, with a "reimagine" approach run across 88+ autonomous communities. — [AWS case study, undated, 2026 copyright](https://aws.amazon.com/solutions/case-studies/itau-aws-transform-mainframe/)
- [Vendor] Reported results are discovery falling from three months to two weeks, unit test creation falling about 97%, testing effort falling 30%, and end-to-end migration time falling about 75% per application where both tools were used. — [AWS case study](https://aws.amazon.com/solutions/case-studies/itau-aws-transform-mainframe/)
- [Vendor] Kiro is adopted in selected applications only, and mainframe retirement remains a target for the end of 2028, so the programme is not complete. — [AWS case study](https://aws.amazon.com/solutions/case-studies/itau-aws-transform-mainframe/)
- [Vendor] The incident and deployment figures (99% and almost 3,000%) cover six years, so they should not be attributed to these AI tools. — [AWS case study](https://aws.amazon.com/solutions/case-studies/itau-aws-transform-mainframe/)

#### ANZ
- [Measured] An ANZ-authored paper reports over 100 participants and a six-week trial with a control group, in which mean time fell from 30.98 to 17.86 minutes per problem, a 42% improvement. — [arXiv 2402.05636, Feb/Apr 2024](https://arxiv.org/pdf/2402.05636)
- [Measured] Bugs and code smells fell significantly, while security was untestable because SonarQube produced only one non-zero vulnerability data point. — [arXiv 2402.05636](https://arxiv.org/pdf/2402.05636)
- [Press/Exec] After rollout to 3,000 engineers, ANZ had no settled way to measure collective value, usage was uneven, and a few niche teams received little value for reasons ANZ could not yet identify. — [iTnews, 19 Jul 2024](https://www.itnews.com.au/news/anz-examines-uneven-benefits-from-ai-augmented-coding-609907)

#### Commonwealth Bank of Australia
- [Exec] At full-year results on 13 August 2025, the CEO reported technology changes delivered up 35%, critical incidents down 30% and recovery time improved 25%, with no method disclosed and no clean attribution to AI. — [iTnews](https://www.itnews.com.au/news/cbas-leaders-are-keeping-a-close-watch-on-ai-metrics-619554)
- [Press] CBA built Lumos as an AI-driven accelerator for cloud preparation, and one executive cited 370 legacy applications scoped as candidates. — [iTnews](https://www.itnews.com.au/news/cba-builds-lumos-an-ai-driven-accelerator-to-prepare-applications-for-cloud-620396) (excerpt only)
- [Practitioner] A CBA engineering post describes the Copilot rollout as having mixed results in utilisation and efficacy, which led to a dedicated AI-powered engineering initiative from late 2024. — [CommBank Technology on Medium via reader mirror](https://hn.jakechampion.name/reader/https://medium.com/commbank-technology/the-evolution-of-ai-software-engineering-75a8a5a02c14) (excerpt only; full fetch returned 403)

#### Capital One
- [Practitioner/Press] The New Stack reports that Capital One deprecated an AI tool it once championed, and a search summary says the firm remains in exploration mode on agent fleets because quality, reliability and security are not yet in place. — [The New Stack](https://thenewstack.io/capital-one-developer-enablement/) (excerpt only; article body not retrieved)
- [Practitioner] Capital One published open-source Context Specs that treat context engineering as the primary lever for AI-assisted coding. — [Capital One Tech](https://www.capitalone.com/tech/open-source/open-source-context-specs/) (excerpt only)
- [Practitioner] A Capital One executive describes a cycle in which AI struggles with poorly structured and poorly tested code, and weak review makes this worse. — [DX podcast](https://getdx.com/podcast/how-capital-one-assesses-ai-readiness/) (excerpt only)

#### Bloomberg
- [Practitioner] (secondary) In a 2025 AI Engineer talk, Lei Zhang described 9,000+ engineers and hundreds of millions of lines of JavaScript, and said gains on proofs of concept, tests and scripts fell off quickly on complex legacy code. — [ZenML summary](https://www.zenml.io/llmops-database/ai-powered-developer-productivity-platform-with-mcp-servers-and-agent-based-automation); [talk page](https://ai.engineer/talks/what-we-learned-deploying-ai-within-bloomberg-s-engineering-organization)
- [Practitioner] (secondary) Bloomberg then focused on "uplift" agents, which scan for applicable patches and open PRs, and on incident-response agents, and open PRs and time-to-merge both rose. — [ZenML summary](https://www.zenml.io/llmops-database/ai-powered-developer-productivity-platform-with-mcp-servers-and-agent-based-automation)
- [Practitioner] (secondary) The talk gave no quantitative productivity, adoption or cost results. — [ZenML summary](https://www.zenml.io/llmops-database/ai-powered-developer-productivity-platform-with-mcp-servers-and-agent-based-automation)

#### Other financial firms
- [Exec/Press] Barclays and Anthropic announced on 1 October 2026 a target of Claude Code adoption by 50% of developers by end-2026 and a majority of engineers in 2027, with no specific controls or legacy results described. — [The Asian Banker, 2 Oct 2026](https://www.theasianbanker.com/updates-and-articles/barclays-expands-anthropic-s-claude-code-to-support-software-development-and-legacy-modernisation)
- [Press] (secondary) Santander reportedly had 17,000 staff using AI for software by June 2026 and AI writing 40% of code that month. — [Lucidate](https://lucidate.substack.com/p/banks-have-counted-the-hours-their)
- [Press] (secondary) Options Clearing Corporation reported writing tests up to 80% faster as a best case, Fiserv has over 8,000 engineers on Copilot, Prudential has over 2,300 staff on coding agents, and Man Group has about 500 technologists writing code with AI. — [Lucidate](https://lucidate.substack.com/p/banks-have-counted-the-hours-their)
- [Vendor] (secondary) A re:Invent 2025 session recap reports Danske Bank migrating 850 applications in 15 months, with COBOL-to-.NET and PL/1-to-Java conversion. — [DEV Community recap](https://dev.to/kazuya_dev/aws-reinvent-2025-digital-transformation-excellence-using-agentic-ai-from-vision-to-victory-mam204-1042) (excerpt only)
- [Vendor] (secondary) A news summary reports Fiserv completing a mainframe modernisation in 17 months against an estimated 29+. — [StartupHub](https://www.startuphub.ai/news/aws-transform-ai-driven-mainframe-modernization) (excerpt only)
- [Vendor] (secondary) A summary reports Western Union and insurer Unum converting 2.5 million lines of COBOL in about 1.5 hours, which measures conversion and not validation or production cutover. — [Feedbagel](https://feedbagel.com/post/western-union-unum-agentic-ai-framework-for-mainframe-modernization-at-scale-zen) (excerpt only)
- [Vendor] Thought Machine and AWS announced an AI core banking migration tool in September 2026, with no production customer metrics in the source. — [Softprom](https://softprom.com/de/aws-thought-machine-ai-core-banking-migration) (excerpt only)

#### Automotive and government
- [Practitioner/Vendor] (secondary) Mercedes-Benz and Capgemini presented the Global Ordering migration, which has about 10M lines of code and 20,000+ interfaces, and they moved a 1.3M-line COBOL pricing service to Java between about February and September 2025. — [ZenML summary](https://www.zenml.io/llmops-database/mainframe-to-cloud-migration-with-ai-powered-code-transformation)
- [Practitioner/Vendor] (secondary) That work was mostly replatforming, used human-written COBOL-to-Java "cookbook" examples and a facade that sent identical requests to both systems, reported zero go-live incidents, and still needed manual database access tuning. — [ZenML summary](https://www.zenml.io/llmops-database/mainframe-to-cloud-migration-with-ai-powered-code-transformation)
- [Vendor] Separately, Cognition says Mercedes-Benz is deploying Devin and Windsurf globally starting with legacy modernisation, and a repost claims an eight-month refactor took eight days, which I could not verify. — [Cognition](https://cognition.ai/blog/mercedes-benz-cognition) (excerpt only)
- [Measured, self-reported] The UK Government Digital Service trial ran from November 2024 to February 2025 and reported 56 minutes saved per working day from 424 survey responses, with no control group. — [GOV.UK, 12 Sep 2025](https://www.gov.uk/government/publications/ai-coding-assistant-trial/ai-coding-assistant-trial-uk-public-sector-findings-report)

#### COBOL, mainframe tooling and consultancy accounts
- [Vendor] IBM's claim that watsonx Code Assistant for Z translation beat ChatGPT 88% to 32% has no methodology that I could find, and I found no named bank outcome or independent evaluation. — [The Decoder](https://the-decoder.com/future-proofing-legacy-systems-ibms-ai-tool-converts-cobol-to-java/) (excerpt only, launch-era coverage)
- [Vendor/Practitioner] Thoughtworks describes CodeConcise, which builds a deterministic AST knowledge graph in Neo4j and then adds LLM explanations by graph traversal, and it went through three generations in about 18 months. — [martinfowler.com, 24 Sep 2024](https://martinfowler.com/articles/legacy-modernization-gen-ai.html)
- [Vendor] In a COBOL/IDMS proof of concept, Thoughtworks estimated reverse engineering per 10,000-line module could fall from about 6 weeks to about 2 weeks, and the 240 FTE-year programme saving is an estimate and not an outcome. — [martinfowler.com](https://martinfowler.com/articles/legacy-modernization-gen-ai.html)
- [Vendor] The same authors state that some questions need SME knowledge absent from the code, that GenAI adds little over mature tools for finding dead code, and that several ideas remain unvalidated with clients. — [martinfowler.com](https://martinfowler.com/articles/legacy-modernization-gen-ai.html)
- [Vendor] McKinsey's LegacyX material describes a multinational bank converting more than 100 risk models from SAS to Python using five squads of at least 25 agents each. — [McKinsey](https://www.mckinsey.com/about-us/new-at-mckinsey-blog/mckinseys-legacyx-rejuvenating-legacy-infrastructure-with-agentic-ai) (excerpt only; full fetch timed out)
- [Practitioner] An ITPro article reports practitioners saying COBOL experts remain necessary to define and validate transformations. — [ITPro](https://www.itpro.com/software/development/you-need-those-experts-to-even-define-what-these-transformations-are-cobol-developers-will-always-be-needed-even-as-ai-takes-the-lead-on-modernization-projects) (excerpt only)

### Inferences
- The recurring successful pattern is a deterministic structure step, followed by an LLM, followed by a behavioural check and human approval, as seen in the CodeConcise graph, the Nubank benchmark and scripts, and the Mercedes parallel-run facade.
- Comprehension and specification extraction appear to be more mature than direct translation, because Morgan Stanley, Thoughtworks and Itaú all put their strongest evidence there.
- Nubank's multiples probably do not transfer to heterogeneous legacy work, because its task was a large number of similar units with historical examples available for tuning.
- Bloomberg's and Capital One's accounts suggest that test coverage and linting are preconditions for agent value on legacy code, and that this limits results on the estates that most need modernisation.

### Gaps
- I found no reliable public account of AI coding agents at Two Sigma or Citadel, and results were interview-preparation and speculative blogs. The nearest hedge fund data point is the Man Group figure above.
- Wells Fargo results were job postings naming Devin, Claude Code, Cursor and Copilot, which do not establish any deployment or outcome. An example is [this posting](https://www.theladders.com/job/lead-specialty-software-engineer-ai-tooling-enablement-wellsfargo-irving-tx_87227777) (excerpt only).
- I found nothing substantive on Accenture's mainframe results. No telecom example had measured outcomes, since AT&T, BMW and Deutsche Telekom appeared only as talk titles or agendas.
- A search summary attributed a 20% productivity figure to Goldman president John Waldron and over 1 million monthly prompts to the GS AI Assistant, but I could not tie either to a specific source, so neither should be cited without checking.
- I did not retrieve the Forbes article of 6 August 2026 on Goldman (HTTP 403), which may contain more recent deployment detail: [Forbes](https://www.forbes.com/sites/bernardmarr/2026/08/06/how-goldman-sachs-is-using-agentic-ai-for-software-engineering-at-scale/).

## How are model risk, data residency, audit trail, segregation of duties, change management and regulator expectations handled for AI-written code?

### Takeaway
No regulator text I found sets rules specifically for AI-written code, so banks handle it by keeping it inside existing SDLC controls: agents produce artifacts, humans approve them, and pipelines test them. The important development is that the US model risk replacement guidance of April 2026 explicitly excludes generative and agentic AI, which leaves firms to rely on their own governance.

### Cited Findings

#### Firm-level controls
- [Exec] Citi's stated controls are that a human oversees all Devin tasks, agents cannot deploy code and only produce artifacts, and changes go through automated testing and human review. — [American Banker, 14 Jul 2025](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers)
- [Exec] Citi says agents access internal repositories through RAG and not external web sources, and CTO Griffiths lists entitlements, identity, security, quality checks and automated testing as requirements. — [American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers)
- [Measured] ANZ assessed IP, data security and privacy risk with its legal and security teams before its trial, and it required participants to read a resulting playbook. — [arXiv 2402.05636](https://arxiv.org/pdf/2402.05636)
- [Vendor] Itaú's generated code reportedly passed existing SonarQube and Veracode CI/CD checks on the first iteration, and extracted business rules went through a validation framework. — [AWS case study](https://aws.amazon.com/solutions/case-studies/itau-aws-transform-mainframe/)
- [Practitioner] (secondary) Bloomberg uses an AI gateway, a tool directory, platform-handled authentication, and tiered access in which production use requires quality controls. — [ZenML summary](https://www.zenml.io/llmops-database/ai-powered-developer-productivity-platform-with-mcp-servers-and-agent-based-automation)
- [Press] JPMorgan's CFO said its strategy focuses on minimising lock-in and maximising optionality, and Morgan Stanley chose to build on OpenAI models in-house. — [Webull transcript](https://www.webull.com/news/15741198075913216); [WSJ via Tiger Brokers](https://www-web.itiger.com/news/2540775365)

#### United States
- [Primary] SR 26-2, dated 17 April 2026, supersedes SR 11-7 and SR 21-8. — [Federal Reserve SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm)
- [Primary] Footnote 3 of the attachment states: "Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance." It adds that a bank's own risk management and governance practices should guide controls for tools not covered. — [SR 26-2 attachment](https://www.federalreserve.gov/supervisionreg/srletters/SR2602a1.pdf)
- [Commentary] One secondary source claims January 2026 Fed clarifications extended SR 11-7 to agentic AI, which conflicts with the primary text and should not be relied on. — [SR 11-7 search result](https://greenwichsoundcapital.com/articles/article-ai-model-risk-sr-11-7) (excerpt only; I could not confirm which result made the claim, so this attribution needs checking)
- [Law firm on primary] FINRA's 2026 Oversight Report, released 9 December 2025, lists coding among observed GenAI use cases and names agent risks: autonomy, scope creep, auditability of chained actions, sensitive data handling, and limited domain expertise. — [Debevoise, 12 Dec 2025](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)
- [Law firm on primary] FINRA's suggested considerations include human-in-the-loop checkpoints, monitoring agent system access, tracking agent actions, and guardrails, and it says rules remain technology-neutral. Its agent section is not written specifically about code. — [Debevoise](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)

#### EU
- [Regulator, excerpt] The Malta regulator's April 2026 article describes DORA change management as requiring transparency and governance, with segregation of duties and record-keeping. — [MFSA](https://www.mfsa.mt/publication/ict-change-management-under-the-digital-operational-resilience-act-dora/) (excerpt only; fetch returned 403)
- [Law firm] A Jones Day note says BaFin holds management bodies accountable for AI-related ICT risk, and that in-house AI development should follow robust development and change-management standards. — [JD Supra](https://www.jdsupra.com/legalnews/bafin-s-expectations-for-ict-risk-5787894/) (excerpt only)

#### Singapore
- [Law firm on primary] MAS published AI Risk Management Guidelines on 7 October 2026, covering generative AI and agents, with lifecycle controls including human oversight, testing, monitoring and change management expected by 7 October 2028. — [Allen & Gledhill, 21 Oct 2026](https://www.allenandgledhill.com/vn/publication/articles/34686/mas-publishes-ai-risk-management-guidelines-setting-out-supervisory-expectations-on-responsible-ai-adoption)
- [Law firm on primary] Firms remain accountable for third-party AI, should test it in their own context, and should have contractual visibility of provider updates, and MAS plans to consult on additional agentic guidance in 2027. The summary does not mention coding tools. — [Allen & Gledhill](https://www.allenandgledhill.com/vn/publication/articles/34686/mas-publishes-ai-risk-management-guidelines-setting-out-supervisory-expectations-on-responsible-ai-adoption)

#### UK
- [Law firm on survey] The BoE/FCA 2026 survey of 196 firms found 80% deploy agents, only 2% with broad autonomy, and coding assistance is listed among internal uses where firms accept agents. — [Lewis Silkin, 30 Oct 2026](https://www.lewissilkin.com/insights/2026/10/30/key-lessons-from-the-bank-of-england-and-fcas-2026-survey-102o6yl)
- [Law firm on survey] Deep technical understanding was reported by 77% of firms for internal systems and 24% for third-party systems, and controls were stronger before deployment than after. — [Lewis Silkin](https://www.lewissilkin.com/insights/2026/10/30/key-lessons-from-the-bank-of-england-and-fcas-2026-survey-102o6yl)
- [Commentary] The FCA's Mills Review, published 6 July 2026, focuses on retail financial services and agentic systems, so it bears on software delivery only indirectly. — [Freeths](https://www.freeths.co.uk/insights-events/legal-articles/2026/fca-s-mills-review-agentic-ai-consumer-duty-and-the-future-of-financial-services/) (excerpt only)

### Inferences
- Treating the coding agent as an untrusted contributor preserves segregation of duties with little new policy, because the author (agent plus instructing developer) is separated from the approver and from deployment.
- That separation has a weakness that I did not see public banks address: if the instructing developer also approves the agent's pull request, the author and the reviewer may effectively be the same person.
- SR 26-2's exclusion means a US bank's coding agent is likely to be governed under technology, third-party and change risk policies and not under formal model validation, though firms' actual classifications are not public.
- Audit trail for AI-written code is mostly inherited from source control and CI records, while FINRA's concern about reconstructing chained agent actions points to a gap that those records alone may not close.

### Gaps
- I found no bank's public account of data residency for coding agents, such as inference region, retention or zero-data-retention terms. Citi's internal-only retrieval is the nearest item.
- I found no SEC guidance bearing on AI-written code, although my search effort on the SEC specifically was limited.
- I did not read the DORA text or its change management technical standard, so article-level citations must be added from primary sources. My recollection is that the relevant hooks are Article 9 of DORA and the ICT change management article of the RTS in Delegated Regulation 2024/1774, and this is unverified in this research.
- I did not find an OCC-specific statement. Secondary sources say the OCC and FDIC acted jointly with the Fed, and this should be checked on occ.gov.
- I found no public enforcement action or supervisory finding specifically about AI-written code.

## What productivity numbers are reported, how were they measured, which were independently verified, and where did programmes stall or disappoint?

### Takeaway
I found no independently verified productivity figure for AI coding at any bank or capital markets firm in production. The strongest published data are either self-reported surveys or small controlled experiments on non-production tasks, and bank CFO statements in late 2026 are materially more cautious than developer-productivity claims.

### Cited Findings

#### Numbers by evidence strength

| Firm | Claim | Basis | Independent? | Source |
|---|---|---|---|---|
| ANZ | 42% less time per problem | Trial with control group, Python algorithm puzzles, self-reported time | No, authored by ANZ staff | [arXiv](https://arxiv.org/pdf/2402.05636) |
| UK government | 56 min/day saved | 424 survey responses, no control group | Government's own evaluation | [GOV.UK](https://www.gov.uk/government/publications/ai-coding-assistant-trial/ai-coding-assistant-trial-uk-public-sector-findings-report) |
| Nubank | 8-12x hours, 20x cost | Delegated scope only, method described | No, vendor | [Cognition](https://devin.ai/customers/nubank) |
| Itaú | 75% migration time per app | Selected applications, no method given | No, vendor | [AWS](https://aws.amazon.com/solutions/case-studies/itau-aws-transform-mainframe/) |
| JPMorgan | 10-20% efficiency | Executive statement | No | [Reuters via Yahoo](https://finance.yahoo.com/news/jpmorgan-engineers-efficiency-jumps-much-190410445.html) (excerpt only) |
| Bank of America | 20% in select SDLC parts | Executive statement | No | [Fortune](https://fortune.com/2025/11/05/bank-of-america-prioritizes-bigger-ai-initiatives-as-annual-spending-on-new-tech-increased-by-44-over-the-past-decade) (excerpt only) |
| Citi | 5-15% from Copilot, 100,000 hours/week from reviews | Executive statement, method undisclosed | No | [American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers) |
| Morgan Stanley | 280,000 hours, 9M lines reviewed | Executive statement, calculation undisclosed | No | [WSJ via Tiger](https://www-web.itiger.com/news/2540775365) |
| Goldman Sachs | 3-4x over earlier tools | Forecast | No | [CNBC](https://www.cnbc.com/2025/07/11/goldman-sachs-autonomous-coder-pilot-marks-major-ai-milestone.html) |
| CBA | Changes +35%, critical incidents -30% | Executive statement, not isolated to AI | No | [iTnews](https://www.itnews.com.au/news/cbas-leaders-are-keeping-a-close-watch-on-ai-metrics-619554) |

#### Measurement limits in the best evidence
- ANZ chose algorithmic problems instead of workplace application scenarios, and it relied on self-reported time without monitoring. — [arXiv 2402.05636](https://arxiv.org/pdf/2402.05636)
- ANZ's tests used a sample size of 17 in the hypothesis table, and its prose says experts benefited most although Table 3 shows the largest improvement for beginners (52% against 40%). — [arXiv 2402.05636](https://arxiv.org/pdf/2402.05636)
- The GOV.UK report warns that respondents may have overestimated time saved through optimism bias, and telemetry showed a 15.8% acceptance rate for suggested lines, with only 39% of users saying they committed AI-suggested code. — [GOV.UK](https://www.gov.uk/government/publications/ai-coding-assistant-trial/ai-coding-assistant-trial-uk-public-sector-findings-report)
- A secondary analysis dated 28 October 2026 concludes none of the banks' hour or percentage claims has been audited and no bank has published its method. — [Lucidate](https://lucidate.substack.com/p/banks-have-counted-the-hours-their)

#### Stalls and disappointments
- JPMorgan's CFO said benefits are not observable in quarterly earnings, token costs will offset some of them, and a one-shot rewrite of minor legacy tools "didn't work perfectly". — [Transcript on Webull, 13 Oct 2026](https://www.webull.com/news/15741198075913216)
- About one third of JPMorgan's Copilot seats were reportedly recently active in April 2026, according to a secondary account of a dashboard report. — [Lucidate](https://lucidate.substack.com/p/banks-have-counted-the-hours-their)
- Bloomberg's gains dropped off on complex legacy code, and pull requests and time-to-merge rose. — [ZenML summary](https://www.zenml.io/llmops-database/ai-powered-developer-productivity-platform-with-mcp-servers-and-agent-based-automation)
- ANZ's value metric remained unsettled after rollout to 3,000 engineers, and a few teams received little value. — [iTnews](https://www.itnews.com.au/news/anz-examines-uneven-benefits-from-ai-augmented-coding-609907)
- CBA's own engineers described Copilot results as mixed. — [CommBank Technology via reader mirror](https://hn.jakechampion.name/reader/https://medium.com/commbank-technology/the-evolution-of-ai-software-engineering-75a8a5a02c14) (excerpt only)
- Capital One deprecated an AI tool it once championed, and the tool and reason were not retrieved. — [The New Stack](https://thenewstack.io/capital-one-developer-enablement/) (headline only)
- Citi's CTO said agents were not ready for complex end-to-end features as of July 2025. — [American Banker](https://www.americanbanker.com/news/citi-is-rolling-out-agentic-ai-to-its-40-000-developers)
- Cross-industry coverage of a study of 700+ firms reports about 30% more agent-driven code, no significant rise in resolved issues, and 49% longer review time, but I saw only aggregators and not the study itself. — [Forkast](https://forkast.news/ai-coding-agents-write-30-more-code-and-resolve-zero-additional-issues-harvard-study-finds/) (excerpt only)

### Inferences
- Banks are reporting different units (hours, percentages, seats, lines reviewed), which prevents comparison between firms, and "lines reviewed" at Morgan Stanley is not the same as lines modernised.
- Gains appear to shift the bottleneck to review and verification, which is likely to bind harder in firms with mandatory human approval, although I found no bank-specific measurement of this.
- Bank of America's statement that gains are reinvested and JPMorgan's statement about earnings are consistent with each other: neither presents engineering AI as a reported cost saving.
- Citi's 30% supplier spending reduction may be the most financially concrete outcome, but it rests on a secondary report and may have causes other than AI.

### Gaps
- I found no third-party audit, academic replication or regulator review of any bank's coding productivity claim.
- I found no public post-incident report attributing a bank production failure to AI-written code. This absence does not show that such incidents have not happened, since firms have little reason to publish them.
- I found no public defect or rollback data comparing AI-migrated and human-migrated legacy code at a bank, including at Nubank, Itaú and Morgan Stanley.
- I found no publicly documented cancelled agent programme at a named bank, and available disappointments are partial or qualitative.
- The Citi and Lucidate-relayed earnings details were not checked against Citi's own Q3 2026 transcript, and the 100,000-hour figure is dated differently by sources, since American Banker carried it in July 2025 while Lucidate cites Reuters from October 2025.
