import os

import uvicorn
from app.glove_recommender import GloVeRecommender
from fastapi import FastAPI, HTTPException, Query


class DummyModel:
    def predict(self, X):
        return "dummy prediction"


def load_model():
    predictor = DummyModel()
    return predictor


app = FastAPI()
app.predictor = load_model()

glove = GloVeRecommender.from_files(
    data_path="data/example/cocktail_data_gold.csv",
    model_path="model/example/autoencoder_model.pth",
    embedding_path="model/example/glove_trained_embeddings.npy",
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

    recommendations = glove.recommend(query)
    relevance_scores = list(glove.get_relevance_scores(query))  
    print(relevance_scores)
    relevance_scores = [int(i) for i in relevance_scores]
    results = [
        {
            "title": rec["drink_title"],
            "Drink Glass": rec["drink_glass"],
            "Garnish": rec["garnish"],
            "Comment": rec["comment"],
            "History": rec["history"],
            "How To": rec["how_to_translated"],
            "relevance": round(relevance, 2),
        }
        for rec, relevance in zip(recommendations, relevance_scores)
    ]

    return {"results": results, "message": "OK"}


def run():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
