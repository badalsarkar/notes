# Java EE

# Table of Contents

- [Java EE](#java-ee)
- [Table of Contents](#table-of-contents)
  - [What is Java EE](#what-is-java-ee)
    - [Multi-tired Application](#multi-tired-application)
      - [Java Technologies Used in Web Tire](#java-technologies-used-in-web-tire)
      - [Java Technologies Used in business tire](#java-technologies-used-in-business-tire)
  - [Java Servlet Technology](#java-servlet-technology)
    - [Servlet Lifecycle](#servlet-lifecycle)
    - [Creating and Initializing a Servlet](#creating-and-initializing-a-servlet)
    - [Dealing with Request and Response](#dealing-with-request-and-response)
    - [Filters](#filters)
    - [Context](#context)
    - [Session Configuration](#session-configuration)
    - [Listeners](#listeners)
  - [Java Server Pages (JSP)](#java-server-pages-jsp)
    - [Directives](#directives)

## What is Java EE

Java EE is a platform to develop large scale, complex, multi-tired, scalable software. The platform
provides VM and API for development. There are 4 platforms in Java.They are-

1. Java SE (Standard Edition)
2. Java EE (Enterprise Edition)
3. Java ME (Micro Edition)
4. JavaFX

Java EE 8 is the latest version of Java EE.

[Nicely written here](https://docs.oracle.com/javaee/6/firstcup/doc/gkhoy.html)

### Multi-tired Application

Typically three tires-

1. Client Tire/Web Components(JSP/Servlet/EL/JSF/JavaBeans)
2. Web Tire - Handles the interaction between client tire and business tire.
3. Middle/Business Tire
4. Data Tire

Java EE concentrates on the middle tire.

[Read more](https://javaee.github.io/tutorial/overview004.html)

#### Java Technologies Used in Web Tire

1. Servlet: This are Java programming classes that process the request and construct response,
   usually for HTML page.
2. JavaServer Faces Technologies
3. JavaServer Faces Faceletes Technologies
4. Expression Language
5. JavaServer Pages
6. JavaServer Pages Standard Tag Library
7. JavaBeans Components

#### Java Technologies Used in business tire

1. Enterprise JavaBeans Components: *JavaBeans are classes in Java that encapsulates many objects
   into a single object.*
2. JAX-RS RESTful Web Services: For restful web services.
3. JAX-WS Web Services Endpoints: For SOAP web services.
4. Java Persistence API entities: For accessing underlying data store.
5. Java EE managed beans.

**Question: What is Java Beans?**

- JavaBeans is a technology to write reusable software component. This technology is based on
JavaBeans specification, which provides guidlines to writing code so that it can be used as a
component in other applications.  JavaBeans components are called beans.
- Beans are distributed as jar files.

[Source](https://docs.oracle.com/javase/8/docs/technotes/guides/beans/index.html)

### Java EE Containers

The servers and containers in EE are following-

- Java EE server: The runtime portion of a Java EE product. A Java EE server provides EJB and web containers.
- EJB container: Manages the execution of enterprise beans for Java EE applications. Enterprise beans and their container run on the Java EE server.
- Web container: Manages the execution of web pages, servlets, and some EJB components for Java EE applications. Web components and their container run on the Java EE server.
- Application client container: Manages the execution of application client components. Application clients and their container run on the client.
- Applet container: Manages the execution of applets. Consists of a web browser and a Java Plug-in running on the client together.

[Read more](https://javaee.github.io/tutorial/overview005.html)

### Java EE APIs

- Enterprise JavaBeans Technology
- Java Servlet Technology
- Java ServerFaces Technology
- Java ServerPages Technology
- JavaServer Pages Standard Tag Library
- Java Persistence API
- Java Transactions API
- Java API for RESTful Web Services(JAX-RS)
- Managed Beans
- Contexts and Dependency Injection (CDI)
- Dependency Injection for Java
- Java API for WebSocket

[Read More](https://javaee.github.io/tutorial/overview008.html)

### Java SE API available to Java EE

- JDBC
- JNDI

[Read more](https://javaee.github.io/tutorial/overview009.html)

## Java Servlet Technology

[Source](https://javaee.github.io/tutorial/servlets.html#BNAFD)

Java Servlet is a class which is used to extend the functionality of servers.  Servlets respond to
requests. They are commonly used to extend the applications hosted by web servers. For such
applications servlets defines HTTP specific classes.

### Servlet Lifecycle

[Read here](https://javaee.github.io/tutorial/servlets002.html)

Lifecycle events can be handled by using event listeners.

### Creating and Initializing a Servlet

[Read here](https://javaee.github.io/tutorial/servlets004.html)

### Dealing with Request and Response

[Read here](https://javaee.github.io/tutorial/servlets005.html)

### Filters

A filter is an object that can transform the header and content of a request or response. More
specifically a filter's main tasks are the following-

- Query request/response
- Block request/response from passing any further
- Modify the request/response header and data by providing a customized version of the request and
response object
- Interact with external resource

A filter class is annotated with @WebFilter. We can provide filter configuaration metadata to
specify the routes or url to which the filter applies, to provide a name of the filter, to define
initialization parameter.  These can also be done in the WebXMLDiscriptor.

Java EE provides filtering API in the `javax.servlet` package. There are Filter, FilterChain,
     FilterConfig interfaces to use the filtering functionality.

### Context

- Request context
- Servlet context (Consider the Thread safety)

### Session Configuration

- Session timeout
- Secure
- HTTP only
- Tracking mode

### Listeners

- Context listener
- Session listener

## Java Server Pages (JSP)

JSP page becomes Servlet.

### Directives

- Include directive: <%@ include %>
- Page directive: <%@ page import ="source" %>
