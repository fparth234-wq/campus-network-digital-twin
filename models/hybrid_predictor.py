import torch
import torch.nn as nn
from .fts_lstm import FTSLSTM
from .mpnn import SpatialGNN

class FaultClassificationHead(nn.Module):
    """
    Fuses temporal (FTS-LSTM) and spatial (MPNN) embeddings and produces
    a K+1-way class distribution: {0: nominal, 1..K: failure modes}.
    """
    def __init__(self, temporal_dim: int = 32, spatial_dim: int = 64,
                 num_classes: int = 6):
        super().__init__()
        fused_dim = temporal_dim + spatial_dim
        self.classifier = nn.Sequential(
            nn.Linear(fused_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes),
        )

    def forward(self, temporal_embed, spatial_embed):
        fused = torch.cat([temporal_embed, spatial_embed], dim=-1)
        return self.classifier(fused)  # (num_nodes, num_classes) logits

class HybridSpatioTemporalPredictor(nn.Module):
    """End-to-end SDFD pipeline: FTS-LSTM -> SpatialGNN -> Classification Head."""
    def __init__(self, num_raw_features: int, num_classes: int = 6):
        super().__init__()
        self.temporal = FTSLSTM(num_raw_features, hidden_dim=64, embedding_dim=32)
        self.spatial = SpatialGNN(embed_dim=32, hidden_dim=64)
        self.head = FaultClassificationHead(temporal_dim=32, spatial_dim=64,
                                             num_classes=num_classes)

    def forward(self, x_seq, edge_index, edge_weight):
        # x_seq: (num_nodes, seq_len, num_raw_features)
        h_temporal = self.temporal(x_seq)                       # (num_nodes, 32)
        h_spatial = self.spatial(h_temporal, edge_index, edge_weight)  # (num_nodes, 64)
        logits = self.head(h_temporal, h_spatial)                # (num_nodes, num_classes)
        return logits
