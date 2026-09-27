# AI-DLC (AI-Driven Development Life Cycle)

Research report, August 2026, revised September 2026. Related notes:
[specification-driven-development.md](specification-driven-development.md),
[software-dev-with-gen-ai.md](software-dev-with-gen-ai.md),
[agentic-ai.md](agentic-ai.md), [sdlc-context-graph.md](sdlc-context-graph.md),
[ai-security.md](ai-security.md).

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

**The strongest part of the method is the front end. Making an agent interrogate a vague business
intent**, in a room with product, engineering and QA present, surfaces ambiguity early. That is a
genuine benefit and it is mostly a human process improvement rather than an AI one.

The weakest part is the evidence. AWS's headline numbers are vendor claims, one of the most
prominent of them is publicly disputed, and the independent research that does exist points in
a more cautious direction. The method also carries real costs that its advocates understate:
synchronous mob ceremonies are expensive, the artifact discipline adds overhead, and the whole
approach front-loads specification in a way that can reintroduce waterfall behaviour if the team
already leans that way.

As of September 2026 there is still no independent measurement of AI-DLC as a method, and the
surrounding evidence has moved in both directions. AWS now has one large named adopter outside
Amazon, DORA has put an explicit price on the review and verification burden that the method
creates, and METR has weakened the headline result that was the strongest single argument for
caution. Section 7.3 covers all three. The cost side of the argument is now better characterised
than the benefit side.

A reasonable position for most organisations is to adopt the artifacts and the approval gates,
adopt the mob elaboration ritual for genuinely ambiguous work, and ignore the vocabulary.

## 3. The problems it claims to solve

The method is presented as a response to six specific complaints about how software is delivered
today. They are worth separating, because the evidence behind them is uneven and AI-DLC addresses
some of them much more directly than others.

- **Requirements ambiguity surfaces late.** A vague business intent passes through grooming without
  anyone forcing its contradictions into the open, and they reappear as rework several weeks later.
  Mob Elaboration is the direct answer: the agent drafts requirements and clarifying questions, and
  the people who can answer them do so in one session before any code exists. This is the complaint
  the method handles best, and the practitioner reports in section 7.1 credit the ceremony rather
  than the AI for the improvement.
- **The sprint boundary no longer matches the size of the work.** A two-week cycle is a batching
  delay if a feature can be specified and built in an afternoon, which is the argument for the bolt.
  This is the least substantiated item on the list, and section 5.3 notes that nothing in the method
  depends on the new vocabulary.
- **Design decisions are not recorded in a form anyone can audit.** Rationale lives in chat
  transcripts, pull request threads and individual memory, so nobody can later reconstruct why a
  thing was built the way it was, and there is no record of which parts an AI produced and which a
  human approved. The mandated artifact directory and timestamped audit file exist for this, and
  section 8.1 rates that layer as the highest value for the lowest cost.
- **Human effort goes into authoring rather than deciding.** The core loop assumes that typing is no
  longer the constraint, so the human's unit of work should be judgement, and the judgement points
  should be explicit rather than implicit. This is asserted rather than measured, and the DORA and
  METR results in section 7.3 are reasons to treat it carefully.
- **Agents drift when the constraints are not written down.** Without steering files each session
  re-derives the architecture, chooses its own dependencies and reopens settled questions. Writing
  the approved dependencies, architectural rules and regulatory obligations down is useful whether
  or not the rest of the method is adopted, as section 9 sets out.
- **Code is now generated faster than it can be reviewed.** This is the point Wiz makes, covered in
  section 8.4. It is a real problem, but AI-DLC contributes to it as much as it answers it, which is
  why review capacity appears as a prerequisite in section 8.2.

The framing behind the list is itself disputed. The argument in section 7.2 is that AI-DLC starts
from the premise that developers are idle waiting for direction, when product and design have also
become faster and implementation-ready ideas still are not flowing; on that reading the method
elaborates an intent well and says nothing about whether the intent was worth building. Of the six
complaints, the ones this note treats as both real and well addressed are late ambiguity, the
missing decision record, and agent drift.

## 4. Where it came from

- **31 July 2025** — Raja SP publishes *AI-Driven Development Life Cycle: Reimagining Software
  Engineering* on the AWS DevOps blog. This is the founding description of the method.
  [aws.amazon.com](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/)
