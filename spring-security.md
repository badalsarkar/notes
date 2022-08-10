---
	mindmap-plugin: basic
---

# spring security (ss)

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

## how it works?
- uses Servlet Filter technology
- FilterChainProxy
   - a servlet filter
   - entry point for all web based security
   - combines numerous filters
      - each filter does its own task