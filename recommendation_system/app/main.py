import os

import uvicorn
from app.tfidf_recommender import TfidfRecommender
from fastapi import FastAPI, HTTPException, Query


class DummyModel:
    def predict(self, X):
        return "dummy prediction"


def load_model():
    predictor = DummyModel()
    return predictor


app = FastAPI()
app.predictor = load_model()

tfidf = TfidfRecommender.from_files(
    data_path="./data/example/cocktail_data_silver.csv",
    vectorizer_path="./model/example/vectorizer.pk",
    matrix_path="./model/example/tfidf_matrix.pk",
    threshold=0.15,
)


@app.get("/predict")
def predict(X: str = Query(..., description="Input text for prediction")):
    result = app.predictor.predict(X)
    return {
        "input_value": X,
        "predicted_value": result,
        "message": "prediction successful",
    }


@app.get("/query")
def query_route(query: str = Query(..., description="Search query")):
    if not query.strip():
        raise HTTPException(status_code=400, detail="No query provided")

    recommendations = tfidf.recommend(query)
    relevance_scores = tfidf.get_relevance_scores(query)

    results = [
        {
            "title": rec["drink_title"],
            "content": f"Garnish: {rec['garnish']}, How to: {rec['how_to'][:500]}...",
            "relevance": round(relevance, 2),
        }
        for rec, relevance in zip(recommendations, relevance_scores)
    ]

    return {"results": results, "message": "OK"}


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
