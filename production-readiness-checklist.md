# Production Readiness Checklist

> This note lists the aspects a tech lead should check when building a production-grade application.
> It is a working checklist to review at design time, before each release, and before go-live.
> Related notes: [software-architecture.md](software-architecture.md), [system-design.md](system-design.md),
> [devops.md](devops.md), [react.md](react.md), [ai-security.md](ai-security.md).

## Contents

- [How to use this checklist](#how-to-use-this-checklist)
- [Requirements and non-functional requirements](#requirements-and-non-functional-requirements)
- [Architecture and design decisions](#architecture-and-design-decisions)
- [Frontend (UI)](#frontend-ui)
- [APIs and integration](#apis-and-integration)
- [Data management](#data-management)
- [Security](#security)
- [Reliability and resilience](#reliability-and-resilience)
- [Observability](#observability)
- [Performance and scalability](#performance-and-scalability)
- [Testing and code quality](#testing-and-code-quality)
- [Build, CI/CD and deployment](#build-cicd-and-deployment)
- [Infrastructure and configuration](#infrastructure-and-configuration)
- [Operations and incident management](#operations-and-incident-management)
- [Compliance, audit and governance](#compliance-audit-and-governance)
- [GenAI features](#genai-features)
- [Cost](#cost)
- [Team, process and documentation](#team-process-and-documentation)
- [Go-live readiness review](#go-live-readiness-review)
- [Resources](#resources)

## How to use this checklist

- Each section lists questions that the team should be able to answer with evidence, not with intent.
  - A good answer points to an artifact, such as a dashboard, a test, a runbook, or a decision record.
  - An item that does not apply should be marked as not applicable with a short reason, so that the omission is a decision rather than an oversight.
- The checklist is used at three points in the life of an application.
  - At design time, it helps the team find non-functional requirements that nobody has written down yet.
  - Before each release, it is a quick review of the items that the release changes.
  - Before go-live, the full list becomes the production readiness review described at the end of this note.
- The depth of each item should match the risk of the application.
  - An internal reporting tool and a client-facing order entry system need the same categories, but they need very different levels of rigour in each one.

## Requirements and non-functional requirements

- The team should know who the users are, what they need to do, and which business outcome the application supports.
- The non-functional requirements should be written down with numbers, because a vague requirement cannot be tested.
  - Availability should be stated as a target, such as 99.9% during trading hours, together with the hours that matter.
  - Latency should be stated as a percentile, such as p95 under 300 ms for the blotter query, rather than as an average.
  - Expected load should include the normal volume and the peak volume, such as market open or month-end.
  - Data volume and growth should be estimated, because they drive database and storage choices.
- Recovery objectives should be agreed with the business.
  - The recovery point objective (RPO) is the maximum amount of data the business accepts losing.
  - The recovery time objective (RTO) is the maximum time the business accepts the application being down.
- Regulatory and data-residency constraints should be identified at the start, because they are expensive to add later.
- The team should record what is out of scope, so that scope changes are visible when they happen.

## Architecture and design decisions

- Significant decisions should be recorded as [architecture decision records](https://adr.github.io/), each with the context, the options considered, the decision, and its consequences.
- The system should be described with a small set of diagrams, such as the context and container levels of the [C4 model](https://c4model.com/).
- The team should prefer the simplest architecture that meets the requirements.
  - A modular monolith is often a better starting point than microservices, because it avoids distributed-system failure modes until the team needs independent deployment. See [microservice.md](microservice.md).
  - The limitation of a monolith is that one team's change can block another team's release, so the module boundaries should be kept clean enough to split later.
- Every external dependency should be listed with its owner, its service level, and what the application does when it is unavailable.
- Build-versus-buy decisions should consider the total cost of ownership, including upgrades, security patches, and the skills needed to operate the component.
- The design should state how the application will be changed safely, including how database schemas and APIs evolve without downtime.

## Frontend (UI)

- **Architecture and state**
  - The team should separate server state from client state.
    - Server state is data owned by the backend, such as positions or orders, and a library such as [TanStack Query](https://tanstack.com/query/latest) handles caching, refetching, and staleness for it.
    - Client state is data owned by the browser, such as an open dialog or a filter value, and it usually fits in component state or a small store. See [redux.md](redux.md).
  - The folder structure should group code by feature rather than by file type, so that a feature can be understood and changed in one place.
  - The rendering strategy should be chosen deliberately.
    - Client-side rendering suits authenticated internal applications, where search engine indexing does not matter.
    - Server-side rendering or static generation suits public pages where first-load speed and indexing matter, at the cost of a more complex hosting model.
- **User experience states**
  - Every screen that loads data should handle four states: loading, empty, error, and success.
  - Errors should tell the user what happened and what they can do next, and they should not expose stack traces or internal identifiers.
  - Long-running actions should show progress and should prevent duplicate submission, for example by disabling the submit button on an order ticket until the request completes.
  - The application should use an [error boundary](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary) so that one failing component does not blank the whole page.
- **Forms and validation**
  - Validation should run in the browser for fast feedback and on the server for correctness, because browser validation can be bypassed.
  - A single schema, for example with [Zod](https://zod.dev/), can drive both the form validation and the TypeScript types.
- **Performance**
  - The team should measure [Core Web Vitals](https://web.dev/articles/vitals) (LCP, INP, CLS) for real users, not only in local testing.
  - Bundle size should be tracked in CI, and large routes should be split with lazy loading.
  - Large tables, such as a blotter with thousands of rows, should use virtualisation so that only visible rows are rendered.
  - Real-time updates, such as streaming prices, should be throttled or batched so that the browser does not re-render on every message.
- **Accessibility**
  - The application should meet [WCAG 2.2](https://www.w3.org/TR/WCAG22/) level AA, which is a legal requirement in many jurisdictions.
  - Every interactive element should be usable with the keyboard, and focus should be visible.
  - Colour should not be the only signal, which matters for profit-and-loss values shown only in red and green.
  - Automated checks such as [axe](https://github.com/dequelabs/axe-core) catch only part of the problems, so a manual keyboard and screen-reader pass is still needed.
- **Security in the browser**
  - The team should rely on React's default escaping and should review every use of `dangerouslySetInnerHTML`.
  - A [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) should restrict which scripts can run.
  - Tokens should not be stored in `localStorage`, because any cross-site scripting flaw can read them. A backend-for-frontend with an HTTP-only session cookie is safer, at the cost of an extra server component. See [oauth.md](oauth.md).
  - The browser must never be the place where authorisation is enforced, because hiding a button does not stop a direct API call.
- **Consistency and maintainability**
  - A shared component library or design system keeps screens consistent and reduces repeated work.
  - Internationalisation, number formatting, time zones, and currency formatting should be decided early. Trade times, for example, should be stored in UTC and displayed in the user's or the market's time zone, and the choice should be explicit.
  - The team should agree which browsers and screen sizes are supported.
- **Frontend observability**
  - Browser errors should be reported to a central tool, together with the release version, so that they can be traced to a deployment.

## APIs and integration

- APIs should be designed contract-first, for example with [OpenAPI](https://www.openapis.org/), so that the frontend and backend can work in parallel. See [api-development.md](api-development.md).
- The versioning policy should be defined before the first external consumer appears.
  - Additive changes should not break existing clients, and removals should follow a published deprecation period.
- Operations that change state should be idempotent where a client may retry.
  - An idempotency key on order submission, as described in [Stripe's API design](https://stripe.com/docs/api/idempotent_requests), prevents a network retry from creating a duplicate order.
- Every outbound call should have a timeout, and retries should use exponential backoff with jitter.
- Collection endpoints should paginate, and the team should prefer cursor-based pagination for large or frequently changing data sets.
- Errors should use a consistent format, such as [RFC 9457 problem details](https://www.rfc-editor.org/rfc/rfc9457), so that clients can handle them uniformly.
- Rate limits should protect the service from misbehaving clients, and clients should receive a clear response when a limit is reached.
- Asynchronous integration through a broker should define message schemas, ordering guarantees, delivery semantics, and a dead-letter process. See [kafka.md](kafka.md) and [rabbitmq.md](rabbitmq.md).

## Data management

- Schema changes should be applied by a migration tool such as [Flyway](https://documentation.red-gate.com/flyway) and should be version-controlled with the code.
- Migrations should be backward compatible with the previous release, so that the application can be rolled back without rolling back the database.
  - The expand-and-contract pattern adds the new column first, migrates the code, and removes the old column in a later release.
- Backups should exist, run on a schedule, be stored away from the primary system, and be tested by restoring them.
  - A backup that has never been restored should be treated as unverified.
- The team should know which data is personal or confidential, where it is stored, and who can read it.
- Retention and deletion rules should be implemented in code rather than left as policy only.
- Indexes should be designed from the actual query patterns. See [database-index.md](database-index.md) and [postgresql.md](postgresql.md).
- Reference data, such as instruments or counterparties, should have one authoritative source and a documented refresh process.

## Security

- The team should produce a lightweight threat model, for example with [STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats), and revisit it when the architecture changes.
- Authentication should use a standard protocol such as OpenID Connect rather than a custom login mechanism. See [authentication-authorization.md](authentication-authorization.md) and [spring-security.md](spring-security.md).
- Authorisation should be enforced on the server for every request, including checks that a user can access the specific record requested.
  - Broken object-level authorisation, where a user changes an account identifier in the URL and sees another client's positions, is one of the most common API flaws in the [OWASP API Security Top 10](https://owasp.org/API-Security/).
- Secrets should never be committed to source control, and they should be injected at runtime and rotated.
- Dependencies should be scanned for known vulnerabilities in CI, and the team should have a process for applying urgent patches. See [opensource-vulnerability.md](opensource-vulnerability.md).
- Build artifacts should be traceable to source, for example with a software bill of materials and the practices described in [SLSA](https://slsa.dev/).
- All traffic should use TLS, and security headers should be configured at the edge.
- Security-relevant events, such as logins, permission changes, and failed access attempts, should be logged in a way that supports investigation.
- The [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) can be used as a detailed verification list when the application's risk justifies it.

## Reliability and resilience

- The team should list the failure modes of each dependency and decide the behaviour for each one.
  - For example, if the market data feed is down, the blotter could show the last known prices with a clear stale-data indicator instead of failing entirely.
- Circuit breakers and bulkheads, for example with [Resilience4j](https://resilience4j.readme.io/), prevent one slow dependency from exhausting threads across the whole service.
- The application should expose separate liveness and readiness health checks, because they answer different questions for the orchestrator.
- The application should shut down gracefully, finishing in-flight requests before it stops.
- Single points of failure should be identified, and each one should either be removed or accepted in writing with the reason.
- Disaster recovery should be rehearsed, because an untested recovery plan usually fails in ways nobody predicted.

## Observability

- Logs should be structured, for example as JSON, and should carry a correlation or trace identifier across services.
- Logs must not contain secrets, tokens, or unnecessary personal data.
- Metrics should cover the [four golden signals](https://sre.google/sre-book/monitoring-distributed-systems/): latency, traffic, errors, and saturation.
- Distributed tracing with [OpenTelemetry](https://opentelemetry.io/docs/) shows where time is spent across services and is vendor-neutral.
- Service level objectives should be defined from the user's point of view, and the error budget should guide the balance between feature work and reliability work. See the [SRE book chapter on SLOs](https://sre.google/sre-book/service-level-objectives/).
- Alerts should fire on symptoms that affect users rather than on every internal cause, and every alert should link to a runbook.
- Business metrics, such as orders submitted or reports generated, should be visible next to technical metrics, because they often reveal problems first.

## Performance and scalability

- The team should load test the expected peak and a margin above it before go-live, and should repeat the test after significant changes.
- The team should know which component saturates first, and what the plan is when it does.
- Caching should be introduced for a measured reason, and the invalidation rule should be written down, because stale data can be a correctness problem.
- Stateless services scale horizontally more easily, so session state should live in a shared store or in the client.
- Database connection pools, thread pools, and queue sizes should be sized deliberately rather than left at their defaults.

## Testing and code quality

- The test suite should follow a pyramid, with many fast unit tests, fewer integration tests, and a small number of end-to-end tests.
  - Integration tests against real dependencies, for example with [Testcontainers](https://testcontainers.com/), catch problems that mocks hide. See [integration-test.md](integration-test.md) and [testing-spring-boot.md](testing-spring-boot.md).
  - End-to-end tests with a tool such as [Playwright](https://playwright.dev/) should cover the critical user journeys only, because they are slow and more fragile.
  - Contract tests help when several teams own the services on either side of an API.
- Tests should run on every pull request, and a failing test should block the merge.
- Code review should check design, readability, and risk, while formatting and simple rules are left to automated linters.
- The team should agree a definition of done that includes tests, documentation, and observability for each change.
- Test data should be realistic but must not be copied from production without masking.

## Build, CI/CD and deployment

- Every build should be reproducible and should produce one immutable artifact, such as a container image, that is promoted unchanged through each environment. See [docker.md](docker.md).
- Images should be tagged with the commit identifier rather than with a mutable tag such as `latest`, so that the running version is always known.
- The pipeline should run build, tests, security scans, and packaging automatically on every change.
- Deployments should be automated, repeatable, and reversible.
  - The team should know how to roll back, how long it takes, and whether the database migration allows it.
  - Progressive delivery, such as canary or blue-green releases, reduces the impact of a bad release at the cost of more infrastructure.
- Feature flags allow code to be deployed before it is released, but each flag should have an owner and a removal date, because old flags become technical debt.
- The team should track [DORA metrics](https://dora.dev/guides/dora-metrics-four-keys/): deployment frequency, lead time for changes, change failure rate, and time to restore service.

## Infrastructure and configuration

- Infrastructure should be defined as code, for example with Terraform, so that environments can be recreated and reviewed. See [cloud-architecture.md](cloud-architecture.md).
- Configuration should be separated from code, following the [twelve-factor app](https://12factor.net/config) principle, so that the same artifact runs in every environment.
- Environments should be as similar as practical, because differences between test and production cause failures that tests did not catch.
- The team should choose the runtime platform based on the team's operating capacity.
  - A managed platform reduces operational work but limits control and can increase cost.
  - Kubernetes gives flexibility and portability but requires skills and time to operate. See [kubernetes.md](kubernetes.md).
- Network access should follow least privilege, with only the required ports and paths exposed.

## Operations and incident management

- Every service should have a named owning team and an on-call arrangement that matches its availability target.
- Runbooks should describe how to diagnose and resolve the common failures, and they should be tested by someone who did not write them.
- The team should have an incident process that defines severity levels, who leads the response, and how stakeholders are informed.
- Incidents should be followed by a blameless post-incident review, and the resulting actions should be tracked to completion.
- Routine operational tasks, such as certificate renewal and dependency upgrades, should be scheduled or automated so that they do not depend on memory.

## Compliance, audit and governance

- The application should keep an audit trail of who did what and when for every business-relevant action.
  - In capital markets, record-keeping rules such as [SEC Rule 17a-4](https://www.ecfr.gov/current/title-17/chapter-II/part-240/subject-group-ECFR3dd95cf4d3f4f6a/section-240.17a-4) and MiFID II can require specific retention periods and tamper-resistant storage.
- Access to production and to sensitive data should be reviewed periodically.
- The team should check the licences of third-party dependencies, because some licences impose obligations on distribution.
- Changes to production should follow the organisation's change-management process, and automated pipelines should produce the evidence that the process needs.

## GenAI features

- The team should build an evaluation set before tuning prompts, so that changes can be measured rather than judged by impression. See [genai-architecture.md](genai-architecture.md).
- Prompt injection should be treated as a permanent design constraint, and the model's tools and data access should be limited accordingly. See [ai-security.md](ai-security.md) and the [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/).
- Model output should be validated before it is used, especially when it is passed to another system or shown as fact.
- Token cost and latency should be monitored per feature, and limits should prevent unexpected spend.
- The application should log prompts, retrieved context, and responses where policy allows, so that failures can be investigated.
- The team should decide how model upgrades are tested and rolled out, because a new model version can change behaviour without any code change.

## Cost

- The team should estimate the running cost before go-live and compare it with the value the application delivers.
- Resources should be tagged by application and environment so that cost can be attributed.
- Non-production environments should be scaled down or stopped outside working hours where possible.
- The team should review the largest cost items regularly, because costs tend to grow without anyone deciding to increase them.

## Team, process and documentation

- The repository should contain a README that lets a new engineer build, test, and run the application locally within a day.
- Architecture decision records, diagrams, runbooks, and API specifications should live close to the code so that they are updated with it.
- The team should keep a visible technical-debt list and should reserve capacity to reduce it.
- Ownership of each component, each dependency, and each operational task should be clear.
- The tech lead should make sure that knowledge is shared, so that no single engineer is the only person who can deploy or debug a critical part.

## Go-live readiness review

- Before the first production release, the team should hold a production readiness review that walks through this checklist. The [Google SRE book chapter on the engagement model](https://sre.google/sre-book/evolving-sre-engagement-model/) describes the practice.
- The review should confirm, with evidence, at least the following items.
  - The non-functional requirements are written down and have been tested.
  - Backups run on a schedule and a restore has been performed successfully.
  - A rollback has been rehearsed.
  - Dashboards, alerts, and runbooks exist, and the on-call team has seen them.
  - A security review and dependency scan have been completed, and open findings have owners.
  - The owning team, support hours, and escalation path are documented.
- Items that are not ready should be recorded as accepted risks with an owner and a date, rather than being dropped silently.

## Resources

- [Google SRE books](https://sre.google/books/), which cover monitoring, SLOs, incident response, and production readiness.
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) and [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/), which provide cloud-oriented review questions similar to this checklist.
- [Release It!, second edition, by Michael Nygard](https://pragprog.com/titles/mnee2/release-it-second-edition/), which describes stability patterns and production failure modes.
- [The twelve-factor app](https://12factor.net/), which describes conventions for building deployable services.
- [OWASP Application Security Verification Standard](https://owasp.org/www-project-application-security-verification-standard/), which provides a detailed security checklist.
- [web.dev](https://web.dev/), which covers frontend performance and accessibility practices.
- [Accelerate, by Forsgren, Humble and Kim](https://itrevolution.com/product/accelerate/), which presents the research behind the DORA metrics.
