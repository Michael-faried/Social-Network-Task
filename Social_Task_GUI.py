import pandas as pd
import networkx as nx
from community import best_partition, modularity
from sklearn.metrics.cluster import normalized_mutual_info_score
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from matplotlib.figure import Figure

global selected_option
class NetworkAnalysisGUI:
    def __init__(self, master):
        self.master = master
        master.title("Network Analysis GUI")

        # Create frame for buttons on the left
        button_frame = tk.Frame(master, width=200,background="#58D68D")
        button_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        style = ttk.Style()
        style.configure("Custom.TButton", background="#1877FF", foreground="black",
                         font=("Arial", 11, "bold"), padding=5, borderwidth=3, relief="raised",focuscolor='red')
        style.configure('Custom.TButton', borderradius=50)

        style2 = ttk.Style()
        style2.configure("1Custom.TButton", background="#FFFF18", foreground="black",
                         font=("Arial", 13, "bold"), padding=5, borderwidth=3, relief="raised")

        text_label = tk.Label(button_frame, text="Apply Louvain Algorithm \n Visualize Graph ", font=("TkDefaultFont", 14,"bold"),background="#58D68D")
        text_label.pack(pady=(15,0),padx=10)
        self.visualize_button =  ttk.Button(button_frame, style="1Custom.TButton",text=" Louvain Algorithm", command= lambda:self.visualize_graph(False,False,selected_option),width=25)
        self.visualize_button.pack(pady=5, padx=10, anchor='center')

        text_label = tk.Label(button_frame, text=" Adjusting Nodes and Edges \n (Based on calculated metrics) ", font=("TkDefaultFont", 13,"bold"),background="#58D68D")
        text_label.pack(pady=(15,0),padx=10)
        self.visualize_button =  ttk.Button(button_frame, style="1Custom.TButton",text="Adjusting Graph", command=lambda: self.visualize_graph(True,True,selected_option),width=25)
        self.visualize_button.pack(pady=5, padx=10, anchor='center')


        text_label = tk.Label(button_frame, text=" Community detection evaluations ", font=("TkDefaultFont", 13,"bold"),background="#58D68D")
        text_label.pack(pady=(10,5),padx=10)
        # Create button for calculating and displaying conductance values
        self.conductance_button = ttk.Button(button_frame, style="Custom.TButton", text=" Conductance Values",
                                             command=lambda: self.calculate_and_display_conductance(selected_option), width=20)
        self.conductance_button.pack(pady=3, anchor='center')

        self.Modularity_Button = ttk.Button(button_frame,style="Custom.TButton", text=" Modularity", command=lambda: self.calculate_modularity(selected_option),width=20)
        self.Modularity_Button.pack(pady=3, anchor='center')

        self.NMI_Button = ttk.Button(button_frame, style="Custom.TButton", text=" NMI VALUE",
                                     command=lambda: self.calculate_nmi(selected_option), width=20)
        self.NMI_Button.pack(pady=3, anchor='center')

        self.CC_Button = ttk.Button(button_frame, style="Custom.TButton", text=" Community Coverage",
                                    command=lambda: self.calculate_community_coverage(selected_option), width=20)
        self.CC_Button.pack(pady=3, anchor='center')


        # # Create a label for the text
        text_label = tk.Label(button_frame, text="Filter Nodes Based on Centrality", font=("TkDefaultFont", 13,"bold"),background="#58D68D")
        text_label.pack(pady=(12,0),padx=10)
        self.filter_degree_centrality_btn = ttk.Button(
            button_frame, style="Custom.TButton", text=" degree centrality", command=lambda: self.filter_degree_centrality(selected_option), width=22)
        self.filter_degree_centrality_btn.pack(pady=3, padx=10, anchor='center')

        self.filter_closeness_centrality_btn = ttk.Button(
            button_frame, style="Custom.TButton", text="  Closeness centrality", command=lambda: self.filter_closeness_centrality(selected_option), width=22)
        self.filter_closeness_centrality_btn.pack(pady=3, padx=10, anchor='center')

        self.filter_Betweeness_centrality_btn = ttk.Button(
            button_frame, style="Custom.TButton", text="  Betweeness centrality", command=lambda: self.filter_betweenness_centrality(selected_option), width=22)
        self.filter_Betweeness_centrality_btn.pack(pady=3, padx=10, anchor='center')

        self.filter_eigenvector_centrality_btn = ttk.Button(
            button_frame, style="Custom.TButton", text="  Eigenvector centrality", command=lambda: self.filter_eigenvector_centrality(selected_option), width=22)
        self.filter_eigenvector_centrality_btn.pack(pady=3, padx=10, anchor='center')

        self.filter_harmonic_centrality_btn = ttk.Button(
            button_frame, style="Custom.TButton", text="  Harmonic centrality", command=lambda: self.filter_harmonic_centrality(selected_option), width=22)
        self.filter_harmonic_centrality_btn.pack(pady=3, padx=10, anchor='center')



        text_label = tk.Label(button_frame, text=" link analysis technique ", font=("TkDefaultFont", 13,"bold"),background="#58D68D")
        text_label.pack(pady=(15,0))
        self.PageRank_Button = ttk.Button(button_frame, style="Custom.TButton",
                                          text=" Nodes Page Rank ", command=lambda: self.calculate_pagerank(selected_option))
        self.PageRank_Button.pack(pady=5, anchor='center')


        # Create frame for output text on the right
        output_frame = tk.Frame(master, width=200,background="#58D68D")
        output_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Create frame for edge and node buttons at top of output text panel
        button_frame_top = tk.Frame(output_frame,background="#58D68D")
        button_frame_top.pack(side=tk.TOP, pady=10)
        text_label = tk.Label(button_frame_top, text=" Load CSV Data ", font=("TkDefaultFont", 14,"bold"),background="#58D68D")
        text_label.pack(pady=(10,0),padx=10)
        # Add edge and node buttons to top frame
        self.edge_button_top = ttk.Button(button_frame_top,style="1Custom.TButton", text="Load Edge CSV", command=self.load_edge_file)
        self.edge_button_top.pack(side=tk.LEFT, padx=5,pady=(10,2))

        self.node_button_top = ttk.Button(button_frame_top,style="1Custom.TButton", text="Load Node CSV", command=self.load_node_file)
        self.node_button_top.pack(side=tk.LEFT, padx=5,pady=(10,2))

        options = ['Direct Graph', 'Undirect Graph']
        # create a StringVar to hold the selected option
        selected_option = tk.StringVar()
        # set the default placeholder text
        selected_option.set('Select Graph Type')

        def on_click(event):
            # remove the placeholder text when the user clicks on the combo box
            if selected_option.get() == 'Select Graph Type':
                selected_option.set('')


        # create the ComboBox
        combo_box = ttk.Combobox(
            output_frame, textvariable=selected_option, values=options, state='readonly')
        combo_box.pack(pady=(0, 0))
        
        # add event binding to remove the placeholder text when the user clicks on the combo box
        combo_box.bind('<FocusIn>', on_click)
        

        # Create text widget to display conductance values
        self.Text_Panal = tk.Text(output_frame, height=30, width=35,background="#D5F5E3")
        self.Text_Panal.pack(pady=10, anchor='center')

        # Create input field to get user input
        text_label = tk.Label(output_frame, text=" Filter Nodes Based on value greater \n than Specific Value ", font=("TkDefaultFont", 13,"bold"),background="#58D68D",foreground="#FF1818")
        text_label.pack(pady=(0,0),padx=10)
        self.user_input = tk.StringVar()
        self.input_field = tk.Entry( output_frame, textvariable=self.user_input, width=20, font=('Arial', 14), bg='#F5F5F5', fg='#333333', bd=2, relief=tk.GROOVE,justify="center")
        self.input_field.pack(pady=(5, 0), padx=(10, 10), anchor='center')
        # Create button to clear the input field

        style = ttk.Style()
        style.configure("2Custom.TButton", background="red", foreground="black",
                         font=("Arial", 11, "bold"), padding=5, borderwidth=3, relief="raised")

        self.clear_button = ttk.Button(output_frame,style="2Custom.TButton" ,text="Clear", command=self.clear_input_field)
        self.clear_button.pack(side=tk.TOP,pady=7)

    # Define function to clear the input field
    def clear_input_field(self):
        self.input_field.delete(0, tk.END)

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
    def calculate_modularity(self, selected_option):
        """Calculates the modularity of the detected communities and prints the result."""
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.Graph())

        communities=list(nx.algorithms.community.greedy_modularity_communities(G))
        modularity=nx.algorithms.community.modularity(G,communities)

        # Delete existing text in the text widget
        self.Text_Panal.delete('1.0', tk.END)
        community ="Modularity "
        self.Text_Panal.insert(tk.END, "          Internal evaluation      \n")
        # Display conductance values for each community in the text widget
        self.Text_Panal.insert(tk.END, "  "+f"{community} = {modularity:.5f}\n")


