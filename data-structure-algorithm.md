# ALGORITHM AND DATA STRUCTURE

## Data Structure

### Stacks and Queues

#### Stacks

The items are inserted at the top. The last inserted item is accessed first.
Most microprocessor architecture uses a stack-based architecture. The pushing
and popping of item happens in O(1) times.

#### Queues

Last in last out. The last item inserted will be accessed last. Queues are
implemented in a circular arrangement. Insertion and removal of item is constant
time O(1).

Queues are most often used in breadth-first search or implementing cache.

#### Dqueue

Double ended queue. Items can be inserted at both end and removed from both end.
Dqueue can be implemented to restrict insertion at left and removal from right
or insertion at right and removal from left. By this, a dqueue works both as a
stack and queue. However, it is not used as widely as stack and queue.

#### Priority Queue

The queue items are prioritized. The top most prioritized item is removed first.
The prioritization can be implemented at the time of insertion or removal. If it
is implemented at insertion time, existing items are shifted to make room for
the to be inserted item. If prioritization is implemented at removal time, the
array is searched for the top priority item.

The time complexity of insertion is O(N), given the prioritization is
implemented at insertion time and the time complexity of removal is O(1).

### Hash Table

### Recursion and Dynamic Programming

1. The condition that leads to a recursive method returning without making
another recursive call is referred to as the base case. It’s critical that every
recursive method have a base case to prevent infinite recursion and the
consequent demise of the program.

Recursion has some overhead as this makes many function call. Another problem is
that memory is used to store all the intermediate arguments and return values.

## Algorithm

### Basic Concepts

#### Logarithm in CS

More specifically, it answers the question "how many one number we need to get
other number".

