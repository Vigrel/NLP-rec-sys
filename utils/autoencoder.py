import torch.nn as nn


class Autoencoder(nn.Module):
    def __init__(self, input_dim, hidden_fst, hidden_snd):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_fst),
            nn.ReLU(True),
            nn.Linear(hidden_fst, hidden_snd),
            nn.ReLU(True),
            nn.Linear(hidden_snd, 50),
            nn.ReLU(True),
        )
        self.decoder = nn.Sequential(
            nn.Linear(50, hidden_snd),
            nn.ReLU(True),
            nn.Linear(hidden_snd, hidden_fst),
            nn.ReLU(True),
            nn.Linear(hidden_fst, input_dim),
            nn.ReLU(True),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x