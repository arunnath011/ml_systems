import logging
import os

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    return_all_scores=True,
)

#pydantic models


logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://redis:6379"
app = FastAPI()


@app.on_event("startup")
def startup():
    pass


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
        predictions=[Sentiment(label=label, score=score) for pred in predictions for label, score in pred["scores"]])
    return response

@app.get("/health")
async def health():
    return {"status": "healthy"}