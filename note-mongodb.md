

## Find api

[API DOC](https://docs.mongodb.com/manual/reference/method/db.collection.find/)

- selects document in collection and returns a **cursor**. It is important to note that the method returns a cursor to
document.

[MongoDB Query Operators](https://docs.mongodb.com/manual/reference/operator/query/#query-selectors)

- For unique index, if the indexed field is missing, mongodb will store a null value. As this is unique index, there can
be only one document with the unique index field missing. 

tag:question- how does having many unique index affect database performance?

