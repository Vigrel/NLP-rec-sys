import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class TfidfRecommender:
    def __init__(
        self, df: pd.DataFrame, vectorizer: TfidfVectorizer, tfidf_matrix, threshold=0.1
    ):
        self.df = df
        self.vectorizer = vectorizer
        self.tfidf_matrix = tfidf_matrix
        self.threshold = threshold

    @classmethod
    def from_files(
        cls, data_path: str, vectorizer_path: str, matrix_path: str, threshold=0.1
    ):
        df = pd.read_csv(data_path)
        with open(vectorizer_path, "rb") as file:
            vectorizer = pickle.load(file)
        with open(matrix_path, "rb") as file:
            tfidf_matrix = pickle.load(file)
        return cls(df, vectorizer, tfidf_matrix, threshold)

    def _get_query_vector(self, query):
        return self.vectorizer.transform([query])

    def recommend(self, query, top_n=10):
        query_vec = self._get_query_vector(query)
        relevance_scores = linear_kernel(query_vec, self.tfidf_matrix).flatten()

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
        relevance_scores = linear_kernel(query_vec, self.tfidf_matrix).flatten()

        return relevance_scores[relevance_scores.argsort()[::-1]]
