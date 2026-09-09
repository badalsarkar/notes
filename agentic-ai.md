# Agentic AI and the Move Beyond Vector Search

Research report, August 2026. Related notes: [genai.md](genai.md),
[genai-architecture.md](genai-architecture.md), [ai-security.md](ai-security.md).

## 1. What this report covers

Between 2023 and 2024, most people building applications on large language models used the
same design: split documents into chunks, convert each chunk into a vector, store the vectors
in a database, and at question time find the chunks whose vectors are closest to the question.
That design is called RAG (retrieval-augmented generation).

Since then the design has changed. This report explains what changed, what the alternatives
are, what each one costs, and where each one is a reasonable choice. Examples are drawn from
capital markets, because the trade-offs are easier to judge against concrete work.

## 2. Summary

Vector search has not been replaced. It has been reduced in scope. It used to be the whole
architecture. It is now one retrieval method among several, and the system decides which one
to use for a given question.

Three things drove the change.

First, the software calling the retriever is now an agent rather than a person. An agent can
run a search, look at the result, decide it was not useful, and search again. A one-shot
similarity lookup was designed for a workflow that no longer applies.

Second, similarity search cannot follow relationships. If a question requires connecting a
fund to its holdings, then those holdings to their issuers, then those issuers to a parent
company, no amount of embedding quality will do it. This is why graph databases came back
into the discussion.

Third, agents now run for a long time and accumulate history. The problem shifted from
finding the right document to managing what stays in the model's context window across many
steps. This work is generally called context engineering.

## 3. The methods

### 3.1 Vector search (classic RAG)

**How it works.** Documents are split into chunks. An embedding model turns each chunk into a
list of numbers. At question time the question is embedded the same way, and the database
returns the chunks with the nearest vectors.

**Strengths.** It handles paraphrase well. A question about "borrowing costs" will find a
passage about "financing expense" without anyone writing a synonym list. It scales to millions
of documents with predictable latency, usually well under a second. It is simple to operate
and every cloud provider offers a managed version.

**Weaknesses.** Chunking discards document structure, which matters for filings and term
sheets where meaning depends on which section a sentence sits in. Embeddings lose precision on
identifiers, so a search for a specific ISIN or trade ID may return chunks that are merely
about similar instruments. It returns a fixed number of results and has no way to recognise
that none of them answered the question. It cannot follow a chain of relationships. It has no
concept of time, so a superseded fact and a current fact look identical. Finally, the index
goes stale, and changing the embedding model means re-embedding the entire corpus.

**Cost.** Embedding is a one-off cost per document plus a recurring cost for updates. Storage
is the main ongoing line item at large volumes. Query cost is low.

**Capital markets example.** An analyst asks, "What did management say about net interest
margin pressure on recent earnings calls?" This is a good fit. The question is answered by a
passage, the wording will vary between transcripts, and there is no relationship to follow.

### 3.2 Hybrid search

**How it works.** Run a keyword search (usually BM25) and a vector search over the same
corpus, combine the two result lists, then use a reranking model to order the combined set.

**Strengths.** It fixes the most common failure of pure vector search. Keyword search finds
exact strings such as CUSIPs, LEIs, trade references and error codes, which embeddings blur.
Vector search finds the paraphrases that keyword search misses. Metadata filters can be
applied at the same time, so a query can be restricted to one asset class, one date range or
one entitlement group before ranking happens.

**Weaknesses.** More components to tune and operate. Reranking adds latency, typically tens to
low hundreds of milliseconds. Combining two ranked lists requires a fusion method, and getting
the weighting right takes evaluation work.

**Cost.** Modestly higher than pure vector search. The reranker is the main addition.

**Capital markets example.** A compliance officer asks for all internal communications
referencing a specific deal codename and the associated ticker over a date window. The
codename is an exact string that only keyword search will find reliably; the surrounding
discussion is paraphrase that only vector search will find. Entitlement filters must be
applied at query time. Hybrid search handles all three.

