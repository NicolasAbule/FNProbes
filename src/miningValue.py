import connectedNodes as CN
import totalValue as TV

def totalMiningValue(graph,dfFNSite,dfProbes):

    """
    Calculates mining value of graph through iteration of nodes and for duplicator probes iterating through neighbours

    :param graph: nx graph of map 
    :param dfFNSite: dataframe of FNSite information containing per site mining and site information
    :param dfProbes: dataframe of Probe information containing probe multipliers

    :return total: total value of mining value of all nodes
    """

    total = 0

    for node in graph:
        if graph.nodes[node]['Probe'] == "Duplicator":
            for neighbour in graph.neighbors(node):
                total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Mirinium'].values[0],
                                      dfProbes[dfProbes['Probe'] == graph.nodes[neighbour]['Probe']]['Mining'].values[0],
                                      1,
                                      CN.boostedSite(graph,node))
        else:
            total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Mirinium'].values[0],
                                  dfProbes[dfProbes['Probe'] == graph.nodes[node]['Probe']]['Mining'].values[0],
                                  CN.chainedSites(graph,node,graph.nodes[node]['Probe']),
                                  CN.boostedSite(graph,node))

    return total