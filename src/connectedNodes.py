def chainedSites(graph, startingSite, probeType):

    """
    recursively goes through node and their neighbours to check for same node type

    :param graph: nx graph of map
    :param startingSite: number of site to check for adjacent neighbours of same type
    :param probeType: the probe on startingSite

    :return: number corrresponding to bonus for chain length
    """

    visitedNodes = set()
    chainLength = 0

    def dfs(node):
        nonlocal chainLength
        visitedNodes.add(node)

        # Check if the current node has the same probe type
        if graph.nodes[node].get("Probe") == probeType:
            chainLength += 1

            # Recursively explore adjacent nodes
            for neighbour in graph.neighbors(node):
                if neighbour not in visitedNodes:
                    dfs(neighbour)

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

    """
    goes through adjacent nodes of site to check for boosters

    :param graph: nx graph of map
    :param site: number of site to check for adjacent boosters

    :return: number corrresponding to bonus from all boosters
    """

    booster = 1

    for neighbour in graph.neighbors(site):
        neighbour_probe_type = graph.nodes[neighbour].get("Probe")
        if neighbour_probe_type == "Booster1":
            booster *= 1.5
        elif neighbour_probe_type == "Booster2":
            booster *= 2
        elif neighbour_probe_type == "Duplicator":
            # Check if the duplicator is connected to a booster
            for dup_neighbour in graph.neighbors(neighbour):
                if graph.nodes[dup_neighbour].get("Probe") == "Booster1":
                    booster *= 1.5
                elif graph.nodes[dup_neighbour].get("Probe") == "Booster2":
                    booster *= 2

    return booster