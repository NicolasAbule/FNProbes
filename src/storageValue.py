import connectedNodes as CN
import totalValue as TV

def totalStorageValue(graph):

    """
    Calculates storage of graph through iteration of nodes and for duplicator probes iterating through neighbours

    :param graph: nx graph of map 

    :return total: total value of storage value of all nodes
    """

    total = 0

    for node in graph:
        if graph.nodes[node]['Probe'] == "Storage":
            total += TV.siteValue(3000,1,CN.chainedSites(graph,node,"Storage"),CN.boostedSite(graph,node))
        elif graph.nodes[node]['Probe'] == "Duplicator":
            for neighbour in graph.neighbors(node):
                if graph.nodes[neighbour]['Probe'] == "Storage":
                    total += TV.siteValue(3000,1,1,CN.boostedSite(graph,node))

    return total