# JavaEE #

## Servlet Life cycle ##

- Parameters
- Attributes
- Every request is allocated a new Thread and runs in parallel.

## JSP ##

JSP pages are translated into servlet files.
Request is an implicit object in JSP. It is available by default.

### JSP Elements ###

- Scriplet
- Expression
- Declaration

### JSP life cycle ###

#### First phase ####

1. Container translate the JSP file into a Servlet file.
2. The servlet file will be compiled into a .class file.
3. Load and instantiate the servlet class.
4. Initializes by calling jspinit().
5. The service method is called \_jspService

The initialization, service and destroy methods comes from the HTTPJspBase
class.

The code written inside the scriplet and expression are put inside the server
method and the code written inside the declaration is put inside the servlet
directly as a method.

### JSP Directives ###

There are total 3 directives.

1. Page
2. Include: allow inclusion JSP resources. Allow component based development.
   Put this directive where you want to add another JSP resource.
3. Taglib

### Implicit Objects in JSP ###

The objects that are available at JSP page by default. One of them is the
request object. Some of the objects are-

1. out
2. request
3. response
4. session
5. config
6. application
7. exception
8. pageContext
9. page

## Session Management ##

Servlet specification provides HTTPSession object. This object is instantiated
for each client. For subsequent request the client provides the session id
either through cookies or url rewriting.

**Cookies** are small pieces of information stored in the browser.

Url rewriting is an alternative method to cookies. It is a fallback option if
the cookies are disabled in the browser.

Session configuration can be placed into the web.xml file.

## Filter ##

Filter is used to do some pre/post-processing on the request/response object.
This is apart from the core business logic which is implemented by the servlets.
An example is the user authentication. A filter is used to authenticate the user
and only allow the authenticated user to go forward in the process. Some other
use cases are logging, response transformation etc.

## Events and Listeners ##

Events occur when the state of an object changes. Events occur in the following
levels -

- Changes in ServletContext object (application level).
- Changes in the HTTPSession object (session level).
- Changes in the HTTPServletRequest object (request level).

### Listener Interface ###

- ServletContextListener
- ServletContextAttributeListener
- HTTPSessionListener
- HTTPSessionAttributeListener
- ServletRequestListener
- HttpSessionBindingListener

## JSP Standard Action ##

JSP code is hard to read and difficult to maintain. Therefore, we can use JSP
Standard Action tag which performs some action when the JSP is executed.

    <jsp: name of tag/>

Some of the tags are-

    <jsp:useBean.../>
    <jsp:forward.../>
    <jsp:include.../>
    <jsp:getProperty.../>
    <jsp:setProperty.../>

## Expression Language(EL) ##

Allows to write simple expression in JSP. The expression is evaluated and the
result is printed in the JSP page.

Some examples:

    ${object.propertyName} //access a property of an object
    ${a / b} //division
    ${a > b} //comparision

### EL Implicit Objects ###

EL implicit objects are generated from the JSP implicit objects. They are in the
form of a Hash Map. 

Some of the objects are-

- requestScope: From HTTTPServletRequest implicit object.
- sessionScope: From HTTPSession implicit object.
- pageScope: From page-scoped attributes.
- applicationScope: From application scoped attributes.
- cookies: From cookies object.
- param: From request parameter.
- header: From request header.
- headerValues
- initParam
- pageContext: Same as JSP pageContext implicit object.

## JSTL (JavaServer Page Standard Tag Library) ##

A bundle of tags. JSTL syntax-

- Core module: <c:name of tag/>
- XML module: <x:name of tag>/
- SQL module: <sql: name of tag/>
- FMT module: <fmt:name of tag/>


