import torch
import torch.nn as nn
import torch.nn.functional as F
torch.manual_seed(1337)

class BigramLanguageModel(nn.Module):
    
    def __init__(self, vocab_size):
        super(BigramLanguageModel, self).__init__()
        self.token_embeddings_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets=None):
        #idx and targets are both (B, T) shape tensors
        logits = self.token_embeddings_table(idx)
        if targets==None:
            loss = None
        else:        
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss
    
    def generate(self, idx, max_new_tokens):
        #idx is a (B, T) shape array
        for _ in range(max_new_tokens):
            logits, loss = self(idx)
            #we are only interested in the last token of the sequence
            #B, C  = logits.shape
            logits = logits[:, -1, :]
            #apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)# (B, 1)
            idx = torch.cat([idx, idx_next], dim=1) #(B, T+1)
        return idx