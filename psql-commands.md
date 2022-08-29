---
mindmap-plugin: basic
---

# psql commands

## commands
- [cluster](https://www.postgresql.org/docs/current/sql-cluster.html)
   - physically reorder a table according to a given index
   - it is a one time operation
   - data insertion or deletion doesn't update the clustered data
- [analyze](https://www.postgresql.org/docs/current/sql-analyze.html)
   - collects statistics on a table
   - statistics are used to plan query later on