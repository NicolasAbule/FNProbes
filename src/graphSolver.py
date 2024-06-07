import random
import numpy as np
import miningValue as MV
import revenueValue as RV
import storageValue as SV

def simulatedAnnealing(graph, dfFNSite, dfProbes, storageWeight, revenueWeight, miningWeight, temperature, coolingRate, iterations):

  """
  finds a graph that maximizes the total of storage, revenue and mining through simulated annealing approach

  :param graph: nx graph of map
  :param dfFNSite: dataframe of FNSite information containing per site revenue, per site mining, and sightseeing information
  :param dfProbes: dataframe of Probe information containing probe multipliers
  :param storageWeight: weight to multiply storage amount by to get weighted score
  :param revenueWeight: weight to multiply revenue amount by to get weighted score
  :param miningWeight: weight to multiply mining amount by to get weighted score
  :param temperature: value to start the annealing schedule at
  :param coolingRate: rate at which temperature decreases to accept suboptimal solutions
  :param iterations: how many times the swaps will happen

  :return graph: altered graph with swapped nodes
  :return bestValue: weighted sum of storage, revenue and mining.
  """

  useableProbes = []
  preassignedProbes = {}

  with open("./data/probeData.txt", 'r') as file:
    for line in file:
      type, amount = line.strip().split(':')
      for _ in range(int(amount)):
        useableProbes.append(type)
  
  with open("./data/assignedProbes.txt", 'r') as file:
    for line in file:
      node, probe = line.strip().split(':')
      preassignedProbes[node] = probe

  for probe in preassignedProbes.values():
    useableProbes.remove(probe)
  random.shuffle(useableProbes)

  availableNodes = [node for node in graph.nodes if node not in [int(node) for node in preassignedProbes.keys()]]
  for node in availableNodes:
    graph.nodes[node]['Probe'] = useableProbes.pop()

  for node, probe in preassignedProbes.items():
    graph.nodes[int(node)]['Probe'] = probe

  bestValue = SV.totalStorageValue(graph) * storageWeight + RV.totalRevenueValue(graph,dfFNSite,dfProbes) * revenueWeight + MV.totalMiningValue(graph,dfFNSite,dfProbes) * miningWeight
  bestConfiguration = graph.copy()

  #making it so less swaps occur after certain number of iterations
  initialSwaps = 8
  thresholdIteration = int(iterations * 0.25)

  try:
    for iteration in range(iterations):
      swapsPerIteration = initialSwaps if iteration < thresholdIteration else int(initialSwaps * 0.75)

      for _ in range(swapsPerIteration):

        # Choose two random nodes (avoid self-swapping)
        node1, node2 = random.sample(availableNodes, 2)
        if node1 == node2:
          continue

        # Perform swap and calculate new value
        probe1 = graph.nodes[node1]['Probe']
        probe2 = graph.nodes[node2]['Probe']
        graph.nodes[node1]['Probe'], graph.nodes[node2]['Probe'] = probe2, probe1
        newValue = SV.totalStorageValue(graph) * storageWeight + RV.totalRevenueValue(graph, dfFNSite, dfProbes) * revenueWeight + MV.totalMiningValue(graph, dfFNSite, dfProbes) * miningWeight

        deltaValue = newValue - bestValue

        if deltaValue >= 0 or random.random() < np.exp(deltaValue / temperature):
          bestValue = newValue
          bestConfiguration = graph.copy()

        # Undo swap if not accepted
        if deltaValue < 0:
          graph.nodes[node1]['Probe'], graph.nodes[node2]['Probe'] = probe1, probe2

      temperature *= coolingRate

      print(f"Iteration {iteration+1}: Best Value - {bestValue}: Temperature - {temperature}")

  except KeyboardInterrupt:

    print(f"Best value: {bestValue}")
    for node, data in bestConfiguration.nodes(data=True):
      print(f"Node {node}: Probe - {data['Probe']}")

    print(f"Total Storage Value: {SV.totalStorageValue(graph)}")
    print(f"Total Revenue Value: {RV.totalRevenueValue(graph, dfFNSite, dfProbes)}")
    print(f"Total Mining Value: {MV.totalMiningValue(graph, dfFNSite, dfProbes)}")
    print(f"Program interrupted.")
    exit(0)

  print(f"Best value: {bestValue}")
  for node, data in bestConfiguration.nodes(data=True):
    print(f"Node {node}: Probe - {data['Probe']}")

  print(f"Total Storage Value: {SV.totalStorageValue(graph)}")
  print(f"Total Revenue Value: {RV.totalRevenueValue(graph, dfFNSite, dfProbes)}")
  print(f"Total Mining Value: {MV.totalMiningValue(graph, dfFNSite, dfProbes)}")

  return graph, bestValue