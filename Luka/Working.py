import pandas as pd
import networkx as nx
from community import best_partition, modularity
from sklearn.metrics.cluster import normalized_mutual_info_score
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog

class NetworkAnalysisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Network Analysis GUI")

        # Create text widget for displaying conductance values
        self.text = tk.Text(self.master)
        self.text.pack()

        # Create menu bar
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        # Create "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Edge CSV",
                              command=self.load_edge_file)
        file_menu.add_command(label="Load Node CSV",
                              command=self.load_node_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create "Analysis" menu
        analysis_menu = tk.Menu(menubar, tearoff=0)
        analysis_menu.add_command(
            label="Apply Louvain Algorithm and Visualize Graph", command=self.visualize_graph)
        analysis_menu.add_command(
            label="Calculate Conductance Values", command=self.calculate_and_display_conductance)
        menubar.add_cascade(label="Analysis", menu=analysis_menu)

        # Create empty graph and node/edge dataframes
        self.graph = nx.Graph()
        self.node_df = pd.DataFrame()
        self.edge_df = pd.DataFrame()

        # Set up canvas for graph visualization
        self.figure = plt.figure(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def load_edge_file(self):
        edge_file_path = filedialog.askopenfilename()
        self.edge_df = pd.read_csv(edge_file_path)
        self.update_graph()

    def load_node_file(self):
        node_file_path = filedialog.askopenfilename()
        self.node_df = pd.read_csv(node_file_path)
        self.update_graph()

    def update_graph(self):
        # Clear existing graph
        self.graph = nx.Graph()

        # Add nodes to graph
        self.graph.add_nodes_from(self.node_df["ID"])

        # Add edges to graph
        self.graph.add_edges_from(
            self.edge_df[["Source", "Target"]].values.tolist())

    def visualize_graph(self):
        # Apply Louvain algorithm to graph
        partition = best_partition(self.graph)
        mod = modularity(partition, self.graph)

        # Create color map for nodes based on Louvain partition
        color_map = [partition.get(node) for node in self.graph.nodes()]
        cmap = plt.cm.get_cmap('Set1', max(color_map) + 1)
        node_colors = [cmap(i) for i in color_map]

        # Draw graph with node colors
        nx.draw(self.graph, with_labels=True, node_color=node_colors)

        # Refresh canvas with updated graph
        self.canvas.draw()


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
                        return 0
                    else:
                        return Eoc / Ec

        conductance_values = []
        for community in set(partition.values()):
            community_nodes = [
                node for node in partition.keys() if partition[node] == community]
            conductance_values.append(conductance(G, community_nodes))
        return conductance_values

    def calculate_and_display_conductance(self):
        # Create graph from edge dataframe
        self.G = nx.from_pandas_edgelist(
            self.edge_df, source='Source', target='Target', create_using=nx.MultiGraph())

        # Apply Louvain algorithm to graph
        self.partition = best_partition(self.G)

        # Calculate conductance values for each community
        self.conductance_values = self.calculate_conductance(
            self.G, self.partition)

        # Clear the text widget
        self.text.delete("1.0", tk.END)

        # Print conductance values in text widget
        for i, conductance_value in enumerate(self.conductance_values):
            self.text.insert(tk.END, f"Community {i}: {conductance_value}\n")


root = tk.Tk()
gui = NetworkAnalysisGUI(root)
root.mainloop()
