# Delivering Standards, Policies and Architecture Knowledge to Coding Agents

Research date: 2026-10-29. Items dated before 2025 are marked "(pre-2025)". Vendor-published statistics are marked "(vendor)".

## 1. Instruction and rules files: formats, layering and known limits

### Takeaway
Every major coding agent now reads a Markdown instruction file that is layered from organization to user to repository to directory, and AGENTS.md has become the cross-vendor baseline under Linux Foundation governance. The evidence shows that these files are treated as advisory context rather than enforced configuration, and that long or unnecessary instructions reduce adherence and can lower task success.

### Cited Findings

**AGENTS.md and its governance**
- AGENTS.md is a plain Markdown file with no required fields that acts as a "README for agents", holding build steps, tests and conventions separately from the human README. — [agents.md](https://agents.md/)
- The agents.md site states that AGENTS.md is used by "over 60k open-source projects"; this figure is self-reported by the project. — [agents.md](https://agents.md/)
- The listed supporting tools include OpenAI Codex, Google Jules, Google Gemini CLI, Cursor, GitHub Copilot coding agent, VS Code, Windsurf/Devin, JetBrains Junie, Aider, goose, opencode, Zed, Warp, Amp, Factory, RooCode, Kilo Code, Augment Code, UiPath and Semgrep. — [agents.md](https://agents.md/)
- The conflict rule is that the AGENTS.md nearest to the edited file wins, and explicit user prompts in chat override all AGENTS.md files. — [agents.md](https://agents.md/)
- The Linux Foundation announced the Agentic AI Foundation (AAIF) on 9 December 2025, with three founding projects: Anthropic's MCP, Block's goose and OpenAI's AGENTS.md. OpenAI, Anthropic and Block co-founded it, with support from Google, Microsoft, AWS, Bloomberg and Cloudflare. — [OpenAI](https://openai.com/blog/agentic-ai-foundation); [AAIF](https://aaif.io/news/linux-foundation-announces-formation-of-aaif); [InfoQ](https://infoq.com/news/2025/12/agentic-ai-foundation/)
- The AAIF is structured as a directed fund under the Linux Foundation that provides neutral governance for shared specifications and reference implementations. — [InfoQ](https://infoq.com/news/2025/12/agentic-ai-foundation/); [Redmond Mag](https://redmondmag.com/Articles/2025/12/09/Linux-Foundation-Launches-Agentic-AI-Foundation.aspx)
- AGENTS.md was released by OpenAI in August 2025, according to secondary coverage. — [dev.to](https://dev.to/digitalapplied/agentic-ai-foundation-open-source-agent-standards-gl8)
- The agents.md site does not describe a versioned specification. — [agents.md](https://agents.md/)

**OpenAI Codex discovery of AGENTS.md**
- Codex reads a global file from `~/.codex` (or `CODEX_HOME`), preferring `AGENTS.override.md` over `AGENTS.md`, then walks from the Git root down to the working directory and takes at most one file per directory. — [OpenAI Codex docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Files are concatenated root-to-leaf, so files closer to the working directory appear later and override broader guidance. — [OpenAI Codex docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- Codex stops adding files once the combined content reaches `project_doc_max_bytes`, which defaults to 32 KiB, so large instruction sets are silently truncated unless the limit is raised or the content is split across directories. — [OpenAI Codex docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- `project_doc_fallback_filenames` in `config.toml` lets Codex treat other names (for example `TEAM_GUIDE.md`) as instruction files, and the chain is built once per session. — [OpenAI Codex docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

**Claude Code (CLAUDE.md and `.claude/rules/`)**
- Claude Code loads a managed-policy CLAUDE.md from a system path (`/etc/claude-code/CLAUDE.md` on Linux, `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS, `C:\Program Files\ClaudeCode\CLAUDE.md` on Windows), intended for company coding standards, security policies and compliance requirements. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- The managed CLAUDE.md is distributed with MDM, Group Policy or Ansible, or embedded via a `claudeMd` key in `managed-settings.json`, and developers cannot exclude it with `claudeMdExcludes`. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Anthropic's documentation distinguishes guidance from enforcement: CLAUDE.md is for code style, compliance reminders and behaviour, while blocking tools, commands or paths belongs in managed settings such as `permissions.deny` and sandbox settings. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- The documentation states that CLAUDE.md content is "context, not enforced configuration", and recommends a PreToolUse hook to block an action regardless of what the model decides. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- CLAUDE.md files above the working directory load at launch, while those in subdirectories load on demand when Claude reads or edits files there. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- `.claude/rules/*.md` files can carry a `paths` frontmatter field so they load only when matching files are touched, and the directory supports symlinks to a shared rules set (for example `ln -s ~/company-standards/security.md .claude/rules/security.md`). — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- `@path` imports expand other files into context with a maximum depth of four hops, but the docs note that imports organize a file without reducing its context cost. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Anthropic recommends keeping each CLAUDE.md under 200 lines because longer files consume more context and reduce adherence. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Claude Code reads AGENTS.md when no CLAUDE.md exists in the working directory or above it, and reading AGENTS.md directly requires v2.1.277 or later; otherwise a CLAUDE.md can import it. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)

**Cursor rules**
- Project rules are `.mdc` files in `.cursor/rules` with frontmatter fields `description`, `globs` and `alwaysApply`, giving four modes: Always Apply, Apply Intelligently (by description), Apply to Specific Files (glob) and Apply Manually (`@rule`). — [Cursor docs](https://cursor.com/docs/context/rules)
- Team rules are managed in the Cursor dashboard on Team and Enterprise plans, admins can enforce them so users cannot disable them, and precedence runs Team, then Project, then User, with all applicable rules merged. — [Cursor docs](https://cursor.com/docs/context/rules)
- Cursor also reads root and nested AGENTS.md files, where the more specific file wins. — [Cursor docs](https://cursor.com/docs/context/rules)
- Cursor recommends keeping rules under 500 lines, and it notes that `@file` references in a rule point the agent to a file without inlining its content. — [Cursor docs](https://cursor.com/docs/context/rules)

**GitHub Copilot custom instructions**
- Copilot supports personal instructions, repository-wide `.github/copilot-instructions.md`, path-specific `.github/instructions/**/*.instructions.md` with an `applyTo` glob, agent instruction files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, plus `REVIEW.md` for code review), and organization-level instructions. — [GitHub docs: support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- Support varies by surface: organization instructions apply only on GitHub.com (Chat, cloud agent, code review), VS Code Chat reads only AGENTS.md among agent files, and Eclipse code review supports none. — [GitHub docs: support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- Organization instructions require Copilot Business or Enterprise. GitHub's precedence lists path-specific first, then repository-wide, then agent instructions, with organization instructions last; one third-party page gives a different ordering, which conflicts with GitHub's documentation. — [GitHub docs: custom instructions](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions); contradicted by [agentpatterns.ai](https://agentpatterns.ai/training/copilot/customization-primitives/)
- Copilot code review gained path-scoped instruction file support in September 2025. — [GitHub changelog](https://github.blog/changelog/2025-09-03-copilot-code-review-path-scoped-custom-instruction-file-support)

**Windsurf rules**
- Windsurf rules use a `trigger` frontmatter field with four modes: `always_on`, `model_decision`, `glob` and `manual`; the legacy `.windsurfrules` file has no activation modes. — [memorylake.ai (third-party)](https://www.memorylake.ai/en/blogs/choose-windsurf-rule-trigger-modes); [agentconfig-ing](https://agentconfig-ing.pages.dev/files/windsurf-rules-md)
- Global rules are capped at 6,000 characters, while the workspace limit is reported as 12,000 characters per file by one source and as 6,000 per file / 12,000 total by another. — [agentconfig-ing](https://agentconfig-ing.pages.dev/files/windsurf-rules-md); conflicting with [agentconfig-ing comparison](https://agentconfig-ing.pages.dev/compare/cursor-vs-windsurf)

**Kiro steering files**
- Kiro stores workspace steering in `.kiro/steering/` and global steering in `~/.kiro/steering/`, with workspace files winning on conflict. — [Kiro docs](https://kiro.dev/docs/steering/)
- The default files are `product.md` (purpose and users), `tech.md` (frameworks, libraries and constraints) and `structure.md` (layout, naming and architectural patterns), which the IDE can generate. — [Kiro docs](https://kiro.dev/docs/steering/)
- Inclusion modes are `always`, `fileMatch`, `manual` and `auto`, and `#[[file:path]]` references can pull in live workspace files such as an OpenAPI spec. — [Kiro docs](https://kiro.dev/docs/steering/)
- Kiro documents distributing global steering as team standards by pushing files through MDM or Group Policy, or by having users download them from a central repository. — [Kiro docs](https://kiro.dev/docs/steering/)
- Kiro also reads AGENTS.md files, which are always included and ignore inclusion modes. — [Kiro docs](https://kiro.dev/docs/steering/)

**Agent Skills (SKILL.md)**
- A skill is a folder with a `SKILL.md` containing at minimum `name` and `description` frontmatter, plus optional `scripts/`, `references/` and `assets/`. — [agentskills.io](https://agentskills.io/)
- Skills use progressive disclosure: only name and description load at startup, the full SKILL.md loads when a task matches, and bundled files load during execution, which keeps the standing context cost small. — [agentskills.io](https://agentskills.io/)
- The format was developed by Anthropic and released as an open standard, with spec discussion on GitHub. — [agentskills.io](https://agentskills.io/); [GitHub agentskills](https://github.com/agentskills/agentskills)
- Secondary sources report that Codex reads skills from `.agents/skills/` and `~/.codex/skills`, that Copilot reads `.github/skills/` and `.agents/skills/`, and that 30+ tools supported the format by April 2026; these are aggregator claims. — [noqta.tn](https://noqta.tn/en/news/skill-md-open-standard-30-ai-coding-tools-adoption-2026); [noqta.tn blog](https://noqta.tn/en/blog/agent-skills-skill-md-universal-ai-coding-standard-2026)

**Limits: instruction decay and context cost**
- The paper "Evaluating AGENTS.md" (Gloaguen et al., ETH Zurich / LogicStar, arXiv 2602.11988, February 2026, ICLR 2026) found that context files tend to reduce task success compared with no repository context and raise inference cost by over 20%. — [arXiv](https://arxiv.org/abs/2602.11988)
- In that study, LLM-generated context files lowered success by about 0.5 to 2 points and developer-written files gave only about a 4% gain, and agents did follow the instructions but the files did not reduce the steps needed to find relevant files. — [arXiv](https://arxiv.org/abs/2602.11988); [themoonlight review](https://www.themoonlight.io/review/evaluating-agentsmd-are-repository-level-context-files-helpful-for-coding-agents)
- The authors conclude that unnecessary requirements make tasks harder and that human-written files should describe only minimal requirements. — [arXiv](https://arxiv.org/abs/2602.11988)
- The IFScale benchmark (Distyl AI, July 2025) found that the best frontier models reach only about 68% accuracy at 500 simultaneous instructions, that models favour earlier instructions, and that failures are mostly omissions. — [arXiv 2507.11538](https://arxiv.org/abs/2507.11538); [Hugging Face](https://huggingface.co/papers/2507.11538)
- Vendor size guidance converges on short files: under 200 lines per CLAUDE.md, under 500 lines per Cursor rule, and a 32 KiB default cap in Codex. — [Claude Code](https://code.claude.com/docs/en/memory); [Cursor](https://cursor.com/docs/context/rules); [Codex](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

### Inferences
- All tools converge on the same three-layer model (central or org, repository, directory/glob-scoped) plus an on-demand layer (skills or manual rules), so an organization can write standards once and map them to each format, but each layer's precedence semantics differ by vendor.
- Only Cursor team rules (enforced), Claude Code managed CLAUDE.md and Copilot organization instructions offer a centrally controlled layer that developers cannot easily disable, and even these remain advisory to the model.
- The research evidence implies that rules files should hold short, non-obvious, high-value constraints, while procedural or rarely needed knowledge belongs in scoped rules or skills.

### Gaps
- I did not fetch the Gemini CLI (`GEMINI.md`) or Google Jules documentation, so their layering details are not verified here.
- I did not verify Kiro spec-driven development (requirements.md, design.md, tasks.md) from primary docs in this session.
- I did not find official Windsurf documentation for character limits, and the third-party sources conflict.
- I did not confirm the official Codex or Copilot skills paths from vendor documentation.

## 2. Architecture knowledge: ADRs, architecture-as-code, catalogs and API specs

### Takeaway
Architecture knowledge reaches agents through two routes: files in the repository that rules files reference (ADRs, OpenAPI specs, steering files) and MCP servers that expose catalogs and decision records. Backstage now ships an official MCP bridge, but ADR and architecture-as-code integrations are mostly small community projects.

### Cited Findings
- Kiro steering files can embed live workspace files through `#[[file:path]]` references, which lets a steering file pull in an API specification or architecture document so that it stays in sync with the source. — [Kiro docs](https://kiro.dev/docs/steering/)
- Kiro's default `structure.md` is meant to record file organization, naming and architectural patterns. — [Kiro docs](https://kiro.dev/docs/steering/)
- Backstage provides `@backstage/plugin-mcp-actions-backend`, which exposes actions registered in the Backstage Actions Registry (for example catalog actions) as MCP tools that AI clients can discover and call. — [Backstage API docs](https://backstage.io/api/stable/modules/_backstage_plugin-mcp-actions-backend.html); [Backstage MCP actions docs](https://backstage.io/docs/ai/mcp-actions)
- The Actions Registry does not enforce permissions automatically, so each action handler must perform its own authorization checks, and the registry is marked alpha in the Next docs. — [Backstage actions registry](https://backstage.io/docs/next/backend-system/core-services/actions-registry)
- Red Hat Developer Hub documents MCP tools for its Backstage-based product and states availability from Backstage 1.40, while a community guide places the Actions Registry in Backstage 1.49; the sources differ. — [Red Hat docs](https://docs.redhat.com/en/documentation/red_hat_developer_hub/1.8/html/interacting_with_model_context_protocol_tools_for_red_hat_developer_hub/assembly-model-context-protocol-tools); [dev.to](https://dev.to/x4nent/backstage-149-complete-guide-new-frontend-system-10-rc-by-default-actions-registry-and-1o5a)
- Spotify's commercial Portal for Backstage documents registering MCP tools. — [Spotify Portal docs](https://backstage.spotify.com/docs/portal/core-features-and-plugins/mcp/registering-tools)
- Community Backstage MCP servers (for example coderrob's) expose the Catalog API using `BACKSTAGE_BASE_URL` and a token. — [lobehub](https://lobehub.com/mcp/omtejedahumano-catalogo-software-mcp); [glama](https://glama.ai/mcp/servers/ldg4i99fgc)
- Cortex has an MCP server listed as giving programmatic access to its service catalog, scorecards and initiatives; this comes from a directory listing rather than Cortex documentation. — [agentpedia.codes](https://agentpedia.codes/mcp/cortex)
- Community ADR MCP servers exist: tosin2013/mcp-adr-analysis-server queries ADRs, validates decisions against code and detects drift, and AdrMcp (.NET) works on a repository's ADR folder and links ADRs to code. Both have small user bases. — [glama: mcp-adr-analysis-server](https://glama.ai/mcp/servers/tosin2013/mcp-adr-analysis-server); [glama: AdrMcp](https://glama.ai/mcp/servers/Atypical-Consulting/AdrMcp)
- Context7 (Upstash) is an MCP server that supplies version-specific library documentation through two tools (resolve a library ID, then query docs), hosted at mcp.context7.com. Sources disagree on private repository support, with most saying it requires a paid plan. — [GitHub upstash/context7](https://github.com/upstash/context7); [developersdigest](https://www.developersdigest.tech/mcp-servers/upstash-context7); contradicted by [dev.co](https://dev.co/ai/frameworks/context7)

### Inferences
- The service catalog is the most mature source of structured architecture metadata for agents (ownership, dependencies, APIs, scorecards), and the official Backstage MCP bridge makes it the most likely enterprise standard for this layer.
- ADRs and C4/Structurizr models are mostly delivered as repository files that a rules file references, because dedicated MCP tooling for them is immature.

### Gaps
- I found no primary documentation for a Port MCP server or for a Structurizr/C4 MCP server in this session.
- I found no primary evidence on how OpenAPI or AsyncAPI specs are exposed to agents beyond file references and generic MCP tooling.
- I found no published enterprise case study of an internal "golden path" MCP server.

## 3. Security policies: prompting versus enforcement

### Takeaway
Security prompting and rules files measurably reduce vulnerabilities but do not remove them, so vendors and researchers recommend pairing them with post-generation scanning run inside the agent loop (hooks, MCP) and in CI. Deterministic blocking belongs in permission settings and hooks rather than in instruction files.

### Cited Findings
- Veracode's 2025 GenAI Code Security Report tested over 100 LLMs on 80 tasks and found that AI-generated code introduced vulnerabilities (including OWASP Top 10 issues) in 45% of cases, that models chose the insecure option 45% of the time when offered a choice, and that security performance did not improve over time (vendor). — [Veracode press release](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/); [Veracode report](https://www.veracode.com/resources/genai-code-security-report/)
- In the Veracode report, Java had a 72% security failure rate, Python 38% and JavaScript 43% (vendor). — [Veracode report](https://www.veracode.com/resources/genai-code-security-report/)
- Bruni et al. (arXiv 2502.06039, 2025) found that a security-aware prompt prefix reduced vulnerabilities by up to 56% for GPT-4o and that Recursive Criticism and Improvement fixed up to 64.7%, while GPT-3.5-turbo barely responded. — [alphaxiv overview](https://alphaxiv.org/overview/2502.06039v1)
- Endor Labs (2 September 2026) summarizes studies showing a 77.5% reduction in weakness density from a secure-insecure diff pattern and 59 to 64% reductions from anti-pattern prompts, and cites Tony et al. (arXiv 2407.07064) as finding the security-expert persona produced the most weaknesses. — [Endor Labs](https://www.endorlabs.com/learn/prompt-patterns-that-make-coding-agents-write-safer-code)
- Endor Labs warns that AI code can become less secure with each iteration and recommends SAST, SCA and secrets scanning on all AI output; it reports that 34% of suggested dependency versions were hallucinated and that giving agents tools improved dependency safety threefold (vendor). — [Endor Labs](https://www.endorlabs.com/learn/prompt-patterns-that-make-coding-agents-write-safer-code)
- Backslash Security reports that naive prompts led all tested LLMs to produce code vulnerable to at least four of ten common CWEs, and that embedding security rules in prompts led all models to produce secure code; the methodology was not visible (vendor). — [Backslash Security](https://backslash.security/blog/harnessing-prompt-rules-for-secure-code-generation)
- Wiz published open-source baseline secure rules files (`wiz-sec-public/secure-rules-files`) on 6 June 2025 for Flask, Django, React, Node.js, Spring and ASP.NET Core, based on the CWE Top 25 and formatted for Cursor, Cline, CLAUDE.md, Windsurf, AGENTS.md, Aider and Copilot. — [Wiz blog](https://wiz.io/blog/safer-vibe-coding-rules-files)
- Wiz notes that rules files have not yet been broadly adopted for security, that they should be tailored to the organization, that they do not replace SAST, SCA, secrets scanning or PR review, and that it published no measured results for its own files. — [Wiz blog](https://wiz.io/blog/safer-vibe-coding-rules-files)
- Wiz cites BaxBench results showing that 25 to 70% of working outputs from leading models contain vulnerabilities. — [Wiz blog](https://wiz.io/blog/safer-vibe-coding-rules-files)
- Semgrep Guardian bundles the Semgrep MCP server, hooks and skills, scans each file an agent writes with Semgrep Code, Supply Chain and Secrets, and names Claude Code and Codex as primary targets. — [Semgrep Guardian docs](https://docs.semgrep.dev/guardian)
- Guardian does not block code; it returns findings to the agent and prompts regeneration, and the hosted Claude Code and Codex plugins use a fixed ruleset that does not apply organization policies, while local CLI integrations do. — [Semgrep Guardian docs](https://docs.semgrep.dev/guardian)
- Semgrep also provides a standalone MCP server for on-demand scans. — [Semgrep MCP docs](https://semgrep.dev/docs/mcp)
- Claude Code documents PreToolUse hooks and managed `permissions.deny` and sandbox settings as the mechanisms for technical enforcement, with CLAUDE.md reserved for guidance. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- A 2026 cross-model study (arXiv 2607.20713) states that whether security-aware prompting prevents vulnerabilities from appearing is still an open question, and its own analysis used static review only. — [arXiv 2607.20713](https://arxiv.org/pdf/2607.20713)

### Inferences
- Prompting reduces the rate of vulnerabilities at the source, which lowers scanner noise and rework, but every source treats scanning as mandatory, so a defensible design uses three layers: rules files for guidance, in-loop scanning via hooks or MCP for fast feedback, and CI gates for enforcement.
- Feedback-style tools such as Guardian leave the final decision to the agent, so organizations that need a hard guarantee still need a blocking gate in CI or a pre-commit hook.

### Gaps
- I found no primary source in this session describing OPA/Rego policy-as-code applied directly to agent actions.
- I did not fetch CodeQL or Snyk agent-integration documentation, so their in-loop capabilities are not recorded here.
- Most effect-size figures come from single studies or vendors, and I found no independent replication across agents.

## 4. Central and enterprise distribution, and keeping documents current

### Takeaway
Central distribution is done through vendor-managed org layers (Cursor team rules, Copilot organization instructions, Claude Code managed CLAUDE.md, Kiro global steering via MDM), shared repositories linked by symlink or import, and MCP servers. Keeping instructions current is mostly a manual review process, although Claude Code now ships an automated audit for conflicting or stale instructions.

### Cited Findings
- Cursor admins can create team rules in a dashboard and enforce them so users cannot disable them. — [Cursor docs](https://cursor.com/docs/context/rules)
- Copilot organization instructions are set in organization settings and apply on GitHub.com Chat, cloud agent and code review. — [GitHub docs](https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions); [GitHub support matrix](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- Claude Code supports a managed CLAUDE.md distributed via MDM, Group Policy or Ansible, or embedded in managed settings. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Kiro supports pushing global steering through MDM or Group Policy, or pulling it from a central repository. — [Kiro docs](https://kiro.dev/docs/steering/)
- Claude Code supports symlinking a shared standards repository into `.claude/rules/`, but symlinks pointing outside the working directory require a one-time approval and network paths are not followed. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- In monorepos, `claudeMdExcludes` lets developers skip other teams' CLAUDE.md files by glob, and arrays merge across settings layers. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Anthropic warns that if two instructions contradict each other, Claude may pick one arbitrarily, that user-level and project rules do not override each other, and that files should be reviewed periodically. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Claude Code provides `/doctor prompt-audit`, which checks CLAUDE.md, AGENTS.md, rules, skills and subagents for instructions written for older models, references to files or commands that no longer exist, and contradictions between files, and proposes edits. — [Claude Code memory docs](https://code.claude.com/docs/en/memory)
- Cross-tool configuration generators exist that compile one canonical rule set into each vendor's format (for example agentsmesh and agent-policy). — [agentsmesh](https://samplexbro.github.io/agentsmesh/canonical-config/rules/); [agent-policy](https://cameronbrooks11.github.io/agent-policy/reference/targets/windsurf-rules)
- Codex builds its instruction chain once per session, so updated files take effect only after a restart. — [OpenAI Codex docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

### Inferences
- Because AGENTS.md is read by nearly every tool, the lowest-maintenance pattern is a single canonical AGENTS.md (or a generator that emits it) with vendor-specific files importing or symlinking it.
- Live sources such as MCP servers and file references to specs avoid copy drift, while copied text in rules files must be reviewed whenever the underlying standard changes.

### Gaps
- I found no quantitative evidence on how often enterprise instruction files go stale or conflict.
- I found no published enterprise case study, with named companies, of a shared instruction repository or an internal standards MCP server; reports of such setups were anecdotal or vendor marketing.
