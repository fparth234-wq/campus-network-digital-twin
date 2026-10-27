import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops

class TopoMPNNLayer(MessagePassing):
    """
    Message-passing layer operating on FTS-LSTM temporal embeddings,
    propagating risk-relevant signal across topological neighbors.
    """
    def __init__(self, in_dim: int, out_dim: int):
        super().__init__(aggr='add')  # sum aggregation over neighbor messages
        self.msg_mlp = nn.Sequential(
            nn.Linear(2 * in_dim + 1, out_dim),  # +1 for edge weight (utilization)
            nn.ReLU(),
        )
        self.update_mlp = nn.Sequential(
            nn.Linear(in_dim + out_dim, out_dim),
            nn.ReLU(),
        )

    def forward(self, h, edge_index, edge_weight):
        edge_index, edge_weight = add_self_loops(
            edge_index, edge_weight, fill_value=1.0, num_nodes=h.size(0)
        )
        return self.propagate(edge_index, h=h, edge_weight=edge_weight)

    def message(self, h_i, h_j, edge_weight):
        # h_i: target node embedding, h_j: source (neighbor) embedding
        edge_feat = edge_weight.unsqueeze(-1)
        return self.msg_mlp(torch.cat([h_i, h_j, edge_feat], dim=-1))

    def update(self, aggr_out, h):
        return self.update_mlp(torch.cat([h, aggr_out], dim=-1))

class SpatialGNN(nn.Module):
    """Two-layer MPNN stack producing a spatially-contextualized embedding."""
    def __init__(self, embed_dim: int = 32, hidden_dim: int = 64):
        super().__init__()
        self.layer1 = TopoMPNNLayer(embed_dim, hidden_dim)
        self.layer2 = TopoMPNNLayer(hidden_dim, hidden_dim)

    def forward(self, h, edge_index, edge_weight):
        h = F.relu(self.layer1(h, edge_index, edge_weight))
        h = F.relu(self.layer2(h, edge_index, edge_weight))
        return h  # (num_nodes, hidden_dim)