- **August 2025** — presented at AWS DevSphere in Bengaluru, then repeatedly at AWS events
  through 2025, including a re:Invent 2025 session.
- **29 November 2025** — AWS open-sources the workflows as agent steering rules under MIT-0:
  [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows). The announcement post is
  [Open sourcing adaptive workflows for AI-DLC](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/).
- **2026** — the term escapes AWS. IBM publishes an explainer, Wiz publishes an AppSec view,
  consultancies publish adoption offerings, and a broad "AI-native SDLC" literature grows around
  it. Much of what is now labelled AI-DLC in blog posts is generic spec-driven development, and
  at least one unrelated third-party methodology has been published under the same name with a
  different phase structure of elaboration, execution, operation and reflection. When reading
  anything called AI-DLC it is worth checking whether it describes the AWS method at all.
- **June 2026** — Southwest Airlines and AWS announce a modernisation partnership in which
  Southwest states that it is adopting AI-DLC, with more than 2,700 developers using Kiro to
  rebuild Southwest.com and a target of a fully cloud-based environment by 2028.
  [press.aboutamazon.com](https://press.aboutamazon.com/aws/2026/6/southwest-airlines-partners-with-amazon-web-services-aws-to-accelerate-ai-capabilities-and-technology-modernization)
  This is the first named adopter outside Amazon, and it is an AWS press release reporting scale
  rather than an independent account reporting outcomes.
- **September 2026** — the open-sourced workflows have reached version 2.9.0 and around 4.7k
  stars. Version 2 is considerably larger than what the founding post describes: 14 agents,
  made up of 11 domain experts, two reviewers and an adaptive composer, running across five
  phases and 33 stages, with a "Classic" mode that preserves the 18-stage version 1 flow at one
  approval per stage. It runs on Claude Code, Kiro CLI, Kiro IDE, Codex CLI, Cursor, opencode and
  GitHub Copilot, there is an MCP server for it, and the published roadmap adds first-class
  DevOps and Security agent integrations so that deployment, observability and security review
  also run as governed stages.

Three things follow from the timeline. First, the method is roughly a year old in its published
form, so nobody has multi-year data on it. Second, the early criticism about AWS tool lock-in is
now out of date: the open-sourced rules ship with instructions for Kiro, Amazon Q Developer,
Cursor, Cline, Claude Code, GitHub Copilot, OpenAI Codex and a generic agent profile. Third, the
implementation is growing rather than simplifying, which sharpens the overhead objection in
section 7.2 — a team evaluating AI-DLC today is looking at a larger surface than most published
write-ups describe.

## 5. The idea

### 5.1 The core loop

Every activity in AI-DLC follows the same four-step cycle: the human states intent, the AI
produces a plan and asks clarifying questions, the human resolves the ambiguity and approves,
the AI executes and the human verifies the result. The claim is not that AI writes code faster.
The claim is that the unit of human work moves from authoring to deciding, and that the decision
points are made explicit and recorded.

### 5.2 The three phases

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
spec-driven tooling. In version 2 the selection is made by a dedicated adaptive composer that
assembles a route through the 33 available stages. The adaptivity is real, but the amount a team
has to understand in order to predict what the agent will do has grown rather than shrunk.

### 5.3 The vocabulary

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

### 5.4 The artifacts

The workflows write their output to a documentation directory in the repository, including an
audit file that records each interaction, approval and decision with its raw input and a
timestamp. This is the feature that distinguishes AI-DLC from lighter spec-driven toolkits: the
paper trail is a first-class deliverable, it lives in version control next to the code, and it
survives the deletion of the code it describes. AWS's financial services write-up leans on this
directly, presenting end-to-end traceability from business intent to production code as the
answer to audit and regulatory review, with organisational policy encoded in steering files
(approved dependencies, security standards, architectural rules, regulatory obligations).

## 6. How it compares to the alternatives

### 6.1 The spec-driven landscape

All of these share the same underlying idea: a written specification, not the chat history, is
the source of truth. They differ in how much process they impose around it, and in how much of
the code they expect to stay hand-maintained.

| | AI-DLC | GitHub Spec Kit | BMAD-METHOD | Kiro specs | Google Antigravity | GitHub Agent HQ | Tessl | Ad-hoc agent rules |
|---|---|---|---|---|---|---|---|---|
| **Shape** | Methodology plus steering rules | CLI toolkit | Multi-agent framework | IDE feature | Agent-first platform | Multi-agent control plane | Spec-as-source platform | Whatever you write |
| **Prescribes team process** | Yes: phases, mob ceremonies, bolts | No | Simulates agile roles as agents | No | No | No | No | No |
| **Audit trail** | Explicit, mandated | Spec and plan files only | Agent artifacts | Spec files | Model decides per task | Agent activity, centrally visible | The spec is the record | None by default |
| **Agent portability** | Broad since Nov 2025 | Very broad | Broad | Kiro only | Antigravity only | GitHub and Copilot only | Tessl only | By construction |
| **Overhead** | Highest | Moderate | High | Low | Low | Low per developer, platform setup up front | Unclear, still early | Lowest |
| **Best fit** | Regulated delivery, multi-stakeholder work | General feature work | Large greenfield builds | Individual and small-team work | Work where the plan should vary by task | Running many agents across many teams | Greenfield work willing to stop editing code | Small changes, spikes |
| **Main weakness** | Ceremony and documentation cost; unproven | No governance story | Complexity; agent sprawl | Tied to one IDE | Tied to one platform; no process guidance | Governs agents, not requirements | Largely a thesis so far | Nothing is reproducible |

The three entrants added since the first version of this note are worth describing separately,
because two of them answer the same problems as AI-DLC without proposing a methodology.

- **Google Antigravity** is an agent-first development platform with spec-driven development
  built in, and its design choice is the opposite of a mandated template: the model decides
  whether a given change needs a written artifact at all, and writes a plan specific to the task
  rather than filling in a standard form. Durable constraints live in a "project constitution" of
  non-negotiable principles plus reusable skills, which is the same role AI-DLC's steering files
  play. Google publishes spec-driven development codelabs for it, including one that drives
  Antigravity with GitHub Spec Kit.
  [medium.com](https://medium.com/google-cloud/benefits-and-challenges-of-spec-driven-development-and-how-antigravity-is-changing-the-game-3343a6942330)
- **GitHub Agent HQ** and the Copilot app are a control plane for running several agents at once,
  presented as making agent work visible, auditable and steerable. Microsoft also publishes
  [microsoft/agentic-sdlc-starter](https://github.com/microsoft/agentic-sdlc-starter), a reference
  architecture for spec-driven AI-assisted development on Copilot, MCP and repository-based
  context engineering. Together these compete directly with AI-DLC's audit-trail pitch, but solve
  it at the platform layer instead of the process layer. For most organisations that is the more
  likely route to a usable record, because it does not require anyone to adopt a methodology.
- **Tessl**, founded by Guy Podjarny of Snyk and funded to $125m, takes the idea furthest with
  "spec-as-source": the specification is the artifact you maintain and code becomes a regenerable
  output, so you edit intent rather than code. As of mid-2026 this is mostly still a thesis, and
  it is the clearest statement of where the whole category is pointed.
- **OpenSpec** is the useful structural contrast rather than a competitor. It works in spec
  *deltas* instead of a complete specification written up front, which suits existing systems and
  is a direct answer to the front-loading problem raised in section 7.2.
  [thoughtworks.com](https://www.thoughtworks.com/en-us/radar/tools/openspec)

The practical reading is that AI-DLC buys accountability and pays for it in velocity, which is
the trade a regulated environment usually wants to make and a prototyping team usually does not.
What has changed is that the accountability is no longer only available as a methodology.

### 6.2 How the market now frames the category

- Forrester named agentic software development in its
  [Top 10 Emerging Technologies for 2026](https://www.forrester.com/press-newsroom/forresters-top-10-emerging-technologies-for-2026/)
  and classed it as medium-term, meaning two to five years before it delivers its full benefit.
  That is a reasonable expectation to set internally against vendor timelines.
- Forrester also launched an
  [Agentic Development Platforms Vendor Landscape](https://www.forrester.com/blogs/launching-the-agentic-development-platforms-vendor-landscape-q3-2026/)
  in Q3 2026 covering 25 vendors, and reports that differentiation has shifted away from code
  generation towards orchestration, enterprise governance, model flexibility and cost
  transparency. Those are the things AI-DLC was pitched on, so the method's distinguishing
  features are becoming table stakes in a product category rather than a reason to adopt a
  process.
- The emerging umbrella term for this work is **harness engineering**: the infrastructure,
  constraints and feedback loops built around coding agents to make them reliable. Thoughtworks
  describes spec-driven development as one feedforward control within it, paired with feedback
  controls such as mutation testing. This is a more useful frame than "methodology", because it
  separates the parts that constrain the agent in advance from the parts that catch it afterwards,
  and AI-DLC is almost entirely the former.

## 7. What the community says

### 7.1 The supportive case

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

### 7.2 The critical case

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
- **The artifacts may not be reviewable in practice.** Thoughtworks placed spec-driven development
  in the "assess" ring of
  [Technology Radar volume 34](https://www.thoughtworks.com/about-us/news/2026/combat-ai-cognitive-debt-radar-v34)
  in April 2026 with three reservations: generated specification files are often long enough to be
  hard to review, it is unclear who the audience is for a generated PRD or user story, and the
  "bitter lesson" may apply, meaning that handcrafting detailed rules for a model does not scale
  as models improve. The volume's overall theme is cognitive debt, the widening gap between the
  systems a team owns and what the people on it actually understand. This is the most direct
  challenge to the layer that section 8.1 rates highest, because a specification that is too
  long to be read provides no more assurance than an approval granted without review.

### 7.3 What the evidence actually shows

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
- The Southwest Airlines adoption announced in June 2026 reports scale rather than outcomes: more
  than 2,700 developers using Kiro, and a 2028 target. Amazon's own internal figures are of the
  same kind. The Agent Z programme in Amazon Stores reports more than 21,000 agents created since
  July 2025, including a delivery address optimisation agent credited with 20,500 hours saved and
  a 74.4% reduction in first-delivery defects. None of these numbers is attributable to AI-DLC as
  a method, and they are useful mainly as evidence that the approach is being used at size.

The independent research is more sober, does not measure AI-DLC specifically, and became less
certain rather than more during 2026.

- DORA's [ROI of AI-assisted Software Development](https://dora.dev/ai/roi/report/), published in
  April 2026, is the most directly relevant of these. It models adoption as a J-curve in which
  productivity falls before it rises, and attributes the dip to three causes: the learning curve
  as teams change how they work, the **verification tax** of checking whether generated code is
  correct, secure and consistent with the architecture, and downstream processes such as testing
  and approval that were never sized for the new volume of change. Its illustrative model for a
  500-person engineering organisation gives roughly 39% first-year return and about an
  eight-month payback, on $11.6m of gross value against $8.4m of investment, and the authors
  state plainly that these are high-uncertainty estimates meant to start a conversation rather
  than a formula. The same model prices an instability tax, where a change failure rate moving
  from 5% to 6% costs around $344,000. Its conclusion restates the 2025 one: the returns come
  from the quality of the internal platform, the clarity of workflows and the alignment of teams
  rather than from the tools.
- The [2025 DORA report](https://dora.dev/dora-report-2025/), based on nearly 5,000 respondents,
  found that AI adoption raises throughput and raises instability at the same time, and that AI
  amplifies whatever a team already is. Strong teams get stronger, weak teams get worse faster.
- METR has weakened its own headline result. The
  [original trial](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) of 16
  experienced open-source developers across 246 tasks found them 19% slower with AI tools while
  they believed they had been 20% faster. A larger
  [follow-up published in February 2026](https://metr.org/blog/2026-02-24-uplift-update/), covering
  57 developers, 143 repositories and more than 800 tasks with late-2025 tooling, estimated 18%
  slower for the ten developers who had also taken part in the first study, on a confidence
  interval running from 38% slower to 9% faster, and 4% slower for the 47 new recruits, on an
  interval from 15% slower to 9% faster. METR's own assessment is that this is an unreliable
  signal, because developers who did not want to work without AI declined to take part and
  between 30% and 50% of participants withheld tasks they did not want to attempt unaided, so the
  organisation is redesigning the experiment. Two things follow. The 19% figure should no longer
  be quoted as a current effect, and the durable finding is the gap between measured and perceived
  speed, which remains the reason not to trust self-reported gains from an AI-DLC pilot.
- Scrum.org's [AI4Agile Practitioners Report 2026](https://www.scrum.org/resources/blog/ai4agile-practitioners-report-2026)
  surveys where practitioners think AI fits. Integration uncertainty is the dominant reported
  challenge at 54.3%, eighteen points ahead of the next item, and the most common concerns are
  the erosion of agile values, the loss of human-centred collaboration and reduced critical
  thinking. Both halves matter here: the first explains why a prescriptive method like AI-DLC is
  attractive, since it answers the integration question directly, and the second describes the
  resistance it will meet, since the practices people are worried about losing are the ones it
  proposes to replace.

The honest summary is that there is still no published independent measurement of AI-DLC as a
method. Anyone adopting it is running an experiment, and should instrument it accordingly. What
the 2026 research adds is a better account of the costs than of the benefits: the verification
tax and the instability tax are now described and roughly priced, while the productivity upside
rests on vendor claims and on a research result whose own authors no longer stand behind it.

## 8. Considerations for adopting it in an organisation

### 8.1 Decide what you are actually adopting

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
package is the main way adoptions fail. The separation matters more now that the published
implementation has grown: the 33-stage version 2 described in section 4 is a larger commitment
than most write-ups suggest, and a team that wants only layer 1 can take the artifact formats and
the approval gates without the stage machinery. The Thoughtworks reservation in section 7.2 is
the counter-argument to rating layer 1 so highly, and it is worth taking seriously: the benefit
depends on the artifacts being short enough that reviewers read them, not on their existence.

### 8.2 Prerequisites

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
  already has a pull request backlog will not benefit from generating more code faster. DORA's
  verification tax and instability tax, in section 7.3, are the closest thing available to a price
  for this, and both fall on the review and testing side rather than on authoring, which is the
  side AI-DLC accelerates.

### 8.3 Governance, audit and regulation

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

### 8.4 Security

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

### 8.5 Team and organisational design

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

### 8.6 How to pilot it

- Pick one team and two or three genuinely ambiguous pieces of work. Ambiguity is what the method
  is for; a well-understood change will show nothing.
- Run a control. Comparable work by a comparable team using your current process, over the same
  period. Without this you will be measuring enthusiasm.
- Measure delivery outcomes rather than perceptions: lead time to production, change failure
  rate, time to restore, defect escape rate, and review effort per change. The METR results are
  the reason to distrust self-reported speed.
- Expect the first months to look worse than the baseline. DORA's J-curve predicts a dip before
  any gain, so a pilot measured only at the midpoint will report a failure it would have recovered
  from, and a decision date set too early will throw away a method that was working.
- Track the costs the advocates leave out: hours spent in mob ceremonies, token and tool spend,
  and time spent maintaining steering files and specs.
- Set a decision date and pre-commit to what would count as failure.

### 8.7 Where it fits and where it does not

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

### 8.8 The main failure modes to watch for

- Approval theatre: humans clicking through gates without reading, which produces a complete audit
  trail of unexamined decisions and is worse than no trail at all.
- Specification drift: the code and the spec diverge after the first hotfix, and the artifacts
  become misleading rather than merely stale.
- Volume over value: more features shipped, none of them validated with a user.
- Ceremony without decisions: mobs that cannot resolve the questions the agent asks, because the
  people with authority are not in the room.
- Adopting the vocabulary and nothing else, which is the most common way a methodology gets
  discredited internally.

## 9. Practical starting point

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
them wholesale. Reading version 2 for its stage definitions and then implementing a much smaller
subset is more defensible than installing 33 stages and hoping the adaptive composer picks well.

Two constraints apply to steps 1 and 2. Set a length at which a specification has to be split
rather than accepting whatever the agent produces, since the Thoughtworks objection in section
7.2 is that these files grow past the point where reviewers read them in full. Also check whether
the platform you already run gives you the record you need: if the organisation is standardising on
GitHub Agent HQ or a similar control plane, much of the audit story in section 5.4 arrives
without a methodology attached.

## 10. The context layer the method does not have

AI-DLC's context layer is markdown files in a repository directory. That is what makes it
portable across seven agent harnesses, and it is also its main structural limitation. Most
organisations running agents at scale have built a graph instead, and
[sdlc-context-graph.md](sdlc-context-graph.md) covers that in full. Four points bear directly on
this note:

- **The steering files are an ontology with no schema.** Section 8.2 treats a codified definition
  of "correct" as a prerequisite, and that is exactly what a business ontology is. Written as
  prose it cannot be queried, cannot be checked against the code, and drifts without anything
  detecting the drift. AWS itself now ships an open-source accelerator that drafts such an
  ontology from an organisation's data for expert review and stores it in a knowledge graph, but
  the AI-DLC workflows do not reference it.
- **The audit questions are relationship queries.** The questions internal audit asks in section 8.3 are
  relationship queries: which requirement produced this code, who approved it, was it generated
  or written, and what else did that decision touch. AWS's own AIDLC Collaborative sample
  acknowledges this by holding requirements, stories, designs, decisions and code as typed linked
  items with a traceability graph view.
- **The competition is solving this at the platform layer.** Atlassian's Teamwork Graph, opened
  in May 2026, gives coding agents governed multi-repository context and an audit surface built
  on work items that already exist, so it inherits freshness rather than requiring maintenance.
  That is the same benefit section 5.4 claims, without adopting a methodology.
- **The gain is efficiency rather than correctness.** Published results for code graphs show large
  reductions in tokens, tool calls and latency and only single-digit improvements in task
  resolution. That is worth having against the cost concerns in section 7.3, but it does nothing
  about the review bottleneck, which remains the binding constraint.

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
- [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) — the steering rules, MIT-0, version 2.9.0 as of September 2026.
- [Southwest Airlines partners with AWS](https://press.aboutamazon.com/aws/2026/6/southwest-airlines-partners-with-amazon-web-services-aws-to-accelerate-ai-capabilities-and-technology-modernization) — June 2026, the first named adopter outside Amazon.
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
- [DORA ROI of AI-assisted Software Development](https://dora.dev/ai/roi/report/) — April 2026, the J-curve, the verification tax and the instability tax. [InfoQ summary](https://www.infoq.com/news/2026/05/dora-roi-ai-assisted-dev-report/).
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR, the 19% slower / felt 20% faster result.
- [We are Changing our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/) — METR, February 2026, the wider intervals and why they no longer trust the signal.
- [Technology Radar volume 34](https://www.thoughtworks.com/about-us/news/2026/combat-ai-cognitive-debt-radar-v34) — Thoughtworks, April 2026, cognitive debt and harness engineering. The [spec-driven development entry](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development) carries the reservations.
- [Forrester's Top 10 Emerging Technologies for 2026](https://www.forrester.com/press-newsroom/forresters-top-10-emerging-technologies-for-2026/) — agentic software development as a medium-term technology, and the [Agentic Development Platforms Vendor Landscape, Q3 2026](https://www.forrester.com/blogs/launching-the-agentic-development-platforms-vendor-landscape-q3-2026/).
- [AI4Agile Practitioners Report 2026](https://www.scrum.org/resources/blog/ai4agile-practitioners-report-2026) — Scrum.org, integration uncertainty and what practitioners fear losing.
- [github/spec-kit](https://github.com/github/spec-kit) — the main alternative, no process layer.
- [microsoft/agentic-sdlc-starter](https://github.com/microsoft/agentic-sdlc-starter) — Microsoft's reference architecture for spec-driven work on Copilot and MCP.
- [How Google Antigravity is changing spec-driven development](https://medium.com/google-cloud/benefits-and-challenges-of-spec-driven-development-and-how-antigravity-is-changing-the-game-3343a6942330) — the project constitution and model-decided artifacts. Google also publishes a [spec-driven development codelab](https://codelabs.developers.google.com/sdd-agy-cli).
- [OpenSpec](https://www.thoughtworks.com/en-us/radar/tools/openspec) — spec deltas rather than a full upfront specification, better suited to existing systems.
- [Tessl raises $125M to build AI Native Development](https://tessl.io/podcast/tessl-raises-125m-to-build-ai-native-development) — the spec-as-source position.
- [Infosys SDLC Agent Framework](https://www.infosys.com/iki/techcompass/sdlc-agent-framework.html) and [Capgemini on agentic SDLC](https://www.capgemini.com/ch-en/insights/expert-perspectives/agentic-ai-a-powerful-new-partner-for-your-software-engineering-teams/) — the consultancy offerings, useful for vocabulary rather than evidence.
