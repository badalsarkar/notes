# Sybase IQ

**Google**: 618c1927f9a26471
**Chat**: d456d4e9-1c58-4f86-a171-b4d65079eac9

**Version**: 16

## Summary

- Storage
  - Columnar DB
  - Supports in-memory operations through caching technique but the storage is primarily in disk
- Designed for high performance analytical workload
- Use advanced compression algo for columnar DB
- Applies bitwise indexing (?)
- Supports horizontal partitioning
- Applies MPP architecture which distributes the query processing to multiple nodes
- Usecases
  - Data warehousing and business intelligence
  - Analytical application that requires complex calculations and aggregation on large datasets
  - Data mart
  - Log analysis
- It is not optimized for transactional workload that requires updates and inserts. It is optimized for read heavy workload

## Data Ingestion

- Bulk loading
- Data pump
- ETL tool integration
- Replication
- Change Data Capture (CDC)
- Direct data integration
- Custom data ingestion
