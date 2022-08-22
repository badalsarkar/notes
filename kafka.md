---
mindmap-plugin: basic
---

# kafka

## what
- distributed streaming platform

## concepts
- message
   - unit of data
   - similar to row in database perspective
   - messages are written in batches
   - they are compressed
- key
   - metadata of message
   - optional
   - just array of bytes
   - used when messages are to be written to partition in a more controlled manner
   - message with same key written to same partition
      provided partition count doesn't change
- schema
   - structure of message
   - JSON/ XML
   - tools
      - Apache Avro
         - serialization framework
- topic
   - category of messages
   - analogous to database table
   - AKA stream
   - they are broken down into partitions
   - messages are written as append only at the end of the partition
   - messages are not guaranteed to be in order across partitions
- partition
   - scalability
      - can be hosted on different server
      - can be replicated
- producer
   - create new messages
   - balance messages across partitions
   - sets offset
- consumer
   - read messages in order from partition
   - keeps track of which messages has been consumed using offset
- consumer group
   - collection of consumers consuming 1 topic
   - ensures each partition is consumed by 1 member
   - the mapping of consumer to a partition is called partition ownership
   - if a member fail remaining members will be assigned to take over
- brokers
   - a single kafka server
   - assigns offset
   - writes messages to disk
   - operate as part of a cluster
   - within the cluster 1 broker work as controller elected automatically by live members
   - a partition is owned by a single broker
      - it is called leader
         - there can be multiple follower if the partition is replicated
            - this ensures redundancy
         - all producer must connect to it
         - but consumers can either connect to it or the followers
- retention
   - specifies how long the data will be stored

## components
- kafka client
- Kafka Connected API
   - Data integration
- Kafka Streams
   - for stream processing