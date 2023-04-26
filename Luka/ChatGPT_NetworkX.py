import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman, modularity
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
from networkx.algorithms.centrality import degree_centrality, betweenness_centrality, closeness_centrality

################################## Response 1: The Whole Code ##################################

# Create a graph object and add nodes and edges
G = nx.Graph()
G.add_nodes_from(nodes_data.to_dict("records"))
G.add_edges_from(edges_data.to_dict("records"))

# Community detection using Girvan Newman algorithm
communities = girvan_newman(G)

# Evaluate community detection using modularity
mod = modularity(G, communities)
print("Modularity:", mod)

# Link analysis using PageRank algorithm
pr = pagerank(G)
print("PageRank:", pr)

# Filtering nodes based on centrality measures
dc = degree_centrality(G)
bc = betweenness_centrality(G)
cc = closeness_centrality(G)
filtered_nodes = [n for n in G.nodes() if dc[n] > 0.2 and bc[n] > 0.1 and cc[n] > 0.3]
print("Filtered Nodes:", filtered_nodes)

# Adjusting nodes and edges based on calculated metrics
for n in G.nodes():
    G.nodes[n]["size"] = dc[n] * 100
for u, v in G.edges():
    G[u][v]["weight"] = pr[u] + pr[v]

# Basic network structure visualization
pos = nx.spring_layout(G)
node_sizes = [G.nodes[n]["size"] for n in G.nodes()]
edge_weights = [G[u][v]["weight"] for u, v in G.edges()]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes)
nx.draw_networkx_edges(G, pos, width=edge_weights)
plt.show()

################################## Response 2: Reading Files ##################################
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read nodes data from CSV file
nodes_df = pd.read_csv("nodes.csv")

# Read edges data from CSV file
edges_df = pd.read_csv("edges.csv")

# Create a graph object and add nodes and edges
G = nx.Graph()
for _, row in nodes_df.iterrows():
    G.add_node(row["node_id"], **row.to_dict())
for _, row in edges_df.iterrows():
    G.add_edge(row["source"], row["target"], **row.to_dict())

# Visualize the graph
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos=pos)
plt.show()