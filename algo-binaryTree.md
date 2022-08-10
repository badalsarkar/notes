# Trees and Graphs

- What is a Tree?
- What is a binary tree?
  A tree in which each node has up to two children.
- What is leaf?
  A node is called leaf if it doesn't have any child node.
- What is a binary search tree?
  A binary tree is a binary search tree if it fulfills a particular ordering
  property. That is all left descendants <= n < all right descendants. This must
  be true for each node *n*.
   
  Note: The binary search tree definition may vary in terms of the equality
  condition. In some cases a binary search tree can't contain any duplicate
  value. In other cases it may be part of right descendants.

  Note: The inequality condition must be true for all of node's descendants not
  just its immediate children.

{% include image.html url="./images/binaryTree.png" description="Image: Binary search tree" title ="" width="" %}

- What is balanced vs unbalanced tree?
- What is complete binary tree?
  A binary tree is complete when every level of the tree is fully filled except
  may be the last level. The last level may be filled from left to right.
- What is a full binary tree?
- What is a perfect binary tree?

## Binary tree traversal

**Pre-order traversal**

nlr(node, left, right).

The current node is visited first, then the left node and then the right node.

**In-order traversal**

lnr(Left, node, right).

The left node is visited first, then the current node and the right node.

**Post-order traversal**

lrn(Left, right, node).

The current node is visited last.

## Binary Heap

Two types of binary heap- mean heap and max heap.

**Mean heap**

A binary tree which is complete where each node is smaller than its child nodes.
So, the root is always the lowest.

**Insertion at mean heap**

When inserting an element we must maintain two properties- 

1) The tree must remain complete, meaning only the last level can be partially
full and that is from left to right. So, only the right node can be empty.
2) The lowest node must be on the top.

To achieve this, we insert a new element to the lowest level and at the
rightmost node. Then we compare it with its parent and swap if necessary.

The run time is O(log n).

**Extracting minimum element**

The minimum element is always at the top. When extracting again we need to
maintain two above mentioned properties. To achieve this, we do the following-

1) We extract the minimum element and replace it with the bottommost and
rightmost element.
2) Then we compare this with its children and swap if necessary. We can compare
either in right or left direction.

The run time is O(log n).

## Tries (Prefix trees)

## Graph

**What is graph?**

Graphs are collection of nodes with edges between some of them. Graphs follows
the following rules-

- A graph is made up of two sets- vertices and edges
- Vertices set may be finite or infinite
- Each element in the edge set is pair of two elements from vertices set

**Types of graphs**

- Undirected
- Directed
- Cyclic
- Weighted
- Connected graph

**Representing a graph**

- Adjacency list
- Adjacency matrices













