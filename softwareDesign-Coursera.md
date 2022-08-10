# Introduction to Software Design and Architecture

## Object Oriented Modeling

1. Conceptual Designs
2. Technical Designs

## User Stories

Use this format

*As a -------------, I want to ------------- so that --------------.*\n
      Actor                   Goal of actor          Why the actor wants this goal?

After filling the user stories you can apply object-oriented thinking to discover objects.

Example: *As an **online shopper**, I want to **add** an **item** to my **shopping cart**, so that I can
**purchase** it.*

Here the nouns are object and the verbs are the responsibilities of objects. Verbs can also identify
connections between objects.

User stories also shows connections between objects. In the above example, an user is associated
with one shopping cart and the shopping cart should be capable of holding multiple items.

## Categories of Objects in Designs

When we breakdown components into smaller objects, we will mostly find three types of objects. They
are-

- Entity Objects: These objects are real world thing. They know the attributes about themselves. For
example- a person, a building etc
- Boundary Objects: Object that sits at the boundary of the system to communicate with other
systems. Any object that deals with another system- a user, another software system, the internet-
can be considered boundary object.
- Control object: When we breakdown a large object, we will get many smaller objects. In that
scenario, we will find it useful to have an object that controls other objects. One example is the
Mediator object which coordinates the activities of many different objects so that they can stay
loosely coupled.

## Requirements

- Functional
- Non-Functional: How well does the software perform
- Reusability
- Flexibility
- Maintainability

There is a common trade off between maintainability and performance, security and performance.

## Class Responsibility Collaborator

Represents candidate components, their responsibilities and connections. This will help identify the
objects, and the overall design.

## Programming Language Evolution

## OOP Design Principals

### Abstraction

- Hides the complexity
- Related to a context
- The properties will be determined by the context

### Encapsulation

- Bundle data and function
- Expose some methods and interface
- Restricts access to some data fields

### Decomposition

- Breaking the problem into smaller pieces
- Identifying the fixed parts and dynamic parts of an object
- The lifetime of parts can be whole or part
- Parts can be shared among the other parts
- These will determine the relationship between classes

### Generalization

- Reduce the redundant code
- We can generalize common behaviour
- Generalization through class is inheritance
- It is the DRY principal

## Technical Design Steps

- Gather requirement
- Class Diagram
- Encapsulation
- Decomposition
  - Association
  - Aggregation
  - Composition
- Generalization with interface. Interface allows polymorphism

## Design Principals

- Lose coupling
- Strong cohesion
- Separation of concern
- Information hidding
- Conceptual integrity: Building software in a consistent manner. A set of rules aggreed upon and
followed by team members. Code reviews helps to identify the bugs and ensures conformance with the
standard.
