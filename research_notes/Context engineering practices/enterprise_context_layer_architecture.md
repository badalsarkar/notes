# Enterprise Context Layer Architecture for LLMs and Agents

Research date: 2026-10-26. Each source carries its publication date where one could be established. "Measured" means a published experiment with a stated method. "Vendor claim" means a figure published by a party that sells the approach being measured.

## 1. What do "context layer", "semantic layer for AI", "context graph" and "knowledge layer" mean, and how do Gartner, a16z, Atlan, dbt Labs and others define them?

### Takeaway
There is no standard definition. Most sources describe a governed tier between enterprise data and agents that supplies business meaning (definitions, canonical entities), provenance (lineage, which table is authoritative), governance (access, certification) and accumulated knowledge (tribal knowledge, corrections, decision history). A semantic layer is treated as one component of that tier, and a "context graph" is a narrower idea about recording decision traces.

### Cited Findings
- a16z (Jason Cui and Jennifer Li, "Your Data Agents Need Context", 10 March 2026) defines the context layer as a superset of the traditional semantic layer, which mainly defines metrics such as revenue or churn for BI tools. Its listed components are access to all relevant data including tribal knowledge in documents, canonical entities and identity resolution, instructions that capture tribal knowledge, governance guidance, and code and natural-language rules similar to `.cursorrules` files. — [a16z](https://a16z.com/your-data-agents-need-context/)
- a16z proposes a five-step build: make sources reachable (ideally through a lakehouse), auto-generate context with LLMs from query frequency, common joins and dbt or LookML definitions, have human experts add implicit and conditional knowledge, expose the context to agents through an API or MCP, and keep it self-updating as upstream data changes and agent errors are corrected. — [a16z](https://a16z.com/your-data-agents-need-context/)
- a16z's motivating failure is the question "what was revenue growth last quarter?": the agent does not know which revenue definition or fiscal quarter applies, the semantic-layer YAML was outdated and missing two product lines, and finance's `fct_revenue` competes with a materialized view `mv_revenue_monthly`. — [a16z](https://a16z.com/your-data-agents-need-context/)
- a16z states that the market is early and leaves open where the context layer should live, whether it can live in several places, and whether it becomes a standalone product. — [a16z](https://a16z.com/your-data-agents-need-context/)
- Atlan (vendor) describes the context layer as a persistent, versioned, portable layer of enterprise knowledge, built from existing business systems, that agents query at runtime, and attributes to Gartner a structure of three components: semantics, operational state and provenance. — [Atlan](https://atlan.com/know/core-components-context-layer/)
- DataHub (vendor) describes it as the shared, governed layer every agent draws from to understand what enterprise data means, whether it is current and whether it can be trusted. — [DataHub](https://datahub.com/blog/context-layer-for-ai-agents/)
- Alation (vendor) distinguishes the semantic layer, which standardizes metric definitions such as "revenue", from the context layer, which adds ownership, lineage and machine-readable delivery on top. — [Alation](https://www.alation.com/blog/what-is-an-enterprise-context-layer/)
- DataWalk (vendor) reports that Gartner's Intelligence Capabilities Framework places the context layer as a distinct tier between the data layer and the intelligence layer; this is a second-hand account of Gartner. — [DataWalk](https://datawalk.com/what-is-context-layer/)
- At Gartner Data and Analytics (March 2026), per Juan Sequeda's recap, Gartner stated that 44% of organizations implemented a semantic layer in 2025 and 48% plan to by 2027, that semantics "break the barrier" to agent-ready data, and Anthony Mullen predicted that by 2030 universal semantic layers will be treated as critical infrastructure alongside data platforms and cybersecurity. Only 14% of organizations were said to be confident their data is secured and governed, and "decision governance" was called the most underrated trend. — [Sequeda recap, 16 Mar 2026](https://juansequeda.substack.com/p/gartner-data-and-analytics-march)
- Vendor blogs repeat a March 2026 Gartner prediction that by 2028, 60% of agentic analytics projects relying solely on MCP will fail because of the absence of a consistent semantic layer, and an earlier prediction that organizations will abandon 60% of AI projects not supported by AI-ready data through 2026. I could not reach the Gartner originals, and the timeframes differ between vendor retellings. — [CTO Magazine](https://ctomagazine.com/semantic-layer-ai-agents-iceberg-mcp/); [TechTarget](https://www.techtarget.com/data-technologies/feature/Agents-semantic-layers-among-top-data-analytics-trends)
- The term "context graph" traces to Foundation Capital's late-2025 essay (Jaya Gupta and Ashu Garg, "AI's trillion-dollar opportunity: Context graphs"), which argues that systems of record keep outcomes but not reasoning, and that a context graph is an accumulated record of decision traces (what context was used, which policy applied, what exception was granted, who approved it) linked across entities and time so precedent becomes searchable. It argues that capturing traces requires sitting in the execution path at commit time. — [Ashu Garg Substack](https://ashugarg.substack.com/p/ais-trillion-dollar-opportunity-context); [Tellius summary](https://www.tellius.com/resources/blog/what-is-a-context-layer-for-ai-agents-the-definitive-guide-for-2026)
- The Open Semantic Interchange (OSI) was announced by Snowflake in September 2025 as a vendor-neutral semantic model specification, co-led with Salesforce, dbt Labs, BlackRock and RelationalAI, with Alation, Atlan, Cube, Hex, Sigma and ThoughtSpot among supporters. — [Business Wire, 23 Sep 2025](https://www.businesswire.com/news/home/20250923902448/en/Snowflake-Salesforce-dbt-Labs-Revolutionize-Data-Readiness)
- Sequeda (data.world/ServiceNow) argues that OSI covers only BI and analytics semantics, and recommends RDF and OWL for ontologies; this is his opinion, not Gartner's. — [Sequeda recap](https://juansequeda.substack.com/p/gartner-data-and-analytics-march)

### Inferences
- The working definition that is common across sources has four parts: meaning (semantic layer or ontology), provenance and trust (catalog, lineage, certification), knowledge (documents, tribal rules, memory, decision traces) and delivery (API or MCP with access control). The terms differ mainly in which part a vendor sells.
- BlackRock's co-leadership of OSI is the clearest capital-markets signal that buy-side firms see shared metric definitions as an interoperability problem across tools.

### Gaps
- I did not obtain any primary Gartner or Forrester document; all Gartner statements here are second-hand. I found no Forrester definition.
- I found no dbt Labs formal definition of "context layer" beyond its semantic-layer positioning.

## 2. Semantic layers and metrics layers, and their measured effect on text-to-SQL accuracy

### Takeaway
On one small insurance benchmark, a semantic layer or knowledge graph raised accuracy substantially (16% to 54% for a knowledge graph in 2023; 98-100% for a modeled dbt Semantic Layer in 2026 within its scope). The gap has narrowed as models improved, the semantic layer answers nothing outside what has been modeled, and every headline result rests on 11 to a few dozen questions. Enterprise-scale benchmarks (Spider 2.0) show raw text-to-SQL is still far from reliable on large schemas.

### Cited Findings
- The data.world benchmark (Sequeda, Allemang, Jacob; 13 Nov 2023) used an insurance-domain enterprise schema and found GPT-4 with zero-shot prompts answered 16% of questions correctly directly over SQL and 54% over a knowledge-graph representation of the same database. — [arXiv 2311.07509](https://arxiv.org/pdf/2311.07509)
- A 2024 follow-up by Allemang and Sequeda cites the same 16% to 54% improvement and proposes ontology-based query checking and repair to reduce the remaining errors. — [arXiv 2405.11706](https://arxiv.org/html/2405.11706v1)
- dbt Labs' 2026 rerun (Jason Ganz and Benoit Perigaud, 7 Apr 2026) used the same ACME Insurance schema (15 normalized tables), 11 questions, each run 20 times. With a modeled dbt project, Claude Sonnet 4.6 scored 90.0% via text-to-SQL and 98.2% via the Semantic Layer; GPT-5.3 Codex scored 84.1% and 100.0%. — [dbt Labs blog](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- On the original raw schema across all questions, text-to-SQL accuracy rose from 32.7% (GPT-4, 2023) to 64.5% (both 2026 models), and Semantic Layer accuracy rose from 60.5% to 72.7%. Within Semantic Layer scope, text-to-SQL scored 62.5% (Sonnet 4.6) and 51.2% (GPT-5.3 Codex) against 100% for the Semantic Layer. On questions needing too many entity hops, the Semantic Layer scored 0% in every run while text-to-SQL scored 70% to 100%. — [dbt Labs blog](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- Across 16 model and reasoning-effort permutations, Semantic Layer accuracy ranged from 87.2% to 100% and text-to-SQL from 50% to 65%; higher reasoning effort had little effect on accuracy but raised latency from about 8 to over 20 seconds per query. — [dbt Labs blog](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- dbt Labs states its own caveats: the benchmark is vendor-run, uses 11 questions on one dataset, and gave text-to-SQL the full schema, which is impractical for large warehouses. It reports that text-to-SQL fails silently with plausible wrong answers, while the Semantic Layer fails visibly by erroring or declining. — [dbt Labs blog](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- Third parties report 100% on the same 11 questions: Cube with Delphi, and Bodo.ai's PyDough (220 of 220 across 20 runs). These are vendor claims on a tiny set. — [Cube](https://cube.dev/blog/semantic-layers-the-missing-piece-for-ai-enabled-analytics); [Bodo.ai](https://www.bodo.ai/blog/how-pydough-reached-100-accuracy-on-dbts-semantic-layer-benchmark)
- A HackerNoon analysis argues these numbers mostly measure how much translation work was already done to the schema and how forgivingly answers were graded, so they are not directly comparable. — [HackerNoon](https://hackernoon.com/why-better-schema-modeling-beats-better-text-to-sql-models)
- Spider 2.0 (ICLR 2025 oral; v1 Nov 2024, v2 Mar 2025) contains 632 real enterprise workflow problems on BigQuery, Snowflake and local databases, often with over 1,000 columns. o1-preview with the paper's agent framework solved 21.3%, compared with 91.2% on Spider 1.0 and 73.0% on BIRD. — [arXiv 2411.07763](https://arxiv.org/abs/2411.07763)
- Spider 2.0 now ships as Spider 2.0-Snow (547 tasks), Spider 2.0-Lite (547 tasks across BigQuery, Snowflake and SQLite) and Spider 2.0-DBT (68 tasks); the repo notes an evaluation-suite fix that refreshed leaderboard scores, and a 12 Aug 2026 notice that Snow access was disrupted by a Snowflake account suspension. — [Spider2 GitHub](https://github.com/xlang-ai/Spider2)
- Oracle claims its SOMA-SQL ranks first on Spider 2.0-Lite at 72.02% execution accuracy (vendor claim). — [Oracle blog](https://blogs.oracle.com/cloud-infrastructure/oci-gen-ai-tops-spider-2-lite)
- A January 2026 audit estimates that Spider 2.0-Snow has a 62.8% annotation error rate on the 121 problems with public gold SQL, which casts doubt on leaderboard rankings. — [arXiv 2601.08778](https://arxiv.org/html/2601.08778v3)
- On BIRD, the human baseline is 92.96% execution accuracy. ReViSQL (Mar 2026) claims 93.2% on an expert-verified Mini-Dev subset, not the full test set, and full-benchmark leaders were reported around 80-82% in mid-2026 (Gemini-SQL2 reported at 80.04% without a public technical report). — [arXiv 2603.20004](https://arxiv.org/abs/2603.20004v1); [AI Weekly](https://aiweekly.co/alerts/googles-gemini-sql2-tops-bird-text-to-sql-at-8004)

### Inferences
- The strongest measured benefit of a semantic layer is not average accuracy but failure behaviour: it either returns the governed answer or refuses. For regulated reporting (P&L, risk exposures, regulatory capital) that property matters more than coverage.
- The weakness is coverage. Questions that need joins the modeler did not anticipate (for example position joined to counterparty hierarchy joined to collateral agreements) get 0% from the semantic layer, so a hybrid router (semantic layer first, governed text-to-SQL fallback) is the pattern dbt itself recommends.
- Benchmark numbers from small single-domain sets and from Spider 2.0 should not be compared directly; the former measure modeling effort, the latter measure schema navigation at scale, and both have documented annotation or grading issues.

### Gaps
- I did not verify the exact post-repair accuracy figure in the Allemang and Sequeda 2024 follow-up (I recall roughly 72% with an explicit "I don't know" category, but did not confirm it this session).
- I found no independent measured benchmark for AtScale or LookML-backed agents; their accuracy statements are vendor claims I did not collect.
- I found no public benchmark on a financial-services schema (trades, positions, reference data).

## 3. Knowledge graphs and ontologies as context (GraphRAG, Palantir Ontology pattern, RDF/OWL vs property graphs)

### Takeaway
Two distinct graph patterns are in use. Ontology-over-structured-data (data.world, Palantir, FIBO) gives agents typed entities, relationships and governed actions and has the strongest measured accuracy evidence. GraphRAG-over-documents builds a graph from unstructured text to answer global "sensemaking" questions, with LLM-judged quality gains and very high indexing cost that newer variants reduce.

### Cited Findings
- The data.world result (16% to 54%) came from querying a knowledge-graph representation of the SQL schema, so it is evidence for the ontology-over-structured-data pattern. — [arXiv 2311.07509](https://arxiv.org/pdf/2311.07509)
- Palantir documents the Ontology as having semantic elements (objects, properties, links) and kinetic elements (actions, functions, dynamic security), in which human and agent actions are staged as scenarios, governed with the same granular access controls as data, and written back to enterprise systems. — [Palantir docs: Why create an Ontology?](https://www.palantir.com/docs/foundry/ontology/why-ontology); [Ontology system](https://palantir.com/docs/foundry/architecture-center/ontology-system/)
- Palantir's April 2026 blog describes the Ontology as designed to represent the decisions in an enterprise, not simply the data, and AIP agents read and write through the same model. — [Palantir blog](https://blog.palantir.com/connecting-agents-to-decisions-277dee8ddb40)
- Microsoft's LazyGraphRAG (Nov 2024) defers summarization to query time; Microsoft reports indexing cost identical to vector RAG and 0.1% of full GraphRAG, and at a relevance budget of 500 it beat vector RAG, RAPTOR and GraphRAG local, global and DRIFT search at about 4% of GraphRAG global-search query cost. — [Microsoft Research](https://www.microsoft.com/en-us/research/blog/lazygraphrag/)
- GraphRAG's original 72-83% comprehensiveness win rates over vector RAG were LLM-judged on two narrow corpora, and the authors acknowledge that generalization is unknown. — [Beancount research log, Jun 2026](https://beancount.io/bean-labs/research-logs/2026/06/04/graphrag-local-to-global-query-focused-summarization)
- One practitioner reports a $33,000 GraphRAG indexing bill for a legal dataset in early 2024; this is an anecdote, not a measured study. — [Medium, Graph Praxis](https://medium.com/graph-praxis/the-graphrag-cost-cliff-how-33-000-became-33-in-eighteen-months-be1b0fbe37e4)
- FIBO (EDM Council) is an open, governed OWL ontology of financial concepts. The Council's example is that "counterparty", "client" and "customer" mean different things across systems, and FIBO maps them to a shared Legal Entity or Party concept with explicit ownership and contract relationships. It includes classes such as CentralCounterpartyClearingHouse and BusinessIdentifierCode. The initiative is chaired by David Newman of Wells Fargo. — [EDM Council FIBO](https://edmcouncil.org/frameworks/industry-models/fibo/); [Knowledge Graph Conference](https://www.knowledgegraph.tech/?p=2789)
- An August 2026 arXiv paper ("Auditable by Construction") proposes an ontology-driven framework for LLM analytics in enterprise finance, cross-referencing its model with FIBO for consistency. — [arXiv 2608.20661](https://arxiv.org/pdf/2608.20661)
- LinkedIn's SQL Bot builds a knowledge graph from database metadata, query logs, wikis and code, and a text-to-SQL agent ranks context from it. — [arXiv 2507.14372](https://arxiv.org/pdf/2507.14372)

### Inferences
- RDF/OWL suits shared, standards-aligned vocabularies (FIBO, regulatory taxonomies) and formal reasoning, at the cost of tooling and skills scarcity. Property graphs (Neo4j-style) are easier for engineering teams and suit operational traversal (ownership chains, netting sets), but lack formal semantics. Many banks will meet both: FIBO-aligned concepts mapped onto a property graph or onto the semantic layer.
- The Palantir pattern adds something semantic layers lack, namely governed write actions. For agents that do more than read (booking an amendment, raising a break), an action layer with permissions is the relevant pattern.
- I did not find a measured comparison of RDF/OWL versus property graphs for LLM accuracy.

### Gaps
- No independent measured study of Palantir Ontology effect on agent accuracy was found; Palantir material is product documentation.
- Neo4j's own measured results (if any) were not retrieved.

## 4. Metadata catalogs, lineage and usage-derived context as agent context

### Takeaway
Production systems at OpenAI, LinkedIn, Uber and Pinterest converge on the same recipe: rank and summarize tables using query logs, owner annotations and code, scope retrieval by business domain, and let users confirm table selection. Usage-derived signals (popular queries, deprecation flags) do much of the work, but schema and descriptions alone are insufficient, and reported accuracy remains moderate.

### Cited Findings
- OpenAI's in-house data agent (published Jan 2026) uses six context layers: table usage metadata (schema, lineage, query history, with queries from popular dashboards ranked above one-off queries), human annotations by owners, Codex enrichment that reads pipeline code to infer derivation and freshness and when to prefer a similar table, institutional knowledge from Slack, Google Docs and Notion via an access-controlled retrieval service, memory of corrections scoped globally or personally, and runtime queries to the warehouse when offline context is stale. — [OpenAI](https://openai.com/index/inside-our-in-house-data-agent/); [ByteByteGo summary](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)
- Per secondary coverage, the first three layers are merged nightly into one embedded description per table, Codex enrichment runs in batches of 100-200 tables at 5-10 minutes each, tool count was cut from about 40 to 13 after overlapping tools produced conflicting answers, retrieving all historical queries hurt because most were one-offs, and prescriptive step-by-step prompts produced worse answers than stating the goal. Reported scale varies across secondary sources (about 70,000 to 90,000 datasets, 600 PB, 3,500 to 5,500 users). — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent); [The Decoder](https://the-decoder.com/openai-develops-six-layer-context-system-to-help-employees-navigate-600-petabytes-of-data/)
- OpenAI's team states that two near-identical tables can differ in meaning (for example, whether logged-out users are included), so schema alone is insufficient. No accuracy figures were published. — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)
- LinkedIn's SQL Bot draws on DataHub metadata (schemas, field descriptions, top-K values for categorical fields, partition keys, classifications), automatically ingests popular tables and uses DataHub deprecation signals to offboard datasets. Expert review found 53% of responses correct or close to correct on an internal benchmark, with over 300 weekly users. — [arXiv 2507.14372 (2025)](https://arxiv.org/pdf/2507.14372); [ZenML summary](https://www.zenml.io/llmops-database/building-a-production-text-to-sql-assistant-with-multi-agent-architecture)
- Uber's QueryGPT (Sep 2024) uses curated workspaces of tables and SQL samples per domain, an intent agent that routes to workspaces, a table agent whose choice users can edit, and a column-prune agent because Tier 1 tables exceed 200 columns (40-60K tokens). Its first version, k-NN retrieval of 3 tables and 7 SQL samples, lost accuracy as more tables were onboarded. It reports about 300 daily users and 78% saying it saved time, estimates query writing falls from about 10 to about 3 minutes, and publishes no overall accuracy. — [Uber Engineering](https://www.uber.com/en-us/blog/query-gpt/)
- Uber evaluates with a golden set of real questions with verified intent, tables and reference SQL, scoring intent accuracy, table overlap, successful execution, non-empty results and LLM-judged similarity, and it ignores run-to-run changes of about 5% as noise. — [Uber Engineering](https://www.uber.com/en-us/blog/query-gpt/)
- Pinterest built an offline vector index of table summaries and historical queries over top-tier tables only, retrieves top-N candidates, then has an LLM re-select top-K; secondary summaries report first-shot acceptance rising from about 20% to over 40%. I did not reach Pinterest's original post. — [ZenML summary](https://www.zenml.io/llmops-database/text-to-sql-system-with-rag-enhanced-table-selection); [Wren AI](https://getwren.ai/post/deep-dive-into-how-pinterest-built-its-text-to-sql-solution)

### Inferences
- Certification and tiering ("top-tier tables only", "Tier 1") act as the trust filter in every case. In a bank this maps to golden-source designations (for example, the books-and-records position store versus a risk-system copy) and should be an explicit metadata attribute the retriever filters on.
- Query logs are both the cheapest and the riskiest context: they encode real usage but also encode wrong and one-off queries, so they need ranking by author, frequency and dashboard use.
- Reported production accuracy (LinkedIn 53%, Pinterest about 40% first-shot) is far below small-benchmark semantic-layer figures, which supports keeping a human confirmation step for table selection.

### Gaps
- Airbnb and Netflix engineering posts on text-to-SQL or data context were not retrieved in this session.
- No source measured the isolated contribution of column descriptions or glossary terms to accuracy.

## 5. Unstructured enterprise knowledge: enterprise search indexes, permission-aware RAG and ACL propagation

### Takeaway
Permissions must be enforced before content enters the model context, normally by indexing document ACLs alongside chunks and pre-filtering at query time. The main failure mode is ACL drift between the source system and the index, plus leakage through caches, summaries and agent memory that sit outside the authorization boundary.

### Cited Findings
- Microsoft ISE (30 Apr 2026) describes SharePoint document-level access in RAG and notes that a revoked user may still see content in the index until the next ingestion run; mitigations are scheduled re-ingestion and webhooks or event receivers that re-index on permission change. — [Microsoft ISE blog](https://devblogs.microsoft.com/ise/sharepoint-doc-level-access/)
- Filtering after generation is insufficient because the model may already have seen restricted facts and can leak them through paraphrase or even through a refusal. — [tianpan.co, 19 Apr 2026](https://tianpan.co/blog/2026-04-19-pii-leak-rag-pipeline-access-control)
- Pre-filtering by ACL before similarity search is more efficient than post-filtering top-K, which wastes compute and can return sparse results; Elasticsearch document-level security, Azure AI Search security filters, Weaviate multi-tenancy and Pinecone metadata filters implement variants. — [DEV Community](https://dev.to/venkathub/permission-aware-rag-enforcing-document-acls-at-retrieval-time-54a7)
- Leakage paths include chunking, embeddings, caches, rerankers, summaries, tool outputs and agent memory, and role-only controls are often too coarse for inherited or attribute-based permissions; tests should cover revoked access and cross-tenant attempts. — [tianpan.co](https://tianpan.co/blog/2026-04-19-pii-leak-rag-pipeline-access-control)
- OpenAI routes institutional documents through an access-controlled retrieval service so the agent does not surface documents a user cannot see; it gives no equivalent detail for warehouse query permissions. — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)

### Inferences
- In capital markets, information barriers (private-side versus public-side, research versus trading) make ACL drift a regulatory issue, not just a privacy one. Cached summaries or GraphRAG community summaries built across documents with different entitlements are a specific risk, because a summary inherits no single document's ACL.
- Agent memory scoped "globally" (as at OpenAI) is a cross-user leakage channel unless memory writes are reviewed or scoped by entitlement.

### Gaps
- I found no measured study quantifying ACL drift or leakage rates in production RAG systems.

## 6. Reference architectures and the build versus buy decision

### Takeaway
The converging reference architecture has five layers: sources, ingestion into a lakehouse with lineage, a meaning layer (semantic layer plus ontology or knowledge graph plus catalog), a retrieval and serving layer exposed through APIs or MCP with entitlement enforcement, and agents with memory and feedback loops. Buying is favoured for catalogs and semantic layers; building is common for the retrieval, routing and memory logic, which is where firm-specific knowledge lives.

### Cited Findings
- a16z's build sequence (data access, automated context construction, human refinement, MCP/API exposure, self-updating flows) is the clearest published reference flow, and it names four supplier types: data platforms (Databricks, Snowflake), AI data analyst companies, dedicated context-layer startups that must rebuild context per customer, and in-house builds such as OpenAI's, with Palantir's ontology as an established example. It states "not every enterprise can (or should) build this in house". — [a16z](https://a16z.com/your-data-agents-need-context/)
- OpenAI's lesson, as reported, is that the foundation (unified data, a monorepo of pipeline code, strong table annotations) mattered more than the agent itself, and that a migration period required explicit tracking of which table copy was authoritative. — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)
- Gartner's Robert Thanaraj reportedly said point solutions are disappearing and being absorbed as platform features. — [Sequeda recap](https://juansequeda.substack.com/p/gartner-data-and-analytics-march)
- dbt Labs recommends routing: check whether the semantic layer can answer, then whether a small modeling change would close the gap, and fall back to text-to-SQL only after that. — [dbt Labs blog](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- OSI aims to let semantic definitions move between tools, which would reduce lock-in to any one semantic-layer vendor. — [Business Wire](https://www.businesswire.com/news/home/20250923902448/en/Snowflake-Salesforce-dbt-Labs-Revolutionize-Data-Readiness)

### Inferences
- Cost centres differ by layer. Semantic modeling and ontology design are human-expert costs that scale with the number of governed concepts. GraphRAG indexing is an LLM compute cost that LazyGraphRAG-style deferral reduces by orders of magnitude. Codex-style enrichment converts documentation cost into batch compute (OpenAI's 5-10 minutes per table).
- A reasonable financial-services layering is: golden-source reference data (instruments, legal entities with LEI, counterparties, books) as the ontology core; trade, position and risk metrics in a semantic layer; policies, ISDA/CSA terms and procedures in a permission-aware document index; and decision traces (for example, why a limit breach was approved) in a context graph.

### Gaps
- I found no published total-cost-of-ownership comparison of build versus buy for a context layer.

## 7. Known failure modes: stale metadata, conflicting definitions, schema drift, permission leakage and cost of curation

### Takeaway
The documented failures are mostly organisational rather than model failures: outdated semantic definitions, competing "authoritative" tables, too many overlapping tools, noisy query history, ACL drift and the ongoing expense of human curation. Benchmark annotation errors are an additional risk when choosing approaches by leaderboard.

### Cited Findings
- Stale and incomplete semantic definitions: a16z's example semantic-layer YAML was outdated, unused and missing two product lines, and finance's revenue table competed with a materialized view. — [a16z](https://a16z.com/your-data-agents-need-context/)
- Conflicting tools and context: OpenAI's agent picked wrong tools and returned conflicting answers with about 40 tools until overlap was removed. — [ByteByteGo](https://blog.bytebytego.com/p/how-openai-built-its-data-agent)
- Retrieval degradation with scale: Uber's similarity-search approach lost accuracy as more tables were onboarded, and hallucinated tables and columns persisted. — [Uber Engineering](https://www.uber.com/en-us/blog/query-gpt/)
- Coverage failure: the semantic layer scored 0% on multi-hop questions outside its model. — [dbt Labs blog](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- Silent wrong answers: text-to-SQL returns plausible incorrect results with no guardrail. — [dbt Labs blog](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026)
- Permission leakage via stale index ACLs after revocation. — [Microsoft ISE](https://devblogs.microsoft.com/ise/sharepoint-doc-level-access/)
- Benchmark unreliability: a 62.8% estimated annotation error rate on Spider 2.0-Snow. — [arXiv 2601.08778](https://arxiv.org/html/2601.08778v3)
- Gap between claimed and usable context: one vendor survey reports 88% of organizations claim their context is operational while 61% delay AI initiatives because it is not usable (vendor survey, treat with caution). — [Upriver](https://www.upriverdata.com/blog/the-ai-context-layer-won-t-build-itself)

### Inferences
- Schema drift is handled in the documented systems by nightly regeneration (OpenAI), deprecation signals (LinkedIn) and runtime fallback queries, not by manual upkeep. A context layer without an automated refresh path will decay.
- In capital markets the conflicting-definition problem is acute: "notional", "exposure", "position" (trade-date versus settlement-date) and "counterparty" (legal entity versus parent group) each have several legitimate definitions, so the context layer must carry the definition and its owner, not just the column.

### Gaps
- I found no quantified measure of the curation cost (person-hours per governed metric or entity) from any primary source.
- No source measured how quickly context accuracy decays without refresh.