As of 2026 this is the standard baseline for production systems. Most organisations should
build this first and measure it before considering anything more elaborate.

### 3.3 Agentic search over files and keyword indexes

**How it works.** No pre-built index of embeddings. The agent is given tools such as list
directory, pattern-match filenames, keyword search within files, and read a specific file or
page range. It plans a search, runs it, reads what came back, refines the search, and repeats
until it has enough to answer.

**Strengths.** Nothing to build or keep in sync, so there is no staleness problem and no
re-embedding when a model changes. The model itself judges relevance at each step, and it gets
many attempts instead of one. It works directly on the source documents, so structure and
tables are preserved. Two published results support the approach. A 2026 Amazon Science paper
found an agent using only keyword search reached about 94.5% of the faithfulness of a
conventional RAG system with no vector database at all, and on FinanceBench, a set of long
financial filings with many tables, it scored higher on answer correctness (30.4% against
24.2%). A LlamaIndex benchmark found that on a small document set an agent with filesystem
tools scored 8.4 out of 10 on correctness against 6.4 for RAG.

**Weaknesses.** It is slower, because every step is another model call. In the LlamaIndex test
the agent averaged 11.2 seconds against 7.4 seconds for RAG on the same questions. Cost scales
with how much exploration the agent does, and that is variable rather than fixed. Most
importantly, it does not scale to large corpora. The same benchmark found that at 100 and
again at 1,000 documents, conventional RAG was faster and no worse on quality. Keyword search
also has no recall on paraphrase, so if the agent guesses the wrong terms it finds nothing.

**Cost.** No indexing cost. Query cost is higher and less predictable than any indexed method.

**Capital markets example.** A settlement break needs investigating. The relevant material is
a known, bounded set: the trade record, the confirmation, the SWIFT messages, the custodian
statement and the counterparty's standing settlement instructions. The agent can open each in
turn, compare fields and identify the mismatch. Building a vector index over this would add
nothing, because the agent already knows which documents matter.

The distinction that matters is corpus size and whether the agent can name the documents it
needs. When it can, indexing is wasted effort. When it cannot, indexing is necessary.

### 3.4 GraphRAG

**How it works.** An extraction step reads the corpus and produces a graph: entities become
nodes, relationships between them become edges. Some implementations then group the graph into
clusters and write a summary of each cluster. At question time the system retrieves a portion
of the graph, or the relevant summaries, rather than raw chunks.

**Strengths.** It answers two classes of question that vector search cannot. The first is
multi-hop: questions requiring two or more relationship steps. The second is corpus-wide
summarisation: questions whose answer is not in any single passage but is distributed across
many. Graph output is also more explainable, because the answer can be traced back through
named entities and named relationships rather than a similarity score.

**Weaknesses.** The extraction step is expensive and imperfect. Entity resolution is the main
difficulty in practice: deciding that "JPMorgan Chase & Co.", "JPM" and a given LEI are the
same node is not trivial, and errors propagate into every answer. Rebuilding the graph when
documents change is costly. For simple lookup questions the graph adds cost without adding
accuracy.

**Cost.** This has changed substantially. Indexing one corpus with the original Microsoft
GraphRAG cost roughly $33,000 in early 2024. Later variants reduced this by orders of
magnitude. Microsoft's LazyGraphRAG uses noun-phrase extraction rather than a model for the
indexing step and defers all model work to query time; its indexing cost is the same as vector
RAG, and its global queries are reported at roughly 1/700th of the cost of full GraphRAG at
comparable quality. LightRAG and Fast GraphRAG take similar approaches. If graphs are being
evaluated in 2026, the lazy variants are the relevant baseline, not the 2024 design.

**Evidence on when it helps.** GraphRAG-Bench, published at ICLR 2026, is the most useful
reference here, and its headline finding is that GraphRAG often underperforms plain RAG on
ordinary tasks. The breakdown:

