# Learning PostgreSQL

## Set up

### Logging in

After installing the database software do the following-

1. To login `sudo -i -u postgres`. This will use the user `postgres` to open the
   database cli. Once there, type `psql` to connect to the default table for
   the user.
2. To create a separate user, `sudo -u postgres createuser --interactive`. Then
   give username. This must be same as the linux username. Then you must also
   create a database with the same name as the username. The command is `sudo -u
   postgres createdb ${databasename}`.
3. Once the user is created you can type `sudo -i -u ${username}`. Then type
   `psql`. This will connect to the default database.
4. To login directly, `sudo -u ${username} psql`.
5. To loging to a different database `sudo -u ${username} psql -d
   ${databasename}`

https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e

### Some commands

Once inside the postgres terminal-

**`\list`**

Lists all databases.

**`\c ${databasename}`**

Switch to database.

**`\dt`**

Lists all tables in the database.

## Architecture

[https://www.postgresql.org/docs/14/tutorial-arch.html](https://www.postgresql.org/docs/14/tutorial-arch.html)

- It has client/server architecture
- If the client and server is not in the same host, the communication happens
over TCP/IP 
- The PostgreSQL server can handle multiple concurrent connections from clients.
To achieve this it starts (“forks”) a new process for each connection. From that
point on, the client and the new server process communicate without intervention
by the original postgres process. Thus, the supervisor server process is always
running, waiting for client connections, whereas client and associated server
processes come and go.

## Fundamentals

### Operator precedence

### Data Types

#### JSON

- _jsonb_ is faster to process and also supports indexing

## Recursive Queries

```plantuml
@startmindmap
* test
** another
endmindmap
```

## Performance

### EXPLAIN

PostgreSQL devises a query plan for each query it receives. Choosing the right plan to match the query structure and the properties of the data is absolutely critical for good performance, so the system includes a complex planner that tries to choose good plans. You can use the EXPLAIN command to see what query plan the planner creates for any query. 

The plan is a tree structure consisting of plan nodes. The bottom most nodes are called `scan node`. These nodes return the raw rows from a table. To return rows from a table the table needs to be accessed. Depending on the access method the scan node type will vary. The access methods are below-

- Sequential scan
- Index scan
- Bitmap scan

:question: Is there any other access method?

In addition to table rows, there are also non-table row source. For example `Values` clause and sets returned from `From` clause. There have different scan method. 

:question: What are those methods?

If the query requires joining, aggregation, sorting, or other operations on the raw rows, then there will be additional nodes above the scan nodes to perform these operations. 

`Seq Scan on tenk1  (cost=0.00..458.00 rows=10000 width=244)`

- Estimated start-up cost. This is the time expended before the output phase can begin, e.g., time to do the sorting in a sort node.
- Estimated total cost. This is stated on the assumption that the plan node is run to completion, i.e., all available rows are retrieved. In practice a node's parent node might stop short of reading all available rows (see the LIMIT example below).
- Estimated number of rows output by this plan node. Again, the node is assumed to be run to completion. The rows value is a little tricky because it is not the number of rows processed or scanned by the plan node, but rather the number emitted by the node. This is often less than the number scanned, as a result of filtering by any WHERE-clause conditions that are being applied at the node. Ideally the top-level rows estimate will approximate the number of rows actually returned, updated, or deleted by the query.
- Estimated average width of rows output by this plan node (in bytes).

**The costs are measured in arbitrary units determined by the [planner's cost parameters](https://www.postgresql.org/docs/9.4/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS). Traditional practice is to measure the costs in units of disk page fetches; that is, seq_page_cost is conventionally set to 1.0 and the other cost parameters are set relative to that. The examples in this section are run with the default cost parameters.**

**It's important to understand that the cost of an upper-level node includes the cost of all its child nodes. It's also important to realize that the cost only reflects things that the planner cares about. In particular, the cost does not consider the time spent transmitting result rows to the client, which could be an important factor in the real elapsed time;**

#### Bitmap Scan

Bitmap is the mechanism of sorting the rows. There are Bitmap index scan, bitmap heap scan

### Window Function

These functions sees rows other than the current rows. Therefore, they are useful to calculation where other rows are needed. Which other rows are visible depends on the defined window. Thus it is called window function.

This is comparable to the type of calculation that can be done with an aggregate function. However, window functions do not cause rows to become grouped into a single output row like non-window aggregate calls would. Instead, the rows retain their separate identities. 

A window function call always contains an OVER clause directly following the window function's name and argument(s). This is what syntactically distinguishes it from a normal function or non-window aggregate. 

The rows considered by a window function are those of the “virtual table” produced by the query's FROM clause as filtered by its WHERE, GROUP BY, and HAVING clauses if any. For example, a row removed because it does not meet the WHERE condition is not seen by any window function. A query can contain multiple window functions that slice up the data in different ways using different OVER clauses, but they all act on the same collection of rows defined by this virtual table.

There is another important concept associated with window functions: for each row, there is a set of rows within its partition called its window frame. Some window functions act only on the rows of the window frame, rather than of the whole partition. By default, if ORDER BY is supplied then the frame consists of all rows from the start of the partition up through the current row, plus any following rows that are equal to the current row according to the ORDER BY clause. When ORDER BY is omitted the default frame consists of all rows in the partition. 

Window functions are permitted only in the SELECT list and the ORDER BY clause of the query. They are forbidden elsewhere, such as in GROUP BY, HAVING and WHERE clauses. This is because they logically execute after the processing of those clauses

- [List of window functions](https://www.postgresql.org/docs/current/functions-window.html)
- [Window function processing](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-WINDOW)
- [Window function call](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS)
- [Window clause in Select](https://www.postgresql.org/docs/current/sql-select.html#:~:text=specified%20with%20HAVING.-,WINDOW%20Clause,-The%20optional%20WINDOW)







