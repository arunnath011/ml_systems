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
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_pipeline.pkl")


# define pydantic models for input and output
class BlockGroup(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: int
    AveOccup: float
    Latitude: float
    Longitude: float

class HousingDataOutput(BaseModel):
    predictions: List[List[float]] = []

# load the pre-trained model
start = datetime.now()
model = joblib.load(MODEL_PATH)
end = datetime.now()
print(f"time to load model: {end-start}")

app = FastAPI()


@app.get("/")
async def root():
    raise HTTPException(status_code=501, detail="Not Implemented")

@app.get("/hello")
async def hello(name: str = None):
    if name is None:
        raise HTTPException(status_code=400, detail="Name not specified")
    return {"message": f"Hello {name}"}


@app.post("/predict", response_model=HousingDataOutput)
def predict(data: BlockGroup):
    x = np.array([[
        data.MedInc,
        data.HouseAge,
        data.AveRooms,
        data.AveBedrms,
        data.Population,
        data.AveOccup,
        data.Latitude,
        data.Longitude
    ]])
    try:
        predictions = model.predict(x)
        predictions_output = [[pred] for pred in predictions]
    except:
        print("Invalid input data")
        return HousingDataOutput(predictions=[])
    return HousingDataOutput(predictions=predictions_output)

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


