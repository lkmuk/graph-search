class directed_graph:
    def __init__(self,name: str):
        # aka adjacency table/ more aptly "descendant table"
        # why not save the edges instead?
        #    adjacency table is an efficient representation
        assert isinstance(name, str)
        self.name = name
        self._adj = dict()
        # how it should look like
        #   'node1':  set("node1's descendant node A" , "node1's descendant node B"
        #   ... 
        #  
        #  the built-in set is really the suitable choice to avoid repeated entries.
        #  the built-in dict also ensures there is no repeated "keys" 
        #  (which in our case, corresponds to dublicates in nodes)

    def add_node(self, node_name: str):
        assert isinstance(node_name, str)
        if node_name in self._adj.keys():
            print(f"[Info] the node {node_name} was already in the graph!")
        else:
            self._adj[node_name] = set()


    def add_edge(self, parent_node: str, child_node: str):
        assert not parent_node == child_node, "self looping prohibited"
        assert isinstance(parent_node, str)
        assert isinstance(child_node, str)

        self.add_node(parent_node)
        self.add_node(child_node)
        if (parent_node in self._adj.keys()) and (child_node in self._adj[parent_node]):
            print(f"[Info] the edge {parent_node} --> {child_node} was already in the graph!")
            return
        else:
            self._adj[parent_node].add(child_node)

    
    def list_all_nodes(self):
        return set(self._adj.keys())
    def list_leaf_nodes(self):
        out = set()
        for node in self._adj.keys():
            if len(self._adj[node]) == 0:
                out.add(node)
        return out

    def get_adj_table_as_dict(self, exclude_leaf_node_from_index=True):
        out = self._adj.copy()
        if exclude_leaf_node_from_index:
            for leaf_node in self.list_leaf_nodes():
                del out[leaf_node]
        return out

    def __str__(self):
        out = "-"*20 + "\nGraph name: " + self.name + f"\n"
        out += " contains the following nodes and directed edges:\n"
        leaf_nodes_list = self.list_leaf_nodes()
        for node in self._adj.keys():
            if node in leaf_nodes_list:
                out += f"{node} (which is a leaf node)\n"
            else:
                out += f"{node} --> {self._adj[node]} \n"
        out += "-"*20
        return out
        
    def print_adj_table(self):
        print(self)

    def viz(self):
        # maybe use igraph? (maybe also use igraph for serializing the graph object)
        pass

class directed_graph_weighted(directed_graph):
    def __init__(self,name: str):
        super().__init__(name)
        self._cost_edge = dict()
        self._cost_node = dict() # could be used for heuristic cost-to-go
    def add_node(self, node_name, node_weight = 0.0):
        assert isinstance(node_weight, float) or isinstance(node_weight, int)
        super().add_node(node_name)
        self._cost_node[node_name] = node_weight
    @staticmethod
    def get_edge_name(parent_node, child_node):
        return f"{parent_node}->{child_node}"
    def add_edge(self, parent_node, child_node, edge_weight = 0.0):
        assert isinstance(edge_weight, float) or isinstance(edge_weight, int)
        assert not parent_node == child_node, "self looping prohibited"
        assert parent_node in self.list_all_nodes(), f"please first define the node {parent_node}"
        assert child_node in self.list_all_nodes(), f"please first define the node {child_node}"
        edge_ID = directed_graph_weighted.get_edge_name(parent_node, child_node)
        if edge_ID in self._cost_edge.keys():
            print(f"[Info] the edge {edge_ID} was already in the graph so your request is ignored!")
            return
        self._adj[parent_node].add(child_node)
        self._cost_edge[edge_ID] = edge_weight
    def get_cost_node(self, node_name):
        return self._cost_node[node_name]
        
    def get_cost_edge(self, parent_node, child_node):
        return self._cost_edge[self.get_edge_name(parent_node, child_node)]

def test_directed_graph():
    print("creating & editing a graph")
    A = directed_graph("A dummy graph")
    A.add_edge('E','C')
    A.add_edge('E','B')
    A.add_edge('H','A')

    print("======== inspection ========= ")
    print("the adjacancy table:")
    A.print_adj_table()

    print("let's trim down the adjacancy table!")
    adj_dict = A.get_adj_table_as_dict()
    for parent_node in adj_dict.keys():
            print(f"{parent_node} --> {adj_dict[parent_node]}")

    # (also to see if the internal data of A got messed up after the previous getting the dict)
    print("here are all the nodes")
    print(A.list_all_nodes())
    print("here are all the leaf nodes")
    print(A.list_leaf_nodes())


def test_directed_weighted_graph():
    print("creating & editing a graph")
    A = directed_graph_weighted("dummy graph with node and edge weights")
    A.add_node('E',10.0)
    A.add_node('C', 5.0)
    A.add_node('A', 20.0)
    A.add_node('B', 3.0)
    A.add_node('H', 1.0)
    A.add_edge('E','C',23.0)
    A.add_edge('E','B',10.0)
    A.add_edge('H','A',2.0)

    print(A)
    print(A.get_cost_node('B'))
    print(A.get_cost_edge('H','A'))

if __name__ == "__main__":
    test_directed_graph()
    test_directed_weighted_graph()