[Read about log](https://www.mathsisfun.com/algebra/logarithms.html)

#### Order of Growth

What is order of growth?

Order of growth is a mechanism to express the change in time taken to perform a
task with the change in input size. For example O(N) states that the time is in
proportional to input size (N). If the input size doubles, it will take double
time.

#### Asymptotic Analysis

[Read
here](https://www.geeksforgeeks.org/analysis-of-algorithms-set-4-analysis-of-loops/?ref=lbp)

In Asymptotic analysis we measure the performance of an algorithm by observing
how the time and space increases with the increase in the input size.

There are three cases to analyze- worst case, average, and best case. Worst case
analysis tells how much time the algorithm takes at the worst scenario. This
analysis is done most of the time. The average case takes into consideration the
average time taken and the best case finds the time taken at best scenario.

The Big O notation does the worst case analysis.

#### Big O notation

Tells how efficient a computer program is. Answers how an algorithm's speed is
related to the number of elements.

#### Drop the constant in Big O

Why do we drop the constant in the Big O notation?

Big O doesn't tell how long an algorithm takes to run but it tells how the
runtime of an algorithm will increase with the increase in the input.  Consider
the below code:

```java
//Min and Max 1 MinandMax2 
int min = Integer.MAX_VALUE; 
int max = Integer.MIN_VALUE; 
for (int x : array) { 
  if (x < min) min = X; 
  if (x > max) max = X; 
}

//Min and Max 2 
int min = Integer.MAX_VALUE; 
int max = Integer.MIN_VALUE;
for (int x : array) { 
  if (x > max) max = X;
} 
for (int x : array) {
  if (x < min) min = X;
}
```

Which one is faster? The first one does one for loop and the other one does two
for loops. But then, the first solution has two lines of code per for loop
rather than one.  

If you're going to count the number of instructions, then you'd have to go to
the assembly level and take into account that multiplication requires more
instructions than addition, how the compiler would optimize something, and all
sorts of other details.

This would be horrendously complicated, so don't even start going down this
road. Big 0 allows us to express how the runtime scales. We just need to accept
that it doesn't mean that 0 (N) is always better than O(N^2).

#### Drop the non-dominant term

![Drop Non dominant constant](./images/dropNonDominant.png "Drop Non-dominant
    constant")

#### Multi-part algorithm: Add vs Multiply

![Multipart Algorithm](./images/multipartAlgo.png "Multipart Algorithm")

#### Amortized Time

Need to read it again.

An example of when to use amortized time: An arraylist is a data structure that
increases the size of the array when the array becomes full. The new array takes
twice as much elements. So, all the items are copied over from the old array to
the new array. This process affects the runtime of insertion of new item into
the array. The insertion is a constant time operation when the array is not
full. When the array is full, the insertion takes longer because of the copy
operation needed to be done. In that case it takes O(N) time to insert an
element. So, how do we represent the runtime of this insertion? That is where
the concept of amortized time comes into play.

#### Log N runtimes

In a nutshell, when the problem space (e.g. array size) becomes half in each
iteration, the runtime will likely be O(log N).

#### Recursive Runtime

If a recursive function makes only one function to itself, it may take O(N)
  time. But if the recursive fuction makes multiple recursive call, the runtime
  will be O(branch^depth).

See the following example:

```java
public int function(in n){
  if(n<=1){
    return 1;
  } 
  return function(n-1)+function(n-1);
}
```

This function will take O(2^N) time. See the explanation below-

![Recursive function runtime](./images/recursiveFunction.png "Source: Cracking
    the Coding Interview")

#### Space Complexity

Analyze how much space does an algorithm takes. If we need to create an array of
size n, it will require O(n) space. If we create a two dimensioanl array of size
nXn, this will require O(n^2) space. Stack space in recursive call counts too.
The following code will take O(n) space.

    int sum(int n){ if(n<=0){ return 0; } return n+summmm(n-1); }

Each call adds a level to the stack.  sum(4) -> sum(3) -> sum(2) -> sum(1) ->
sum(0)

It is important to understand here that, having n call to a function doesn't
mean it will take O(n) space. If the function call doesn't stay in the call
stack simultaneously, it will take less space. See the following example:

    int pairSumSequence(int n){ int sum= 0; for(int i=0; i< n; i++){ sum +=
      pairSum(i, i+1); } return sum; }

    int pairSum(int a, int b){ return a+b; }

Here thare are approximately O(n) calls to the pairSum. However, those calls
don't exist in the call stack simultaneously. So it needs only O(1) space.

### Analysis of Algorithm

#### Analysis of Loops

**O(1)**

Order of growth is constant.

Time complexity of a loop is constant time if it does not contain any loop,
     recursion or any other non-constant code. A loop or recursion is also
     constant if it runs for constant time.

     //constant loop for(int i = 0, i < c; i++){ //some O(1) code }

**O(n)**

The order of growth is linear.

Time complexity of a loop is O(n), if the loop variable is incremented or
decremented by a constant number.

    //O(n) loop for(int i = 0, i< n; i+=c){ //some o(1) expression }

An interesting [example](https://www.mathsisfun.com/algebra/logarithms.html)

**O(n^c)**

O(n^2) -> The order of growth is quadratic.  O(n^3) -> The order of growth is
cubic.

This happens in nested loops. The time complexity depends on the number of times
the inner most statement is executed. [src2](#analysis-of-loops).

    //Quadratic loop for(int i= 0; i < n; i++){ for(int j = 1; j < n; j++){
    //some O(1) expression } }

    //Cubic loop for(int i= 0; i < n; i++){ for(int j = 1; j < n; j++){ for(int
k = 0; k < n; k++){ //some O(1) expression } } }

**O(logn)**

The order of growth is logarithmic.

[Watch this](https://www.youtube.com/watch?v=M4ubFru2O80)

Question: If a loop is incremented by power of 3 or any other number number
apart from 2, how do we write O?

#### Some complex runtimes

See the following example:

![Analysis of Algorithm](./images/analysisOfAlgorithm.png "Analysis of
    Algorithm")

**Source: Cracking the Coding Interview, Page: 49**

For more exercise see "Cracking the coding interview".

### Algorithm Design Technique

#### Levels of Design

- Naive Algorithm: Convert the problem definition into algorithm. Provides
insight of problem and hints of improving the algorithm. These are slow.
- Algorithm by way of standard tools: Is there other algorithm that solves the
problem efficiently
- Optimized algorithm: Look into the design and try to improve
- Magic algorithm: Unique insight

#### Steps to develop a usable algorithm

1. Model the problem- Figure out what needs to be solved
2. Find Algorithm- Find an existing algorithm to solve the problem
3. Analyze speed and space- Is the algorithm fast enough? Does it fit into
   memory?
4. Find reason- If doesn't meet time and space requirement find the reason why.
5. Find solution- Find a way to address the reason
6. Loop- Iterate until satisfied

### Greedy Algorithm

First, find a greedy solution, and prove that it is safe which means that it is
correct. Then split the problem into sub-problem.

@tag-question: What is optimal solution?

@tag-answer: An optimal solution is a solution to an **optimization problem**
which minimizes(or maximizes) the objective function.
[Source](https://xlinux.nist.gov/dads/HTML/optimization.html)

@tag-question: What is optimization problem?

@tag-answer: An optimization problem asks what is the best solution to a
problem. This is a computational problem in which the objective is to find out
the best of all possible solutions. More formally find a solution in the
feasible region which has the minimum (or maximum) value of objective function.
[Source](https://xlinux.nist.gov/dads/HTML/optimization.html)

@tag-question: What is objective function?

@tag-answer: A function associated with optimization problem which determines
how good the solution is. For example, the total cost of edges in a solution to
traveling salesman problem.
[Source](https://xlinux.nist.gov/dads/HTML/optimization.html)

Commonly, greedy algorithm and the problems they can solve are characterized by
most or all of the following features-

- We have some problem to solve in an optimal way.
- To solve the problem we have a **set or** **list of candidates**.
- As the algorithm proceeds we accumulate **two other** **sets**.
- One contains candidates that have already been considered and **chosen**.
- Other contains candidates that have been considered and **rejected**.
- So, we **pick one candidate** and put it in either chosen or rejected set. We
use the selection function to chose the next most promising value.
- There is a function that checks whether a **particular set of candidates
provides a solution** to the problem, ignoring questions of optimality. So, we
take the **chosen** set and check if it solves the problem.
- A second function checks whether a **set of candidates is feasible.** It means
whether it is possible to construct a set by adding further candidates so that
it solves the problem. We expect that will be at least one solution using the
initial set of candidates.
- There is another function, Selection Function. This function tells us which of
the remaining candidates are most promising to chose next. These remaining
candidates are neither chosen nor rejected.
- Finally, an objective function gives the value of a solution we have found.
For example, the number of coins in money change problem. This function does not
appear explicitly in the algorithm.

So basically, to solve our problem, we try to find a solution using the set of
candidates and then optimize the value of objective function. We start with an
empty set of chosen candidates. Then at each step, we take the **best remaining
untried** candidate and **consider adding**to **chosen set.** We use the
**selection function** to find the best choice. We need to define it based on
the problem we are trying to solve.

Once the selection function provides us a candidate, we see whether an enlarged
set of chosen item is feasible. We use **feasible function** to check it. If not
feasible, we reject the candidate and add to rejected set. If the enlarged set
is feasible, we add the candidate to the chosen set.

After, enlarging the chosen set, we check to see if it constitute a solution to
our problem.

We can write the structure of a greedy algorithm in the following way- 

![Greedy Algo Structurej](./images/greedyAlgo.png "Greedy Algorithm Structure")

Note three functions- selection, feasible and solution. The objective function
is not present explicitly in this algorithm. The selection function is related
to the objection function. For example, if my objective is to choose minimum
number of coins for a change, I need to select the largest value coin. If we
want to minimize cost, we need to select the cheapest remaining candidate. But
sometimes there will be multiple plausible selection function. So, we need to
chose the right one if we want our algorithm properly. Question is how do we
chose?

### Divide and Conquer Algorithm

- Break the problem into smaller problems. Sub-problems must be of same type of the larger problem and can not overlap.
- Solve the sub-problems. Naturally leads to recursion.
- Combine the result of all sub-problems.

### Sorting

#### Bubble sort

1. Compare two items
2. Swap them based on comparison result

At the end of each loop the item that meets the comparison criteria goes at the
end of the array.

Time complexity is O(n^2) - quadratic.

#### Selection sort

1. A value is selected from array
2. It is compared with next value
3. If next value is smaller, the next value becomes new selected value
4. The two values are swapped

Selection sort is a little bit more efficient than bubble sort because it need
less swaps between elements. However, the time complexity is still O(n^2)-
quadratic.

It can be useful when the data set is small and it is expensive to swap objects
because it makes less swap.

#### Insertion sort

1. An element is removed from array and stored in a temporary variable
2. All the items to the left of the removed position are compared with the
removed item and shifted right.
3. The removed item is placed into appropriate place.

Time complexity is quadratic (O(n^2)). However, it runs twice as fast as bubble
sort because it copies item not swap. Copy is less expensive than swap. But, if
the data is inversely sorted, it is no better than bubble sort.

It is useful, when the data is partially sorted. In many cases, insertion sort
is used as the last stage of complex sort algorithm.

## Source

1. [Analysis of Algorithm](https://www.geeksforgeeks.org/analysis-of-algorithms-set-1-asymptotic-analysis/)
[](#analysis-of-loops)
2. [Analysis of
Loops](https://www.geeksforgeeks.org/analysis-of-algorithms-set-4-analysis-of-loops/?ref=lbp)
3. Data Structures and Algorithms in Java, 2nd Edition, by Robert Lafore
4. [Complexity and Big-O
Notation](http://pages.cs.wisc.edu/~vernon/cs367/notes/3.COMPLEXITY.html)
5. Cracking the coding interview
6. [Coursera Interactive
Site](https://suyvpwfgcxkbyggcoouhpe.coursera-apps.org/notebooks/bigo.ipynb)

