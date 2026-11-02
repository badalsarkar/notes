# Coding agents at product engineering companies with large production codebases

Research date is 2026-11-02. Every company metric below is self-reported unless a bullet says otherwise, and I found no independent audit of any company's figure.

**Evidence labels used on each case study**

- **[P]** means that I read the company's own post or talk page.
- **[V]** means that the source is a customer story written by a vendor that sells to the company.
- **[S]** means that I read a secondary summary or an aggregator, and the primary source was not read.
- **[Sn]** means that the claim comes from a search-result summary and the page was not opened, so it needs checking before it is quoted.

**Contents**

- [Case studies by company](#case-studies-by-company)
- [Metrics, their definitions, and superseded claims](#metrics-their-definitions-and-superseded-claims)
- [Common architecture and points of disagreement](#common-architecture-and-points-of-disagreement)

## Case studies by company

### Takeaway

Stripe, Ramp, Spotify, Shopify, Uber, Dropbox, DoorDash, LinkedIn, Duolingo and Notion run their own background-agent platforms, and most of them wrap a third-party or open-source agent loop rather than writing one. Faire is the notable reverse case because it built a system and then replaced it with a vendor product, while Coinbase, Intercom, Salesforce and Block's public evidence is mainly about adopting or distributing agents rather than about a documented sandboxed platform.

### Cited Findings

#### Stripe: Minions [P]

- **Built versus bought:** Stripe built a custom harness and runs the core agent loop on a fork of Block's goose, which it modified to interleave agent loops with deterministic code. — [Stripe Part 1, 2026-02-09](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- **Context:**
  - Most rules are scoped to subdirectories or file patterns because global rules would fill the context window in a repository of this size. — [Stripe Part 2, 2026-02-19](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
  - Stripe standardized on Cursor's rule format and syncs those rules for Claude Code, so that minions and human tools read the same guidance. — [Stripe Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
  - Toolshed, an internal MCP server, holds nearly 500 tools, and each minion receives a small curated subset by default. — [Stripe Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
  - MCP tools run on likely links before the run starts, so that the agent begins with context already loaded. — [Stripe Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- **Execution:** Runs happen on devboxes, which are standard AWS EC2 instances that engineers also use, kept in a pre-warmed pool with a 10-second readiness target. They use QA data, have no production access and have limited network egress, which is why minions run without human permission checks. — [Stripe Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- **Orchestration:** Blueprints are code-defined workflows that mix deterministic nodes, such as linting and pushing, with agent nodes, such as implementing a task or fixing CI failures. — [Stripe Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- **CI feedback:** A local executable runs selected lints in under five seconds on each push, and CI draws on a suite of over three million tests. The standard blueprint allows two CI rounds and then hands the branch to a human, because returns diminish and each run costs tokens, compute and time. — [Stripe Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [Stripe Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- **Triggers:** Slack is the most common trigger, and runs can also start from internal docs, feature flag tools and ticketing tools, including a button on flaky-test tickets. — [Stripe Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- **Review:** The requesting engineer asks another Stripe engineer to review the PR, and the PRs are human-reviewed but contain no human-written code. — [Stripe Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents)
- **Metrics:** Stripe reports over 1,300 merged PRs per week that are fully minion-produced and human-reviewed, up from over 1,000 in Part 1. It publishes no percentage of all PRs. — [Stripe Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- **Lessons:** Stripe credits earlier developer-productivity investment, and it recommends shifting feedback left, constraining LLMs to contained steps and keeping tool sets small. — [Stripe Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)

#### Ramp: Inspect [P, V, paywalled S]

- **Built versus bought:** Ramp built the platform and adopted OpenCode as the agent because OpenCode is server-first with a typed SDK and plugin system. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent)
- **Why not buy:** Local machines could run only one or two agent sessions at a time, and most third-party harnesses lacked internal integrations such as telemetry and feature flags, so they could not verify their own changes. — [Pragmatic Engineer, 2026-08-25, partly paywalled](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect)
- **Context:** The sandbox is connected to Sentry, Datadog, LaunchDarkly, Braintrust, GitHub, Slack and Buildkite, so that the agent can run tests, read telemetry, query flags and check frontend changes visually. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent)
- **Execution:** Each session runs in a sandboxed VM on Modal, and repository images are rebuilt and snapshotted every 30 minutes. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [Modal customer story, 2026-02-19](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal)
- **Triggers:** Ramp offers Slack with a repository classifier, a web interface with hosted VS Code, a Chrome extension for selecting React elements, GitHub PR discussions and voice. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent)
- **Review:** The API opens the PR with the initiating user's GitHub token, which prevents that user from approving their own change. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent)
- **Adoption:** Ramp did not mandate Inspect, and it relied on public Slack usage, multiplayer sessions and managed-device distribution of the extension. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent)
- **What failed:** The first version was a Chrome extension for visual edits. Engineers did not need it for one-line edits, and its local dev setup was too complicated for non-developers, so the team moved to remote environments. Version 2 was released in November 2025. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect)
- **Team and scale:** The team has about 5.5 people, more than 150 engineers have contributed, more than 200 agents run on the platform, sessions passed one million in July 2026 and environment spin-up takes under five seconds. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect)
- **Metrics:** The percentage history is inconsistent and is covered in the metrics section below.

#### Spotify: Honk on Fleet Management [P]

- **Built versus bought:** Spotify built a small internal CLI that delegates to swappable agents and LLMs, runs MCP-based formatting and linting, judges diffs with an LLM, uploads logs to GCP and captures MLflow traces. — [Spotify Part 1, 2025-11-06](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)
- **Agent history:**
  - Goose and Aider worked on small tasks but did not reliably produce mergeable PRs across thousands of repositories. — [Spotify Part 2, 2025-11-24](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)
  - A homegrown loop with 10 turns per session and three retries failed on cascading multi-file changes and lost the task when context filled. — [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)
  - Claude Code became the top performer, with about 50 migrations and most of the merged background-agent PRs. — [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)
- **Context:** Spotify deliberately withholds code search and documentation tools, and it puts context into large, version-controlled static prompts or generates prompts with separate workflow agents. — [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)
- **Tool limits:** The agent has a verify tool through MCP, a limited Git tool that cannot push, and an allowlisted Bash. — [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)
- **Execution:** The agent runs in a container with limited permissions, few binaries and virtually no access to surrounding systems, and surrounding infrastructure handles pushing and Slack. — [Spotify Part 3, 2025-12-09](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- **Verification:** Verifiers are hidden from the agent and activate by repository contents, such as a `pom.xml`. They run through a Claude Code stop hook before a PR opens, and a failure prevents the PR. — [Spotify Part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- **LLM judge:** A judge compares the diff with the prompt, vetoes about a quarter of thousands of sessions, and the agent corrects itself after about half of the vetoes. Spotify says it has yet to invest in evals for the judge. — [Spotify Part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- **Triggers:** Tasks can start from Slack and GitHub Enterprise through MCP, and a workflow agent gathers details before handing a prompt to the coding agent. — [Spotify Part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)
- **Metrics:** Spotify reports more than 1,500 merged agent PRs and 60–90% time savings on migrations compared with writing by hand. — [Spotify Part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)
- **Worst failure mode:** A PR that passes CI but is functionally incorrect is ranked as the most serious failure because it erodes trust. — [Spotify Part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- **Later limits:** A migration touching about 1,800 direct pipelines rolled out 240 PRs, saved an estimated 10 engineering weeks and ran over six months. A context file adapted from a human guide was insufficient until explicit mapping tables were added, Scio pipelines were excluded, and BigQuery and dbt repositories rarely had build-time tests, so owning teams tested manually. — [Spotify Part 4, 2026-04-22](https://engineering.atspotify.com/2026/4/background-coding-agents-dataset-migrations-honk-part-4)

#### Shopify: River on Aquifer [P for architecture, S for the CEO post]

- **Built versus bought:** Shopify built Aquifer, an internal agent-running substrate, and River is one Nix-built profile on it. The post does not name the underlying model or a purchased agent. — [Shopify, 2026-05-28](https://shopify.engineering/under-the-river)
- **Architecture:** A Postgres-backed session with an append-only event log is the durable record. The harness loop runs outside the sandbox and can be replaced, and session cells exit when idle and can resume on another host. — [Shopify](https://shopify.engineering/under-the-river)
- **Context:** Shopify consolidated into one monorepo called World in spring 2024 and built dev environments, CI and production images on Nix. River also has a memory of company information, according to a transcription of Tobi Lütke's post. — [Shopify](https://shopify.engineering/under-the-river); [third-party transcription, 2026-05-09](https://hq-raydata-co.pages.dev/vault/06-reference/2026-05-09-tobi-lutke-river-public-channel-agent/)
- **Triggers:** River responds to `@river` in public Slack channels and does not support direct messages. Automations and CI or batch jobs are separate invocation types on the same substrate. — [Shopify](https://shopify.engineering/under-the-river)
- **Review:** The engineering post does not describe a formal review process, while the transcription describes River's monorepo PRs as human-reviewed. — [Shopify](https://shopify.engineering/under-the-river); [transcription](https://hq-raydata-co.pages.dev/vault/06-reference/2026-05-09-tobi-lutke-river-public-channel-agent/)
- **Metrics:** Shopify reports 59,918 sessions in 5,170 channels, 7,000+ people touched and 3,536 merged River-coauthored PRs in a 30-day window, with a median of 19 minutes and 50 tool calls per session. It also says that one in eight merged PRs is coauthored by River. — [Shopify](https://shopify.engineering/under-the-river)
- **Merge rate:** River's merge rate reportedly rose from 36% to 77% over two months without retraining or switching the model, and the credited cause was people watching failures and recording what River should have known. — [transcription, not checked against the X original](https://hq-raydata-co.pages.dev/vault/06-reference/2026-05-09-tobi-lutke-river-public-channel-agent/)
- **What failed:** Consolidating into one repository broke CI, which had to scale by roughly an order of magnitude, and local private agents hit a ceiling because their learnings stayed with one person. — [Shopify](https://shopify.engineering/under-the-river)
- **Adoption pressure:** Lütke's April 2025 memo reportedly requires teams to show that AI cannot do a job before requesting more people. — [India TV, Sn](https://www.indiatvnews.com/technology/news/shopify-ceo-says-ai-comes-first-teams-must-prove-ai-can-t-handle-a-task-before-hiring-new-people-is-this-the-future-of-work-2025-04-08-984515)

#### Uber: Minion, uReview, AutoCover, Validator and supporting platform [P, partly paywalled S]

- **Built versus bought:** Uber builds the platform and buys agents and models. Claude Code usage rose from 32% in December 2025 to 63% in February 2026, the platform sits on Michelangelo, and it includes a model gateway. — [Pragmatic Engineer, 2026-03-10, Minion section paywalled](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development)
- **Minion:** Minion is an internal background-agent platform with monorepo access. Its lineage runs from a container prototype to DevPod and then to Minion, and it connects to Shepherd for migrations and Code Inbox for review routing. — [Summit session page, 2026-05-07](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/)
- **Triggers:** Minion reportedly takes prompts from web, Slack or the command line. — [Port analysis, S](https://software-factories.port.io/uber)
- **Context:** Uber's AI Context Graph has 24 million nodes and 80 million edges. A grounded agent answered correctly in 38 seconds, while an ungrounded agent took 20 minutes 9 seconds and wrongly concluded that the dataset was unqueryable. This is a single example, not a benchmark. — [Uber, 2026-08-27](https://www.uber.com/us/en/blog/efficient-software-factory/)
- **Six building blocks:** The talk's sections are Model Gateway, MCP Gateway, DevPods, a skills marketplace, the context graph and Cortana. The page does not list them together, so this list is inferred from section headings. — [AI Engineer World's Fair 2026](https://ai.engineer/talks/17-YSUHo6Lk-agentic-sdlc-at-uber-building-blocks-ubers)
- **uReview:**
  - Uber built uReview because third-party tools produced many false positives, were coupled to GitHub while Uber uses Phabricator, and could not reach internal systems. — [Uber, 2025-08-12](https://www.uber.com/blog/ureview/)
  - Single-shot prompting produced hallucinated issues and duplicates, so Uber moved to chained generation, grading and filtering steps and pruned readability comments. — [Uber](https://www.uber.com/blog/ureview/)
  - About 75% of comments are marked useful, and over 65% are addressed in the same changeset compared with 51% for human comments. The post states ~65,000 diffs as both weekly and monthly, which it does not resolve. — [Uber](https://www.uber.com/blog/ureview/)
- **AutoCover:**
  - AutoCover generates 5,000+ unit tests per month. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development)
  - A summary of an ICSE-SEIP paper reports about 11% of new reviewed tests and success rates of about 20% for Java, 40% for Go and 80% for Python, with the authors stating that coverage is not effectiveness. I could not open the paper because the fetch returned 403. — [Port summary](https://software-factories.port.io/uber); [ACM DOI](https://dl.acm.org/doi/10.1145/3786583.3786918)
- **Validator:** Validator and AutoCover were presented at LangChain Interrupt in May 2025. A search summary describes Validator as an IDE-embedded LangGraph agent that combines an LLM sub-agent with deterministic linters. — [Ry Walker summary](https://rywalker.com/research/uber-coding-agents)
- **Superseded claim:** The 21,000 hours figure is often attached to AutoCover alone, but one summary says it covers the coding agents collectively. The 10% coverage figure is talk-only. — [Ry Walker summary](https://rywalker.com/research/uber-coding-agents)
- **What failed:**
  - For a JUnit 4 to 5 migration covering 75,000+ test classes, generative AI on several files at once failed, so Uber used OpenRewrite and limited AI to debugging test and build failures. — [Uber, 2026-04-07](https://www.uber.com/us/en/blog/junit-migration/)
  - Exposing many MCP tools loaded roughly 50K–70K tokens of schema per session, which led Uber to code mode, CLI resolution and tool search. Prompt-cache expiry on idle gaps led to a one-hour cache TTL for interactive sessions. — [Uber, 2026-08-27](https://www.uber.com/us/en/blog/efficient-software-factory/)
  - Skills had duplicated work, poor discoverability and uneven quality, and CI capacity and reviewer attention are named constraints. — [AI Engineer talk](https://ai.engineer/talks/17-YSUHo6Lk-agentic-sdlc-at-uber-building-blocks-ubers)
- **Cost:** AI costs are up 6x since 2024. Uber uses live cost counters, spend tiers with manager sign-off and alerts at 50%, 80% and 100% of expected spend rather than strict caps. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development); [Uber](https://www.uber.com/us/en/blog/efficient-software-factory/)
- **Adoption:** Uber's speakers report that top-down mandates are less effective than engineers sharing wins. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development); [Summit session page](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/)

#### Dropbox: Nova [P]

- **Built versus bought:** Third-party agents suit local iteration but do not fit Dropbox's Bazel monorepo and on-prem build and test infrastructure, so Dropbox built one platform for interactive, background and service workflows. Nova runs multiple unnamed agents behind one interface. — [Dropbox, 2026-05-21](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **Context:** Context comes from the task description, Slack threads, localized AGENTS.md files, test logs and notes carried between attempts, and Dash and MCP integrations are planned to expand it. — [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **Execution and triggers:** Each session has an isolated environment with a codebase snapshot at a commit. Triggers include the web UI, CLI, API, CI failures, the Deflaker flaky-test workflow, RenovateBot breakages and production crash alerts. — [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **Verification and publishing:** Callers supply validation commands, failures feed back up to a configured limit such as five, and publication happens outside the agent with one branch per session. — [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **What failed:**
  - An earlier Goose-based migrator had no interactivity, so failed runs often could not be recovered. — [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
  - Highly repeatable migrations were often better handled by owners with a shared runbook. — [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
  - Agents managing their own CI loops waited for hours or validated against the wrong tests, so that control moved out of the agent. — [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **Metrics:** The post gives no success rates or adoption numbers. — [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)

#### DoorDash: Flux [S, primary returned 403]

- **Built versus bought:** DoorDash built Flux because, in its argument, hosted agents force a choice between sending sensitive code to a third party and opening a path back into internal systems. The design remains modular. — [ZenML summary, 2026-08](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks); [DoorDash primary, not read](https://careersatdoordash.com/blog/delegating-engineering-work-to-cloud-based-agents/)
- **Execution:** Sandboxes use Firecracker microVMs with a p95 setup target under five seconds. — [ZenML summary](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks)
- **Context and orchestration:** Agent Gateway is an MCP gateway to CI, observability, issue trackers and code search. YAML playbooks combine agentic and deterministic steps and declare the tools they need. — [ZenML summary](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks)
- **Triggers:** Surfaces include Slack, GitHub, cron, CLI and conversational skills. — [ZenML summary](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks)
- **Metrics:** DoorDash reports about 130,000 engineering tasks in one month, more than 25,000 automated code reviews per week, more than 10,000 playbook invocations per week and more than 300 playbooks. No share of merged PRs is given. — [ZenML summary](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks)
- **Lessons:** DoorDash started with automated code review because it was frequent and measurable, and it found that public threads built team habits better than private per-run Slack channels. — [ZenML summary](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks)
- **Claude Code:** Anthropic's customer page reports CTO Andy Fang saying that Claude Code was introduced in 2025 and correlates with team throughput. — [Anthropic customer page, V, Sn](https://claude.com/customers/doordash-boris-office-hours)

#### Faire: Samurai replaced by Cursor Cloud Agents [V]

- **Built versus bought:** Faire built Samurai on self-hosted infrastructure, found that hiring, machine setup and upkeep were expensive, and moved to Cursor. The vendor wrote this account, so it has an interest in the conclusion. — [Cursor, 2026-05-26](https://cursor.com/blog/faire)
- **Context and execution:** Agent-led onboarding inspects each repository and produces an editable environment configuration, or teams define a Dockerfile. Agents run in isolated VMs. — [Cursor](https://cursor.com/blog/faire)
- **Triggers:** Triggers include a designated Slack bug channel, CI failures on a PR, and `@cursor` in Slack threads. — [Cursor](https://cursor.com/blog/faire)
- **Migration:** Swarm, built on Cursor, assigns MobX-to-React tasks to cloud agents and starts the next task when a PR merges. The work was estimated at 18 months for a full team, and one engineer now runs it. — [Cursor](https://cursor.com/blog/faire)
- **Metrics:** Cursor reports a doubling of weekly PR throughput without defining it, and 2,000+ automated runs per week across 25+ Automations. — [Cursor](https://cursor.com/blog/faire)

#### Coinbase: Cursor plus internally built agents [V, Sn]

- **Built versus bought:** Coinbase buys Cursor for over 2,400 engineers, and its Superbuilders group built a Slack coding agent. — [Cursor, 2026-06-23](https://cursor.com/blog/coinbase)
- **Other tools:** Greptile's page says that Coinbase built its own background-agent system and uses Cursor, Claude and OpenCode, and that Greptile has reviewed about 25,000 PRs. — [Greptile, V, Sn](https://www.greptile.com/customers/coinbase)
- **Triggers:** Linear tickets, Plan Mode and the Slack agent are the described entry points. — [Cursor](https://cursor.com/blog/coinbase)
- **Metrics:** Agents create 75% of PRs across cloud and local, PRs merged per engineer rose 55% since the start of the year, and some teams moved from 20 days to under 2 days from idea to production. No time window is given for the 75%. — [Cursor](https://cursor.com/blog/coinbase)
- **CEO figure:** Brian Armstrong reportedly said that agents write more than 50% of code, which is a different metric from PR share. — [OfficeChai, Sn](https://officechai.com/ai/ai-agents-are-now-writing-more-than-50-of-code-at-coinbase-ceo-brian-armstrong)
- **Adoption:** Coinbase used "agent speedruns," which are 30-minute sessions in which every developer must ship a PR with Cursor. These grew from 50–70 PRs to over 500 PRs. — [Cursor](https://cursor.com/blog/coinbase)
- **Mux:** A search summary reports 39.6 PRs per engineer for Mux users against an 11.4 baseline in April 2026. The primary page returned 403, and a mirror redirected to an unrelated site, which I did not follow. Mux users are likely self-selected. — [Coinbase, not read](https://www.coinbase.com/blog/coding-had-a-concurrency-problem-how-mux-helped-solve-it)

#### Block: goose [S, Sn]

- **Built versus bought:** Block built goose and open-sourced it, and Stripe's fork and Dropbox's earlier migrator show that it was reused elsewhere. — [Stripe Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **Usage:** Forbes reportedly cites CTO Dhanji Prasanna saying that about two-thirds of more than 10,000 employees use goose weekly and save eight to ten hours a week. The page returned 403, and the savings are unmeasured self-report as far as I could determine. — [Forbes, 2025-11-18, Sn](https://www.forbes.com/sites/richardnieva/2025/11/18/block-cto-dhanji-prasanna-cio-next/)
- **Layoffs:** Block cut about 4,000 jobs, about 40% of its workforce, in February 2026 and attributed the decision to AI tools, and commentators dispute how much of it AI explains. — [Forbes, 2026-02-27, Sn](https://www.forbes.com/sites/petercohan/2026/02/27/block-stock-pops-16-on-40-layoffs-where-aipocalypse-may-strike-next/); [Bloom commentary, Sn](https://adambloom.me/2026/03/08/block-case-study-the-clearest-red-pill-moment-in-corporate-history/)

#### LinkedIn [S from a podcast with LinkedIn engineers]

- **Built versus bought:** LinkedIn uses GitHub Copilot for foreground work, augmented with MCP tools and generated instruction files, and it built background agents in-house. Prince Valluri advises solving company-specific problems instead of rebuilding Copilot or Cursor. — [InfoQ podcast, 2025-12-10](https://www.infoq.com/podcasts/platform-engineering-scaling-agents)
- **Context:** A semantic index and RAG system cover code and engineering knowledge, and specs make scope, allowed tools and acceptance criteria explicit. — [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents)
- **Execution and review:** Agents run in a remote restricted sandbox with their own auditable identity, the platform handles GitHub auth and PR creation, and agents cannot merge. — [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents)
- **Evals:** Evals use tens or hundreds of thousands of historical human-reviewed PRs plus verifiable checks such as build success. — [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents)
- **Metrics:** Thousands of developers use the tools daily, and no productivity or PR metrics were shared. — [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents)

#### Duolingo [P]

- **Built versus bought:** Duolingo built a thin platform on Temporal with a CodingAgent library that wraps Codex CLI and the Claude Code SDK, so that switching agents takes one enum value. — [Duolingo, 2025-12-11](https://blog.duolingo.com/agentic-workflows/)
- **Triggers and review:** Employees run JSON-defined or custom workflows from an internal tools list, and PRs come from a shared GitHub App bot account. — [Duolingo](https://blog.duolingo.com/agentic-workflows/)
- **Limits:** The post reports no success or adoption numbers, Docker-in-Docker issues blocked planned features, and MCP integration was still a prototype. — [Duolingo](https://blog.duolingo.com/agentic-workflows/)

#### Notion: Boxy or Software Factory [S]

- **Implementation:** Agents run in isolated VMs provisioned with Aider and Claude Code. An engineer @-mentions the agent in a Notion task, and the agent opens a PR with a preview URL and screenshots. — [ZenML summary of Ryan Nestrom talk, 2026](https://www.zenml.io/llmops-database/ai-powered-engineering-management-and-autonomous-development-workflows)
- **Agent choice:** Nestrom preferred Aider because Claude Code lost context when its window filled. This is his experience and is not a benchmark, and it may predate later versions. — [ZenML summary](https://www.zenml.io/llmops-database/ai-powered-engineering-management-and-autonomous-development-workflows)
- **Metrics:** The source gives only a single example of about 11 minutes to a PR and no volume or failure data. — [ZenML summary](https://www.zenml.io/llmops-database/ai-powered-engineering-management-and-autonomous-development-workflows)

#### Cloudflare: internal AI stack on its own platform [P]

- **Built versus bought:** Cloudflare built the proxy Worker, MCP servers and portal, AI Code Reviewer and AGENTS.md generator. It uses OpenCode as the primary client along with Windsurf and frontier models. — [Cloudflare, 2026-04-20](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- **Status:** Background agents were planned rather than deployed at publication, so this is mainly an interactive and review platform. — [Cloudflare](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- **Context:** A pipeline generated AGENTS.md proposals for about 3,900 repositories from Backstage data and sent merge requests to owning teams. The MCP portal exposes 182+ tools through two Code Mode tools. — [Cloudflare](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- **Metrics:** 93% of R&D used AI coding tools in the last 30 days, and the four-week average of merge requests rose from about 5,600 to over 8,700 per week. The post does not attribute this rise to agents through any controlled method. — [Cloudflare](https://blog.cloudflare.com/internal-ai-engineering-stack/)

#### GitHub: Copilot coding agent on github.com's core repository [P through a mirror]

- **Model:** Engineers assign Copilot an issue, it opens a first-pass PR, and engineers review it like any other PR and merge, iterate or close it. — [GitHub, 2025-11-12](https://github.blog/ai-and-ml/github-copilot/how-copilot-helps-build-the-github-platform/), read through [mirror](https://enggist.vercel.app/post/0f125076-99db-450f-87cc-7d1c6b102148)
- **Candid limit:** GitHub says that Copilot's merged PR rate is lower than that of human contributors, and it gives no total count. — [GitHub](https://github.blog/ai-and-ml/github-copilot/how-copilot-helps-build-the-github-platform/)
- **Work types:** Work includes UI fixes, flag removal, refactors, flaky tests, API endpoints, schema migrations and codebase audits reported through PRs. — [GitHub](https://github.blog/ai-and-ml/github-copilot/how-copilot-helps-build-the-github-platform/)

#### Intercom: Claude Code plus plugins [S, thread]

- **Built versus bought:** Intercom buys Claude Code and has built 13 plugins and 100+ skills, with hooks such as one that intercepts raw `gh pr create` and requires the PR skill. — [Brian Scanlan thread, Mar 17, year not shown](https://threadreaderapp.com/thread/2033978300003987527.html)
- **Context and execution:** Intercom exposes a read-only Rails production console through MCP with read-replica use, blocked tables, Okta auth and an audit trail. Agents appear to run mostly on laptops, because remote agents are described as planned. — [Scanlan thread](https://threadreaderapp.com/thread/2033978300003987527.html)
- **Feedback:** A SessionEnd hook classifies transcript gaps with Claude Haiku, and those gaps become issues and new skills. — [Scanlan thread](https://threadreaderapp.com/thread/2033978300003987527.html)
- **Metrics:** Merged PRs per R&D head reportedly doubled in nine months. The page I read gives no baseline or quality figures. — [How I AI, 2026-04-20](https://www.lennysnewsletter.com/p/how-intercom-2xd-their-engineering)
- **Caveats:** Secondary summaries say that CI costs rose, the bottleneck moved to review, and Stanford researchers measured quality. I could not verify the Stanford work. — [StartupHub summary, Sn](https://www.startuphub.ai/news/intercom-s-ai-leap-doubling-engineering-throughput)

#### Atlassian: Rovo Dev [P, seller of the product]

- **Implementation:** Rovo Dev reviews each PR commit, checks PRs against standards held in Confluence, and checks Jira acceptance criteria. — [Atlassian, 2026-01-28](https://www.atlassian.com/blog/rovo/how-we-cut-pr-cycle-time-with-ai-code-reviews)
- **Metrics:** PR cycle time fell 45% since early 2025 and the wait for a first review comment fell from 18 hours to zero. Atlassian gives no method, no acceptance rate and no false-positive rate. — [Atlassian](https://www.atlassian.com/blog/rovo/how-we-cut-pr-cycle-time-with-ai-code-reviews)

#### Airbnb: LLM migration pipeline [P]

- **Implementation:** About 3,500 Enzyme test files moved to React Testing Library through per-file state-machine stages, in which the LLM ran only when a check failed. Prompts reached 40,000–100,000 tokens and included up to 50 related files. — [Airbnb, about April 2025, date inferred from image paths](https://airbnb.tech/?p=366)
- **Metrics:** 75% of files migrated in 4 hours, 97% after 4 days of tuning, and the total was 6 weeks against an estimated 1.5 years. — [Airbnb](https://airbnb.tech/?p=366)
- **Lesson:** Retries with error feedback and choosing the right related files mattered more than prompt wording. — [Airbnb](https://airbnb.tech/?p=366)
- **Limit of the evidence:** This is a single bounded migration and not a background-agent platform, and I found no 2026 update.

#### Salesforce: hiring statements, not a platform write-up [S, Sn]

- **Claim:** In December 2024, Marc Benioff said that Salesforce would add no software engineers in 2025 because productivity rose more than 30% with Agentforce and other AI. He repeated a 30% figure on the February 2025 earnings call. — [SalesforceBen](https://salesforceben.com/salesforce-will-hire-no-more-software-engineers-in-2025-says-marc-benioff); [The Register, 2025-02-27](https://www.theregister.com/2025/02/27/salesforce_misses_revenue_guidance/)
- **Later framing:** In April 2026 reporting he said, "Our engineering organisation is probably more than 30% productive, but I wouldn't call it 100% more productive," and, "The models still cannot operate autonomously." — [ITPro, 2026-04-08](https://www.itpro.com/software/development/big-tech-is-still-hiring-software-engineers-despite-claims-ai-will-replace-them-and-marc-benioff-says-thats-the-canary-in-the-coal-mine-for-whether-the-technology-is-up-to-scratch)
- **Tools and spend:** Reports say that Salesforce plans about $300M of Anthropic token spend in 2026, mostly for coding. — [Technology Magazine, Sn](https://technologymagazine.com/news/salesforce-plans-to-spend-us-300m-on-anthropic-ai-tokens)
- **Scepticism:** An informal post argued that open engineering job listings conflicted with the freeze, and I did not verify the counts. — [Substack, Sn](https://ellensation.substack.com/p/no-company-for-coders-salesforce)

#### Datadog and Pinterest: adjacent evidence only

- **Datadog:**
  - Datadog's harness-first post covers redis-rust and Helix, two new systems evaluated in staging, so it does not describe work in the main production codebase. It reports that specifying invariants costs roughly 2–3x the effort of writing the code, and that incomplete invariants can create false confidence. — [Datadog, 2026-03-09](https://www.datadoghq.com/blog/ai/harness-first-agents/)
  - Bits AI Dev Agent is a product that delivers draft PRs labeled "Attempt to Fix." — [Datadog, Sn](https://datadoghq.com/blog/bits-ai-dev-agent)
- **Pinterest:**
  - Summaries report 66,000 MCP invocations per month, 844 active users and an estimated 7,000 hours saved per month. Tool owners estimate minutes saved per invocation, so this is not a controlled measure, and the sources disagree on the reference date. — [Botmonster, Sn](https://botmonster.com/ai/pinterest-mcp-playbook-monthly-invocations-engineering-hours/); [Pinterest summary](https://engineered.at/articles/building-an-mcp-ecosystem-at-pinterest)
  - Job postings describe an effort across 3,000+ engineers to move humans "on the loop," which indicates intent and not results. — [Job posting, Sn](https://remoteleaf.com/company/pinterest/principal-engineer-agentic-engineering-united-states/)

### Inferences

- The phrase "built" usually means the platform around the agent. Stripe, Ramp, Spotify, Duolingo and Notion all reuse a third-party or open-source loop, and they build the environment, tools, verification and triggers themselves.
- Publicly documented failure comes mostly from engineering-authored posts such as those from Spotify, Dropbox and Uber. Vendor-authored stories from Cursor and Modal contain almost none, so their absence of failures should not be read as evidence of smooth rollouts.

### Gaps

- Zapier produced no usable evidence, and its search results concerned only its role as an integration product.
- I found no primary evidence for Block's Builderbot, and one weak page describes it as autonomously merging PRs, so I excluded that claim from the findings.
- A claim that Block's blog describes a pattern of about 90% AI-generated code could not be traced to a specific page.
- I could not read the DoorDash primary, the Forbes Block profile, the Coinbase Mux post, the ACM AutoCover paper or the Pinterest primary because each fetch returned 403.
- The Minion architecture section of the March 2026 Pragmatic Engineer article is paywalled, so Minion's internals remain thinly documented.
- A Hacker News thread reports that Uber used its 2026 AI budget in four months, but no primary source was given. — [Ry Walker summary](https://rywalker.com/research/uber-coding-agents)

## Metrics, their definitions, and superseded claims

### Takeaway

The headline percentages cannot be compared across companies because they count different things, ranging from fully agent-produced and merged PRs to any PR that merely involves a local agent. Uber shows the size of the effect by reporting both about 11–15% for Minion and more than 70% for local or cloud agents in the same year.

### Cited Findings

| Company | Latest figure | What it counts | Date | Source quality |
|---|---|---|---|---|
| Stripe | 1,300+ per week | Merged PRs fully produced by minions and human-reviewed; no share of total | 2026-02-19 | [Primary](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2) |
| Ramp | 75% | Merged PRs by Inspect; repository scope is not visible in the free text | 2026-08-25 | [Paywalled secondary](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect) |
| Shopify | 1 in 8; 3,536 in 30 days | Merged PRs coauthored by River | 2026-05-28 | [Primary](https://shopify.engineering/under-the-river) |
| Uber | 11%, then about 15% | Merged or production PRs through Minion | 2026-05 and 2026-10 | [Session page](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/); [Port summary](https://software-factories.port.io/uber) |
| Uber | More than 70% | PRs "attributed to" or that "involve" local or cloud agents, with no definition | 2026-08-27 | [Primary](https://www.uber.com/us/en/blog/efficient-software-factory/) |
| Coinbase | 75% | PRs created by agents across cloud and local | 2026-06-23 | [Vendor](https://cursor.com/blog/coinbase) |
| Spotify | 1,500+ total | Merged agent PRs, cumulative | 2025-11-06 | [Primary](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1) |
| Faire | 2x | Weekly PR throughput, undefined | 2026-05-26 | [Vendor](https://cursor.com/blog/faire) |
| Intercom | 2x | Merged PRs per R&D head over nine months | 2026-04-20 | [Podcast page](https://www.lennysnewsletter.com/p/how-intercom-2xd-their-engineering) |
| Salesforce | About 30% | Productivity, undefined | 2024-12 to 2026-04 | [ITPro](https://www.itpro.com/software/development/big-tech-is-still-hiring-software-engineers-despite-claims-ai-will-replace-them-and-marc-benioff-says-thats-the-canary-in-the-coal-mine-for-whether-the-technology-is-up-to-scratch) |

**Superseded or conflicting claims**

- **Ramp:**
  - Ramp's own post says that about 30% of PRs merged to frontend and backend repos are written by Inspect, and an aggregator dates the post to about January 12, 2026. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [Pulse](https://www.pulse.bot/saas/news/why-we-built-our-own-background-agent-67ea098f-5e48-4450-8091-17090f0d7175/)
  - Modal's February 2026 story says "over half" in one place and "roughly half … started by Inspect" in another. — [Modal](https://modal.com/blog/how-ramp-built-a-full-context-background-coding-agent-on-modal)
  - Pragmatic Engineer reports 60% in January 2026 and 75% by May. This January figure conflicts with the 30% figure if the aggregator's date is right. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect)
- **Uber:** The 11% figure was stated as PRs opened by agents in March 2026 and as merged PRs in May 2026. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development); [Session page](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/)
- **Uber, unverified:** The October figure of about 15% comes only from Port's summary, and the Pragmatic Engineer URL it cites returned 404 when I tried it. — [Port summary](https://software-factories.port.io/uber)
- **Uber, AI-generated code:** The 65–72% figure applies to IDE tools, and the same source treats CLI tools as 100%, so this measure rises with tool mix by definition. — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development)
- **Stripe:** The figures moved from 1,000+ to 1,300+ merged PRs and from 400+ to nearly 500 tools within ten days of publication, and I found no later official update. — [Part 1](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [Part 2](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- **Spotify:** "Around half of PRs automated" since mid-2024 refers to Fleet Management automation overall, so it should not be read as agent output. — [Spotify Part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)
- **Shopify:** The CEO post says "authored by River" in the main monorepo, while the engineering post says "coauthored" across Shopify. The CEO post also reports 1,870 PRs opened in a week. — [transcription](https://hq-raydata-co.pages.dev/vault/06-reference/2026-05-09-tobi-lutke-river-public-channel-agent/); [Shopify](https://shopify.engineering/under-the-river)
- **Block:** Business Insider's 2025 report of about 1,000 internal engineers is older than Forbes's November 2025 figure of about two-thirds of employees using goose weekly, and the two count different populations. — [Business Insider NL, Sn](https://www.businessinsider.nl/a-lead-block-engineer-said-the-fintechs-new-ai-agent-writes-better-code-than-him-and-the-fintech-is-open-sourcing-it-to-competitors/); [Forbes, Sn](https://www.forbes.com/sites/richardnieva/2025/11/18/block-cto-dhanji-prasanna-cio-next/)

**Independent evidence on the metric itself**

- A 2026 MSR paper studied 11,048 closed agentic PRs and manually inspected 717. It found that only 35.7% of rejected PRs reflected clear agent failure, and that 15.4% of merged PRs required explicit reviewer involvement. This covers public repositories rather than these companies, but it shows that merge rate is an imperfect measure of autonomy. — [arXiv 2605.22534, Sn](https://arxiv.org/html/2605.22534)
- A January 2026 study of 33,000 agent-authored PRs found that unmerged PRs tended to be larger, touch more files and fail CI more often. — [arXiv 2601.15195 listing, Sn](https://arxiv.org/abs/2601.15195)
- Spotify says that it is unclear whether a merged PR actually solved the original problem, which is a rare first-party statement of the same limit. — [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)

### Inferences

- A rough calculation from Shopify's figures implies about 28,000 merged PRs per 30 days if the 3,536 and one-in-eight figures share a window, but the post does not state the window for the ratio.
- The Shopify figures of 1,870 opened per week and 3,536 merged per 30 days look low against a 77% merge rate, which would imply roughly 6,000 merged. Different dates, definitions or scopes may explain the difference.
- High percentages in the table correlate with broad definitions or with companies whose platform is the default path, such as Ramp. Stripe's narrow definition and absolute count should not be read as lower adoption.
- The numbers measure activity and not outcomes. No company in this set publishes a defect-escape rate, an incident rate attributed to agents, or code durability for agent PRs.

### Gaps

- I found no independent verification of any company's percentage.
- I found no public measurement that compares reviewer load or defect rates between agent and human PRs at these companies. Intercom's Stanford collaboration is the nearest claim, and it remains unverified.
- A vendor abstract from Greptile reports that detectable agent PRs rose from under 1% to 27.6% between February 2025 and April 2026, but it is a conference abstract and its population is unclear. — [Session page, Sn](https://dash.datadoghq.com/sessions/presented-by-greptile-lessons-learned-about-coding-agents-from-millions-of-ai-generated-pr-s)

## Common architecture and points of disagreement

### Takeaway

A common shape has emerged: a disposable pre-warmed sandbox, a replaceable agent loop, a governed MCP tool layer, scoped context, deterministic steps around the agent, several invocation surfaces, and ordinary human PR review. Companies still disagree on how much context and tooling to give the agent, who controls CI, whether to build or buy, how to attribute identity, and whether mandates work.

### Cited Findings

**Common elements**

- **Disposable isolated environments with fast starts:**
  - Stripe uses pre-warmed EC2 devboxes with a 10-second target. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
  - Ramp uses Modal snapshots rebuilt every 30 minutes and reports under five seconds. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/why-ramp-built-inspect)
  - DoorDash uses Firecracker with a p95 target under five seconds. — [ZenML](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks)
  - Shopify and Dropbox also use disposable or isolated per-session environments. — [Shopify](https://shopify.engineering/under-the-river); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **Replaceable agent loop:** Spotify's CLI, Duolingo's enum, Dropbox's single interface, Shopify's disposable harness and DoorDash's supported harnesses all avoid coupling to one agent. — [Spotify](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1); [Duolingo](https://blog.duolingo.com/agentic-workflows/); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents); [Shopify](https://shopify.engineering/under-the-river); [ZenML](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks)
- **Deterministic steps around the agent:** Stripe's blueprints, DoorDash's playbooks and Dropbox's externally controlled publishing and CI all place certain operations outside the model. Spotify's infrastructure does the same for pushes. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2); [ZenML](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents); [Spotify Part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- **Governed tool gateways:** Stripe's Toolshed, Uber's MCP Gateway, Cloudflare's MCP Portal, DoorDash's Agent Gateway and Pinterest's registry all centralize access. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2); [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development); [Cloudflare](https://blog.cloudflare.com/internal-ai-engineering-stack/); [ZenML](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks); [Pinterest summary](https://engineered.at/articles/building-an-mcp-ecosystem-at-pinterest)
- **Tool-schema overhead is a shared problem:** Uber and Cloudflare both report large schema costs and adopted code-mode approaches, and Stripe limits tools to a curated subset. — [Uber](https://www.uber.com/us/en/blog/efficient-software-factory/); [Cloudflare](https://blog.cloudflare.com/internal-ai-engineering-stack/); [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2)
- **Short, scoped context files:** Stripe scopes rules by directory, Dropbox uses localized AGENTS.md files, and Cloudflare keeps generated files short and warns that a stale file can be worse than none. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents); [Cloudflare](https://blog.cloudflare.com/internal-ai-engineering-stack/)
- **Slack as the leading trigger:** Stripe, Ramp, Shopify, Spotify, DoorDash, Faire, Coinbase and reportedly Uber all offer it. Notion's Notion-task trigger and GitHub's issue assignment are exceptions that use each company's own product. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [Shopify](https://shopify.engineering/under-the-river); [Spotify](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1); [GitHub](https://github.blog/ai-and-ml/github-copilot/how-copilot-helps-build-the-github-platform/)
- **Humans review and agents do not merge:** Stripe, Ramp, LinkedIn and GitHub state this directly. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents); [GitHub](https://github.blog/ai-and-ml/github-copilot/how-copilot-helps-build-the-github-platform/)
- **Earlier infrastructure is the precondition:** Stripe, Shopify and Uber all attribute agent results to prior developer-environment, monorepo or CI investment. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2); [Shopify](https://shopify.engineering/under-the-river); [Summit session page](https://background-agents.com/summit/sessions/nikhil-ramakrishnan/)

**Points of disagreement**

- **Rich tools versus a narrow agent:** Spotify withholds code search and documentation tools to gain predictability, while Stripe, Ramp, LinkedIn and Uber give agents search, telemetry or a context graph. Spotify's Part 4 roadmap moves toward Honk gathering its own context, which suggests that the narrow position depends on the type of task. — [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2); [Spotify Part 4](https://engineering.atspotify.com/2026/4/background-coding-agents-dataset-migrations-honk-part-4); [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [Uber](https://www.uber.com/us/en/blog/efficient-software-factory/)
- **Build versus buy:** DoorDash, Dropbox and Ramp cite security or infrastructure fit as reasons to build, while Faire moved from building to buying because of operating cost. Intercom extends a purchased agent with plugins, and LinkedIn splits by buying foreground and building background. — [ZenML](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents); [Cursor](https://cursor.com/blog/faire); [Scanlan thread](https://threadreaderapp.com/thread/2033978300003987527.html); [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents)
- **Who controls CI:** Stripe caps the agent at two CI rounds, and Dropbox removed CI control from the agent after long waits. Faire's automations instead trigger an agent on CI failure to push fixes, and Spotify requires verifiers to pass before a PR exists. — [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents-part-2); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents); [Cursor](https://cursor.com/blog/faire); [Spotify Part 3](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
- **LLMs for migrations:** Airbnb, Faire and Spotify report LLM-driven migrations that saved time, while Uber used OpenRewrite for its JUnit migration after a generative attempt failed, and Dropbox found that runbooks with owners were often better for repeatable work. — [Airbnb](https://airbnb.tech/?p=366); [Cursor](https://cursor.com/blog/faire); [Spotify Part 1](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1); [Uber](https://www.uber.com/us/en/blog/junit-migration/); [Dropbox](https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents)
- **PR identity:** Ramp opens PRs with the user's token so that the user cannot self-approve. LinkedIn gives each agent its own identity, Duolingo uses a shared bot account, and Spotify standardizes the committer. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents); [Duolingo](https://blog.duolingo.com/agentic-workflows/); [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2)
- **Mandates:** Ramp did not force use and Uber's speakers favour peer sharing, while Coinbase's speedruns require every developer to ship a PR and Shopify reportedly has an AI-first staffing rule. — [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-uber-uses-ai-for-development); [Cursor](https://cursor.com/blog/coinbase); [India TV, Sn](https://www.indiatvnews.com/technology/news/shopify-ceo-says-ai-comes-first-teams-must-prove-ai-can-t-handle-a-task-before-hiring-new-people-is-this-the-future-of-work-2025-04-08-984515)
- **Public versus private sessions:** Shopify refuses direct messages, and DoorDash and Ramp report that public use spreads learning. Intercom's published model instead relies on shared skills and telemetry that deliberately excludes prompts. — [Shopify](https://shopify.engineering/under-the-river); [ZenML](https://www.zenml.io/llmops-database/cloud-based-agent-platform-for-automated-engineering-tasks); [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [Scanlan thread](https://threadreaderapp.com/thread/2033978300003987527.html)
- **Reading diffs:** Datadog argues for reviewers reading harness output rather than diffs on systems with explicit invariants, and it states an upfront cost of 2–3x. Stripe, LinkedIn and GitHub keep normal PR review on production repositories. — [Datadog](https://www.datadoghq.com/blog/ai/harness-first-agents/); [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [InfoQ](https://www.infoq.com/podcasts/platform-engineering-scaling-agents); [GitHub](https://github.blog/ai-and-ml/github-copilot/how-copilot-helps-build-the-github-platform/)
- **Which agent works:** Spotify moved away from Goose and Aider toward Claude Code, Stripe kept a goose fork, Notion's speaker preferred Aider for long tasks, and Ramp and Cloudflare use OpenCode. These accounts come from different dates and workloads, so they do not amount to a ranking. — [Spotify Part 2](https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2); [Stripe](https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents); [ZenML](https://www.zenml.io/llmops-database/ai-powered-engineering-management-and-autonomous-development-workflows); [Ramp](https://builders.ramp.com/post/why-we-built-our-background-agent); [Cloudflare](https://blog.cloudflare.com/internal-ai-engineering-stack/)

### Inferences

- The platform layer is more stable than the agent layer, because companies have swapped agents while keeping sandboxes, gateways and verification. This explains why so many designs make the harness replaceable.
- Companies with narrow, repeated tasks, such as Spotify's migrations, benefit from constraint and static prompts. Companies serving open-ended requests from Slack, such as Stripe and Ramp, need richer context and tools. Much of the "narrow versus rich" disagreement may therefore reflect workload.
- The bottleneck appears to be moving from writing code to CI capacity, review attention and token cost, based on statements from Uber and on secondary reports about Intercom. Shopify's CI breakage came from monorepo consolidation, which is a related but distinct cause.
- Faire's reversal suggests that self-hosting has a real operating cost, but the only account comes from the vendor that won the business. Ramp's team of about 5.5 people is a partial counterexample, although Ramp rents its sandbox layer from Modal.

### Gaps

- No public source compares the total cost of building and buying on the same workload.
- No company in this set publishes a controlled experiment that attributes throughput change to a background agent.
- No source describes an agent-caused production incident in detail, so I cannot assess how well sandboxing and review have performed under failure. This absence likely reflects publication incentives.
