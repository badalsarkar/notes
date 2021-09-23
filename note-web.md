# WEB NOTES

## CORS (Cros Origin Resource Sharing)

<https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS>

## Web Services vs Web Application

Web service: a client can be any device that run a HTTP client. The server serves JSON/xml data
Web apps: a cilent is a browser and the server serves html page

## Constraints for Rest web services

- Stateless: The server doesn't hold any information about the client state.

- Client server: The client and server act independently. The server does not
send any information without a request from the client.  

- Cacheable: Many clients often request the same resources; therefore, it is
useful to cache responses in order to improve performance.

- Uniform interface: Requests from different clients look the same. Clients may
include, for example, a browser, a Java application, and a mobile application.
Layered system: REST allows us to use a layered system architecture.
Code on demand: This is an optional constraint.




## Technical Jargons

These are some of the technical words used-
    - Resource: It is a digital asset identified by URI. The URI standard is described [here](https://tools.ietf.org/html/rfc3986#section-1.1).
    - Representation: A representation is a digital asset that is formatted as a specific inter media type.
    - Internet media type: It is a data format for a representation of a resource on the internet. It is defined and
     published by IANA (https://www.iana.org/assignments/media-types/media-types.xhtml).
    - JSON: It is data interchange format. <https://www.json.org/json-en.html>
    - State, data: The state of the data
    - State, interaction: The state of the interaction among programs in a distributed system. The server does not keep 
     track of this state. It is the responsibility of the client. 
    - REST: Roy Fielding paper <https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm>


## JQuery

Add jquery to your project- add the following files<br /> 

```javascript
CSS<br />
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
```

```javascript
Javascript- Jquery<br />
<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha256-pasqAKBDmFT4eHoN2ndd6lN370kFiGUFyTiUHWhU7k8=" crossorigin="anonymous"></script>
```

```javascript
Javascript- Bootstrap<br />
<script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
```

- all jquery code goes inside $() 
- $ is shortcut for "jQuery(function())

## Resources:

Description   |   Link   |
:----------|:----
Jquery plugin registry |<https://plugins.jquery.com/> 
Web technologies |something else 
