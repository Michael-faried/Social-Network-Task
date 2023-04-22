import pandas as pd
import networkx as nx
from community import best_partition, modularity
from sklearn.metrics.cluster import normalized_mutual_info_score
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog


class NetworkAnalysisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Network Analysis GUI")

        # Create buttons for loading edge and node CSV files
        self.edge_button = tk.Button(master, text="Load Edge CSV", command=self.load_edge_file)
        self.edge_button.pack()

        self.node_button = tk.Button(master, text="Load Node CSV", command=self.load_node_file)
        self.node_button.pack()

        # Create button for applying Louvain algorithm and visualizing the network graph
        self.visualize_button = tk.Button(master, text="Apply Louvain Algorithm and Visualize Graph", command=self.visualize_graph)
        self.visualize_button.pack()

    def load_edge_file(self):
        # Open file dialog to select edge CSV file
        edge_filepath = filedialog.askopenfilename(title="Select Edge CSV File")

        # Load edge CSV file into pandas dataframe
        self.edge_df = pd.read_csv(edge_filepath)

    def load_node_file(self):
        # Open file dialog to select node CSV file
        node_filepath = filedialog.askopenfilename(title="Select Node CSV File")

        # Load node CSV file into pandas dataframe
        self.node_df = pd.read_csv(node_filepath)

    def calculate_conductance(self, G, partition):
        """Calculates the conductance of each community 
        and returns the conductance values for each community."""
        def conductance(G, community):
            Eoc = 0
            Ec = 0
            for node in community:
                neighbors = set(G.neighbors(node))
                for neighbor in neighbors:
                    if neighbor not in community:
                        if G.has_edge(node, neighbor):
                            Eoc += G[node][neighbor]['weight'] if G.is_directed() else 1 
                            # it adds the weight of the edge (or 1 if the graph is unweighted) to Eoc.
                    else:
                        Ec += G[node][neighbor]['weight'] if G.is_directed() else 1
                        # it adds the weight of the edge (or 1 if the graph is unweighted) to Ec.
            if Ec == 0:
                return 1
            else:
                return 2 * Eoc / (2 * Ec + Eoc)

        communities = {c: [] for c in set(partition.values())}
        for node, community in partition.items():
            communities[community].append(node)

        conductance_values = {f"community {c} : conductance": conductance(G, communities[c]) for c in communities}

        # Return the conductance values for each community
        return conductance_values

    def visualize_graph(self):
        # Create network graph from edge dataframe
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target")

        # Partition nodes into communities using Louvain algorithm
        partition = best_partition(G)

        # Calculate conductance values for each community
        conductance_values = self.calculate_conductance(G, partition)

        # Draw network graph with nodes colored by community
        pos = nx.spring_layout(G)
        cmap = plt.cm.tab20
        node_colors = [partition[node] for node in G.nodes()]
        node_sizes = [G.degree(node) * 10 for node in G.nodes()]
        nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap)
        nx.draw_networkx_edges(G, pos)
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=5)
        plt.title('Louvain algorithm')
        plt.colorbar(mappable=plt.cm.ScalarMappable(cmap=cmap), label="Community")
        plt.axis('off')

        # Display conductance values for each community
        conductance_text = ''
        for community, conductance in conductance_values.items():
            conductance_text += f"{community} = {conductance:.4f}\n"
        conductance_label = tk.Label(self.master, text=conductance_text)
        conductance_label.pack()

        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = NetworkAnalysisGUI(root)
    root.mainloop()