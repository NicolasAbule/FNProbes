import pandas as pd
import networkx as nx
import graphSolver as GS
import connectedNodes as CN
import miningValue as MV
import revenueValue as RV
import storageValue as SV

df = pd.read_csv('./data/fnSiteInfo.csv')

G = nx.Graph()

# Add nodes from the 'node name' column
for _, row in df.iterrows():
    node_attributes = {
        'FNSite': int(row['FNSite']),
        'Mirinium': int(row['Mirinium']),
        'Revenue': int(row['Revenue']),
        'Probe': "Revenue5"
    }
    G.add_node(row['FNSite'], **node_attributes)

# Add edges from the list of connected nodes
for _, row in df.iterrows():
    connected_nodes = row['Connections'].strip('[]').split(',')
    for node in connected_nodes:
        G.add_edge(row['FNSite'], int(node.strip()))

dfProbes = pd.read_csv('./data/probeInfo.csv')

GS.simulatedAnnealing(G,df,dfProbes,1000,50,10,50000,0.99,10000)