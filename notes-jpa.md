# Java Persistent API(JPA)

Makes it easy to map object to relational database. It is an alternative to JDBC.

## What is persistence

## Entity Manager

To work with JPA, we need to configure an EntityManager which performs the CRUD operations.
Previously the configuration used to be in XML file. But now Spring supports anonotation based
configuration. EntityManager is thread safe.

## Annotations

- @PersistenceContext : Injects an EntityManager from EntityManagerFactory.
- @Transient: This field will not be persisted into database.

### JPA CRUD

- Create: EntityManager.persist();
- Read: EntityManager.find(class type, parameter);
- Update: There is no method for updating. The update automatically happens in a managed entity. An
entity becomes a managed entity once it is persisted. To update a record, first use find method of
EntityManager to find the record, then update the object, then call EntityManager.flush(). The
flush() methods synchronizes the object to the database.
- Delete: EntityManager.remove(); Before removing an entity, it has to be retrieved from database.
In order to remove an entity, it has to be a managed entity.

## Entity Lifecycle

The lifecycle of entity is different from POJO because entity is managed by EntityManager. An entity
can have four state-

- Transient: An entity is created but not persisted yet.
- Managed: After persisting.
- Removed: If marked for deletion.
- Detached: The final lifecycle state. An entity is in detached state if it is marked for deletion,
  committed, or flushed. Detached entities are entitle for garbage collected.

## JTA (Java Transaction Manager)

Transactions are automatically managed by the container. We just need to include @Transactional
anonotation.

## Default Mapping Strategy

In order to declare a class as an entity, it must have a public or protected no argument
constructor, no instance variable or getter/setter method can be final. The class must not be final.
Every entity must have a primary key.

The mapping happens following some default mapping rules. But we can also customize these rules.

Default rules:

- Entity class name -> table name
- Id -> primary key
- Attributes -> column name
- string -> varchar(255)

## Mapping Relationship and dependencies

- @ManyToOne
- @JoinTable: Uses a third table to associate two other tables
- @JoinColumn: Foreign key relationship

## Cardinality

- @OneToOne -> @JoinColumn
- @OneToMany -> @JoinTable
- @ManyToOne -> @JoinColumn
- @ManyToMany -> @JoinTable

## Cascading

@todo further study
