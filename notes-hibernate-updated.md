# Hibernate

[Official Documentation](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#_getting_started_guide)

This is an ORM, that maps the objects to the database table. It also provides
abstraction for connection management.  Hibernate has its own query language
called HQL.

## Reverse Engineering

Generating class from database table.

- <tag-mapping>
- <table>

## State of Object

Using hibernate, you can only persist an object that has instance field. There
are three states of an object. They are -

- Transient: The object is in the memory, database has no knowledge of it.
- Persistent: The object is in the database. Hibernate manages the object. There
is an active connection between the object and the database. If there is any
change in the object, hibernate automatically updates the object in the
database.
- Detached: The object is persistent in the database but the session has been
closed.

## Session

Used to connect to the database. Open a session when needed and close it after
using it. There is a SessionFactory, which is instantiated at the startup that
provides session on demand. One SessionFactory per database. Persistent objects
are written and retrieved through a session object.

SessionFactory factory is thread safe but Session object is not thread safe.

## Domain Model

### Type

#### Value Type

In simple term these are the data members of a class that will be persisted.
These type doesn't define their own lifecycle.

1. Basic type
2. Embeddable type
3. Collection type

#### Entity Type

These are independent objects that has their own lifecycle.

### Naming Strategies

- 2 step process
- 1st step is to determine logical name
- 2nd step is to apply [PhysicalNamingStrategy](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#PhysicalNamingStrategy)

**For JPA compatibility use the logical naming strategy**

### Basic Type

See the full list of mapping [here](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#basic).

If we don't annotate a field with anything, a basic type is assumed.
Alternatively, we can use `@Basic` annotation.

**JPA has restriction on which Java types can be used as basic type. The following
types are allowed-**

- Java primitive types (boolean, int, etc)
- wrappers for the primitive types (java.lang.Boolean, java.lang.Integer, etc)
- java.lang.String
- java.math.BigInteger
- java.math.BigDecimal
- java.util.Date
- java.util.Calendar
- java.sql.Date
- java.sql.Time
- java.sql.Timestamp
- byte[] or Byte[]
- char[] or Character[]
- enums
- any other type that implements Serializable (JPA’s "support" for Serializable
    types is to directly serialize their state to the database).

**Explicit BasicTypes**

Specifying the BasicTypes to use explicitly by annotation.

**Mapping Enum**

### Embeddable Types

They are referred to as component in Hibernate. Embeddable types represents
composition relationship. It is a value type and its lifecycle is bound to the
parent entity.

Embeddable types can be made up of basic values as well as associations, with
the caveat that, when used as collection elements, they cannot define
collections themselves.

**JPA defines two terms for working with Embeddable types. `@Embeddable` to
specify a class that can be embedded into other class. `@Embedded` is for
referencing a given embeddable types.**

`Embedded` class form a composition relationship which is a better design in
OOP.

#### Multiple Embeddable Types

If there is multiple embeddable types in one entity, we need to customize the
mapping by overriding the column name and associations. [Read here](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#embeddable-multiple).

This is due to the fact that implicit naming strategy will derive the column
name from the field name. So, if there are two or more embeddable types, then
there will be conflict in column name.

JPA defines `@AttributeOverride` annotation to provide explicit name for columns
to resolve the conflict. If the embeddable type has any association then we need
to use `@AssociationOverride`.

#### Interface as Embeddable type

If we want to use an interface as an `Embeddable` type we need to provide the
implementing class as `@Target` attribute. [Read here](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#embeddable-Target).

### Entity type

#### Identifier attribute

Hibernate recommends to use either Long or Integer as identifier type.

#### Mapping entity

An entity models a database table. The `@Entity` annotation is used. It has a
name attribute. If we don't specify the name attribute, hibernate uses the
unqualified name of the class. So, there can't be same named class even in
different package.

The `@Entity` annotation has two attributes- `schema` and `catalog`.

#### Implementing `equals()` and `hashCode()`

This is super important and needs careful consideration.

[Read from here](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#mapping-model-pojo-equalshashcode)

#### Mapping an entity to SQL query

We can map an entity to the result of an SQL query.

[Read here](https://docs.jboss.org/hibernate/orm/5.4/userguide/html_single/Hibernate_User_Guide.html#entity-sql-query-mapping)

### Inheritance

#### MappedSuperClass

Inheritance is only at domain model level not database level. Polymorphic
queries are not possible.

#### Single table

If we don't specify inheritance strategy, hibernate will choose single table by
default.

Super-class and sub-classes are stored in the same table. Polymorphic queries
are possible. It is not possible to use `NOT NULL` constraint. This must be
enforced either in data access layer or by using `CHECK` or `TRIGGER`
constraints.

A discriminator is used to separate the sub-classes. It not provided, the
sub-class name is used as discriminator.

### Collection

## Transaction Object

## Mapping Strategies

## HQL

## Named parameter

## Aggregate methods

## Create Criteria API

Restricts the result to show.

## Associations

### ManyToOne

Annotated with `@ManyToOne`.



## Annotation list

**@Entity**

**@Embeddable**

@**Basic**

It has 2 attributes. `optional` and `fetch`.

`Optional` identifies a field as nullable.

`fetch` has two possible values- `Eager` and `Lazy`. Hibernate ignores this
setting for basic type and defaults to `Eager` which means the value will be
retrieved from database when the owner is retrieved. `Lazy` means the value will
be retrieved when it is accessed.

**@Column**

The name of the cloumn in the table.

