# Clean code notes

## Functions

1. Function should be small

2. Function should do one thing: If a function does only those steps that are one level below the
stated name of the function, then the function is doing one thing.

3. Use one level of abstraction per function

4. Beware of the problems of `switch` statement. Using `switch` statement may violate several design
principals like - single responsibility, open close etc. Use polymorphism instead.

5. Use descriptive name

6. Function arguments:

- The ideal number of arguments is zero( niladic ). Next comes one (monadic)
  followed closely by two
  (dyadic).

  ?? Function arguments takes a lot of computation power??

  - Arguments make it harder to write test cases as you have to write test cases for different
  combination of arguments.

  - **Command query separation**- Functions should either do something or answer something but not
  both. Either your function should change an object or return some information about that object.

  - If a function is transforming an object it should return transformed object instead of taking a
  return argument.

  - Don't pass flag argument to a function. It clearly means that the function is doing more than one
  thing.

  - Function taking two arguments are not evil but try to convert them into moadic function. You can
  use two arguments if there is natural ordering between the arguments.

  - If functions requires more than two or three arguments, it is likely that some of those arguments
  can be wrapped in to their own class.

  - Variable length function arguments can be mondas, dyads or even triads. If the variable arguments
  are all treated identically then they are equivalent to a single argument of type `List`.

  - "Choosing good names for a function can go a long way toward explaining the intent of the
  function, and the order and intent of the arguments. In the case of a monad, the function and
  argument should form a very nice verb/noun pair. For example, `write(name)` is very evocative.
  Whatever this “name” thing is, it is being “written.” An even better name might
  be `writeField(name)`, which tells us that the “name” thing is a “field.”

  This last is an example of the keyword form of a function name. Using this form we encode the
  names of the arguments into the function name. For example, `assertEquals` might be better written
  as
  `assertExpectedEqualsActual(expected, actual)`. This strongly mitigates the problem of having to
  remember the ordering of the arguments."


  7. Side effects: Side effects are those when a function promises to do one thing and also does some
  other things. Side effects causes temporal coupling which means a function can be called only a
  certain times. In that case it must be made clear in the function name.

  8. Anything that makes you to check the declaration of function is a double take. It's a cognitive
  break and should be avoided.

  9. In general avoid output arguments. If a function needs to change the state of something have it
  change the state of its owning object.

  10. Prefer exceptions to returning error codes: if you return error codes from a function, the happy
  path and the error handling code gets mixed, and it becomes ugly. On the other if exception s
  are thrown then the happy path can be separated from error handling code.

  11. Put the error handling in a separate function. If `try` block exists in a function that should
  be the first line and there should be nothing after `catch/finally` block.

  12. When designing a class think about if changing it will require to recompile and redeploy other
  classes.

  13. Avoid using dependency magnet. One example of this is putting different error codes in a single
  class. Many other classes must use those. thus, when this cals/enum changes all those classes
  need to be recompiled a redeployed. If exception was used then new exceptions could be extended
  from existing one. THis is example of open close principal.

  14. As per the rule of structured programming by Edsger Dijkstra every function and every block
  within a function should have one entry a one exit. Following these rules' means that there
  should only be one return statement in a function and no break or continue statements in a loop
  and never any `goto`
  statements. If we keep our functions small then having multiple `return`, `break` or `continue`
  doesn't harm.


## Error Handling

## Testing

  - Write clean test by using helper function.
  - One concept per test.
  - Try to minimize the number of assert per test.
  - Unit tests should be fast
  - Unit test should be independent. One test should not fix the condition for other tests.
  - Unit tests should be repeatble in any environment. They should run in dev, prod, without network.
  - Unit tests must be written before production code.
