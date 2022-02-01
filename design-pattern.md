# Software Design Pattern

- Class is the implementation of an Object and Interface is the type of an
object
- Class inheritance vs Type(Interface) inheritance
- Program to interface not implementation
- Don't declare variable to be instance of a concrete class. Instead commit only
to an interface defined by abstract class
- Implementation dependency is bad 
- Favor composition over inheritance

> "Class inheritance has some problems. First, you can't change the imple-
> mentations inherited from parent classes at run-time, because inheritance is
> defined at compile-time. Second, and generally worse, parent classes often
> define at least part of their subclasses' physical representation. Because
> inheritance exposes a subclass to details of its parent's implementation, it's
> often said that "inheritance breaks encap- sulation" [Sny86]. The
> implementation of a subclass becomes so bound up with the implementation of
> its parent class that any change in the parent's implementation will force the
> subclass to change.  Implementation dependencies can cause problems when
> you're trying to reuse a sub- class. Should any aspect of the inherited
> implementation not be appropriate for new problem domains, the parent class
> must be rewritten or replaced by something more appropriate. This dependency
> limits flexibility and ultimately re-usability. One cure for this is to inherit
> only from abstract classes, since they usually provide little or no
> implementation.
> Object composition is defined dynamically at run-time through objects
> acquiring references to other objects. Composition requires objects to respect
> each others' interfaces, which in turn requires carefully designed interfaces
> that don't stop you from using one object with many others. But there is a
> payoff. Because objects are accessed solely through their interfaces, we don't
> break encapsulation. Any object can be replaced at run-time by another as long
> as it has the same type. Moreover, because an object's implementation will
> be written in terms of object interfaces, there are substantially fewer
> implementation dependencies.  Object composition has another effect on system
> design. Favoring object composition over class inheritance helps you keep each
> class encapsulated and focused on one task.  Your classes and class
> hierarchies will remain small and will be less likely to grow into
> unmanageable monsters. On the other hand, a design based on object composition
> will have more objects (if fewer classes), and the system's behavior will
> depend on their interrelationships instead of being defined in one class."

- Delegation is a way of making composition as powerful as inheritance. Two
objects are responsible for processing a request where one object delegates part
of the work to another object. In case of inheritance the subclass can refer to
the parent class with `this` keyword whereas in delegation, the receiver passes
itself to the delegate.

- Delegation has disadvantage it shares with other techniques that makes
software more flexible using composition- Dynamic software, highly parameterized
software is harder to understand than more static software.

- Parameterized types (Generics) is also a way to reuse code.
- Understanding run-time structure and compile-time structure of code is
important. Design pattern helps to understand that. 

- The hard part about object-oriented design is decomposing a system into
objects.The task is difficult because many factors come into play: encapsulation,
  granularity,dependency, flexibility, performance, evolution, re-usability, and
  on and on. They all influence the decomposition, often in conflicting ways

- When a request is sent to an object, the particular operation that is performed depends on
both the request and the receiving object. Different objects that support identical requests
may have different implementations of the operations that fulfill these requests. The
run-time association of a request to an object and one of its operations is known as
dynamic binding.

## 
