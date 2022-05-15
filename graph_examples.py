from graph_rep import directed_graph_weighted

def make_german_wiki_example():
    """
    https://de.wikipedia.org/wiki/A*-Algorithmus
    """
    # start = SB (Saarbrücke)
    # goal = WB (Würzburg)
    net = directed_graph_weighted()
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

    return net

if __name__ == "__main__":
    # inspect the test case!
    net = make_german_wiki_example()
    print(net)