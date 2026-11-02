# AI code review in large organisations, and how AI-generated code is reviewed

Research date: 2026-11-02. Unless a finding says "snippet only", I read the cited page through a fetch tool that returned an extraction rather than the raw text, so exact wording should be checked against the source before it is quoted. "Snippet only" means that the figure came from a search-result summary and that the page itself was not opened. COI marks a conflict of interest, meaning that the publisher sells or operates the thing being measured.

## Implementations with numbers

### Takeaway
Almost every large deployment reports a "comments addressed" proxy of roughly 20-80% and a self-reported benefit, and nearly all of it is published by the operator or vendor. The only randomised results found (Google and Meta) show no review-time gain or a small slowdown, which is less favourable than the observational 10-31% cycle-time improvements from Microsoft and Atlassian.

### Cited Findings

**In-house systems at large organisations**

- **Uber uReview (published 2025-08-12; COI: operator).**
  - It analyses over 90% of roughly 65,000 diffs across six monorepos, and it reviews each commit in CI with a median of 4 minutes — [Uber](https://www.uber.com/blog/ureview/).
  - The same post says "weekly" in one place and "per month" in another for the 65,000 figure, and it separately says that the tool processes over 10,000 commits weekly, so the volume is internally inconsistent — [Uber](https://www.uber.com/blog/ureview/).
  - Engineers who rate comments mark 75% as useful, over 65% of posted comments are addressed, and human comments are addressed at 51% in Uber's internal audits — [Uber](https://www.uber.com/blog/ureview/).
  - Uber estimates about 1,500 hours saved weekly by assuming that a second reviewer would need 10 minutes per commit, which is an assumption and not a measurement — [Uber](https://www.uber.com/blog/ureview/).
  - Uber rejected third-party tools because of false positives, low-value true positives, no internal-system access, and Phabricator incompatibility, and it says that its AI cost is about an order of magnitude lower — [Uber](https://www.uber.com/blog/ureview/).
- **ByteDance BitsAI-CR (arXiv 2025-01, FSE 2025 industry; COI: operator).**
  - Online precision was about 25% in the first three weeks, and it reached a peak of 75% at the ReviewFilter stage over 18 weeks — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
  - The Go "Outdated Rate" (flagged code later changed) peaked at 26.7%, against a human rate of 35-46% at ByteDance — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
  - The system had over 12,000 weekly active users, second-week retention of 61.64%, and about 48% retention through eight weeks — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
  - In a survey of 137 users, 74.5% found value, 12.4% called comments correct but unnecessary, and 10.9% called them incorrect — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
  - The paper has internal inconsistencies in its offline precision figures (54.50% to 67.12% in text, and 57.03% to 65.59% in its table) — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
- **Atlassian RovoDev (arXiv 2026-01, ICSE-SEIP 2026; COI: operator and vendor).**
  - The 12-month deployment covered over 1,900 repositories and over 54,000 comments, at an average of 2.1 comments per PR, using Claude 3.5 Sonnet without fine-tuning on customer data — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2).
  - The code resolution rate was 38.70%, against 44.45% for human comments — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2).
  - Median PR cycle time was 14.35 h with the tool and 20.73 h without it (30.8% lower, across 43,633 and 42,981 PRs), and human comments per PR fell 35.6% — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2).
  - In an alignment benchmark, only about 7% of PRs had at least one human-aligned RovoDev comment and about 4% of comments were human-aligned, so the tool largely does not reproduce what humans flag — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2).
  - The design is not randomised, and Atlassian's later marketing figure of a 45% cycle-time reduction is a separate unreviewed claim — [Atlassian](https://www.atlassian.com/blog/rovo/how-we-cut-pr-cycle-time-with-ai-code-reviews) (snippet only).
