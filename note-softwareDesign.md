# Software Design

# Table of Contents

- [Software Design](#software-design)
- [Table of Contents](#table-of-contents)
  - [Modeling with UML](#modeling-with-uml)
    - [Types of Models](#types-of-models)
    - [Types of Model is Software Development](#types-of-model-is-software-development)
    - [Types of UML Models](#types-of-uml-models)
    - [CASE Tools](#case-tools)
  - [Use Case Diagram](#use-case-diagram)
    - [Key Elements](#key-elements)
      - [Use Cases](#use-cases)
      - [Systems](#systems)
      - [Actors](#actors)
      - [Associations](#associations)
        - [Between actor and use case](#between-actor-and-use-case)
        - [Between use cases](#between-use-cases)
        - [Between actors](#between-actors)
  - [Activity Diagram](#activity-diagram)
  - [Class Diagram](#class-diagram)
    - [Key Elements of Class Diagram](#key-elements-of-class-diagram)
    - [Classifiers](#classifiers)
    - [Features](#features)
    - [Relationships](#relationships)
      - [Association Link](#association-link)

## Modeling with UML

UML is a family of graphical notations to describe and design software systems,
especially those using an object oriented approach.

The notations and their meaning is defined by a computer industry standard
consortium named Object Management Group(OMG).

There are 13 types of UML model. The most recent version is 2.5.

[UML Diagram Type](https://creately.com/blog/diagrams/uml-diagram-types-examples/)

### Types of Models

- Computational
- Analytical
- Nonanalytical/Descriptive: Describe components and their relationship in
system.

### Types of Model is Software Development

The non-analytical models can be divided into two groups-

- One that model data, entity relationship model
- The other that model the application that works on data, UML. UML uses the
data but the focus is on modeling the application logic and structure of how the
application uses the data. There are other diagram types like UML. SysML and
BPMN models. SysML is more general purpose. BPMN focuses on business process ans
workflows.

### Types of UML Models

UML notations are categorized into three diagram types.

- Structural: Models the structure of the system.
- Behavior: Models the behaviour of the system.
- Interaction: Models the interaction between the components of the system and
external systems.

### CASE Tools

- Open source
  - Visual Paradigm
  - PlantUML

## Use Case Diagram

Shows overall functionality of a system at a very high level. This a summary of
all use cases that have been identified.

### Key Elements

#### Use Cases

#### Systems

#### Actors

An external entity.

- Primary: Who triggers the use case
- Secondary: Who is involved in the use case. It can often be an external
system.

#### Associations

##### Between actor and use case

The primary actor on the left side of the use case. The arrow notations can also
be used. If the arrow goes away from actor, that means the actor is primary.

##### Between use cases

- Include
- Extend
- Generalization

##### Between actors

## Activity Diagram

Used for workflow and process modeling.

## Class Diagram

Models the type of objects and relationships among them.

### Key Elements of Class Diagram

- Classifiers: Any one of the six class-
  - Concrete class
  - Abstract class
  - Interface
  - Enumeration
  - Generic class
  - Active class
- Features: Structural and behavioral(methods)
- Relationships: Associations, Generalization, Dependency

### Classifiers

### Features

### Relationships

- Associations
  - Association Link
  - Association class
    - Aggregation
    - Composition
- Generalization
- Dependency

#### Association Link

When one class (source) uses an instance of other class(target). The source will
have reference to some attribute of the target. There are multiplicity of
relationship. Multiplicity tells given the source, how many target is associated
with it. Again, given the target, how many source is associated with it.

- \* means 0 or more
- 1...\* means one or more
- 1 means exactly one
- m...n means m and m