| Task type | Plain chunks | Graph | Difference |
|---|---|---|---|
| Simple fact retrieval | 60.9 | 60.1 | none in practice |
| Single-hop question answering (F1) | 64.8 | 63.0 | slightly worse |
| Complex reasoning | 42.9 | 53.4 | +10.5 |
| Contextual summarisation | 51.3 | 64.4 | +13.1 |
| Multi-hop retrieval (Recall@5) | 73.4% | 87.8% | +14.4pp |

The pattern is consistent: graphs help when the question requires connecting things or
covering everything, and do not help otherwise.

**Capital markets example where it helps.** A risk manager asks, "What is our total exposure
to entities ultimately controlled by a given parent company?" Answering this means walking a
legal entity hierarchy through subsidiaries and holding companies, then joining to positions,
then aggregating. Every step is a relationship traversal. Similarity search cannot perform any
of them.

**Capital markets example where it does not help.** "What is the coupon on this bond?" is a
lookup. A graph adds build cost, query latency and a new failure mode, and returns the same
answer a keyword search would have.

### 3.5 Agentic GraphRAG

**How it works.** Rather than the system building one subgraph and handing it to the model,
the graph is exposed as a set of tools: a vector index over node descriptions, a set of
parameterised queries, and a natural-language-to-query translator such as Text2Cypher. The
agent chooses which to call, inspects the result and traverses further if needed.

**Strengths.** It handles questions whose shape was not anticipated at design time. It also
avoids a practical problem with plain GraphRAG, which is that retrieving a large subgraph can
exceed the context window. Research systems in this area, such as Graph-O1, use search
algorithms to expand only the most promising parts of the graph. Reported gains over agentic
vector RAG baselines cover correctness, recall and multi-turn consistency.

**Weaknesses.** Generated queries can be wrong in ways that are hard to detect, and a wrong
query returns a confident but incorrect answer. Multi-turn traversal is slow. It requires a
maintained graph schema, which is an ongoing data engineering commitment rather than a
one-time build.

**Capital markets example.** A credit analyst working through a counterparty's group structure
asks a series of connected questions: who owns this entity, what other entities share that
owner, what is our aggregate exposure across them, and which of those have collateral
agreements. Each question depends on the answer to the previous one, and the sequence is not
known in advance.

### 3.6 Temporal knowledge graphs for agent memory

This is a separate use of graphs. Here the graph is not an index over a document corpus; it is
the agent's memory of what it has learned about a user, an account or a process.

**How it works.** Facts are stored as edges in a graph, and each edge carries a validity
period: when the fact became true and, if applicable, when it stopped being true. When new
information contradicts an existing fact, the old edge is marked invalid rather than deleted,
so the history remains available.

**Strengths.** It handles change and contradiction, which a vector store cannot. An embedding
of "the client's mandate excludes emerging market debt" and an embedding of the same sentence
from two years ago are indistinguishable, so a vector memory will retrieve whichever is
closer to the question and may return the outdated one. A temporal graph knows which is
current and can also answer questions about the past. On LongMemEval, a benchmark covering
temporal, multi-hop and knowledge-update questions, Zep's temporal graph scored 63.8% against
Mem0's 49.0%.

**Weaknesses.** It adds a stateful service to maintain. Extracting facts reliably from
conversation is imperfect, and a wrong fact written into memory persists and affects later
answers. Research published in 2026 covers memory contamination as a live security concern,
which is relevant if any part of the input is untrusted.

**Capital markets example.** A sales assistant supporting a coverage team needs to know the
client's current restrictions, current benchmark, current authorised traders and current
settlement instructions, while still being able to answer why a past trade was structured a
certain way. All of these change over time, and using a superseded value would cause a real
error rather than an unhelpful answer.

### 3.7 Ontologies and semantic layers

**How it works.** Rather than indexing documents, the organisation defines its business
objects and their relationships explicitly: what an instrument is, what a position is, what a
counterparty is, how they relate, and what operations are permitted on each. The agent works
against this layer rather than against raw tables or documents.

