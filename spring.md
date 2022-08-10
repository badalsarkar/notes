# SPRING FRAMEWORK

## Introduction

Spring is a lightweight Inversion of Control (IoC) and aspect-oriented container
framework.  Historically, it was created to alleviate the complexity of the then
J2EE standard, often giving an alternative model. Any Java EE application can
benefit from the Spring Framework in terms of simplicity, loose coupling, and
testability.

Spring's main aim is to promote good programming practice such as coding to
interfaces and make Java EE easier to use. It does this by enabling a Plain Old
Java Object (POJO)-based programming model, which can be applicable in a wide
range of development environments.

Technically, a POJO is any ordinary object that should not implement
pre-specified interface or extend pre-specified class or contains annotation.

```java
/* This is a simple Java Class – POJO */ 
public class POJOClass {
  private String message; public String getMessage() { 
    return this.message; 
    }
  public void setMessage(String message) { 
    this.message = message; } } 
```

In the preceding code snippet, we have POJOClass containing a field and
corresponding getter and setter methods. This class is a POJO class as it is not
extending or implementing any class or predefined interface of Spring API.

**Question** Does POJO mean we are not allowing inheritance?

### Features of Spring

- Lightweight
- Non-intrusive
- IoC
- ASP(Aspect Oriented Programming): Aspects can be added or removed without
                                    changing your code
- JDBC exception handling
- Spring MVC
- Spring security

Spring first released on March 2004.

Spring provides you some modules and you choose which one to use.

![Spring Framework](./images/springFramework.png "Spring Framework")

### Spring Core Container Module

Spring core consists of following modules:

#### Core

The core module provides the IoC mechanism.

#### Beans

This module provides a BeanFactory.

**What is BeanFactory?** A BeanFactory is like a factory class that contains a
collection of beans. The BeanFactory holds Bean Definitions of multiple beans
within itself and then instantiates the bean whenever asked for by clients.  The
BeanFactory is the actual container which instantiates, configures, and manages
a number of beans

BeanFactory in spring core supports two scopes modes of object:

- Singletone
- Prototype

#### Context

Provides the ApplicationContext which loads the Bean definitions and wires them
together.

#### Expression Language

Spring Expression Language (SpEL) is a powerful expression language supporting
the features for querying and manipulating an object graph at runtime. SpEL can
be used to inject bean or bean property in another bean. SpEL supports method
invocation and retrieval of objects by name from IoC container in Spring.

### AOP Module

The Spring framework uses the AOP for providing most of the infrastructure logic
in it.  AOP is a mechanism that allows us to introduce new functionalities into
an existing code without modifying it design. AOP is used to weave cross-cutting
aspects into the code. The Spring Framework uses AOP to provide various
enterprise services, such as security in an application. The Spring AOP
framework is configured at runtime.

Spring integrates with AspectJ, which is an extension of AOP. AspectJ lets
programmers define special constructs called Aspects, which contains several
entities unavailable to standard classes.

### Data Access/ Integration

#### JDBC Module

#### ORM Module

#### OXM Module

Provides support to convert Java Beans to XML and XML to Java Beans. This helps
in communication with other systems. Spring also has module to do conversion
between JSON and Object.

#### JMS module

This is a specification for Java programs to create, send and read distributed
enterprise messages.  Spring Java mail provides support for electronic mail.

#### Transaction module

### Web Module

Helps to build large scale web application

#### Web module

#### Servlet module

Supports the MVC pattern for web development

#### Struts module

Integrate struts

#### Portlet module

For UI layer

### Test Module

Helps in testing application either using JUnit or TestNG.

## Inversion of Control

In software engineering, IoC is a programming technique in which object coupling
is bound at runtime by an assembler object and is usually not known at compile
time using static analysis.

IoC is a more general concept, whereas DI is a concrete design pattern.

IoC is a way of thinking; a mechanism is required to activate components that
provide specific functionality, due to which IoC depends on DI. The IoC pattern
inverts responsibility of the managing the life cycle from the application to
the framework, which makes writing Java applications even easier. IoC makes your
code more manageable, more testable, and more portable. IoC also keeps component
dependencies, life cycle events, and configuration outside of the components.

![Without IoC](./images/withoutIoC.png "Without IoC")

![With IoC](./images/withIoC.png "With IoC")

### What is a Container

In software development terminology, the word "container" is used to describe
any component that can contain other components inside it. For example, Tomcat
is a web container to contain deployed WAR files. JBoss is an application
server/container; it contains an EJB container, web container, and so on.

The container first creates the objects and then wires them together, after
which it moves on to configure them, and finally manage their complete life
cycle. It identifies the object dependencies, creates them, and then injects
them into the appropriate objects.

So, we can think about a container as an intermediate who'll register vehicle
and car objects as separate entities, create the vehicle and car objects, and
inject the vehicle object into car.

