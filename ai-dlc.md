# AI-DLC (AI-Driven Development Life Cycle)

Research report, August 2026. Related notes:
[specification-driven-development.md](specification-driven-development.md),
[software-dev-with-gen-ai.md](software-dev-with-gen-ai.md),
[agentic-ai.md](agentic-ai.md), [ai-security.md](ai-security.md).

## 1. What this note covers

AI-DLC is a software delivery methodology published by AWS in 2025. It proposes that the AI
agent, not the developer, drafts the requirements, the plan, the architecture, the code, the
tests and the deployment artifacts, and that humans spend their time validating and deciding
rather than typing. This note describes what the method actually prescribes, how the industry
and the practitioner community have responded, what evidence exists either way, and what an
organisation would have to put in place before adopting it.

## 2. Summary

AI-DLC is best understood as AWS's opinionated version of spec-driven development, with a
process wrapper around it. The spec-driven part (write intent, generate a plan, decompose into
tasks, then generate code, with human approval at each boundary) is not unique to AWS and is
shared with GitHub Spec Kit, BMAD, Kiro's spec mode and OpenSpec. What is distinctive is the
process layer: named phases, named ceremonies, a replacement for the sprint, and a mandated
paper trail of every decision.

The strongest part of the method is the front end. Making an agent interrogate a vague business
intent, in a room with product, engineering and QA present, surfaces ambiguity early. That is a
genuine benefit and it is mostly a human process improvement rather than an AI one.

The weakest part is the evidence. AWS's headline numbers are vendor claims, one of the most
prominent of them is publicly disputed, and the independent research that does exist points in
a more cautious direction. The method also carries real costs that its advocates understate:
synchronous mob ceremonies are expensive, the artifact discipline adds overhead, and the whole
approach front-loads specification in a way that can reintroduce waterfall behaviour if the team
already leans that way.

A reasonable position for most organisations is to adopt the artifacts and the approval gates,
adopt the mob elaboration ritual for genuinely ambiguous work, and ignore the vocabulary.

## 3. Where it came from

- **31 July 2025** — Raja SP publishes *AI-Driven Development Life Cycle: Reimagining Software
  Engineering* on the AWS DevOps blog. This is the founding description of the method.
  [aws.amazon.com](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/)
- **August 2025** — presented at AWS DevSphere in Bengaluru, then repeatedly at AWS events
  through 2025, including a re:Invent 2025 session.
- **29 November 2025** — AWS open-sources the workflows as agent steering rules under MIT-0:
  [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows). The announcement post is
  [Open sourcing adaptive workflows for AI-DLC](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/).
  As of August 2026 the repository is around 4.2k stars and actively maintained.
- **2026** — the term escapes AWS. IBM publishes an explainer, Wiz publishes an AppSec view,
  consultancies publish adoption offerings, and a broad "AI-native SDLC" literature grows around
  it. Much of what is now labelled AI-DLC in blog posts is generic spec-driven development.

Two things follow from the timeline. First, the method is roughly a year old in its published
form, so nobody has multi-year data on it. Second, the early criticism about AWS tool lock-in is
now out of date: the open-sourced rules ship with instructions for Kiro, Amazon Q Developer,
Cursor, Cline, Claude Code, GitHub Copilot, OpenAI Codex and a generic agent profile.

## 4. The idea

### 4.1 The core loop

Every activity in AI-DLC follows the same four-step cycle: the human states intent, the AI
produces a plan and asks clarifying questions, the human resolves the ambiguity and approves,
the AI executes and the human verifies the result. The claim is not that AI writes code faster.
The claim is that the unit of human work moves from authoring to deciding, and that the decision
points are made explicit and recorded.

### 4.2 The three phases

- **Inception.** The AI turns a business intent into requirements, user stories and units of
  work. Scope is validated, assumptions are written down, and the application architecture is
  outlined.
- **Construction.** The AI proposes a domain model and a detailed design, then generates code,
  tests and the testing strategy, with the team reviewing technical choices as they are made.
- **Operations.** The AI produces infrastructure-as-code, deployment automation and monitoring
  configuration, again under human approval.

