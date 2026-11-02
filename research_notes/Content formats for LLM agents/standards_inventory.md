# Standards and specifications for making content consumable by LLMs and agents

Status labels used throughout, applied as of 2 November 2026:

- **Formal standard** means a document approved by a recognised standards body (ISO, IEC, IEEE, W3C, OASIS, Ecma, or an IETF standards-track RFC).
- **Foundation-hosted open specification** means a specification under neutral foundation governance that has not passed a standards-body approval process. This label is my own distinction, and it covers the Agentic AI Foundation (AAIF) projects.
- **Government specification** means a specification published by a government agency such as NIST.
- **Vendor specification** means a format defined and controlled by one company.
- **Community convention** means a format with no controlling body, or one maintained by individuals or a volunteer project.
- **Proposal or draft** means a document that has not reached a stable release.

## Agent-facing content conventions

### Takeaway
No formal standard from a standards body exists for agent-facing content. The nearest things are AAIF-hosted open specifications (AGENTS.md, Agent Skills, MCP, A2A), and the only standards-track work is IETF AIPREF, which covers usage preferences rather than content format and is still at draft stage. Major providers have made no public commitment that their crawlers use llms.txt, and the measured traffic is small, with coding agents as the most visible genuine consumers.

### Cited Findings

**llms.txt**

