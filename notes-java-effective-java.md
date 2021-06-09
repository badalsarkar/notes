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



