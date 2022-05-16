from graph_rep import * # in order to 
from abc import ABC
from numpy.testing import assert_almost_equal

class graph_algo_verifier(ABC):
    def __init__(self):
        """
        When subclassing this class, please 
        replace the placeholders if necessary
        """
        self.start = start
        self.goal = goal 
        self.graph = None
        # None ==> no-solution
        self.true_min_cost = None
        # there might be non-unique globally minimal paths, so a tuple
        self.tuple_global_soln = None 
        # a possible solution represents a globally optimal path, e.g.
        # soln1 == ("my Start", "B", "D", "E", "my goal")  # please use tuple!
        # `tuple_global_soln` is something like
        # (soln1,  soln2  )

       
        
    def print_problem(self, omit_weights=True):
        if omit_weights:
            print(self.graph)
        else:
            raise NotImplementedError("not yet supported by the implementation of directed_graph_weighted")
        print("Start node named: ", self.start)
        print("Goal  node named: ", self.goal)

    def print_expected_soln(self):
        if self.true_min_cost is None:
            print("No feasible solution") 
        else:
            print(f"Global minimum path cost: {self.true_min_cost: .2f}")
            print(f"The optimizer(s) can be:")
            for soln in self.tuple_global_soln:
                print(" ", soln)
    
    def print_summary(self):
        self.print_problem()
        self.print_expected_soln()

    def verify(self, algo_class:type, num_expected_iter = None, **kwargs):
        """

        Args:
            algo_class (type): _description_
            num_expected_iter (int, optional):
                this value is algorithm/ config-specific. If don't care, leave the defaults to None.
        """
        assert type(algo_class) == type, "Please pass in a class, not an object!"

        # instantiate an algorithm object
        solver = algo_class(self.start, self.goal, self.graph, **kwargs)

        soln_path, soln_cost = solver.solve(validate_heuristics=True)
        # It makes more sense to first test whether the optimal cost are correct!
        assert_almost_equal(soln_cost, self.true_min_cost)
        assert soln_path in self.tuple_global_soln

        if num_expected_iter is not None:
            assert isinstance(num_expected_iter,int) and num_expected_iter >= 1, "expect the expected number of iterations to be a positive integer!"
            assert solver.iter == num_expected_iter, f"got {solver.iter} but expect {num_expected_iter}"



class german_city_network_acc_de_wikipedia(graph_algo_verifier):
    def __init__(self):
        """
        https://de.wikipedia.org/wiki/A*-Algorithmus
        """
        self.start = "SB" #Saarbrücke
        self.goal = "WB" #Würzburg
        net = directed_graph_weighted("German city network from SB to WB")
        net.add_node("SB", 222.)
        net.add_node("KL", 158.)
        net.add_node("Frankfurt", 96.)
        net.add_node("LH", 108)
        net.add_node("KA", 140.)
        net.add_node("HB", 87.)
        net.add_node("WB", 0.)

        
        net.add_edge("SB", "KL", 70.)
        net.add_edge("SB", "KA", 145.)

        net.add_edge("KA", "HB", 84.)
        net.add_edge("HB", "WB", 102.)

        net.add_edge("KL","Frankfurt", 103.)
        net.add_edge("Frankfurt", "WB", 116.)
        net.add_edge("KL", "LH", 53.)
        net.add_edge("LH", "WB", 183.)

        self.graph = net
        self.true_min_cost = 289.0
        self.tuple_global_soln=tuple(
            [
                ('SB', 'KL', 'Frankfurt', 'WB')
            ]
        )


class longway_round(graph_algo_verifier):
    """
    In this test case ... 
    * The heuristics values are admissible. 
    * In particular, they are contrieved to show that 
      it is sometimes necessary to revisit
      some (visited) nodes.
    
      Here the node to be revisited is node E 
      (which is initially explored by expanding node "Start"
      and subsequently re-explored" by expanding node D).

    Aside:
    ------------
    How I came up with the example
    * imagine you are situated in a hostile terrain (starting point)
    * and you aim to reach another point at some distance apart (goal point), 
      which is also in a hostile terrain (possibly the same hilly region)
    * various possible paths:
      1. long way round (downhill to a valley, take the highway, then go uphill again) 
         Start --> C --> D --> E --> Goal (indeed contrieved to be the optimal path)
      2. Start --> C --> D --> Goal (contrieved to be similar to path 1, except the last stage)
      3. Start --> B --> E --> Goal  
    """
    def __init__(self):
        self.start = "Start"
        self.goal = "Goal"

        self.graph = directed_graph_weighted("longway round")
        self.graph.add_node("Start",0.)  # the heuristic (optimistic) cost-to-go estimate
        self.graph.add_node("C", 80.)
        self.graph.add_node("D", 50.)
        self.graph.add_node("E", 5.)
        self.graph.add_node("Goal",0.)

        self.graph.add_edge("Start", "C", 16.)
        self.graph.add_edge("Start", "E", 90.)
        self.graph.add_edge("C", "D", 30.)
        self.graph.add_edge("D", "E", 40.)
        self.graph.add_edge("E", "Goal", 10.)
        self.graph.add_edge("D", "Goal", 300.)

        self.true_min_cost = 96.0
        self.tuple_global_soln= tuple(
            [
                ('Start', 'C', 'D', 'E', 'Goal')
            ]
        )

if __name__ == "__main__":
    # inspect the test case!
    tcase1 = german_city_network_acc_de_wikipedia()
    tcase1.print_summary()

    tcase2 = longway_round()
    tcase2.print_summary()