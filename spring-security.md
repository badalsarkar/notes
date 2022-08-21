---
	mindmap-plugin: basic
---

# spring security (ss)

## usage
- servlet application
   - Sub title
   - how it works?
      - uses Servlet Filter technology
      - [FilterChainProxy](https://docs.spring.io/spring-security/reference/servlet/architecture.html#servlet-filterchainproxy)
         - what?
            - a servlet filter
            - entry point for all web based security
            - combines numerous security filters
         - delegate to
            - [SecurityFilterChain](https://docs.spring.io/spring-security/reference/servlet/architecture.html#servlet-securityfilterchain)
               - what?
                  - chain of
                     - SecurityFilters
                        - what?
                           - spring bean
                  - the [order of filters](https://docs.spring.io/spring-security/reference/servlet/architecture.html#servlet-filters-review) matters
                  - [order of Spring Security filters](https://docs.spring.io/spring-security/reference/servlet/architecture.html#servlet-security-filters)
               - how many?
                  - [more than 1 in an application](https://docs.spring.io/spring-security/reference/servlet/architecture.html#servlet-multi-securityfilterchain-figure)
                     - allows
                        - different security config for different pieces of app
                  - only 1 is used
               - references
                  - [api](https://docs.spring.io/spring-security/site/docs/5.7.2/api/org/springframework/security/web/SecurityFilterChain.html)
                  - [code](https://github.com/spring-projects/spring-security/blob/main/web/src/main/java/org/springframework/security/web/SecurityFilterChain.java)
         - [decides which SecurityFilterChain to use](https://docs.spring.io/spring-security/reference/servlet/architecture.html#servlet-multi-securityfilterchain-figure)
         - references
            - [api](https://docs.spring.io/spring-security/site/docs/3.2.8.RELEASE/apidocs/org/springframework/security/web/FilterChainProxy.html)
            - [code](https://github.com/spring-projects/spring-security/blob/main/web/src/main/java/org/springframework/security/web/FilterChainProxy.java)
      - [exception](https://docs.spring.io/spring-security/reference/servlet/architecture.html#servlet-exceptiontranslationfilter)
- reactive application
   - authentication
   - [[authentication-authorization#OAuth | OAuth 2.0]] Log In
      - allows user to login using their existing account at an
         - OAuth 2.0 provider
         - OpenID Connect 1.0 provider
      - implemented using Authorization Code Grant in
         - [OAuth 2.0](https://www.rfc-editor.org/rfc/rfc6749#section-4.1)
         - [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html#CodeFlowAuth)
      - Sub title
      - Sub title

## features
- authentication
   - default implementation
      - default login
      - default logout
      - default AuthenticationProvider impl
   - custom implementation
      - implement
         - UserDetailsService
            - if access to credential
         - AuthenticationProvider
            - if no access to credential
- authorization
- protection against common attacks