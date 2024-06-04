import connectedNodes as CN
import totalValue as TV

def totalRevenueValue(graph,dfFNSite,dfProbes):

    """
    Calculates revenue of graph through iteration of nodes and for duplicator probes iterating through neighbours
    :param graph: nx graph of map 
    :param dfFNSite: dataframe of FNSite information containing per site revenue and sightseeing information
    :param dfProbes: dataframe of Probe information containing probe multipliers

    :return total: total value of revenue of all nodes
    """

    total = 0

    for node in graph:
        spots = dfFNSite[dfFNSite['FNSite'] == node]['Spots'].values[0]
        
        if graph.nodes[node]['Probe'][:7] == "Revenue":
            total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Revenue'].values[0] + (1000 * spots),
                                  dfProbes[dfProbes['Probe'] == graph.nodes[node]['Probe']]['Revenue'].values[0],
                                  CN.chainedSites(graph,node,graph.nodes[node]['Probe']),
                                  CN.boostedSite(graph,node))
            
        elif graph.nodes[node]['Probe'] == "Duplicator":
            # makes duplicator act as neighbouring probes for calculations
            for neighbour in graph.neighbors(node):
                if graph.nodes[neighbour]['Probe'][:7] == "Revenue":
                    total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Revenue'].values[0] + (1000 * spots),
                                          dfProbes[dfProbes['Probe'] == graph.nodes[neighbour]['Probe']]['Revenue'].values[0],
                                          1,
                                          CN.boostedSite(graph,node))
                else:
                    total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Revenue'].values[0],
                                          dfProbes[dfProbes['Probe'] == graph.nodes[neighbour]['Probe']]['Revenue'].values[0],
                                          1,
                                          CN.boostedSite(graph,node))
        else:
            total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Revenue'].values[0],
                                  dfProbes[dfProbes['Probe'] == graph.nodes[node]['Probe']]['Revenue'].values[0],
                                  CN.chainedSites(graph,node,graph.nodes[node]['Probe']),
                                  CN.boostedSite(graph,node))
    
    return total