# 4- Calculate NMI External Evaluation
    def calculate_nmi(self, selected_option):
        """Loads the ground truth communities from a CSV file, calculates the NMI between the detected communities
        and the ground truth communities, and prints the result."""
        # Load ground truth communities from CSV file
        ground_truth_file =self.node_df
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target",create_using=nx.Graph())
        partition = best_partition(G)

        ground_truth_dict = dict(zip(ground_truth_file['ID'], ground_truth_file['Class']))
        # Calculate NMI between detected communities and ground truth communities
        #print(list(set(partition.values())))

        # Convert ground truth values format to lists of integers
        unique_labels = list(set(ground_truth_dict.values()))
        labels_map = {label: i for i, label in enumerate(unique_labels)}
        ground_truth_communites = [labels_map[ground_truth_dict[node]] for node in G.nodes()]
        #print(list(set(ground_truth_communites)))

        nmi = normalized_mutual_info_score(ground_truth_communites, list(partition.values()))
        # Delete existing text in the text widget
        self.Text_Panal.delete('1.0', tk.END)
        community ="NMI VALUE "
        self.Text_Panal.insert(tk.END, "          External evaluation      \n")
        self.Text_Panal.insert(tk.END,"  "+ f"{community} = {nmi:.4f}\n")

    def calculate_community_coverage(self, selected_option):
        self.Text_Panal.delete('1.0', tk.END)
        """Calculates the coverage of each community and prints the result."""
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())        

        partition = best_partition(G.to_undirected())

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
                            if G[node][neighbor].get('weight') is not None:
                                Eoc += G[node][neighbor]['weight']
                            else:
                                Eoc += 1
                    else:
                        if G.has_edge(node, neighbor):
                            if G[node][neighbor].get('weight') is not None:
                                Ec += G[node][neighbor]['weight']
                            else:
                                Ec += 1
            if Ec == 0:
                return 1
            else:
                return 2 * Eoc / (2 * Ec + Eoc)
        communities = {c: [] for c in set(partition.values())}
        for node, community in partition.items():
            communities[community].append(node)

        conductance_values = {f"community {c} : conductance": conductance(G, community) for c, community in communities.items()}
        return conductance_values

    def calculate_and_display_conductance(self, selected_option):
        # Create network graph from edge dataframe
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.Graph())
        # Partition nodes into communities using Louvain algorithm
        partition = best_partition(G.to_undirected())

        # Calculate conductance values for each community
        conductance_values = self.calculate_conductance(G, partition)

    # Calculate average conductance across all communities
        avg_conductance = sum(conductance_values.values()) / len(conductance_values)

        # Delete existing text in the text widget
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert(tk.END," Community Conductance : \n \n")
        # Display conductance values for each community in the text widget
        for community, conductance in conductance_values.items():
            self.Text_Panal.insert(tk.END, f"{community} = {conductance:.4f}\n")
    # Display average conductance across all communities
        self.Text_Panal.insert(tk.END, f"\n Average Conductance = {avg_conductance:.4f}\n")
    

    def calculate_pagerank(self, selected_option):
        """Calculates the PageRank score for each node in the graph and prints the result."""
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())        

        pagerank = nx.pagerank(G)
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert(tk.END," Page Rank Nodes Values : \n \n")
        for node, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True):
            self.Text_Panal.insert(tk.END," Node "+ f"{node} = {score:.4f}\n")


    def visualize_graph(self, apply_nodeSize=False, apply_edges_weight=False, selected_option=""):
        # Create network graph from edge dataframe
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())


        partition = best_partition(G.to_undirected())
        edge_weights = self.edge_df.groupby(["Source", "Target"]).size().to_dict()

        # Draw network graph with nodes colored by community
        pos = nx.spring_layout(G)
        cmap = plt.cm.tab20
        node_colors = [partition[node] for node in G.nodes()]

        node_sizes = 250  # default value of node sizes
        if apply_nodeSize:  # if the user wants to apply the node sizes
            self.Text_Panal.delete('1.0', tk.END)
            degree_dict = {node: G.degree(node) for node in G}
            sorted_degrees = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
            for node, degree in sorted_degrees:
                self.Text_Panal.insert(tk.END, f"Node {node} : {degree}\n")

            if len(G.nodes()) <= 50:
                node_sizes = [G.degree(node) * 100 for node in G.nodes()]
            else:
                node_sizes = [G.degree(node) *5 for node in G.nodes()]
            

        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)

        if len(G.edges()) <= 100:
            w = 1
            scalling_factor = 1
        else:
            w = 0.1
            scalling_factor = 500


        if apply_edges_weight:
            if 'Weight' in self.edge_df.columns:
                edges = nx.draw_networkx_edges(G, pos, ax=ax, width=self.edge_df['Weight'] / 5000, edge_color='black')
            else:
                edges = nx.draw_networkx_edges(G, pos, ax=ax, width=[edge_weights.get((u, v), w) / scalling_factor for u, v in G.edges()], edge_color='black')
        else:  # for louvian Button
            edges = nx.draw_networkx_edges(G, pos, ax=ax, width=0.1, edge_color='gray')


        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=6, ax=ax)

        if selected_option == 'Direct Graph':
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weights, label_pos=0.3, font_size=6, ax=ax)

        plt.title('Louvain algorithm')
        plt.colorbar(mappable=plt.cm.ScalarMappable(cmap=cmap), label="Community")
        plt.axis('off')

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.497, rely=0.5, anchor=tk.CENTER, width=870, height=700)

    def filter_degree_centrality(self, selected_option):
        # Create network graph from edge dataframe
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())  

        # Compute degree centrality for each node and create a DataFrame to store the results
        degree_centrality = nx.degree_centrality(G)
        df = pd.DataFrame(index=G.nodes())
        df.index.name = 'Node ID'
        df['degree_centrality'] = pd.Series(degree_centrality).round(3)
        df = df.sort_values(by='degree_centrality', ascending=False)
        user_input = self.user_input.get()
        if not user_input:
            user_input = 0
        else:
            user_input = float(user_input)

        # Filter nodes based on degree centrality
        filtered_nodes = sorted([node for node in G.nodes() if degree_centrality[node] >= user_input],
                    key=lambda node: degree_centrality[node], reverse=True)
        # Create a new graph with only the filtered nodes
        filtered_G = G.subgraph(filtered_nodes)

        # Set node color and size for filtered nodes
        cmap = plt.cm.tab20
        node_colors = '#FC3131'
        if (len(G.nodes()) <= 100):
            node_sizes = 1000
        else:
            node_sizes = 250

        # Generate visualization
        pos = nx.spring_layout(filtered_G)
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(filtered_G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax )
        if (selected_option.get() == 'Direct Graph'):
            for u, v, data in filtered_G.edges(data=True):
                ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", color="Black"))
        else:
            nx.draw_networkx_edges(filtered_G, pos, ax=ax)

        labels = {node: node for node in filtered_nodes}
        nx.draw_networkx_labels(filtered_G, pos, labels=labels, font_size=7, ax=ax)
        plt.title(f'     Degree Centrality Greater {user_input}')
        plt.axis('off')

        # Insert degree centrality values in the Text_Panal
        filtered_df = df.loc[filtered_nodes]
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', filtered_df.to_string())

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    def filter_betweenness_centrality(self, selected_option):
        # Create network graph from edge dataframe
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())        

        # Compute degree centrality for each node and create a DataFrame to store the results
        betweenness_centrality = nx.betweenness_centrality(G)

        df = pd.DataFrame(index=G.nodes())
        df.index.name = 'Node ID'
        df['betweenness_centrality'] = pd.Series(betweenness_centrality).round(3)
        df = df.sort_values(by='betweenness_centrality', ascending=False)
        user_input = self.user_input.get()
        if not user_input:
            user_input = 0
        else:
            user_input = float(user_input)

        # Filter nodes based on degree centrality
        filtered_nodes = sorted([node for node in G.nodes() if betweenness_centrality[node] >= user_input],
                    key=lambda node: betweenness_centrality[node], reverse=True)
        # Create a new graph with only the filtered nodes
        filtered_G = G.subgraph(filtered_nodes)

        # Set node color and size for filtered nodes
        cmap = plt.cm.tab20
        node_colors = '#F7DC6F'
        if (len(G.nodes()) <= 100):
            node_sizes = 1000
        else:
            node_sizes = 250
        # Generate visualization
        pos = nx.spring_layout(filtered_G)
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(filtered_G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax)
        if (selected_option.get() == 'Direct Graph'):
            for u, v, data in filtered_G.edges(data=True):
                ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", color="Black"))
        else:
            nx.draw_networkx_edges(filtered_G, pos, ax=ax)
        labels = {node: node for node in filtered_nodes}
        nx.draw_networkx_labels(filtered_G, pos, labels=labels, font_size=7, ax=ax)
        plt.title(f'     Betweeness Centrality Greater {user_input}')
        plt.axis('off')

        # Insert degree centrality values in the Text_Panal
        filtered_df = df.loc[filtered_nodes]
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', filtered_df.to_string())

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)


    def filter_eigenvector_centrality(self, selected_option):
        # Create network graph from edge dataframe
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())

        # Compute degree centrality for each node and create a DataFrame to store the results
        eigenvector_centrality = nx.eigenvector_centrality(G)

        df1 = pd.DataFrame(index=G.nodes())
        df1.index.name = 'Node ID'
        df1['eigenvector_centrality'] = pd.Series(eigenvector_centrality).round(3)
        df1 = df1.sort_values(by='eigenvector_centrality', ascending=False)
        user_input = self.user_input.get()
        if not user_input:
            user_input = 0
        else:
            user_input = float(user_input)

        # Filter nodes based on degree centrality
        filtered_nodes = sorted([node for node in G.nodes() if eigenvector_centrality[node] >= user_input],
                    key=lambda node: eigenvector_centrality[node], reverse=True)
        # Create a new graph with only the filtered nodes
        filtered_G = G.subgraph(filtered_nodes)

        # Set node color and size for filtered nodes
        cmap = plt.cm.tab20
        node_colors = '#85C1E9'
        if (len(G.nodes()) <= 100):
            node_sizes = 1000
        else:
            node_sizes = 250
        # Generate visualization
        pos = nx.spring_layout(filtered_G)
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(filtered_G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax )
        if (selected_option.get() == 'Direct Graph'):
            for u, v, data in filtered_G.edges(data=True):
                ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", color="Black"))
        else:
            nx.draw_networkx_edges(filtered_G, pos, ax=ax)        
        labels = {node: node for node in filtered_nodes}
        nx.draw_networkx_labels(filtered_G, pos, labels=labels, font_size=7, ax=ax)
        plt.title(f'     Eigenvector Centrality Greater {user_input}')
        plt.axis('off')

        # Insert degree centrality values in the Text_Panal
        filtered_df = df1.loc[filtered_nodes]
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', filtered_df.to_string())

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)

    def filter_harmonic_centrality(self, selected_option):
            # Create network graph from edge dataframe
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())

        # Compute degree centrality for each node and create a DataFrame to store the results
        harmonic_centrality = nx.harmonic_centrality(G)

        df = pd.DataFrame(index=G.nodes())
        df.index.name = 'Node ID'
        df['harmonic_centrality'] = pd.Series(harmonic_centrality).round(4)
        df = df.sort_values(by='harmonic_centrality', ascending=False)
        user_input = self.user_input.get()
        if not user_input:
            user_input = 0
        else:
            user_input = float(user_input)

        # Filter nodes based on degree centrality
        filtered_nodes = sorted([node for node in G.nodes() if harmonic_centrality[node] >= user_input],
                    key=lambda node: harmonic_centrality[node], reverse=True)
        # Create a new graph with only the filtered nodes
        filtered_G = G.subgraph(filtered_nodes)

        # Set node color and size for filtered nodes
        cmap = plt.cm.tab20
        node_colors = '#F1948A'
        if (len(G.nodes()) <= 100):
            node_sizes = 1000
        else:
            node_sizes = 250
        # Generate visualization
        pos = nx.spring_layout(filtered_G)
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(filtered_G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax )
        if (selected_option.get() == 'Direct Graph'):
            for u, v, data in filtered_G.edges(data=True):
                ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", color="Black"))
        else:
            nx.draw_networkx_edges(filtered_G, pos, ax=ax)
        labels = {node: node for node in filtered_nodes}
        nx.draw_networkx_labels(filtered_G, pos, labels=labels, font_size=7, ax=ax)
        plt.title(f'   harmonic Centrality Greater {user_input}')
        plt.axis('off')

        # Insert degree centrality values in the Text_Panal
        filtered_df = df.loc[filtered_nodes]
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', filtered_df.to_string())

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)


    def filter_closeness_centrality(self, selected_option):
        # Create network graph from edge dataframe
        if (selected_option.get() == 'Direct Graph'):
            G = nx.from_pandas_edgelist(
                self.edge_df, source="Source", target="Target", create_using=nx.DiGraph())
        else:
            G = nx.from_pandas_edgelist(self.edge_df, source="Source", target="Target", create_using=nx.Graph())

        # Compute degree centrality for each node and create a DataFrame to store the results
        closeness_centrality = nx.closeness_centrality(G)

        df = pd.DataFrame(index=G.nodes())
        df.index.name = 'Node ID'
        df['closeness_centrality'] = pd.Series(closeness_centrality).round(3)
        df = df.sort_values(by='closeness_centrality', ascending=False)

        user_input = self.user_input.get()
        if not user_input:
            user_input = 0
        else:
            user_input = float(user_input)

        # Filter nodes based on degree centrality
        filtered_nodes = sorted([node for node in G.nodes() if closeness_centrality[node] >= user_input],
                    key=lambda node: closeness_centrality[node], reverse=True)
        # Create a new graph with only the filtered nodes
        filtered_G = G.subgraph(filtered_nodes)

        # Set node color and size for filtered nodes
        cmap = plt.cm.tab20
        node_colors = '#58D68D'
        if (len(G.nodes()) <= 100):
            node_sizes = 1000
        else:
            node_sizes = 250
        # Generate visualization
        pos = nx.spring_layout(filtered_G)
        fig, ax = plt.subplots()
        nodes = nx.draw_networkx_nodes(filtered_G, pos, node_color=node_colors, node_size=node_sizes, cmap=cmap, ax=ax )
        if (selected_option.get() == 'Direct Graph'):
            for u, v, data in filtered_G.edges(data=True):
                ax.annotate("", xy=pos[v], xytext=pos[u], arrowprops=dict(arrowstyle="->", color="Black"))
        else:
            nx.draw_networkx_edges(filtered_G, pos, ax=ax)
        labels = {node: node for node in filtered_nodes}
        nx.draw_networkx_labels(filtered_G, pos, labels=labels, font_size=7, ax=ax)
        plt.title(f'       Closeness Centrality Greater {user_input}')
        plt.axis('off')

        # Insert degree centrality values in the Text_Panal
        filtered_df = df.loc[filtered_nodes]
        self.Text_Panal.delete('1.0', tk.END)
        self.Text_Panal.insert('1.0', filtered_df.to_string())

        # Embed the plot in the GUI using a canvas
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=600)



root = tk.Tk()
root.geometry("1200x800")
gui = NetworkAnalysisGUI(root)
root.configure(bg="#D5F5E3")
root.wm_state("zoomed")
root.mainloop()
