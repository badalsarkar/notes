# MongoDB

## Data Modeling

https://docs.mongodb.com/manual/core/data-modeling-introduction/

- When designing data models, always consider the application usage of the data (i.e. queries, updates, and processing of the data) as well as the inherent structure of the data itself.
- The key decision in designing data models for MongoDB applications revolves around the structure of documents and how the application represents relationships between data. MongoDB allows related data to be embedded within a single document.
- **Very Important**: In MongoDB, a write operation is atomic on the level of a single document, even if the operation modifies multiple embedded documents within a single document. A denormalized data model with embedded data combines all related data in a single document instead of normalizing across multiple documents and collections. This data model facilitates atomic operations. [Here](https://docs.mongodb.com/manual/core/data-modeling-introduction/#single-document-atomicity)
- When a single write operation (e.g. db.collection.updateMany()) modifies multiple documents, the modification of each document is atomic, but the operation as a whole is not atomic.
- Effective data models support your application needs. The key consideration for the structure of your documents is the decision to embed or to use references.



## Find api

[API DOC](https://docs.mongodb.com/manual/reference/method/db.collection.find/)

- selects document in collection and returns a **cursor**. It is important to note that the method returns a cursor to
document.

[MongoDB Query Operators](https://docs.mongodb.com/manual/reference/operator/query/#query-selectors)

- For unique index, if the indexed field is missing, mongodb will store a null value. As this is unique index, there can
be only one document with the unique index field missing. 

tag:question- how does having many unique index affect database performance?