**Strengths.** It gives agents access to authoritative data with consistent definitions,
rather than whatever a document happened to say. Because permissions and permitted actions are
part of the model, the agent can be allowed to take actions with governance and an audit trail
rather than only producing text. It removes the ambiguity that causes most enterprise agent
failures, where two systems define "notional" or "exposure" differently. Palantir's Ontology
is the best-known commercial implementation of this pattern.

**Weaknesses.** It is a large, slow programme of work involving data modelling and
organisational agreement, not a technical component that can be installed. It does not help
with unstructured text, so it complements retrieval rather than replacing it.

**Analyst view.** Gartner has placed semantic layers alongside data platforms as core
infrastructure and predicts that by 2028 around 60% of agentic analytics projects relying only
on the Model Context Protocol will fail because there is no consistent semantic layer beneath
it. Gartner also uses the term "context graph" for a knowledge graph extended with decision
traces and workflow history, and predicts over half of enterprise agent systems will use one
by 2028. These are vendor-adjacent forecasts and should be read as direction rather than
measurement, but the underlying observation is reasonable: connecting an agent to a warehouse
without agreed definitions produces confident and inconsistent answers.

**Capital markets example.** A portfolio agent is asked to rebalance towards a target duration.
Producing a written recommendation requires only retrieval. Actually staging the orders
requires knowing what a position is, which accounts are in scope, what the mandate permits,
what pre-trade compliance checks apply and who is authorised to approve. That information is
structural, not textual.

### 3.8 Reinforcement learning applied to search

Rather than instructing a model when to search, the search policy is trained. Search-R1
reported roughly a 24% relative improvement over conventional RAG by training the model to
interleave reasoning and retrieval with outcome-based rewards. Work published in 2026, such as
AutoSearch and Search-P1, is mostly concerned with the resulting inefficiency, since trained
agents tend to search more than necessary.

This matters as a direction but is not yet a normal build option for most teams. It requires
training infrastructure and a reward signal, and the frontier models available through APIs
increasingly include this behaviour already.

### 3.9 Long context instead of retrieval

A reasonable question is whether large context windows remove the need for retrieval. The
evidence says no. Chroma's context rot study tested 18 frontier models and found all of them
degraded as input length grew, with accuracy dropping by more than 30% when the relevant
information sat in the middle of a long input. Effective usable context is generally well
below the advertised maximum. Long context raises the ceiling but does not remove the need to
select what goes into the window.

## 4. Side-by-side comparison

| Method | Best for | Latency | Build cost | Ongoing cost | Main risk |
|---|---|---|---|---|---|
| Vector search | Paraphrase-heavy lookup at scale | Low | Low | Embedding refresh | Misses exact identifiers; no multi-hop |
| Hybrid search | General production retrieval | Low–medium | Medium | Index plus reranker | Tuning and fusion weighting |
| Agentic file search | Small, known, structured document sets | High | None | Per-query tokens | Does not scale; keyword recall gaps |
| GraphRAG (lazy variants) | Multi-hop and corpus-wide questions | Medium | Medium | Graph rebuild | Entity resolution errors |
| Agentic GraphRAG | Open-ended relationship exploration | High | High | Schema maintenance | Silently wrong generated queries |
| Temporal graph memory | Facts that change over time | Medium | Medium | Stateful service | Bad facts persist |
| Ontology / semantic layer | Agents that take actions | Low | Very high | Governance | Programme cost and timeline |

## 5. Worked capital markets scenarios

**Research question answering over filings and transcripts.** Large corpus, paraphrase-heavy,
mostly single-passage answers. Hybrid search with a reranker. Add graph retrieval only for the
subset of questions that span issuers or supply chains. Note that tables in filings are a
known weakness of chunk-based retrieval; either use a parser that preserves table structure or
let the agent open the source document directly for numeric questions.

**Counterparty and beneficial ownership analysis.** Inherently relational. A knowledge graph
built on entity identifiers, with the agent traversing it through query tools. Document
retrieval supports this rather than driving it. This is the clearest case in capital markets
for graph technology, and it is also the case where entity resolution quality determines
whether the system works at all.

