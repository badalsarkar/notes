# Spring Security

Spring Security is a framework that provides authentication, authorization, and protection against
common attacks. With first class support for both imperative and reactive applications.

## Features

- Authentication
- Authorization
- Protection against common exploits

### OAuth 2.0 Login

_source (https://docs.spring.io/spring-security/site/docs/current/reference/html5/#webflux-oauth2-login)_

> The OAuth 2.0 Login feature provides an application with the capability to have users log in to the
application by using their existing account at an OAuth 2.0 Provider (e.g. GitHub) or OpenID Connect
1.0 Provider (such as Google). OAuth 2.0 Login implements the use cases: "Login with Google" or
"Login with GitHub".

*OAuth 2.0 login is implemented by using the [Authorization Code Grant](https://datatracker.ietf.org/doc/html/rfc6749#section-4.1)*

### Steps to setup OAuth login in Spring

Step 1: Obtain OAuth 2.0 credentials from authentication provider

Step 2: Set the redirect URI. The redirect URI is the path in the application that the end use's
agent is redirected back to after they have been authenticated.

The default redirect URI template in Spring security is
`{baseurl}/login/oauth2/code/{registrationId}`. The `registrationId` is a unique identifier for
`ClientRegistration`. [Read about ClientRegistration](https://docs.spring.io/spring-security/site/docs/current/reference/html5/#oauth2Client-client-registration).

Step 3: At this point we have a OAuth client registered with a provider. Now we need to [configure
our
application](https://docs.spring.io/spring-security/site/docs/current/reference/html5/#webflux-oauth2-login-sample-config)
to use the client for a [specific flow](https://auth0.com/docs/authorization/flows).

At this point running the application will initiate authorization using OAuth.

Spring security provides necessary defaults for OAuth Authorization Provider's configuration for
well known provides e.g. Google. For not well known providers or own providers that supports [OpenID
Provider Configuration](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig)
or [Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414#section-3), the
OpenID Provider Response's `issuer-uri` can be used to configure the application like below-


```yaml
spring:
  security:
    oauth2:
      client:
        provider:
          keycloak:
            issuer-uri: https://idp.example.com/auth/realms/demo
        registration:
          keycloak:
            client-id: spring-security
            client-secret: 6cea952f-10d0-4d00-ac79-cc865820dc2c
```

The `issuer-uri` instructs Spring Security to query in series the endpoints to discover the
configuration.

Note: In the above example the `client-id` and `client-secret` are linked to provider as `keycloak`
has been used for both.

#### Explicit OAuth login configuration

```java

@Bean
ReactiveClientRegistrationRepository clientRegistrations() {
    ClientRegistration clientRegistration = ClientRegistrations
            .fromIssuerLocation("https://idp.example.com/auth/realms/demo")
            .clientId("spring-security")
            .clientSecret("6cea952f-10d0-4d00-ac79-cc865820dc2c")
            .build();
    return new InMemoryReactiveClientRegistrationRepository(clientRegistration);
}

@Bean
SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
    http
        // ...
        .oauth2Login(withDefaults());
    return http.build();
}

```

`InMemoryReactiveClientRegistrationRepository` implements `ClientRegistrationRepository` which
serves as a repository for OAuth 2.0/ OpenID Connect 1.0 `ClientRegistration`s. 

Client registration information is ultimately stored and owned by the associated Authorization
Server. This repository provides the ability to retrieve a sub-set of the primary client
registration information, which is stored with the Authorization Server.

Spring Boot 2.x auto-configuration binds each of the properties under
`spring.security.oauth2.client.registration.[registrationId]` to an instance of `ClientRegistration` and
then composes each of the `ClientRegistration` instance(s) within a `ClientRegistrationRepository`.

The default implementation of `ClientRegistrationRepository` is `InMemoryClientRegistrationRepository`.

## 5 Important concepts

1. Authentication
2. Authorization
3. Principal: The authenticated user. App remembers the principals.
4. Granted authority: The allowed actions for an user. 
5. Roles: Grouping of permissions

## Resources

- [YouTube Video- Laurentiu Spilca](https://www.youtube.com/watch?v=Of4HFbsPKqk&list=PLEocw3gLFc8XRaRBZkhBEZ_R3tmvfkWZz)