The open-sourced workflows add an adaptive element: the agent is instructed to run only the
stages a change actually warrants, so a one-line fix does not have to pass through full
architectural elaboration. AWS positions this as the fix for the rigidity of first-generation
spec-driven tooling.

### 4.3 The vocabulary

- **Bolt** replaces the sprint. A bolt is a work cycle measured in hours or days rather than two
  weeks, on the argument that a two-week boundary is meaningless when a feature can be specified
  and built in an afternoon.
- **Unit of Work** replaces the epic. Intent is decomposed into units, and units are executed as
  bolts.
- **Mob Elaboration** is the Inception ceremony. The AI drafts requirements and clarifying
  questions, and product, engineering and QA answer them together in one synchronous session
  before anything is built.
- **Mob Construction** is the equivalent during build: the team validates the design, the
  generated code and the test approach together rather than through asynchronous pull request
  review.

The vocabulary is the part most likely to generate internal resistance and is the part with the
least substance behind it. Nothing in the method breaks if a team keeps saying "sprint".

### 4.4 The artifacts

The workflows write their output to a documentation directory in the repository, including an
audit file that records each interaction, approval and decision with its raw input and a
timestamp. This is the feature that distinguishes AI-DLC from lighter spec-driven toolkits: the
paper trail is a first-class deliverable, it lives in version control next to the code, and it
survives the deletion of the code it describes. AWS's financial services write-up leans on this
directly, presenting end-to-end traceability from business intent to production code as the
answer to audit and regulatory review, with organisational policy encoded in steering files
(approved dependencies, security standards, architectural rules, regulatory obligations).

## 5. How it compares to the alternatives

All of these share the same underlying idea: a written specification, not the chat history, is
the source of truth. They differ in how much process they impose around it.

| | AI-DLC | GitHub Spec Kit | BMAD-METHOD | Kiro specs | Ad-hoc agent rules |
|---|---|---|---|---|---|
| **Shape** | Methodology plus steering rules | CLI toolkit | Multi-agent framework | IDE feature | Whatever you write |
| **Prescribes team process** | Yes: phases, mob ceremonies, bolts | No | Simulates agile roles as agents | No | No |
| **Audit trail** | Explicit, mandated | Spec and plan files only | Agent artifacts | Spec files | None by default |
| **Agent portability** | Broad since Nov 2025 | Very broad | Broad | Kiro only | By construction |
| **Overhead** | Highest | Moderate | High | Low | Lowest |
| **Best fit** | Regulated delivery, multi-stakeholder work | General feature work | Large greenfield builds | Individual and small-team work | Small changes, spikes |
| **Main weakness** | Ceremony and documentation cost; unproven | No governance story | Complexity; agent sprawl | Tied to one IDE | Nothing is reproducible |

The practical reading is that AI-DLC buys accountability and pays for it in velocity, which is
the trade a regulated environment usually wants to make and a prototyping team usually does not.

## 6. What the community says

### 6.1 The supportive case

The recurring positive comment is about Mob Elaboration rather than about AI. An agent that
interrogates a vague intent in front of the whole team surfaces the ambiguities that otherwise
appear as rework several weeks later, and the ceremony forces the people who can resolve those
ambiguities into the same room at the same time. One widely shared Japanese write-up makes the
sharper version of this point: the valuable part of AI-DLC has almost nothing to do with AI, and
is really a design for getting decision-makers to reach consensus without interruption.

Practitioner reports also converge on small cross-functional teams of four to six people, with a
business analyst leading Inception, an architect or senior engineer leading Construction, and QA
present throughout. Decisions are written into the repository so that later sessions and later
agents do not diverge from them.

### 6.2 The critical case

