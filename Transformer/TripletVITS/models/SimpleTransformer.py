
from torch import nn
from models.TransformerBlock import TransformerBlock
from PatchEmbedding import PatchEmbedding_CNN
from models.PositionalEncoding import PositionalEncoding
import torch

class SimpleTransformer(nn.Module):
    def __init__(self, dim, num_unique_tokens=256, num_layers=6, heads=8,
        dim_head=None, max_seq_len=1024):
        super().__init__()
        self.max_seq_len = max_seq_len
        
        #self.token_emb = nn.Embedding(num_unique_tokens, dim)
        self.token_emb = PatchEmbedding_CNN(emb_size=dim)
        # our position embedding class
        self.pos_enc = PositionalEncoding(dim,max_seq_length=max_seq_len)

        self.block_list = [TransformerBlock(dim=dim, heads=heads,dim_head=dim_head) for _ in range(num_layers)]
        self.layers = nn.ModuleList(self.block_list)
        self.to_logits = nn.Sequential(
                        nn.LayerNorm(dim),
                        nn.Linear(dim, num_unique_tokens)
                        )
    

    def forward(self, x):
    
        pos = torch.arange(0, x.shape[-1], dtype=torch.long,device='cuda').unsqueeze(0) # shape (1, t)
        x = self.token_emb(x)
        x = x + self.pos_enc(x)
        for layer in self.layers:
            x = layer(x)
        return self.to_logits(x)