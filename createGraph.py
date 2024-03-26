import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

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


test = 412
# Example: Accessing attributes of a node
print("Attributes of node:", G.nodes[test])
print("Mirinium value of node:", G.nodes[test]['Mirinium'])
print("Revenue value of node:", G.nodes[test]['Revenue'])
print("Edges:", G.edges(test))

nx.draw(G, nx.spring_layout(G, k=0.15,iterations=20), with_labels=True, node_size=500, font_size=10)
plt.show()