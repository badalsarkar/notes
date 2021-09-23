# Effective Java Notes

## Creating and destroying objects

#### Item 1: Consider static factory methods

Pros:

1.  A third advantage of static factory methods is that, unlike constructors,
    they can return an object of any subtype of their return type. This gives
    you great flexibility in choosing the class of the returned object.

2.  A fourth advantage of static factories is that the class of the returned
    object can vary from call to call as a function of the input parameters. Any
    subtype of the declared return type is permissible. The class of the
    returned object can also vary from release to release.

3. It provides the basis for **Service Provider Framework**.

> Service Provider Framework decouples the client from implementations. There
> are mainly three components to SPF. **Service Interface** which represents the
> implementations. **Provider Registration API** which is used by providers to
> register implementations. **Service Access API** which is used by the client
> to get an instance of the **Service Interface**.

Cons:

1. Class without `public` or `protected` constructors can't be sub-classed.
2. They are hard to identify in the API documentation

Follow the below naming conventions for static factory methods-

- from—A type-conversion method that takes a single parameter and returns a
corresponding instance of this type, for example:

`Date d = Date.from(instant);`

- of—An aggregation method that takes multiple parameters and returns an
instance of this type that incorporates them, for example:

`Set<Rank> faceCards = EnumSet.of(JACK, QUEEN, KING);`

- valueOf—A more verbose alternative to from and of, for example:

`BigInteger prime = BigInteger.valueOf(Integer.MAX_VALUE);`

- instance or getInstance—Returns an instance that is described by its
parameters (if any) but cannot be said to have the same value, for example:

`StackWalker luke = StackWalker.getInstance(options);`

- create or newInstance—Like instance or getInstance, except that the method
guarantees that each call returns a new instance, for example:

`Object newArray = Array.newInstance(classObject, arrayLen);`

- getType—Like getInstance, but used if the factory method is in a different
class. Type is the type of object returned by the factory method, for example:

`FileStore fs = Files.getFileStore(path);`

- newType—Like newInstance, but used if the factory method is in a different
class. Type is the type of object returned by the factory method, for example:

`BufferedReader br = Files.newBufferedReader(path);`

- type—A concise alternative to getType and newType, for example:

`List<Complaint> litany = Collections.list(legacyLitany);`


## Exceptions

#### Use exceptions only for exceptional conditions

#### Use checked exceptions for recoverable conditions and runtime exceptions for programming error

Use checked exceptions for recoverable conditions and unchecked exceptions for
non-recoverable conditions. When in doubt use unchecked exceptions. Don't define
throwable that are neither checked exceptions nor runtime exceptions.  Provide
methods for your checked exceptions to aid recovery.

#### [Avoid use unnecessary use of checked exceptions](https://learning.oreilly.com/library/view/effective-java/9780134686097/ch10.xhtml#lev71)

In summary, when used sparingly, checked exceptions can increase the reliability
of programs; when overused, they make APIs painful to use. If callers won’t be
able to recover from failures, throw unchecked exceptions. If recovery may be
possible and you want to force callers to handle exceptional conditions, first
consider returning an optional. Only if this would provide insufficient
information in the case of failure should you throw a checked exception.

#### [Favor use of standard exceptions](https://learning.oreilly.com/library/view/effective-java/9780134686097/ch10.xhtml#lev72)

Re-using the standard exceptions provided by Java is also code re-use which is a
good thing. Don't reuse Exception, RuntimeException, Throwable, or Error
directly. Because you can't reliably test these exceptions as they are
superclass of other classes.

Use the following table for common re-use cases-

![Reuse exceptions (Source: Effective Java)](./images/exception-reuse.png "Reuse exception (Source: Effective Java)")

#### Throw exception appropriate to the abstraction

Never throw lower level exception in higher level of exception unless they are
appropriate.







