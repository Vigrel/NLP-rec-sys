import torch
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


def train_autoencoder(model, data, criterion, optimizer, epochs=20, batch_size=256):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        # for i in range(0, len(data), batch_size):
        batch = data
        # batch = data[i:i+batch_size]
        batch = torch.FloatTensor(batch)

        outputs = model(batch)

        loss = criterion(outputs, batch)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        print(f"Epoch [{epoch+1}/{epochs}], Loss: {total_loss/len(data):.4f}")
