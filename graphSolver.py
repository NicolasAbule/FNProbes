import random
import numpy as np
import miningValue as MV
import revenueValue as RV
import storageValue as SV

def simulatedAnnealing(G, df, dfProbes, storageWeight, revenueWeight, miningWeight, temperature, cooling_rate, iterations):
  """
  Args:
    G: A networkx graph object with a 'Probe' attribute on each node.
    probes: A list of all available probes.
    temperature: Initial temperature.
    cooling_rate: Rate at which temperature cools down.
    iterations: Number of iterations to run the algorithm.

  Returns:
    The modified graph (G) with updated probe assignments and the best value found.
  """
  # Randomly assign probes to nodes (avoid duplicates)

  useableProbes = ['Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining5', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining6', 'Mining7', 'Mining7', 'Mining7', 'Mining7', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining8', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining9', 'Mining10', 'Mining10', 'Mining10', 'Mining10', 'Revenue1', 'Revenue1', 'Revenue1', 'Revenue2', 'Revenue2', 'Revenue2', 'Revenue2', 'Revenue3', 'Revenue3', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue4', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue5', 'Revenue6', 'Revenue6', 'Revenue6', 'Revenue6', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Storage', 'Booster1', 'Booster1', 'Booster1', 'Booster2', 'Booster2', 'Booster2']

  random.shuffle(useableProbes)

  for node in G.nodes:
    G.nodes[node]['Probe'] = useableProbes.pop()

  best_value = SV.totalStorageValue(G) * storageWeight + RV.totalRevenueValue(G,df,dfProbes) * revenueWeight + MV.totalMiningValue(G,df,dfProbes) * miningWeight
  best_configuration = G.copy()

  try:
    for iteration in range(iterations):
      # Choose a node with unassigned probe (optional)
      available_nodes = [node for node in G.nodes if G.nodes[node]['Probe'] in useableProbes]
      node = random.choice(available_nodes) if available_nodes else None
      
      if not node:  # No more unassigned nodes or probes left
        break

      # Random probe different from current
      new_probe = random.choice(useableProbes)

      # Update node probe
      old_probe = G.nodes[node]['Probe']
      useableProbes.append(old_probe)
      G.nodes[node]['Probe'] = new_probe
      useableProbes.remove(new_probe)

      # Calculate new value and delta
      new_value = SV.totalStorageValue(G) * storageWeight + RV.totalRevenueValue(G,df,dfProbes) * revenueWeight + MV.totalMiningValue(G,df,dfProbes) * miningWeight
      delta_value = new_value - best_value

      # Accept worse solution with some probability
      if delta_value >= 0 or random.random() < np.exp(delta_value / temperature):
        best_value = new_value
        best_configuration = G.copy()

      # Cool down temperature
      temperature *= cooling_rate

      print(f"Iteration {iteration+1}: Best Value - {best_value}")

  except KeyboardInterrupt:

    print(f"Best value: {best_value}")
    for node, data in best_configuration.nodes(data=True):
      print(f"Node {node}: Probe - {data['Probe']}")

    print(f"Total Storage Value: {SV.totalStorageValue(G)}")
    print(f"Total Revenue Value: {RV.totalRevenueValue(G, df, dfProbes)}")
    print(f"Total Mining Value: {MV.totalMiningValue(G, df, dfProbes)}")
    print(f"Program interrupted.")
    exit(0)

  print(f"Best value: {best_value}")
  for node, data in best_configuration.nodes(data=True):
    print(f"Node {node}: Probe - {data['Probe']}")

  print(f"Total Storage Value: {SV.totalStorageValue(G)}")
  print(f"Total Revenue Value: {RV.totalRevenueValue(G, df, dfProbes)}")
  print(f"Total Mining Value: {MV.totalMiningValue(G, df, dfProbes)}")

  return G, best_value