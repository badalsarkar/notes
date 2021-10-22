# API Development Note

## Resource oriented API

[book](https://learning.oreilly.com/library/view/api-design-patterns/9781617295850/OEBPS/Text/01.htm#heading_id_5a)

- Stateful API: An API is stateful if it stores the state and uses it in
subsequent requests.
- Stateless API: An API is called stateless when it can be made independently
from all other API request.

RPC style API are good for stateless functionality.


## What are API design?

An example API design pattern might specify that a certain RPC can be eventually
consistent.

An API is rigid and difficult to change, therefore, design pattern is important.

## Design Principles

### Naming

Source: https://learning.oreilly.com/library/view/api-design-patterns/9781617295850/OEBPS/Text/03.htm#heading_id_3

1. Expressive: Clearly convey the thing it is naming.
2. Simple
3. Predictable: The basic underlying goal is to allow users of an API to learn
   one name and continue building on that knowledge to be able to predict what
   future names (e.g., if they represent the same concept) would look like. By
   using topic consistently throughout an API when we mean “the topic for a
   given message” (and something else when we mean something different), we’re
   allowing users of an API to build on what they’ve already learned rather than
   confusing them and forcing them to research every single name to ensure it
   means what they would assume.


## Anatomy of API design

## Pagination pattern






