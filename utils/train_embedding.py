import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from utils.autoencoder import Autoencoder
from utils.glove import Glove
from utils.tokenizer import MyTokenizer


def train_autoencoder(model, data, criterion, optimizer, epochs=20, batch_size=256):
    model.train()  
    for epoch in range(epochs):
        total_loss = 0
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            batch = torch.FloatTensor(batch) 

            outputs = model(batch)

            loss = criterion(outputs, batch)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

    return model

def create_embedding_matrix(vocab, glove_vectors, embedding_dim=300):
    vocab_size = len(vocab)

    embedding_matrix = np.random.randn(vocab_size, embedding_dim)
    embedding_matrix[vocab["<PAD>"]] = np.zeros(embedding_dim)
    embedding_matrix[vocab["<UNK>"]] = np.random.randn(embedding_dim)

    for word, idx in vocab.items():
        if word in glove_vectors:
            embedding_matrix[idx] = np.asarray(glove_vectors[word])

    return embedding_matrix


def mean_pooling(vectors):
    vectors = np.array(vectors)
    return np.mean(vectors, axis=0)


def get_enhanced_embeddings(model, data):
    model.eval() 
    enhanced_embeddings = []
    with torch.no_grad():
        for sentence_embedding in data:
            sentence_embedding = torch.FloatTensor(sentence_embedding).unsqueeze(0)
            encoded_embedding = model.encoder(sentence_embedding)
            enhanced_embeddings.append(encoded_embedding.squeeze(0).numpy())
    return enhanced_embeddings

if __name__ == "__main__":
    input_dim = 300  
    hidden_fst = 200
    hidden_snd = 100

    documents = pd.read_csv('data/example/cocktail_data_silver.csv')
    glove = Glove._load_glove_vectors("model/glove.6B/glove.6B.300d.txt")


    autoencoder = Autoencoder(input_dim, hidden_fst, hidden_snd)

    criterion = nn.MSELoss() 
    optimizer = torch.optim.Adam(autoencoder.parameters(), lr=0.01)

    tokenizer = MyTokenizer(sentence_length=450, case_sensitive=False)
    tokenizer.fit(documents.whole_text)

    embedding_matrix = create_embedding_matrix(tokenizer.vocab, glove)

    sentence_embeddings = []
    for phrase in documents.whole_text:
        tokens = tokenizer(phrase)  
        vectors = [embedding_matrix[token] for token in tokens]  
        pooled_embedding = mean_pooling(vectors)  
        sentence_embeddings.append(pooled_embedding)

    data_sentence_embeddings = sentence_embeddings.copy()
    model = train_autoencoder(autoencoder, data_sentence_embeddings, criterion, optimizer)

    enhanced_embeddings = get_enhanced_embeddings(model, data_sentence_embeddings)

    torch.save(model.state_dict(), "model/example/autoencoder_model.pth")
    with open('model/example/glove_trained_embeddings.npy', 'wb') as f:
        np.save(f, np.array(enhanced_embeddings))
