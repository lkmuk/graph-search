# Data structures for representation directed graphs

* set of edges + set of vertices (used by `igraph`)
* (sparse) adjacency table (used here, see `graph_rep.py`)
* (dense) connectivity matrix (generally assymetric!)

> notatation:
>   * $N$: number of nodes in the graph
>   * $E$: number of edges in the graph

For a fully-connected graph, we have $E = 2^N$ 
but it has limited practical value, 
instead a (sparse) graph typically has much fewer edges, 
i.e. $E \ll 2^N$.


# Graph/ Path search problems
Remarks: when solving such graph problems, we assume the graph is "frozen".

## Feasibility problem & traversal methods

### Problem statement:

Given a start node ($S$), a goal node ($G$), and a directed graph (containing those end nodes),
determine a path from $S$ to $G$, if any; otherwise report `None`.

### Attributes of an traversal algorithm:
* Here, complexity (for a test case) refers to the number of iterations required to find a solution 
* worst-case (analytical) complexity
* average complexity
  > todo: empirically compare DFS vs BFS


### Not a reasonable approach
* enumerate all permutations of $ 0, ... , N-2$ nodes, which all are preceeded by $S$ and followed by $G$.
  ```
  Think about how many nodes are in between
  S->G         ==> 1
  S->X-> G     ==> N-2
  S->X->Y->G   ==> (N-2)(N-3)
  ...
  S->...->G    ==> (N-2)!
  --------------------------
  total            worst-case complexity  = $O(N^{N-2})$ !!!
  ```
  

### Two efficient approaches
* Breadth-First-Search, BFS for short (using FIFO)
* Depth-First-Search, DFS for short (using LIFO)
  
>  worst-case complexity = $O(E)$
>  obviously, this is much better than the enumeration "approach".

Note that BFS and DFS are basically the same, 
except from the distinctive node opening strategies (FIFO vs LIFO).
(see the implementation in algo_forward.py)


# Discrete optimal path problems

## Forward methods 

* API
  * constructor `(graph_with_cost_attr, start, goal)`
  * `solve()`

* Algorithms
  * Dijkstra (can be considered a special case of A*, but the search policy is no longer goal-guided!)
  * A*
    > discussions on the heuristic cost (function):
    >  1. its interpretation/ admissibility requirement
    >  2. how to ensure it is admissible? (Euclidean distance if the objective is to minimize total path length)
    >  3. benefit of the  (overoptimistic) remaining cost 
    >     [more "informant"] --- at least as efficient!
    >     [extreme case: h = cost-to-go (i.e. the upper bound)]
  * D* (and other incremental search techniques)

## Dynamic programming

* API
  * constructor `(graph_with_cost_attr, goal)`
  * `solve_backward()`
  * `solve_forward(start)`

> value function, aka cost-to-go function

> discussion: DP vs A*
>    feedback solution (useful in case for some reason deviated from the original optimal path)
