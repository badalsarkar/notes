# CALM: Architecture as Code

Research report, November 2026. Related notes: [software-architecture.md](software-architecture.md),
[system-design.md](system-design.md), [cloud-architecture.md](cloud-architecture.md),
[devops.md](devops.md), [ai-security.md](ai-security.md).

## Contents

- [1. What CALM is](#1-what-calm-is)
- [2. The problem it solves](#2-the-problem-it-solves)
- [3. Core model](#3-core-model)
- [4. Patterns and validation](#4-patterns-and-validation)
- [5. Tooling](#5-tooling)
- [6. Spec versions](#6-spec-versions)
- [7. Capital markets example](#7-capital-markets-example)
- [8. Comparison with other architecture-as-code approaches](#8-comparison-with-other-architecture-as-code-approaches)
- [9. Limitations](#9-limitations)
- [Resources](#resources)

## 1. What CALM is

- CALM stands for Common Architecture Language Model, and it is an open-source specification for describing software architecture as JSON that is machine-readable, version-controlled and validated with JSON Schema ([what is CALM](https://calm.finos.org/introduction/what-is-calm)).
  - The model has three basic parts: nodes, relationships and metadata, and it is built on a JSON meta schema.
  - A CALM document is a plain JSON file that validates against the published schema ([finos/calm-schema](https://github.com/finos/calm-schema)).
- Morgan Stanley created CALM and contributed it to FINOS, the Fintech Open Source Foundation, in December 2024 ([finos/community#455](https://github.com/finos/community/issues/455)).
  - The project entered FINOS incubation on 2025-04-14.
  - Spec v1.0 was released on 2025-08-13, and CLI v1.0 was released on 2025-09-05.
  - The FINOS Technical Oversight Committee approved the project's graduation in October 2026.
- The code lives in the [finos/architecture-as-code](https://github.com/finos/architecture-as-code) monorepo, and the schema lives in [finos/calm-schema](https://github.com/finos/calm-schema).
  - The monorepo holds the CLI, CALM Hub, the VS Code extension, CALM Studio, CALM Guard and the documentation site.
  - Everything is licensed under Apache-2.0.
- The project has 19 maintainers from six organisations, of whom 13 work at Morgan Stanley ([finos/community#455](https://github.com/finos/community/issues/455)).
  - The other maintainers come from Fidelity Investments, Freddie Mac, Revanite, OpsFlow and turntabl.
  - Morgan Stanley and Fidelity Investments have agreed to be named publicly as adopters, and the project states that at least five organisations use it.

## 2. The problem it solves

- Architecture diagrams drift away from the systems they describe.
  - The project states that whiteboard sketches and Visio diagrams lack standardisation, version control and validation, and that keeping them in sync with the implementation is a manual, error-prone process ([why use CALM](https://calm.finos.org/introduction/why-use-calm)).
  - A Morgan Stanley lead architect described solution architecture documents as diagrams that "rot the moment they are saved" ([FINOS blog](https://www.finos.org/blog/confessions-of-a-calm-aholic-how-morgan-stanley-automates-architecture-without-writing-json)).
- A diagram cannot be checked by a machine.
  - A drawing cannot tell anyone whether a system still conforms to an approved reference architecture.
  - As a result, architecture review and compliance review in regulated firms are mostly done by people reading documents.
- Security and regulatory controls are usually recorded separately from the design.
  - Controls such as "connections leaving the firm must use mTLS" are typically tracked in a governance, risk and compliance tool or a spreadsheet.
  - CALM attaches controls directly to the nodes, relationships and flows they govern, which the Morgan Stanley architect named as the feature he had "always found missing".
- There is no shared format for describing architecture across teams and tools.
  - Without a standard, each team describes its systems differently, so descriptions cannot be reused, compared or aggregated across an organisation.
- The project claims measurable use, but the figures come from a single press source.
  - The graduation issue cites CIO Dive (August 2025) as saying that CALM eased more than 1,400 internal deployments at Morgan Stanley and underpinned more than 2,000 application deployments across several firms.
  - These figures were not independently verified for this note.

## 3. Core model

- Nodes are the components of the system ([nodes](https://calm.finos.org/core-concepts/nodes)).
  - Each node has a mandatory `unique-id` and a `node-type`, with documented examples including `actor`, `system`, `service`, `database`, `network` and `webclient`.
  - A node can point to a more detailed architecture through `details.detailed-architecture`, so models can be nested from system level down to service level.
  - A node can also name a `required-pattern` that its detailed architecture must follow.
- Relationships connect nodes, and CALM defines five relationship types ([relationships](https://calm.finos.org/core-concepts/relationships), [patterns](https://calm.finos.org/core-concepts/patterns)).
  - `interacts` describes an actor using a system or service.
  - `connects` describes one node connecting to a specific interface on another node, optionally with a protocol such as JDBC or HTTPS.
  - `deployed-in` describes a node deployed inside another, such as a service in a Kubernetes cluster.
  - `composed-of` describes a system made up of its parts.
  - `options` records a design decision in a pattern, where each choice lists the nodes and relationships it would add.
- Interfaces describe how a node exposes its functionality ([interfaces](https://calm.finos.org/core-concepts/interfaces)).
  - Examples include a host and port, a URL, an OAuth2 audience, a rate limit and a container image.
  - The 1.0 release removed the built-in interface types from the core schema, so organisations now define them through standards.
- Controls pair a requirement with a configuration that shows how the requirement is met ([controls](https://calm.finos.org/core-concepts/controls)).
  - The `requirement-url` points to a JSON Schema that defines the control, for example `security-002` "Permitted Connection" with an enumerated list of allowed protocols.
  - The `config-url`, or an inline `config`, holds this architecture's answer, for example `protocol: mTLS`, and it is validated against the requirement schema.
  - Controls are grouped by domain, such as security, and can be attached to nodes, relationships and flows.
- Flows describe a business process as an ordered set of transitions across existing relationships ([flows](https://calm.finos.org/core-concepts/flows)).
  - Each transition names a `relationship-unique-id`, a `sequence-number` and a `direction`, which is either `source-to-destination` or `destination-to-source`.
  - Validation fails if a transition references a relationship that does not exist or if two transitions share a sequence number.
  - The tooling can render a flow as a Mermaid sequence diagram.
- Standards are organisation-specific JSON Schema extensions of the core types ([standards](https://calm.finos.org/core-concepts/standards)).
  - A standard extends a core definition with `allOf` and `$ref`, for example to require a cost-centre or owner field on every node.
  - `calm validate` checks a document against core CALM and against every standard it references.
- Timelines, added in schema 1.2, record snapshots of an architecture at points in time ([timelines](https://calm.finos.org/core-concepts/timelines)).
  - Each snapshot is called a moment and has a `valid-from` date, a link to the detailed architecture at that time, and links to architecture decision records.
- Decorators, added in schema 1.2, attach supplementary data to an architecture without changing it ([decorators](https://calm.finos.org/core-concepts/decorators)).
  - Published decorator standards cover deployment status and control evaluation results, where each control is marked as met, not met or not applicable.
  - CALM Hub can draw control evaluation results on architecture diagrams.
- Metadata holds free-form key and value data on any element or on the whole architecture ([metadata](https://calm.finos.org/core-concepts/metadata)).
- The following example of a `connects` relationship is taken from the documentation.

  ```json
  {
    "unique-id": "service-to-db",
    "description": "The Spring Boot service connects to the PostgreSQL database for persistence.",
    "relationship-type": {
      "connects": {
        "source": { "node": "spring-service" },
        "destination": { "node": "postgres-db", "interfaces": ["db-interface"] }
      }
    },
    "protocol": "JDBC"
  }
  ```

## 4. Patterns and validation

- A pattern is a reusable reference architecture written in JSON Schema ([patterns](https://calm.finos.org/core-concepts/patterns)).
  - A pattern states which nodes and relationships must exist and which constraints apply to them.
  - Structural fields such as `unique-id` and `node-type` are fixed with `const`, while descriptive fields are left as plain strings for teams to fill in.
  - Cardinality and choice are expressed with `prefixItems`, `minItems`, `maxItems`, `items`, `oneOf`, `anyOf` and `options` relationships.
- A pattern serves two purposes.
  - `calm generate -p pattern.json -o architecture.json` creates a starting architecture with placeholders such as `[[ DESCRIPTION ]]`, and it prompts the user to choose between `oneOf` and `anyOf` alternatives.
  - `calm validate -p pattern.json -a architecture.json` checks that an existing architecture still contains the required nodes and relationships and respects the pattern's constraints.
- An architecture records the pattern it follows in its `$schema` field, which `calm generate` sets to the pattern's `$id` ([CALM Hub MCP and API](https://calm.finos.org/calm-hub/calm-hub-mcp-api)).
- Validation is standard JSON Schema validation with additional Spectral rules for flows and timelines ([validate](https://calm.finos.org/calm-cli/validate)).
  - The `--format junit` option produces test reports that CI systems can display, and `--strict` makes warnings fail the build.
  - The benefit is that architecture conformance becomes a pipeline check, and the limitation is that the check is only as good as the patterns and control schemas that architecture and security teams write and maintain.

## 5. Tooling

- The CLI is installed with `npm install -g @finos/calm-cli` or `brew install calm-cli`, and it requires Node.js 22.13 or later ([CLI](https://calm.finos.org/working-with-calm/cli)).
  - `generate` and `validate` work with patterns, as described in section 4.
  - `docify` builds a documentation website from an architecture, and it can export diagrams as SVG or PNG ([docify](https://calm.finos.org/calm-cli/docify)).
  - `template` renders Handlebars templates from the model, which can be used to produce Markdown reports or infrastructure configuration ([template](https://calm.finos.org/calm-cli/template)).
  - `diff` and `timeline` compare architectures and work with timelines.
  - `hub` and `workspace` push, pull and version documents in CALM Hub.
  - `init-ai` installs CALM agents or skills for GitHub Copilot, Kiro, Claude Code or Codex ([CALM AI tools](https://calm.finos.org/working-with-calm/calm-ai-tools)).
- The VS Code extension, named CALM Tools, activates on files whose `$schema` points to a CALM meta schema ([VS Code extension](https://calm.finos.org/working-with-calm/vscode-extension)).
  - It shows a tree of model elements, a live diagram preview with Docify and template tabs, and validation errors in the Problems panel.
- CALM Hub is a versioned store and REST API for architectures, patterns, flows, standards, interfaces, controls and architecture decision records, organised by namespace ([CALM Hub](https://calm.finos.org/calm-hub/)).
  - It runs on MongoDB in production or on NitriteDB as a standalone store, and it ships as the `finos/calm-hub` Docker image.
  - A public instance runs at [hub.calm.finos.org](https://hub.calm.finos.org/).
  - An experimental MCP server, disabled by default, lets AI agents list and search architectures, patterns, controls, timelines and decision records ([CALM Hub MCP and API](https://calm.finos.org/calm-hub/calm-hub-mcp-api)).
- CALM Studio is an experimental visual editor that keeps a diagram canvas and the CALM JSON in sync in both directions ([CALM Studio](https://calm.finos.org/working-with-calm/calm-studio)).
  - It includes extension packs for AWS, Azure, GCP, Kubernetes and AI agent components.
  - It can score a design against the 23 risk categories of the FINOS AI Governance Framework.
  - It currently generates CALM 1.2 rather than the latest 1.3.
- The validation server, `calm-server`, exposes validation as an HTTP endpoint at `POST /calm/validate` ([validation server](https://calm.finos.org/working-with-calm/validation-server)).
  - It has no built-in authentication, so it should only be exposed behind a gateway that adds it.

## 6. Spec versions

- The schema changelog lists the following releases ([calm-schema changelog](https://github.com/finos/calm-schema/blob/main/CHANGELOG.md)).
  - 1.0-rc1 and 1.0-rc2 were release candidates, and rc2 removed the built-in interface types and the node `run-as` property and renamed the control properties to `requirement-url`, `config-url` and `config`.
  - 1.0 was the first stable release, built on rc2, and was released on 2025-08-13.
  - 1.1 tightened the flow definition so that flows can no longer carry extra properties.
  - 1.2 added timelines and decorators.
  - 1.3 is a minor revision of 1.2 that adds optional `$schema` and `target-type` fields to decorators.
- Schemas are published at `https://calm.finos.org/release/<version>/meta/`, and a draft schema is being prepared for a later release.

## 7. Capital markets example

- An enterprise architecture team publishes a pattern for a low-latency order gateway.
  - The pattern requires an `actor` for the trading desk, an order entry `service`, a pre-trade risk check `service`, and a `connects` relationship to the exchange over FIX.
  - It attaches a control stating that every connection leaving the firm must use TLS or mTLS.
  - It attaches a control stating that orders must pass through the risk check service, which supports the firm's obligations under SEC Rule 15c3-5 on market access.
- An equities trading team runs `calm generate` against the pattern and fills in its own hosts, interfaces and control configurations.
- Every pull request to the team's architecture file runs `calm validate` in CI.
  - If someone adds a plain TCP connection to a market data vendor, or routes orders around the risk service, the build fails before a review meeting is needed.
- Decorators record each deployment and each control evaluation, so CALM Hub gives risk and audit staff a queryable view of which systems meet which controls.
  - The limitation is that this view shows the intended design, so it still needs to be reconciled with what is actually running in production.

## 8. Comparison with other architecture-as-code approaches

- The C4 model and Structurizr DSL describe architecture mainly for diagrams and communication.
  - They are easier to write by hand and produce clearer diagrams than CALM.
  - They do not have built-in controls, JSON Schema patterns or pattern conformance validation.
- Terraform and other infrastructure-as-code tools describe deployable infrastructure.
  - CALM describes the logical architecture one level above infrastructure, and it can generate infrastructure configuration through `calm template`.
  - CALM does not replace infrastructure as code, and a firm using both has two descriptions to keep consistent.
- ArchiMate and commercial enterprise architecture repositories cover business, application and technology views in more depth.
  - They are usually proprietary and are not designed to be edited and reviewed through pull requests.
  - CALM is narrower in scope, but it fits the same review and CI workflow as application code.

## 9. Limitations

- Writing CALM JSON by hand is slow and verbose.
  - The project addresses this with AI agents installed through `init-ai` and with the CALM Studio editor.
  - In a public Morgan Stanley demonstration, the AI assistant created a "System" where a "Service" was intended and mis-rendered an `interacts` relationship, so the architect had to correct it with further prompts ([FINOS blog](https://www.finos.org/blog/confessions-of-a-calm-aholic-how-morgan-stanley-automates-architecture-without-writing-json)).
- CALM describes the intended architecture and has no link to production observability.
  - The roadmap item for CALM-to-code observability was closed because no adopter asked for it ([finos/community#455](https://github.com/finos/community/issues/455)).
  - Unless deployment configuration is generated from the model, the model and the running system can still diverge.
- The documentation does not fully match the schema.
  - Some pages still show properties that 1.0-rc2 removed, such as `run-as` and the built-in interface types.
  - The relationships page lists four relationship types, while the patterns page lists five.
  - The schema changelog should be treated as the source of truth.
- The schema has changed quickly.
  - Versions 1.0 to 1.3 were released within about a year, and 1.1 began rejecting inline flow properties that 1.0 allowed.
- Governance is concentrated in one firm.
  - Morgan Stanley supplies most of the maintainers, although the project graduated with maintainers from six organisations.

## Resources

- [CALM documentation site](https://calm.finos.org/)
- [Why use CALM](https://calm.finos.org/introduction/why-use-calm)
- [CALM core concepts](https://calm.finos.org/core-concepts/)
- [CALM CLI documentation](https://calm.finos.org/working-with-calm/cli)
- [CALM Hub documentation](https://calm.finos.org/calm-hub/)
- [finos/architecture-as-code repository](https://github.com/finos/architecture-as-code)
- [finos/calm-schema repository and changelog](https://github.com/finos/calm-schema/blob/main/CHANGELOG.md)
- [FINOS graduation issue for CALM](https://github.com/finos/community/issues/455)
- [FINOS blog: how Morgan Stanley automates architecture with CALM](https://www.finos.org/blog/confessions-of-a-calm-aholic-how-morgan-stanley-automates-architecture-without-writing-json)
- [CIO Dive: Morgan Stanley open-sources CALM through FINOS](https://www.ciodive.com/news/morgan-stanley-open-source-software-development-finos-calm/758339/)
- [DevOps.com: Morgan Stanley open sources CALM](https://devops.com/morgan-stanley-open-sources-calm-the-architecture-as-code-solution-transforming-enterprise-devops)
