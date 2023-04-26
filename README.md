# Mini Social Networks Analysis Tool

## Community Detection Algorithm:
### 1. Louvain Algorithm
A modularity-based algorithm for community detection in networks that optimizes the modularity score by iteratively moving nodes between communities to maximize modularity.

##Community Detection Evaluation:
### 1. Conductance (External)
A measure of the ratio of the number of edges that connect nodes within the community to the total number of edges incident on nodes in the community, used to evaluate the quality of community detection algorithms.
### 2. Modularity (Internal)
A measure of the degree of density of edges within a community compared to the density of edges between communities, used to evaluate the quality of community detection algorithms.
### 3. NMI (External)
A measure of the similarity between two clustering solutions, used to compare a clustering solution with a ground truth clustering or to evaluate the stability of different clustering algorithms.
### 4. Community Coverage (Internal)
A measure of the fraction of nodes in the network that are assigned to communities, used to evaluate the quality of community detection algorithms.

##Link Analysis Technique:
### 1. Page Rank
An algorithm that assigns a score to each node in a network based on the importance of its incoming links, with the assumption that important nodes will receive more incoming links.

##Filtering Nodes:
### 1. Degree Centrality
A measure of the number of edges incident on a node, used to identify highly connected nodes.
### 2. Closeness Centrality
A measure of the average shortest path length between a node and all other nodes in the network, used to identify nodes that are close to other nodes in the network.
### 3. Betweenness Centrality
A measure of the number of shortest paths between any two nodes in the network that pass through a given node, used to identify nodes that act as "bridges" between different parts of the network.
### 4. Harmonic Centrality
A measure of the sum of the reciprocal of the shortest path length between a node and all other nodes in the network, used to identify nodes that are central to communication flow in the network.
### 5. Eigenvector Centrality
A measure of the importance of a node based on the importance of its neighbors, used to identify nodes that are connected to other important nodes in the network.
