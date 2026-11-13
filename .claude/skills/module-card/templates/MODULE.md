---
id: svc.example                      # stable identifier, reused from the service catalog if one exists
name: Example Service
archetypes: [service]                # service | consumer | stream-processor | library | workflow | data-pipeline | ui | cli | batch
owner: team-example                  # from CODEOWNERS or the service catalog
status: proposed                     # proposed | confirmed (overall status of the card)
sections:                            # status per section; never overwrite a confirmed section
  purpose: proposed
  responsibilities: proposed
  capabilities: proposed
  concepts: proposed
  relationships: proposed
  rules: proposed
  external_behaviour: proposed
  non_functional: proposed
  change_guidance: proposed
  traps: proposed
commands:                            # generated
  build: ""
  test: ""
  lint: ""
  run: ""
depends_on: []                       # generated: internal modules and libraries
key_external_dependencies: []        # generated: frameworks that shape the code
provides:                            # generated: contracts other modules rely on
  apis: []
  topics: []
  packages: []                       # libraries only: exported packages or entry modules
consumes:                            # generated
  apis: []
  topics: []
  external: []
data_owned: []                       # generated: tables, schemas, collections
flags: []                            # generated: feature flags and key configuration properties
co_changes_with: []                  # generated: modules frequently changed in the same commits
capabilities: []                     # feature identifiers from the feature registry, if one exists
decisions: []                        # ADR identifiers or links
source_commit: ""
last_generated: ""
---

# Example Service

## Purpose

State in two or three sentences the business reason this module exists and the outcome it
produces.

## Responsibilities

- State each thing this module is responsible for as a full sentence.

### Not responsible for

- State each thing a reader might expect here that belongs elsewhere, and name the module that
  owns it.

## Domain concepts

| Business term | Meaning | Names in code | Also called |
|---|---|---|---|
| | | | |

## Relationships

| Module | Relationship | Reason |
|---|---|---|
| | calls / is called by / consumes from / publishes to / depends on | |

## Business rules and invariants

- **RULE-ID:** State the rule in business terms. Checked by: name the test suite. (proposed)

## Behaviour defined outside the code

- Describe any rules, reference data, workflow models or schemas held outside the repository,
  and say where they live.

## Non-functional expectations

- State cut-off times, latency or throughput expectations, batch windows, data classification
  and regulatory drivers, where documented.

## How to change it safely

- State the conventions to follow and name the type or class to use as an example.
- State the deprecated approaches to avoid and what replaces them.
- State the tests that must pass before a change is merged.

## Known traps

- Describe surprising behaviour, ordering assumptions, shared state or past incidents.

## Open questions

- Ask a specific question for the owner about anything that could not be established.
