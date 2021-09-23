# Spring Notes from Documentation

## Core Technologies

### Inversion of Control(IoC) Container

The container manages the instantiation of the objects. Objects don't
instantiate other objects they are dependent on by themselves.

Two packages are the basis for this container-

- `org.springframework.beans`
- `org.springframework.context`

`BeansFactory` interface in the `beans` package, provides configuration and basic
functionality and the `ApplicationContext` in `context` package provides more
enterprise specific functionality. This is a sub-interface of `BeansFactory`.

### Container Overview

`org.springframework.context.ApplicationContext` is the IoC container. It needs
a configuration file for configuring the objects. Spring provides many
implementations of this interface. For standalone application two most common
implementations are-

- [`ClassPathXmlApplicationContext`](https://docs.spring.io/spring-framework/docs/5.3.2/javadoc-api/org/springframework/context/support/ClassPathXmlApplicationContext.html)
- [`FileSystemXmlApplicationContext`](https://docs.spring.io/spring-framework/docs/5.3.2/javadoc-api/org/springframework/context/support/FileSystemXmlApplicationContext.html)

#### Configuration Metadata

These are provided by either of the following methods-

- XML file
- [Annotation based](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-annotation-config)
- [Java based](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#beans-java)

In the xml file the configuration for objects are given inside `<bean>` element.

>> Typically, you define service layer objects, data access objects (DAOs),
>> presentation objects such as Struts Action instances, infrastructure objects
>> such as Hibernate SessionFactories, JMS Queues, and so forth. Typically, one
>> does not configure fine-grained domain objects in the container, because it
>> is usually the responsibility of DAOs and business logic to create and load
>> domain objects.

#### Instantiating a Container

For different types of objects, we can create different configuration files and
pass those while instantiating IoC container. The configuration files can be
passed to the constructor or can be imported in the application context
configuration file as below-

![Multiple configuration file ](./images/multiple-configuration-file.png
    "Multiple configuration file")




