# Specification Driven Development

Research report, September 2026. Related notes:
[ai-dlc.md](ai-dlc.md), [software-dev-with-gen-ai.md](software-dev-with-gen-ai.md),
[working-with-ai.md](working-with-ai.md), [agentic-ai.md](agentic-ai.md),
[ai-security.md](ai-security.md), [genai-architecture.md](genai-architecture.md).

## 1. What this note covers

Spec-driven development (SDD) is the practice of writing a structured, reviewable specification
of intended behaviour, and treating that specification rather than the chat transcript as the
input a coding agent works from. This note covers what the practice actually is, the tools that
implement it, how teams are adopting it, what the measured evidence says, where it fails, and
what an organisation would need to put in place to adopt it deliberately.

## 2. Summary

The uncontroversial part of spec-driven development is that agents produce better results when
given a written, reviewed statement of intent than when given a one-line prompt. Essentially
every practitioner report agrees on this, and the industry has largely absorbed it as a default
working practice rather than a named methodology.

The contested part is how much apparatus that statement of intent needs. The first generation of
tools, released through late 2025, generated large sets of markdown artifacts through fixed phase
gates. Measured against iterative prompting, several independent trials found this produced
comparable code for several times the tokens, several times the elapsed time, and a much larger
review burden. The market has since corrected towards lighter tooling and towards built-in plan
modes in the agents themselves.

The unsolved problem is drift. A specification that is not mechanically tied to the code diverges
from it, and a stale specification is worse than no specification, because an agent will follow it
confidently and will not flag the inconsistency. The research and tooling frontier in 2026 is
drift detection and enforcement rather than richer specification formats.

For an organisation, the reasonable position is to adopt the artifacts and the review gate, size
the ceremony to the change, keep specifications scoped to the area being modified rather than to
the whole system, and invest in the mechanical checks that keep specification and code aligned.
The methodology branding is optional and mostly a distraction.

## 3. What the practice actually is

### 3.1 The core loop

Nearly every implementation follows the same sequence, with different names for the steps.

1. **Establish standing context.** A durable file or set of files describing the project's
   principles, technology constraints, architectural rules and conventions. Spec Kit calls this
   the constitution, Kiro calls it steering, AWS AI-DLC calls it steering rules, and the
   tool-agnostic convention that emerged in 2026 is `AGENTS.md`. This is loaded at the start of
   every session and is the cheapest high-value part of the whole practice.
2. **Specify.** A statement of what should happen, expressed as requirements and acceptance
   criteria, deliberately excluding how it should be implemented.
3. **Clarify.** The agent asks questions about ambiguities it found. This step is where most of
   the reported value sits, because the questions surface decisions nobody had made.
4. **Plan.** The technical design: components touched, data model changes, interfaces, sequencing.
   This is where the how appears.
5. **Tasks.** Decomposition into units small enough for an agent to execute and a human to review.
6. **Implement.** Code generation, usually task by task rather than in one pass.
7. **Validate or converge.** Checking the implementation against the specification, and updating
   whichever of the two turned out to be wrong.

The human decision points are between steps 3 and 4, and between steps 5 and 6. Everything else
can be delegated. The value of the method depends almost entirely on whether those two review
gates are real.

### 3.2 Three levels of ambition

The most useful framing in the field comes from Birgitta Böckeler's October 2025 analysis on
martinfowler.com, and has since been adopted by the academic survey literature. The three levels
differ in what happens to the specification after the code exists.

- **Spec-first.** The specification is scaffolding for one piece of work. It is written, used to
  generate code, and then effectively discarded. This level is cheap, low-risk and largely
  uncontroversial. Most real adoption is here.
- **Spec-anchored.** The specification persists in version control and is maintained alongside the
  code, so that future changes start from it. This is the level most guidance recommends and the
  level where drift is the unsolved problem.
- **Spec-as-source.** The specification is the only artifact humans maintain; code is generated
  and never hand-edited. Tessl is the main commercial attempt at this. It remains unproven, and
  its framework has stayed in restricted beta for roughly a year.

Being explicit about which level you are adopting matters, because the tools disagree about it and
because the cost profile is completely different. Spec-first costs a document per change.
Spec-as-source costs a rebuild of how the organisation maintains software.

### 3.3 What actually goes in a specification

The technical detail that separates a useful specification from a verbose one:

- **Acceptance criteria in a constrained syntax.** The pattern that has spread furthest is EARS
  (Easy Approach to Requirements Syntax), originally developed at Rolls-Royce for aerospace
  requirements and now the default in Kiro's `requirements.md`. Its core form is
  `WHEN <trigger> THE SYSTEM SHALL <observable behaviour>`, with variants for state-driven
  (`WHILE`), optional (`WHERE`) and unwanted-behaviour (`IF … THEN`) requirements. A constrained
  sentence is a better instruction to a literal machine than a fluent paragraph, and it converts
  directly into a test case. This is the single highest-value technique in the whole practice.
- **Machine-checkable contracts wherever one exists.** OpenAPI for REST interfaces, Avro or
  Protobuf schemas for events, JSON Schema for payloads, Pact or Specmatic for consumer-driven
  contract tests. Where a contract can be validated by a tool in CI, it should be, and the prose
  specification should reference it rather than restate it. This is the part of SDD that predates
  the LLM tooling by a decade and already works.
- **Explicit non-goals and out-of-scope statements.** Agents expand scope when the boundary is
  unstated. Naming what the change must not touch is more effective than it sounds.
- **The decisions that were made and rejected.** A short decision record per change, kept next to
  the specification, is what stops the next session re-litigating a settled question.
