# OAuth (Open Authorization)

## How does OAuth 2.0 work?

_source: (https://auth0.com/intro-to-iam/what-is-oauth-2/)_

At the most basic level, before OAuth 2.0 can be used, the Client must acquire
its own credentials, a client id and client secret, from the Authorization
Server in order to identify and authenticate itself when requesting an Access
Token.

Using OAuth 2.0, access requests are initiated by the Client, e.g., a mobile
app, website, smart TV app, desktop application, etc. The token request,
exchange, and response follow this general flow:

1. The Client requests authorization (authorization request) from the Authorization
   server, supplying the client id and secret to as identification; it also
   provides the scopes and an endpoint URI (redirect URI) to send the Access Token
   or the Authorization Code to.

2. The Authorization server authenticates the Client and verifies that the
   requested scopes are permitted.

3. The Resource owner interacts with the Authorization server to grant access.

4. The Authorization server redirects back to the Client with either an
   Authorization Code or Access Token, depending on the grant type, as it will be
   explained in the next section. A Refresh Token may also be returned.

5. With the Access Token, the Client requests access to the resource from the
   Resource server.

## Grant types in OAuth 2.0

_source: (https://auth0.com/intro-to-iam/what-is-oauth-2/)_

1. Authorization Code grant: The Authorization server returns a single-use
   Authorization Code to the Client, which is then exchanged for an Access
   Token. This is the best option for traditional web apps where the exchange
   can securely happen on the server side. The Authorization Code flow might be
   used by Single Page Apps (SPA) and mobile/native apps. However, here, the
   client secret cannot be stored securely, and so authentication, during the
   exchange, is limited to the use of client id alone. A better alternative is
   the Authorization Code with PKCE grant, below.

2. Implicit Grant: A simplified flow where the Access Token is returned directly
   to the Client. In the Implicit flow, the authorization server may return the
   Access Token as a parameter in the callback URI or as a response to a form
   post. The first option is now deprecated due to potential token leakage.

3. Authorization Code Grant with Proof Key for Code Exchange (PKCE): This authorization flow is similar to the Authorization Code grant, but with additional steps that make it more secure for mobile/native apps and SPAs.

4. Resource Owner Credentials Grant Type: This grant requires the Client first
   to acquire the resource owner’s credentials, which are passed to the
   Authorization server. It is, therefore, limited to Clients that are
   completely trusted. It has the advantage that no redirect to the
   Authorization server is involved, so it is applicable in the use cases where
   a redirect is infeasible.

5. Client Credentials Grant Type: Used for non-interactive applications e.g.,
   automated processes, microservices, etc. In this case, the application is
   authenticated per se by using its client id and secret.

6. Device Authorization Flow: A grant that enables use by apps on
   input-constrained devices, such as smart TVs.

7. Refresh Token Grant: The flow that involves the exchange of a Refresh Token
   for a new Access Token.
