# Empirical evidence on how content format affects LLM and agent performance

Evidence labels used below are as follows. **[Preprint]** marks an academic paper, most of them on arXiv. **[Vendor]** marks a benchmark or claim from a party that sells the model, tool or format in question. **[Project]** marks a benchmark by a format's own authors. **[Practitioner]** marks a blog post or independent experiment that has not been peer reviewed. Verification status is also stated. "Read in full text" means that the paper body was examined. "Abstract only" and "search summary only" mean that the figures were not checked against the paper's tables, so the report writer should treat them more cautiously. The research was carried out on 2 November 2026.

## What benchmarks or papers compare input formats for LLM accuracy, and how well do they generalise to prose?

### Takeaway
Format effects are real but they are not consistent in direction across models, tasks or studies, and the gaps usually shrink on stronger models and smaller inputs. Almost all of the measured work uses tabular data, config data or benchmark prompts, and I found no controlled study that encodes the same engineering prose in JSON and Markdown.

### Cited Findings

**Prompt format: "Does Prompt Formatting Have Any Impact on LLM Performance?" (Microsoft and MIT, 2024) [Preprint, read in full text, older models]**
- The study tested plain text, Markdown, YAML and JSON wrappers on gpt-35-turbo-0613, gpt-35-turbo-16k-0613, gpt-4-1106-preview and gpt-4-32k-0613. Its datasets were MMLU (14,079 questions), NER Finance (500), HumanEval (164), FIND (500), CODEXGLUE Java and C# (1,000) and HumanEval-X (164) — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).
- The authors state that "the only differences are in structure and syntax", so the study changes the prompt wrapper around the same content and does not restructure a document — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).
- On MMLU, GPT-3.5-0613 scored 59.7 with JSON and 50.0 with Markdown, while GPT-4-1106 scored 73.9 with JSON and 81.3 with Markdown, so the preferred format reversed between model families — [arXiv 2411.10541, Appendix E](https://arxiv.org/html/2411.10541v1).
- On HumanEval, GPT-4-32k scored 21.95 with JSON and 76.22 with plain text, although GPT-4-1106 scored 86.59 with JSON on the same benchmark. The authors hypothesise that this collapse relates to OpenAI's "laziness" fix, and they did not test that explanation — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).
- GPT-4-1106 stayed below 0.036 on the paper's robustness measure on all benchmarks, while GPT-3.5 ranged from 0.035 to 0.176, which supports the claim that the larger models were less sensitive — [arXiv 2411.10541, Appendix D.2](https://arxiv.org/html/2411.10541v1).
- At temperature zero on MMLU, only 16% of GPT-3.5 responses matched between Markdown and JSON, so format changed individual answers even where averages were closer — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).
- The headline "up to 40%" figure in the [abstract](https://arxiv.org/abs/2411.10541) could not be traced to a single table entry. The widely repeated "over 300%" claim is also inconsistent with the table values, because 76.22 against 21.95 is about 247% higher. Table 1 and Table 8 also disagree on some CODEXGLUE values. The study did not test HTML or XML — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).

**Multi-table question answering: TQA-Bench [Preprint, format table read in full text, mostly small open models]**
- The paper reports that Markdown outperforms CSV, JSON and HTML "across most LLMs and context lengths" — [arXiv 2411.19504](https://arxiv.org/pdf/2411.19504).
- Overall accuracy for Qwen2.5-7B-Instruct at an 8K context was 49.86 for Markdown, 46.57 for HTML, 41.00 for JSON and 40.57 for CSV — [arXiv 2411.19504, Table VIII](https://arxiv.org/pdf/2411.19504).
- For Llama3.1-8B-Instruct at 8K, the scores were 46.57 for Markdown, 44.29 for CSV, 44.00 for HTML and 34.29 for JSON — [arXiv 2411.19504, Table VIII](https://arxiv.org/pdf/2411.19504).
- At 64K, the same Llama model scored 35.86 for Markdown and 35.71 for CSV, so that gap effectively closed — [arXiv 2411.19504, Table VIII](https://arxiv.org/pdf/2411.19504).

**Flat tabular lookup: Improving Agents [Practitioner, primary page read]**
- The test used GPT-4.1-nano, 1,000 synthetic employee records and 1,000 single-field questions in each of 11 formats. Accuracy was 60.7% for Markdown-KV, 56.0% for XML, 55.7% for INI, 54.7% for YAML, 53.6% for HTML, 52.3% for JSON, 51.9% for Markdown tables, 49.6% for natural language, 45.0% for JSONL, 44.3% for CSV and 41.1% for pipe-delimited text. The confidence intervals were about ±3 points — [Improving Agents](https://www.improvingagents.com/blog/best-input-data-format-for-llms/).
- The authors caution that they tested one model, one data pattern and flat data only, without repeated headers, and that "Markdown-KV" is their own non-standard term — [Improving Agents](https://www.improvingagents.com/blog/best-input-data-format-for-llms/).

**Nested config lookup: Improving Agents [Practitioner, primary page read]**
- The test used synthetic Terraform-like data, 1,000 questions per format per model and substring scoring. GPT-5 Nano scored 62.1% on YAML, 54.3% on Markdown, 50.3% on JSON and 44.4% on XML. Gemini 2.5 Flash Lite scored 51.9%, 48.2%, 43.1% and 33.8% on the same formats. Llama 3.2 3B scored 52.7% on JSON, 50.7% on XML, 49.1% on YAML and 48.0% on Markdown — [Improving Agents](https://www.improvingagents.com/blog/best-nested-data-format).
- Data volume was deliberately inflated until accuracy fell to 40–60%, and the authors say that "accuracy is close to 100% with much smaller amounts of data". This is a stress test that amplifies differences. Only small models were tested — [Improving Agents](https://www.improvingagents.com/blog/best-nested-data-format).

**TOON [Project benchmark, README read, not independent]**
- The benchmark used 244 questions over 13 datasets on claude-haiku-4-5, gemini-3.6-flash, gpt-5.4-nano and grok-4.5, for 5,856 calls. Accuracy was 72.2% ±2.8 for TOON, 71.4% ±2.8 for JSON, 70.7% ±2.9 for XML, 70.1% ±2.9 for YAML and 69.0% ±2.9 for compact JSON — [toon-format/toon](https://github.com/toon-format/toon).
- The README itself notes that many gaps fall inside the confidence intervals and are not statistically meaningful. On gpt-5.4-nano, TOON ranked below XML and JSON — [toon-format/toon](https://github.com/toon-format/toon).
- An older README version gave 73.9% against 69.7%, as repeated in [secondary coverage](https://labs.lamatic.ai/p/cut-token-costs-with-toon). The advantage therefore narrowed from about 4.2 points to about 0.8 points between versions — [toon-format/toon](https://github.com/toon-format/toon).
- A small single-author test on Gemini 2.5 Flash reported a first-attempt TOON success rate of about 30%, rising to 70% after adding two examples. That test appears to concern TOON as an output format, and it is search summary only — [DEV Community](https://dev.to/shudiptotrafder/toon-for-llms-a-comparative-performance-analysis-against-json-52am).

**Other table studies [Preprints, search summary only unless stated]**
- arXiv 2310.10358 found that results depended on both format and task. JSON beat the alternatives on some navigation and whole-table transformation tasks, and Markdown performed poorly on the tasks tested — [arXiv 2310.10358](https://arxiv.org/pdf/2310.10358).
- arXiv 2305.16344 reported that plain text and CSV beat XML and HTML on hybrid long documents — [arXiv 2305.16344](https://arxiv.org/pdf/2305.16344).
- TableEval reported that HTML and LaTeX scored about 2 F1 points above Markdown — [arXiv 2506.03949](https://arxiv.org/pdf/2506.03949).
- "A Closer Look into LLMs for Table Understanding" found that differences between HTML and other inputs mostly fell within confidence intervals — [arXiv 2603.15402](https://arxiv.org/pdf/2603.15402).
- TeleTables reported that Markdown used about 42% fewer tokens than HTML while remaining competitive on accuracy — [arXiv 2601.04202](https://arxiv.org/pdf/2601.04202).

**Prose-bearing web documents: HtmlRAG [Preprint, full text read, older open models]**
- With 128K context on Llama-3.1-70B, ASQA Hit@1 was 59.75 for plain text, 58.75 for cleaned HTML and 56.00 for Markdown. HotpotQA exact match was 42.25 for cleaned HTML, 41.00 for plain text and 39.00 for Markdown. Each of the six datasets used about 400 sampled questions — [arXiv 2411.02959, Table 2](https://arxiv.org/html/2411.02959v2).
- With Llama-3.1-8B, ASQA Hit@1 was 61.75 for Markdown, 61.50 for plain text and 61.00 for cleaned HTML, so differences of this size were not stable across models — [arXiv 2411.02959, Table 6](https://arxiv.org/html/2411.02959v2).
- Pruned HtmlRAG is the method the paper promotes, and the fair baseline comparison is against unpruned HtmlRAG, as the plain text and Markdown baselines received no pruning — [arXiv 2411.02959](https://arxiv.org/html/2411.02959v2).

### Inferences
- The prompt-formatting and table studies should not be used to justify either position on prose documents. The first changes wrappers, and the others test lookup in structured records.
- HtmlRAG is the closest available evidence for prose. In the rows extracted here, its gaps between plain text, Markdown and cleaned HTML are at most about four points, and the direction varies. This suggests that the choice of light markup has a small effect on prose comprehension, at least for the older models tested.
- JSON's poor results in TQA-Bench and its strong results in the GPT-3.5 experiments show that "JSON is worse" and "JSON is better" are both too general.

### Gaps
- I found no controlled experiment that encodes the same prose engineering documents (standards, ADRs or policies) in JSON and Markdown and then measures comprehension or task success on current frontier models.
- The search summary claim of a 42% accuracy gain for JSON against Markdown in arXiv 2411.10541 could not be traced to the paper's tables and should not be quoted.
- A [DEV Community study of 1,080 evaluations](https://dev.to/ker102/ai-format-wars-does-the-shape-of-your-prompt-matter-1080-evals-later-3fn7) (YAML 74.6, JSON 74.4, Markdown 72.9, plain text 70.8) concerns the prompt or requested output format and did not vary input documents. It reports no statistical tests, and its author promotes a related tool. It should not be cited as input-format evidence.

## How do token counts and costs compare between formats for the same content?

### Takeaway
On structured data, Markdown and CSV use the fewest tokens, and XML and HTML use the most. JSON's overhead against Markdown ranges from about 6–9% in TQA-Bench to about 50% on nested config, and compact JSON closes much of the gap to other formats. Token savings for prose are not measured in the sources I found.

### Cited Findings
- **Multi-table data (TQA-Bench) [Preprint, read in full text].** At the 8K scale, token counts were 3,730 for CSV, 5,400 for Markdown, 5,750 for JSON and 10,500 for HTML. At the 64K scale, they were 29,300 for CSV, 41,700 for Markdown, 45,400 for JSON and 81,600 for HTML — [arXiv 2411.19504, Table VII](https://arxiv.org/pdf/2411.19504).
- **Flat records (Improving Agents) [Practitioner].** Token counts for the same 1,000 records were 19,524 for CSV, 25,140 for Markdown tables, 48,100 for INI, 52,104 for Markdown-KV, 55,395 for YAML, 66,396 for JSON, 75,204 for HTML and 76,114 for XML — [Improving Agents](https://www.improvingagents.com/blog/best-input-data-format-for-llms/).
- **Nested config (Improving Agents) [Practitioner].** On GPT-5 Nano's data, token counts were 38,357 for Markdown, 42,477 for YAML, 57,933 for JSON and 68,804 for XML. Markdown used the fewest tokens for every model — [Improving Agents](https://www.improvingagents.com/blog/best-nested-data-format).
- **Mixed structures (TOON) [Project].** Average tokens were 2,474 for TOON, 2,892 for compact JSON, 3,487 for YAML, 4,308 for pretty JSON and 4,909 for XML, counted with the `o200k_base` encoding. The README's token-total section reports different aggregates, with TOON at 264,734 and compact JSON at 260,451, so TOON uses 1.6% more than compact JSON on that total while the average table suggests the reverse. The two figures should not be quoted together without checking the README's definitions — [toon-format/toon](https://github.com/toon-format/toon).
- **TOON's limits [Project].** TOON used more tokens than compact JSON on nested e-commerce data (+5.6%), semi-uniform event logs (+19.9%) and deeply nested configuration (+6.7%). On flat data, it used 5.9% more tokens than CSV — [toon-format/toon](https://github.com/toon-format/toon).
- **Web pages (HtmlRAG) [Preprint].** Relative to raw HTML, cleaned HTML removed over 94.07% of tokens, plain text removed 96.71% and Markdown conversion removed 90.32% — [arXiv 2411.02959, Section 4.6.1](https://arxiv.org/html/2411.02959v2).
- **Claude tokenizer [Practitioner, search summary only].** A DEV Community test using Anthropic's `count_tokens` endpoint reported averages of 3,252 tokens for JSON, 2,208 for YAML and 1,514 for Markdown — [DEV Community](https://dev.to/webramos/yaml-vs-markdown-vs-json-vs-toon-which-format-is-most-efficient-for-the-claude-api-4l94).
- **Cost of a real agent context [Preprint].** Adding a context file increased agent cost by up to 23%, and the study also recorded more steps and reasoning tokens, so the cost of a document to an agent is not limited to its own token count — [arXiv 2602.11988](https://arxiv.org/html/2602.11988v1).

### Inferences
- The following ratios are my own calculations from the figures above. In TQA-Bench, JSON is 6–9% larger than Markdown and HTML is about 95% larger. On the Improving Agents nested data, JSON is 51% larger than Markdown on GPT-5 Nano's data, and on the flat data, JSON is 2.6 times the size of a Markdown table and 3.4 times the size of CSV.
- The size of the JSON penalty depends heavily on repeated keys and pretty-printing. TQA-Bench's small JSON penalty and the larger Improving Agents penalties are therefore not in conflict.
- For prose, overhead should be lower than on records because few keys repeat relative to the text. JSON strings also need escaped newlines and quotes, which adds a smaller per-line cost. This is reasoning and has not been measured.

### Gaps
- I found no measurement of token cost for the same long prose document in JSON, YAML and Markdown across tokenizers.
- Most counts use OpenAI encodings, and the TOON README warns that other providers' absolute counts differ — [toon-format/toon](https://github.com/toon-format/toon).

## How does document structure affect RAG, and what are the measured retrieval improvements?

### Takeaway
Measured gains come mainly from adding context or metadata to chunks and from hybrid search with reranking, and these do not depend on the source format. Structure-aware chunking shows gains in some studies, but I found no controlled benchmark isolating Markdown heading chunking from fixed-size chunking at the same size.

### Cited Findings

**Contextual retrieval [Vendor benchmark, Anthropic, 2024, primary page read]**
- From a 5.7% baseline top-20 failure rate, contextual embeddings reached 3.7% (a 35% relative reduction), adding contextual BM25 reached 2.9% (49%) and adding reranking reached 1.9% (67%) — [Anthropic](https://www.anthropic.com/news/contextual-retrieval).
- The figures are averages across codebases, fiction, arXiv papers and science papers, using Gemini Text 004 embeddings and Claude 3 Haiku for contextualisation. The post does not report independent verification, and the absolute improvements are 2.0, 2.8 and 3.8 percentage points — [Anthropic](https://www.anthropic.com/news/contextual-retrieval).

**Element-based chunking on financial reports (Unstructured, 2024) [Preprint, read in full text, a vendor of document parsing]**
- On FinanceBench (141 questions), manual Q&A accuracy was 35.46% at 128 tokens, 36.88% at 256 tokens, 48.23% at 512 tokens and 53.19% for the best element-based configuration — [arXiv 2402.05131](https://arxiv.org/html/2402.05131v3).
- Page-level retrieval accuracy was higher for fixed-size chunks, at 68.09–73.05%, than for element-based chunks, at 46.10–67.38%, so individual element-based runs did not beat the baseline on this retrieval metric. The aggregated runs were 84.40% for element-based and 83.69% for base — [arXiv 2402.05131](https://arxiv.org/html/2402.05131v3).
- No statistical significance testing is reported, and the study covers one domain and one pipeline — [arXiv 2402.05131](https://arxiv.org/html/2402.05131v3).
- A search summary reports the authors' comment that Markdown-based chunking only partly captures element types — [arXiv 2402.05131](https://arxiv.org/abs/2402.05131v3).

**Null result on semantic chunking [Preprint, abstract only]**
- A comparison with fixed-size chunking on document retrieval, evidence retrieval and answer generation concluded that "the computational costs associated with semantic chunking are not justified by consistent performance gains" — [arXiv 2410.13070](https://arxiv.org/abs/2410.13070).

**Heading-aware chunking**
- A practitioner guide states that its authors found no published benchmark isolating Markdown-header chunking and that they treat the method as design reasoning — [Olostep](https://www.olostep.com/blog/rag-chunking-strategies).
- The same guide reports paragraph-group chunking at an nDCG@5 of about 0.459 against 0.244 for 100-character fixed chunks. This compares against an unusually small chunk size and I did not locate the primary source — [Olostep](https://www.olostep.com/blog/rag-chunking-strategies).
- A secondary guide reports 67% for fixed-size and 69% for recursive character splitting on academic papers, but its source is unclear — [PremAI](https://blog.premai.io/rag-chunking-strategies-the-2026-benchmark-guide).
- A small evaluation (30 queries over 18 Markdown documents) reported that BM25 over structural chunks reached Recall@5 of 1.000 and MRR of 0.911, while dense retrieval over the full pipeline reached Recall@5 of 0.867. This is search summary only and the sample is very small — [arXiv 2603.23533](https://arxiv.org/html/2603.23533v2).
- A systematic review of 16 financial-document studies reported precision gains of up to 33.42% for structure-aware and semantic chunking. This is an upper bound from search summary only, and I could not confirm the venue — [BINUS summary](https://research.binus.ac.id/airdc/?p=2987).
- MultiDocFusion reported retrieval precision gains of 8–15% and QA gains of 2–3% from hierarchical parsing. This is search summary only — [arXiv 2604.12352](https://arxiv.org/pdf/2604.12352).

**Metadata [Preprints, search summary only]**
- One enterprise study reported HR@10, NDCG@10 and MRR of 0.775, 0.699 and 0.519 with all metadata against 0.700, 0.615 and 0.389 with content only. Headline figures differ between versions of the paper — [arXiv 2512.05411](https://arxiv.org/pdf/2512.05411).
- On SEC filings, company and year fields gave strong disambiguating signals while section titles gave more modest gains. Prefixing metadata into chunk text retrieves well but requires re-embedding when metadata changes — [arXiv 2601.11863](https://arxiv.org/html/2601.11863v1).

**Tables and parsing**
- OfficeQA Pro reported a 16.1% average relative gain across agents from a structured document representation produced by Databricks' `ai_parse_document`, on 133 questions over 89,000 pages. This is a relative gain, and the parser is the product of the party that I understand published the benchmark, which the report writer should confirm — [arXiv 2603.08655](https://arxiv.org/abs/2603.08655).
- A search summary states that HTML edged Markdown overall in OfficeQA Pro and that Claude Opus 4.5 and Sonnet 4.5 did better with hierarchical Markdown. I could not verify this from the PDF, because its text did not yield matches when extracted — [arXiv 2603.08655](https://arxiv.org/pdf/2603.08655).
- Converting PDF and PPTX files to Markdown for RAG reliably extracted text but lost significant information, according to one study (search summary only) — [arXiv 2508.15817](https://arxiv.org/html/2508.15817v1).

### Inferences
- The source format matters to RAG mostly as a means of giving a chunker reliable boundaries and metadata. A chunker can use the headings in Markdown or the keys in JSON, so this benefit does not itself favour either format.
- The gains that are best evidenced are document or section context attached to each chunk, combined with hybrid retrieval and reranking. A consistent title, identifier, owner and date on each document would support this in either format.

### Gaps
- I found no controlled benchmark that holds chunk size constant and varies only heading-aware against fixed splitting on a Markdown corpus.
- I found no evaluation that isolates YAML frontmatter filtering on engineering documents. Metadata studies mostly use prefixing on financial or enterprise corpora.
- I found no comparison of the same engineering corpus chunked from JSON and from Markdown.

## How does structure affect agents reading files directly with grep and file tools?

### Takeaway
There is measured evidence that harness design, delivery path and context-file presence affect agents, and these effects are large compared with format effects. I found no controlled study of heading structure, document length or file granularity in engineering documents.

### Cited Findings

**"Is Grep All You Need?" (May 2026) [Preprint, results sections extracted from the PDF, current models, memory corpus and not code or documents]**
- The study used a 116-question subset of LongMemEval-S over session JSON, the Chronos custom harness and Claude Code, Codex and Gemini CLI — [arXiv 2605.15184](https://arxiv.org/pdf/2605.15184).
- With inline results on the Chronos harness, grep spanned 83.6–93.1% and vector spanned 62.9–83.6%. The grep lead ranged from 86.2% against 62.9% (Chronos, Gemini 3.1 Flash-Lite) to 76.7% against 75.0% (Claude Code, Opus 4.6) — [arXiv 2605.15184](https://arxiv.org/pdf/2605.15184).
- Harness choice alone moved the same Opus 4.6 model from 93.1% on Chronos to 76.7% on Claude Code — [arXiv 2605.15184](https://arxiv.org/pdf/2605.15184).
- Delivering tool results through files reshuffled the comparison. Vector exceeded grep in five of the compared configurations, and Codex with GPT-5.4 fell from 93.1% with inline grep to 55.2% with file-based grep — [arXiv 2605.15184](https://arxiv.org/pdf/2605.15184).
- When the number of sessions in the corpus was varied, accuracy did not change monotonically. Chronos with Opus and grep reached 90.5% at 20 sessions, 85.3% at 30 and 89.7% at full size — [arXiv 2605.15184, Table 2](https://arxiv.org/pdf/2605.15184).
- The authors state, "We do not claim that grep 'beats' vector in general" — [arXiv 2605.15184](https://arxiv.org/pdf/2605.15184).

**"Evaluating AGENTS.md" (ETH Zurich and LogicStar.ai, 2026) [Preprint, read in full text, current models]**
- The study used Claude Code with Sonnet-4.5, Codex with GPT-5.2 and GPT-5.1 mini, and Qwen Code, over SWE-bench Lite (300 tasks) and AGENTbench (138 instances from 12 repositories) — [arXiv 2602.11988](https://arxiv.org/html/2602.11988v1).
- LLM-generated context files reduced the resolution rate by 0.5% on SWE-bench Lite and 2% on AGENTbench (the introduction says 3% on average, without explaining the difference), and raised cost by 20–23%. Developer-written files improved success by about 4% on average and raised cost by up to 19% — [arXiv 2602.11988](https://arxiv.org/html/2602.11988v1).
- On AGENTbench with Sonnet-4.5, the no-context, LLM-file and human-file conditions used 40.7, 46.5 and 45.3 steps at $1.15, $1.33 and $1.30 per task — [arXiv 2602.11988, Table 2](https://arxiv.org/html/2602.11988v1).
- Context files did not meaningfully reduce the number of steps before the agent first touched a file changed in the pull request, which is evidence against the usefulness of repository overviews. Eight of the 12 human files included an overview — [arXiv 2602.11988](https://arxiv.org/html/2602.11988v1).
- With repository documentation removed, LLM-generated files improved performance by 2.7% on average and beat developer-written files, so their value depends on what else the agent can read — [arXiv 2602.11988](https://arxiv.org/html/2602.11988v1).
- The studied files averaged 641 words (range 24–2,003) and 9.7 sections (range 1–29), but these are descriptive figures and the summary I reviewed found no analysis of length as a causal factor — [arXiv 2602.11988, Table 1](https://arxiv.org/html/2602.11988v1).
- The study's limits are its focus on Python and its use of task resolution as the only quality measure — [arXiv 2602.11988](https://arxiv.org/html/2602.11988v1).

**Contrasting study [Preprint, abstract only]**
- Across 10 repositories and 124 pull requests, AGENTS.md was "associated with" a 28.64% lower median runtime and 16.58% lower output tokens, with comparable task completion. This differs from the ETH cost result, and the two studies measure different quantities on different task sets — [arXiv 2601.20404](https://arxiv.org/abs/2601.20404).

**Vercel Next.js evals [Vendor benchmark, primary page read]**
- Pass rates were 53% with no docs, 53% with a default skill, 79% with a skill with explicit instructions and 100% with an AGENTS.md docs index. The tests targeted Next.js 16 APIs absent from training data. The sample size is not reported — [Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals).
- The docs index was compressed from about 40KB to about 8KB with the 100% pass rate maintained. This is one vendor's single-framework result and does not compare formats — [Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals).

### Inferences
- Lexical tools favour literal, consistent terms, so stable identifiers and exact names in documents are likely to help grep-based agents. The study above supports this mechanism only for memory recall, and its authors do not generalise it to all corpora.
- Content and placement of information appear to matter more than syntax. The context-file evidence varies by who wrote the file and what it contains. None of these studies varied Markdown against JSON.
- Grep-based retrieval worked well on session JSON in arXiv 2605.15184, so JSON is not inherently unsearchable. That study has no Markdown arm, so no comparison follows from it.

### Gaps
- I found no controlled evidence on heading depth, document length or one-large-file against many-small-files for agents using file tools.
- No study found compares agent task success with the same ADR or policy in Markdown and JSON.
- arXiv 2601.20404 was read at abstract level, so its design and whether its association can be interpreted causally were not checked.

## What do model vendors advise, and which of that advice lacks published measurement?

### Takeaway
All three vendors recommend clear delimiters and all accept tags or Markdown structure, but they speak about prompt construction and not about how source documents should be authored. Most of this advice has no published method or data.

### Cited Findings
- **Anthropic, vendor guidance without published method.** The documentation says that XML tags "help Claude parse complex prompts unambiguously" and reduce misinterpretation. No measurement is cited in the passage — [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags).
- **Anthropic, vendor claim with a figure but no published study.** For inputs of 20k tokens or more, it advises placing long documents above the query and states, "Queries at the end can improve response quality by up to 30 percent in tests, especially with complex, multidocument inputs." The tests are not described — [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags).
- **Anthropic, vendor guidance.** It advises wrapping multiple documents in `<document>` tags with `<document_content>` and `<source>` subtags, and asking the model to quote relevant passages first. These are runtime prompt wrappers and they say nothing about the format in which a document should be stored — [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags).
- **OpenAI, vendor-relayed practitioner anecdote.** The GPT-5 guide says Cursor found that "structured XML specs like <[instruction]_spec> improved instruction adherence", and gives no figures. Its JSON content appears only in sample response output and it offers no advice to format context documents as JSON — [OpenAI GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide).
- **OpenAI, vendor observation.** It reports that adherence to a Markdown output instruction can degrade over a long conversation and that repeating it every 3–5 user messages helped. This concerns output format and gives no data — [OpenAI GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide).
- **Google, vendor guidance without measurement.** It says "XML-style tags (e.g., `<context>`, `<task>`) or Markdown headings are effective", advises choosing one format consistently, and recommends supplying context first with specific questions at the end. The page cites no quantitative measurements — [Google Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies).
- **Measured vendor work is on retrieval.** Anthropic's Contextual Retrieval is the only vendor document in this review that provides a stated baseline and results — [Anthropic](https://www.anthropic.com/news/contextual-retrieval).

### Inferences
- Vendor advice supports separating instructions from data at prompt time. It does not support writing source documents in XML or JSON, because a harness can add wrappers when it assembles the prompt.
- Google's explicit acceptance of either tags or Markdown headings is at odds with a strict reading that one syntax is necessary.
- The evidence reviewed gives no independent replication of Anthropic's "up to 30 percent" figure.

### Gaps
- I found no vendor-published experiment that compares authoring formats for source documents.
- Anthropic's tests behind the 30% figure are undocumented in the page reviewed.

## Where is JSON or another structured format measurably better than Markdown, and where is it worse?

### Takeaway
The clearest advantages of structured formats are deterministic validation and parseable machine output, where success can be guaranteed or checked without an LLM. As an input for model reading, JSON's results are mixed and it costs more tokens than Markdown.

### Cited Findings

**Where JSON or structured formats do better**
- GPT-3.5 models scored higher on JSON than Markdown on MMLU (59.7 against 50.0) and HumanEval (59.76 against 54.27). These are older models — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).
- JSON was slightly more accurate than Markdown in the HumanEval-X results on GPT-4 models (72.30 against 70.70, and 72.39 against 71.65) — [arXiv 2411.10541, Appendix E](https://arxiv.org/html/2411.10541v1).
- On nested data, Llama 3.2 3B scored 52.7% on JSON and 48.0% on Markdown, although their confidence intervals overlap slightly, and YAML beat Markdown on two other models — [Improving Agents](https://www.improvingagents.com/blog/best-nested-data-format).
- On flat lookup, JSON at 52.3% was tied with Markdown tables at 51.9%. Key-value Markdown was higher at 60.7%, which shows that repeating field labels matters more than whether the syntax is called JSON or Markdown — [Improving Agents](https://www.improvingagents.com/blog/best-input-data-format-for-llms/).
- Constrained decoding makes output parseable by construction, but this is described as a constraint at the sampler level and not a quality improvement — [Together AI documentation](https://docs.together.ai/learn/structured-outputs). A benchmark of six constrained-decoding frameworks evaluates efficiency, coverage and output quality (search summary only) — [arXiv 2501.10868](https://arxiv.org/html/2501.10868v1).

**Where JSON or strict structure does worse**
- "Let Me Speak Freely?" reports "a significant decline in LLMs reasoning abilities under format restrictions", with stricter constraints generally causing greater reductions. This concerns output format and not input documents — [arXiv 2408.02442](https://arxiv.org/abs/2408.02442).
- The same paper reportedly finds that stricter formats can improve classification accuracy, and suggests answering in natural language first and converting second. This detail is search summary only — [arXiv 2408.02442](https://arxiv.org/pdf/2408.02442).
- TQA-Bench reports JSON as lowest or near lowest for almost all tested small models and context lengths, for example 34.29 against 46.57 for Markdown on Llama3.1-8B at 8K — [arXiv 2411.19504, Table VIII](https://arxiv.org/pdf/2411.19504).
- GPT-4-1106 scored 73.9 on JSON and 81.3 on Markdown on MMLU, and GPT-4-32k scored 21.95 on JSON on HumanEval — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).
- The TOON benchmark found compact JSON lowest in overall accuracy at 69.0%, and pretty JSON at 71.4% used 74% more tokens than TOON according to the reported averages (2,474 against 4,308). Most accuracy gaps there are within the intervals — [toon-format/toon](https://github.com/toon-format/toon).

### Inferences
- A well-supported distinction separates machine-verifiable fields from human-readable reasoning. Status, owner, dates, applicability and control identifiers suit a schema and can be checked deterministically. Rationale and trade-offs have no measured gain from being encoded as JSON string values.
- Deterministic validation does not need the LLM to read JSON. Frontmatter or a sidecar schema can be validated by a linter, while the body stays in Markdown. This is a design inference and has not been tested as a comparison.

### Gaps
- I found no measured study comparing JSON and Markdown for field extraction from engineering documents specifically.
- Numeric details for "Let Me Speak Freely?" and JSONSchemaBench were not extracted, and neither paper tests input formats.

## What evidence contradicts the claim that Markdown is best for LLMs?

### Takeaway
A substantial body of results contradicts the universal claim, because Markdown often ranks below YAML, HTML, plain text or JSON in specific tests. No single format wins consistently, although Markdown stays competitive and cheap, so the supportable claim is "good default at low token cost" and not "best".

### Cited Findings

**Results where Markdown lost**
- YAML beat Markdown on nested data for GPT-5 Nano (62.1% against 54.3%) and Gemini 2.5 Flash Lite (51.9% against 48.2%) — [Improving Agents](https://www.improvingagents.com/blog/best-nested-data-format).
- Markdown tables scored 51.9% on flat records, below XML at 56.0%, and overlapped JSON at 52.3% — [Improving Agents](https://www.improvingagents.com/blog/best-input-data-format-for-llms/).
- Plain text beat Markdown on many HtmlRAG measures, for example NQ Hit@1 of 59.75 against 57.00 on the 70B model and TriviaQA Hit@1 of 94.00 against 91.50 on the 8B model. Cleaned HTML also beat Markdown on several measures — [arXiv 2411.02959](https://arxiv.org/html/2411.02959v2).
- On GPT-3.5, Markdown was often the weakest wrapper, for example 50.0 on MMLU against 59.7 for JSON, and 5.19 on FIND against 15.9 for plain text — [arXiv 2411.10541, Appendix E](https://arxiv.org/html/2411.10541v1).
- TableEval reported HTML and LaTeX about 2 F1 points above Markdown (search summary only) — [arXiv 2506.03949](https://arxiv.org/pdf/2506.03949). arXiv 2310.10358 found Markdown poor across its tasks (search summary only) — [arXiv 2310.10358](https://arxiv.org/pdf/2310.10358).

**Null or near-null results**
- The TOON project's accuracy differences mostly fall within confidence intervals — [toon-format/toon](https://github.com/toon-format/toon).
- HumanEval on GPT-4-1106 had a best-to-worst format comparison with p = 0.055, which was not significant at the 5% level, and JSON and Markdown tied at 86.59 — [arXiv 2411.10541](https://arxiv.org/html/2411.10541v1).
- Llama 3.2 3B showed little format sensitivity on nested data, according to the authors — [Improving Agents](https://www.improvingagents.com/blog/best-nested-data-format).
- Differences between input representations in arXiv 2603.15402 mostly fell within confidence intervals (search summary only) — [arXiv 2603.15402](https://arxiv.org/pdf/2603.15402).
- Semantic chunking did not justify its cost against fixed-size chunking — [arXiv 2410.13070](https://arxiv.org/abs/2410.13070).

**Results that favour Markdown, for balance**
- TQA-Bench favours Markdown across most tested models and context lengths — [arXiv 2411.19504](https://arxiv.org/pdf/2411.19504).
- Spider2-V notes that Markdown uses fewer tokens than HTML to represent structure (a design remark, search summary only) — [arXiv 2407.10956](https://arxiv.org/pdf/2407.10956).

**Claims to treat with caution**
- A Medium article contrasts JSON at about 69.7% with Markdown-KV at 60.7% and concludes that JSON remains a sensible default, but those figures appear to come from different benchmarks with different models and data, so the comparison is unsound — [SoftServe on Medium](https://medium.com/softserve-technical-communication/rethinking-llm-inputs-json-against-toon-and-markdown-kv-b713bcbe7eb5), [Improving Agents](https://www.improvingagents.com/blog/best-input-data-format-for-llms/).

### Inferences
- The evidence does not show that Markdown is uniquely understood by LLMs. Its strongest measured advantage is token cost combined with acceptable accuracy.
- For the wider question, the evidence does not support rewriting prose standards, ADRs or policies as JSON to improve LLM comprehension. It also does not prove Markdown superior on prose, because no direct test exists. The practical basis for Markdown is lower token cost, human review, diffability and the absence of a measured penalty, combined with validated structured metadata where determinism is needed. The human-review and diffability parts of that basis are engineering judgement and were not measured here.
- A team with a large corpus should run a small evaluation of its own, because the studies repeatedly show dependence on model and task. Model-specific reversals in arXiv 2411.10541 imply that a format choice tuned to one model may not transfer.

### Gaps
- Most format comparisons use older or small models, or stress inputs to induce failure, so effect sizes on current frontier models at normal document sizes are likely to be smaller but have not been shown directly.
- I found no measured evidence on whether `llms.txt` improves LLM accuracy.
- The search summaries for arXiv 2310.10358, 2305.16344, 2506.03949, 2603.15402, 2601.04202, 2512.05411 and 2603.23533 were not checked against full text in this pass.