- **What is deliberately left open.** If the specification pins down implementation detail that
  does not matter, it has become pseudo-code and the program has been written twice.

The corresponding anti-pattern, seen repeatedly in tool output, is a specification that restates
what already exists in the codebase. Böckeler found that Spec Kit, run against an existing
codebase, documented classes that were already there, after which the agent read its own
description as a new requirement and generated duplicates.

## 4. Where it came from

- **Long before the current tooling.** Design by contract, behaviour-driven development, and
  API-first development with OpenAPI are all specification-driven in the original sense. The
  academic lineage runs back to Ostroff, Makalsky and Paige's agile variant combining test-driven
  development with design by contract. Model-driven development attempted the spec-as-source idea
  in the 2000s and failed on overhead and inflexibility, which is the closest historical analogue
  and worth taking seriously.
- **14 July 2025.** AWS announces Kiro, an agentic IDE built on Code OSS whose defining feature is
  generating `requirements.md`, `design.md` and `tasks.md` before writing code.
- **September 2025.** GitHub open-sources [Spec Kit](https://github.com/github/spec-kit), a
  CLI that installs the workflow into any of a long list of coding agents. This is the point at
  which the term enters general use.
- **October 2025.** Böckeler publishes the comparison of Kiro, Spec Kit and Tessl that establishes
  the spec-first / spec-anchored / spec-as-source vocabulary, along with the first widely read
  criticism.
- **November 2025.** Thoughtworks places spec-driven development in the Assess ring of its
  Technology Radar, with the caution that the workflows are elaborate and opinionated and that the
  industry may be relearning the bitter lesson that hand-crafted rules for AI do not scale.
  AWS open-sources its AI-DLC workflows in the same month. Mercari publishes its internal Agent
  Spec-Driven Development methodology in December.
- **Through 2026.** The practice fragments into tools rather than consolidating into a methodology.
  OpenSpec and GitHub Spec Kit both appear in the Assess ring of the April 2026 Radar, while
  spec-driven development as a technique drops off the current edition. Kiro reaches general
  availability on 7 May 2026 and replaces Amazon Q Developer, whose IDE plugins are supported
  until 30 April 2027. Spec Kit ships v1.0.0 on 21 August 2026, adding a `converge` step aimed
  squarely at drift. Thoughtworks reframes the whole area as *harness engineering*: the
  feed-forward controls (specs, skills, conventions) and feedback controls (tests, static
  analysis, mutation testing) that make agents reliable.

The shape of the last year is that the idea won and the first-generation tooling lost. Plan modes
built into the agents themselves now do most of what the early frameworks did, with less ceremony.

## 5. The tool landscape

Each tool below is described with the same structure so they can be compared directly.

### 5.1 GitHub Spec Kit

- **How it works.** A Python CLI (`specify init`) installs slash commands and markdown templates
  into your repository for whichever agent you use. The v1.0 workflow is constitution → specify →
  clarify → plan → tasks → implement → converge, with `analyze` and `checklist` as additional
  quality gates. Artifacts land in a per-feature directory, historically on a branch per
  specification.
- **Strengths.** It is the reference implementation and the most agent-portable option, with
  support for roughly thirty agents. The templates are genuinely well thought out, particularly
  the clarify step. The constitution mechanism is a clean way to encode organisational rules. It
  is free and MIT-licensed, and it reached v1.0 with a real answer to drift in the `converge`
  command.
- **Weaknesses.** It is the heaviest of the open-source options. It does not size itself to the
  change: the same seven phases apply to a one-line fix and a new subsystem. Its artifact volume
  is the source of the most-cited criticism in the field — François Zaninotto at Marmelab recorded
  eight files and roughly 1,300 lines of specification for a feature that displays the current
  date. Branch-per-spec pushes it towards spec-first behaviour even though the documentation
  aspires to spec-anchored.
- **Cost.** Free, but the token cost is the real number. Independent comparisons put it at roughly
  twice the tokens of OpenSpec for equivalent work, and Scott Logic reported a Spec Kit run around
  ten times slower than iterative prompting for the same task. GitHub's own issue tracker carries
  excessive-token-usage reports.
- **Worked example.** Building a new trade surveillance rule set from scratch, where the rule
  definitions, their parameters and their alert thresholds are themselves regulatory artifacts that
  need to be written down, reviewed by compliance and retained. Here the artifact volume is not
  overhead, because the documents were going to be produced anyway.

### 5.2 OpenSpec

- **How it works.** An MIT-licensed framework from Fission AI, installed with `openspec init`,
  built around **delta specs**. Instead of restating the whole specification for each change, a
  change proposal records only `ADDED`, `MODIFIED` and `REMOVED` requirements against a
  source-of-truth spec. The loop is `propose` → `apply` → `sync` (merge the deltas into the main
  specs) → `archive`.
- **Strengths.** It is the best fit for brownfield work, because the delta model matches how
  existing systems actually change. Setup is minutes rather than half an hour, there is no Python
  dependency, and it is tool-agnostic. In side-by-side comparisons it repeatedly scores highest on
  friction and delivered comparable or better results at roughly half the token cost of Spec Kit.
  Thoughtworks put it in Assess in April 2026.
- **Weaknesses.** The `sync` step is a manual discipline, so drift is managed by hand rather than
  enforced. It offers less structure for teams that actually want the process scaffolding, and it
  has no governance or audit story of its own.
- **Cost.** Free, and the cheapest of the structured options in tokens.
- **Worked example.** Adding a new break category to an existing settlement break classification
  service. The delta names the new category, its matching rules and its routing, without
  re-specifying the twenty categories that already work.

### 5.3 Amazon Kiro

- **How it works.** A full IDE built on Code OSS, powered by Claude through Amazon Bedrock.
  A prompt produces `requirements.md` in EARS notation, `design.md` with architecture and sequence
  diagrams, and `tasks.md` as a sequenced plan. Steering files (`product.md`, `tech.md`,
  `structure.md`) hold persistent project context. Agent hooks can trigger actions on file events.
- **Strengths.** The lowest-friction path for an individual developer, because the workflow is in
  the IDE rather than in a CLI on top of it. EARS-formatted requirements are the best default
  output format of any tool here. It is a supported AWS product with an enterprise purchasing path,
  which matters in a regulated firm.
- **Weaknesses.** You are inside one IDE, and the specifications are less portable in practice than
  the plain markdown suggests. The over-ceremony problem is at its most visible here: Böckeler
  reported Kiro generating four user stories and sixteen acceptance criteria for a small bug fix.
  Credit metering makes cost hard to predict.
- **Cost.** Credit-metered: a free tier with 50 monthly credits, then roughly 20, 40, 100 and 200
  US dollars per user per month for 1,000, 2,000, 5,000 and 10,000 credits, with additional credits
  around four cents each. Budget for the metering rather than the headline price.
- **Worked example.** A developer implementing a well-bounded change to a corporate actions
  processing rule, where EARS acceptance criteria map cleanly onto the existing test suite and the
  whole change fits one session.

### 5.4 BMAD-METHOD

- **How it works.** An open-source framework that simulates a full delivery team as named agent
  personas — analyst, product manager, architect, scrum master, developer, QA — with strict role
  boundaries and file-based context handoff between them.
- **Strengths.** The most thorough front end of any option for genuinely greenfield work, and the
  role separation produces artifacts that map onto how an enterprise already organises delivery.
  Large and active community.
- **Weaknesses.** The highest learning curve and the highest token cost. Agent sprawl is a real
  operational problem, and the ceremony is difficult to justify for anything routine.
- **Cost.** Free, with the highest token consumption of the open-source options.
- **Worked example.** A ground-up build of a client mandates and restrictions engine, where the
  hard work is enumerating precedence rules across overlapping restrictions and the multi-persona
  interrogation earns its cost.

### 5.5 Tessl

- **How it works.** A commercial framework installed as "tiles" into a `.tessl/` directory, which
  teaches any MCP-compatible agent a spec-driven workflow. Specifications map to individual source
  files, which are marked as generated and not to be edited, with tags such as `@generate` and
  `@test` controlling output. Separately, the Tessl Spec Registry publishes more than ten thousand
  specifications for open-source libraries, so that agents call their APIs correctly rather than
  hallucinating method signatures.
- **Strengths.** The only serious attempt at spec-as-source, and the clearest articulation of the
  thesis that code becomes a regenerable output. The Spec Registry is useful on its own and is free
  to use, independent of the framework.
- **Weaknesses.** The framework has been in closed or restricted beta for around a year with no
  general availability, and the spec-as-source model is unproven at any scale. Non-determinism is
  the structural objection: the same specification does not regenerate the same code twice, so
  "just regenerate it" is not equivalent to recompiling.
- **Cost.** Registry free; framework commercial and gated.
- **Worked example.** Not one I would run on a production system yet. The Spec Registry, however,
  is worth adopting immediately for any codebase where agents call unfamiliar libraries.

### 5.6 Built-in plan modes

- **How it works.** Claude Code's plan mode, and the equivalents now shipping in most agents, do
  read-only analysis, produce a reviewable plan, take your edits, then implement. One document, one
  round of iteration, then code.
- **Strengths.** No framework to install, no artifact sprawl, and it captures most of the benefit,
  which is the forced pause and the reviewed statement of intent. This is now the most common
  real-world lightweight workflow, and several practitioners who trialled the heavy frameworks
  returned to it.
- **Weaknesses.** Nothing persists. There is no reusable specification, no audit trail, and no
  shared artifact for a product owner or compliance reviewer to read. It is spec-first only, by
  construction.
- **Cost.** Included in the agent subscription; the lowest token overhead of any option.
- **Worked example.** Almost all routine change: a bug fix in a reconciliation job, a library
  upgrade, adding a field to an existing report.

### 5.7 Side-by-side comparison

| | Spec Kit | OpenSpec | Kiro | BMAD-METHOD | Tessl | Plan mode |
|---|---|---|---|---|---|---|
| **Shape** | CLI + templates | CLI + delta specs | IDE | Multi-agent framework | Framework + registry | Agent feature |
| **Level** | Spec-first, aspires to anchored | Spec-anchored | Spec-first | Spec-first | Spec-as-source | Spec-first |
| **Greenfield fit** | Strong | Adequate | Strong | Strongest | Unproven | Weak |
| **Brownfield fit** | Weak, duplicates existing code | Strongest | Moderate | Weak | Unproven | Strong for small change |
| **Agent portability** | ~30 agents | Tool-agnostic | Kiro only | Broad | MCP-compatible agents | N/A |
| **Requirements format** | Prose + checklists | Prose deltas | EARS | Persona-authored docs | Tagged specs | Free-form plan |
| **Drift handling** | `converge` (v1.0) | Manual `sync` | None | None | Regeneration | None |
| **Token cost** | High | Low | Metered, opaque | Highest | Unknown | Lowest |
| **Governance / audit** | Constitution, artifact trail | Change archive | Steering files | Role artifacts | Spec as record | None |
| **Main weakness** | Ceremony and verbosity | Drift managed by hand | Single IDE, over-specifies small work | Complexity and cost | Unproven, non-deterministic | Nothing persists |

Adjacent to these, [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) wraps the
same core loop in a full delivery methodology with mandated approval gates and an audit trail; see
[ai-dlc.md](ai-dlc.md) for the detail. The contract-testing and schema tools — OpenAPI, Protobuf,
Pact, Specmatic, Cucumber — are not competitors to these tools but the layer underneath them, and
they are what turn a specification into something a machine can check.

## 6. How teams are actually adopting it

- **Adoption is broad in awareness and shallow in depth.** JetBrains' AI Pulse survey of around
  11,000 developers in January 2026 found 90% using AI at work but only 13% using it across the
  whole software development lifecycle. Spec-driven development in its full form sits in that 13%.
  Spec-first habits, by contrast, are close to universal among people using agents seriously.
- **The dominant pattern is one specification per change, not one per system.** The consistent
  advice from enterprise write-ups is that the specification should be most granular near the area
  of change. Teams that tried to specify a whole application either exceeded the context window or
  produced something no human would review.
- **Brownfield is where the interest is, and where the tools are weakest.** Thoughtworks reports
  most of its Spec Kit experimentation happening in brownfield environments. The practice that
  works there is extracting a specification of current behaviour for the slice being modified,
  which doubles as a way to distinguish required behaviour from accumulated accident.
- **The specification is becoming the cross-functional interface.** The recurring organisational
  observation is that the specification is where product, architecture and engineering converge
  simultaneously, rather than handing artifacts down a chain. This is a process change more than a
  technology change, and it is the same observation the AI-DLC community makes about mob
  elaboration.
- **Ceremony is being cut.** The market moved through 2026 from heavyweight frameworks towards
  delta-based tools, minimal harnesses distributed as agent skills, and built-in plan modes.
- **Published organisational results exist but are self-reported.** Mercari published its Agent
  Spec-Driven Development methodology in December 2025 and reported, six months in, a 150%
  improvement over its traditional baseline and 80% over freeform prompting, along with a project
  estimated at six months delivered by two engineers in six weeks. These are the firm's own
  figures with no independent replication, and should be read the same way as AWS's AI-DLC numbers.

## 7. What the evidence shows

### 7.1 Findings that hold up

- **A reviewed written intent beats a prompt.** This is the one point on which supporters and
  critics agree. Where the disagreement starts is how long that document needs to be.
- **Human-refined specifications reduce generated-code errors materially.** The survey literature
  cites controlled studies showing error reductions up to roughly 50% when a human refines the
  specification before generation. The important qualifier, stated in the same papers, is that
  passing the specification's tests only proves the code matches the specification, not that the
  software is correct.
- **Constrained requirement syntax works.** EARS-formatted acceptance criteria are consistently
  reported as reducing ambiguity and as portable across tools, and they convert directly into
  tests.
- **Code health dominates.** Research associated with Adam Tornhill and CodeScene puts roughly 30%
  higher defect risk on AI-generated changes in less-healthy code. A specification does not fix
  this; the specification quality ceiling is set by the codebase it is written against.
- **AI amplifies the existing system.** DORA's 2025 report, from close to 5,000 respondents, found
  AI raising both throughput and instability and concluded that AI magnifies whatever a team
  already is. Its 2026 follow-up on return on investment reaches the same conclusion from the other
  direction: the returns come from platform quality, workflow clarity and team alignment rather
  than from the tools.
- **Self-reported speed is not reliable.** METR's randomised trial of 16 experienced open-source
  developers across 246 tasks found them 19% slower with AI tools while believing they had been 20%
  faster. The tooling has improved since early 2025; the perception gap is the durable result and
  is the reason a spec-driven pilot must be measured rather than surveyed.

### 7.2 Findings that argue against the heavy frameworks

- **Marmelab, November 2025.** Eight files and roughly 1,300 lines of specification for a feature
  that displays the current date.
- **Scott Logic.** A Spec Kit run around ten times slower than iterative prompting for the same
  work, with output of comparable quality.
- **An independent head-to-head, 2026.** 33 minutes and 2,577 lines of markdown to produce 689
  lines of code under a full SDD workflow, against 8 minutes with iterative prompting, with no
  quality difference the author could detect.
- **Token economics.** Spec Kit measured at up to twice OpenSpec's token consumption for equivalent
  or worse results, with a meaningful share of those tokens spent reasoning about the framework's
  own rules rather than the task.
- **Practitioner field synthesis.** Specification work consuming around half of total project time
  on small features; agents ignoring elaborate specification requirements they had been given; and
  reviewers spending their time reading long markdown files hunting for basic mistakes rather than
  reviewing code.

### 7.3 The academic frontier

- **[arXiv:2602.00180](https://arxiv.org/abs/2602.00180)** (Piskala, January 2026) is the closest
  thing to a survey of the field, and formalises the spec-first / anchored / as-source taxonomy
  along with a catalogue of pitfalls.
- **[arXiv:2606.30689](https://arxiv.org/abs/2606.30689)** (June 2026) compares traceSDD, which
  mandates a per-line requirement citation in generated code, against Spec Kit's artifact-level
  traceability and OpenSpec's post-hoc trace maps, across two frontier models. It finds a direct
  trade-off: uncited conditions produce more deterministic output, while only cited conditions make
  automated hallucination detection possible, at detection rates around 86–88%. This is the most
  technically interesting result in the area, because it says traceability is not free.
- **[arXiv:2605.12981](https://arxiv.org/abs/2605.12981)** proposes protocol-driven development,
  replacing the upfront specification as sole authority with formal invariants plus continuous
  runtime evidence that those invariants hold. This is the most credible structural answer to the
  drift problem.
- **[arXiv:2601.03878](https://arxiv.org/abs/2601.03878)** is a registered report accepted at SANER
  2026 studying how human refinement of specifications and tests affects generated code, using a
  purpose-built VS Code extension. The protocol is peer-reviewed; results are not published yet.
  It is worth watching, because it is one of the few properly controlled studies in progress.

There is still no independent controlled trial of spec-driven development as a delivery practice at
organisational scale. Anyone adopting it is running an experiment.

## 8. Challenges and failure modes

- **Drift is the central unsolved problem.** Specification and code diverge from the first hotfix.
  Maintaining the specification is invisible work competing with visible work, and it loses. The
  consequence is worse with agents than with humans: a stale design document misleads a person who
  may notice, whereas an agent executes it confidently and does not flag the mismatch.
- **Non-determinism undermines the contract.** The same specification produces different
  implementations across runs, with different structures and different error handling. A
  specification's authority over the implementation is a probability, not a guarantee, and that
  probability falls as the document grows. This is the objection that most directly blocks
  spec-as-source.
- **Natural language remains ambiguous.** Writing the requirement down does not make it precise.
  This is why the EARS and machine-checkable-contract parts matter more than the prose parts.
- **Review load moves rather than disappearing.** Teams end up reviewing generated markdown and
  then reviewing generated code. Several practitioners report preferring code review to markdown
  review, and reviewer fatigue leads to rubber-stamping, which produces a complete paper trail of
  unexamined decisions.
- **The workflow does not size itself.** Full ceremony on a bug fix is the most commonly reported
  failure. The corollary is also true: for a large system, no single specification is reviewable.
- **Brownfield breaks the assumptions.** Comprehensive specification of a codebase with hundreds of
  thousands of files is impossible within context limits and human review capacity; tribal
  knowledge needed to write the specification has left the firm; implicit cross-module dependencies
  are invisible; behavioural contracts such as ordering and timing assumptions have to be
  reverse-engineered; and AI defect rates are higher in exactly the unhealthy code that legacy
  systems consist of.
- **False confidence is the dangerous one.** A reviewed and approved wrong specification produces
  wrong software with institutional authority behind it. The specification review gate creates the
  impression of assurance whether or not the review was substantive.
- **It can reintroduce waterfall.** Sequential phase gates with completion criteria are big design
  up front under a new name. The risk is not the artifacts, it is organisations with existing
  waterfall tendencies using the method as permission to front-load specification and skip
  validation with users.
- **Cost is real and invisible.** Overhead tokens do not show up unless you instrument for them.
  At frontier-model pricing, the per-session overhead is small and the monthly total at team scale
  is not.
- **The historical warning.** Model-driven development attempted specification-as-source two
  decades ago and failed on overhead and inflexibility. LLMs remove some of the constraints that
  killed it and add non-determinism, which MDD did not have. That is not a reason to dismiss the
  idea, but it is a reason to require evidence before committing to the strongest form of it.

## 9. Adopting it in an organisation

### 9.1 Decide which layer you are adopting

The practice separates into layers with very different cost and value. Adopting them as one package
is the most common way this fails.

1. **Standing context files.** A repository-level `AGENTS.md` or equivalent holding approved
   libraries, architectural rules, security and logging standards, naming conventions, and the
   regulatory constraints that apply. High value, low cost, portable across every tool, and useful
   even if you abandon everything else. Start here.
2. **Machine-checkable contracts.** OpenAPI, schemas, contract tests, and acceptance criteria in
   EARS form wired into the test suite. High value, moderate cost, and this is the part that
   actually constrains an agent rather than merely advising it.
3. **Per-change specification artifacts and a review gate.** A specification and a decision record
   per change, in version control, reviewed before code generation. High value if the review is
   real, moderate cost.
4. **A named framework with phase gates.** Spec Kit, BMAD or AI-DLC in full. Worth it for
   high-stakes, multi-stakeholder or audited work; not worth it for routine change.
5. **Spec-as-source.** Not yet. Revisit when a tool demonstrates deterministic regeneration.

### 9.2 Prerequisites

- **A codified definition of correct.** The standing context files are where your approved
  dependency list, architectural rules, data-handling constraints and regulatory obligations live.
  If those rules currently exist only in senior engineers' heads, writing them down is the real
  project, and it pays for itself regardless.
- **A test suite that means something.** The method leans on validating generated code against
  tests. A thin suite means the practice accelerates the production of confidently wrong code.
- **Review capacity.** The bottleneck moves from writing to reviewing. A team with an existing pull
  request backlog will not benefit from generating more code faster.
- **Someone who can answer the clarifying questions.** The clarify step produces a list of
  decisions. If the person who knows which client mandate takes precedence when two restrictions
  conflict is unavailable for two weeks, the work stalls in a way ordinary backlog work does not.
- **Healthy enough code in the target area.** Given the higher defect risk in unhealthy code,
  choosing where to start matters more than choosing which tool.
- **Fast CI and a capable development environment.** If the feedback loop is slow, the agent cannot
  self-correct and every error surfaces at review time instead.

### 9.3 A reference framework to put in place

A concrete shape that does not depend on any one vendor:

- **Repository layout.** `AGENTS.md` at the root for standing context. A `specs/` directory holding
  one directory per change, containing the specification, the acceptance criteria, the decision
  record, and a link to the pull request. Archive completed changes rather than deleting them, so
  the directory becomes a searchable record of why the system is the way it is.
- **Specification template.** Context and problem; in scope and explicitly out of scope; acceptance
  criteria in EARS form; interfaces and schemas affected, by reference to the contract files rather
  than restated; data and migration impact; non-functional constraints with numbers rather than
  adjectives; open questions; decisions made and rejected. Cap it. A specification that exceeds two
  or three pages for a normal change is a signal to split the change, not to keep writing.
- **Sizing rule, written down.** Define, in advance, which changes get full ceremony, which get a
  plan-mode plan only, and which get neither. Something like: full specification for anything that
  changes an external contract, touches a regulated calculation, or spans more than one service;
  plan mode for everything else; nothing for typo-level fixes. Without an explicit rule, teams
  default to full ceremony and then quietly abandon the whole practice.
- **CI enforcement, because discipline alone will not hold.** Validate OpenAPI and schema files
  against the running service. Run consumer-driven contract tests. Fail the build when a pull
  request changes a contract without changing the corresponding specification. Require a
  specification reference in the pull request template for changes above the sizing threshold.
  These mechanical checks are what separates spec-anchored from spec-first in practice.
- **Traceability, if you need it.** Requirement identifiers carried into test names, so coverage of
  acceptance criteria is measurable and a regulator's question maps to a test. Note the research
  finding that per-line citation discipline improves hallucination detection but reduces output
  determinism, so apply it where the audit value justifies the cost rather than everywhere.
- **Drift review.** A recurring, scheduled task that reconciles specifications against code in the
  areas that changed. Treat it as maintenance, budget for it, and delete specifications you are not
  going to maintain. A deleted specification is honest; a stale one is not.
- **Harness improvement loop.** After each significant piece of agent work, capture what the agent
  got wrong and fix it in the standing context, the templates, or the tests, rather than in a
  one-off correction. This is the highest-leverage habit in the whole practice and costs nothing.

### 9.4 Rollout plan

- **Phase 0, two to four weeks.** Write the standing context files for one codebase. Measure your
  current baseline: lead time to production, change failure rate, defect escape rate, review time
  per pull request, and current AI tool spend. Without a baseline the pilot cannot be judged.
- **Phase 1, four to six weeks, one team.** Plan mode plus a lightweight specification template.
  No framework yet. Pick two or three genuinely ambiguous pieces of work, because well-understood
  changes will show nothing. Run a comparable team on the current process over the same period as a
  control.
- **Phase 2, six to eight weeks.** Add machine-checkable contracts and EARS acceptance criteria in
  the pilot area, and add the CI gates. This is the phase that produces the durable benefit, and it
  is also the phase most likely to be skipped because it is unglamorous.
- **Phase 3.** Only now evaluate a framework, and evaluate it against the sizing rule you wrote in
  Phase 1. For brownfield, start with OpenSpec's delta model. For audited greenfield work, evaluate
  Spec Kit or AI-DLC.
- **Phase 4.** Roll out the template, the standing context convention and the CI gates as the
  organisational standard. Leave tool choice to teams. Standardising the artifacts and the gates
  matters; standardising the tool does not, and the tooling is moving too fast to be worth mandating.
- **Set a decision date, and pre-commit to what failure looks like.**

### 9.5 What to measure

- Lead time from intent to production, and change failure rate. These are the outcomes.
- Defect escape rate and rework rate, which is where a real specification benefit should appear.
- Review effort per change, split between specification review and code review. If specification
  review is not reducing code review, the practice is adding work rather than moving it.
- Specification drift rate: how many merged changes modified code covered by a specification
  without updating it. This is the leading indicator of the whole thing decaying.
- Token and tool spend per change, instrumented explicitly, since overhead is otherwise invisible.
- Time spent in clarification, and the number of requirements changed as a result. This is the
  quantity that most directly represents the value of the front end.
- Do not measure developer-reported speed and treat it as evidence. The METR result is the reason.

### 9.6 Governance, audit and security

- **Decide what the artifact trail is for before generating it.** If specifications are audit
  artifacts, they need an owner, a retention policy and access control. If they are a development
  aid, say so, or you have created a large corpus of discoverable material with no custodian.
- **Record what was AI-generated and what a human approved.** This is the first question internal
  audit will ask, and the trail only answers it if approvals are substantive rather than reflexive.
- **Encode obligations specifically.** "Comply with the EU AI Act" in a markdown file is not a
  control. An approved-dependency allowlist, a specific logging requirement, a data residency rule
  or a named retention period is.
- **Expect model risk and operational risk questions.** In a bank, an agent generating production
  code will attract attention from functions that do not think of themselves as covering software
  tooling. Engage them before the pilot.
- **Security controls have to move left and run continuously**, because generated code reaches
  review faster than review can absorb it. Dependency selection by agents is a supply-chain risk in
  its own right, including hallucinated package names that squatters register; the approved-
  dependency list in the standing context is the direct mitigation. Generated infrastructure-as-code
  replicates a single mistake across every deployment, so policy-as-code checks matter more than
  they did. See [ai-security.md](ai-security.md).
- **Accountability does not transfer to the specification.** Whoever approves it owns the outcome,
  and that should be written into the process definition rather than left implied.

### 9.7 Where it fits and where it does not

**It fits** work that is ambiguous at the outset, involves several stakeholders who must agree, and
must be defensible afterwards. In a capital markets context: rebuilding a settlement break
investigation workflow, where the rules for classifying a break are folklore spread across
operations teams and the clarify step is where they finally get written down; changing a trade
surveillance rule set, where the specification and the approval trail are themselves regulatory
artifacts; implementing a client mandates and restrictions engine, where the difficulty is
enumerating precedence rules rather than writing the evaluator; and any change to a regulatory
reporting field, where the specification is the mapping document the regulator will ask to see.

**It does not fit** exploratory work where the point is to learn by building, small well-understood
changes where the ceremony costs more than the change, incident response, or work in a system whose
behaviour nobody can currently describe. It also fits badly where the acceptance criteria are
inherently visual or subjective, since a written specification of a user interface is expensive and
rarely settles the argument.

## 10. Answers to the open questions in my earlier notes

- **What should requirements look like?** Acceptance criteria in EARS form, one testable statement
  per criterion, plus references to machine-checkable contracts for anything with a schema. Explicit
  non-goals. Numbers rather than adjectives for non-functional constraints. No implementation detail
  unless it is a real constraint, and if it is, say why. Keep it to the length a reviewer will
  actually read.
- **Whole project, or per feature?** Per change, scoped to the area being modified. The consistent
  enterprise finding is that whole-system specifications either exceed context limits or exceed
  human review capacity, and the delta model is what works on existing systems. Specification
  density then grows naturally in the areas that change most, which are the areas where it is worth
  having.
- **How should a bug fix flow?** Not through the full ceremony. A bug fix needs a failing test that
  reproduces the defect, a one-paragraph statement of the intended behaviour, and the fix. If the
  bug reveals that an existing specification was wrong, update that specification as part of the
  change. Reserve the full loop for cases where the correct behaviour is genuinely in dispute.
- **On specs being verbose without adding value.** This is the single most common complaint in the
  field and it is a property of the first-generation tooling rather than of the idea. The remedies
  are a length cap, a sizing rule, templates that ask for acceptance criteria rather than narrative,
  and a preference for the lighter tools.

## My notes

- Make infrastructure ready for AI
    - Left shift dev environment
    - dev env needs to be more capable and allow running end to end test
    - Improve CI/CD
        - CI/CD should be fast
    - Code structure
        - More mono repo structure?
- Working team structure
    - Work is done in pair programming fashion with people from different domains e.g. developer,
      product manager, architect.
    - People should not be working individually
- Metric
    - Time taken from ideation to production
    - Compare the cost with previous step
- Flow as originally sketched: specification, then plan, then task list, then code, then review.
  This still holds; the open question was always how heavy each step should be.
- Greenfield: write the use cases, then generate the architecture, using an organisation-specific
  skill that knows the approved technologies and patterns. This is the standing-context idea in
  section 9.1, and it is worth building.

## Resources

### Primary tools and documentation

- [github/spec-kit](https://github.com/github/spec-kit) — the reference open-source toolkit; see also the [documentation site](https://github.github.com/spec-kit/).
- [Spec-driven development with AI: get started with a new open source toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) — GitHub's launch post.
- [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) — delta-spec framework; [concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) and [existing projects](https://github.com/Fission-AI/OpenSpec/blob/main/docs/existing-projects.md) are the two docs worth reading.
- [Kiro](https://kiro.dev/) — AWS's spec-driven IDE; `requirements.md` in EARS, `design.md`, `tasks.md`, plus steering files.
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) — multi-agent persona framework.
- [Tessl](https://tessl.io/) — spec-as-source framework and the [Spec Registry](https://tessl.io/registry) of library specifications; [Spec-Driven Development with Tessl](https://docs.tessl.io/use/spec-driven-development-with-tessl).
- [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows) — AWS AI-DLC steering rules, MIT-0. See [ai-dlc.md](ai-dlc.md).
- [Easy Approach to Requirements Syntax](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax) — EARS, the requirement notation used by Kiro and portable to any tool.
- [cameronsjo/spec-compare](https://github.com/cameronsjo/spec-compare) — interactive side-by-side comparison of the tools with a decision guide.

### Analysis and industry position

- [Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) — Birgitta Böckeler, October 2025. The origin of the spec-first / spec-anchored / spec-as-source framing and still the best single article on the topic.
- [Exploring Generative AI](https://martinfowler.com/articles/exploring-gen-ai.html) — Böckeler's ongoing series, including the mid-2026 state-of-play covering context engineering, harness engineering, costs and security.
- [Spec-driven development](https://www.thoughtworks.com/en-us/radar/techniques/spec-driven-development) — Thoughtworks Technology Radar, Assess, November 2025, with the "bitter lesson" caution.
- [OpenSpec](https://www.thoughtworks.com/en-us/radar/tools/openspec) and [GitHub Spec Kit](https://www.thoughtworks.com/en-de/radar/languages-and-frameworks/github-spec-kit) — Radar entries, Assess, April 2026.
- [What is harness engineering?](https://www.thoughtworks.com/insights/podcasts/technology-podcasts/what-harness-engineering) — the reframing of specs as one control among several.
- [Spec Driven Development: When Architecture Becomes Executable](https://www.infoq.com/articles/spec-driven-development/) — Leigh Griffin and Ray Carroll, InfoQ, January 2026. The five-layer model and a candid account of the costs.
- [Spec-Driven Development: A Spec-First Approach to AI-Native Engineering](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/) — Apoorv Gupta, Microsoft, June 2026.
- [Diving Into Spec-Driven Development With GitHub Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit/) — Microsoft walkthrough.
- [Inside Spec-Driven Development](https://www.epam.com/insights/ai/blogs/inside-spec-driven-development-what-githubspec-kit-makes-possible-for-ai-engineering) and [using Spec Kit for a brownfield codebase](https://www.epam.com/insights/ai/blogs/using-spec-kit-for-brownfield-codebase) — EPAM.
- [Spec-Driven Development for Brownfield Enterprise Codebases](https://www.augmentcode.com/guides/spec-driven-development-brownfield-codebases) — the five brownfield failure modes and mitigations.
- [Spec-Driven Development – Adoption at Enterprise Scale](https://intent-driven.dev/blog/2026/02/19/enterprise-spec-driven-development/) — the specification as cross-functional interface.

### Critical accounts

- [What spec-driven development gets wrong](https://www.augmentcode.com/blog/what-spec-driven-development-gets-wrong) — the drift argument and a bidirectional maintenance proposal.
- [Why Spec-Driven Development Breaks at Scale (And How to Fix It)](http://arcturus-labs.com/blog/2025/10/17/why-spec-driven-development-breaks-at-scale-and-how-to-fix-it/) — Arcturus Labs.
- [Spec-driven development is dead. Long live plan mode](https://instil.co/blog/spec-driven-development-is-dead-long-live-plan-mode) — Matthew Wilson, Instil. Token economics and the Scott Logic ten-times-slower result.
- [Why Spec-Driven Development Fails](https://dev.to/casamia918/why-spec-driven-development-fails-and-what-we-can-learn-from-it-2pec) — the 33-minute / 2,577-line measurement and the REAP alternative.
- [Why Specification-Driven Development is Not a Silver Bullet for AI-Assisted SDLC](https://pub.towardsai.net/why-specification-driven-development-sdd-is-not-a-silver-bullet-for-ai-assisted-sdlc-491c71bcf835) — Alex Punnen, on cognitive load and blind sign-off.
- [The Limits of Spec-Driven Development](https://isoform.ai/blog/the-limits-of-spec-driven-development) — the missing-context argument.
- [Skepticism Toward Specification-Driven Development](https://zenn.dev/cbmrham/articles/202601-spec-driven-development-skepticism?locale=en) — a well-argued practitioner objection.
- [agentic-engineering-field-study: spec-driven development](https://github.com/ianhxu/agentic-engineering-field-study/blob/main/04-spec-driven-development.md) — the most complete synthesis of practitioner reports, positive and negative, with sources.

### Research

- [Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants](https://arxiv.org/abs/2602.00180) — Piskala, January 2026. Survey, taxonomy and pitfalls.
- [Citation Discipline in Spec-Driven Development](https://arxiv.org/abs/2606.30689) — June 2026. Determinism against hallucination detection across traceSDD, Spec Kit and OpenSpec.
- [Protocol-Driven Development: Governing Generated Software Through Invariants and Continuous Evidence](https://arxiv.org/abs/2605.12981) — He and Yu, May 2026. Invariants and runtime evidence as an answer to drift.
- [Understanding Specification-Driven Code Generation with LLMs: An Empirical Study Design](https://arxiv.org/abs/2601.03878) — registered report accepted at SANER 2026; results pending.
- [One Developer Is All You Need: A Case Study of an AI-Augmented One-Person Squad in a Brownfield Enterprise](https://arxiv.org/abs/2605.18461) — May 2026.
- [Towards Specification-Driven LLM-Based Generation of Embedded Automotive Software](https://arxiv.org/abs/2411.13269) — the safety-critical variant.
- [DORA State of AI-assisted Software Development 2025](https://dora.dev/dora-report-2025/) and the [2026 ROI follow-up](https://dora.dev/research/publications/) — AI as amplifier; returns come from the surrounding system.
- [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) — METR; 19% slower while feeling 20% faster.

### Practitioner accounts and case studies

- [Taming Agents in the Mercari Web Monorepo](https://engineering.mercari.com/en/blog/entry/20251030-taming-agents-in-the-mercari-web-monorepo/) and [mercari-pm-agent Design](https://engineering.mercari.com/en/blog/entry/20260427-mercari-pm-agent-design-automating-the-pm-workflow-with-claude-code-skills-and-mcp/) — Mercari's agent spec-driven work, including its use of `AGENTS.md`.
- [Spec Kit + Claude Code: a case study](https://orangeloops.com/2026/05/spec-driven-development-with-ai-a-spec-kit-claude-code-case-study/) — OrangeLoops; two hours of generation for 195 tasks, then four days of stabilisation and review.
- [Spec-Driven Development in Practice: My Experience with spec-kit](https://medium.com/@lookoutking/spec-driven-development-in-practice-my-experience-with-spec-kit-8f250b47d677) — an honest single-project account.
- [How to use a spec-driven approach for coding with AI](https://blog.jetbrains.com/junie/2025/10/how-to-use-a-spec-driven-approach-for-coding-with-ai/) — JetBrains.
- [BMAD vs Spec Kit vs OpenSpec: choosing your spec-driven AI framework](https://reenbit.com/bmad-vs-spec-kit-vs-openspec-choosing-your-spec-driven-ai-framework/) — a straightforward selection guide.

## See also

- [ai-dlc.md](ai-dlc.md) — AWS AI-DLC, the methodology wrapper around spec-driven development.
- [software-dev-with-gen-ai.md](software-dev-with-gen-ai.md) — the wider SDLC picture.
- [working-with-ai.md](working-with-ai.md) — day-to-day working notes and open questions.
- [ai-security.md](ai-security.md) — the security controls this practice assumes.
