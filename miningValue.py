def siteMiningValue(base,efficiency,chain,booster):
    return base * efficiency * chain * booster

def chainedSites(graph, startingSite, probeType):

    visitedNodes = set()
    chainLength = 0

    def dfs(node):
        nonlocal chainLength
        visitedNodes.add(node)

        # Check if the current node has the same probe type
        if graph.nodes[node].get("Probe") == probeType:
            chainLength += 1

            # Recursively explore adjacent nodes
            for neighbor in graph.neighbors(node):
                if neighbor not in visitedNodes:
                    dfs(neighbor)

    # Start DFS exploration from the specified starting site
    dfs(startingSite)
    if chainLength >= 8:
        return 1.8
    elif chainLength >= 5:
        return 1.5
    elif chainLength >= 3:
        return 1.3
    else:
        return 1

def boostedSite(graph, site):

    booster = 1

    for neighbor in graph.neighbors(site):
        neighbor_probe_type = graph.nodes[neighbor].get("Probe")
        if neighbor_probe_type == "Booster1":
            booster *= 1.5
        elif neighbor_probe_type == "Booster2":
            booster *= 2
        elif neighbor_probe_type == "Duplicator":
            # Check if the duplicator is connected to a booster
            for dup_neighbor in graph.neighbors(neighbor):
                if graph.nodes[dup_neighbor].get("Probe") == "Booster1":
                    booster *= 1.5
                elif graph.nodes[dup_neighbor].get("Probe") == "Booster2":
                    booster *= 2

    return booster

def totalMiningValue(graph):
    total = 0
    for node in graph:
        total += siteMiningValue(node.base,node.efficency,chainedSites(graph,node.Site,node.Probe),boostedSite(graph,node))