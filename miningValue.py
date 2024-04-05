import connectedNodes as CN
import totalValue as TV

def totalMiningValue(graph,dfFNSite,dfProbes):
    total = 0

    for node in graph:
        total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Mirinium'].values[0],dfProbes[dfProbes['Probe'] == graph.nodes[node]['Probe']]['Mining'].values[0],CN.chainedSites(graph,node,graph.nodes[node]['Probe']),CN.boostedSite(graph,node))

    return total