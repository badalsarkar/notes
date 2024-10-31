---
mindmap-plugin: basic
---

# authentication-authorization

## OAuth

- What?
  - Protocol
- used by
  - OpenID Connect (OIDC)
    - what
      - Identity layer
        - functions
          - authentication done by Authorization server
          - verifies identity of end user
          - obtain basic profile information about end user
            in REST like manner
          - receive information about authenticated sessions
            and end users
      - extenstion to OAuth2
      - Only focused on Authentication
      - introduces
        - JWT
        - standard endpoints
          - /login, /token/, /userinfo
        - standard scopes
          - openid, profile, email
        - ID token
          - it only identifies who a person is not access
        - single logout
    - clients
      - Web client
      - mobile
      - Javascript
    - implementations
      - certified implementations
        - PingFederate
        - and many more (https://openid.net/developers/certified/ )
    - provider
      - provides
        - stores user credential
        - Manage login security
        - manages user registration
        - manages integration with LDAP/ SAML
        - manages password reset process
        - implements 2 factor authentication
        - SSO (Single Sign On)
          - integrated through
            - cloud company
              - Google
              - Github
              - Facebook
              - Apple
            - corporate login
              - Okta
              - AuthO
              - Any OpenID Connect Certified provider
              - PingFederate
    - flows
      - Authorization Code
        - similar to OAuth2 Authorization Code flow
        - This enables SSO
        - The client gets back an ID token
      - Hybrid flow
        - returns both ID token and access token
- specification
  - Roles
    - Resource owner
    - Resource Server
    - Authorization Server
    - Client/ Application
  - Tokens
    - Access Token
      - Bearer Token
        - whoever have the token owns the token
      - JWT Token
      - Opaque Token
    - Refresh Token
  - Scopes
    - what
      - what is allowed to do
      - A permitted authority or action
      - usually "." separated example calendar.readonly
    - how is it applied
  - Grant types
    - Client Credentials
      - Simplest flow
      - Service to service communication
      - The client has to be trusted
      - how it works?
        - each client has id and secret
        - id & secret used to retrieve access token
    - Authorization Code
      - Browser based login
      - for SPAs
      - Confidential
      - Secure
      - Makes heavy use of browser ridirects and back channels
      - User typically approves the scopes to the client
      - [flow](https://www.rfc-editor.org/rfc/rfc6749#section-4.1)
        - 1. Client initiate authentication by redirecting the user-agent to authz server auth endpoint
        - 2. Auth server completes the auth and permission
        - 3. Auth server re-direct user agent to the re-direct url provided by client and send auth token
        - 4. Client send request to auth server access token endpoint with the auth toke from previous step
        - 5. Auth server authenticate client and provide access token
    - Device code
      - Televisions and env with limited input capability
    - Refresh
      - obtain new token when one expires
    - Password
      - less secure
      - for CLI, SPAs
      - how it works?
        - User provide credentials to client
        - client use the credential to retrive access token from authorization server
        - user must trust the client absolutely
    - Implicit
      - similar to Authorization Code flow
    - Sub title

## LDAP Authentication

Read about LDAP [here](./ldap.md)

## Entra ID

## [[spring-security]] Spring security

- Built in OAuth Support
  - Recommended for new app
- Spring Security OAuth
- integrations
  - login
    - SSO
  - client
    - access OAuth2 protected resources
  - resource server

