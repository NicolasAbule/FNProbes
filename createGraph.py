import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import miningValue as MV
import revenueValue as RV
import storageValue as SV

df = pd.read_csv('./fnSiteInfo.csv')

# Create an undirected graph
G = nx.Graph()

# Add nodes from the 'node name' column
for _, row in df.iterrows():
    node_attributes = {
        'FNSite': int(row['FNSite']),
        'Mirinium': int(row['Mirinium']),
        'Revenue': int(row['Revenue']),
        'Probe': "Basic"
    }
    G.add_node(row['FNSite'], **node_attributes)

# Add edges from the list of connected nodes
for _, row in df.iterrows():
    connected_nodes = row['Connections'].strip('[]').split(',')
    for node in connected_nodes:
        G.add_edge(row['FNSite'], int(node.strip()))

dfFNSite = pd.read_csv('./fnSiteInfo.csv')
dfProbes = pd.read_csv('./probeInfo.csv')
test = 315

G.nodes[316]['Probe'] = "Booster2"

# Example: Accessing attributes of a node
print("Attributes of node:", G.nodes[test])
print("Mirinium value of node:", G.nodes[test]['Mirinium'])
print("Revenue value of node:", G.nodes[test]['Revenue'])
print("Probe type of node:", G.nodes[test]['Probe'])
print("Edges:", G.edges(test))

print(MV.totalMiningValue(G,dfFNSite,dfProbes))
print(RV.totalRevenueValue(G,dfFNSite,dfProbes))
print(SV.totalStorageValue(G))