# Feature Registry and Drift Detection for Agent-Generated Code

Design note, November 2026. Related notes: [code-intelligence-tools.md](code-intelligence-tools.md),
[knowledge-graphs-for-coding-agents.md](knowledge-graphs-for-coding-agents.md),
[coding-agents-in-large-codebases.md](coding-agents-in-large-codebases.md),
[agent-ready-content-formats.md](agent-ready-content-formats.md),
[context-engineering.md](context-engineering.md).

## Contents

- [1. Summary](#1-summary)
- [2. Why map features to code](#2-why-map-features-to-code)
  - [2.1 The problem the registry solves](#21-the-problem-the-registry-solves)
  - [2.2 Why full code paths should not be recorded](#22-why-full-code-paths-should-not-be-recorded)
- [3. What the registry stores](#3-what-the-registry-stores)
  - [3.1 Fields and their sources](#31-fields-and-their-sources)
  - [3.2 Example entry](#32-example-entry)
  - [3.3 Footprints from runtime traces](#33-footprints-from-runtime-traces)
- [4. Direction of authority](#4-direction-of-authority)
- [5. Drift detection mechanisms](#5-drift-detection-mechanisms)
  - [5.1 Regenerate and diff](#51-regenerate-and-diff)
  - [5.2 Reference validation](#52-reference-validation)
  - [5.3 Contract conformance](#53-contract-conformance)
  - [5.4 Executable acceptance criteria](#54-executable-acceptance-criteria)
  - [5.5 Footprint fingerprints](#55-footprint-fingerprints)
  - [5.6 Semantic review by a language model](#56-semantic-review-by-a-language-model)
  - [5.7 Scheduled sweep](#57-scheduled-sweep)
  - [5.8 Side-by-side comparison](#58-side-by-side-comparison)
- [6. Fitting drift control into the agent workflow](#6-fitting-drift-control-into-the-agent-workflow)
- [7. Rollout](#7-rollout)
- [8. Generation instructions for any codebase](#8-generation-instructions-for-any-codebase)
  - [8.1 How the instructions handle stack and size](#81-how-the-instructions-handle-stack-and-size)
  - [8.2 The skill file](#82-the-skill-file)
  - [8.3 Usage notes](#83-usage-notes)
- [9. Limitations](#9-limitations)
- [Resources](#resources)

## 1. Summary

- A feature registry maps each business feature of an application to its entry points, core symbols, cross-boundary dependencies, tests and owners.
  - Its main value is translating business vocabulary into code names, which neither grep nor a call graph can do without a starting point.
  - It records only starting points and the edges that static analysis cannot see, and it leaves the full call path for tools to derive at query time.
- Drift control depends first on deciding the direction of authority for each artifact.
  - Artifacts upstream of the code, such as specifications and API contracts, should block the build when the code disagrees with them.
  - Artifacts downstream of the code, such as the registry footprint, module cards and diagrams, should be regenerated rather than edited.
  - Human-only knowledge, such as invariants and decision rationale, cannot be derived and should be flagged for review when the code beneath it changes.
- Bidirectional synchronisation should be avoided, because rewriting a specification to match the code converts a bug into documentation.
- The recommended starting set of checks is regenerate-and-diff, reference validation and footprint fingerprints, because they are deterministic and cheap.
  - Executable acceptance criteria should be added for high-risk features, and an advisory language-model review should be added last.
- The checks should run inside the coding agent's loop through hooks as well as in CI, so the agent repairs drift before a human reviews the pull request.

## 2. Why map features to code

### 2.1 The problem the registry solves

- The hardest step for an agent in a large codebase is turning a business term into the right code.
  - A ticket may say "partial settlement of a failed trade" while the code uses names such as `BreakResolver`, `SettlementInstructionSplitter` and a topic called `stl.part.v2`.
  - Lexical search cannot connect these names, and a call graph cannot help until the agent knows where to start.
- A registry supplies exactly this missing fact, which the agent cannot discover cheaply on its own.
- The same footprints support other uses, such as working out which features a pull request touches, choosing reviewers and selecting tests to run.

### 2.2 Why full code paths should not be recorded

- A hand-written path such as controller, service, repository, topic and consumer becomes wrong after the next refactor, and nothing reports the error.
  - Generated prose without a drift check has failed this way in practice, as the DeepWiki reports in [knowledge-graphs-for-coding-agents.md](knowledge-graphs-for-coding-agents.md) describe.
- The intermediate steps can already be derived by a symbol index such as [SCIP](https://github.com/sourcegraph/scip), a language server or grep once the starting point is known.
- Duplicating derivable paths adds near-duplicate text to the agent's context, and similar distractors are known to lower accuracy.
- Real paths branch through feature flags, configuration, dependency injection, asynchronous messaging and calls to other services, so a single clean path hides the branches where defects usually occur.
- Evaluation of context files found that generated codebase overviews added cost without helping agents reach the right files ([Gloaguen et al.](https://arxiv.org/html/2602.11988v3)), which argues for storing facts rather than descriptions.

## 3. What the registry stores

### 3.1 Fields and their sources

| Field | Content | Source | Provenance |
|---|---|---|---|
| `id` | A stable identifier such as `feat.settlement.partial` | Assigned once and reused | Generated, then fixed |
| `name`, `summary` | The business name and a one-sentence description | Inferred from code, UI and documents | Proposed until a person confirms |
| `aliases` | Business terms that differ from code names | UI text, documents, tickets, commit messages | Proposed until confirmed |
| `entry_points` | Routes, topics, jobs, commands and screens | Deterministic extraction | Generated |
| `key_symbols` | The domain-core symbols reached within two or three hops | Shallow tracing from entry points | Generated |
| `crosses` | Other services, topics, tables, external APIs and feature flags | Extraction and tracing | Generated where possible |
| `tests` | Integration and acceptance tests that exercise the feature | Test names, coverage or traces | Generated |
| `owner` | The owning team | CODEOWNERS, overridable by a person | Generated or human |
| `invariants` | Rules the code relies on but does not show | Written by a person | Human only |
| `source_commit`, `footprint_hash` | The commit and content hash the entry was built from | Generator | Generated |

- The registry stores one YAML file per feature, which keeps diffs small and lets CODEOWNERS assign review per feature ([GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)).
- Generated fields must never be edited by hand, and human fields must never be overwritten by the generator.

### 3.2 Example entry

```yaml
id: feat.settlement.partial
name: Partial settlement of failed trades
status: confirmed
summary: Splits a failed settlement instruction into deliverable parts.
aliases: ["partial settle", "split settlement", "break resolution"]
entry_points:
  - {kind: http, id: "POST /api/v2/settlements/{id}/partial", handler: PartialSettlementController#create, unit: settlement-engine}
  - {kind: kafka-consumer, id: stl.part.v2, handler: PartialSettlementListener#onMessage, unit: settlement-engine}
  - {kind: job, id: EodBreakSweepJob, handler: EodBreakSweepJob#run, unit: settlement-engine}
key_symbols: [SettlementInstructionSplitter#split, BreakResolver#resolve]
crosses:
  services: [ref-data]
  topics: {consumes: [stl.part.v2], produces: [stl.instructed.v1]}
  tables: [SETTLEMENT_INSTR]
  flags: [settlement.partial.enabled]
tests: [PartialSettlementIT, golden/partial_*.json]
owner: team-post-trade
invariants:
  - "A partial instruction must never exceed the original quantity in aggregate."
provenance:
  generated: [entry_points, key_symbols, crosses, tests, owner]
  inferred: [aliases]
  human: [name, summary, invariants]
source_commit: 9f3c2ab
footprint_hash: sha256:...
```

### 3.3 Footprints from runtime traces

- The most reliable way to find a feature's real footprint is to run its integration tests with tracing or per-test coverage enabled and record the symbols that executed.
  - [OpenTelemetry](https://opentelemetry.io/docs/) spans capture calls across services and messaging, and per-test coverage captures the in-process symbols.
  - This approach captures branches taken through flags and configuration, which static extraction misses.
- The limitation is that traces only cover paths the tests exercise, so a feature with weak tests will have an incomplete footprint.

## 4. Direction of authority

- In spec-driven development the flow runs from specification to agent to code to other artifacts, and each artifact either sits upstream of the code or downstream of it.
- The direction of authority decides what drift means and what the correct response is.

| Artifact | Authority | Meaning of drift | Response |
|---|---|---|---|
| Feature specification and acceptance criteria | Upstream | The code is wrong, or the specification changed without the code | Block the build |
| API contracts, Avro and Protobuf schemas | Upstream, generated into code | The code does not conform to the contract | Block the build |
| Registry entry points and footprint | Downstream | The registry is stale | Regenerate |
| Module cards, dependency lists and commands | Downstream | The card is stale | Regenerate |
| Diagrams and dependency graphs | Downstream | The diagram is stale | Regenerate |
| Invariants, aliases, ADRs and rationale | Human, not derivable | Unknown until a person judges it | Flag for review |

- Bidirectional synchronisation tools should be avoided for upstream artifacts.
  - When code and specification disagree, the code is usually the thing that is wrong, so rewriting the specification from the code records the defect as intended behaviour.
- Upstream artifacts should only ever block, and downstream artifacts should only ever be regenerated.

## 5. Drift detection mechanisms

### 5.1 Regenerate and diff

- What it is:
  - CI rebuilds every generated artifact and fails if the committed version differs, for example by running the generator and then `git diff --exit-code`.
- What it covers:
  - It covers registry entry points and footprints, module card fields, OpenAPI documents generated from code, and diagrams.
- Benefit:
  - Drift in generated artifacts cannot reach the main branch, and the check needs no judgement.
- Limitation:
  - It only works for content that can be derived deterministically, and generated blocks must be clearly marked so people and agents do not edit them.

### 5.2 Reference validation

- What it is:
  - CI checks that every symbol, path, route, topic, table, flag and test named in any artifact still exists in the current commit.
- How:
  - Lookups run against a symbol index such as [SCIP](https://github.com/sourcegraph/scip), structural search with [ast-grep](https://ast-grep.github.io/), or plain grep for non-code identifiers.
- Benefit:
  - It is cheap, produces no false positives, and catches renames and deletions, which account for most practical drift.
- Limitation:
  - It proves that references exist but not that the surrounding text is still true.

### 5.3 Contract conformance

- What it is:
  - Tooling compares code and published contracts and fails on incompatible changes.
- Tools:
  - [oasdiff](https://github.com/oasdiff/oasdiff) and [Spectral](https://github.com/stoplightio/spectral) check OpenAPI documents.
  - [buf breaking](https://buf.build/docs/breaking/) checks Protobuf compatibility.
  - Schema registry compatibility rules check Avro evolution ([Confluent schema evolution](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html)).
  - [Pact](https://docs.pact.io/) checks consumer-driven contracts between services.
  - [ArchUnit](https://www.archunit.org/) checks architectural rules such as allowed dependencies between layers.
- Benefit:
  - Contract drift is caught at the boundary where it does the most damage to other teams.
- Limitation:
  - It only covers what the contract expresses, and generating code from the contract removes much of the need for comparison.

### 5.4 Executable acceptance criteria

- What it is:
  - The testable parts of each specification are written as examples, such as [Gherkin](https://cucumber.io/docs/gherkin/) scenarios or input and output tables, and each example becomes a test.
- Benefit:
  - It is the only mechanism that checks behaviour rather than names, so drift between specification and code appears as a failing test.
- Limitation:
  - Writing and maintaining examples costs effort, and it only covers behaviour that someone thought to express as an example.
- Capital markets example:
  - A mandate rules engine can express each restriction type as a table of client, instrument and expected decision, so a change that allows a restricted issuer fails immediately.

### 5.5 Footprint fingerprints

- What it is:
  - Each human-written artifact stores a hash of the files or symbols it describes, together with the commit at which it was last reviewed.
  - When a pull request changes those files, CI requires that the artifact is updated in the same pull request or that a commit trailer acknowledges the review, such as `Spec-Reviewed: feat.settlement.partial (no behaviour change)`.
- How:
  - The registry supplies the mapping from changed files to affected features, and a pull request bot such as [Danger](https://danger.systems/js/) or a custom CI step enforces the rule.
- Benefit:
  - It guarantees that a person looks at human knowledge whenever the code beneath it changes.
- Limitation:
  - It does not prove the text is correct, and it can create review fatigue if footprints are too broad.

### 5.6 Semantic review by a language model

- What it is:
  - A reviewer agent reads the diff alongside the relevant specification sections and reports contradictions.
- Example:
  - The reviewer might report that the specification rejects partial fills below 1,000 shares while the change accepts them.
- Benefit:
  - It catches meaning-level drift that the deterministic checks cannot see.
- Limitation:
  - It produces false positives and misses, so it should post an advisory comment and never block a merge.

### 5.7 Scheduled sweep

- What it is:
  - A nightly job audits the whole codebase rather than a single pull request.
- What it finds:
  - It finds stale fingerprints, specifications not reviewed within a set period, orphaned features, and code paths observed in test or production traces that no registry entry covers.
- Benefit:
  - It detects new unmapped code, which pull request checks cannot see because nothing references it.
- Limitation:
  - Its findings arrive after merge, so someone must own the resulting backlog.

### 5.8 Side-by-side comparison

| Mechanism | Artifacts covered | Deterministic | Blocking | Cost to run | Main limitation |
|---|---|---|---|---|---|
| Regenerate and diff | Downstream | Yes | Yes | Low | Derivable content only |
| Reference validation | All | Yes | Yes | Low | Existence, not truth |
| Contract conformance | Upstream contracts | Yes | Yes | Low to medium | Only what the contract expresses |
| Executable acceptance criteria | Specifications | Yes | Yes | Medium to high | Only behaviour written as examples |
| Footprint fingerprints | Human knowledge | Yes | Yes | Low | Forces review, does not verify content |
| Language-model review | Specifications and human knowledge | No | No | Medium | False positives and misses |
| Scheduled sweep | All, including unmapped code | Mostly | No | Low | Findings arrive after merge |

## 6. Fitting drift control into the agent workflow

- The agent should edit the specification before the code, and both changes should be in the same pull request so reviewers see the change in intent next to the change in implementation.
  - A skill can encode this ordering as a procedure ([Claude Code skills](https://code.claude.com/docs/en/skills)).
- The deterministic checks should run inside the agent's session through a pre-commit hook or a Stop hook ([Claude Code hooks](https://code.claude.com/docs/en/hooks)).
  - The agent then sees the failure and repairs the artifact before a person reviews the pull request.
  - An instruction such as "keep the docs in sync" in AGENTS.md is advisory, whereas a hook and a CI gate are enforced.
- The agent may regenerate downstream artifacts but must not edit generated blocks by hand.
- The agent may propose changes to upstream specifications and human fields, and a person approves them through review and CODEOWNERS.

## 7. Rollout

| Phase | Scope | Exit criterion |
|---|---|---|
| 1 | Generate the registry for the 10 to 20 features with the most change or the most incidents, chosen from git history and incident records | A person has confirmed names, aliases and grouping |
| 2 | Add regenerate-and-diff, reference validation and footprint fingerprints as hooks and blocking CI checks | Checks block in CI with an acceptable false-failure rate |
| 3 | Add executable acceptance criteria for high-risk features such as settlement and mandate checks | Each high-risk feature has example-based tests linked from its specification |
| 4 | Add advisory language-model review and the nightly sweep | The false-positive rate of the review is measured and acceptable |
| 5 | Evaluate the registry by giving an agent recent tasks with and without it | The registry is kept only if it improves file localisation or task success |

## 8. Generation instructions for any codebase

### 8.1 How the instructions handle stack and size

- Stack independence comes from detecting the stack first and then applying a table of entry-point conventions per framework.
  - Framework route listings and OpenAPI files are preferred over pattern matching when they can run offline.
- Size independence comes from choosing a strategy after measuring the codebase.
  - A small codebase is processed in a single pass.
  - A medium codebase is inventoried as a whole and described per module.
  - A large or multi-repository estate is partitioned by deployable unit, processed in parallel, and then merged.
- The inventory of entry points must be exhaustive and come from search, while judgement is limited to grouping and naming.

### 8.2 The skill file

- The instructions below are written as a Claude Code skill, placed at `.claude/skills/feature-registry/SKILL.md` in the target codebase, and they work equally as a prompt for other agents.

````markdown
---
name: feature-registry
description: Generate or refresh a feature registry that maps each business feature of this codebase to its entry points, key symbols, cross-boundary dependencies, tests and owners. Use when asked to build, update or validate the feature registry.
---

# Feature registry generation

## Goal

Produce a registry that lets a coding agent go from a business term ("partial settlement",
"client onboarding") to the code that implements it. The registry records the starting points
and the edges that static analysis cannot see. It does not record full call paths, because tools
derive those at query time and a written path goes stale.

## Ground rules

- Extract facts from the code with deterministic tools (grep, ast-grep, framework route dumps,
  build files, OpenAPI specs) wherever possible. Use your own judgement only for grouping entry
  points into features and for proposing names and aliases.
- Never invent a symbol, path, route, topic, table or test. Every reference you write must be
  verified to exist before you finish.
- Do not write prose overviews of the architecture, and do not paste code into the registry.
- Exclude generated, vendored, build-output and third-party code from every footprint.
- Do not record secrets, credentials, hostnames of production systems or personal data.
- When something is ambiguous, add it to the open-questions list instead of guessing.
- Mark every field with its provenance: `generated` (extracted by a tool), `inferred` (your
  judgement), or `human` (written or confirmed by a person). Never overwrite a `human` field.

## Phase 0: Assess size and choose a strategy

1. Count source files and lines per language, excluding generated and vendored directories.
   Identify deployable units (services, apps, jobs, libraries) from build files
   (pom.xml, build.gradle, package.json, pyproject.toml, *.csproj, go.mod, Cargo.toml,
   Gemfile, Makefile, JCL libraries, Dockerfiles, Helm charts, serverless templates).
2. Choose a strategy:
   - **Small** (under ~50k lines and one deployable unit): run all phases in a single pass.
   - **Medium** (one repository with several modules): run Phase 1 and 2 across the whole
     repository, then Phase 3 to 5 per module, then a merge pass.
   - **Large** (multi-repository or over ~1M lines): partition by deployable unit. Run Phase 1
     to 5 for each partition independently (in parallel sub-agents where available), each
     writing to its own partition output. Then run the merge pass in Phase 6.
3. Record the chosen strategy, the partitions and the excluded directories in the report.

## Phase 1: Detect the stack and its entry-point conventions

For each deployable unit, identify the languages and frameworks, then search for every kind of
entry point below that applies. Prefer a framework's own route listing when it can run offline
(for example `rails routes`, `python manage.py show_urls`, an OpenAPI file, Spring
`@RequestMapping` scans) over pattern matching.

| Entry-point kind | Examples of what to search for |
|---|---|
| HTTP and RPC | Spring `@RestController`/`@*Mapping`; JAX-RS `@Path`; ASP.NET controllers and minimal-API `Map*`; Express/Fastify/Nest routes; FastAPI/Flask/Django URL patterns; Rails `routes.rb`; Go `http.HandleFunc`, gin/echo/chi routers; gRPC service implementations; GraphQL resolvers |
| Messaging | `@KafkaListener`, `@RabbitListener`, `@JmsListener`, SQS/SNS/EventBridge handlers, Celery/RQ/Sidekiq/Hangfire workers, MassTransit consumers, topic producers |
| Scheduled and batch | `@Scheduled`, Quartz, cron files, Kubernetes CronJobs, Airflow DAGs, Spring Batch jobs, JCL jobs, Control-M or Autosys definitions |
| User interface | React Router/Next.js/Nuxt/Angular routes, page components, menu definitions, mobile screens and deep links |
| Command line | CLI command registrations (picocli, click, typer, cobra, commander), management commands, rake tasks |
| Serverless | Handlers declared in serverless.yml, SAM/CloudFormation, Azure Functions, Cloud Functions |
| Mainframe and database | CICS transactions, IMS transactions, batch COBOL programs called from JCL, stored procedures and triggers called by applications |
| Webhooks and integrations | Inbound webhook endpoints, file drops and SFTP pollers, FIX sessions and message handlers |

Write the complete list to `features/_inventory.json`. Each record holds the kind, the
identifier (route, topic, job name, command), the handler symbol, the file and line, and the
deployable unit. The inventory must be exhaustive and must come from search, not sampling.

## Phase 2: Collect grouping signals

Gather evidence that helps group entry points into features:

- URL prefixes, OpenAPI tags, GraphQL types and gRPC service names.
- Package, namespace and module names, and the domain types each handler uses.
- Database tables and message topics shared by several entry points.
- Files that change together in git history (`git log --name-only` over the last 12 months).
- UI menus, page titles, test class and test case names, README sections, ADRs, and
  ticket keys or epic names found in commit messages.
- Owners from CODEOWNERS, and the most frequent recent committers per directory.

## Phase 3: Group entry points into features

A feature is a capability that a user, an operator or another system would recognise and could
describe in one sentence of business language. Apply these rules:

- A feature usually has between 2 and 15 entry points. One feature per endpoint is too fine,
  and one feature per service is too coarse.
- A feature may span several deployable units. Keep it as one feature with entry points in
  each unit.
- Put cross-cutting infrastructure (authentication, logging, health checks, metrics) in a
  single `platform` group and do not treat each piece as a business feature.
- Every entry point must belong to exactly one feature or appear in the `unassigned` list
  with a reason.
- Give each feature a stable identifier `feat.<domain>.<capability>` in lowercase with dots.
  Reuse an existing identifier from the registry when refreshing.

## Phase 4: Describe each feature

For each feature, fill in the schema below.

- **Key symbols:** follow calls from each entry point for at most two or three hops, until you
  reach the domain core (the service, aggregate or rule engine that does the work). Record only
  those core symbols, not every hop.
- **Crosses:** list the boundaries the feature touches that a call graph cannot show:
  calls to other services, message topics produced and consumed, database tables and stored
  procedures, external APIs, files, and feature flags or configuration keys that change its
  behaviour.
- **Tests:** list the tests that exercise the feature, preferring integration and acceptance
  tests over unit tests.
- **Aliases:** collect the business terms used for the feature in UI text, docs, tickets and
  commit messages, especially terms that differ from the names in the code.
- **Name, summary and aliases** are `inferred` with `status: proposed` until a person confirms them.

## Phase 5: Validate

Before writing output, run these checks and fix or report every failure:

1. Every symbol, file, route, topic, table, flag and test referenced exists in the current
   commit.
2. Every inventory entry point is assigned to one feature or listed as unassigned.
3. No feature identifier is duplicated, and no footprint includes excluded directories.
4. Every `human` field from the previous registry is preserved unchanged.

## Phase 6: Merge (medium and large strategies only)

Combine partition outputs into one registry. Merge features from different partitions that
share a topic, table, API contract or business alias into a single feature. Resolve identifier
conflicts in favour of the identifier already in the registry. Re-run Phase 5 on the merged
result.

## Output

Write these files:

- `features/<feature-id>.yaml`, one file per feature, using the schema below.
- `features/_inventory.json`, the full entry-point inventory from Phase 1.
- `features/_report.md`, containing the strategy and partitions, counts of entry points,
  features and unassigned entry points, validation results, the list of `proposed` fields
  that need a person to confirm them, and open questions.

Schema:

```yaml
id: feat.settlement.partial                 # stable identifier
name: Partial settlement of failed trades   # inferred until confirmed
status: proposed                            # proposed | confirmed | orphaned
summary: Splits a failed settlement instruction into deliverable parts.   # one sentence
aliases: [partial settle, split settlement] # business vocabulary
entry_points:                               # generated
  - {kind: http, id: "POST /api/v2/settlements/{id}/partial", handler: PartialSettlementController#create, unit: settlement-engine}
  - {kind: kafka-consumer, id: stl.part.v2, handler: PartialSettlementListener#onMessage, unit: settlement-engine}
key_symbols: [SettlementInstructionSplitter#split, BreakResolver#resolve]   # generated
crosses:                                    # generated where possible
  services: [ref-data]
  topics: {consumes: [stl.part.v2], produces: [stl.instructed.v1]}
  tables: [SETTLEMENT_INSTR]
  flags: [settlement.partial.enabled]
tests: [PartialSettlementIT]                # generated
owner: team-post-trade                      # from CODEOWNERS, human may override
invariants: []                              # human only; never generate
provenance:
  generated: [entry_points, key_symbols, crosses, tests]
  inferred: [name, summary, aliases]
  human: [invariants]
source_commit: 9f3c2ab
footprint_hash: sha256:...                  # hash of the files containing entry points and key symbols
```

## Refresh mode

When `features/` already exists, do not start from scratch. Rebuild the inventory, compare it
with the previous `_inventory.json`, and update only the features whose entry points, key
symbols or footprint hash changed. Add new entry points to an existing feature when the grouping
signals clearly support it, otherwise propose a new feature. Never delete a feature that has
`human` fields. Mark it `status: orphaned` and list it in the report instead.
````

### 8.3 Usage notes

- The Phase 1 search patterns should be turned into a committed extraction script per stack after the first run.
  - Later refreshes and the CI drift checks then use the same deterministic extraction instead of the model's judgement.
- On an unfamiliar codebase, the agent should stop after Phase 3 and present the proposed feature groups for review.
  - Correcting the grouping at that point is much cheaper than correcting dozens of finished feature files.
- The merge pass on a large estate needs the closest human review, because features that span services are where grouping errors concentrate.
- Mainframe estates and applications that rely heavily on dependency injection or reflection will produce more unassigned entry points and weaker key symbols.
  - Output from a mainframe analyser, as described in [code-intelligence-tools.md](code-intelligence-tools.md), can supply the missing call relationships for COBOL and JCL.

## 9. Limitations

- None of these mechanisms proves that a specification is correct.
  - They prove that the specification, the code and the artifacts agree, and that a person reviewed the artifacts when they stopped agreeing.
- Feature grouping is a judgement, so two runs of the generator can propose different groupings until a person confirms them and the identifiers become fixed.
- Footprints derived from traces are only as complete as the tests that produce the traces.
- Fingerprint checks can create review fatigue if footprints are drawn too broadly, so footprints should be limited to entry points and key symbols rather than every file a feature touches.
- No public evaluation measures the effect of a feature registry on agent performance, so an organisation should measure it on its own tasks before investing in full coverage.

## Resources

- [SCIP code intelligence protocol](https://github.com/sourcegraph/scip) — precise symbol indexes used for reference validation.
- [ast-grep](https://ast-grep.github.io/) — structural search for entry-point extraction.
- [OpenTelemetry documentation](https://opentelemetry.io/docs/) — tracing for runtime footprints.
- [oasdiff](https://github.com/oasdiff/oasdiff), [Spectral](https://github.com/stoplightio/spectral), [buf breaking](https://buf.build/docs/breaking/), [Pact](https://docs.pact.io/) and [ArchUnit](https://www.archunit.org/) — contract and architecture conformance.
- [Gherkin reference](https://cucumber.io/docs/gherkin/) — a format for executable acceptance criteria.
- [Danger](https://danger.systems/js/) — pull request rules such as footprint fingerprint enforcement.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) and [Claude Code skills](https://code.claude.com/docs/en/skills) — running checks and procedures inside the agent loop.
- [Gloaguen et al.](https://arxiv.org/html/2602.11988v3) — evaluation of context files for coding agents.

### Related notes

- [code-intelligence-tools.md](code-intelligence-tools.md) — tools that build the indexes these checks rely on.
- [knowledge-graphs-for-coding-agents.md](knowledge-graphs-for-coding-agents.md) — channels and stores for delivering codebase knowledge to agents.
- [coding-agents-in-large-codebases.md](coding-agents-in-large-codebases.md) — evidence on running coding agents across large estates.
- [agent-ready-content-formats.md](agent-ready-content-formats.md) — formats and validation for engineering documents read by agents.
- [context-engineering.md](context-engineering.md) — techniques for keeping agent context small and accurate.
