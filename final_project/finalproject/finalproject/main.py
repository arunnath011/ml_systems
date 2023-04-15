import logging
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from transformers import AutoConfig, AutoModelForSequenceClassification, AutoTokenizer
import json
import os
from typing import List
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import redis


# create a Redis client this for running locally
# redis_client = redis.Redis(host='localhost', port=6379, db=0)
#for running redis on docker
redis_client = redis.Redis(host='redis', port=6379, db=0)

app = FastAPI()
# #for running  locally
# hub_path = "./distilbert-base-uncased-finetuned-sst2"

#for running in docker
hub_path = "/app/model"

model = AutoModelForSequenceClassification.from_pretrained(hub_path)
tokenizer = AutoTokenizer.from_pretrained(hub_path)

classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    top_k=None,
)

class SentimentRequest(BaseModel):
    text: List[str]

class Sentiment(BaseModel):
    label: str
    score: float

class SentimentResponse(BaseModel):
    predictions: List[Sentiment]

# @app.post("/predict", response_model=SentimentResponse)
# def predict(sentiments: SentimentRequest):
#     predictions = classifier(sentiments.text)
#     response = SentimentResponse(
#         predictions=[
#             Sentiment(
#                 label=label,
#                 score=score
#             )
#             for pred in predictions
#             for label, score in zip(
#                 [p.get("label") for p in pred],
#                 [p.get("score") for p in pred]
#             )
#         ]
#     )
#
#     return response

@app.post("/predict", response_model=SentimentResponse)
def predict(sentiments: SentimentRequest):
    # Check if the input exists in the cache
    input_key = json.dumps({"text": sentiments.text})
    cache_result = redis_client.get(input_key)

    if cache_result:
        # If the result exists in the cache, return it
        response = json.loads(cache_result)
    else:
        # If the result doesn't exist in the cache, compute it and store it in the cache
        predictions = classifier(sentiments.text)
        response = SentimentResponse(
            predictions=[
                Sentiment(
                    label=label,
                    score=score
                )
                for pred in predictions
                for label, score in zip(
                    [p.get("label") for p in pred],
                    [p.get("score") for p in pred]
                )
            ]
        )

        # Store the result in the cache with an expiration time (e.g., 60 seconds)
        redis_client.set(input_key, json.dumps(response.dict()), ex=60)

    return response

@app.get("/health")
async def health():
    return {"status": "healthy"}