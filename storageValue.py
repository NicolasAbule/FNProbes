import connectedNodes as CN
import totalValue as TV

def totalStorageValue(graph):
    total = 0

    for node in graph:
        if graph.nodes[node]['Probe'] == "Storage":
            total += TV.siteValue(3000,1,CN.chainedSites(graph,node,"Storage"),CN.boostedSite(graph,node))

    return total