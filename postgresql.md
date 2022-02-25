# Learning PostgreSQL

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









## Logging in

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

## Some commands

Once inside the postgres terminal-

**`\list`**

Lists all databases.

**`\c ${databasename}`**

Switch to database.

**`\dt`**

Lists all tables in the database.

## Data Types

### JSON

- _jsonb_ is faster to process and also supports indexing


## Performance

### EXPLAIN

PostgreSQL devises a query plan for each query it receives. Choosing the right plan to match the query structure and the properties of the data is absolutely critical for good performance, so the system includes a complex planner that tries to choose good plans. You can use the EXPLAIN command to see what query plan the planner creates for any query. 









