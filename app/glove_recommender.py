import numpy as np
import pandas as pd
import torch
from sklearn.metrics.pairwise import linear_kernel

from utils.autoencoder import Autoencoder
from utils.glove import Glove
from utils.tokenizer import MyTokenizer
from utils.train_embedding import create_embedding_matrix, mean_pooling, get_enhanced_embeddings


class GloVeRecommender:
    def __init__(
        self, df: pd.DataFrame, model, embeddings, threshold=0.1
    ):
        self.df = df
        self.model = model
        self.embeddings = embeddings
        self.threshold = threshold

        glove = Glove._load_glove_vectors("model/glove.6B/glove.6B.300d.txt")
        self.tokenizer = MyTokenizer(sentence_length=450, case_sensitive=False)
        self.tokenizer.fit(df.whole_text)

        self.embedding_matrix = create_embedding_matrix(self.tokenizer.vocab, glove)

    @classmethod
    def from_files(
        cls, data_path: str, model_path: str, embedding_path: str, threshold=0.1
    ):
        df = pd.read_csv(data_path)
        with open(model_path, "rb") as file:
            model = Autoencoder(300,200,100)
            model.load_state_dict(torch.load('model/example/autoencoder_model.pth'))
        with open(embedding_path, "rb") as file:
            embeddings = np.load(file)



        return cls(df, model, embeddings, threshold)

    def _get_query_vector(self, query):
        self.model.eval() 
        tokens = self.tokenizer(query)  
        vectors = [self.embedding_matrix[token] for token in tokens]  
        pooled_embedding = mean_pooling(vectors) 
        with torch.no_grad():
            sentence_embedding = torch.FloatTensor(pooled_embedding).unsqueeze(0)
            sentence_embedding = self.model.encoder(torch.FloatTensor(sentence_embedding).unsqueeze(0)).squeeze(0).detach().numpy()
        return sentence_embedding
    
    def recommend(self, query, top_n=10):
        query_vec = self._get_query_vector(query)
        relevance_scores = linear_kernel(query_vec, self.embeddings)[0]
        
        top_indices = [
            i
            for i in relevance_scores.argsort()[::-1]
            if relevance_scores[i] > self.threshold
        ][:top_n]

        if not top_indices:
            return []

        return (
            self.df[
                [
                    "drink_title",
                    "drink_glass",
                    "garnish",
                    "comment",
                    "history",
                    "how_to_translated",
                ]
            ]
            .iloc[top_indices]
            .fillna("")
            .to_dict(orient="records")
        )
    
    def get_relevance_scores(self, query):
        query_vec = self._get_query_vector(query)
        relevance_scores = linear_kernel(query_vec, self.embeddings)[0]
        return relevance_scores[relevance_scores.argsort()[::-1][:10]]