# Code Smell

#### Which code smells?

**Duplication**

- `switch/case` and `if/else` block that examines same set of conditions can be
replaced with polymorphism.
- Modules with similar algorithm can be replaced with _Template Method_ or
_Strategy Pattern_.

**Wrong level of abstraction**

- Abstraction should separate higher level of concepts and lower level of
detailed concepts. The separation must be complete meaning base class should
know nothing about derivative classes. Same thing is true for files, components
and modules. Good software design requires that we separate the concepts at
multiple level and put in different containers.[1](#resources)

- Base class should not depend on derivatives, in general. There are exceptions
to this rule when the number of derivatives are strictly fixed or base class
code selects between derivatives. In those the base class and the derived class
are deployed together in the same jar file. But decoupling this relationship
allows us to deploy independently. [1](#resource)

## Resources

1. [Clean code](https://learning.oreilly.com/library/view/clean-code-a/9780136083238/chapter17.html#ch17lev1sec1)