- **It may be solving the wrong bottleneck.** The argument, made most directly in
  [AI-DLC solves the wrong bottleneck](https://wakamoleguy.com/p/ai-dlc-solves-wrong-bottleneck),
  is that AI-DLC starts from the observation that developers are now idle waiting for direction,
  and concludes that developers should be handed raw intent. But product and design are also
  faster with AI, and implementation-ready ideas still are not flowing. The real constraint is
  user understanding, user validation and stakeholder alignment, none of which AI-DLC addresses.
  The risk is that teams ship more volume of low-discovery work.
- **It can reintroduce waterfall.** Arin Sime's
  [analysis](https://agilityfeat.com/blog/will-ai-driven-development-push-us-back-to-waterfall/)
  argues that the danger is not the method itself but organisations with latent waterfall
  tendencies using it as permission to front-load specification and skip customer validation.
  If each phase must complete before the next begins, the result is a sequence of mini-waterfalls.
  His remedy is to shorten the customer feedback loop to match the shortened build loop, not to
  extend the planning phase.
- **The overhead is real.** A practitioner review from ELEKS lists mandatory markdown artifacts,
  mandatory approval gates between phases and a rule set large enough to need onboarding. Their
  conclusion is that the framework trades velocity for accountability and is the wrong choice for
  rapid prototyping.
- **Mob ceremonies do not scale for free.** Putting product, engineering and QA in a synchronous
  session is the most expensive coordination pattern available. It is justified for genuinely
  ambiguous work and hard to justify for routine change.
- **It discards practices that solved real problems.** Several critics object to the "start from
  scratch" framing, on the grounds that Scrum, Kanban and Lean addressed coordination problems
  that AI does not remove.

### 6.3 What the evidence actually shows

AWS's headline figures are vendor claims and should be read as such.

- The most cited is that six engineers rebuilt the Amazon Bedrock inference engine in 76 days
  against an estimate of 40 engineers for a year. This was repeated in Andy Jassy's shareholder
  letter and appears throughout AI-DLC marketing. It is publicly disputed: at least one detailed
  rebuttal claims the real team was a distinguished engineer plus a group of principal engineers,
  working for roughly five months, on a component of an inference platform rather than the whole
  of Bedrock. The rebuttal is itself an unverified blog account, but the claim is contested
  enough that it should not be used as a business case.
- AWS also cites a European financial services firm moving from one product owner and twelve
  developers delivering fifteen features per sprint to one product owner and three developers
  delivering thirty-five, with nine contractor positions removed. There is no independent
  confirmation and no definition of "feature".

The independent research is more sober and does not measure AI-DLC specifically.

- The [2025 DORA report](https://dora.dev/dora-report-2025/), based on nearly 5,000 respondents,
  found that AI adoption raises throughput and raises instability at the same time, and that AI
  amplifies whatever a team already is. Strong teams get stronger, weak teams get worse faster.
  Its central recommendation is that the returns come from platform quality, workflow clarity and
  team alignment rather than from the tools.
- METR's [randomized trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
  of 16 experienced open-source developers across 246 tasks found them 19% slower with AI tools,
  while they believed they had been 20% faster. The tooling has moved on since early 2025, but
  the perception gap is the durable finding, and it is the reason self-reported productivity
  gains from an AI-DLC pilot should not be trusted on their own.

The honest summary is that there is no published independent measurement of AI-DLC as a method.
Anyone adopting it is running an experiment, and should instrument it accordingly.

## 7. Considerations for adopting it in an organisation

### 7.1 Decide what you are actually adopting

The method separates cleanly into three layers, and they have very different cost and value:

1. **Artifacts and approval gates** — specs, plans, decision records, an audit trail in version
   control. High value, low cost, portable to any agent. Adopt this first and independently.
2. **Ceremonies** — Mob Elaboration and Mob Construction. High value on ambiguous work, high
   coordination cost, and it needs the organisation to be able to convene the right people.
   Adopt selectively.
3. **Vocabulary and cadence** — bolts, units of work, the replacement of sprint mechanics. Low
   value, high political cost, and it breaks whatever your delivery metrics currently feed.
   Adopt last, if at all.

Most of the reported benefit sits in layers 1 and 2. Treating the whole thing as one indivisible
package is the main way adoptions fail.

### 7.2 Prerequisites

- **The intent has to have an owner who can answer questions.** Mob Elaboration produces a list
  of clarifying questions. If the business owner is unavailable for two weeks, the method stalls
  in a way that ordinary backlog work does not. In a capital markets setting this is the usual
  binding constraint: the person who knows which client mandates take precedence when two
  restrictions conflict has a day job.
- **A codified definition of "correct" for your domain.** The steering files are where approved
  libraries, architectural rules, data-handling constraints and regulatory obligations live. If
  those rules only exist in senior engineers' heads today, writing them down is the real project,
  and it is worth doing whether or not you adopt AI-DLC.
- **Tests that mean something.** The method leans on the agent validating its own work against
  tests. If the existing suite is thin, AI-DLC accelerates the production of confidently wrong
  code.
- **Review capacity.** The constraint moves from writing code to reviewing it. A team that
  already has a pull request backlog will not benefit from generating more code faster.

### 7.3 Governance, audit and regulation

This is where the method has the most to offer a regulated firm, and where it needs the most
care.

- Decide what the audit trail is *for* before you generate it. If it is genuinely an audit
  artifact, it needs a retention policy, access control and an owner. If it is only a development
  aid, say so, or you will have created a large corpus of discoverable material with no custodian.
- Establish the record of what was AI-generated and what a human approved. This is the question
  internal audit will ask first, and the artifact trail answers it only if approvals are real
  rather than reflexive clicks.
- Map the steering files to actual obligations. Encoding "follow the EU AI Act" as a line in a
  markdown file is not a control. Encoding a specific approved-dependency list, a specific
  logging requirement or a specific data residency rule is.
- Expect model risk questions. In a bank, an agent that writes production code will attract
  attention from model risk management and from operational risk even though it is not a model in
  the traditional sense. Engage those functions before the pilot, not after.
- Human accountability does not transfer. Whoever approves the plan owns the outcome, and that
  should be explicit in the process definition.

### 7.4 Security

Wiz's [AppSec analysis](https://www.wiz.io/academy/ai-security/ai-driven-development-lifecycle-ai-dlc)
makes the central point that code is now generated faster than any human can review it, which
changes what controls have to look like. See [ai-security.md](ai-security.md) for the wider
picture. The specific items to plan for:

- Scanning has to run continuously in the IDE, on the pull request and in CI, not as a nightly
  batch, because misconfigurations now reach production in hours.
- Dependency selection by agents is a supply-chain risk in its own right, including hallucinated
  package names that squatters register. An approved-dependency allowlist in the steering files
  is the direct mitigation.
- Infrastructure-as-code generated at scale replicates a single mistake across many deployments.
  Policy-as-code checks on generated IaC matter more than they did.
- Agents operating in pipelines need least-privilege credentials of their own, and their actions
  need to be attributable.

### 7.5 Team and organisational design

- Small cross-functional teams of four to six with a clear decision-maker per phase. Larger mobs
  degrade quickly.
- The role mix shifts. Demand rises for people who can specify precisely, review critically and
  make architectural judgements, and falls for straightforward implementation. Say this openly.
  The AWS financial services case study is explicitly a headcount reduction story, and staff will
  read it that way whether or not that is your intent.
- Existing delivery metrics break. Story points and velocity are meaningless when work is sized
  in hours, and if your organisation reports on them upward you need a replacement agreed in
  advance.
- Keep the customer feedback loop shorter than the build loop. This is the single most important
  guard against the mini-waterfall failure mode.

### 7.6 How to pilot it

- Pick one team and two or three genuinely ambiguous pieces of work. Ambiguity is what the method
  is for; a well-understood change will show nothing.
- Run a control. Comparable work by a comparable team using your current process, over the same
  period. Without this you will be measuring enthusiasm.
- Measure delivery outcomes rather than perceptions: lead time to production, change failure
  rate, time to restore, defect escape rate, and review effort per change. The METR result is the
  reason to distrust self-reported speed.
- Track the costs the advocates leave out: hours spent in mob ceremonies, token and tool spend,
  and time spent maintaining steering files and specs.
- Set a decision date and pre-commit to what would count as failure.

### 7.7 Where it fits and where it does not

**It fits** work that is ambiguous at the start, has multiple stakeholders who must agree, and
must be defensible afterwards. Examples from a capital markets context: rebuilding a settlement
break investigation workflow, where the rules for classifying a break are folklore spread across
operations teams and the elaboration session is where they finally get written down; changing a
trade surveillance rule set, where the specification and the approval trail are themselves
regulatory artifacts; or implementing a client mandate and restriction engine, where the hard
part is enumerating precedence rules rather than writing the evaluator.

**It does not fit** exploratory work where the point is to learn by building, small well-understood
changes where the ceremony costs more than the change, incident response, or work in a system
whose behaviour nobody can currently specify. It also does not fit an organisation that cannot
reliably get its business stakeholders into a room, because the elaboration ceremony is the whole
mechanism and there is no asynchronous fallback in the method as published.

### 7.8 The main failure modes to watch for

- Approval theatre: humans clicking through gates without reading, which produces a complete audit
  trail of unexamined decisions and is worse than no trail at all.
- Specification drift: the code and the spec diverge after the first hotfix, and the artifacts
  become misleading rather than merely stale.
- Volume over value: more features shipped, none of them validated with a user.
- Ceremony without decisions: mobs that cannot resolve the questions the agent asks, because the
  people with authority are not in the room.
- Adopting the vocabulary and nothing else, which is the most common way a methodology gets
  discredited internally.

## 8. Practical starting point

If the goal is to get most of the value quickly without committing the organisation to a
methodology, a defensible sequence is:

1. Write the steering files: approved dependencies, architectural rules, security and logging
   standards, and the regulatory constraints that apply to the codebase in question. This is
   useful on its own.
2. Adopt spec, plan and decision-record artifacts in version control, with a real approval gate
   before code generation. Any agent can be pointed at these.
3. Run Mob Elaboration for one ambiguous initiative and judge it on whether it surfaced
   requirements you would otherwise have discovered late.
4. Only then decide whether the phase structure and the cadence changes are worth the disruption.

The AWS rules in [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) are MIT-0
and can be read as a reference implementation and adapted, which is a cheaper path than adopting
them wholesale.

## My notes

- Make infrastructure ready for AI
    - Left shift dev environment
    - dev env needs to be more capable and allow running end to end test
    - Improve CI/CD
        - CI/CD should be fast
    - Code structure
        - More mono repo structure? 
- Working team structure
    - Work is done in pair programming fasion with people from different domains e.g. developer, product manager, architect. 
    - People should not be working individually 
- Metric
    - Time taken from ideation to production
    - Compare the cost with previous step
- AWS AI DLC steering tools?


## Resources

- [AI-Driven Development Life Cycle: Reimagining Software Engineering](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/) — AWS, July 2025, the founding post.
- [Open sourcing adaptive workflows for AI-DLC](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/) — AWS, November 2025.
- [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) — the steering rules, MIT-0.
- [Building with AI-DLC using Amazon Q Developer](https://aws.amazon.com/blogs/devops/building-with-ai-dlc-using-amazon-q-developer) — AWS walkthrough.
- [AI-Driven Development Lifecycle for Financial Services](https://aws.amazon.com/blogs/industries/ai-driven-development-lifecycle-for-financial-services/) — AWS, the regulated-industry framing and the vendor metrics.
- [AI-DLC: The AI-Driven Development Lifecycle](https://www.ibm.com/think/topics/ai-dlc) — IBM's neutral explainer.
- [What is AI-DLC? How agentic development reshapes AppSec](https://www.wiz.io/academy/ai-security/ai-driven-development-lifecycle-ai-dlc) — Wiz, security implications.
- [AI-DLC solves the wrong bottleneck](https://wakamoleguy.com/p/ai-dlc-solves-wrong-bottleneck) — the sharpest structural critique.
- [Will AI-Driven Development Push Us Back to Waterfall?](https://agilityfeat.com/blog/will-ai-driven-development-push-us-back-to-waterfall/) — Arin Sime on the mini-waterfall risk.
- [Working with AI-DLC: Team Structure and Practices](https://www.buildwithdc.co/posts/working-with-ai-dlc-team-structure-and-practices/) — practitioner account of roles and ceremonies.
- [AI-DLC Explained: How AWS Labs Brings Structure to AI Coding](https://eleks.com/blog/aws-ai-dlc-explained/) — practitioner review, including the overhead objections.
- [The Essence of AI-DLC is Extreme Decision Making through Mob Work](https://zenn.dev/kiakiraki/articles/437ba4d9441b2b?locale=en) — argues the method is a human process design, not an AI one.
- [DORA State of AI-assisted Software Development 2025](https://dora.dev/dora-report-2025/) — throughput up, instability up, AI as amplifier.
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR, the 19% slower / felt 20% faster result.
- [github/spec-kit](https://github.com/github/spec-kit) — the main alternative, no process layer.
