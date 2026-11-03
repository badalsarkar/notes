# Databases and Tools for an Enterprise Context Layer

Research report, October 2026. Related notes: [agentic-ai.md](agentic-ai.md),
[sdlc-context-graph.md](sdlc-context-graph.md), [genai-architecture.md](genai-architecture.md),
[postgresql.md](postgresql.md), [mongodb.md](mongodb.md),
[datastore-SingleStore.md](datastore-SingleStore.md).

## Contents

- [1. What this report covers](#1-what-this-report-covers)
- [2. Summary](#2-summary)
- [3. What a context layer is made of](#3-what-a-context-layer-is-made-of)
- [4. Graph databases](#4-graph-databases)
- [5. Vector and search databases](#5-vector-and-search-databases)
- [6. General-purpose databases with vector and graph support](#6-general-purpose-databases-with-vector-and-graph-support)
- [7. Agent memory layers](#7-agent-memory-layers)
- [8. Semantic layers, catalogs and packaged context platforms](#8-semantic-layers-catalogs-and-packaged-context-platforms)
- [9. Side-by-side comparison](#9-side-by-side-comparison)
- [10. Worked capital markets scenarios](#10-worked-capital-markets-scenarios)
- [11. Reference combinations](#11-reference-combinations)
- [12. Selection risks and checklist](#12-selection-risks-and-checklist)
- [Resources](#resources)

## 1. What this report covers

- This report surveys the products that organisations use to build a context layer for AI agents.
  - A context layer is the set of stores and services that decide what an agent knows at the moment it acts: which documents it can retrieve, which entities and relationships it can traverse, what it remembers from earlier sessions, and which business definitions and permissions apply.
  - The report compares products by category: graph databases, vector and search databases, general-purpose databases with vector and graph extensions, agent memory layers, and semantic layers and catalogs.
  - Each product is described with the same structure: how it works, strengths, weaknesses, cost and licence, and a capital markets example.
- The report does not repeat the retrieval methods themselves.
  - [agentic-ai.md](agentic-ai.md) already covers vector search, hybrid search, GraphRAG, temporal knowledge graphs, ontologies and long context as techniques, with benchmark results.
  - [sdlc-context-graph.md](sdlc-context-graph.md) already covers code graphs and work graphs in software delivery, including Uber, Atlassian and Sourcegraph.
- Most published comparisons in this category are written by vendors, and most of them rank their own product first.
  - Atlan, DataHub, Airbyte, Cognee and FalkorDB have all published "best of 2026" lists that place themselves at or near the top.
  - Performance figures quoted below are vendor-reported unless the bullet says otherwise, and they should be treated as claims to verify in a proof of concept.

## 2. Summary

- No single database is a context layer on its own, and every serious implementation combines at least two kinds of store.
  - A vector or hybrid search index handles unstructured text such as research notes, filings and emails.
  - A graph or relational model handles entities and their relationships, such as legal entity hierarchies, accounts and mandates.
  - A semantic layer or catalog holds the agreed definitions of business terms, metrics and permissions.
  - A memory store holds what agents have learned during earlier interactions, and it needs to track when each fact was true.
- The most popular choices in 2026 fall into a small number of defaults.
  - Neo4j is the most widely adopted graph database for this purpose, and in October 2026 it launched a packaged Context Engine with a predefined business ontology and graph-native memory, currently in private preview.
  - PostgreSQL with pgvector is the most common starting point for teams that already run Postgres, and it covers vector search, keyword search and relational data in one system up to roughly 100 million vectors.
  - Among dedicated vector databases, Pinecone is the managed default, Qdrant and Weaviate are the most common open-source choices, Milvus is chosen for billion-scale workloads, and turbopuffer has become the low-cost option for workloads with many mostly-idle tenants.
  - Mem0 is the most widely used agent memory library, and Zep with its open-source Graphiti engine is the main choice when facts change over time.
  - Snowflake, Databricks and Microsoft each now ship a semantic or ontology layer inside their own platform, and the Open Semantic Interchange specification, now Apache Ossie, is the attempt to make those definitions portable between them.
- The market is moving from databases towards packaged context products.
  - Neo4j Context Engine, Pinecone Nexus, AWS Context, Microsoft Fabric IQ and Glean's Enterprise Graph all sell a pre-assembled layer rather than a storage engine.
  - These products reduce build time, but they also tie the organisation's business ontology to one vendor's model, and most of them are less than six months old.
- The hardest problems are not storage problems.
  - Entity resolution, keeping the layer current, and enforcing the same access control that the source systems enforce are the issues that decide whether a context layer is trustworthy, and no product removes them.

## 3. What a context layer is made of

- A context layer has five logical stores, and products differ in how many of them they cover.
  - **Document and passage index.** This store holds chunks of unstructured text with embeddings and keyword indexes, and it answers "find passages about this topic".
  - **Entity and relationship graph.** This store holds business objects and typed relationships between them, and it answers multi-hop questions such as "which funds are exposed to this issuer through subsidiaries".
  - **Semantic definitions.** This store holds governed definitions of metrics, dimensions and business terms, such as what "net exposure" means and how it is calculated.
  - **Agent memory.** This store holds facts learned during interactions, with validity periods, so that an agent can distinguish the client's current restrictions from superseded ones.
  - **Metadata, lineage and policy.** This store holds where data came from, who owns it, how sensitive it is and who may see it, and it is what a data catalog provides.
- The Model Context Protocol (MCP) is the common interface between these stores and the agent.
  - Neo4j, Pinecone, Qdrant, Weaviate, MongoDB, Glean, Atlan and most other products in this report now ship an MCP server.
  - MCP has no built-in authorisation, audit logging or rate limiting, as [sdlc-context-graph.md](sdlc-context-graph.md) section 5.4 notes, so a regulated deployment needs a gateway or the database's own access control in front of it.
- Choosing a context layer is therefore a question of which of the five stores each product covers well, and which ones the organisation will build or buy separately.

## 4. Graph databases

### 4.1 Neo4j

- **How it works.**
  - Neo4j is a native property graph database queried with Cypher, which is now the basis of the ISO GQL standard.
  - It includes vector indexes alongside the graph, so a query can find similar passages and then traverse from them to related entities in one statement.
  - Every Aura cloud instance has included a hosted MCP server since August 2026, with OAuth and configurable permissions.
  - The [Neo4j Context Engine](https://neo4j.com/press-releases/neo4j-context-engine/), announced on 20 October 2026 and in private preview, adds a predefined six-layer business ontology, short-term, long-term and reasoning memory, and decision tracking on top of the database.
- **Strengths.**
  - It has the largest developer ecosystem of any graph database, with integrations in LangChain, LlamaIndex, Graphiti, Cognee and most agent frameworks.
  - The Graph Data Science library provides community detection, centrality and path algorithms that are useful for entity resolution and for GraphRAG community summaries.
  - Role-based access control can be applied at the label and property level in the Enterprise edition, which matters when different desks may see different parts of the graph.
- **Weaknesses.**
  - Ingestion from many source systems and keeping the graph current require custom pipelines, and this is where most of the effort goes.
  - Horizontal scaling of writes is more limited than in distributed databases, and very large graphs require careful sharding with Neo4j Fabric or the newer composite databases.
  - The Context Engine is new and in private preview, so its ontology model and pricing are not yet proven in production.
- **Cost and licence.**
  - The Community edition is GPLv3 and lacks clustering and fine-grained security.
  - The Enterprise edition and AuraDB are commercial, and enterprise pricing is negotiated.
- **Capital markets example.**
  - Neo4j fits a beneficial ownership and counterparty hierarchy, where an agent must answer which ultimate parent a trade rolls up to, across several layers of subsidiaries and joint ventures, before checking a credit limit.
  - Neo4j does not fit a store of five years of tick data or trade blotters, which are wide, append-heavy and analysed by time, and belong in a columnar store such as [clickhouse.md](clickhouse.md) or kdb+.

### 4.2 Amazon Neptune and AWS Context

- **How it works.**
  - Neptune Database is a managed transactional graph database that supports both property graphs with openCypher and Gremlin, and RDF with SPARQL.
  - Neptune Analytics is a separate in-memory engine for graph algorithms and vector search, and it is the store behind GraphRAG in Amazon Bedrock Knowledge Bases.
  - [AWS Context](https://thenewstack.io/aws-context-knowledge-graph-agents/), announced in June 2026, is a separate product that automatically maps relationships across tables, columns and business rules in the Glue Data Catalog, SageMaker and Lake Formation, and exposes them to agents with existing permissions.
  - The AWS Context Ontology Accelerator is open source under Apache 2.0, uses W3C standards and targets Neptune.
- **Strengths.**
  - It is fully managed and integrates with IAM, VPC isolation and existing AWS governance, which simplifies approval in firms that are already on AWS.
  - Support for both RDF and property graphs means one service can host a formal ontology and an operational graph.
  - AWS Context reuses Lake Formation permissions, so the agent sees only what the user could already see.
- **Weaknesses.**
  - It is available only on AWS, and moving a graph out later requires rewriting queries if Gremlin was used.
  - The ecosystem and tooling are smaller than Neo4j's, and Neptune Analytics graphs must fit in memory.
  - AWS Context availability was described as preview or "coming soon" by different sources in mid-2026, so its status should be confirmed before planning around it.
- **Cost and licence.**
  - Neptune is billed per instance hour or per serverless capacity unit, plus storage and I/O, and Neptune Analytics is billed by provisioned memory.
- **Capital markets example.**
  - Neptune fits a firm whose data lake and trade data already sit in S3 and Glue, and which wants a governed graph of instruments, issuers and reference data without adding another vendor.
  - Neptune does not fit a multi-cloud bank that must run the same context layer on premises for regulatory reasons, because it has no self-hosted option.

### 4.3 FalkorDB and Memgraph

- **How it works.**
  - FalkorDB is a graph database that runs as a Redis module and represents adjacency as sparse matrices, using linear algebra for traversal, and it supports openCypher.
  - Memgraph is an in-memory graph database that is compatible with Cypher and the Neo4j Bolt protocol, and it is aimed at streaming and real-time graph workloads.
  - FalkorDB is a supported backend for Graphiti, Zep's temporal memory engine, and ships its own GraphRAG SDK.
- **Strengths.**
  - Both are designed for low-latency traversal, which suits agents that issue many small graph queries per task.
  - Memgraph can ingest directly from Kafka, so the graph can stay close to real time without a separate batch pipeline.
  - Cypher compatibility reduces lock-in, because queries can often move to or from Neo4j with modest changes.
- **Weaknesses.**
  - Both are smaller companies with smaller ecosystems than Neo4j.
  - In-memory designs make very large graphs expensive, because RAM rather than disk is the limit.
  - FalkorDB's published performance comparisons with Neo4j are vendor benchmarks and have not been independently reproduced.
- **Cost and licence.**
  - FalkorDB is published under the Server Side Public License, which restricts offering it as a hosted service, and it has a commercial cloud.
  - Memgraph's core is under the Business Source License, with an enterprise edition for security and high availability.
- **Capital markets example.**
  - Memgraph fits real-time trade surveillance, where an agent investigating a possible wash trade needs the current graph of accounts, beneficial owners and orders as events arrive from Kafka.
  - Neither fits a long-term regulatory archive that must be held for seven years, because RAM-resident storage is the wrong cost profile for cold data.

### 4.4 Google Spanner Graph

- **How it works.**
  - Spanner Graph adds a graph model and GQL queries to Spanner, Google's globally distributed relational database, so the same rows can be queried as tables or as a graph.
  - Google's reference architectures pair Spanner Graph with session storage and Memory Bank on the Gemini Enterprise Agent Platform, and graph algorithms were announced in preview.
- **Strengths.**
  - It inherits Spanner's horizontal scale, strong consistency and high availability, which few graph databases match.
  - There is no separate copy of the data, because the graph is a view over relational tables that the operational system already writes.
- **Weaknesses.**
  - It is available only on Google Cloud, and Spanner's cost is high for small workloads.
  - Graph analytics tooling is less mature than Neo4j's, and agent memory is a separate service rather than part of the database.
- **Cost and licence.**
  - It is billed as Spanner compute and storage, with no separate graph charge.
- **Capital markets example.**
  - Spanner Graph fits a global payments or settlement platform already on Spanner, where the agent needs to traverse the same live data that the settlement engine writes.
  - It does not fit a team that only needs a few million nodes for a research assistant, because the minimum cost is out of proportion to the workload.

### 4.5 RDF knowledge graph platforms: Stardog and Graphwise GraphDB

- **How it works.**
  - These platforms store data as RDF triples, query it with SPARQL, and apply OWL and rule-based reasoning to infer facts that were not stated explicitly.
  - Stardog adds virtualisation, so the graph can query relational sources in place rather than copying them, and an LLM interface called Voicebox.
  - Graphwise was formed from the merger of Ontotext and the Semantic Web Company, and combines GraphDB with the PoolParty taxonomy tools.
- **Strengths.**
  - They support formal ontologies and standards such as FIBO, the Financial Industry Business Ontology maintained by the EDM Council, which gives a ready-made vocabulary for instruments, legal entities and contracts.
  - Reasoning lets the graph derive facts such as "this entity is a subsidiary of that group" from a chain of ownership statements, which is useful for regulatory classification.
  - Virtualisation avoids the staleness problem for sources that can be queried live.
- **Weaknesses.**
  - SPARQL and OWL require specialist skills that most engineering teams do not have.
  - Reasoning over large graphs can be slow, and virtualised queries depend on the performance of the source systems.
  - Some security features, such as fine-grained named-graph security in Stardog, are not enabled by default and must be configured deliberately.
- **Cost and licence.**
  - Both are commercial products, and GraphDB has a free edition with limits on concurrency.
- **Capital markets example.**
  - An RDF platform fits a regulatory reporting programme that must classify every legal entity and instrument against FIBO and explain each classification to an auditor.
  - It does not fit a small team building a research assistant over earnings call transcripts, because the ontology work would take longer than the assistant itself.

### 4.6 TigerGraph

- **How it works.**
  - TigerGraph is a distributed, massively parallel graph database with its own GSQL query language, and it added hybrid graph and vector search in 2025.
- **Strengths.**
  - It is designed for deep traversals across billions of edges, which suits analytics such as fraud ring detection.
- **Weaknesses.**
  - GSQL is proprietary, the ecosystem for agent frameworks is smaller, and there was little public product news in 2026.
- **Cost and licence.**
  - It is commercial, with a free Community Edition.
- **Capital markets example.**
  - TigerGraph fits an anti-money-laundering programme that runs ten-hop traversals across the full payments graph.
  - It does not fit an agent context layer where most queries are one or two hops, because a simpler and better-supported database would do the same job.

### 4.7 Embedded graph databases: Kuzu and LadybugDB

- **How it works.**
  - Kuzu was an embedded, columnar graph database that ran inside the application process, similar to how SQLite or DuckDB work.
  - Apple agreed to acquire Kuzu in October 2025, and the repository was archived. The MIT-licensed code continues as a community fork called LadybugDB.
- **Strengths.**
  - Embedded graphs suit agents that need a private, local graph per task or per user, with no server to operate.
- **Weaknesses.**
  - The original project has no sponsor, and the fork is maintained by a small community, so it is a dependency risk for enterprise use.
- **Cost and licence.**
  - It is free under the MIT licence.
- **Capital markets example.**
  - An embedded graph fits a desktop research tool that builds a temporary graph of companies mentioned in one analyst's documents.
  - It does not fit a shared, governed firm-wide context layer.

## 5. Vector and search databases

- These databases are the document and passage index of a context layer.
  - They do not store business definitions, resolve entities or validate facts, so they are always one component rather than the whole layer.
  - Hybrid retrieval, which combines dense vectors with keyword matching, is now the production norm, as [agentic-ai.md](agentic-ai.md) section 3.2 describes, so keyword support is a selection criterion.

### 5.1 Pinecone and Pinecone Nexus

- **How it works.**
  - Pinecone is a fully managed, serverless vector database that separates storage from compute and supports dense and sparse vectors, metadata filtering and namespaces.
  - [Pinecone Nexus](https://www.pinecone.io/newsroom/general-availability-of-pinecone-nexus-proves-knowledge-drives-real-outcomes-for-agentic-ai/md/), generally available since August 2026, compiles source data into structured, task-specific artefacts before an agent asks for them, rather than retrieving chunks at query time, and it can be deployed in the customer's own AWS, Google Cloud or Azure account.
- **Strengths.**
  - It requires no infrastructure work and has predictable low latency, which makes it the default for teams that want a managed service.
  - Nexus moves Pinecone towards a context product, and Pinecone reports up to 90% lower token use for agent tasks.
- **Weaknesses.**
  - There is no self-hosted version of the core database, which matters for firms that must keep data on premises.
  - Storage cost per gigabyte is higher than object-storage designs, and cost can grow quickly with many namespaces.
  - In 2026 Pinecone replaced its founding CEO and was reported to be exploring a sale. This is unconfirmed, but it is a vendor-continuity consideration for a long-term dependency.
- **Cost and licence.**
  - It is commercial and usage-based, with entry plans in the tens of dollars per month and enterprise contracts above that.
- **Capital markets example.**
  - Pinecone fits a sell-side research portal that needs semantic search over published research with minimal operational staff.
  - It does not fit a firm whose data policy forbids client communications from leaving its own data centre.

### 5.2 Qdrant

- **How it works.**
  - Qdrant is an open-source vector database written in Rust, with HNSW indexing, rich payload filtering, quantisation and native sparse vectors for hybrid search.
- **Strengths.**
  - Filtering is applied during the vector search rather than afterwards, which keeps results correct when queries are restricted by desk, region or entitlement.
  - It can be self-hosted, run in Qdrant Cloud, or deployed as a hybrid cloud inside the customer's Kubernetes cluster.
  - It raised a $50 million Series B in March 2026, which supports its long-term viability.
- **Weaknesses.**
  - Running it yourself at scale requires operational skill with sharding, replication and snapshots.
  - It offers search only, so graph traversal and business definitions must come from elsewhere.
- **Cost and licence.**
  - It is Apache 2.0 licensed, with paid managed and enterprise offerings.
- **Capital markets example.**
  - Qdrant fits a compliance search tool where every query must be filtered by the user's information barrier, because filtered search is a first-class feature.
  - It does not fit a question such as "which of our clients hold bonds of issuers in this supply chain", which requires graph traversal.

### 5.3 Weaviate

- **How it works.**
  - Weaviate is an open-source vector database with built-in BM25 keyword search, hybrid fusion, multi-tenancy and modules that call embedding models automatically.
- **Strengths.**
  - Hybrid search is built in and well documented, which suits text that mixes concepts with exact identifiers such as ISINs and CUSIPs.
  - Native multi-tenancy isolates each tenant's data, which helps when each client or desk must have a separate index.
- **Weaknesses.**
  - Memory use can be high at large scale unless compression is configured.
  - Its company funding is smaller than some competitors, with a strategic investment from Ricoh in 2026.
- **Cost and licence.**
  - It is BSD-3 licensed, with a managed cloud priced by usage.
- **Capital markets example.**
  - Weaviate fits a search tool over ISDA agreements and credit support annexes, where users search both by concept and by exact counterparty names and clause numbers.
  - It does not fit a need for a governed definition of exposure, because it stores text, not definitions.

### 5.4 Milvus and Zilliz

- **How it works.**
  - Milvus is an open-source, distributed vector database with separate query, data and index nodes, supporting GPU indexes and many index types, and Zilliz Cloud is the managed version.
- **Strengths.**
  - It is designed for billions of vectors and high ingest rates, and it is the usual choice at that scale.
- **Weaknesses.**
  - The distributed deployment has many components and dependencies, which makes it the most complex of these databases to run.
- **Cost and licence.**
  - It is Apache 2.0 licensed, and Zilliz Cloud is commercial.
- **Capital markets example.**
  - Milvus fits a firm that embeds every email, chat and voice transcript for communications surveillance across the whole front office.
  - It does not fit a team with under a few million documents, where its operational cost is not justified.

### 5.5 turbopuffer

- **How it works.**
  - turbopuffer is a serverless vector and full-text search engine that keeps all data in object storage such as S3 and caches active namespaces on NVMe and in memory.
- **Strengths.**
  - Storage cost is close to object-storage cost, around $0.02 per gigabyte, which is far lower than memory-resident designs.
  - It suits workloads with very many namespaces of which only a few are active at once. Cursor and Notion are its best-known customers, and Notion reports more than 10 billion vectors on it.
- **Weaknesses.**
  - The first query against a cold namespace is slower, in the hundreds of milliseconds, so it does not guarantee low latency for every query.
  - It is a younger company and a managed-only service.
- **Cost and licence.**
  - It is commercial and usage-based, with a low entry price.
- **Capital markets example.**
  - turbopuffer fits a wealth platform that keeps a separate index per client relationship, where only a fraction of clients are discussed on any given day.
  - It does not fit a trading assistant that must answer within a fixed latency budget on every request.

### 5.6 Elasticsearch and OpenSearch

- **How it works.**
  - Both are distributed search engines built on Lucene that combine BM25 keyword search, dense vectors with HNSW and quantisation, and sparse learned retrieval.
  - OpenSearch 3.5 and 3.6 added agent conversation memory with semantic and hybrid search over it.
- **Strengths.**
  - Many firms already run them for logs and search, so the operational skills, security integration and access control by document and field already exist.
  - Their keyword search, aggregations and filtering are more mature than those of any dedicated vector database.
- **Weaknesses.**
  - Vector search at very large scale needs more memory and tuning than in purpose-built engines.
  - Elasticsearch's licence changes since 2021 have made some organisations cautious, which is why OpenSearch exists.
- **Cost and licence.**
  - Elasticsearch is available under AGPL, SSPL or the Elastic License, with paid features and Elastic Cloud. OpenSearch is Apache 2.0 and is offered as a managed service by AWS.
- **Capital markets example.**
  - Elasticsearch fits a firm that already indexes trade surveillance alerts and wants agents to search them with hybrid queries under the existing document-level security.
  - It does not fit relationship questions across entities, for the same reason as other search engines.

## 6. General-purpose databases with vector and graph support

### 6.1 PostgreSQL with pgvector, pgvectorscale and Apache AGE

- **How it works.**
  - pgvector adds a vector type and HNSW and IVFFlat indexes to Postgres. pgvectorscale, from Tiger Data, adds a disk-based StreamingDiskANN index and quantisation for larger datasets.
  - Apache AGE adds openCypher graph queries over Postgres tables, and Postgres full-text search or extensions such as ParadeDB provide BM25 ranking.
  - A design presented at Postgres Summit US 2026 stores each agent fact three ways, as text, as an embedding and as graph triples in AGE, and retrieves with one hybrid query across all three.
  - Databricks Lakebase, built on the Neon acquisition, and Snowflake Postgres, built on the Crunchy Data acquisition, place managed Postgres inside the two largest data platforms specifically for agent workloads.
- **Strengths.**
  - One database holds relational reference data, vectors, keyword indexes and simple graphs, with transactions across all of them, which removes synchronisation between separate stores.
  - Row-level security applies to vector queries, so entitlements are enforced by the same mechanism as for the rest of the firm's data.
  - Most firms already have Postgres skills, backup, monitoring and approval in place, which shortens the path to production.
- **Weaknesses.**
  - pgvector's HNSW index must fit in memory for good latency, and sources generally put the practical ceiling at around 100 million vectors.
  - Apache AGE is less mature and slower for deep traversals than a native graph database, and its community is small.
  - Filtered vector search can return too few results unless iterative index scans are configured.
- **Cost and licence.**
  - Postgres and pgvector use the PostgreSQL licence, AGE is Apache 2.0, and pgvectorscale is under the PostgreSQL licence. Managed services are offered by every major cloud.
- **Capital markets example.**
  - Postgres fits a client mandate assistant, where mandates, restrictions and accounts already live in relational tables and the agent needs semantic search over the mandate documents joined to those tables.
  - It does not fit a firm-wide ownership graph with tens of millions of entities and deep traversals, which a native graph database handles better.

### 6.2 MongoDB Atlas

- **How it works.**
  - Atlas Vector Search indexes embeddings inside document collections, and MongoDB added Voyage AI embedding models and automated embedding in January 2026.
  - Hybrid fusion is available through `$rankFusion` and `$scoreFusion`, which were in preview at the time of writing.
- **Strengths.**
  - Documents with nested structure, such as a client profile with accounts and contacts, are stored and retrieved as one unit together with their embeddings.
  - Firms that already run MongoDB avoid adding a new database.
- **Weaknesses.**
  - Graph traversal is limited to `$graphLookup`, which is not suitable for complex multi-hop queries.
  - Some hybrid search features are still in preview.
- **Cost and licence.**
  - The server is under SSPL, and Atlas is commercial and usage-based.
- **Capital markets example.**
  - MongoDB fits a client onboarding assistant where each KYC file is a document with attachments and the agent searches across them.
  - It does not fit questions that span many hops between legal entities. See [mongodb.md](mongodb.md).

### 6.3 Oracle AI Database 26ai and SingleStore

- **How it works.**
  - Oracle AI Database 26ai includes vector search, property graphs with SQL/PGQ, JSON and relational data in one engine.
  - SingleStore combines row and column storage with vector search and full-text search for real-time analytics, as described in [datastore-SingleStore.md](datastore-SingleStore.md).
- **Strengths.**
  - Both let firms that have standardised on them add vector and graph capability without introducing a new vendor, which matters in banks where onboarding a new database can take months.
- **Weaknesses.**
  - Neither has the agent-framework ecosystem of Postgres or Neo4j, and licensing costs are high.
- **Cost and licence.**
  - Both are commercial.
- **Capital markets example.**
  - Oracle fits a bank whose core trade booking and reference data already run on Oracle and whose architecture board will not approve another database.

## 7. Agent memory layers

- Memory layers are not databases. They are services or libraries that extract facts from conversations, decide what to store and retrieve it, and they sit on top of a vector or graph database.
  - The key distinction between them is whether they track when a fact was true, which [agentic-ai.md](agentic-ai.md) section 3.6 explains in detail.

### 7.1 Mem0

- **How it works.**
  - Mem0 extracts facts from interactions using an LLM, stores them in a vector store with an optional graph store, and updates or deletes facts that conflict with new ones.
  - OpenMemory MCP is a local-first memory server that shares memory across MCP clients.
- **Strengths.**
  - It is the simplest to adopt, works with many vector and graph backends, and has the largest community, with over 58,000 GitHub stars by mid-2026.
- **Weaknesses.**
  - It is vector-first, so time-dependent facts are handled by overwriting rather than by validity periods. It scored 49.0% against Zep's 63.8% on LongMemEval in Zep's comparison, and Mem0, Zep and Letta have publicly disputed each other's benchmark claims.
- **Cost and licence.**
  - The core library is Apache 2.0. The managed platform has a free tier and paid plans from about $19 per month, with enterprise pricing above that. Mem0 raised about $24 million in 2025.
- **Capital markets example.**
  - Mem0 fits an internal assistant that remembers an analyst's preferred coverage universe and report format.
  - It does not fit memory of client restrictions, where using a superseded restriction causes a breach.

### 7.2 Zep and Graphiti

- **How it works.**
  - Graphiti is an open-source engine that builds a temporal knowledge graph from conversations and documents, where each edge has a validity period, and it runs on Neo4j, FalkorDB and other backends.
  - Zep is the managed service built on Graphiti.
- **Strengths.**
  - It is the strongest option for facts that change over time, and it keeps superseded facts so that past states can still be queried.
- **Weaknesses.**
  - Zep is cloud-only, so self-hosting means running Graphiti and its graph database yourself, which requires more integration work.
  - Every ingested message requires LLM calls for extraction, which adds cost and latency at write time.
- **Cost and licence.**
  - Graphiti is Apache 2.0. Zep is commercial.
- **Capital markets example.**
  - Zep fits a coverage assistant that must know a client's current authorised traders and settlement instructions while still explaining why a trade last year was settled differently.

### 7.3 Letta

- **How it works.**
  - Letta, formerly MemGPT, is an agent runtime in which the agent manages its own tiered memory, moving information between an in-context core memory and external archival memory.
- **Strengths.**
  - It suits long-running agents that work on one task for days and need to manage their own context.
- **Weaknesses.**
  - It is a full agent stack rather than a memory component, so adopting it means building agents in Letta, and leaving it later means rebuilding them.
- **Cost and licence.**
  - It is Apache 2.0, with a commercial cloud.
- **Capital markets example.**
  - Letta fits a long-running agent that monitors a portfolio's corporate actions over a quarter.
  - It does not fit a firm that has already standardised on another agent framework.

### 7.4 Cognee

- **How it works.**
  - Cognee is an open-source pipeline that builds a combined knowledge graph and vector index from many data sources, intended as shared memory for many agents.
- **Strengths.**
  - It is self-hostable and targets shared organisational knowledge rather than per-user memory.
- **Weaknesses.**
  - It is a young project, and most published comparisons of it are its own.
- **Cost and licence.**
  - It is Apache 2.0, with commercial support.
- **Capital markets example.**
  - Cognee fits a pilot that builds a shared graph over a team's research notes and filings to test whether graph memory helps before committing to a commercial platform.

## 8. Semantic layers, catalogs and packaged context platforms

### 8.1 Semantic layers and the Apache Ossie standard

- **How it works.**
  - A semantic layer defines metrics, dimensions and relationships once, so every agent and dashboard calculates "net exposure" or "realised P&L" the same way.
  - The main products are dbt's MetricFlow, Cube, AtScale, Snowflake semantic views, Databricks Unity Catalog metric views and Power BI semantic models.
  - The [Open Semantic Interchange](https://ossie.apache.org/updates/) specification, version 1.0 released in January 2026 and now Apache Ossie in the Apache Incubator, is a format for exchanging these definitions between platforms. dbt open-sourced MetricFlow under Apache 2.0 as a reference implementation.
- **Strengths.**
  - Agents that generate SQL against a semantic layer produce consistent answers, which is the main remedy for agents that compute the same metric differently on different days.
- **Weaknesses.**
  - The definitions themselves require agreement between business owners, which is an organisational task rather than a technical one.
  - Ossie is an interchange format and not a query engine, and adoption across platforms is still in progress.
- **Cost and licence.**
  - MetricFlow and Ossie are Apache 2.0. Warehouse-native layers are included in the platform cost. Cube and AtScale are commercial with open-source components.
- **Capital markets example.**
  - A semantic layer fits a risk reporting agent that must calculate exposure by counterparty exactly as the risk system does.
  - It does not help an agent that answers questions from research notes and emails.

### 8.2 Warehouse-native context: Snowflake, Databricks and Microsoft Fabric IQ

- **How it works.**
  - Snowflake combines Horizon governance, semantic views and Cortex agents. Databricks combines Unity Catalog, metric views and Lakebase.
  - [Microsoft Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/overview) adds an ontology that binds entity types and rules to live Fabric data, with Work IQ supplying context from email, files and meetings. The ontology was still in preview in October 2026.
- **Strengths.**
  - Governance, lineage and permissions are already in place, so agents inherit them without extra work.
- **Weaknesses.**
  - Each covers only its own platform. Firms with data spread across several platforms get a partial context layer from each.
- **Cost and licence.**
  - They are included in, or charged as consumption on, the platform.
- **Capital markets example.**
  - Snowflake fits a buy-side firm whose positions, holdings and benchmark data all sit in Snowflake.
  - It does not fit a bank where trade data sits in on-premises Oracle and Sybase IQ, research in SharePoint and reference data in a vendor system.

### 8.3 Data catalogs as context layers: Atlan, DataHub, Collibra and Alation

- **How it works.**
  - Catalogs hold metadata, lineage, ownership, glossary terms and sensitivity classifications across many platforms, and they now expose this to agents through MCP.
- **Strengths.**
  - They are the only category that covers metadata and policy across many platforms, and they reuse governance work the firm has often already done for BCBS 239 data lineage.
- **Weaknesses.**
  - They describe data rather than containing it, so they must be combined with search and graph stores.
  - Their claimed accuracy improvements for agents are self-reported.
- **Cost and licence.**
  - Atlan, Collibra and Alation are commercial. DataHub is Apache 2.0 with a commercial cloud.
- **Capital markets example.**
  - A catalog fits an agent that must tell a user which dataset is the golden source for counterparty ratings, who owns it and whether the user may use it for client reporting.

### 8.4 Packaged context platforms: Glean, Neo4j Context Engine, Pinecone Nexus and Palantir

- **How it works.**
  - Glean indexes enterprise applications into an Enterprise Graph of people, content and workflows, combined with a personal graph per employee, and exposes it to its own agents and through MCP.
  - Neo4j Context Engine, Pinecone Nexus and AWS Context are described in sections 4.1, 5.1 and 4.2.
  - Palantir's Ontology models business objects, links and permitted actions over the firm's data, and it is described in [agentic-ai.md](agentic-ai.md) section 3.7.
- **Strengths.**
  - They give the fastest route to a working context layer, because connectors, permissions and ranking are included.
- **Weaknesses.**
  - The organisation's model of its business is held in a vendor's format, which makes switching costly.
  - Several of these products were released or reached general availability only in 2026.
- **Cost and licence.**
  - All are commercial, typically priced per user or per platform contract.
- **Capital markets example.**
  - Glean fits an investment bank that wants agents to answer "who in the firm has covered this issuer and what did they write" across email, Slack, Confluence and the CRM.
  - It does not fit a need for governed calculation of regulatory capital, which requires authoritative structured data.

## 9. Side-by-side comparison

### 9.1 Databases

| Product | Store it covers | Deployment | Licence | Scale sweet spot | Main strength | Main limitation |
|---|---|---|---|---|---|---|
| Neo4j | Graph, vector | Self-hosted, Aura | GPLv3 / commercial | Up to billions of edges | Ecosystem, Cypher, MCP | Ingestion and freshness are custom work |
| Amazon Neptune | Graph (property and RDF), vector | AWS only | Commercial | Large, managed | AWS governance integration | AWS lock-in, smaller tooling |
| FalkorDB / Memgraph | Graph | Self-hosted, cloud | SSPL / BSL | In-memory graphs | Low-latency traversal, streaming | RAM cost, smaller vendors |
| Spanner Graph | Graph over relational | Google Cloud only | Commercial | Global scale | No separate copy of data | Cost for small workloads |
| Stardog / GraphDB | RDF graph, reasoning | Self-hosted, cloud | Commercial | Ontology-heavy | FIBO, reasoning, virtualisation | Specialist skills |
| Pinecone | Vector, sparse | Managed, BYOC for Nexus | Commercial | Any size | No operations | No self-hosting, vendor uncertainty |
| Qdrant | Vector, sparse | Self-hosted, cloud | Apache 2.0 | Up to billions | Filtered search | Operations at scale |
| Weaviate | Vector, BM25 | Self-hosted, cloud | BSD-3 | Medium to large | Built-in hybrid, multi-tenancy | Memory use |
| Milvus | Vector | Self-hosted, Zilliz | Apache 2.0 | Billions | Scale | Operational complexity |
| turbopuffer | Vector, full text | Managed | Commercial | Many idle tenants | Storage cost | Cold-query latency |
| Elasticsearch / OpenSearch | Keyword, vector | Self-hosted, cloud | AGPL/SSPL/ELv2 / Apache 2.0 | Large | Mature search and security | Vector memory cost |
| PostgreSQL + pgvector + AGE | Relational, vector, keyword, graph | Anywhere | PostgreSQL / Apache 2.0 | Under ~100M vectors | One transactional store | Graph and vector ceilings |
| MongoDB Atlas | Document, vector | Cloud, self-hosted | SSPL / commercial | Medium to large | Document model | Weak graph |

### 9.2 Memory and context layers

| Product | Category | Tracks time | Self-hostable | Licence | Best for | Main limitation |
|---|---|---|---|---|---|---|
| Mem0 | Memory library | No, overwrites | Yes | Apache 2.0 | Personalisation | Superseded facts are lost |
| Zep / Graphiti | Temporal graph memory | Yes | Graphiti only | Apache 2.0 / commercial | Changing facts | Write-time LLM cost |
| Letta | Agent runtime with memory | Partly | Yes | Apache 2.0 | Long-running agents | Framework lock-in |
| Cognee | Graph and vector memory | Partly | Yes | Apache 2.0 | Shared team knowledge | Maturity |
| dbt MetricFlow / Ossie | Semantic layer | Not applicable | Yes | Apache 2.0 | Consistent metrics | Needs business agreement |
| Snowflake / Databricks / Fabric IQ | Platform semantic layer | Not applicable | No | Platform | Single-platform estates | One platform only |
| Atlan / DataHub / Collibra | Catalog | Lineage history | DataHub only | Commercial / Apache 2.0 | Cross-platform metadata | Holds no content |
| Glean | Packaged enterprise graph | Partly | No | Commercial | Workplace knowledge | Vendor model |
| Neo4j Context Engine | Packaged ontology and memory | Yes | Not yet stated | Commercial | Graph-centred firms | Private preview |
| Pinecone Nexus | Compiled context | Not stated | BYOC | Commercial | Token reduction | New, vendor-reported results |

## 10. Worked capital markets scenarios

### 10.1 Settlement break investigation

- An operations agent is asked why a trade failed to settle and what to do about it.
  - The agent needs the trade and settlement instruction data, which is relational, the counterparty's standard settlement instructions over time, which change, and the operations team's past notes on similar breaks, which are text.
  - A good fit is Postgres holding trade and instruction tables with pgvector over break notes, plus Zep or Graphiti to track the history of each counterparty's settlement instructions.
  - A poor fit is a vector database alone, because it would retrieve similar past notes but could not tell whether the instructions it found are the current ones.

### 10.2 Counterparty exposure across a legal entity hierarchy

- A credit agent is asked for total exposure to a group, including all subsidiaries and guarantors.
  - The agent needs a legal entity hierarchy with ownership percentages, sourced from LEI data and internal reference data, and a governed definition of exposure.
  - A good fit is Neo4j or Neptune for the hierarchy, joined to a semantic layer that defines exposure exactly as the risk engine calculates it.
  - A poor fit is GraphRAG over documents, because extracted ownership relations would contain errors that propagate into a limit check.

### 10.3 Research over filings and earnings call transcripts

- An analyst's assistant is asked which companies mentioned supply constraints in a specific component in the last two quarters, and who supplies them.
  - The agent needs hybrid search over transcripts and filings, plus a supply-chain graph to answer the second part.
  - A good fit is Weaviate or Elasticsearch for hybrid search, with a modest Neo4j graph of companies and suppliers built from structured vendor data.
  - A poor fit is a semantic layer, because the information is in text rather than in governed metrics.

### 10.4 Client mandate and restriction checks

- A portfolio agent proposes trades and must check them against each client's mandate before staging orders.
  - The agent needs current, authoritative restrictions with an audit trail of who approved each one and when.
  - A good fit is the restrictions held in the firm's compliance system or a relational store, exposed through a semantic or ontology layer with permissions, with a temporal memory only for conversational context.
  - A poor fit is any memory layer used as the source of truth for restrictions, because extracted facts can be wrong and memory is not an approved compliance record.

### 10.5 Communications surveillance

- A surveillance agent triages alerts across email, chat and voice transcripts.
  - The agent needs search over very large volumes of text, filtered by information barriers, plus the relationship graph between traders and accounts.
  - A good fit is Milvus or Elasticsearch for the text at scale and Memgraph or Neo4j for the relationship graph, with entitlements enforced in both.
  - A poor fit is turbopuffer for the primary alert queue, because the workload queries most of the data continuously rather than a few active namespaces.

## 11. Reference combinations

- **Starting small on existing infrastructure.**
  - Use Postgres with pgvector and full-text search for documents and reference data, Mem0 or Graphiti for memory, and add Apache AGE only if simple graph queries are needed.
  - The limitation is that this combination outgrows itself when the entity graph becomes large or deep, at which point the graph moves to a native graph database.
- **Graph-centred context layer.**
  - Use Neo4j for entities, relationships and vectors, Graphiti on Neo4j for temporal memory, and a catalog such as DataHub for lineage and ownership.
  - The limitation is that the ingestion pipelines from each source system have to be built and maintained, and their freshness monitored.
- **Single data platform.**
  - Use the platform's own semantic layer, catalog, vector search and Postgres service, such as Snowflake Horizon with Cortex and Snowflake Postgres, or Databricks Unity Catalog with Lakebase.
  - The limitation is that data outside the platform is not covered and must be brought in or left out.
- **Buy a packaged layer.**
  - Use Glean for workplace knowledge, or Neo4j Context Engine or AWS Context for structured enterprise data.
  - The limitation is dependence on a vendor's ontology and on products that are less than a year old.

## 12. Selection risks and checklist

- **Verify vendor benchmarks.**
  - Run a proof of concept on the firm's own documents and questions, with an evaluation set that includes multi-hop and time-dependent questions, before relying on any published number.
- **Check that entitlements carry through.**
  - Confirm that the context layer enforces the same information barriers and data entitlements as the source systems, at query time, for every store including vector indexes and memory.
- **Plan for freshness.**
  - Every derived store, whether a graph, an index or a memory, needs a refresh mechanism and a visible "last updated" timestamp, because a stale answer looks the same as a current one. [sdlc-context-graph.md](sdlc-context-graph.md) section 7 covers this in detail.
- **Check the licence.**
  - SSPL, BSL and AGPL licences restrict how a database can be offered as a service, which matters if the context layer will be exposed to clients.
- **Assess vendor continuity.**
  - The Kuzu acquisition and the reported Pinecone sale process show that the category is consolidating, so prefer products with open formats, Cypher or SQL interfaces, or an open-source core that can be run independently.
- **Keep authoritative records out of memory.**
  - Restrictions, approvals and regulatory records belong in systems of record, and memory layers should reference them rather than copy them.

## Resources

- [Neo4j Context Engine launch](https://neo4j.com/press-releases/neo4j-context-engine/) — press release, 20 October 2026, with coverage at [StorageReview](https://www.storagereview.com/news/neo4j-context-engine-ai-agents-knowledge-layer-ontology-graph-native-memory).
- [This Week in Neo4j: agent memory and the hosted MCP server](https://neo4j.com/blog/twin4j/this-week-in-neo4j-nodes-agentmemory-graphrag-knowledgelayer-and-more/) — Neo4j weekly update, 2026.
- [AWS Context: knowledge graph for agents](https://thenewstack.io/aws-context-knowledge-graph-agents/) — The New Stack, June 2026.
- [Graphiti adds FalkorDB support](https://blog.getzep.com/graphiti-knowledge-graphs-falkordb-support/) — Zep blog, with FalkorDB's [agentic memory documentation](https://docs.falkordb.com/agentic-memory.md).
- [KuzuDB abandoned](https://www.theregister.com/2025/10/14/kuzudb_abandoned/) — The Register, and [Apple acquires Kuzu](https://betakit.com/apple-strikes-deal-to-acquire-canadian-database-software-startup-kuzu/) — BetaKit.
- [Spanner Graph](https://cloud.google.com/products/spanner/graph) and [GraphRAG infrastructure on Spanner Graph](https://docs.cloud.google.com/architecture/gen-ai-graphrag-spanner) — Google Cloud.
- [General availability of Pinecone Nexus](https://www.pinecone.io/newsroom/general-availability-of-pinecone-nexus-proves-knowledge-drives-real-outcomes-for-agentic-ai/md/) — Pinecone, August 2026, and [InfoQ coverage](https://infoq.com/news/2026/07/pinecon-nexus-knowledge-engine).
- [Vector database landscape](https://druce.ai/governance/wiki/comparisons/vector-database-landscape) — includes the Pinecone sale reports and 2026 funding.
- [How turbopuffer is refactoring the economics of search](https://aws.amazon.com/aws-startups/learn/how-turbopuffer-is-refactoring-the-economics-of-search/) — AWS case study, and [turbopuffer's object-storage-first architecture](https://jxnl.co/writing/2025/09/11/turbopuffer-object-storage-first-vector-database-architecture/).
- [Best Vector Databases in 2026](https://www.firecrawl.dev/blog/best-vector-databases) — a comparison that is less vendor-aligned than most.
- [Agent memory is three Postgres extensions in a trench coat](https://postgresql.us/events/postgressummitus2026/sessions/session/2465-agent-memory-is-three-postgres-extensions-in-a-trench-coat/) — Postgres Summit US 2026.
- [Snowflake buys Crunchy Data, Databricks buys Neon](https://saastr.com/snowflake-buys-crunchy-data-for-250m-databricks-buys-neon-for-1b-the-new-ai-database-battle) — the Postgres acquisitions for agent workloads.
- [Best AI agent memory tools in 2026](https://www.braintrust.dev/articles/best-ai-agent-memory-tools-2026) — Braintrust, and [Best AI Agent Memory Systems in 2026](https://vectorize.io/articles/best-ai-agent-memory-systems) — Vectorize.
- [Mem0 raises $24 million](https://pulse2.com/mem0-24-million-raised-for-powering-memory-layer-for-ai-agents/) — funding and licence background.
- [Apache Ossie (incubating)](https://ossie.apache.org/updates/) — the Open Semantic Interchange specification.
- [What is Fabric IQ?](https://learn.microsoft.com/en-us/fabric/iq/overview) — Microsoft Learn, and [Making sense of Work IQ, Fabric IQ and Foundry IQ](https://www.jamesserra.com/archive/2026/02/making-sense-of-microsofts-ai-strategy-work-iq-fabric-iq-foundry-iq/) — James Serra.
- [Glean's third-generation assistant and Enterprise Graph](https://www.glean.com/press/glean-introduces-third-generation-ai-assistant-new-enterprise-graph-to-enable-the-superintelligent-enterprise) — Glean press release, September 2025.
- [Agent Context Layer Tools Compared](https://atlan.com/know/ai-agent/agent-context-layer-tools-compared/) — Atlan, and [Best Context Management Platforms](https://datahub.com/blog/best-context-management-platform/) — DataHub. Both are vendor-authored and rank their own products highly.
- [FIBO, the Financial Industry Business Ontology](https://spec.edmcouncil.org/fibo/) — EDM Council, the standard vocabulary used by RDF platforms in financial services.
