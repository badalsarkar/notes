# REST Service with Spring

# Table of Contents

- [REST Service with Spring](#rest-service-with-spring)
- [Table of Contents](#table-of-contents)
  - [Annotations](#annotations)
    - [@Entity](#entity)
    - [@SpringBootApplication](#springbootapplication)
    - [@RestController](#restcontroller)
  - [Exception Handling](#exception-handling)
  - [Lombok](#lombok)
    - [@Data](#data)
  - [Java Persistence API (JPA)](#java-persistence-api-jpa)
    - [Entity](#entity-1)
    - [Requirements for Entity Classes](#requirements-for-entity-classes)
  - [**Spring Data JPA**](#spring-data-jpa)
    - [How to handle the inheritance relationship?](#how-to-handle-the-inheritance-relationship)
    - [Pagination](#pagination)
  - [Java](#java)
    - [Optional Class](#optional-class)
  - [Testing Rest API in Spring](#testing-rest-api-in-spring)
    - [@WebMvcTest](#webmvctest)
    - [MockMvc](#mockmvc)
    - [@MockBean](#mockbean)
    - [TestRestTemplate](#testresttemplate)
    - [RestTemplate](#resttemplate)
  - [Spring HATEOAS](#spring-hateoas)
    - [Links](#links)
    - [Representation Model](#representation-model)
    - [Representation Model Assembler](#representation-model-assembler)

## Annotations

### @Entity

This annotation marks a POJO as JPA entity which is an object. The nontransient
fields of this object is persisted into a relational database by an entity
manager. Entity manager is managed by the container.

All the data fields of an entity is persisted unless the field is annotated with
`@Transient`.

The JPA persistence provider is specified in the `persistence.xml` file. In
spring boot this configuration is done automatically. So, a separate
`persistence.xml` file is not needed.

The data type of the fields are automatically configured by the persistence
provider. However, we can specify `@Basic`, `@Enumerated`, `@Temporal` and
`@Lob`.

The relationship between entities are configured by `@OneToOne`, `@ManyToOne`,
    `@OneToMany`, and `@ManyToMany`.

Each entity must have primary key. The primary keys are restricted to the
following-

- primitive object types
- serializable type
- types that can be mapped to SQL types

[Source](https://docs.oracle.com/cd/E16439_01/doc.1013/e13981/undejbs003.htm)

### @SpringBootApplication

It is a meta-annotation, meaning it provides information about annotation. This
annotation pulls in `component scanning`, `autoconfiguration` and `property
support`. This annotation will fire up a servlet container and serve our
service.

A bean of type **@CommandLineRunner** is automatically run by Spring Boot when
it loads the application context.

### @RestController

This is a meta annotation which combines `@Controller` and `@ResponseBody`. The
`@Controller` annotation for a class makes the class a bean and allows for
auto-detecting and auto-registering. It also describes the class's role as a web
component. The `@ResponseBody` annotation indicates that every methods of a
controller class inherits the type-level `@ResponseBody` which means that they
will write directly to response body instead of resolving a view and rendering
an HTML template.


## Exception Handling

Different implementation of exception handling in Spring Framework-

- ExceptionHandlerExceptionResolver- define exception handler methods in
controllers
- SimpleMappingExceptionResolver- map each exception class with an error page
- DefaultExceptionResolver- default which maps exceptions to error codes
- ResponseStatusExceptionResolver- resolves custom exceptions using status code
defined in @ResponseStatus

For some exceptions we may create a handler that will work application wide-
meaning where ever the exception is generated from the application, this handler
will handle the exception. To do this we need to create a class and annotate it
with `@ControllerAdvice`. The class with this annotation is a specialized class
that declares `@ExceptionHandler`, `@InitBinder` or `ModelAttribute` methods.
For exception handling we will use `@ExceptionHandler`. One more thing, the
`@ControllerAdvice` annotated class doesn't have to be applied globally. We can
restrict the scope by using `annotations()`, `basePackageClasses()` or
`basePackages()` selectors. [Source](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/bind/annotation/ControllerAdvice.html)

## Lombok

### @Data

Generates getters, setters, hashCodeAndEquals, toString and constructors. If a data field is final no setter
will be generated. If a data field is marked as transient, it will not be used
for hashCodeAndEquals generation.

## Java Persistence API (JPA)

[Source](https://docs.oracle.com/javaee/7/tutorial/persistence-intro001.htm#BNBQA)

### Entity

An entity is a lightweight persistence domain object. Typically, an entity
represents a table in a relational database, and each entity instance
corresponds to a row in that table. The primary programming artifact of an
entity is the entity class, although entities can use helper classes.

The persistent state of an entity is represented through either persistent
fields or persistent properties. These fields or properties use
object/relational mapping annotations to map the entities and entity
relationships to the relational data in the underlying data store.

### Requirements for Entity Classes


An entity class must follow these requirements.

- The class must be annotated with the javax.persistence.Entity annotation.

- The class must have a public or protected, no-argument constructor. The class
may have other constructors.

- The class must not be declared final. No methods or persistent instance
variables must be declared final.

- If an entity instance is passed by value as a detached object, such as through
a session bean's remote business interface, the class must implement the
Serializable interface.

- Entities may extend both entity and non-entity classes, and non-entity classes
may extend entity classes.

- Persistent instance variables must be declared private, protected, or
package-private and can be accessed directly only by the entity class's methods.
Clients must access the entity's state through accessor or business methods.

The persistent state of an entity can be accessed through either the entity's
instance variables or properties.

## **Spring Data JPA**

[Java Persistence API (JPA)](https://docs.oracle.com/javaee/7/tutorial/persistence-intro.htm)

### How to handle the inheritance relationship?

JPA supports class inheritance, polymorphic association and polymorphic queries.
This means that if there is `Entity A` which is an abstract class and `Entity B`
and `Entity C` both of which extends `Entity A`, then any query on `Entity A`
will also be run on `Entity B` and `C`.

Entity classes can extend non-entity classes, and non-entity classes can extend
entity classes. Entity classes can be both abstract and concrete.

### Pagination

## Java

### Optional Class

A container object which may or may not contain a non-null value. If a value is
present, isPresent() returns true. If no value is present, the object is
considered empty and isPresent() returns false.  Additional methods that depend
on the presence or absence of a contained value are provided, such as orElse()
  (returns a default value if no value is present) and ifPresent() (performs an
      action if a value is present).

This is a value-based class; use of identity-sensitive operations (including
    reference equality (==), identity hash code, or synchronization) on
instances of Optional may have unpredictable results and should be avoided.

API Note: Optional is primarily intended for use as a method return type where
there is a clear need to represent "no result," and where using null is likely
to cause errors. A variable whose type is Optional should never itself be null;
it should always point to an Optional instance.


## Testing Rest API in Spring

### @WebMvcTest

### MockMvc

### @MockBean

### TestRestTemplate

This is convenient alternative to RestTemplate that is suitable for integration
tests. They are fault tolerant and optionally can carry Basic authentication
headers. When we use the `@SpringBootTest`, this is automatically available. All
we need to do is to autowire it.

### RestTemplate

Synchronous client to perform HTTP request.

## Spring HATEOAS

### Links

It makes it easy to create links for resource.

> Spring HATEOAS lets you work with links through its immutable Link value type.
> Its constructor takes both a hypertext reference and a link relation, the
> latter being defaulted to the IANA link relation self. Read more on the latter
> in Link relations.

- Link type, LinkRelation type
- Templated Link
- IANA (Internet Assigned Numbers Authority) provides some [pre-defined link
relations](https://www.iana.org/assignments/link-relations/link-relations.xhtml).

### Representation Model

Makes it easy to create links. Its container for collection of Links. The
created model can then be rendered into different media type.

`RepresentationModel` is the root of all the representation models. [See
here](https://docs.spring.io/spring-hateoas/docs/1.2.2/reference/html/#fundamentals.representation-models).

### Representation Model Assembler