**Trade surveillance.** Requires connecting communications, orders, executions and market
events across time. Graph structure for the relationships, temporal handling because sequence
and timing carry the meaning, and hybrid search over the communications text. Vector search
alone is not sufficient because the question is about connections between records, not about
the content of one record.

**Post-trade exception handling.** Bounded document set per case, known in advance. Agentic
search over the actual records. No index needed. If the agent is expected to correct the break
rather than describe it, the action layer needs the structure described in section 3.7.

**Client coverage assistant.** Needs current state that changes: mandates, restrictions,
contacts, instructions. Temporal graph memory, plus hybrid retrieval over research and past
correspondence.

## 6. Practical build order

1. Build hybrid retrieval with a reranker and metadata filters. Measure it against a set of
   real questions from the intended users.
2. Categorise the failures. If the system is failing on exact identifiers, fix the lexical
   side. If it is failing because answers require connecting records, that is the case for a
   graph. If it is failing because it retrieved an outdated fact, that is the case for
   temporal memory.
3. Add graph retrieval only for the query patterns that failed structurally, and use a lazy
   indexing variant so the build cost is comparable to vector indexing.
4. Expose each retrieval method as a separate tool and let the agent choose. Route rather than
   replace. Published evaluations consistently find that combining graph and chunk retrieval
   beats either alone.
5. Take on ontology and semantic layer work only when agents need to take actions on business
   objects, and treat it as a data programme with its own timeline.

## 7. Operational considerations

**Tool count.** As agents gain tools, the tool definitions themselves consume context. A
typical multi-system setup can reach roughly 50,000 tokens of tool schemas, and selection
accuracy declines once an agent has more than about 30 to 50 tools available. The current fix
is to search over tool descriptions and load only the relevant schemas, which reduces tool
tokens by around 85%. This is the same retrieval problem applied one level up.

**Adoption reality.** MIT's study found that around 95% of enterprise generative AI pilots
produced no measurable return, and Gartner expects more than 40% of agentic AI projects to be
cancelled by the end of 2027. The reported causes are mostly organisational rather than
technical: unclear ownership, no measurable objective, and workflow change that was not
planned for. The systems that succeed are generally connected to authoritative internal data
and to real operations, which is the practical argument behind the ontology work in section
3.7.

**Security.** Retrieval and memory both expand the attack surface. Retrieved content can carry
prompt injection, and memory systems can be poisoned so that a false fact affects later
sessions. Entitlements must be enforced at retrieval time, not by asking the model to respect
them. See [ai-security.md](ai-security.md).

## 8. Sources

- [Effective context engineering for AI agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [LazyGraphRAG — Microsoft Research](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/)
- [When to use Graphs in RAG (GraphRAG-Bench, ICLR 2026)](https://arxiv.org/pdf/2506.05690) — [benchmark repo](https://github.com/GraphRAG-Bench/GraphRAG-Benchmark)
- [Keyword search is all you need — Amazon Science, AAAI 2026](https://www.amazon.science/publications/keyword-search-is-all-you-need-achieving-rag-level-performance-without-vector-databases-using-agentic-tool-use)
- [Did filesystem tools kill vector search? — LlamaIndex](https://www.llamaindex.ai/blog/did-filesystem-tools-kill-vector-search)
- [Zep: a temporal knowledge graph architecture for agent memory](https://arxiv.org/abs/2501.13956)
- [Context Rot — Chroma](https://www.trychroma.com/research/context-rot)
- [When GraphRAG beats vector RAG — VentureBeat](https://venturebeat.com/orchestration/stop-graphing-everything-when-graphrag-actually-beats-vector-rag)
- [From RAG to context — RAGFlow year-end review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context)
- [Gartner on context graphs](https://atlan.com/know/gartner-context-graphs/)
- [Beyond semantic similarity: agentic search via direct corpus interaction](https://arxiv.org/pdf/2605.05242)
- [neo4j-graphrag-python](https://github.com/neo4j/neo4j-graphrag-python)
- [20 advanced RAG types — Turing Post](https://www.turingpost.com/p/ragtypes)
