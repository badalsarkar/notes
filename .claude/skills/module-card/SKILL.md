---
name: module-card
description: Generate, refresh or validate a module card (MODULE.md) that describes what a module is for, the business capabilities it realises, the domain concepts it owns, its contracts, dependencies, invariants and how to change it safely. Use when asked to create, update, review or check module cards for one module or a whole codebase.
---

# Module card generation

## Goal

A module card tells a person or a coding agent what a module is for and how it relates to the
rest of the system, at a level the code alone does not show. It answers these questions:

- Why does this module exist, and which business capabilities does it realise?
- Which domain concepts does it own, and what are they called in the code?
- What does it promise to other modules, and what does it rely on from them?
- Which rules must always hold, and where are the traps?
- How do I build, test and change it safely?

A card is not an index of the code. It contains no file paths below the module root, no line
numbers and no code excerpts, because tools can find those at query time and they go stale.
It refers to code only through stable names: the module identifier, contract names, domain
type names, topic and table names, and test suite names.

## Ground rules

- Extract facts with deterministic tools wherever possible: build files, API and schema files,
  CODEOWNERS, configuration and git history. Use judgement only for purpose, responsibilities,
  concepts and relationships, and mark those as proposed until a person confirms them.
- Never invent a name, contract, dependency, topic, table, rule or ticket. Every name you write
  must exist in the repository or in a document you read.
- Never overwrite a section or field that a person has confirmed. Propose a change in the
  report instead.
- Write every statement as a plain, full sentence. Do not write marketing language or general
  descriptions that would be true of any module, such as "handles business logic".
- Keep the card short. A card longer than about 150 lines is a sign that the module is too
  large or that the card contains detail the code index should hold.
- Do not record secrets, credentials, production hostnames or personal data.
- When you cannot determine something, write a specific question for a person rather than a
  guess.

## Step 1: Identify modules

1. Find deployable units and modules from build files (pom.xml, build.gradle, settings.gradle,
   package.json workspaces, pyproject.toml, *.csproj and *.sln, go.mod, Cargo.toml workspaces,
   Nx or Bazel targets, Helm charts, JCL libraries).
2. Choose the card granularity. A card describes a unit that has its own purpose and owner,
   usually a deployable service, a library, or a bounded context inside a modular monolith.
   Do not create cards for small technical packages such as `utils` or `config`; mention them
   in the parent module's card instead.
3. Give each module a stable identifier such as `svc.settlement-engine`, `lib.money` or
   `job.eod-sweep`. Reuse identifiers from the service catalog or existing cards if they exist.
4. Classify the module's archetype: `service`, `consumer`, `stream-processor`, `library`,
   `workflow`, `data-pipeline`, `ui`, `cli` or `batch`. A module may have more than one.
5. For more than about ten modules, process them one at a time or in parallel sub-agents, and
   then run a consistency pass across all cards (Step 6).

## Step 2: Extract facts

Collect these with tools, and mark them as `generated`:

- **Build and run:** the commands to build, test, lint and run the module locally, taken from
  build files, Makefiles, package scripts, CI configuration and README files. Run a command only
  if it is safe and fast; otherwise record it without running it.
- **Dependencies on other modules:** internal modules and libraries from the build files.
- **Notable external dependencies:** frameworks and libraries that shape how code is written,
  such as the web framework, messaging client, ORM and rules engine. Omit utility libraries.
- **Contracts provided:** OpenAPI, AsyncAPI, Protobuf, Avro or GraphQL definitions, exported
  library packages, CLI commands, and topics produced.
- **Contracts consumed:** clients for other services, topics consumed, shared databases,
  external APIs and file feeds.
- **Data owned:** tables, schemas, collections and caches that this module writes, from
  migrations and ORM mappings.
- **Configuration that changes behaviour:** feature flags and key configuration properties.
- **Ownership:** owners from CODEOWNERS or the service catalog.
- **Change activity:** the modules this one most often changes together with, from git
  history over the last 12 months. Use it to find hidden coupling.

