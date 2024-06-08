# Foundation of Scalable Systems

## Salable distributed database

- [dbi Blog](https://www.dbi-services.com/blog/the-myth-of-nosql-vs-rdbms-joins-dont-scale/)

- Cheap hardware makes is easy to scale database horizontally
- Relational database scaling strategy
  - scaling up:
    - Relational DBs are designed to run on a single machine
    - DB engines can utilize multiple CPU, memories to process thousands of queries in parallel
    - Scaling has no impact on application code
    - downsides
      - cost- hardware cost tend to grow exponentially
      - availability - a single node DB, failure mean the DB is down
      - growth - if the data continues to grow, migration to another powerful DB is painful
      - when low latency DB access is required for an international client base, traversing international network to access data doesn't work
    - therefore distributing DB is necessary
  - scaling out
    - Read replicas
      - Multiple node will contain the data
      - The main DB node is known as primary, and read replicas are known as secondary
      - Replicas contain copy of main database
      - Writes are only possible in main DB
      - Replicas update asynchronously
      - Replicas can be located in different data centers to serve global clients
      - DB read requests are served by replicas
      - Good for high read environments
      - Writes are efficient as the main DB only handle writes
      - If the main DB fails the reads are not impacted
      - Problems
        - There is delay in updating the read replicas. So, the users may read stale data
    - Partitioning data
      - splitting data into multiple disk partitions and storage engines
      - Partitioning strategies
        - horizontal partitions
          - Splits table into multiple physical partitions
          - Rows are allocated to partitions based on some partitioning strategy
          - Common partitioning strategies are to allocate rows based on some value in a row or to use a hash function on the primary key
        - vertical partitions
          - AKA row splitting
          - Partitions a table by the columns in a row
          - A common strategy is to partition a row between static, read-only data and dynamic data
  - Relational DBs will have various partitioning supports. Some support partitioning is disk and others support partitioning across nodes
  - Partitions will split the table into multiple nodes. However, if a query needs to access multiple nodes the performance benefit may vanish
- Distributed joins
  - Relational DB joins are complicated when the data is distributed across large clusters of machines
  - Joins needs to be carefully designed
    - strategies for joins
      - TODO: