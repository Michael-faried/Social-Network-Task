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

    def load_edge_file(self):
        # Open file dialog to select edge CSV file
        edge_filepath = filedialog.askopenfilename(
            title="Select Edge CSV File")

        # Load edge CSV file into pandas dataframe
        self.edge_df = pd.read_csv(edge_filepath)

    def load_node_file(self):
        # Open file dialog to select node CSV file
        node_filepath = filedialog.askopenfilename(
            title="Select Node CSV File")

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

        # Display conductance values in new window
        conductance_window = tk.Toplevel(self.master)
        conductance_window.title("Conductance Values")

        for i, conductance_value in enumerate(self.conductance_values):
            label = tk.Label(conductance_window,
                             text=f"Community {i}: {conductance_value}")
            label.pack()

    def visualize_graph(self):
        # Create graph from edge dataframe
        self.G = nx.from_pandas_edgelist(
            self.edge_df, source='Source', target='Target', create_using=nx.MultiGraph())

        # Apply Louvain algorithm to graph
        self.partition = best_partition(self.G)

        # Create figure and axes for graph visualization
        fig, ax = plt.subplots(figsize=(8, 8))

        # Create layout for graph visualization
        pos = nx.spring_layout(self.G)

        # Draw nodes and edges
        nx.draw_networkx_nodes(self.G, pos, node_size=400,
                               cmap=plt.cm.RdYlBu, node_color=list(self.partition.values()))
        nx.draw_networkx_edges(self.G, pos)

        # Add node labels
        node_labels = dict(zip(self.node_df['ID'], self.node_df['Class']))
        nx.draw_networkx_labels(self.G, pos, labels=node_labels)

        # Add graph title
        ax.set_title("Graph Visualization")

        # Add legend for node colors
        nodes = self.G.nodes()
        sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlBu, norm=plt.Normalize(
            vmin=min(nodes), vmax=max(nodes)))
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.set_label('Community')

        # Display graph visualization in new window
        graph_window = tk.Toplevel(self.master)
        graph_window.title("Graph Visualization")
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()


root = tk.Tk()
gui = NetworkAnalysisGUI(root)
root.mainloop()
