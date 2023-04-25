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


        text_label = tk.Label(button_frame, text=" Apply Louvain Algorithm & Visualize Graph ", font=("TkDefaultFont", 12,"bold"))
        text_label.pack(pady=(20,0),padx=10)
        # Create button for applying Louvain algorithm and visualizing the network graph
        self.visualize_button = tk.Button(button_frame, text=" Louvain Algorithm", command=self.visualize_graph)
        self.visualize_button.pack(pady=10, padx=10, anchor='center')


        text_label = tk.Label(button_frame, text=" Community detection evaluations ", font=("TkDefaultFont", 12,"bold"))
        text_label.pack(pady=(15,0),padx=10)
        # Create button for calculating and displaying conductance values
        self.conductance_button = tk.Button(button_frame, text=" Conductance Values", command=self.calculate_and_display_conductance,width=20)
        self.conductance_button.pack(pady=10, anchor='center')

        self.Modularity_Button = tk.Button(button_frame, text=" Modularity", command=self.calculate_modularity,width=20)
        self.Modularity_Button.pack(pady=5, anchor='center')

        self.NMI_Button = tk.Button(button_frame, text=" NMI VALUE", command=self.calculate_nmi,width=20)
        self.NMI_Button.pack(pady=5, anchor='center')

        self.CC_Button = tk.Button(button_frame, text=" Community Coverage", command=self.calculate_community_coverage,width=20)
        self.CC_Button.pack(pady=5, anchor='center')


        # # Create a label for the text
        text_label = tk.Label(button_frame, text="Filter Nodes Based on Centrality", font=("TkDefaultFont", 12,"bold"))
        text_label.pack(pady=(15,0),padx=10)
        self.filter_degree_centrality_btn = tk.Button(button_frame, text=" degree centrality", command=self.filter_degree_centrality)
        self.filter_degree_centrality_btn.pack(pady=5, padx=10, anchor='center')

        self.filter_Betweeness_centrality_btn = tk.Button(button_frame, text="  Betweeness centrality", command=self.filter_betweenness_centrality)
        self.filter_Betweeness_centrality_btn.pack(pady=5, padx=10, anchor='center')

        self.filter_eigenvector_centrality_btn = tk.Button(button_frame, text="  Eigenvector centrality", command=self.filter_betweenness_centrality)
        self.filter_eigenvector_centrality_btn.pack(pady=5, padx=10, anchor='center')

        self.filter_harmonic_centrality_btn = tk.Button(button_frame, text="  Harmonic centrality", command=self.filter_harmonic_centrality)
        self.filter_harmonic_centrality_btn.pack(pady=5, padx=10, anchor='center')

        self.filter_closeness_centrality_btn = tk.Button(button_frame, text="  Closeness centrality", command=self.filter_closeness_centrality)
        self.filter_closeness_centrality_btn.pack(pady=5, padx=10, anchor='center')



        text_label = tk.Label(button_frame, text=" link analysis technique ", font=("TkDefaultFont", 12,"bold"))
        text_label.pack(pady=(15,0))
        self.PageRank_Button = tk.Button(button_frame, text=" Nodes Page Rank ", command=self.calculate_pagerank)
        self.PageRank_Button.pack(pady=5, anchor='center')


        # Create frame for output text on the right
        output_frame = tk.Frame(master, width=200)
        output_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Create frame for edge and node buttons at top of output text panel
        button_frame_top = tk.Frame(output_frame)
        button_frame_top.pack(side=tk.TOP, pady=10)

        # Add edge and node buttons to top frame
        self.edge_button_top = tk.Button(button_frame_top, text="Load Edge CSV", command=self.load_edge_file)
        self.edge_button_top.pack(side=tk.LEFT, padx=5,pady=(20,10))

        self.node_button_top = tk.Button(button_frame_top, text="Load Node CSV", command=self.load_node_file)
        self.node_button_top.pack(side=tk.LEFT, padx=5,pady=(20,10))

        # Create text widget to display conductance values
        self.Text_Panal = tk.Text(output_frame, height=30, width=35)
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
        communities=list(nx.algorithms.community.greedy_modularity_communities(G))
        modularity=nx.algorithms.community.modularity(G,communities)

        # Delete existing text in the text widget
        self.Text_Panal.delete('1.0', tk.END)
        community ="Modularity "
        self.Text_Panal.insert(tk.END, "\n")
        # Display conductance values for each community in the text widget
        self.Text_Panal.insert(tk.END, "  "+f"{community} = {modularity:.4f}\n")




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
        self.Text_Panal.insert(tk.END, "          External evaluation      \n")
        self.Text_Panal.insert(tk.END,"  "+ f"{community} = {nmi:.4f}\n")

    def calculate_community_coverage(self):
        self.Text_Panal.delete('1.0', tk.END)
        """Calculates the coverage of each community and prints the result."""
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())
        partition = best_partition(G)

        communities = set(partition.values())
        self.Text_Panal.insert(tk.END, "Communities coverage Values : \n\n")
        for community_id in communities:
            community_nodes = [node for node in G.nodes() if partition[node] == community_id]
            internal_edges = G.subgraph(community_nodes).number_of_edges()
            total_edges = sum([G.degree(node) for node in community_nodes])
            coverage = internal_edges / total_edges
            self.Text_Panal.insert(tk.END, f" Community {  community_id} = {coverage:.4f}\n")

        # Delete existing text in the text widget


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
        self.Text_Panal.insert(tk.END," Community Conductance : \n \n")
        # Display conductance values for each community in the text widget
        for community, conductance in conductance_values.items():
            self.Text_Panal.insert(tk.END, f"{community} = {conductance:.4f}\n")


    def calculate_pagerank(self):
        """Calculates the PageRank score for each node in the graph and prints the result."""
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())
        pagerank = nx.pagerank(G)
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert(tk.END," Page Rank Nodes Values : \n \n")
        for node, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
            self.Text_Panal.insert(tk.END," Node "+ f"{node} = {score:.4f}\n")


    def visualize_graph(self):
        # Create network graph from edge dataframe
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.MultiGraph())

        # Partition nodes into communities using Louvain algorithm
        partition = best_partition(G)

        # Draw network graph with nodes colored by community
        pos = nx.spring_layout(G)
        cmap = plt.cm.tab20
        node_colors = [partition[node] for node in G.nodes()]
        node_sizes = [G.degree(node)/2 for node in G.nodes()]
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

    def filter_degree_centrality(self):
        # Create network graph from edge dataframe
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.MultiGraph())
        G = nx.Graph(G)

        # Compute degree centrality for each node and create a DataFrame to store the results
        degree_centrality = nx.degree_centrality(G)
        df = pd.DataFrame(index=G.nodes())
        df.index.name = 'Node ID'
        df['degree_centrality'] = pd.Series(degree_centrality).round(3)
        df = df.sort_values(by='degree_centrality', ascending=False)

        # Insert degree centrality values in the Text_Panal
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', df.to_string())

        # Generate visualization
        top_nodes = df.head(10)
        pos = nx.spring_layout(G)
        cmap = plt.cm.tab20
        red_nodes = top_nodes.index
        node_colors = ['red' if node in red_nodes else 'grey' for node in G.nodes()]
        node_sizes = [G.degree(node) * 3 if node in red_nodes else G.degree(node) for node in G.nodes()]
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        labels = {node: node for node in red_nodes}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
        plt.title('Top 10 Degree Centrality Nodes')
        plt.axis('off')

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    def filter_betweenness_centrality(self):
        # Create network graph from edge dataframe
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.MultiGraph())
        G = nx.Graph(G)

        # Compute degree centrality for each node and create a DataFrame to store the results
        betweenness_centrality = nx.betweenness_centrality(G)

        df = pd.DataFrame(index=G.nodes())
        df.index.name = 'Node ID'
        df['betweenness_centrality'] = pd.Series(betweenness_centrality).round(3)
        df = df.sort_values(by='betweenness_centrality', ascending=False)

        # Insert degree centrality values in the Text_Panal
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', df.to_string())

        # Generate visualization
        top_nodes = df.head(10)
        pos = nx.spring_layout(G)
        cmap = plt.cm.tab20
        red_nodes = top_nodes.index
        node_colors = ['red' if node in red_nodes else 'grey' for node in G.nodes()]
        node_sizes = [G.degree(node) * 3 if node in red_nodes else G.degree(node) for node in G.nodes()]
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        labels = {node: node for node in red_nodes}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
        plt.title('Top 10 Betweenness Centrality Nodes')
        plt.axis('off')

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    def filter_eigenvector_centrality(self):
        # Create network graph from edge dataframe
        G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.MultiGraph())
        G = nx.Graph(G)

        # Compute degree centrality for each node and create a DataFrame to store the results
        eigenvector_centrality = nx.eigenvector_centrality(G)

        df = pd.DataFrame(index=G.nodes())
        df.index.name = 'Node ID'
        df['eigenvector_centrality'] = pd.Series(eigenvector_centrality).round(3)
        df = df.sort_values(by='eigenvector_centrality', ascending=False)

        # Insert degree centrality values in the Text_Panal
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', df.to_string())

        # Generate visualization
        top_nodes = df.head(10)
        pos = nx.spring_layout(G)
        cmap = plt.cm.tab20
        red_nodes = top_nodes.index
        node_colors = ['red' if node in red_nodes else 'grey' for node in G.nodes()]
        node_sizes = [G.degree(node) * 3 if node in red_nodes else G.degree(node) for node in G.nodes()]
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        labels = {node: node for node in red_nodes}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
        plt.title('Top 10 Eigenvector Centrality Nodes')
        plt.axis('off')

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    def filter_harmonic_centrality(self):
            # Create network graph from edge dataframe
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.MultiGraph())
            G = nx.Graph(G)

            # Compute degree centrality for each node and create a DataFrame to store the results
            harmonic_centrality = nx.harmonic_centrality(G)

            df = pd.DataFrame(index=G.nodes())
            df.index.name = 'Node ID'
            df['harmonic_centrality'] = pd.Series(harmonic_centrality).round(4)
            df = df.sort_values(by='harmonic_centrality', ascending=False)

            # Insert degree centrality values in the Text_Panal
            self.Text_Panal.delete('1.0', tk.END)
            self.Text_Panal.insert('1.0', df.to_string())

            # Generate visualization
            top_nodes = df.head(10)
            pos = nx.spring_layout(G)
            cmap = plt.cm.tab20
            red_nodes = top_nodes.index
            node_colors = ['red' if node in red_nodes else 'grey' for node in G.nodes()]
            node_sizes = [G.degree(node) * 3 if node in red_nodes else G.degree(node) for node in G.nodes()]
            fig, ax = plt.subplots()
            nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)
            nx.draw_networkx_edges(G, pos, ax=ax)
            labels = {node: node for node in red_nodes}
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
            plt.title('Top 10 harmonic Centrality Nodes')
            plt.axis('off')

            # Embed the plot in the GUI using a canvas
            canvas = FigureCanvasTkAgg(fig, master=self.master)
            canvas.draw()
            canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)
 
    def filter_closeness_centrality(self):
            # Create network graph from edge dataframe
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.MultiGraph())
            G = nx.Graph(G)

            # Compute degree centrality for each node and create a DataFrame to store the results
            closeness_centrality = nx.closeness_centrality(G)

            df = pd.DataFrame(index=G.nodes())
            df.index.name = 'Node ID'
            df['closeness_centrality'] = pd.Series(closeness_centrality).round(3)
            df = df.sort_values(by='closeness_centrality', ascending=False)

            # Insert degree centrality values in the Text_Panal
            self.Text_Panal.delete('1.0', tk.END)
            self.Text_Panal.insert('1.0', df.to_string())

            # Generate visualization
            top_nodes = df.head(10)
            pos = nx.spring_layout(G)
            cmap = plt.cm.tab20
            red_nodes = top_nodes.index
            node_colors = ['red' if node in red_nodes else 'grey' for node in G.nodes()]
            node_sizes = [G.degree(node) * 3 if node in red_nodes else G.degree(node) for node in G.nodes()]
            fig, ax = plt.subplots()
            nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)
            nx.draw_networkx_edges(G, pos, ax=ax)
            labels = {node: node for node in red_nodes}
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
            plt.title('Top 10 closeness Centrality Nodes')
            plt.axis('off')

            # Embed the plot in the GUI using a canvas
            canvas = FigureCanvasTkAgg(fig, master=self.master)
            canvas.draw()
            canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)


root = tk.Tk()
root.geometry("1000x600")
gui = NetworkAnalysisGUI(root)
root.mainloop()