- **Owner and status:** It is a community convention and proposal authored by Jeremy Howard, and the site names no standards body. The page calls itself "an informal overview" and says the specification is "open for community input" — [llmstxt.org](https://llmstxt.org/).
- **Version and date:** It was published on 3 September 2024 and modified on 10 August 2026, and the current text is v2 of the proposal — [llmstxt.org](https://llmstxt.org/).
- **Format and scope:** It is a Markdown file at a site root or subpath. Only an H1 with the project name is required, and a blockquote summary, detail paragraphs, and H2 link lists are optional — [llmstxt.org](https://llmstxt.org/).
- **Publishing adoption:** Ahrefs found that 28% of 137,210 domains in its analytics product publish a file, and Ahrefs treats this figure as an upper bound because its customers skew technical and SEO-aware — [Ahrefs, 15 June 2026](https://ahrefs.com/blog/llmstxt-study/).
- **A lower publishing figure from another population:** A log audit of Adobe Experience Manager customers found that 137 of 4,685 probed hosts returned HTTP 200, and only 20 returned non-empty plain text — [Longato, June 2026](https://www.longato.ch/llmstxt-2026-june/).
- **Limitation:** The format has no schema or validation requirement beyond the H1, and it carries no provider commitment to read it — [llmstxt.org](https://llmstxt.org/).

**Do major LLM providers consume llms.txt?**

- **Google, stated position:** Gary Illyes reportedly said at a Search Central Live event that Google does not support llms.txt and does not plan to — [Search Engine Roundtable, 24 July 2025](https://www.seroundtable.com/openai-crawling-Ilms-txt-files-39811.html).
- **Google, hosted file:** John Mueller answered "no" when asked whether Google's llms.txt on ai.google.dev was an endorsement — [Search Engine Roundtable, 20 January 2026](https://www.seroundtable.com/google-does-not-endorse-llms-txt-40789.html).
- **Google, mixed signal:** Chrome's Lighthouse documentation calls llms.txt an "emerging convention", treats a missing file as Not Applicable, and tells site owners how to create one — [Chrome for Developers](https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt). Google Search and Chrome are therefore saying different things.
- **Ahrefs request data:** 97% of the roughly 38,000 published files received no requests in May 2026, and the rest received roughly 22,000 requests in total — [Ahrefs](https://ahrefs.com/blog/llmstxt-study/).
- **Ahrefs bot shares:** AI bots made up 19.5% of those requests, divided into agents and agentic infrastructure at 10.5%, training crawlers at 5.3%, assistants at 2.5%, and retrieval bots at 1.1% — [Ahrefs](https://ahrefs.com/blog/llmstxt-study/).
- **Ahrefs named agents:** GPTBot was the largest single AI fetcher at 4.51%, ClaudeBot had 0.8%, and OAI-SearchBot had 0.74%. Claude-Code fetched more than any AI retrieval bot, assistant, or training crawler except GPTBot and statespace-indexer — [Ahrefs](https://ahrefs.com/blog/llmstxt-study/).
- **Ahrefs on Google:** Googlebot fetched the files about 900 times, which Ahrefs attributes to routine crawling rather than interest in the file — [Ahrefs](https://ahrefs.com/blog/llmstxt-study/).
- **Adobe Experience Manager log data:** Out of 22,494 hits in a 30-day window, verifiable LLM or AI agents accounted for 258 (1.1%), and 92.2% came from other or unverified agents. Named counts included OpenAI at 242 including GPTBot, Anthropic's ClaudeBot at 10, and Perplexity at 5 — [Longato](https://www.longato.ch/llmstxt-2026-june/).
- **Adobe Experience Manager, routing evidence:** No logged request had an llms.txt URL as its referrer, so the data shows no observable routing from the file to pages. The author notes that this does not prove that no provider crawls from it — [Longato](https://www.longato.ch/llmstxt-2026-june/).
- **Measurement limit:** Both studies measure requests and not model use, and both authors say so — [Ahrefs](https://ahrefs.com/blog/llmstxt-study/); [Longato](https://www.longato.ch/llmstxt-2026-june/).
- **Anecdote:** An SEO practitioner reported OpenAI polling his files every 15 minutes, and the report contains no OpenAI statement — [Search Engine Roundtable](https://www.seroundtable.com/openai-crawling-Ilms-txt-files-39811.html).
- **Anthropic as a publisher:** An Anthropic engineering post says LLM-friendly documentation is commonly found in flat llms.txt files — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents). Claude Code's documentation points agents to its own index in a page header — [Claude Code docs](https://code.claude.com/docs/en/memory). Publishing a file is not evidence that a crawler consumes other sites' files.

**AGENTS.md**

- **Owner and status:** It is a foundation-hosted open specification, stewarded by AAIF under the Linux Foundation — [agents.md](https://agents.md/). OpenAI contributed it as a founding project on 9 December 2025 — [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation).
- **Version and format:** No version is listed. It is plain Markdown with no required fields or schema, and the nearest file in the directory tree takes precedence — [agents.md](https://agents.md/).
- **Adoption:** The site claims use by over 60,000 open-source projects and lists tools including Codex, Jules, Cursor, Gemini CLI, Copilot coding agent, Windsurf, Devin, and Zed — [agents.md](https://agents.md/). The 60,000 figure is self-reported and also appears in the December 2025 press release, so it may be stale — [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation).
- **Limitation:** It defines location and precedence but not content structure, so conformance cannot be validated beyond the file's existence — [agents.md](https://agents.md/).

**Agentic AI Foundation**

- **Formation:** The Linux Foundation announced AAIF on 9 December 2025 with MCP, goose, and AGENTS.md. Platinum members are AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI — [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation).
- **Current projects:** AAIF now lists ten projects, namely Agent Router, Agent Skills, A2A, AGENTS.md, agentgateway, goose, MCP, Open Responses, OpenEnv, and OpenSandbox — [AAIF](https://aaif.io/projects/).

**Agent Skills and SKILL.md**

- **Owner and status:** It is a foundation-hosted open specification. Anthropic developed it and announced on 22 October 2026 that it was donating the standard, name, logo, GitHub organisation, and domain to AAIF — [Anthropic](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation).
- **Version:** The repository shows no versioned releases — [GitHub](https://github.com/agentskills/agentskills). Versioned releases and a formal proposal process are on the proposed roadmap — [Anthropic](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation).
- **Format:** A skill is a directory with a `SKILL.md` file that has YAML frontmatter and a Markdown body. `name` and `description` are required, `license`, `compatibility`, and `metadata` are optional, and `allowed-tools` is experimental — [agentskills.io](https://agentskills.io/specification).
- **Progressive disclosure:** The specification defines three loading tiers, which are about 100 tokens of metadata, an instruction body of under 5,000 tokens, and resources on demand — [agentskills.io](https://agentskills.io/specification).
- **Validation:** A reference validator named `skills-ref` checks frontmatter and naming — [agentskills.io](https://agentskills.io/specification).
- **Adoption:** Anthropic claims more than 70 integrating platforms, including ChatGPT, Cursor, GitHub Copilot, and VS Code, about 1 million published skills, and nearly 280 million installs — [Anthropic](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation). These are the donor's own figures.
- **Limitation:** The body has no format restrictions, so only the frontmatter is machine-checkable — [agentskills.io](https://agentskills.io/specification).

**CLAUDE.md**

- **Owner and status:** It is a vendor specification documented by Anthropic for Claude Code, and it has no published independent specification that I could find — [Claude Code docs](https://code.claude.com/docs/en/memory).
- **Format:** It is a Markdown file with `@path` imports up to four hops deep. Path-scoped rules live in `.claude/rules/` with `paths:` frontmatter — [Claude Code docs](https://code.claude.com/docs/en/memory).
- **AGENTS.md interoperation:** Claude Code v2.1.277 and later reads `AGENTS.md` when no `CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or above it, and it reads only the `CLAUDE.md` files if both exist — [Claude Code docs](https://code.claude.com/docs/en/memory).
- **Limitation:** The documentation says Claude treats these files as context and not as enforced configuration — [Claude Code docs](https://code.claude.com/docs/en/memory).
- **Adoption beyond Anthropic:** GitHub Copilot also accepts a single root `CLAUDE.md` or `GEMINI.md` as agent instructions — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions).

**Cursor rules**

- **Owner and status:** It is a vendor specification owned by Cursor — [Cursor docs](https://cursor.com/docs/context/rules).
- **Format:** Rules are `.mdc` files in `.cursor/rules` with `description`, `globs`, and `alwaysApply` frontmatter, and a plain `.md` file in that directory is ignored — [Cursor docs](https://cursor.com/docs/context/rules).
- **AGENTS.md interoperation:** Cursor also supports `AGENTS.md`, including nested files, as a simpler alternative — [Cursor docs](https://cursor.com/docs/context/rules).
- **Limitation:** The `.mdc` format is not portable to other tools on the evidence I found, because I found no other vendor documenting support for it.

**GitHub Copilot instructions**

- **Owner and status:** It is a vendor specification owned by GitHub — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions).
- **Format:** It uses `.github/copilot-instructions.md` and `.github/instructions/NAME.instructions.md` with `applyTo` globs and an optional `excludeAgent` key, and it also reads `AGENTS.md` — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions).
- **Limitation:** Path-specific instructions on GitHub.com currently work only with the cloud agent and code review — [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions).

**MCP resources and prompts**

- **Owner and status:** MCP is a foundation-hosted open specification. Anthropic contributed it to AAIF at the December 2025 launch — [Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation).
- **Version:** The current revision found is 2026-07-28, which GitHub lists as a tagged release — [GitHub release](https://github.com/modelcontextprotocol/specification/releases/tag/2026-07-28); [changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog).
- **Resources:** In revision 2025-11-25, a resource has a URI, a name, an optional `mimeType`, and optional annotations for `audience`, `priority`, and `lastModified` — [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/resources).
- **Changes in 2026-07-28:** `subscriptions/listen` replaces `resources/subscribe`, list and read results must carry `ttlMs` and `cacheScope`, and the resource-not-found error code changes to `-32602` — [changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog).
- **Limitation:** MCP defines how content is transported and annotated, and hosts decide how to use it, because resources are "application-driven". It does not specify what makes a document well structured for a model — [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/resources).

**NLWeb**

- **Owner and status:** It is a proposal with a Python reference implementation under the `nlweb-ai` GitHub organisation, MIT-licensed, with no entries in its Releases section. Third-party material describes it as a Microsoft announcement at Build 2025 with "proposed" status — [GitHub](https://github.com/nlweb-ai/NLWeb); [VIPS reference page](https://learn.engineering.vips.edu/agent-protocols/nlweb-protocol).
- **Format and scope:** It defines a natural-language `ask` method returning JSON structured with Schema.org vocabulary, and each instance acts as an MCP server — [GitHub](https://github.com/nlweb-ai/NLWeb).
- **Adoption evidence:** The repository has about 6,300 stars and 694 forks, which show interest rather than production use — [GitHub](https://github.com/nlweb-ai/NLWeb).

**Agent2Agent (A2A)**

- **Owner and status:** It is a foundation-hosted open specification and an AAIF project — [AAIF](https://aaif.io/projects/). Google originated it, and the Linux Foundation already hosted it before the AAIF move — [PureAI, 23 June 2025](https://pureai.com/Articles/2025/06/23/Linux-Foundation-Adopts-Google-Backed-Protocol-for-AI-Agent-Interoperability.aspx).
- **AAIF move date:** The move was reported on 17 August 2026 — [Axios](https://axios.com/2026/08/17/a2a-agentic-ai-foundation-open-ai-standards). The project's own blog link is dated 27 August 2026, so the sources differ by ten days — [A2A specification page](https://a2a-protocol.org/latest/specification/).
- **Version:** The latest version is 1.0.0, and `spec/a2a.proto` is the normative definition — [A2A specification](https://a2a-protocol.org/latest/specification/). The 1.0 release date conflicts across secondary sources. One reports January 2026 — [Jacar](https://jacar.es/?p=204). A search summary of the AAIF coverage gave March 2026, and I could not trace that to a specific page.
- **Scope:** It specifies agent-to-agent communication, including an Agent Card JSON metadata document and `Part` content containers for text, files, and structured data — [A2A specification](https://a2a-protocol.org/latest/specification/).
- **Limitation:** It is a protocol for exchanging tasks and is not an authoring format for knowledge content — [AAIF](https://aaif.io/projects/).

**Content negotiation for Markdown (`Accept: text/markdown`)**

- **Underlying standard:** RFC 7763 registers `text/markdown` with a `variant` parameter and a variants registry. It is an Informational RFC from March 2016, and it is explicitly not standards track — [RFC 7763](https://www.rfc-editor.org/info/rfc7763).
- **Status of the pattern:** It is a community convention built on ordinary HTTP negotiation. I found no specification defining how agent-oriented Markdown responses should behave.
- **Cloudflare implementation:** Markdown for Agents is a vendor feature announced in February 2026 — [Cloudflare changelog](https://developers.cloudflare.com/changelog/2026-02-12-markdown-for-agents). It converts HTML at the edge, sets `Vary: Accept`, and emits optional YAML frontmatter and JSON-LD in a fenced block — [Cloudflare docs](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/). Search snippets gave a 2 MB origin limit, whereas the current page gives 6 MiB, so the limit appears to have changed.
- **Other adopter:** HackMD returns Markdown when `text/markdown` has higher priority than `text/html` — [HackMD](https://hackmd.io/blog/2026/03/22/agentic-workflow-2026).
- **Client adoption:** A February 2026 test found that Claude Code, Cursor, and OpenCode request Markdown first, while Codex, Gemini CLI, Copilot, and Windsurf do not — [Checkly](https://www.checklyhq.com/blog/state-of-ai-agent-content-negotation/).
- **Conflict on Claude Code:** A Claude Code feature request mirrored by a third party stated that WebFetch did not send the header — [claudeissues.com](https://claudeissues.com/issue/41097-feature-request-webfetch-should-follow-link-rel-alternate-type-text-markdown-and). This conflicts with Checkly's capture, and I could not resolve the difference.

**IETF AI preferences (AIPREF)**

- **Owner and status:** It is an IETF working group with two active Internet-Drafts intended as Proposed Standards, and neither is an RFC yet — [IETF Datatracker](https://datatracker.ietf.org/wg/aipref/documents/).
- **Versions:** `draft-ietf-aipref-vocab-08` is dated 13 September 2026, and `draft-ietf-aipref-attach-05` is dated 18 August 2026 — [IETF Datatracker](https://datatracker.ietf.org/wg/aipref/documents/).
- **Scope:** The vocabulary defines `train-ai`, `ai-use`, and `search` preference categories — [draft-ietf-aipref-vocab](https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/). The attach draft associates preferences with content in HTTP — [IETF Datatracker](https://datatracker.ietf.org/wg/aipref/documents/).
- **Related vendor framework:** Cloudflare's Markdown responses default to `content-signal: ai-train=yes, search=yes, ai-input=yes` unless the origin sets a value, and they link to Content Signals — [Cloudflare docs](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/).

### Inferences
- The accurate answer to "is there a standard for agent-facing content?" is no formal standard, with a small set of foundation-hosted specifications converging quickly. Calling AGENTS.md or Agent Skills an "industry standard" overstates their status, even though their adoption is real, because AAIF hosting is neutral governance and not standards-body approval.
- The most portable instruction layer today is `AGENTS.md`, since Cursor, Copilot, and Claude Code all document reading it, though each tool applies its own precedence rules.
- llms.txt evidence points to on-demand use by coding agents and people directing agents to the file, rather than systematic use by search or training crawlers. This is my reading of the category split, and the studies measure requests and not use.
- The Ahrefs and Adobe totals of about 22,000 requests are from different datasets, and their similarity appears to be coincidental. The two 1.1% figures also measure different categories.

### Gaps
- I found no official statement from OpenAI, Anthropic, Perplexity, or Meta committing their crawlers to using, or not using, llms.txt.
- No study I found measures whether llms.txt improves answer quality or citation rates under controlled conditions.
- I did not read the MCP 2026-07-28 prompts page or confirm that the resource annotations are unchanged in that revision. The changelog lists no annotation change.
- The nlweb.ai/spec page failed with a certificate error, so NLWeb's specification version and date are unverified.
- The owner, governance, and relationship to AIPREF of Content Signals could not be established because contentsignals.org returned no usable text.
- The current status of the legacy `.cursorrules` file is not stated on the Cursor page I read.
- Vercel's support for Markdown negotiation was reported only by a secondary source and is unconfirmed.

## Markup and data formats

### Takeaway
The only formal standards in this group are JSON-LD (W3C), DITA 1.3 (OASIS), and the YAML media type registration (IETF, if confirmed as standards track). CommonMark, GFM, Schema.org, reStructuredText, and TOON are not standards-body products, and YAML frontmatter has no specification at all, even though most agent formats depend on it.

### Cited Findings

**CommonMark**

- **Owner and status:** It is a community convention credited to John MacFarlane under CC BY-SA 4.0, and the page names no standards body — [CommonMark](https://spec.commonmark.org/).
- **Version:** The latest version is 0.31.2, dated 28 January 2024 — [CommonMark](https://spec.commonmark.org/).
- **Limitation:** The version number remains below 1.0, and the specification does not cover metadata blocks, which is a gap that frontmatter fills by convention.

**GitHub Flavored Markdown**

- **Owner and status:** It is a vendor specification published on a GitHub domain — [GFM](https://github.github.com/gfm/).
- **Version:** The current version is 0.29-gfm, dated 6 April 2019, which is a strict superset of CommonMark that adds tables, task lists, strikethrough, extended autolinks, and disallowed raw HTML — [GFM](https://github.github.com/gfm/).
- **Limitation:** It tracks CommonMark 0.29, which is older than the current CommonMark release — [CommonMark](https://spec.commonmark.org/).

**YAML frontmatter**

- **Status:** No formal standard exists. The result of my search is that the practice is a de facto convention popularised by Jekyll, and a Stack Overflow discussion reaches the same conclusion — [Jekyll docs](https://jekyllrb.com/docs/front-matter/); [Stack Overflow archive](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/27838730/is-there-a-yaml-front-matter-standard-validator).
- **Closest definition:** Jekyll requires a YAML block between triple-dashed lines as the first thing in the file, and the page cites no formal specification beyond the YAML website — [Jekyll docs](https://jekyllrb.com/docs/front-matter/).
- **Adjacent standards that do not cover it:** RFC 7763 does not mention frontmatter — [RFC 7763](https://www.rfc-editor.org/info/rfc7763). The IETF YAML media-type draft registers `application/yaml` and does not address frontmatter — [IETF Datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-yaml-mediatypes/10/).
- **Dependants:** Agent Skills requires it, and Cursor rules, Copilot path instructions, Claude Code rules, and MADR all use it, each with its own fields — [agentskills.io](https://agentskills.io/specification); [Cursor docs](https://cursor.com/docs/context/rules); [GitHub Docs](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions); [Claude Code docs](https://code.claude.com/docs/en/memory); [MADR](https://adr.github.io/madr/).

**JSON Schema**

- **Owner and status:** It is a community specification under the OpenJS Foundation and is not a formal standard. Its releases were published as Internet-Drafts, and the project is decoupling the main specification from the IETF to self-publish it — [JSON Schema blog](https://json-schema.org/blog/posts/future-of-json-schema).
- **Version:** The current version is 2020-12 — [JSON Schema](https://json-schema.org/specification).
- **Adoption:** MCP allows any JSON Schema 2020-12 keywords in tool schemas — [MCP changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog). TypeSpec emits JSON Schema 2020-12 — [TypeSpec](https://typespec.io/).
- **Limitation:** It validates JSON-shaped data and does not address prose documents.

**JSON-LD and Schema.org**

- **JSON-LD:** JSON-LD 1.1 is a formal standard, namely a W3C Recommendation dated 16 July 2020 — [W3C](https://www.w3.org/TR/json-ld11/).
- **Schema.org:** It is a community-maintained vocabulary and is not a standards-body product on the evidence I gathered. The latest version is 30.1, dated 16 September 2026 — [Schema.org releases](https://schema.org/docs/releases.html).
- **AI relevance:** NLWeb uses Schema.org as its semantic layer — [GitHub](https://github.com/nlweb-ai/NLWeb). Cloudflare preserves JSON-LD in its Markdown output — [Cloudflare docs](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/). Schema.org's release notes mention generative AI only in connection with a digital source type vocabulary in version 24.0 — [Schema.org releases](https://schema.org/docs/releases.html).

**AsciiDoc**

- **Owner and status:** The AsciiDoc Language is an incubating specification project at the Eclipse Foundation, tied to the AsciiDoc working group. The project page shows no released version — [Eclipse Foundation](https://projects.eclipse.org/projects/asciidoc.asciidoc-lang).
- **Limitation:** A specification project is underway, but I could not confirm a ratified specification.

**DITA**

- **Owner and status:** DITA 1.3 is a formal OASIS Standard, and Errata 02 was approved on 29 June 2018 — [OASIS DITA TC](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita).
- **DITA 2.0:** I found no evidence that it has been approved as an OASIS Standard. The cover page cites a working draft — [dita-lang.org](https://dita-lang.org/2.0/dita/resources/oasis-cover). DITA Open Toolkit 4.4 describes "preview support" following OASIS drafts — [DITA-OT](https://www.dita-ot.org/4.4/reference/dita-v2-0-support). A TC member nonetheless noted that new adopters already use 2.0 — [TC minutes, February 2026](https://groups.oasis-open.org/discussion/dita-tc-minutes-17-february-2026-uploaded).
- **OASIS and AI:** I found no OASIS DITA specification or subcommittee on AI. AI appears as a discussion topic in TC minutes, including an internal LLM connected to an authoring tool and about 13 trial use cases, plus a governance question about keeping an LLM current as content changes — [February 2026 minutes](https://groups.oasis-open.org/discussion/dita-tc-minutes-17-february-2026-uploaded); [March 2026 minutes](https://groups.oasis-open.org/discussion/dita-tc-minutes-17-march-2026-uploaded?hlmlt=VT).
- **Limitation:** It requires XML tooling and a specialised authoring discipline, and agents do not read it natively according to any evidence I found.

**reStructuredText**

- **Owner and status:** It is a community convention specified as part of the Docutils project, with no claimed standards-body status — [Docutils](https://docutils.sourceforge.io/rst.html).
- **Version:** The page gives no specification revision and is dated 13 September 2025 — [Docutils](https://docutils.sourceforge.io/rst.html).

**TOON**

- **Owner and status:** It is a proposal from the `toon-format` organisation, and the MIT licence names Johann Schopplich. Version 4.4 is labelled a "Working Draft", and the `text/toon` media type is marked provisional — [TOON specification](https://github.com/toon-format/spec).
- **Scope:** It is a line-oriented, indentation-based encoding of the JSON data model, with tabular forms for uniform arrays — [TOON specification](https://github.com/toon-format/spec).
- **Claims:** The project reports about 32.7% fewer tokens than formatted JSON on mixed data, about 1.6% more than compact JSON, and 72.2% against 71.4% retrieval accuracy against JSON — [TOON repository](https://github.com/toon-format/toon).
- **Limitations:** The benchmarks are the project's own and many confidence intervals overlap. The project says compact JSON often wins for deeply nested or non-uniform data and CSV is smaller for purely tabular data — [TOON repository](https://github.com/toon-format/toon).

### Inferences
- Frontmatter is the largest unstandardised dependency in the agent ecosystem. Tools that share the syntax do not share field semantics, so a file is not portable merely because it has frontmatter.
- A Markdown document that targets agents should use the CommonMark or GFM subset, since neither those specifications nor RFC 7763 confer any formal semantic guarantee on structure.
- TOON is an optimisation for structured data sent to models and is not a content authoring standard. Its results should not be relied on until independently replicated.

### Gaps
- I did not confirm RFC 9512's final status from a primary source, because the search result was the draft page.
- I did not find controlled evidence on whether Schema.org or JSON-LD markup improves LLM retrieval.
- The YAML 1.2 specification's own governance was not researched.
- The approval status of DITA 2.0 needs direct confirmation from OASIS, because the standard's page URL I tried returned 404 and the TC page does not mention it.

## ADR and architecture formats

### Takeaway
No formal standard defines an ADR format, and the only formal standard in this group, ISO/IEC/IEEE 42010, explicitly leaves format open. I found no published JSON Schema for any ADR format, so MADR's frontmatter is the most structured ADR option, while Structurizr and Backstage are the architecture-adjacent options with machine-readable structure.

### Cited Findings

- **Nygard ADR:** It is a community convention from a blog post by Michael Nygard dated 15 November 2011. It specifies Title, Context, Decision, Status, and Consequences sections in a short text file, in Markdown or Textile, numbered sequentially. It has no schema — [Cognitect](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).
- **MADR:** It is a community convention from the ADR GitHub organisation. Version 4.0.0 is dated 17 September 2024 — [MADR](https://adr.github.io/madr/).
- **MADR format:** It is Markdown with required context, considered options, and decision outcome sections. Optional frontmatter provides `status`, `date`, `decision-makers`, `consulted`, and `informed`. The page mentions no JSON Schema — [MADR](https://adr.github.io/madr/).
- **Y-statements:** It is a community convention, a sentence-pattern format attributed to the Zdun et al. "Sustainable Architectural Decisions" article. It has no machine-readable schema that I could find — [ADR organisation](https://adr.github.io/).
- **arc42:** It is a community template created by Peter Hruschka and Gernot Starke with 12 sections under CC BY-SA 4.0. The overview page mentions no schema and states no version — [arc42](https://arc42.org/overview).
- **C4 model:** It is a community convention created by Simon Brown. It describes itself as notation and tooling independent and does not claim to be a formal standard — [C4 model](https://c4model.com/).
- **Structurizr DSL:** It is a vendor or project-owned text format that defines a software architecture model based on C4, and it includes an ADR "Decisions" topic and "DSL vs JSON" workspace documentation in its navigation — [Structurizr docs](https://docs.structurizr.com/dsl).
- **ISO/IEC/IEEE 42010:2022:** It is a formal standard, and its current edition was published in November 2022 — [ISO](https://www.iso.org/standard/74393.html). Catalogue extracts state that it "does not specify any format or media for recording an AD", nor any notation or tools — [iTeh catalogue](https://iteh.es/catalog/standards/iso/5fed7736-385f-477c-9133-5ba449a3c3b8/iso-iec-ieee-42010-2022).
- **Backstage catalog-info:** It is a project specification with a YAML descriptor containing `apiVersion`, `kind`, `metadata`, and `spec`, where most kinds use `backstage.io/v1alpha1`. The alpha and beta versions signal that the format may change. The site's footer links to CNCF Incubation — [Backstage](https://backstage.io/docs/features/software-catalog/descriptor-format).
- **TechDocs:** It is Backstage's docs-as-code system using Markdown stored with the code and rendered as a site, with generation through a CLI and a container — [Backstage TechDocs](https://backstage.io/docs/features/techdocs/).
- **adr-tools:** It is a community command-line tool that manages Markdown ADRs, including supersession through `adr new -s`. It has about 5,800 stars and no schema — [GitHub](https://github.com/npryce/adr-tools).
- **Log4brains:** It is a community tool that uses MADR as its default template and builds a static site, and its page mentions no structured export such as JSON — [GitHub](https://github.com/thomvaill/log4brains).

### Inferences
- ADR formats are machine-parseable only by convention, through predictable headings and optional frontmatter. A team wanting validated ADRs would need to write its own schema or linter.
- Structured status and supersession fields are the features most relevant to agents because they let an agent identify the current decision, and MADR's frontmatter is the closest published form of this. This relevance is my judgement and is not a finding from the sources.
- ISO 42010 is relevant as conceptual vocabulary, such as viewpoints and model kinds, and cannot serve as a format choice.

### Gaps
- The published Structurizr JSON schema could not be verified, because the `docs.structurizr.com/json` page returned 404.
- I did not verify whether Backstage publishes a JSON Schema for its entity descriptors, as the descriptor page does not mention one.
- The `backstage.io/techdocs-ref` annotation and MkDocs dependency were not confirmed on the page read.
- Last-activity dates for adr-tools and Log4brains are unavailable, because the GitHub API was blocked by this environment's sandbox and the pages showed no dates.

## Security and policy formats

### Takeaway
This is the most formally standardised group, with OSCAL mandated in US federal practice and SARIF, CSAF, STIX, CycloneDX, and SPDX tied to standards bodies. None of them was designed for LLMs, and ISO 27001 does not mandate any format according to secondary sources.

### Cited Findings

**NIST OSCAL**

- **Owner and status:** It is a government specification led by NIST, with machine-readable formats in XML, JSON, and YAML — [NIST](https://pages.nist.gov/OSCAL/).
- **Version:** The latest release is v1.2.3, with asset timestamps of 7 August 2026, and it is mainly a dependency and security-fix patch — [GitHub releases](https://github.com/usnistgov/OSCAL/releases).
- **Version conflict:** MeriTalk reports a forthcoming version 1.4 and a prior 1.3 patch from November 2024, which does not match the GitHub tags — [MeriTalk](https://www.meritalk.com/tag/oscal/). I treat the GitHub release list as authoritative.
- **Models:** The control layer has Catalog, Profile, and Control Mapping. The implementation layer has SSP and Component Definition. The assessment layer has Assessment Plan, Assessment Results, and POA&M. All are listed as released — [NIST](https://pages.nist.gov/OSCAL/learn/concepts/layer/).
- **Federal mandate:** FedRAMP's Consolidated Rules for 2026 quote OMB M-24-15. Footnote 4 names OSCAL as the standard machine-readable format until NIST designates a successor, and PDFs and Word files do not count as machine-readable — [FedRAMP](https://www.fedramp.gov/2026/authority/m-24-15/automation/).
- **RFC-0024:** The FedRAMP page for this RFC, on Rev5 machine-readable packages, still shows it as a proposal. It would require new packages in an approved machine-readable format, with most rules effective on 30 September 2026 and a grace period ending on 30 September 2027. OSCAL stays on the approved list while maintained, and other public formats can be added — [FedRAMP RFC-0024](https://www.fedramp.gov/rfcs/0024/).
- **Scope as vendors describe it:** Two vendors say the requirement covers all Rev5 assessments, with new packages from 30 September 2026, existing authorisations at their next annual assessment, and enforcement from 30 September 2027 — [ActiveState](https://www.activestate.com/blog/your-compliance-team-just-handed-engineering-a-new-deliverable-its-called-oscal); [Paramify](https://www.paramify.com/blog/oscal-ssp). See the Gaps below for a conflicting report that the scope was later narrowed.
- **Direction of FedRAMP:** The Cloud Security Alliance says the Consolidated Rules were published on 25 June 2026, replace narrative SSPs and POA&Ms with machine-readable evidence as primary artefacts, stop new Rev5 applications on 11 June 2027, and end Rev5 authorisations on 31 December 2028 — [CSA](https://labs.cloudsecurityalliance.org/research/csa-research-note-fedramp-20x-consolidated-rules-transition/).
- **Adoption example:** The Department of Veterans Affairs reported being the first federal agency to submit an OSCAL SSP to GSA — [MeriTalk](https://www.meritalk.com/?p=204188).

**Policy and detection languages**

- **OPA and Rego:** It is a foundation-hosted language, and OPA reached CNCF Graduated status on 29 January 2021 — [CNCF](https://www.cncf.io/projects/open-policy-agent-opa/). Rego is a declarative Datalog-inspired language, defined by a policy reference with a grammar rather than a standards-body specification — [OPA docs](https://www.openpolicyagent.org/docs/policy-language).
- **Cedar:** It is a CNCF Sandbox project that originated at AWS, with Apache-2.0 licensing and JSON entities — [AWS](https://aws.amazon.com/blogs/opensource/cedar-joins-cncf-as-a-sandbox-project); [GitHub](https://github.com/cedar-policy/cedar). Its authorization engine and validator are modelled in Lean, and key properties are proved — [AWS](https://aws.amazon.com/jp/blogs/opensource/lean-into-verified-software-development/).
- **Sigma:** It is a community convention owned by SigmaHQ, with Markdown specifications for rules, correlations, and filters, plus JSON Schemas for validation. Version 2.1.0 is the most recent referenced, and no date is shown — [GitHub](https://github.com/SigmaHQ/sigma-specification).

**Interchange formats**

- **SARIF:** It is a formal OASIS Standard. Version 2.1.0 was approved on 27 March 2020, with an errata version on 28 August 2023, and logs are JSON — [OASIS](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html).
- **CycloneDX:** It is a formal standard through Ecma as ECMA-424. The current version is 1.7, released on 21 October 2025, in JSON, XML, and Protobuf, and it can represent machine learning models — [CycloneDX](https://cyclonedx.org/specification/overview/).
- **SPDX:** It is a Linux Foundation specification, and its site describes it as an international open standard and links to ISO/IEC 5962:2021. I did not confirm which SPDX version that ISO edition covers — [SPDX](https://spdx.dev/use/specifications/). Version 3.0.1 includes AI and Dataset profiles — [SPDX 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/).
- **STIX and TAXII:** Both are maintained by the OASIS CTI Technical Committee at version 2.1. STIX is a language and serialisation format, and TAXII is an HTTPS application protocol — [OASIS CTI](https://oasis-open.github.io/cti-documentation/).
- **CSAF:** CSAF 2.0 is a formal OASIS Standard dated 18 November 2022, with Errata 01 dated 26 January 2024, and it provides JSON schemas — [OASIS](https://docs.oasis-open.org/csaf/csaf/v2.0/csaf-v2.0.html). CSAF 2.0 was reportedly also published as ISO/IEC 20153:2025 — [BSI listing](https://6sku3uaup9f9.din.de/en/standard/bs-iso-iec-20153/390544631).
- **OpenSCAP and XCCDF:** XCCDF 1.2 is a government specification in NISTIR 7275 Rev. 4 from September 2011, with XML Schema and Schematron validation. NIST lists SCAP 1.4 as the most recent release and links to a SCAP v2 project — [NIST](https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/xccdf).

**ISO 27001**

- **Format mandate:** Secondary sources say ISO/IEC 27001:2022 requires documented information and leaves format and medium to the organisation, which must define format as part of document control under clause 7.5 — [DataGuard](https://www.dataguard.com/iso-27001/clause-7-5-documented-information/); [DQS](https://www.dqsglobal.com/en/explore/blog/understanding-clause-7.5-documented-information).

### Inferences
- These formats give agents validated structure and clear semantics, which prose documents lack, but that is a by-product of their design for tool interchange. Their presence in this inventory does not imply that they were designed for model consumption or that models parse them well.
- FedRAMP is the clearest case of a mandate driving machine-readable compliance content, although the current rule's exact scope needs confirmation.
- Using OSCAL does not satisfy ISO 27001 by itself, but ISO 27001's openness on format means an organisation may choose OSCAL or Markdown if its document control is met.

### Gaps
- The final FedRAMP text on OSCAL scope and dates was not located. RFC-0024's page shows a proposal, while the rules are reported as consolidated by secondary sources.
- A search summary reported that, after public comment, FedRAMP narrowed the comprehensive requirement to Rev5 High (Class D) providers with a two-year transition for others. I could not trace this to a specific page, so it is unverified, and it should not be cited without checking the FedRAMP text.
- The ISO 27001 text is paywalled, so the format finding rests on consultancy summaries rather than the standard itself.
- STIX and TAXII 2.1 approval stages were not stated on the page read, although they are OASIS TC outputs.
- CSAF 2.1 status is reported only by a secondary aggregator as a Committee Specification Draft, so I have excluded it from the findings as unconfirmed. The OASIS TC was still working on it in February 2026 — [OASIS TC](https://groups.oasis-open.org/discussion/tc-meeting-2026-02-25).
- The ECMA-424 "Published On" date of 10 December 2025 is not explained on the page, so which edition it refers to is unclear.
- I did not review OpenSCAP as a project, or find adoption statistics for OSCAL beyond FedRAMP.

## API and specification formats

### Takeaway
OpenAPI, Arazzo, and AsyncAPI are mature, community-governed specifications that are not standards-body products on the evidence gathered. Spec-driven development formats such as Spec Kit and Kiro are vendor conventions with no shared standard, although they reuse older notations such as EARS.

### Cited Findings

- **OpenAPI:** It is a foundation-style specification from the OpenAPI Initiative — [OpenAPI specs](https://spec.openapis.org/). The latest version is 3.2.1, published on 10 September 2026 — [OpenAPI 3.2.1](https://spec.openapis.org/oas/latest.html).
- **Arazzo:** It is an OpenAPI Initiative specification. Version 1.1.0 was published on 17 May 2026, and it defines sequences of API calls and their dependencies to deliver outcomes — [Arazzo](https://spec.openapis.org/arazzo/latest.html).
- **AsyncAPI:** The current version documented is 3.1.0, in JSON or YAML under Apache 2.0, and part of its content derives from OpenAPI — [AsyncAPI](https://www.asyncapi.com/docs/reference/specification/latest).
- **TypeSpec:** It is a vendor specification, described as "Microsoft-built, community-supported", at version 1.17.0. It is an API description language that emits OpenAPI 3.0, JSON Schema 2020-12, and Protobuf — [TypeSpec](https://typespec.io/).
- **Spec Kit:** It is a vendor project from GitHub under the MIT licence. Its flow produces a constitution, specification, plan, tasks, and code through `/speckit-*` commands, and its bug-fix and assessment extensions write Markdown artefacts under `.specify/`. The page mentions Spec Kit 1.0 in a news item — [GitHub](https://github.com/github/spec-kit).
- **Spec Kit limitation:** The artefact structure is defined by the tool's templates and is not a neutral format specification, according to the page I read — [GitHub](https://github.com/github/spec-kit).
- **Kiro specs:** It is a vendor format, with `requirements.md` or `bugfix.md`, `design.md`, and `tasks.md` — [Kiro docs](https://kiro.dev/docs/specs/). Kiro's `requirements.md` uses EARS notation — [Kiro feature specs](https://kiro.dev/docs/specs/feature-specs/).
- **EARS:** It is a community convention developed by Alistair Mavin and colleagues at Rolls-Royce and first published in 2009. Its patterns are ubiquitous, state-driven, event-driven, optional-feature, unwanted-behaviour, and complex. The site calls it a lightweight notation and does not describe it as a formal standard — [EARS](https://alistairmavin.com/ears/).
- **Gherkin:** It is a community convention owned by the Cucumber Open Source Project. It uses line-based plain text in `.feature` files with `Feature`, `Rule`, `Scenario`, `Given`, `When`, and `Then` keywords, in over 70 spoken languages. The reference page defines no formal grammar — [Cucumber](https://cucumber.io/docs/gherkin/reference/).

### Inferences
- Formally validated API descriptions are a natural fit for agents because they are machine-checkable, and this group has stronger validation than any agent-instruction format. That is a judgement from the format properties, as I did not find a study on it.
- "Spec-driven development" names a practice and not a standard. Teams that adopt Spec Kit or Kiro should treat the file layout as tool-specific and the EARS or Gherkin content as the portable part.

### Gaps
- I did not confirm the OpenAPI Initiative's and AsyncAPI's Linux Foundation relationships from the pages read.
- Other spec-driven formats, such as OpenSpec, were not verified.
- I did not find whether Gherkin publishes a formal grammar outside the reference page. The Cucumber repository was not reviewed.
- Adoption counts for OpenAPI, Arazzo, AsyncAPI, and TypeSpec were not gathered.

## Documentation frameworks and guidance on writing for AI

### Takeaway
No formal standard or widely accepted specification exists for writing documentation for AI. Diátaxis, the Good Docs Project, and the Google style guide are human-oriented frameworks with no AI guidance that I could find, and what exists comes from vendors and individual projects.

### Cited Findings

- **Diátaxis:** It is a community framework by Daniele Procida, with four forms (tutorials, how-to guides, reference, and explanation) and no implementation constraints — [Diátaxis](https://diataxis.fr/); [colophon](https://diataxis.fr/colophon/). It claims use in several hundred projects and quotes testimonials from Vonage, Gatsby, and Cloudflare — [Diátaxis](https://diataxis.fr/). The home page has no AI content.
- **Good Docs Project:** It is a volunteer community publishing open-source template packs, with "Iron" v1.6.0 as the latest listed. The page contains no AI guidance — [Good Docs Project](https://www.thegooddocsproject.dev/).
- **Google developer documentation style guide:** It is a vendor style guide. I found only word-list entries on AI terminology and no chapter on writing for AI — [Google word list](https://developers.google.com/style/word-list?hl=en). A secondary claim that Google "updates guidance for machine comprehension" could not be confirmed — [draft.dev](https://draft.dev/learn/technical-writer-style-guides).
- **Anthropic guidance:** A vendor engineering post covers writing tools for agents, including steering agents towards many small and targeted searches rather than one broad search — [Anthropic](https://www.anthropic.com/engineering/writing-tools-for-agents).
- **Agent Skills guidance:** The specification gives concrete writing limits, namely keeping `SKILL.md` under 500 lines and file references one level deep — [agentskills.io](https://agentskills.io/specification).
- **OpenAI guidance:** A vendor guide says high-quality instructions are especially critical for agents — [OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf).
- **Project guidance:** Weaviate's contributor guide recommends consistent headings and code blocks, and it recommends inline information over linked files — [Weaviate](https://docs.weaviate.io/contributor-guide/weaviate-docs/llms).
- **Commercial guidance:** Mintlify publishes guidance on LLM readability, and it has a commercial interest as a documentation vendor — [Mintlify](https://www.mintlify.com/blog/how-to-improve-llm-readability).
- **Research:** Academic work optimises tool documentation for agents, including EasyTool and DocSchisel, but these are research proposals and not standards — [EasyTool](https://arxiv.org/pdf/2401.06201); [DocSchisel](https://arxiv.org/pdf/2608.10037).

### Inferences
- Human-oriented documentation frameworks still apply because their structural separation, such as Diátaxis's split of reference from explanation, is compatible with selective retrieval. No framework I found makes or tests that claim, so this remains my inference.
- Guidance on writing for AI is advice from vendors with interests in the outcome and should be treated as practice reports rather than as a standard.

### Gaps
- I did not fetch the Google guide's full contents, so a specific section on AI could exist that search did not surface.
- I did not verify the detailed content of the OpenAI, Mintlify, Weaviate, EasyTool, or DocSchisel documents beyond search extracts.
- Possible guidance from Microsoft or the Write the Docs community was not researched within the available effort.