## Step 3: Gather context for the semantic sections

Read, in this order, whatever exists: the module README, ADRs, design documents, the service
catalog entry, API descriptions, test names and test descriptions, UI text, recent ticket keys
and titles in commit messages, and review comments that recur in merged pull requests. Read the
core domain types and the main entry points to understand what the module does. Do not read the
whole module line by line.

## Step 4: Draft the card

Fill in the template in `templates/MODULE.md` in this skill's directory. For each semantic
section:

- **Purpose:** two or three sentences on the business reason the module exists and the outcome
  it produces. Name the business capability, not the technology.
- **Responsibilities and non-responsibilities:** what the module does, and what a reader might
  expect it to do but which belongs elsewhere, with the module that owns it. The
  non-responsibilities prevent agents from adding logic in the wrong place.
- **Capabilities realised:** the business features this module implements in whole or in part,
  using feature identifiers from a feature registry if one exists.
- **Domain concepts:** each business term the module owns or uses heavily, with its definition
  and its names in the code (types, tables, topics). Include synonyms used by the business.
- **Relationships:** for each important neighbouring module, the nature of the relationship and
  the reason for it, for example "calls ref-data to resolve standing settlement instructions
  because SSIs are owned there".
- **Business rules and invariants:** rules that must always hold, stated in business terms, each
  with an identifier if the organisation has one and the test suite that checks it if known.
  Propose candidates from code and tests, but mark every rule as proposed, because only a
  person can confirm that a rule is intended rather than accidental.
- **Behaviour defined outside the code:** rules or reference data loaded from a database,
  deployed workflow models, or schemas in a registry.
- **Non-functional expectations:** cut-off times, latency or throughput expectations, batch
  windows, data classification and regulatory drivers, when documented.
- **How to change it safely:** the conventions to follow, the patterns to copy (name the
  type or class to use as an example), deprecated approaches to avoid, and the tests that must
  pass.
- **Known traps:** surprising behaviour, ordering assumptions, shared state and past incidents.
- **Decisions:** ADRs and design documents that explain why the module is shaped as it is.
- **Open questions:** specific questions for the owner about anything you could not establish.

Mark every proposed item with `(proposed)` at the end of the line, and record the status of
each section in the frontmatter.

## Step 5: Validate

Run the validator in this skill's directory, replacing `<skill-dir>` with that directory:

    python3 <skill-dir>/scripts/validate_module_card.py <path-to-MODULE.md> --root <repo-root>

If Python is not available, perform the same checks by hand:

1. The frontmatter contains every required field and the identifier is unique.
2. Every module, contract, type, topic, table, flag and test suite named in the card can be
   found in the repository.
3. No file path below the module root, line number or code excerpt appears in the card.
4. Every confirmed section from the previous version is unchanged.
5. The card is under about 150 lines.

The validator covers checks 1 (except uniqueness), 2 (for names in the frontmatter), 3 and 5.
Perform the remaining checks yourself. Fix every failure or report it.

## Step 6: Consistency pass across modules

When several cards exist, check that relationships agree in both directions, that each domain
concept has one owning module, that no two modules claim the same responsibility, and that
every non-responsibility names a module that does take it on. Report conflicts rather than
resolving them silently.

## Output

- Write the card to `MODULE.md` in the module's root directory, unless the repository already
  keeps cards elsewhere (for example `docs/modules/<id>.md`), in which case follow that
  convention.
- Produce a short report in the conversation: modules processed, sections still proposed,
  validation results, cross-module conflicts, and the open questions grouped by owner.
- Do not commit. Leave the changes for review.

## Refresh mode

When a card already exists, re-extract the generated facts, update them, and compare
`source_commit` with the current commit. For semantic sections, check whether the code changes
since `source_commit` affect them. If they do, propose changes in the report and add open
questions instead of editing confirmed text. Update `source_commit` and `last_generated` only
for the generated sections you refreshed.
