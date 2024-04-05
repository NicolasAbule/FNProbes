import connectedNodes as CN
import totalValue as TV

def totalRevenueValue(graph,dfFNSite,dfProbes):
    total = 0

    for node in graph:
        spots = dfFNSite[dfFNSite['FNSite'] == node]['Spots'].values[0]
        
        if graph.nodes[node]['Probe'][:7] == "Revenue":
            total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Revenue'].values[0] + (1000 * spots),dfProbes[dfProbes['Probe'] == graph.nodes[node]['Probe']]['Revenue'].values[0],CN.chainedSites(graph,node,graph.nodes[node]['Probe']),CN.boostedSite(graph,node))
        else:
            total += TV.siteValue(dfFNSite[dfFNSite['FNSite'] == node]['Revenue'].values[0],dfProbes[dfProbes['Probe'] == graph.nodes[node]['Probe']]['Revenue'].values[0],CN.chainedSites(graph,node,graph.nodes[node]['Probe']),CN.boostedSite(graph,node))
    
    return total