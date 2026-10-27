import torch
import torch.nn as nn

class FTSLSTM(nn.Module):
    """
    Fast Time-Series LSTM: a pruned-gate recurrent encoder producing a
    per-node temporal embedding from a sliding window of telemetry.
    Input:  x  -> (batch, seq_len, num_raw_features)
    Output: h  -> (batch, embedding_dim)  per-node temporal embedding
    """
    def __init__(self, num_raw_features: int, hidden_dim: int = 64,
                 embedding_dim: int = 32, num_layers: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=num_raw_features,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
        )
        self.proj = nn.Linear(hidden_dim, embedding_dim)
        self.norm = nn.LayerNorm(embedding_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (batch, seq_len, num_raw_features)
        _, (h_n, _) = self.lstm(x)          # h_n: (num_layers, batch, hidden_dim)
        last_hidden = h_n[-1]                # (batch, hidden_dim)
        embedding = self.proj(last_hidden)   # (batch, embedding_dim)
        return self.norm(embedding)
