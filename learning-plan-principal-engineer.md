# Learning Plan: Principal Engineer

> This note is a 26-week plan, from 27 September 2026 to 21 March 2027, for building and operating one
> production-grade application end to end. Related notes: [production-readiness-checklist.md](production-readiness-checklist.md),
> [react.md](react.md), [devops.md](devops.md), [genai-architecture.md](genai-architecture.md).

## Contents

- [Goal and constraints](#goal-and-constraints)
- [The project: portfolio and trade blotter](#the-project-portfolio-and-trade-blotter)
- [Skill tiers](#skill-tiers)
- [Session format](#session-format)
- [Phases and gates](#phases-and-gates)
- [Week-by-week plan](#week-by-week-plan)
- [Progress tracker](#progress-tracker)
- [Resources](#resources)

## Goal and constraints

- The goal is to design, build, deploy and operate one production-grade application by 21 March 2027.
  - The purpose is to lead a development team as a principal engineer with first-hand experience of every layer.
  - The plan also supports a job change, because the finished application and its decision records become portfolio material.
- The time budget is 2 hours every Sunday for 26 Sundays, which is about 52 hours in total.
- The main gaps are hands-on building experience, UI development, and DevOps and deployment infrastructure.
- Each technology is learned because the project needs it, and the remaining topics are covered as short conceptual reads.
- Every phase is reviewed against [production-readiness-checklist.md](production-readiness-checklist.md).

## The project: portfolio and trade blotter

- A trade blotter is a screen that lists trades and orders as they happen, with one row per trade.
  - Each row usually shows the trade identifier, execution time, instrument, side, quantity, price, account, counterparty, status and derived values such as notional and unrealised P&L.
  - Users expect to filter, sort and group the rows, see live updates, open a trade for detail, and export the view.
- The application combines a blotter, an order ticket for creating or amending orders, and an AI assistant added in the GenAI phase.
- The project was chosen because it covers large tables, live updates, forms, authentication and charts, and because it fits my capital markets background.
- The stack is chosen so that the limited hours go to unfamiliar areas.

| Layer | Technology | Reason for the choice |
| --- | --- | --- |
| UI | React, TypeScript, Vite | This is my target frontend stack and my largest gap. |
| UI data and forms | TanStack Query, React Hook Form, Zod | These are the common choices for server state and validated forms. |
| Mock API (UI phase) | Mock Service Worker (MSW) | It lets the UI be built before the backend exists. |
| Backend | Java, Spring Boot | It is my strongest stack, so the hours go to the unfamiliar parts. |
| Database | PostgreSQL, Flyway | It is a standard relational store with versioned migrations. |
| Authentication | OpenID Connect with Keycloak | It is a standard protocol and can be self-hosted. |
| Build and delivery | Docker, GitHub Actions, GHCR | They provide an immutable image per commit and automated CI. |
| Hosting | Home server behind Nginx Proxy Manager | It follows the pinned-SHA, backup, migrate, switch and health-check deploy model. |
| Observability | OpenTelemetry | It is vendor-neutral and widely adopted. |
| GenAI | Spring AI with a Claude model | It keeps the AI feature in the same backend stack. |

## Skill tiers

- About 80% of the time goes to Tier 1 skills, which are learned by building them into the project.
  - React and TypeScript, including the rendering model, hooks, state, data fetching, forms and routing.
  - API design and a Spring Boot backend.
  - Authentication with OpenID Connect, and server-side authorisation.
  - Containers, CI/CD, an image registry and automated deployment.
  - Observability with logs, metrics, traces and health checks.
  - A testing strategy covering unit, integration and end-to-end tests.
  - A GenAI feature with tool use or retrieval, an evaluation set, guardrails and cost limits.
- Tier 2 skills are concepts I need to understand as an architect but will not implement in this project.
  - Kubernetes compared with Docker Compose and managed platforms, and when each one fits. See [kubernetes.md](kubernetes.md).
  - Infrastructure as code with Terraform, and GitOps with Argo CD.
  - Platform engineering, golden paths, internal developer platforms and DORA metrics.
  - Service level objectives, error budgets and threat modelling with STRIDE.
  - Cloud cost basics, and how AWS and Azure services map to what I run myself. See [cloud-architecture.md](cloud-architecture.md).
  - Architecture decision records and design documents.
- Tier 3 skills are deliberately skipped for now.
  - Streaming analytics is out of scope.
  - Mobile development, data mesh and lakehouse architectures are out of scope.
  - Machine learning theory beyond what the GenAI feature needs is out of scope.

## Session format

- Each Sunday session has 90 minutes of building and 30 minutes of writing, and it ends with a commit.
  - In the first 10 minutes, I re-read last week's note and pick the session's single goal.
  - In the next 80 minutes, I build it. I use AI coding assistants for boilerplate, but I write the code for the concept being learned myself, so that I understand it.
  - In the last 30 minutes, I write a note in this repository or an architecture decision record, and I read one Tier 2 topic when time allows.
- If I miss a Sunday, I use one of the two buffer weeks rather than compressing the next session.
- The project lives in `~/Documents/code/trade-blotter`, and running `claude` there starts a `mentor` agent.
  - The mentor writes a session guide for each week, explains concepts, reviews my code and notes, and records progress in `mentor/progress.md`.
  - The mentor never writes code, and a hook blocks it from writing any file outside its `mentor/` folder.

## Phases and gates

- Each phase must pass its gate before the next phase starts.

| Phase | Weeks | Dates | Gate that closes the phase |
| --- | --- | --- | --- |
| 1. UI foundations and the blotter | 1 to 8 | 27 Sep to 15 Nov 2026 | The UI demo works end to end on mock data, with tests and an ADR. |
| 2. Backend, data and authentication | 9 to 12 | 22 Nov to 13 Dec 2026 | Users log in, and the blotter shows live data from the Spring Boot API. |
| Buffer | 13 to 14 | 20 Dec and 27 Dec 2026 | Missed sessions are caught up. |
| 3. Containers, CI/CD and deployment | 15 to 18 | 3 Jan to 24 Jan 2027 | The app is deployed from CI and is reachable over HTTPS on the home server. |
| 4. Operate it | 19 to 20 | 31 Jan and 7 Feb 2027 | The production readiness review is passed, and open items have owners. |
| 5. GenAI feature | 21 to 24 | 14 Feb to 7 Mar 2027 | The assistant meets the target score on the evaluation set. |
| 6. Reflect and position | 25 to 26 | 14 Mar and 21 Mar 2027 | The architecture write-up is published, and two practice design sessions are done. |

## Week-by-week plan

| Week | Sunday | Focus | What I build or write |
| --- | --- | --- | --- |
| 1 | 27 Sep 2026 | How React renders, JSX, and TypeScript basics | A Vite, React and TypeScript scaffold with a positions table from static data |
| 2 | 4 Oct 2026 | Components, props, state, and hooks, including when not to use `useEffect` | A positions table that can be filtered and sorted |
| 3 | 11 Oct 2026 | Routing and a feature-based folder structure | Pages for positions, orders and the order ticket with React Router |
| 4 | 18 Oct 2026 | Server state with TanStack Query, and loading, error and empty states | Data fetched from a mock API built with MSW, with an error boundary |
| 5 | 25 Oct 2026 | Forms and validation with React Hook Form and Zod | An order ticket with validation, duplicate-submit protection and an idempotency key |
| 6 | 1 Nov 2026 | A component library and accessibility basics | A consistent layout, keyboard navigation, and P&L that does not rely on colour alone |
| 7 | 8 Nov 2026 | Performance: memoisation, virtualised tables and throttled updates | A 10,000-row blotter with simulated streaming prices |
| 8 | 15 Nov 2026 | UI testing with Vitest, Testing Library and one Playwright test | Tests for the order ticket, and an ADR on the state-management choices |
| 9 | 22 Nov 2026 | Contract-first API design with OpenAPI | A Spring Boot API that replaces the mock API |
| 10 | 29 Nov 2026 | Persistence and migrations | PostgreSQL with Flyway, and integration tests with Testcontainers |
| 11 | 6 Dec 2026 | Authentication and authorisation | Keycloak login with OpenID Connect, and server-side access checks per account |
| 12 | 13 Dec 2026 | Real-time delivery with server-sent events or WebSockets | Live trade and price updates pushed from the backend to the blotter |
| 13 | 20 Dec 2026 | Buffer | Catch up on missed sessions |
| 14 | 27 Dec 2026 | Buffer | Catch up on missed sessions |
| 15 | 3 Jan 2027 | Containers | Multi-stage Dockerfiles and a local Docker Compose stack |
| 16 | 10 Jan 2027 | Continuous integration | A GitHub Actions pipeline that builds, tests, scans and publishes images to GHCR |
| 17 | 17 Jan 2027 | Deployment | A pinned-SHA deploy script with backup, migrate, switch and health check, behind Nginx Proxy Manager with TLS |
| 18 | 24 Jan 2027 | Tier 2 concepts: IaC, GitOps, and Kubernetes compared with Compose | An ADR explaining which runtime platform I would choose at work, and why |
| 19 | 31 Jan 2027 | Observability with OpenTelemetry | Traces, metrics, structured logs and one dashboard |
| 20 | 7 Feb 2027 | SLOs, alerts and a STRIDE threat model | A production readiness review of the app against the checklist |
| 21 | 14 Feb 2027 | GenAI feature design and evaluation | A written feature design and an evaluation set of 20 to 30 questions |
| 22 | 21 Feb 2027 | Tool use with Spring AI | A portfolio assistant that answers questions by calling the app's own APIs |
| 23 | 28 Feb 2027 | Guardrails, prompt-injection defences and cost tracking | Output validation, limited tool permissions and a token budget per user |
| 24 | 7 Mar 2027 | Evaluation and iteration | Evaluation results before and after changes, recorded in an ADR |
| 25 | 14 Mar 2027 | Cloud mapping and cost | A mapping of the setup to AWS or Azure services, with a cost estimate |
| 26 | 21 Mar 2027 | Architecture write-up and interview preparation | C4 diagrams, the ADR set, and two practice system design sessions |

## Progress tracker

- [ ] Phase 1 is complete: the UI demo works end to end on mock data, with tests and an ADR. The phase started on 27 September 2026.
- [ ] Phase 2 is complete: users log in, and the blotter shows live data from the Spring Boot API.
- [ ] Phase 3 is complete: the app is deployed from CI and is reachable over HTTPS on the home server.
- [ ] Phase 4 is complete: the production readiness review is passed, and open items have owners.
- [ ] Phase 5 is complete: the assistant meets the target score on the evaluation set.
- [ ] Phase 6 is complete: the architecture write-up is published, and two practice design sessions are done.

## Resources

- [React documentation](https://react.dev/learn), which is the primary source for the UI phase.
- [TanStack Query documentation](https://tanstack.com/query/latest) and [React Hook Form documentation](https://react-hook-form.com/), which cover server state and forms.
- [Spring Boot reference documentation](https://docs.spring.io/spring-boot/) and [Spring AI reference documentation](https://docs.spring.io/spring-ai/reference/), which cover the backend and GenAI phases.
- [OpenTelemetry documentation](https://opentelemetry.io/docs/), which covers the observability phase.
- [Google SRE books](https://sre.google/books/), which cover SLOs and production readiness.
