# Learning PostgreSQL

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







