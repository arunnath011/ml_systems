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


app = FastAPI()

hub_path = "./distilbert-base-uncased-finetuned-sst2"

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
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
@app.post("/predict", response_model=SentimentResponse)
def predict(sentiments: SentimentRequest):
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

    return response

@app.get("/health")
async def health():
    return {"status": "healthy"}