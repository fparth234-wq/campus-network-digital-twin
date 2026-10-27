import torch
import torch.nn as nn
import torch.nn.functional as F

class FocalLoss(nn.Module):
    """Class-imbalance-aware training objective (Section 3.1.2)."""
    def __init__(self, alpha: torch.Tensor, gamma: float = 2.0):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, logits, targets):
        log_p = F.log_softmax(logits, dim=-1)
        p = log_p.exp()
        p_t = p.gather(1, targets.unsqueeze(1)).squeeze(1)
        log_p_t = log_p.gather(1, targets.unsqueeze(1)).squeeze(1)
        alpha_t = self.alpha[targets]
        loss = -alpha_t * (1 - p_t) ** self.gamma * log_p_t
        return loss.mean()
