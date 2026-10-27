import torch
import os
from models.hybrid_predictor import HybridSpatioTemporalPredictor
from models.losses import FocalLoss
from torch_geometric.data import Data

def run_dry_test():
    dataset_path = "data/campus_dataset.pt"
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}. Please run dataset_generator.py first.")
        return

    print("Loading synthetic campus network dataset...")
    # Setting weights_only=False to load PyTorch Geometric Data object
    dataset = torch.load(dataset_path, weights_only=False)
    
    x_seq = dataset.x
    edge_index = dataset.edge_index
    edge_weight = dataset.edge_attr
    labels = dataset.y
    
    num_nodes = x_seq.size(0)
    seq_len = x_seq.size(1)
    num_raw_features = x_seq.size(2)
    num_classes = 6       # 0: nominal, 1-5: failure modes
    
    print(f"Dataset loaded successfully!")
    print(f" - Nodes: {num_nodes}")
    print(f" - Sequence Length: {seq_len}")
    print(f" - Edge connections: {edge_index.size(1)}")
    
    print("\nInitializing Hybrid Spatio-Temporal Predictor...")
    model = HybridSpatioTemporalPredictor(num_raw_features=num_raw_features, num_classes=num_classes)
    
    print("Running forward pass through the hybrid model...")
    logits = model(x_seq, edge_index, edge_weight)
    
    print("\nCalculating Loss (Focal Loss)...")
    alpha = torch.ones(num_classes)
    alpha[0] = 0.2 # Downweight majority class (nominal)
    alpha[1:] = 1.0 # Upweight fault classes
    criterion = FocalLoss(alpha=alpha, gamma=2.0)
    
    loss = criterion(logits, labels)
    print(f"Initial Forward Pass Loss: {loss.item():.4f}")
    
    print("\n--- Output Diagnostics ---")
    predicted_classes = torch.argmax(logits, dim=-1)
    
    print("Evaluating injected faults:")
    for i in range(num_nodes):
        if labels[i].item() != 0: # Only print nodes where we injected faults
            print(f"Node {i} | Injected Fault: Class {labels[i].item()} | Predicted: Class {predicted_classes[i].item()} | Confidence: {torch.softmax(logits[i], dim=-1).max().item():.2f}")
            
    print("\nDataset generation, loading, and model forward pass completed successfully.")

if __name__ == "__main__":
    run_dry_test()
