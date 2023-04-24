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

        # Create frame for buttons on the left
        button_frame = tk.Frame(master, width=200)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create button for applying Louvain algorithm and visualizing the network graph
        self.visualize_button = tk.Button(button_frame, text="Louvain Algorithm 'Visualize Graph'", command=self.visualize_graph)
        self.visualize_button.pack(pady=10, padx=10, anchor='center')

        # Create button for calculating and displaying conductance values
        self.conductance_button = tk.Button(button_frame, text="Calculate Conductance Values", command=self.calculate_and_display_conductance)
        self.conductance_button.pack(pady=10, anchor='center')
        self.Modularity_Button = tk.Button(button_frame, text="Modularity", command=self.calculate_modularity)
        self.Modularity_Button.pack(pady=10, anchor='center')
        self.Modularity_Button = tk.Button(button_frame, text="NMI VALUE", command=self.calculate_nmi)
        self.Modularity_Button.pack(pady=10, anchor='center')
        self.Modularity_Button = tk.Button(button_frame, text="Community Coverage", command=self.calculate_community_coverage)
        self.Modularity_Button.pack(pady=10, anchor='center')

        # Create frame for output text on the right
        output_frame = tk.Frame(master, width=200)
        output_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Create frame for edge and node buttons at top of output text panel
        button_frame_top = tk.Frame(output_frame)
        button_frame_top.pack(side=tk.TOP, pady=10)

        # Add edge and node buttons to top frame
        self.edge_button_top = tk.Button(button_frame_top, text="Load Edge CSV", command=self.load_edge_file)
        self.edge_button_top.pack(side=tk.LEFT, padx=5)

        self.node_button_top = tk.Button(button_frame_top, text="Load Node CSV", command=self.load_node_file)
        self.node_button_top.pack(side=tk.LEFT, padx=5)

        # Create text widget to display conductance values
        self.Text_Panal = tk.Text(output_frame, height=20, width=35)
        self.Text_Panal.pack(pady=10, anchor='center')
        
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

# 2- Modularity internal evaluation
    def calculate_modularity(self):
        """Calculates the modularity of the detected communities and prints the result."""
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())
        partition = best_partition(G)
        modularity_score = modularity(partition, G)
        # Delete existing text in the text widget
        self.Text_Panal.delete('1.0', tk.END)
        community ="Modularity "
        # Display conductance values for each community in the text widget
        self.Text_Panal.insert(tk.END, f"{community} = {modularity_score:.4f}\n")


# 4- Calculate NMI External Evaluation
    def calculate_nmi(self):
        """Loads the ground truth communities from a CSV file, calculates the NMI between the detected communities
        and the ground truth communities, and prints the result."""
        # Load ground truth communities from CSV file
        ground_truth_file =self.node_df
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())
        partition = best_partition(G)
        ground_truth_dict = dict(zip(ground_truth_file['ID'], ground_truth_file['Class']))
        # Calculate NMI between detected communities and ground truth communities
        nmi = normalized_mutual_info_score(list(ground_truth_dict.values()), list(partition.values()))
        # Delete existing text in the text widget
        self.Text_Panal.delete('1.0', tk.END)
        community ="NMI VALUE "
        # Display conductance values for each community in the text widget
        self.Text_Panal.insert(tk.END, f"{community} = {nmi:.4f}\n")

    def calculate_community_coverage(self):
        self.Text_Panal.delete('1.0', tk.END)
        """Calculates the coverage of each community and prints the result."""
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())
        partition = best_partition(G)

        communities = set(partition.values())
        for community_id in communities:
            community_nodes = [node for node in G.nodes() if partition[node] == community_id]
            internal_edges = G.subgraph(community_nodes).number_of_edges()
            total_edges = sum([G.degree(node) for node in community_nodes])
            coverage = internal_edges / total_edges
            self.Text_Panal.insert(tk.END, f" Community {  community_id} = {coverage:.4f}\n")

        # Delete existing text in the text widget
        # Display conductance values for each community in the text widget


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

        conductance_values = {f"community {c} : conductance": conductance(G, community) for c, community in communities.items()}
        return conductance_values

    def calculate_and_display_conductance(self):
        # Create network graph from edge dataframe
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())

        # Partition nodes into communities using Louvain algorithm
        partition = best_partition(G)

        # Calculate conductance values for each community
        conductance_values = self.calculate_conductance(G, partition)

        # Delete existing text in the text widget
        self.Text_Panal.delete('1.0', tk.END)

        # Display conductance values for each community in the text widget
        for community, conductance in conductance_values.items():
            self.Text_Panal.insert(tk.END, f"{community} = {conductance:.4f}\n")


    def visualize_graph(self):
        # Create network graph from edge dataframe
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())

        # Partition nodes into communities using Louvain algorithm
        partition = best_partition(G)

        # Calculate conductance values for each community
        conductance_values = self.calculate_conductance(G, partition)

        # Draw network graph with nodes colored by community
        pos = nx.spring_layout(G)
        cmap = plt.cm.tab20
        node_colors = [partition[node] for node in G.nodes()]
        node_sizes = [G.degree(node) for node in G.nodes()]
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=5, ax=ax)
        plt.title('Louvain algorithm')
        plt.colorbar(mappable=plt.cm.ScalarMappable(cmap=cmap), label="Community")
        plt.axis('off')

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

root = tk.Tk()
root.geometry("1000x600")
gui = NetworkAnalysisGUI(root)
root.mainloop()


