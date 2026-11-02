# AI agents beyond feature code across the SDLC in large organisations

Research date: 2026-11-02. Sources marked **(vendor)** sell the product they describe. Sources marked **(self-reported)** are a company describing its own internal use without external audit. Sources marked **(secondary)** are press or aggregators, used because I could not read the primary source.

## Large-scale migrations: what succeeded, what design made it succeed, and how much manual effort remained

### Takeaway
Migrations have the strongest and most repeatedly reported benefit of any stage, and the successful designs share a shape: a mechanical target state, deterministic discovery or codemods where possible, an LLM for the remainder, automatic validation with error-fed retries, and human review at the end. Almost all time savings are self-reported estimates against a hypothetical manual baseline, and review and rollout remain the human bottleneck.

### Cited Findings

**Airbnb, Enzyme to React Testing Library (March 2025 per [InfoQ](https://www.infoq.com/news/2025/03/airbnb-llm-test-migration/); self-reported)**
- Airbnb migrated nearly 3.5K React test files in six weeks against a manual estimate of about 1.5 years of engineering time. The estimate is a projection and not a measured baseline. — [Airbnb](https://airbnb.tech/?p=366)
- Each file moved through a per-file state machine with steps for the Enzyme refactor, Jest fixes, lint and tsc fixes, and completion, and a file advanced only after the previous step's validation passed. — [Airbnb](https://airbnb.tech/?p=366)
- Each retry received the validation errors and the latest version of the file. Most files finished within 10 attempts, and long-tail files were retried 50 to 100 times. — [Airbnb](https://airbnb.tech/?p=366)
- Prompts grew to roughly 40,000 to 100,000 tokens and could include as many as 50 related files plus few-shot and sibling-test examples. — [Airbnb](https://airbnb.tech/?p=366)
- The first bulk run migrated 75% of files in about four hours, and four days of "sample, tune, sweep" tuning raised this to 97%. — [Airbnb](https://airbnb.tech/?p=366)
- **Human effort remaining:** just under 100 files were fixed manually over about another week, within roughly six weeks of total engineering time. The post gives no dollar cost. — [Airbnb](https://airbnb.tech/?p=366)
- InfoQ reports that the original test intent and code coverage were preserved, which I could not confirm with independent measurement. — [InfoQ](https://www.infoq.com/news/2025/03/airbnb-llm-test-migration/)

**Slack, Enzyme to React Testing Library (22 May 2024, updated 3 October 2024; self-reported)**
- More than 15,000 tests were in scope. AST rules alone converted about 45% of code, the LLM alone succeeded 40-60% of the time, and the hybrid reached about 80% on selected files. — [Slack](https://slack.engineering/balancing-old-tricks-with-new-feats-ai-powered-conversion-from-enzyme-to-react-testing-library-at-slack/)
- The 80% figure comes from a manual quality review of nine files. On the larger evaluation, only about 500 of about 2,300 test cases across 338 files were converted, ran, and passed, and Slack reports about 22% developer time saved on that basis. — [Slack](https://slack.engineering/balancing-old-tricks-with-new-feats-ai-powered-conversion-from-enzyme-to-react-testing-library-at-slack/)
- **Human effort remaining:** developers verified all generated code, fixed about 20% of content, and finished what the tool left. Adoption was about 64% of converted files. — [Slack](https://slack.engineering/balancing-old-tricks-with-new-feats-ai-powered-conversion-from-enzyme-to-react-testing-library-at-slack/)

**Asana, Enzyme to React Testing Library (August 2026 per search result; the fetched copy shows no date; self-reported)**
- Asana had worked on the migration since 2022 and estimated it was still about five years from finishing. It finished in about a week and a half of engineering time over two calendar weeks. — [Asana](https://asana.com/inside-asana/migrating-off-enzyme-2-weeks.md)
- The cost was about $11K in model usage and $1K in infrastructure, against an estimated $6M of manual engineering. — [Asana](https://asana.com/inside-asana/migrating-off-enzyme-2-weeks.md)
- The setup was OpenAI Codex with up to four agents, each on its own directory, using one short prompt. Asana reports that elaborate setups with tickets, notes files, and sub-agents made results worse. — [Asana](https://asana.com/inside-asana/migrating-off-enzyme-2-weeks.md)
- **Human effort remaining:** engineers checked progress and opened pull requests each morning and evening. The main bottleneck was Asana's own tooling, including a lint step that sometimes took over ten minutes and differences between CI and local checks. — [Asana](https://asana.com/inside-asana/migrating-off-enzyme-2-weeks.md)

**Google, four migrations (arXiv 12 January 2025; experience report by its own description, not a controlled study)**
- The Google Ads int32 to int64 ID migration covered a 500+ million line code base with tens of thousands of locations across thousands of files. 80% of the code modifications in landed changelists were fully AI-authored, and engineers estimated a 50% reduction in total time including review and landing. — [Google paper](https://arxiv.org/pdf/2501.06972)
- **Human effort remaining in that case:** the paper states that in most cases a human needed to revert at least some incorrect or unnecessary model changes, and that each change needed careful rollout. — [Google paper](https://arxiv.org/pdf/2501.06972)
- In the JUnit3 to JUnit4 migration about 87% of AI-generated code was committed unchanged, and Google limited weekly change volume to avoid overwhelming reviewers. — [Google paper](https://arxiv.org/pdf/2501.06972)
- For Joda Time to java.time, Google estimates about 89% time saved on small clusters only, based on comparisons by team technical leads. Large dependency clusters remained a problem that needed careful ordering of changes and synchronisation with reviewers. — [Google paper](https://arxiv.org/pdf/2501.06972)
- The paper says prompting alone is not sufficient for anything but the simplest migrations, that deterministic AST techniques still have a role, and that code reviews and rollouts "can quickly become bottlenecks", so some work was deliberately slowed. — [Google paper](https://arxiv.org/pdf/2501.06972)

**Google, 39 migrations (arXiv 13 April 2025)**
- Three developers performed 39 migrations over twelve months, producing 595 code changes and 93,574 edits. The LLM generated 74.45% of the code changes and 69.46% of the edits. Developers estimated a 50% reduction in total time. — [Google paper](https://arxiv.org/abs/2504.09691)
- **Human effort remaining:** about a quarter of changes and 30% of edits did not come from the LLM, and the 50% figure is a developer estimate. — [Google paper](https://arxiv.org/abs/2504.09691)

**Amazon, Java 8/11 to 17 with Amazon Q (August 2024; self-reported and also marketing for a product Amazon sells)**
- Jassy reported that the average upgrade fell from about 50 developer-days to a few hours, that the savings equal an estimated 4,500 developer-years, that more than 50% of production Java systems were upgraded in under six months, and that developers shipped 79% of auto-generated code reviews without additional changes. — [Jassy quoted by Simon Willison](https://simonwillison.net/2024/Aug/24/andy-jassy-amazon-ceo/)
- AWS describes "tens of thousands" of production applications and $260M in annualised savings, and the savings come from host reductions due to Java 17 performance and not from the AI itself. — [AWS](https://aws.amazon.com/blogs/devops/amazon-q-developer-just-reached-a-260-million-dollar-milestone)
- The developer-years estimate was derived by counting migrated dependencies and assuming that each typically takes a developer a day or more by hand. — [AWS](https://aws.amazon.com/blogs/devops/amazon-q-developer-just-reached-a-260-million-dollar-milestone)
- **Human effort remaining:** the 79% figure implies that 21% of reviews needed changes. AWS does not describe the human role in these upgrades beyond developers being able to revise the agent's plan. — [AWS](https://aws.amazon.com/blogs/devops/amazon-q-developer-just-reached-a-260-million-dollar-milestone)

**Spotify, Fleet Management with the Honk background agent (6 November and 9 December 2025; self-reported)**
- Spotify reports more than 1,500 merged AI-generated pull requests and 60-90% total time savings on migrations compared with writing the changes by hand. Migration types include Java value types to records, Scio upgrades with breaking changes, Backstage frontend migration, and schema-bound configuration changes. — [Spotify part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)
- The agent replaced hand-written transformation scripts inside the existing Fleet Management system, while targeting, review, and merging stayed unchanged. The prior Maven updater script had grown past 20,000 lines. — [Spotify part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)
- Verifiers for formatting, build, and tests are hidden behind an MCP tool layer, activate according to repository contents, and block the pull request if they fail. Errors are filtered down to the relevant lines. — [Spotify part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- An LLM judge compares the diff with the prompt. It vetoes about a quarter of sessions across thousands of sessions, the agent course-corrects about half the time, and the most common trigger is the agent going outside the prompt's instructions. Spotify states it has not yet evaluated the judge with evals. — [Spotify part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- Spotify ranks the failure modes as no pull request (minor), a pull request failing CI (frustrating), and a pull request passing CI while functionally wrong (most serious). It publishes no overall success rate. — [Spotify part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- **Human effort remaining:** humans write the prompts and review and merge the pull requests. Verifiers run only on Linux x86, so macOS and ARM64 targets are not covered. — [Spotify part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)

**Salesforce (27 May 2026; self-reported)**
- Salesforce reports moving 33 API endpoints to a new architecture in 13 days against an estimated 231 person-days, in five pull requests, with the largest delivering 21 endpoints at 100% test coverage. — [Salesforce](https://salesforce.com/news/stories/how-engineering-became-agentic/)
- **Human effort remaining:** the article does not quantify it, and it gives no headcount or hours. Comparing calendar days with estimated person-days inflates the "18 times" ratio if more than one person worked on the migration. — [Salesforce](https://salesforce.com/news/stories/how-engineering-became-agentic/)
- Secondary coverage disagrees on the description, as one outlet calls it an API migration and another an Apex-to-Java migration. — [The Decoder](https://the-decoder.com/salesforce-claims-ai-agents-cut-a-231-day-migration-to-13-days-with-fewer-incidents/); [AICerts](https://www.aicerts.ai/news/?p=13874)

**Uber (mixed quality)**
- Uber migrated over 75,000 test classes from JUnit 4 to JUnit 5 using OpenRewrite and internal orchestration, which is primarily a deterministic approach. **(secondary)** — [daily.dev summary](https://app.daily.dev/posts/uber-migrates-75-000-test-classes-from-junit-4-to-junit-5-using-automated-code-transformation-vnaof82ob)
- For Java to Kotlin on an Android monorepo of more than 10 million lines, Uber's LLM drafts deterministic AST rules instead of migrating code, and each rule goes through CI and platform engineer review. The timelines are projections, and the summary is inconsistent, listing about 3 years for CI automation alone and about 4 years with LLM rule generation against a current pace of 8 years. **(secondary, date unclear)** — [ZenML summary of Uber talk](https://zenml.io/llmops-database/llm-driven-developer-experience-and-code-migrations-at-scale)
- Sonar describes Uber's use of Piranha and Polyglot Piranha for the Thrift to gRPC change across tens of millions of lines and for adding context to millions of lines of Go. — [Sonar](https://www.sonarsource.com/blog/automating-code-migrations-with-speed-and-accuracy/)
- Shepherd is listed as Uber's migration management agent, with no published results that I could find. **(secondary)** — [ZenML](https://www.zenml.io/llmops-database/building-internal-ai-agent-infrastructure-for-software-development-at-scale)

**dotnet/runtime, Copilot coding agent, as a non-migration baseline (March 2026, summarising a Microsoft post; secondary)**
- Over about ten months, 535 of 878 pull requests were merged (67.9%), with a 0.6% revert rate. Merge rate rose from 41.7% in the first month to about 72% after a detailed instructions file was added. Success was 80.0% at 1-10 lines, 64.0% at 101-500 lines, and 84.7% for cleanup and removal. — [Start Debugging](https://startdebugging.net/2026/03/copilot-coding-agent-dotnet-runtime-ten-months-data/)
- **Human effort remaining:** pull request generation outpaced review, and nine queued pull requests created roughly 5-9 hours of review work. — [Start Debugging](https://startdebugging.net/2026/03/copilot-coding-agent-dotnet-runtime-ten-months-data/)

### Inferences
- The same Enzyme to RTL migration appears with very different results across time: about 22% measured time saved at Slack in 2024 with Claude 2.1, 97% automated at Airbnb in 2025 with retry loops and large context, and a complete finish at Asana in 2026 with a single short prompt on a stronger agent. Both model strength and pipeline design differ, so this sequence cannot separate the two causes.
- Asana's finding that a simple prompt beat elaborate scaffolding suggests that some 2024-2025 pipeline engineering may become unnecessary, but the validation loop stays in every case. This rests on a single report.
- Migrations suit agents because the target is known and the existing test suite and compiler provide an oracle. This advantage is weakest when tests are themselves the migration target, and when the code passes CI while wrong, which is Spotify's most serious failure mode.
- Google's two reports of 50% total time reduction are much lower than the task-level figures of 87-89% and than the headline ratios from other companies, and Google is one of the few that includes review and rollout time. I would treat 50% as the more realistic programme-level figure for hard migrations.

### Gaps
- I found no Pinterest case of AI-driven migration. The only results were job postings and an MCP summary, and I could not confirm the case exists. — [Job listing](https://startup.jobs/principal-engineer-agentic-engineering-pinterest-7934747); [daily.dev](https://app.daily.dev/posts/pinterest-deploys-production-scale-model-context-protocol-ecosystem-for-ai-agent-workflows-gjxpm2osb)
- I found no Uber Java upgrade or Go monorepo LLM migration with measured results.
- No company publishes a post-migration defect rate or a rate of tests silently weakened. Migration failure rates are generally reported as the share of files not automated, not as defects that reached production.
- I found no independent audit of any savings figure.

## Testing: generated test quality and the risk of tests that mirror the implementation

### Takeaway
Testing has real measured deployment at Meta and Uber, and the strongest evidence comes where a filter decides what reaches humans, such as a coverage gain, a killed mutant, or a change-specific catch. Coverage is a weak proxy for quality, generation yields are low before filtering, and the mirroring risk remains incompletely measured.

### Cited Findings

**Meta TestGen-LLM (arXiv 14 February 2024)**
- On Instagram Reels and Stories, 75% of generated test cases built correctly, 57% passed reliably, and 25% increased coverage. Across test-a-thons it improved 11.5% of classes, and engineers accepted 73% of recommendations. — [Meta paper](https://arxiv.org/abs/2402.09171)
- The design filters out any test class that does not show measurable improvement over the original suite. — [Meta paper](https://arxiv.org/abs/2402.09171)
- **Human effort remaining:** engineers review all recommendations, and the 73% figure comes from test-a-thon settings instead of routine workflows. — [Meta paper](https://arxiv.org/abs/2402.09171)

**Meta ACH, mutation-guided generation (arXiv 22 January 2025)**
- ACH was applied to 10,795 Android Kotlin classes across 7 platforms, generating 9,095 mutants and 571 privacy-hardening tests. The equivalent-mutant detector reached precision 0.79 and recall 0.47, rising to 0.95 and 0.96 with simple pre-processing. Engineers accepted 73% of tests, and 36% were judged privacy-relevant. — [Meta paper](https://arxiv.org/abs/2501.12862)

**Meta catching tests (arXiv January 2026; blog 29 October 2026)**
- The paper analyses 22,126 generated tests. Change-aware methods produced 4x more candidate catches than hardening tests and 20x more than coincidentally failing tests, and rule and LLM assessors cut human review load by 70%. Of 41 candidate catches reported to engineers, 8 were confirmed true positives, and 4 of those would have caused serious failures. **(from search summary of the paper)** — [Meta paper](https://arxiv.org/pdf/2601.22832)
- The full-scale post reports that 589 engineers engaged (64% of outreach), that engineers reported a 60% true-positive rate, that 74 serious privacy bugs were caught at the diff stage in the first half of 2026, and that privacy SEVs dropped 20% over the same period. **(self-reported; no control group is described, so the 20% is a correlation)** — [Meta blog](https://engineering.fb.com/2026/10/29/security/catching-bugs-before-they-land-jittestings-human-on-the-loop-approach-at-full-scale/)
- **Human effort remaining:** engineers are contacted only for highly ranked candidates and confirm whether an observed behaviour change was intended, without usually reading test code. — [Meta blog](https://engineering.fb.com/2026/10/29/security/catching-bugs-before-they-land-jittestings-human-on-the-loop-approach-at-full-scale/)

**Uber AutoCover (ICSE-SEIP 2026 paper; data from August and September 2025)**
- AutoCover generates about 11% of new tests reviewed and added to Uber's code base. It is a LangGraph pipeline for preparation, generation, execution, and validation or repair, with mutation testing used in validation. — [Uber paper](https://homes.cs.washington.edu/~rjust/publ/auto_cover_icse_2026.pdf)
- The rate of viable tests, meaning passing tests that increase coverage, is about 20% for Java, 40% for Go, and 80% for Python. Viable IDE tests are explicitly accepted about 44% of the time. — [Uber paper](https://homes.cs.washington.edu/~rjust/publ/auto_cover_icse_2026.pdf)
- In a survey, 83% of active users and 40% of inactive users agreed that AI test generation improves productivity. Active users rated test quality good or excellent at 70%, and no inactive user did. Free-text complaints covered ignored project conventions (6 responses), bloat (4), speed (4), and missing support for project-specific guidelines (4). The paper addresses the mirroring risk directly: its Validator rejects change-detector tests, and its expert rubric rates tests that assert internal details as "Bad" and not landable. — [Uber paper](https://homes.cs.washington.edu/~rjust/publ/auto_cover_icse_2026.pdf)
- A claim of 21,000 developer hours saved and a 10% coverage increase appears only in a third-party summary, which I did not verify. **(secondary)** — [Ry Walker summary](https://rywalker.com/research/uber-coding-agents)

**Dotnet evidence and independent oracle research**
- In dotnet/runtime, merged agent code was 65.7% test code against 49.9% for humans, with test additions at 75.6% success. **(secondary)** — [Start Debugging](https://startdebugging.net/2026/03/copilot-coding-agent-dotnet-runtime-ten-months-data/)
- A 2024 study asked whether LLM oracles capture actual or expected behaviour, found them heavily influenced by naming conventions, and notes that generated tests are likely to be incorrect when the code is buggy. This is the closest study I found to the mirroring concern. — [arXiv 2410.21136](https://arxiv.org/html/2410.21136v1)
- An ASE 2025 study reports that LLM oracles had an average mutation score of 43% against 45% for human oracles on an unbiased dataset, which indicates comparable strength on that measure. — [Ernst et al.](https://homes.cs.washington.edu/~mernst/pubs/neurosymbolic-oracles-ase2025-abstract.html)
- The GEM paper states that recent studies identify oracle weakness, and not insufficient coverage, as the main limitation of LLM-generated tests, and it observes a gap between coverage and mutation score. — [GEM](https://sol.sbc.org.br/index.php/cibse/article/view/42441)

### Inferences
- Meta's sequence moves from coverage (TestGen-LLM) to mutants (ACH) to tests tied to a specific change (catching tests). This is a move away from coverage as a target and towards a defined fault, and it is the most credible response to mirroring because a test must fail on an injected or real behaviour change.
- Catching tests have a much higher reported true-positive figure at scale (60%) than in the paper (8 of 41, about 20%). The two numbers use different filters and different definitions, and the 60% is engineer-reported, so they should not be presented as an improvement trend.
- Acceptance rates measure engineer willingness to land a test and do not measure the test's ability to find bugs.

### Gaps
- I found no study measuring how often production LLM tests copy implementation behaviour, and no longitudinal data on bugs found by accepted tests except Meta's privacy SEV figures.
- I did not find a recent Google test generation paper with measured results within the search budget, and this is a gap in my search and not evidence of absence.

## Requirements, design, and spec-driven development

### Takeaway
This stage has the weakest evidence. Reports on AWS AI-DLC and Kiro are vendor-authored and mostly qualitative, independent practitioner evaluation is critical, and the one large empirical study finds no defect benefit from specification artifacts, although it did not test SDD tool output itself.

### Cited Findings
- **Thoughtworks evaluation (15 October 2025):** Birgitta Böckeler classifies SDD as spec-first, spec-anchored, and spec-as-source, and finds that all reviewed approaches are spec-first while few aim higher. — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Böckeler reports that Kiro produced four user stories and 16 acceptance criteria for a small bug, that Spec Kit was heavy for a mid-sized feature and produced duplicate classes because the agent ignored notes about existing code, and that Tessl's output was non-deterministic from the same spec. — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- Her critiques are one workflow for all task sizes, markdown review being more tedious than code review, a false sense of control when agents ignore instructions, an unclear target user, harder brownfield adoption, and the risk that spec-as-source combines the inflexibility of model-driven development with LLM non-determinism. This was a small hands-on evaluation and not a large codebase study. — [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- **Empirical null result (ESEM 2026, independent researcher):** across 88,052 pull requests in 119 open-source repositories, spec'd and unspec'd pull requests were indistinguishable in defect introduction after matching (-0.6 percentage points, p = 0.133), and specifications did not constrain the scope of AI-tagged changes (p = 0.997). — [Hill, ESEM 2026](https://drops.dagstuhl.de/storage/00lipics/lipics-vol394-esem2026/LIPIcs.ESEM.2026.84/LIPIcs.ESEM.2026.84.pdf)
- The paper's limitation matters: the artifacts are overwhelmingly references to issues and tickets, no repository in the sample commits SDD tool output, and the author states that SDD tool adoption remains untested. The paper also states that no vendor has published empirical evidence for its claims. — [Hill, ESEM 2026](https://drops.dagstuhl.de/storage/00lipics/lipics-vol394-esem2026/LIPIcs.ESEM.2026.84/LIPIcs.ESEM.2026.84.pdf)
- **Non-independent benchmark:** Uvik, a services firm, ran 50 Python tickets across five spec workflows and a control, and blind reviewers found 0.46 defects per merged ticket against 0.86 without specs. The spec phase consumed 35.1% of tokens in the spec arms, and the benefit depended on ticket type. **(vendor; from search summary)** — [Uvik](https://uvik.net/blog/spec-driven-development-benchmark/)
- **AWS AI-DLC at Dynata (15 October 2026; vendor):** Dynata reports that features typically spanning 3-4 sprints took about one sprint's worth of time, and that requirements alignment took a single structured day. The post gives no codebase size or team size, and its quality claims are qualitative. — [AWS](https://aws.amazon.com/blogs/architecture/how-dynata-scaled-ai-across-the-development-lifecycle-with-ai-dlc-and-kiro-ide/)
- **Human effort remaining at Dynata:** humans approve each stage and each code generation plan, leads validate design artifacts, steering files needed iterative tuning, and testing, edge-case hardening, and release preparation remained after the workshop. — [AWS](https://aws.amazon.com/blogs/architecture/how-dynata-scaled-ai-across-the-development-lifecycle-with-ai-dlc-and-kiro-ide/)
- **Other Kiro reports (vendor or partner):** Amorepacific describes spec mode in a legacy SAP ECC environment with a custom MCP server, and the snippet carries no numeric result. Leighton, a partner, gives a self-estimated "up to 6x". — [Amorepacific via AWS News](https://aws-news.com/article/2026-10-21-how-amorepacific-brought-ai-driven-development-to-sap-ecc-with-kiro); [Leighton](https://www.manchesterdigital.com/post/leighton/kiro-ai-spec-driven-delivery-and-what-it-means-for-the-future-of-software-development)
- Wipro, S&P Global, Persistent Systems, and NASDAQ are named only as experimenting with AI-DLC. **(secondary)** — [YourStory](https://yourstory.com/2025/09/devsparks-hyderabad-2025-aws-unveils-ai-driven-development-lifecycle)

### Inferences
- The Dynata workshop gain is at least partly attributable to putting product, leads, and developers in one room, so the requirements alignment figure may reflect the meeting format as much as the AI.
- Google's and Spotify's migration work suggests that a precise prompt with a verifiable target works well, which supports specificity but does not validate a general SDD methodology. Migrations have an oracle, and new-feature specifications generally do not.

### Gaps
- I found no controlled or audited study of Kiro, Spec Kit, or AI-DLC on a large existing code base, and no independent measurement of requirements quality.
- I did not read Spec Kit's own documentation or the Diaz et al. paper (arXiv 2609.00252) cited by [a blog post](https://codex.danielvaughan.com/2026/09/04/spec-driven-development-wisespec-requirements-quality-codex-cli-productivity-paradox/), whose content remains unverified.

## CI and build repair, flaky tests, dependency upgrades, and documentation

### Takeaway
Build repair has the only true A/B result in this research, and it shows a small but safe effect of about 2%. Flaky test repair has good production funnel data from Uber with a modest end-to-end yield. Dependency upgrades and documentation lack enterprise measurements of agents.

### Cited Findings
- **Google build repair (23 April 2024):** an 11-week 50/50 A/B test found about 2% less active coding time per changelist, about 2% less shepherding time, and about 2% more throughput, with no detectable difference in rollback rate or new sanitizer failures. About 34% of developers who hit a breakage in a month applied a fix. — [Google Research](https://www.research.google/blog/safely-repairing-broken-builds-with-ml)
- **Human effort remaining:** this is an IDE suggestion that the developer previews and applies, and it is not an autonomous agent. — [Google Research](https://www.research.google/blog/safely-repairing-broken-builds-with-ml)
- **Google test failure diagnosis (arXiv 13 April 2026, ICSE 2026):** AutoDebug posts a likely root cause for integration test failures into code review, with p50 latency of 56 seconds and p90 of 346 seconds. The version I fetched had unfilled placeholders for accuracy and scale. A search summary reported a "not helpful" rate of 5.8%, and the paper says that rate is below Google's 10% guideline. — [Google paper](https://arxiv.org/html/2604.12108); [Gentic summary, secondary](https://gentic.news/article/google-s-auto-diagnose-ai-hits-90)
- **Limits stated in that paper:** feedback came from a self-selected group, it covers one model and prompt, and logs lost from crashed components caused some failed diagnoses. — [Google paper](https://arxiv.org/html/2604.12108)
- **Uber FlakyGuard (arXiv 18 November 2025, with UT Austin):** over six months, 798 of 1,115 flaky tests were reproduced (71.6%), fixes were produced for 380 of those (47.6%), and 197 of those fixes were accepted and landed (51.8%). — [FlakyGuard](https://arxiv.org/html/2511.14002v1)
- **Reasons for rejection in that paper:** fixes ignored organisational test helpers, relaxed mock expectations in place of a proper fix, changed test semantics by removing or adding irrelevant assertions, or were hard to read, and developers sometimes fixed tests in parallel. All 19 surveyed developers rated the root cause explanations useful. — [FlakyGuard](https://arxiv.org/html/2511.14002v1)
- **FlakyDoctor (arXiv April 2024):** this LLM and program-analysis technique reported 57% and 59% success on two flakiness classes across 873 tests in 243 open-source projects, which is not a production deployment. — [FlakyDoctor](https://arxiv.org/pdf/2404.09398)
- **Dependency upgrades, research:** an FSE 2025 paper reports up to 23% repair success for an agentic approach and up to 19% for zero-shot prompting on the BUMP Java dataset of breaking updates. This is a benchmark and not enterprise deployment. — [He et al.](https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/38/Automatically-fixing-dependency-breaking-changes)
- **Dependency upgrades, non-LLM baseline:** a study of 502,752 Dependabot pull requests found it reduces technical lag and that developers are receptive. — [arXiv 2206.07230](https://arxiv.org/abs/2206.07230v2)
- **Dependency upgrades, vendor:** FOSSA reports that organisations using its fossabot agent merge updates over 50% faster. **(vendor; January 2026)** — [FOSSA](https://fossa.com/blog/autofix-enhanced-dependency-upgrades.md)
- **Documentation:** a study on legacy MUMPS and mainframe assembly found comments generally free of hallucination and useful, while no automated metric reliably predicted comment quality. — [arXiv 2411.14971](https://arxiv.org/abs/2411.14971v1)
- **Documentation:** a Javadoc study of 142 classes and 273 methods with three LLMs rated 58.8% equivalent and 27.7% superior to the original comments. This is an academic sample and not an enterprise deployment. — [arXiv 2408.14007](https://arxiv.org/html/2408.14007v2)
- **Stale guidance as a risk:** Asana found that outdated internal docs and agent guidance favouring Enzyme steered the agent wrongly, which shows that documentation is also an input to agents. — [Asana](https://asana.com/inside-asana/migrating-off-enzyme-2-weeks.md)

### Inferences
- From the FlakyGuard counts, 197 of 1,115 attempted tests ended with a landed fix, which is about 18% end to end. The accepted-fix percentage alone overstates the yield.
- FlakyGuard's rejected fixes that remove assertions are a direct instance of agents satisfying a green-CI goal by weakening the check. Spotify's judge also guards against disabling flaky tests, according to its [post](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3).
- The 2% result at Google is a useful anchor against larger self-reported claims, although it predates current agents and measures a narrow assist.

### Gaps
- I found no Meta or Microsoft production study of autonomous CI repair in this search. Spotify lists acting on CI checks as future work, which suggests this outer loop was not mature there in late 2025.
- I found no enterprise measurement of agent-generated documentation accuracy, and no peer-reviewed study of autonomous agents acting on dependency pull requests at enterprise scale.

## Incident response and SRE: benefits, limits, and reported accidents

### Takeaway
Diagnosis assistance has credible results, but the large remediation numbers are vendor self-reports with conflicting figures, independent benchmarks show low success, and the most widely reported accident involved an agent with excess permissions. Read-only diagnosis has better support than autonomous remediation.

### Cited Findings
- **Microsoft RCACopilot (arXiv May 2023, revised November 2023):** on a year of real Microsoft incidents, root cause category prediction accuracy reached up to 0.766, and the diagnostic collection component has been used for over four years. — [RCACopilot](https://arxiv.org/abs/2305.15778)
- **Azure SRE Agent (vendor and self-reported):** the GA post of March 2026 claims 1,300+ internal agents, 35K+ incidents mitigated, and 20K+ engineering hours saved, while the Customer Zero post of April 2026 claims 35K+ incidents handled, 50K+ developer hours saved, and App Service time to mitigation falling from 40.5 hours to 3 minutes. I read these figures on Microsoft's repository page, as the blog bodies did not load, and the page gives no methodology. — [Microsoft GitHub hub](https://github.com/microsoft/sre-agent)
- "Handled" and "mitigated" are not the same claim, and the 20K and 50K figures are not reconciled by Microsoft in anything I could read. — [Microsoft GitHub hub](https://github.com/microsoft/sre-agent)
- A Microsoft blog reports 89% positive responses to root cause analyses from Azure Container Apps engineers, covering over 90% of incidents, and the Azure Functions team reports a 30% reduction in time to mitigate. **(from search summaries; not read in full)** — [Microsoft blog](https://techcommunity.microsoft.com/blog/appsonazureblog/-/4462613); [Azure Functions summary](https://news.lavx.hu/article/from-coding-agents-to-cloud-automation-how-azure-functions-uses-ai-to-accelerate-incident-response)
- **Meta root cause ranking (24 June 2024; self-reported):** heuristic retrieval followed by a fine-tuned Llama 2 ranker placed the root cause in the top five suggested code changes for 42% of web monorepo investigations. This was a backtest at investigation creation time, and no live figure is given. — [Meta](https://engineering.fb.com/2024/06/24/data-infrastructure/leveraging-ai-for-efficient-incident-response/)
- **Meta's stated mitigations:** explanations that responders can reproduce and validate, feedback loops, and withholding low-confidence answers at the cost of recall. — [Meta](https://engineering.fb.com/2024/06/24/data-infrastructure/leveraging-ai-for-efficient-incident-response/)
- **Datadog Bits AI SRE (vendor):** Datadog reports that each new feature caused regressions elsewhere, which led it to build a replayable evaluation framework using labelled real incidents. Its blog says customers saw reduced time to root cause without giving numbers, and it publishes no accuracy percentage that I could find. — [Datadog](https://datadoghq.com/blog/building-bits-ai-sre/)
- **incident.io (vendor):** its documentation treats accuracy as the headline metric and adds "reach" to separate failures of reasoning from failures to find the evidence. A third-party review notes that a self-reported 90%+ accuracy has no independent validation, and that review comes from another company in the AI tools market. — [incident.io docs](https://docs.incident.io/investigations/measuring-accuracy); [Augment](https://www.augmentcode.com/tools/best-ai-sre-tools)
- **Independent benchmarks:** IBM and UIUC's ITBench reported that agents solved 13.8% of SRE scenarios in the February 2025 preprint, and the ICML 2025 version reportedly gives 11.4%. — [ITBench preprint](https://arxiv.org/abs/2502.05352); [ICML talk](https://slideslive.com/39044115)
- A 2026 benchmark, ORCA-bench, reports that agents hallucinate an implausible root cause in 7-40% of incident reports depending on the model. **(from search summary; not read in full)** — [alphaXiv](https://www.alphaxiv.org/abs/2607.28545.md)

**Accidents**
- **AWS, December 2025:** the Financial Times, citing four sources, reported a 13-hour disruption after engineers let Kiro make changes and it chose to "delete and recreate the environment". — [The Register, 20 February 2026](https://www.theregister.com/2026/02/20/amazon_denies_kiro_agentic_ai_behind_outage/)
- **Amazon's dispute:** Amazon attributes the event to misconfigured access controls and not to AI, says that it affected AWS Cost Explorer in one of two mainland China regions, says that Kiro requests authorisation by default while this engineer's role had broader permissions, and says that it added safeguards including mandatory peer review for production access. — [The Register](https://www.theregister.com/2026/02/20/amazon_denies_kiro_agentic_ai_behind_outage/)
- **Amazon retail, March 2026:** a nearly six-hour retail disruption was attributed to an erroneous code deployment. The FT, via secondary reports, described an internal note on a trend of incidents with "high blast radius" and "Gen-AI assisted changes", followed by a senior sign-off requirement for AI-assisted changes by junior and mid-level engineers. Reports disagree on the scope, and Amazon disputes that AI was the primary cause. **(secondary)** — [TechRadar](https://www.techradar.com/pro/amazon-is-making-even-senior-engineers-get-code-signed-off-following-multiple-recent-outages); [Ars Technica mirror](https://tagteam.harvard.edu/hub_feeds/3382/feed_items/17327753)

### Inferences
- The Azure figure of 40.5 hours to 3 minutes is unusual enough that it probably describes a specific incident class or a redefined metric, but I could not read the method, so it should not be presented as a general result.
- Benchmarks and vendor numbers are not directly comparable, as benchmarks use hard injected scenarios with autonomous scoring, while vendors count incidents in environments where they have deployed, often with a human present. Their gap is still large enough to justify scepticism.
- The AWS dispute does not need settling to learn from it. Both accounts agree that the agent's permissions exceeded what the task needed, and this points to least privilege and approval gates as necessary controls.

### Gaps
- I could not read the Azure blog posts in full, so I have no data on approval modes, the share of incidents mitigated without a human, or wrongful mitigations.
- I found no published false-remediation rate from any vendor, no independent evaluation of Bits AI or incident.io, and no published Amazon metric for its internal incident agents.
- I did not obtain OpenRCA's own success rate.

## Which stages have measured benefit and which have only anecdotes

### Takeaway
Evidence is strongest for migrations, followed by test generation and narrow build or flaky repair. Diagnosis has moderate evidence, autonomous remediation has only self-reports, and requirements and design have almost no measurement. Only one case in this research is a randomised experiment.

### Cited Findings
Evidence grades below are my own assessment, based on the sources cited in the earlier sections.

| Stage | Best evidence | Evidence type | Grade | Human effort remaining |
|---|---|---|---|---|
| Migrations | [Google](https://arxiv.org/abs/2504.09691), [Airbnb](https://airbnb.tech/?p=366), [Spotify](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) | Production counts, with self-estimated time savings | Strong on feasibility, moderate on size of savings | Review, rollout, long-tail files, prompt tuning |
| Test generation | [Meta ACH](https://arxiv.org/abs/2501.12862), [Uber AutoCover](https://homes.cs.washington.edu/~rjust/publ/auto_cover_icse_2026.pdf) | Production funnels and acceptance rates | Moderate; quality outcome data is sparse | Review of each test or of ranked candidates |
| Change-specific bug catching | [Meta](https://engineering.fb.com/2026/10/29/security/catching-bugs-before-they-land-jittestings-human-on-the-loop-approach-at-full-scale/) | Production count without a control group | Moderate, single company | Confirming intended behaviour changes |
| Build repair | [Google](https://www.research.google/blog/safely-repairing-broken-builds-with-ml) | Randomised A/B test | Strong, small effect, narrow assist | Developer applies the fix |
| Flaky test repair | [Uber FlakyGuard](https://arxiv.org/html/2511.14002v1) | Six-month production funnel | Moderate, single company | About half of fixes rejected; non-reproducible tests remain |
| Failure and root cause diagnosis | [Google AutoDebug](https://arxiv.org/html/2604.12108), [RCACopilot](https://arxiv.org/abs/2305.15778), [Meta](https://engineering.fb.com/2024/06/24/data-infrastructure/leveraging-ai-for-efficient-incident-response/) | Backtests, surveys, and expert review | Moderate | Responder validates the conclusion |
| Autonomous incident mitigation | [Azure SRE Agent](https://github.com/microsoft/sre-agent) | Vendor self-report with conflicting figures | Weak; [ITBench](https://arxiv.org/abs/2502.05352) is unfavourable | Not published |
| Dependency upgrades by agent | [He et al.](https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/38/Automatically-fixing-dependency-breaking-changes), [FOSSA](https://fossa.com/blog/autofix-enhanced-dependency-upgrades.md) | Benchmark and vendor claim; [Amazon](https://aws.amazon.com/blogs/devops/amazon-q-developer-just-reached-a-260-million-dollar-milestone) overlaps with the migration row | Weak outside Amazon | Not published |
| Documentation | [arXiv 2408.14007](https://arxiv.org/html/2408.14007v2) | Academic sample only | Weak; no enterprise data found | Not published |
| Requirements and design, SDD | [Dynata](https://aws.amazon.com/blogs/architecture/how-dynata-scaled-ai-across-the-development-lifecycle-with-ai-dlc-and-kiro-ide/), [Hill](https://drops.dagstuhl.de/storage/00lipics/lipics-vol394-esem2026/LIPIcs.ESEM.2026.84/LIPIcs.ESEM.2026.84.pdf), [Böckeler](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) | Vendor anecdote, an indirect null result, and a practitioner trial | Weak | All approvals and post-workshop work |

### Inferences
- Measured value appears where an automatic oracle exists, such as a compiler, a test suite, a coverage or mutation gate, or a historic fix label. Value claims become anecdotal where no oracle exists, as with requirements quality, or where failures are rare and expensive, as with remediation.
- Effect sizes fall as measurement rigour rises: ratios of 18x and 12x-plus come from estimated baselines, 50% comes from engineers including review and rollout, and about 2% comes from the sole A/B test. The tasks differ, so this pattern is suggestive and does not prove inflation.
- The recurring remaining human work is review capacity and rollout, which [Google](https://arxiv.org/pdf/2501.06972) and [dotnet/runtime](https://startdebugging.net/2026/03/copilot-coding-agent-dotnet-runtime-ten-months-data/) both report as the bottleneck.

### Gaps
- Nearly all evidence comes from companies describing their own success, so survivorship bias is likely, and I found very few published accounts of a failed or abandoned agent-led migration.
- Several findings rest on search summaries instead of a full reading, and they are marked above. These include the Meta catching test paper numbers, ORCA-bench, Uvik, and Microsoft's blog figures. The original Airbnb Medium post returned HTTP 403, so I used Airbnb's own tech site copy.