### Spring Container

Spring Container is the central component of the Spring Framework. Spring
Container manages the life cycle of an application's bean, which will live
within Spring Container. Spring Container is responsible for wiring an
application's beans by associating different beans together. Spring Container
manages the components of applications using DI. The configuration metadata,
        which can be represented in XML, Java annotations, or Java code, helps
        Spring Container to decide the object to initiate, configure, and
        assemble.

Let's take an example of Tomcat, which is a Servlet container. Tomcat creates
the Servlet objects, which are required in order to run an application. While
deploying an application, we configure all Servlets in an XML file. Tomcat reads
this XML file, identifies the Servlet to be instantiated, and then creates the
identified Servlet.

Spring is a container but not a container of Servlet. It is a container of beans
and behaves as a factory of beans. So, we can have Spring Container and we can
have as many objects as we want, as shown in the following diagram. Also, all
these objects are managed by Spring Container. The container handles the
instantiation of object, their whole life cycle, and finally their destruction
too:

![Spring Container](./images/springContainer.png "Spring Container")

### Beans

Beans are reusable software components that are managed by the Spring IoC
container. It contains the properties, setter, and getter methods of a class.

The Spring IoC container is represented by the interface
org.springframework.context.ApplicationContext, which is responsible for
instantiating, configuring, and assembling beans. Beans are reflected in the
configuration metadata used by a container. The configuration metadata defines
the instruction for the container and the objects to instantiate, configure, and
assemble. This configuration metadata can be represented in XML, Java
annotations, or Java code. In this chapter, we will configure using XML, which
has been the traditional format to define configuration metadata.

### XML Configuration

This XML file has <beans> as the root element and it has <bean> as child
element. <bean> element holds the configuration of a bean. Each <bean> element
has a mandatory class attribute and optional Id and name attribute. The class
attribute holds the fully qualified class name, id attribute provides uniqueness
of bean.

Spring provides two interfaces for container-

- BeanFactory: This is the general interface which is implemented by all other
container
- ApplicationContext: This is the interface for Enterprise Application. It is a
subinterface of BeanFactory. This container provides WebApplicationContext for
web applications.

### BeanFactory

It is a central place to instantiate object. There are many implementations of
the BeanFactory interface, with the
org.springframework.beans.factory.xml.XmlBeanFactory.

The constructor of xmlBeanFactory takes a Resource. Resource has two most commn
implementations are

- FileSystemResource
- ClassPath resource

BeanFactory is a lazy container. On instantiation the container doesn't
instantiate beans.

### Application Context

ApplicationContext is active container. As soon as the ApplicationContext is
created, it instantiates all the configured beans.

- ClassPathXmlApplicationContext: This bean definition is loaded by the
container from the XML file that is present in the classpath by treating context
definition files as classpath resources.  ApplicationContext can be loaded from
within the application's classpath using ClassPathXmlApplicationContext:
- FileSystemXmlApplicationContext: This bean definition is loaded by the
container from an XML file.  Here, the full path of the XML bean configuration
file should be provided to the constructor:
- XmlWebApplicationContext: This is used to create the context in web
application by loading configuration the XML file with definitions of all beans
from standard locations within a web application directory. The default location
of the configuration XML file is /WEB-INF/applicationContext.xml.  
- AnnotationConfigWebApplicationContext: This is used to create the web
application context by loading the Java classes annotated with the
@Configuration annotation instead of XML files in the web application.

## Dependency Injection

Dependency Injection (DI) is a design pattern in which an object's dependency is
injected by the framework rather than by the object itself. It reduces coupling
between multiple objects as it is dynamically injected by the framework. In DI,
        the framework is completely responsible for reading configuration.

The advantages of DI are as follows:

- Loosely coupled architecture.
- Separation of responsibility.
- Configuration and code are separate.
- A different implementation can be supplied using configuration without
changing the code dependent.
- Improves testability.
- DI allows you to replace actual objects with mock objects. This improves
testability by writing simple JUnit tests that use mock objects.

### DI in Spring

