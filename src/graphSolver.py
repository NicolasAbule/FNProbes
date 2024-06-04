import random
import numpy as np
import miningValue as MV
import revenueValue as RV
import storageValue as SV

def simulatedAnnealing(G, dfFNSite, dfProbes, storageWeight, revenueWeight, miningWeight, temperature, coolingRate, iterations):

  """
  finds a graph that maximizes the total of storage, revenue and mining through simulated annealing approach

  :param G: nx graph of map
  :param dfFNSite: dataframe of FNSite information containing per site revenue, per site mining, and sightseeing information
  :param dfProbes: dataframe of Probe information containing probe multipliers
  :param storageWeight: weight to multiply storage amount by to get weighted score
  :param revenueWeight: weight to multiply revenue amount by to get weighted score
  :param miningWeight: weight to multiply mining amount by to get weighted score
  :param temperature: value to start the annealing schedule at
  :param coolingRate: rate at which temperature decreases to accept suboptimal solutions
  :param iterations: how many times the swaps will happen

  :return G: altered graph with swapped nodes
  :return bestValue: weighted sum of storage, revenue and mining.
  """
  
  useableProbes = ['Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining7', 'Mining7', 'Mining7', 'Mining7', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining10', 'Mining10', 'Mining10', 'Mining10', 'Revenue1', 'Revenue1', 'Revenue1', 'Revenue2', 'Revenue2', 'Revenue2', 'Revenue2', 'Revenue3', 'Revenue3', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue6', 'Revenue6', 'Revenue6', 'Revenue6', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Booster1', 'Booster1', 'Booster1', 'Booster2', 'Booster2', 'Booster2', 'Duplicator', 'Duplicator', 'Duplicator', 'Duplicator']
  random.shuffle(useableProbes)

  for node in G.nodes:
    G.nodes[node]['Probe'] = useableProbes.pop()

  bestValue = SV.totalStorageValue(G) * storageWeight + RV.totalRevenueValue(G,dfFNSite,dfProbes) * revenueWeight + MV.totalMiningValue(G,dfFNSite,dfProbes) * miningWeight
  bestConfiguration = G.copy()

  #making it so less swaps occur after certain number of iterations
  initialSwaps = 8
  thresholdIteration = int(iterations * 0.25)

  try:
    for iteration in range(iterations):
      swapsPerIteration = initialSwaps if iteration < thresholdIteration else int(initialSwaps * 0.75)

      for _ in range(swapsPerIteration):

        # Choose two random nodes (avoid self-swapping)
        node1, node2 = random.sample(list(G.nodes), 2)
        if node1 == node2:
          continue

        # Perform swap and calculate new value
        probe1 = G.nodes[node1]['Probe']
        probe2 = G.nodes[node2]['Probe']
        G.nodes[node1]['Probe'], G.nodes[node2]['Probe'] = probe2, probe1
        newValue = SV.totalStorageValue(G) * storageWeight + RV.totalRevenueValue(G, dfFNSite, dfProbes) * revenueWeight + MV.totalMiningValue(G, dfFNSite, dfProbes) * miningWeight

        deltaValue = newValue - bestValue

        if deltaValue >= 0 or random.random() < np.exp(deltaValue / temperature):
          bestValue = newValue
          bestConfiguration = G.copy()

        # Undo swap if not accepted
        if deltaValue < 0:
          G.nodes[node1]['Probe'], G.nodes[node2]['Probe'] = probe1, probe2

      temperature *= coolingRate

      print(f"Iteration {iteration+1}: Best Value - {bestValue}: Temperature - {temperature}")

  except KeyboardInterrupt:

    print(f"Best value: {bestValue}")
    for node, data in bestConfiguration.nodes(data=True):
      print(f"Node {node}: Probe - {data['Probe']}")

    print(f"Total Storage Value: {SV.totalStorageValue(G)}")
    print(f"Total Revenue Value: {RV.totalRevenueValue(G, dfFNSite, dfProbes)}")
    print(f"Total Mining Value: {MV.totalMiningValue(G, dfFNSite, dfProbes)}")
    print(f"Program interrupted.")
    exit(0)

  print(f"Best value: {bestValue}")
  for node, data in bestConfiguration.nodes(data=True):
    print(f"Node {node}: Probe - {data['Probe']}")

  print(f"Total Storage Value: {SV.totalStorageValue(G)}")
  print(f"Total Revenue Value: {RV.totalRevenueValue(G, dfFNSite, dfProbes)}")
  print(f"Total Mining Value: {MV.totalMiningValue(G, dfFNSite, dfProbes)}")

  return G, bestValue