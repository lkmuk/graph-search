from collections import deque
from graph_rep import directed_graph # for the tree

class BFS:
    def __init__(self, start: str, goal: str, graph: directed_graph):
        """Breadth-first-search

        Args:
            start (str): 
            goal (str): 
            adjacency_tab (directed_graph): 

        state of a node
        * 0 --- unopened/ unvisited
        * 1 --- open (i.e. the node is in the buffer)
        * (the state of being processed is not included here, as it is "atomic")
        * 2 --- visited
        """
        node_set = graph.list_all_nodes()
        assert isinstance(graph, directed_graph)
        assert start in node_set, f"The start node {start} cannot found in the graph!"
        assert goal in  node_set, f"The goal node {goal} cannot found in the graph!"
        self.start = start
        self.goal = goal
        

        self._adjacency = graph.get_adj_table_as_dict(exclude_leaf_node_from_index=False)
        # initialize the node information (that are relevant for the traversal problem)
        self._node_parent = dict([(node_name, None) for node_name in node_set])
        self._node_state = dict([(node_name, 0) for node_name in node_set])

        self._buffer = deque([self.start]) # holding nodes to process

        self.iter = 0 # relevant for academic purpose

    def get_unvisited_node_set(self):
        out = set()
        for node in self._node_state.keys():
            if self._node_state[node] == 0:
                out.add(node)
        return out

    def add_nodes_to_buffer(self, node_set_to_add: set):
        """ Here FIFO (BFS)
        assuming `node_set_to_add` is NON-empty!
        """
        # the specific order is implementation-dependent
        for node in node_set_to_add:
            self._buffer.appendleft(node) 

    def solve(self):
        current_node = None # whatever != self.goal

        # forward traversal
        while current_node != self.goal:
            if len(self._buffer) == 0:
                return None # No path connecting S--> G !

            # Our convention: pop from the RHS (even for LIFO, i.e. DFS)
            current_node = self._buffer.pop()
            
            # node expansion
            node_set_candidate = self._adjacency[current_node]
            node_set_unvisited = self.get_unvisited_node_set()
            node_set_to_add = node_set_candidate.intersection(node_set_unvisited)
            if len(node_set_to_add) > 0:
                self.add_nodes_to_buffer(node_set_to_add)
          
            # update the node status and parents
            for node_new in node_set_to_add:
                self._node_state[node_new]  = 1
                self._node_parent[node_new] = current_node
            self._node_state[current_node]  = 2
            self.iter += 1


        # backward traversal (to assemble the path)
        backward_path = [self.goal]
        while backward_path[-1] != self.start:
            current_node_on_path = backward_path[-1] 
            backward_path.append(self._node_parent[current_node_on_path])
        return backward_path[::-1]    


class DFS(BFS):
    def add_nodes_to_buffer(self, node_set_to_add: set):
        """ Here LIFO (DFS)
        assuming `node_set_to_add` is NON-empty!
        """
        # the specific order is implementation-dependent
        for node in node_set_to_add:
            self._buffer.append(node) 

if __name__ == "__main__":
    def make_sample_graph(with_loop=False):
        net = directed_graph()
        net.add_edge('S', 'depot')
        net.add_edge('S', 'A')
        net.add_edge('depot', 'D')
        net.add_edge('X', 'D')
        net.add_edge('X', 'F')
        net.add_edge('D', 'C')
        net.add_edge('A', 'C')
        if with_loop:
            net.add_edge('C', 'N')
            net.add_edge('N', 'A')
        return net
    
    graph1 = make_sample_graph(with_loop=False)
    print(graph1)
    solver = BFS('S', 'C', graph1)
    ans = solver.solve()
    print(ans)
    print(f"finished in {solver.iter} iteration(s)")