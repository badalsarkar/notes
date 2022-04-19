# Uniform Resorce Identifier (URI)

- Each URI begins with a scheme name

some examples: 

```
 ftp://ftp.is.co.za/rfc/rfc1808.txt

 http://www.ietf.org/rfc/rfc2396.txt

 ldap://[2001:db8::7]/c=GB?objectClass?one

 mailto:John.Doe@example.com

 news:comp.infosystems.www.servers.unix

 tel:+1-816-555-1212

 telnet://192.0.2.16:80/

 urn:oasis:names:specification:docbook:dtd:xml:4.1.2
```

- A URI can be further classified as a locator, a name, or both.  The
   term "Uniform Resource Locator" (URL) refers to the subset of URIs
   that, in addition to identifying a resource, provide a means of
   locating the resource by describing its primary access mechanism
   (e.g., its network "location").  The term "Uniform Resource Name"
   (URN) has been used historically to refer to both URIs under the
   "urn" scheme [RFC2141], which are required to remain globally unique
   and persistent even when the resource ceases to exist or becomes
   unavailable, and to any other URI with the properties of a name.
   
   ## Sources
   
   1. [RFC 3986](https://datatracker.ietf.org/doc/html/rfc3986)