- **Google (COI: operator).**
  - The 2023 comment-resolution model addressed 52% of comments offline at a 50% precision target, and authors applied 40-50% of previewed edits; the "hundreds of thousands of hours annually" figure was an estimate made before a planned A/B test — [Google Research, 2023-05-23](https://research.google/blog/resolving-code-review-comments-with-ml/). This predates the requested window.
  - AutoCommenter (best-practice comments, AIware 2024) reached all Google developers in October 2023 after an A/B experiment on about half of them — [arXiv 2405.13565](https://arxiv.org/html/2405.13565).
  - AutoCommenter's useful ratio plateaued around 54% and rose to 66% after suppression, while a rater study went from 60% to 74%; resolution was estimated at about 40% from a manual sample of only 40 pairs — [arXiv 2405.13565](https://arxiv.org/html/2405.13565).
  - The A/B experiment found no statistically significant change in review duration, active review time, or comment-response iterations — [arXiv 2405.13565](https://arxiv.org/html/2405.13565).
- **Meta MetaMateCR (arXiv 2025-07; COI: operator).**
  - The system generates fixes for human review comments, and its fine-tuned Llama model reached an ActionableToApplied rate of 19.7% in production, 9.2 points above GPT-4o — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499).
  - A randomised safety trial found that reviewers took over 5% longer when shown AI patches; showing patches only to authors removed the regression — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499).
- **Meta review-time programme, before LLMs (2022-11-16; COI: operator).** Next Reviewable Diff raised review actions per day by 17%, a stale-diff nudge bot cut average Time In Review by 7%, and diffs waiting over three days fell 12% — [Meta Engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/). This predates the requested window but provides a non-AI comparison.
- **Microsoft (2025-07-14; COI: operator and vendor).** The internal reviewer covers over 90% of PRs and over 600,000 PRs per month, and 5,000 onboarded repositories saw a 10-20% improvement in median PR completion time according to "early experiments", with no published precision or acceptance rate — [Microsoft Engineering](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/).
- **Mozilla and Ubisoft RevMate (arXiv 2024-11; academic-industry study).**
  - This 5-6 week live study covered 59 reviewers and 587 reviews, and acceptance was 8.1% at Mozilla and 7.2% at Ubisoft, while appreciation including useful tips was 23.0% and 28.3% — [arXiv 2411.07091](https://arxiv.org/html/2411.07091v1).
  - In the survey, 24 of 37 reviewers said the tool slowed them, and 11 said the extra time was worthwhile — [arXiv 2411.07091](https://arxiv.org/html/2411.07091v1).
- **Ericsson (arXiv 2025-07; COI: operator).** Nine developers used a lightweight LLM and static-analysis tool for 15 days, 4 of 9 agreed that it saved time, and 3 of 9 rated it not very effective; there are no statistics and the models are small — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v2).
- **Kuaishou-affiliated defect-focused review (arXiv 2025-05).**
  - Key bug inclusion reached 42.22% against 0-2.22% for earlier baselines, but the false alarm rate across all merge requests stayed roughly 75-95% — [arXiv 2505.17928](https://arxiv.org/html/2505.17928v2).
  - This is the paper that surfaced when searching for Tencent, and it lists no Tencent affiliation — [arXiv 2505.17928](https://arxiv.org/html/2505.17928v2).
- **Cloudflare (2026-04-20, data from 2026-03-10 to 2026-04-09; COI: operator).** The system covers 5,169 repositories and 48,095 merge requests with 131,246 review runs, at a median of 3m 39s and an average cost of $1.19, using up to seven specialist reviewers; it reports no precision or acceptance figure — [Cloudflare](https://blog.cloudflare.com/ai-code-review/).
- **An unnamed company using Qodo PR-Agent (arXiv 2024-12).** Across 4,335 PRs, of which 1,568 received automated reviews, 73.8% of comments were resolved, but average closure time rose from 5h52m to 8h20m, with variation by project — [arXiv 2412.18531](https://arxiv.org/abs/2412.18531).

**Vendor products (all COI)**

- **Anthropic Code Review (2026-03-09).** Substantive review comments rose from 16% to 54% of PRs, under 1% of findings were marked incorrect, PRs over 1,000 lines got findings 84% of the time (7.5 issues on average), PRs under 50 lines got them 31% of the time (0.5 issues), reviews cost $15-25, and they take about 20 minutes — [Anthropic](https://claude.com/blog/code-review). "Marked incorrect" relies on engineers flagging a finding and is not a false-positive audit.
- **GitHub Copilot code review (2026-03-05).** It has completed 60 million reviews and accounts for more than one in five reviews on GitHub, with 71% of reviews surfacing actionable feedback, 29% staying silent, and about 5.1 comments per review; these are product metrics and not audited precision — [GitHub](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/).
- **Cursor Bugbot.**
  - Resolution rose from 52% in July 2025 to over 70% by January 2026 after 40 major experiments, and bugs flagged per run rose from 0.4 to 0.7 — [Cursor, 2026-01-15](https://cursor.com/blog/building-bugbot).
  - A later post reports 78.13% on public repositories, judged by an LLM — [Cursor, 2026-04-08](https://cursor.com/blog/bugbot-learning). A May 2026 post reports about 80% — [Cursor](https://cursor.com/blog/may-2026-bugbot-changes) (snippet only).
  - Cursor's table reports 78.13% for Bugbot, 63.49% for Greptile, 48.96% for CodeRabbit, 46.69% for Copilot, 45.07% for Codex, and 30.93% for Gemini Code Assist. Cursor designed this comparison, chose the judge, and ranks first in it — [Cursor](https://cursor.com/blog/bugbot-learning).
- **Greptile, CodeRabbit, and the Martian benchmark.**
  - Greptile's report of Martian's Code Review Bench on 2026-07-30 lists Greptile at F1 60.8% and precision 76.2%, the ChatGPT Codex Connector at F1 59.4%, Cubic at 58.7%, Devin at 58.6%, and CodeRabbit at 57.5% — [Greptile](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark). The publisher is the top-ranked vendor, and I did not check Martian's own leaderboard or independently verify Martian's independence.
  - CodeRabbit separately claimed a Martian first place in March 2026 on a different snapshot — [CodeRabbit](https://coderabbit.ai/blog/coderabbit-tops-martian-code-review-benchmark) (snippet only).
  - Tenki's own benchmark reports 68.9% recall and 29.9% precision for itself across 50 PRs — [Tenki](https://tenki.cloud/blog/benchmarking-ai-code-reviewers) (snippet only, COI).

**Comparison of human and AI "addressed" rates in the same organisation** (the metric definitions differ, so compare within a row only)

| Organisation | AI | Human | Source |
|---|---|---|---|
| Uber | 65% | 51% | [Uber](https://www.uber.com/blog/ureview/) |
| Atlassian | 38.7% | 44.45% | [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2) |
| ByteDance (Go, peak) | 26.7% | 35-46% | [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1) |

### Inferences
- Vendor "resolution" and "precision" numbers are not comparable with one another, because they all rely on later code change as a proxy, and an LLM judge or five-run re-detection sits between the comment and the score.
- Atlassian and ByteDance, the two sources with peer-reviewed methods, report AI addressed rates below human ones, whereas Uber's blog reports the opposite. The two peer-reviewed figures deserve more weight, although Uber's comparison may be correct for its filtered output.
- Rates of 7-8% in the RevMate study and 65-80% in current products differ partly by model generation and filtering, and partly by metric. This range should not be presented as a pure improvement trend.
- The claim that AI review saves time is unsettled. Randomised evidence at Google and Meta shows no gain or a slowdown, while observational data ranges from a 42% increase in closure time to a 31% reduction.
- Atlassian's 35.6% decline in human comments can be read either as AI catching issues or as humans reviewing less, and the paper's data does not separate these two readings.

### Gaps
- I found no Tencent code-review deployment with numbers, and the paper that appeared in search is affiliated with Kuaishou.
- I found no Microsoft precision or acceptance figures, and no independently audited false-positive rate for any commercial product.
- I could not verify Graphite's AI review figures. An "under 3% unhelpful comments" claim appeared only on aggregator pages, such as [aicodereview.cc](https://aicodereview.cc/tool/graphite), and I did not find Graphite's own source.
- I did not find a more recent Google paper with resolution rates, or a post-A/B result for the 2023 suggested-edit system.

## Precision, noise, useful categories, and false-positive reduction

### Takeaway
Bug and correctness comments are the stated goal, and style and nit comments are the most consistently suppressed, but the Mozilla and Ubisoft data shows that acceptance does not always follow that preference. The mechanisms with reported numbers are post-generation filtering, a verifier stage, repeated passes with voting, and removal of low-value rules.

### Cited Findings

**Useful and ignored categories**

- Uber reports that correctness bugs, missing error handling, and best-practice violations with examples or internal links were well received, whereas readability nits, minor logging tweaks, low-impact performance suggestions, and style were suppressed — [Uber](https://www.uber.com/blog/ureview/).
- Atlassian's most-resolved comment types relate to readability, bugs, and maintainability, which conflicts with Uber's view of readability comments — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2).
- Refactoring comments were accepted far more often than functional ones in RevMate (18.2% against 4.8% at Mozilla, and 18.6% against 5.2% at Ubisoft) — [arXiv 2411.07091](https://arxiv.org/html/2411.07091v1).
- Google suppressed subjective rules, systematic false positives, multi-topic guides, and low-value nitpicks, and it notes that 66% of its top 50 best-practice URLs are beyond traditional static analysis — [arXiv 2405.13565](https://arxiv.org/html/2405.13565).
- Uber concludes that linters remain best for simple syntactic rules and that LLMs suit semantic rules, and that uReview catches code-evident bugs but cannot assess system design without further context — [Uber](https://www.uber.com/blog/ureview/).
- Atlassian's reported weakness is incorrect or non-actionable comments caused by missing context, such as wrong language or framework assumptions — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2).
- BitsAI-CR's per-category Outdated Rate ranged from 0% to 41.37%, and its review context is mostly function-level, with cross-file review left as future work — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).

**False-positive reduction, with evidence where available**

- **Verifier stage.** ReviewFilter raised BitsAI-CR's offline precision from 57.03% to 65.59% while recall fell from 45.50% to 39.77%, which shows the trade-off directly — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1). A taxonomy mattered more than the filter, because the base model without it reached 16.83%, and 30.92% with the filter — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
- **Reasoning order in the verifier.** A conclusion-first format reached 77.09% precision at 1.7 s, against 65.80% at 31 s for reasoning-first — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
- **Actionability classifier.** A ModernBERT model trained on over 50,000 comments added 15-20 points of human alignment at Atlassian, while an LLM factual-check judge had minimal impact, and review guidelines added about 5 points — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2).
- **Per-item thresholds and suppression.** Google moved from one 0.98 threshold to per-URL thresholds, removed comments on unmodified lines, and suppressed 22 URLs, which raised its useful ratio by 12 points — [arXiv 2405.13565](https://arxiv.org/html/2405.13565). Uber sets thresholds per assistant, language, and category — [Uber](https://www.uber.com/blog/ureview/).
- **Parallel passes and voting.** Bugbot's launch flow ran eight passes with randomised diff order and removed bugs seen in only one pass, and Cursor calls this one of its most effective early improvements — [Cursor](https://cursor.com/blog/building-bugbot).
- **Multi-reviewer agreement.** A meta-reviewer that keeps comments raised by multiple reviewers is used in the Kuaishou-affiliated system, whose false alarm rate nevertheless stayed high — [arXiv 2505.17928](https://arxiv.org/html/2505.17928v2).
- **Adversarial verification.** Anthropic's agents verify findings before posting, with no published precision change attributable to that step — [Anthropic](https://claude.com/blog/code-review).
- **Feedback learning.** Bugbot's learned rules turn reactions, replies, and human comments on missed issues into candidate rules, across over 110,000 repositories and 44,000 rules; Cursor credits both offline improvements and learning for its gain — [Cursor](https://cursor.com/blog/bugbot-learning).
- **Explicit feedback is sparse.** Only about 10% of Google review comments received explicit feedback — [arXiv 2405.13565](https://arxiv.org/html/2405.13565); Atlassian says that thumbs were rarely used — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2); ByteDance treats likes as supplementary and samples up to 10% of output daily for manual annotation — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
- **Rule pruning.** BitsAI-CR removed underperforming Go rules from week 14 and used a 14-day review of precision and Outdated Rate — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1).
- **Scope control.** Cloudflare uses "What NOT to Flag" prompt sections, risk tiers, generated-file filtering, and a coordinator that removes duplicates and nitpicks, and it reports no resulting precision change — [Cloudflare](https://blog.cloudflare.com/ai-code-review/).
- **Negative results.** Cursor says that many experiments regressed metrics across models, prompts, validators, category filters, and agentic designs — [Cursor](https://cursor.com/blog/building-bugbot).

### Inferences
- Precision gains are bought with recall. ByteDance and Google state that they prioritised precision, and neither those systems nor most vendors publish how many defects they miss, so a high precision figure does not show that a tool is protecting production.
- Explicit ratings are too sparse and self-selected to act as a primary metric, which explains why operators have moved to change-based proxies. Those proxies have their own flaw, because code can change for unrelated reasons, as ByteDance acknowledges.
- Atlassian's finding that a trained classifier outperformed an LLM judge suggests that organisations with comment history may gain more from learned filters than from adding another LLM stage. This rests on a single company's data.

### Gaps
- I found no study that measures production defects prevented by AI review through a controlled design.
- Category data is not comparable across studies, because each one uses its own taxonomy.
- Security-category acceptance rates are not separately published by Uber's AppSec assistant or by other tools that I reviewed.

## Evidence of review as the new bottleneck

### Takeaway
Output growth is well measured at Meta, Anthropic, and in Faros telemetry, and open-source data shows that agent PRs often receive little independent scrutiny. Evidence that review is the binding constraint is mostly correlational, and evidence of reviewer fatigue and rubber-stamping is largely self-reported.

### Cited Findings

**Volume and size**

- Meta reports that lines of code per human-landed diff rose 105.9% year over year and diffs per developer per month rose 51%, attributing over 80% of that growth to agentic AI — [arXiv 2605.30208](https://arxiv.org/html/2605.30208). This is the strongest large-organisation data found, although it is self-reported.
- Anthropic reports that code output per engineer grew 200% over a year (COI) — [Anthropic](https://claude.com/blog/code-review).
- Faros (2025-07-23; COI: engineering analytics vendor), using telemetry from over 10,000 developers across 1,255 teams, associates high AI adoption with 21% more tasks, 98% more merged PRs, 91% longer PR review time, 154% larger PRs, and 9% more bugs per developer, and it finds no significant company-level correlation — [Faros](https://www.faros.ai/blog/ai-productivity-paradox-report-2025).
- A Faros FAQ gives different figures of 51.3% for PR size and 54% for bugs, and I could not reconcile them with the report — [Faros FAQ](https://www.faros.ai/blog/bain-technology-report-2025-why-ai-gains-are-stalling) (snippet only).
- Greptile's report is cited as showing median PR size rising 33% from 57 to 76 lines between March and November 2025 — [CodeAnt, a competing vendor](https://codeant.ai/blogs/top-pull-request-automation-tools) (secondary, snippet only).
- DORA 2025 (nearly 5,000 respondents, published 2025-09) reports that AI adoption now has a positive relationship with throughput while instability continues to rise; 59% report better code quality, and the InfoQ article gives no code-review statistics — [InfoQ](https://www.infoq.com/news/2025/09/dora-state-of-ai-in-dev-2025). I read secondary coverage only, and DORA is Google-run survey research.

**Agent PR outcomes in open source**

- **AIDev-pop** (MSR 2026, 33,596 PRs in projects with over 100 stars): the overall merge rate was 71.48%, with Codex at 82.59%, Cursor at 65.22%, Claude Code at 59.04%, Devin at 53.76%, and Copilot at 43.04% — [arXiv 2601.15195](https://arxiv.org/html/2601.15195).
- **Task differences:** documentation merged at 84%, CI at 79%, and build at 74%, while performance merged at 55% and fix at 64% — [arXiv 2601.15195](https://arxiv.org/html/2601.15195).
- **Rejection reasons** (562 categorised PRs): 40.6% were abandoned or not reviewed, 25.3% were duplicates, 17.6% were CI or test failures, 4.3% were unwanted features, 3.4% were incorrect implementations, and 2.7% were incomplete implementations — [arXiv 2601.15195](https://arxiv.org/html/2601.15195).
- **Merge predictors:** not-merged PRs are larger, and each additional failed CI check lowers merge odds by about 15% — [arXiv 2601.15195](https://arxiv.org/html/2601.15195).
- **A second study** (MSR 2026, 9,799 human-reviewed PRs from repositories with at least 500 stars) reports a 63.1% merge rate and quite different agent rankings (Cursor 71.4%, Codex 71.0%, Claude Code 61.0%, Copilot 58.7%, Devin 53.6%) — [arXiv 2605.22534](https://arxiv.org/html/2605.22534).
- **Rejection reasons in that study** (353 rejections): 35.7% were agentic failures, 31.2% were workflow failures, and 33.1% had no observable rationale; 79.1% of merged PRs had no observable feedback loop or reviewer commits — [arXiv 2605.22534](https://arxiv.org/html/2605.22534).
- **A third study of fix-related agent PRs** (8,106 PRs) reports 65.0% merged and 26.1% closed without merging — [arXiv 2602.00164](https://arxiv.org/html/2602.00164) (snippet only).
- **Human baseline:** one topic page gives a human merge rate of 76.8%, alongside agent figures that conflict with those above — [Emergent Mind](https://emergentmind.com/topics/aidev-dataset) (secondary, snippet only). The AIDev paper says that agent PRs are accepted significantly less often than human contributions — [AIDev](https://www.alphaxiv.org/abs/2507.15003v1) (snippet only).
- **Missing review records:** 98.2% of Codex PRs had no recorded comments, and 90.6% of all PRs in the task-level dataset had zero recorded review comments — [arXiv 2602.02345](https://arxiv.org/html/2602.02345) (snippet only).

**Rubber-stamping, independent review, and comprehension**

- A CMU study (submitted 2026-07-08; 2,860 repositories) finds that the share of repositories merging all agent PRs without review fell from 34% in May 2025 to 13% in February 2026 — [arXiv 2607.07980](https://arxiv.org/html/2607.07980).
- At PR level, merged agent PRs with no human review fell from over 50% in mid-2025 to about 12%, near the stable human rate of about 14% — [arXiv 2607.07980](https://arxiv.org/html/2607.07980).
- Among projects that merge without review, agent no-review rates were 69% for tests, 41% for refactors, and 25% for bug fixes, which the authors read as informal triage by risk — [arXiv 2607.07980](https://arxiv.org/html/2607.07980).
- In the same study, 40.1% of agent PRs were examined only by the invoking developer against 21.5% of human PRs, but the authors say that this comparison can reverse under a different counting choice — [arXiv 2607.07980](https://arxiv.org/html/2607.07980).
- The same study's median time to merge is faster for agent PRs, rising from about 20 minutes to 2-3 hours, against a human median that rose from about 5 to 8 hours — [arXiv 2607.07980](https://arxiv.org/html/2607.07980).
- The study's theory, coded from 3,100 practitioner documents, proposes that review load and surface plausibility reduce review depth, and that low depth increases comprehension debt. The authors state that the theory is not empirically validated, and the corpus may include LLM-generated and vendor-advocacy content — [arXiv 2607.07980](https://arxiv.org/html/2607.07980).
- In Anthropic's randomised trial with 52 engineers (January 2026; COI: AI developer, though the result is unfavourable to its product category), the AI group scored 50% on a quiz and the hand-coding group 67%, without a significant speed gain; the authors note the small, short-horizon sample — [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills) (snippet only).
- Before LLMs became common, Meta used "Eyeball Time" as a guardrail against rubber-stamping when optimising review speed — [Meta Engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/).

### Inferences
- Rejection data suggests that open-source agent PRs often fail because of attention and coordination rather than code quality: abandonment and duplicates total about 66% in one taxonomy, while incorrect or incomplete code totals about 6%. The second study attributes more to agents (35.7%), so the taxonomy and sampling clearly matter.
- Agent merge rates vary too much by repository selection for agent rankings to be meaningful. Codex ranges from 82.59% to 71.0% between the two MSR studies, and workflow differences may explain more than capability.
- Open-source data transfers imperfectly to large organisations, since mandatory-review policies, code ownership, and CI gates differ. Meta's growth figures and Faros's telemetry are closer to the enterprise setting.
- Declining no-review rates contradict the simple claim that rubber-stamping is growing. However, these metrics measure the presence of a review and not its depth, so shallow approvals remain invisible in this data.

### Gaps
- I found no direct measurement of reviewer fatigue or review depth in a large company under high agent PR volume.
- "Comprehension debt" has only a proposed theory and a small related trial, and no longitudinal measurement.
- I found no LinearB primary data on wait time for AI PRs.
- Most AIDev studies have no enterprise equivalent, since internal PR data is not public.

## Policies and which have evidence of working

### Takeaway
Risk-tiered automation at Meta has the strongest evidence, though it is observational and selects low-risk diffs by design. Mandatory human approval remains the stated default for most products, and I found almost no measured evidence for agent-review-agent loops, stacked diffs, or PR size limits in the AI era.

### Cited Findings

- **Risk-tiered auto-review: Meta RADAR (arXiv v2 2026-06-12; COI: operator).**
  - RADAR reviewed 535,290 diffs and landed 331,720, with a peak of over 25,000 per day — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
  - Its revert rate was one third of the non-RADAR rate and its production-incident rate one fiftieth, while median diff review wall time fell 35%; a claimed "over 330%" reduction in time to close is not meaningful as written — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
  - The design combines the Diff Risk Score percentile (default P5 for human diffs, P50 for allowlisted bot runbooks, and P20 for other bots), an LLM review requiring confidence of at least 8/10 with safe categories only, and deterministic checks — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
  - Exclusions cover open-source code, SOX-scoped code, code-freeze diffs, and blocklisted content, and bot runbooks need a 60-day clean record and have daily caps — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
  - The study was not randomised, and the paper says that the calibration comparison is not causal. It also gives no RADAR share of total diffs — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
- **Risk scoring for gating: Meta Diff Risk Score (2025-08-06).** Lower-risk changes were allowed to land during freezes, with over 10,000 changes landed during one 2024 partner event and minimal reported production impact — [Meta Engineering](https://engineering.fb.com/2025/08/06/developer-tools/diff-risk-score-drs-ai-risk-aware-software-development-meta/) (snippet only).
- **Mandatory human approver.**
  - Anthropic's Code Review will not approve PRs: "that's still a human call" — [Anthropic](https://claude.com/blog/code-review).
  - Microsoft requires authors to choose whether to apply suggestions, and it attributes applied changes in commit history — [Microsoft Engineering](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/).
  - The evidence for this policy is mostly by default. I found no controlled comparison of defect outcomes with and without a human approver for comparable AI code, other than Meta's selected low-risk comparison.
  - Self-approval gives limited assurance: 40.1% of agent PRs were examined only by the invoking developer, subject to the counting caveat above — [arXiv 2607.07980](https://arxiv.org/html/2607.07980).
- **AI review with a merge effect: Cloudflare.** Cloudflare records "break glass" overrides on 288 merge requests (0.6%), and it uses an approval bias in which a lone warning still produces approval with comments — [Cloudflare](https://blog.cloudflare.com/ai-code-review/). The low override rate shows little friction, and it does not show that findings were correct.
- **Agent-authored and agent-reviewed code: Meta RACER with RADAR.** RACER landed about 3,000 diffs per week, 59% without human revisions, and approved bot diffs land after a delay during which a human can reject them — [arXiv 2605.30208](https://arxiv.org/html/2605.30208). Deterministic codemods get blanket auto-accept — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
- **Agent-review-agent repair loops: Cursor Autofix.** Cursor reports its Bugbot resolution rate at 76% in that post, which promotes automatic fixing of findings; I found no safety or defect result for the loop — [Cursor](https://cursor.com/blog/bugbot-autofix) (snippet only, COI).
- **Audience control in UX.** Showing AI patches only to authors removed a measured review slowdown at Meta. This is one of the few policy-like changes backed by a randomised trial — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499).
- **Accountability.**
  - RADAR authors can ship on RADAR approval, wait for a human, or return the diff to "Needs Review", but the paper does not detail who is accountable for auto-landed diffs — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
  - RADAR's eligibility also requires authors to be on an operational on-call rotation, which ties authorship to operational responsibility — [arXiv 2605.30208](https://arxiv.org/html/2605.30208).
- **Review guardrails.** Meta's "Eyeball Time" is a non-AI precedent for detecting shallow review when pushing for speed — [Meta Engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/).
- **Process nudges.** Non-AI nudges and queueing cut Time In Review by 7% and raised review actions by 17% — [Meta Engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/).
- **Stacked diffs.** Aggregator pages report Shopify merging 33% more PRs per developer and Asana cutting median PR size by 11% with Graphite, but I could not confirm these against primary material, and they would be vendor-sourced customer stories — [aicodereview.cc](https://aicodereview.cc/tool/graphite) (unverified, snippet only).
- **PR size.** Size is associated with non-merge for agent PRs — [arXiv 2601.15195](https://arxiv.org/html/2601.15195). AI findings per PR also scale with size at Anthropic — [Anthropic](https://claude.com/blog/code-review). Neither result tests a size limit.

### Inferences
- RADAR's revert and incident ratios cannot be read as "AI review beats human review", because the eligible diffs were selected for being low risk. They show that a conservative, gated, reversible auto-landing path did not produce visible harm at Meta's scale.
- A defensible order of evidence is: risk-tiered automation with deterministic checks (observational, large scale), then process nudges (measured, non-AI), then AI as a first reviewer alongside a human (mixed time effects), then stacked diffs and size limits (assumed, with no AI-era evidence that I could verify).
- Open-source teams appear to be applying informal risk tiers already, given the 69% no-review rate for agent test PRs, so formal policy would codify an existing practice rather than introduce a new one.
- Eligibility and exclusion lists may be as important as the model at Meta. The RADAR controls (regulated code, track records, volume caps) would need to be replicated by any organisation copying the approach, and smaller organisations may lack a comparable risk model.

### Gaps
- I found no measured evidence for large-PR limits under AI authorship, and no peer-reviewed study of stacked diffs with AI.
- I found no controlled evidence for agent-reviewer loops improving production outcomes.
- I found no published organisational accountability rule set beyond product stances and RADAR's controls.
- Whether RADAR results replicate outside Meta is unknown, as no other organisation has published similar data that I found.

## Security review of AI code and prompt injection into review bots

### Takeaway
AI code carries measurable security weaknesses in benchmarks and vendor telemetry, although the most-cited figures come from security vendors and have narrow definitions. Review bots are themselves an attack surface, because the injection path runs through attacker-controlled PR text, and vendor fixes reported so far did not change the underlying tool access.

### Cited Findings

**Weakness in generated code**

- Veracode (2025-07-30; COI: application security vendor) tested more than 100 LLMs on 80 curated tasks, and about 45% of cases introduced OWASP Top 10 weaknesses. Java exceeded 70%, Python, C#, and JavaScript fell between 38% and 45%, and failure rates were 86% for CWE-80 and 88% for CWE-117 — [Veracode](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/). The test uses curated completion tasks and does not measure production code.
- A "2.74x more vulnerabilities than human code" figure attributed to Veracode appears in secondary sources but not in its press release — [SoftwareSeni](https://softwareseni.com/ai-generated-code-security-risks-why-vulnerabilities-increase-2-74x-and-how-to-prevent-them) (snippet only, unconfirmed).
- Apiiro (September 2025; COI: application security vendor) data from Fortune 50 enterprises, as reported by The Register, says AI-assisted developers produced 3-4x more code and 10x more security issues, a broad definition including dependencies, secrets, and misconfigurations that are not necessarily exploitable — [The Register](https://theregister.com/2025/09/05/ai_code_assistants_security_problems).
- The same article also describes the 10x as a growth in monthly findings between December 2024 and June 2025, to over 10,000 per month, which is a different quantity from a developer comparison — [The Register](https://theregister.com/2025/09/05/ai_code_assistants_security_problems).
- The article also reports 76% fewer syntax errors, 60% fewer logic bugs, 322% more privilege escalation paths, 153% more architectural design flaws, and nearly double the exposure of cloud credentials, with little methodology given — [The Register](https://theregister.com/2025/09/05/ai_code_assistants_security_problems). Apiiro's own post returned HTTP 403 when fetched — [Apiiro](https://apiiro.com/blog/4x-velocity-10x-vulnerabilities).
- CodeRabbit (December 2025; COI: review vendor) compared 320 AI-co-authored and 150 human-only open-source PRs and found 10.83 and 6.45 issues per PR, or about 1.7x, with the caveat that human labels cannot be guaranteed — [CodeRabbit](https://coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) (snippet only).
- In the Stanford user study (CCS 2023; 47 participants, 33 with AI and 14 without), the AI group wrote less secure code on four of five tasks (for example, 3% against 21% secure on message signing), and it was more likely to believe its code was secure — [arXiv 2211.03622](https://arxiv.org/html/2211.03622v3). The sample is small and the study predates agentic tools.

**Prompt injection into review bots and CI agents**

- "Comment and Control" (Aonan Guan with Johns Hopkins researchers, reported 2026-04-16) affected three tools — [SecurityWeek](https://www.securityweek.com/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments/):
  - In Anthropic's Claude Code Security Review, a crafted PR title led to command execution and credential extraction.
  - In Google's Gemini CLI Action, comments bypassed guardrails and obtained an API key.
  - In GitHub's Copilot Agent, a hidden HTML comment bypassed environment filtering and the network firewall, but the victim had to assign the issue to Copilot.
- Bounties were $100 (Anthropic), $1,337 (Google), and $500 (GitHub). Anthropic disallowed one tool, Google added guardrail prompts, and GitHub called the issue a known architectural limitation. The researcher argues that excessive tool access remains unaddressed, and SecurityWeek's update says that the attack still works in principle with an updated payload — [SecurityWeek](https://www.securityweek.com/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments/).
- A secondary report says the Anthropic variant rated CVSS 9.4 and that Anthropic's documentation warned that the action "is not hardened against prompt injection attacks and should only be used to review trusted PRs" — [Pulse](https://www.pulse.bot/cybersecurity/news/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments-8045c250-964a-4008-a307-78141b2d0d11/) (secondary, snippet only). The CVSS figure was not in my SecurityWeek extraction.
- Cloudflare's Cloudforce One (reported 2026-05-04) tested 100 malicious Workers scripts on seven models over 18,400 API calls. Detection averaged 67.3% at baseline and 53.3% when deceptive comments made up under 1% of a file, and rose to about 98% when they were over 25%, so heavy repetition backfired on the attacker — [IT Brief](https://itbrief.co.uk/story/cloudflare-warns-of-ai-code-review-prompt-injection).
- In that test, detection was near 100% for files under 500KB and 12-18% for files over 3MB. The suggested defences were stripping comments, prioritising functional code, anonymising variable names, and using narrower prompts — [IT Brief](https://itbrief.co.uk/story/cloudflare-warns-of-ai-code-review-prompt-injection). This tests malicious-script classification and not ordinary PR review, so it transfers only partly.
- Secondary sources also mention Copilot CVE-2025-53773 (reported CVSS 9.6, via hidden injection), a June 2026 Trail of Bits chain, and an April 2026 Cline triage-bot token leak, and I did not verify any of these — [Cycode](https://cycode.com/blog/ai-security-vulnerabilities/) and [DEV](https://dev.to/truongandev/ai-coding-agent-security-the-2026-reckoning-32dc) (snippet only).

**AI security review in practice**

- Uber runs a dedicated AppSec assistant within uReview, and Cloudflare includes a security specialist reviewer, but neither publishes security-specific precision or recall — [Uber](https://www.uber.com/blog/ureview/), [Cloudflare](https://blog.cloudflare.com/ai-code-review/).

### Inferences
- The figures answer different questions. Veracode measures model output on curated tasks, Apiiro measures broad findings in one customer data set, CodeRabbit measures its tool's own findings on a small open-source sample, and Stanford measures humans using a 2022-era assistant. They support the same direction, but they should not be combined into one rate.
- The Apiiro comparison could be inflated by adding more code and by the wider definition of "finding", and growth in findings may partly reflect volume.
- A review bot that reads untrusted PR text while holding secrets and tools should be treated as a privileged CI workload. The Comment and Control results suggest that prompt-level guardrails do not change this exposure, so narrowing tool access and credentials is the more reliable control. This inference relies on the researcher's account and on one news report.
- Large-file blindness in the Cloudflare test suggests that large PR limits may matter for AI security review, independent of human reviewer capacity, though this is an extrapolation from a different task.

### Gaps
- I did not read Guan's original post, the vendor advisories, or Cloudflare's original blog, and relied on SecurityWeek and IT Brief.
- I found no large-enterprise study comparing vulnerability rates in AI and human code in production with a controlled design.
- I found no measured false-negative rate for AI security review in production.
- I found no evidence on real-world exploitation of review bots beyond research disclosures and unverified secondary reports.
