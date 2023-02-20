from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import numpy as np
from datetime import datetime
import requests
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_pipeline.pkl")


# define pydantic models for input and output
 #Define input data model
class BlockGroup(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: int
    AveOccup: float
    Latitude: float
    Longitude: float

# Define input data list model
class HousingDataInputList(BaseModel):
    data: List[BlockGroup]

# Define output data model
class HousingDataOutput(BaseModel):
    predictions: List[List[float]] = []


# load the pre-trained model
start = datetime.now()
model = joblib.load(MODEL_PATH)
end = datetime.now()
print(f"time to load model: {end-start}")

app = FastAPI()

@app.post("/predict", response_model=HousingDataOutput)
def predict(data: HousingDataInputList):
    x = np.array([[bg.MedInc, bg.HouseAge, bg.AveRooms, bg.AveBedrms, bg.Population, bg.AveOccup, bg.Latitude, bg.Longitude] for bg in data.data])
    if x.size == 0:
        print("Input data should not be empty")
        return HousingDataOutput(predictions=[])
    if x.ndim != 2 or x.shape[1] != 8:
        print("Input data should have 8 columns")
        return
    try:
        predictions = model.predict(x)
        predictions_output = [[pred] for pred in predictions]
    except:
        print("Invalid input data")
        return HousingDataOutput(predictions=[])

    return HousingDataOutput(predictions=predictions_output)


# define the health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

