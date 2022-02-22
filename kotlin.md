# Kotlin Notes

## Questions

What does it mean when someone says that a programming language is safe?

## Asynchronous programming techniques

[Kotlin doc](https://kotlinlang.org/docs/async-programming.html)

## Coroutines

Coroutine is an instance of suspendable computation. It is conceptually similar
to thread, in the sense that it takes a block of code to run that works
concurrently with the rest of the code. However, a coroutine is not bound to any
particular thread. It may suspend its execution in one thread and resume in
another thread.

[Read more about Coroutine in Wikipedia](https://en.wikipedia.org/wiki/Coroutine)

> Coroutines open the doors to concurrency and actors.
 
- [ ] How does asynchronous or non-blocking programming work?
- [ ] What is the difference between Concurrency vs Asynchronous?  
- [ ] What is Actor?

**Coroutine Scope** 

This is an interface that defines a scope for new coroutines. 
Every coroutine builder like launch, async etc is an extension on
CoroutineScope and inherits its coroutine context to automatically propagate all
its elements and cancellation.

It doesn't complete until all launched children completes.

- [ ] What is structured concurrency?

**Scope builders**: `launch`, `async`, `runBlocking`, `coroutineScope`

- `runBlocking` vs `coroutineScope`: runBlocking and coroutineScope builders may
look similar because they both wait for their body and all its children to
complete. The main difference is that the runBlocking method blocks the current
thread for waiting, while coroutineScope just suspends, releasing the underlying
thread for other usages. Because of that difference, runBlocking is a regular
function and coroutineScope is a suspending function.

- The `launch` coroutine builder returns a `job` object that is a handle to the
launched coroutine.

- The `async` returns a `Deferred` which is a light-weight non-blocking future
that represents a promise to provide a result later. We can use `.await()` on a
deferred value to get its eventual result, but `Deferred` is also a `Job` which
can be cancelled if needed. `await` starts the coroutine and waits for its
completion.

We can use concurrent coroutine using the `async` keyword. Otherwise the
coroutines are sequential in nature. 

**Suspending** **Function**

[Composing suspending functions](https://kotlinlang.org/docs/composing-suspending-functions.html)

## Asynchronous Flow

When we want to return multiple asynchronously computed value we can use `Flow`.
If we use a collection like `List`, we will return all the value together. But
if we want to return like stream, we need to use `Flow`.

[Kotlin doc](https://kotlinlang.org/docs/flow.html#flows-are-cold)

Flows are cold streams which means the code inside the `flow` block doesn't run
until the flow is collected. The flow can be collected using the `.collect()`
method. Every time the `collect()` method is called the code in the `flow`
block runs.

#### Flow Cancellation

[Kotlin Doc](https://kotlinlang.org/docs/flow.html#flow-cancellation-basics)

[Intermediate flow operator:](https://kotlinlang.org/docs/flow.html#intermediate-flow-operators)
These operators are used to transform the flow.

[Terminal flow operators](https://kotlinlang.org/docs/flow.html#terminal-flow-operatorsa)
Terminal operators on flows are suspending functions that start a collection of
the flow. The `collect` is the most basic one. Other terminal operators are
`toList`, `toSet`. There are operators to get the first value(`first`) and to ensure that
a flow emits a single value (`single`).

[Flows are sequential.](https://kotlinlang.org/docs/flow.html#flows-are-sequential)

#### Flow Buffering

Normally
[`Flows`](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow/index.html)
are sequential. It means that the code of all operators is executed in the same
coroutine. The `buffer` operator creates a separate coroutine during execution
for the flow it applies to.

#### Conflation

#### Composing multiple flows

#### Flattening flows

#### [Flow exceptions](https://kotlinlang.org/docs/flow.html#flow-exceptions)

Collector `try-catch` block: Wrap the flow collection with a `try-catch` block.

## Inline function

- [First class function](https://en.wikipedia.org/wiki/First-class_function)
- [Higher order function](https://en.wikipedia.org/wiki/Higher-order_function)

[Read about Lambda](https://martinfowler.com/bliki/Lambda.html)
Lambda is also known Closures, Anonymous function, or Blocks.

## Resources

1. Kotlin in action by Dmitry Jemerov and Svetlana Isakova [https://learning.oreilly.com/library/view/kotlin-in-action/9781617293290/](https://learning.oreilly.com/library/view/kotlin-in-action/9781617293290/)


