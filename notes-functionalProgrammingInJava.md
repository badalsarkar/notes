# Functional Programming in Java



## Functional Languages

- LISP
- Clojure
- Haskell
- ML
- F#

## Why functional programming

- Parallelism

## Java Interfaces New Features

- Static methods
- Default methods

**Interfaces vs Abstract class**

- Interface doesn't have any instance field. Opposite for abstract class.

## Functional Interface

Any interface having a single abstract method. But it can have many static and default methods.

Some functional interfaces are pure. These are intended to be implemented by classes with no
instance field. Pure functional interface respects the main property of functional programming.
Purity is not a property of the interface.

Pure functional interface can be annotated by @FunctionalInterface. Compiler will check single
abstract method property. But compiler can't tell if an interface is pure. Therefore, this
annotation is used to tell that an interface is pure.

In java all pure functional interface are in java.util.function package.

## Lambda Expression

Lambda expression is used to implement functional interface.




