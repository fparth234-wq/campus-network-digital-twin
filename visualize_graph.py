import torch
from torch_geometric.utils import to_networkx
import networkx as nx
import matplotlib.pyplot as plt

def plot_network_graph():
    # Load the synthetic campus dataset we generated
    dataset_path = "data/campus_dataset.pt"
    dataset = torch.load(dataset_path, weights_only=False)
    
    # Convert PyTorch Geometric data to NetworkX graph
    # to_networkx handles the edge_index translation automatically
    G = to_networkx(dataset, to_undirected=True)
    
    # Define node colors based on their roles
    # Nodes 0-1: Core (Red)
    # Nodes 2-7: Distribution (Orange)
    # Nodes 8-29: Access (Light Blue)
    node_colors = []
    node_labels = {}
    for i in range(dataset.num_nodes):
        if i < 2:
            node_colors.append('red')
            node_labels[i] = f"C{i}"
        elif i < 8:
            node_colors.append('orange')
            node_labels[i] = f"D{i}"
        else:
            # Highlight injected faults
            if i == 15:
                node_colors.append('purple') # Fault: Hardware
                node_labels[i] = f"A{i}\n(Degraded)"
            elif i == 22:
                node_colors.append('purple') # Fault: Loop
                node_labels[i] = f"A{i}\n(Loop)"
            elif i == 5: # Actually 5 is a distribution node, so let's overwrite
                pass
            else:
                node_colors.append('lightblue')
                node_labels[i] = f"A{i}"
                
    # Fix the label for Node 5 (Distribution Congestion)
    node_colors[5] = 'purple'
    node_labels[5] = "D5\n(Congest)"

    # Plot the graph
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G, seed=42) # Layout algorithm for tree-like graphs
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, edgecolors='black')
    nx.draw_networkx_edges(G, pos, alpha=0.5, width=2)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=9, font_weight='bold')
    
    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=12, label='Core Layer'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=12, label='Distribution Layer'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=12, label='Access Layer'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=12, label='Injected Faults')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.title("Campus Network Topology Graph (30 Nodes)\nUsed by the AI Message-Passing Neural Network", fontsize=14)
    plt.axis('off')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('graph_visualization.png', dpi=300)
    print("Graph visualization saved to graph_visualization.png")

if __name__ == "__main__":
    plot_network_graph()
