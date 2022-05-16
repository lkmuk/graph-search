from graph_rep import directed_graph_weighted

__all__ = ["Astar"]

class Astar:
    def __init__(self, start: str, goal: str, graph: directed_graph_weighted):
        """

        Args:
            start (str):
            goal (str): 
            graph (directed_graph_weighted): (alias!)


        Important additional data structure employed here

        1. a node_table (aka the tree):

            node name (as ID),  parent, cum_cost_estimate

        2. the open buffer (should be a set of node names)

        Remarks on the choices made above:
        * to avoid data staleness, there is no "visited flag" for every node in `graph`,
          instead it is computed based on `node_is_visited(node_name)`
        * In principle, cum_cost_estimate is also redundant but
          it makes perfect sense to "cache" it.
          In fact, I use cum_cost_estimate (often denoted as g) instead of f
        * This implementation has a VERY SIMPLE buffer (just a dict)
          --- priority queue is NOT used

        """

        node_set = graph.list_all_nodes()
        assert start in node_set, f"The start node {start} cannot found in the graph!"
        assert goal in  node_set, f"The goal node {goal} cannot found in the graph!"
        self.start = start
        self.goal = goal
        
        assert isinstance(graph, directed_graph_weighted)
        self.graph = graph # just an alias

        self.tree_cum_cost = {start: 0.0} # often denoted as g
        self.tree_parent  = {start: None}

        self._buffer = set([self.start]) # holding nodes to investigate further, aka the fringe/ OPEN set
        # you might want to implement it as a priority queue instead

        self.iter = 0 # relevant for academic purpose

    def node_is_visited(self,node):
        return node in self.tree_parent.keys()
    
    def calc_total_cost_est(self,intermediate_node):
        assert self.node_is_visited(intermediate_node), f"Node {intermediate_node} not yet visited"
        return self.tree_cum_cost[intermediate_node] + self.graph._cost_node[intermediate_node]

    def extract_best_node_from_buffer(self):
        list_nodes_in_buffer = list(self._buffer)
        # just an initialization for searching among nodes in the OPEN buffer
        # the node with minimum estimated total path cost
        node_to_pop = list_nodes_in_buffer[0]
        f_lowest = self.calc_total_cost_est(node_to_pop)
        for n in list_nodes_in_buffer[1:]:
            f = self.calc_total_cost_est(n)
            if f < f_lowest:
                node_to_pop = n
                f_lowest = f

        # don't forget this!
        self._buffer.remove(node_to_pop)
        return node_to_pop

    def solve(self,validate_heuristics = True):
        """
        If a solution is found, 
            it will output 
            1. the (forward) path sequence (list)
            2. the total path cost (float)
        Suppose a solution is found,
            This implementation can also 
            validate the admissibility of the heuristic costs
            (at least along the identified path)
            This is a SUFFICIENT condition 
            for the solution to be optimal

        Raises:
            ValueError: if the algorithm fails to find a solution

            An error can be caused by 
            * the non-existence of solution and/or
            * non-admissible heuristics (TBD: examples).
        """
        while True:
            self.iter += 1
            node_current = self.extract_best_node_from_buffer()
            if node_current == self.goal:
                break # goto where???

            nodes_to_investigate = self.graph._adj[node_current] # a set object

            for fringe_node in nodes_to_investigate:
                if not self.node_is_visited(fringe_node): # unvisited
                    # make a new entry
                    self.tree_parent[fringe_node] = node_current
                    self.tree_cum_cost[fringe_node] = \
                        self.tree_cum_cost[node_current] \
                        + self.graph.get_cost_edge(node_current,fringe_node)

                    self._buffer.add(fringe_node) # not to forget!
                # IF ...
                #   a. already visited AND 
                #   b. it is better off to base the fringe_node
                #      from node_current (instead of basing from self.tree_parent[fringe_node])
                # THEN
                #   update the buffer (for my implementation, it's just about adding it to the buffer, if it hasn't)
                #   update the tree
                else:
                    cum_cost_alternative_path_start_to_fringe = \
                        self.tree_cum_cost[node_current] + self.graph.get_cost_edge(node_current,fringe_node)
                    if self.tree_cum_cost[fringe_node] > cum_cost_alternative_path_start_to_fringe:
                        # update the tree
                        self.tree_cum_cost[fringe_node] =  cum_cost_alternative_path_start_to_fringe
                        self.tree_parent[fringe_node] = node_current
                        # update the buffer (to allow expanding this fringe node in the next iteration)
                        self._buffer.add(fringe_node) 
                        # Remark 1: 
                        #   the built-in "set" dtype (the dtype of self._buffer) 
                        #   already ensures the buffer always contains distinctive elements
                        # Remark 2:
                        #   in my implementation, the cum cost (or equivalently the f-values)
                        #   are stored in the tree instead of the buffer                    

            if len(self._buffer)== 0:
                # raise ValueError("Can't find a solution")
                return None, None
        
        # backtracing the path (and validate the heuristics' admissibility)
        # initialization
        backward_path_seq = [self.goal]  # current node being backward_path_seq[-1]
        while backward_path_seq[-1] != self.start:
            node_next = self.tree_parent[backward_path_seq[-1]]

            # extra validation stuff
            if validate_heuristics:
                node_next_rem_cost_soln = self.tree_cum_cost[self.goal] - self.tree_cum_cost[node_next]
                node_next_rem_cost_heuristic = self.graph.get_cost_node(node_next)
                if node_next_rem_cost_soln < node_next_rem_cost_heuristic:
                    warnTxt  = f"[Info] your heuristic value for node {node_next} is unadmissible, \n"
                    warnTxt += f"       i.e. cost-to-go <= {node_next_rem_cost_soln} (from the soln) < {node_next_rem_cost_heuristic} (from the heuristics)"
                    warnTxt +=  "       ==> This means the solution might be sub-optimal."
                    print(warnTxt)

            backward_path_seq.append(node_next)
        return tuple(backward_path_seq[::-1]), self.tree_cum_cost[self.goal]


if __name__ == "__main__":
    from graph_examples import german_city_network_acc_de_wikipedia
    from graph_examples import longway_round

    tcase1 = german_city_network_acc_de_wikipedia()
    tcase1.verify(Astar, num_expected_iter=6)

    tcase2 = longway_round()
    tcase2.verify(Astar, num_expected_iter=6)
