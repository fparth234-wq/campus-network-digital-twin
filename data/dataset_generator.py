"""
dataset_generator.py

Generates a synthetic spatio-temporal dataset representing a campus network.
Creates node features (telemetry over time), edge indices (topology),
and fault labels (multi-class) to satisfy Review 1 requirements.
"""
import os
import torch
from torch_geometric.data import Data

def generate_synthetic_dataset(num_nodes=30, seq_len=15, num_features=5, num_classes=6, save_path="data/campus_dataset.pt"):
    print(f"Generating synthetic topology for {num_nodes} nodes...")
    
    # Create a tree-like topology (Core -> Dist -> Access)
    edges = []
    # 2 Core, 6 Dist, 22 Access
    # Cores connected to each other
    edges.append([0, 1])
    edges.append([1, 0])
    
    # Dists connected to cores
    for i in range(2, 8):
        core_parent = i % 2
        edges.append([core_parent, i])
        edges.append([i, core_parent])
        
    # Access connected to dists
    for i in range(8, num_nodes):
        dist_parent = 2 + (i % 6)
        edges.append([dist_parent, i])
        edges.append([i, dist_parent])
        
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    edge_weight = torch.rand(edge_index.size(1)) * 0.5 + 0.5 # utilization weights
    
    print(f"Generating time-series telemetry ({seq_len} steps, {num_features} metrics)...")
    # Features: utilizationPct, ifInErrors, ifOutErrors, queueDepthPct, dropRatePps
    # Most nodes are nominal
    x_seq = torch.rand(num_nodes, seq_len, num_features) * 0.3
    
    # Inject faults in a few nodes
    labels = torch.zeros(num_nodes, dtype=torch.long)
    
    # Fault 1: Congestion (Node 5 - Dist)
    x_seq[5, :, 0] = torch.linspace(0.5, 0.99, seq_len) # utilization ramps up
    x_seq[5, :, 3] = torch.linspace(0.4, 0.95, seq_len) # queue depth ramps up
    labels[5] = 1 # Congestion class
    
    # Fault 2: Hardware degradation (Node 15 - Access)
    x_seq[15, :, 1] = torch.linspace(0.1, 0.8, seq_len) # In errors rising
    labels[15] = 2 # Hardware degradation class
    
    # Fault 3: Broadcast Storm / Loop (Node 22 - Access)
    x_seq[22, :, 0] = 0.99 # Pinned at max utilization
    x_seq[22, :, 4] = torch.linspace(0.2, 0.9, seq_len) # high drop rate
    labels[22] = 3 # Loop class

    dataset = Data(x=x_seq, edge_index=edge_index, edge_attr=edge_weight, y=labels)
    
    torch.save(dataset, save_path)
    print(f"Dataset saved to {save_path}")
    print("Dataset stats:")
    print(f" - Nodes: {num_nodes}")
    print(f" - Edges: {edge_index.size(1)}")
    print(f" - Sequence Length: {seq_len}")
    return dataset

if __name__ == "__main__":
    generate_synthetic_dataset()