[Read
here](https://learning.oreilly.com/library/view/spring-developing-java/9781787127555/ch02s02.html)
Two ways DI is done

- Constructor injection
- Setter injection

IoC container uses setter injection to set value before handing over the object.

#### Injecting Collections

#### Injecting Inner Beans

#### Injecting null and empty string

### Bean definition inheritance

It is not same as class inheritance in Java. Here the parent bean is used as
template to be reused in the child beans.

#### Inheritance with abstract

If we make a parent bean abstract, it can't be instantiated. It can only be used
as template.

### Autowiring in Spring

The Spring Framework provides autowiring features where we don't need to provide
bean injection details explicitly. The Spring container can autowire
relationships between collaborating beans without using the <constructor-arg>
and <property> elements. This immensely helps in cutting down the XML
configuration. Spring is capable of automatically resolving dependencies at
runtime. This automatic resolution of bean dependencies is also called
autowiring.

Autowiring can by done by-

- Byname
- Bytype
- ByConstructor

### Bean Scope

There are different bean scope.

- Singletone
- Prototype
- request
- session and
- global session

#### Singletone

By default all the beans in one instance of Spring container has singletone
scope which means there will be only one instance of a class in one container.
Of course, there can be multiple container running in JVM.

#### Prototype

The prototype is second bean scope in Spring, which returns a brand-new instance
of a bean on each call to the getBean() method. When a bean is defined as a
prototype, Spring waits for getBean() to happen and only then does it initialize
the prototype. For every getBean() call, Spring has to perform initialization,
    so instead of doing default initialization while a context is being created,
    it waits for a getBean() call. So, every time getBean() gets called, it
    creates a new instance.

Spring doesn't maintain the complete life cycle of the prototype. Here, the
container instantiates and configures prototype beans and returns this bean to
the client with no further record of this prototype instance.

#### Request Scope

The third bean scope in Spring is request, which is available only in web
applications that use Spring and create an instance of bean for every HTTP
request. Here, a new bean is created per Servlet request. Spring will be aware
of when a new request is happening because it ties well with the Servlet APIs,
   and depending on the request, Spring creates a new bean. So, if the request
   scope has getBean() inside it, for every new request, there will be a new
   bean. However, as long as it's in the same request scope, the same bean is
   going to be used.

#### Session Scope

The session is the fourth bean scope in Spring, which is available only in web
applications that use Spring and create an instance of bean for every HTTP
session. Here, a new bean is created per session. As long as there is one user
accessing in a single session, each call to getBean() will return same instance
of the bean. But if it's a new user in a different session, then a new bean
instance is created.

#### Global Session

The global session is the fifth bean scope in Spring, which works only in
portlet environments that use Spring and create a bean for every new portlet
session.

### Spring Bean Life Cycle

Spring provides us with callback methods for life cycle events. These callbacks
are categorized into two groups:

- Post-initialization callback methods
- Pre-destruction methods

![Bean Lifecycle](./images/beanLifecycle.png "Bean Lifecycle")

#### Initialization

**Initialization Callback**

This can be achieved by either implementing InitializingBean interface or
providing a init() method.

The InitializingBean interface provides a function afterPropertiesSet(). The
implementing class defines this function. When a bean is initialized this
function is called.

Otherwise, we can provide a init-method attribute in the bean.xml file. With
this we need to provide a void no-argument function which will be called as part
of initialization.

**Destruction Callback**

This can be achieved either implementing DisposableBean interface or
destroy-method attribute in xml file.


#### Activation

The bean has been initialized and the dependency has been injected. Now the bean
is ready to be used by the application.

#### Destruction

This represents the following sequence of activities:

- If the Bean class implements the DisposableBean interface, then call the
destroy() method when the application no longer needs the bean reference 
- If the bean definition in the configuration file contains the destroy-method
attribute, then call this method after resolving the value for the attribute to
a method name in the Bean class.

## DAO and JDBC in Spring

### DAO design pattern

![DAO Design Pattern](./images/DAO.png "DAO Design Pattern")

Spring JDBC provides abstraction to access database and perform database
operations. 

Spring JDBC package,Description core,Simplifies database operation using JDBC
datasource,DataSource implementation object,Contains classes that convert
database result into Java object support,Exception support config,Contains
classes that support JDBC configuaration within ApplicationContext

To connect to database-

Put DataSource configuaration in the xml file.

The central class of the Spring JDBC abstraction framework is the JdbcTemplate
class that includes the most common logic in using the JDBC API to access data,
      such as handling the creation of connection, statement creation, statement
      execution, and release of resource.

### JDBC Template

The JdbcTemplate class instances are thread-safe once configured. A single
JdbcTemplate can be configured and injected into multiple DAOs.

- setup JdbcDataSource 
- configure JdbcTemplate
- User JdbcTemplate api

### JDBC Batch Processing

The batch update operation allows you to submit multiple SQL queries to the
DataSource for processing at once. Submitting multiple SQL queries at once
instead of submitting them individually improves the performance.

This section explains how to use an important batch update option with the
JdbcTemplate. The JdbcTemplate includes a support for executing the batch of
statements through a JDBC statement and through PreparedStatement.

The JdbcTemplate includes the following two overloaded batchUpdate() methods
that support this feature:

- public int[] batchUpdate(String[] sql) throws DataAccessException
- public int[] batchUpdate(String sql, BatchPreparedStatementSetter bPSS) throws
DataAccessException

### Stored Proccedures

Database operation saved in the database.

## Hibernate

It is an ORM for Java. The query language is called HQL.

![Hibernate](./images/Hibernate.png "Hibernate with Java")

Hibernate makes use of various existing Java APIs such as Java Database
Connectivity (JDBC), Java Naming and Directory Interface (JNDI), and Java
Transaction API (JTA). JDBC supports functionality common to relational
databases, which allows almost any database with a JDBC driver to be supported
by Hibernate, whereas JTA and JNDI allow Hibernate to be integrated with Java EE
application servers.

![Hibernate flow](./images/HibernateFlow.png "Hibernate Flow")

The hibernate.properties and hibernate.cfg.xml files are configurations files
that are supported by Hibernate. We can use the hibernate.properties file to
specify the default values for the new configuration object.

### Session Factory

The org.hibernate.SessionFactory interface provides an abstraction for the
application to obtain the Hibernate session object. The SessionFactory
initialization process includes various operations that consume huge resources
and extra time, so it is generally recommended to use a single SessionFactory
per JVM instance. For each database, we need to have one SessionFactory using a
separate configuration file. So we have to create multiple SessionFactory if we
are using multiple databases.

The SessionFactory is a heavyweight and immutable towards the application; that
is, it is a thread safe object. It is mostly configured as a singleton in an
application so that there will be only one object per application. It is usually
created during the startup of an application and is kept for later reference.
The SessionFactory is used by all threads of the application. We can open
multiple sessions using a single SessionFactory.

### Session

The org.hibernate.Session interface is an interface between the Hibernate system
and the application. It is used to get the connection with a database. It is
light weight and is initiated each time an interaction is needed with the
database.

Session objects are not usually thread safe and it is recommended to obtain a
separate session for each thread or transaction. After we are done using
session, it has to be closed to release all the resources such as cached entity
objects and the JDBC connection.

The Session interface provides an abstraction for Java application to perform
CRUD operations on the instance of mapped persistent classes.

### Transaction

The Transaction interface is an optional interface that represents a unit of
work with the database.  It is supported by most RDBMS systems. In Hibernate,
     Transaction is handled by the underlying transaction manager.

### Query

The org.hibernate.Query interface provides an abstraction to execute the
Hibernate query and to retrieve the results. The Query object represents the
Hibernate query built using the HQL. We will learn about the Query interface in
more detail in a later section of this chapter.

### Criteria

The org.hibernate.Criteria interface is an interface to use the criterion API
and is used to create and execute object-oriented criteria queries, which is an
alternative to HQL or SQL.

### Persistent Object

Persistent classes are the entity classes in an application. Persistent objects
are objects that are managed to be in the persistent state. Persistent objects
are associated with exactly one org.hibernate.Session. And once the
org.hibernate.Session is closed, these objects will be detached and will be free
to be used in any layer of the application.

### Configuration of Hibernate SessionFactory with Spring

We create a spring bean that represents the JDBC DataSource or Hibernate
SessionFactory. This prevents us from hard coding the resource lookup for
application object. ApplicationContext uses this bean reference.

The Hibernate session interface is used for CRUD operation. The session object
is created by first creating SessionFactory. Spring provides many classes to
configure the SessionFactory.

For Session creation Spring provides implementation of
**LocalSessionFactoryBean** and **AnnotationSessionFactoryBean**.

packagesToScan is a property for Hibernate configuration file. This tells
hibernate which packages to scan for Annotated Classes. hibernateProperties
defines the configuration for hibernate.

**Hibernate Properties**

hibernate.dialect: Specifies which database I am using

max_fetch_depth: This property is used to set the maximum depth for the outer
join when the mapping object is associated with other mapped objects. This
property is used to determine the number of associations Hibernate will traverse
by join when fetching data. The recommended value lies between 0 and 3.

fetch_size: This property is used to set the total number of rows that can be
retrieved by each JDBC fetch.

show_sql: This property file is used to output all SQL to the log file or
console, which is an alternative to set log to debug and troubleshooting
process. It can be set to either True or False.

Hibernate provides JPA implementation which allows user to use JPA annotation in
model beans.

### Hibernate Query Language

This is an object oriented query language that works on objects and properties
not on tables and columns. Hibernate converts these HQL into SQL.

Basically we create a query object that provides many methods.

### Hibernate Criteria Query Language (HCQL)

This supports methods to add criteria on a query. Session interface provides a
method to create Criteria object. We can add restrictions to the criteria
object. For example, salary = 2000.

HQL provides methods to add restrictions.

## Spring Security

Spring security is primarily targeted towards spring framework based web
applications. Spring security handles both authentication and authorization at
request level and method invocation level.

Request level is not enough for web application as urls can be manipulated and
thus some methods can be invoked. Therefore, we need method level security that
ensures that only the designated person can invoke certain methods.

## Building a Spring MVC Application


## Spring Classes/Interfaces

## Hibernate Classes/Interfaces

1. AnnotationSessionFactoryBean 2. 


