# Spring Boot

- @EnableAutoConfiguration
- spring.factories
- Conditional loading
- @ConditionalOnClass
- @ConditionalOnBean
- @ConditionalOnProperty
- @ConditionalOnMissingBean
- @EnableConfigurationProperties
- Properties can be overridden
- Application type based conditional
- Resource based conditional
- Expression based conditional
- Spring expression language

## Configuring Spring

- Property based configuration
- application.properties or application.yml: These are basic
- Environmental variable: Modify runtime environment
- Command line injection
- Cloud configuration(config server, vault, consul)

## Bean Configuration

## Profile

Spring boot support yml file.

## Spring Boot Starter 

- Tomcat
- JSON Marshaller
- Logging framework: Slf4j
- Spring library - core, AOP, beans, context, exprssion
- Spring web and webmvc
- SnakeYAML
- Validators

## Bootstarting Spring

[source: Spring boot in action by Craig Walls]

- Spring started as lightweight alternative to JEE or J2EE. EJBs are heavyweight
objects. Spring with the help of dependency injection and aspect-oriented
programming, provided the same functionality with POJOs.

Spring boot performs four tricks/ activities under the hood:

1. Automatic configuration- Spring Boot can automatically provide configuration
   for application functionality common to many Spring applications.
2. Starter dependency- You tell Spring Boot what kind of functionality you need,
   and it will ensure that the libraries needed are added to the build.
3. The CLI- This optional feature of Spring Boot lets you write complete
   applications with just application code, but no need for a traditional
   project build.
4. The actuator- Gives you insight into what’s going on inside of a running
   Spring Boot application.
      
Busting some misconceptions-

- Spring Boot doesn’t employ any form of code generation to accomplish its
magic. Instead, it leverages conditional configuration features from Spring 4,
  along with transitive dependency resolution offered by Maven and Gradle, to
  automatically configure beans in the Spring application context.

## Working with spring application

- The main class performs two purposes: configuration and bootstraping.

**@SpringBootApplication**: Combines three annotations- @Configuration,
  @ComponentScan, and @EnableAutoConfiguration.

