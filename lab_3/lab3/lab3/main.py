#importing all the necessary packages
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
import redis
import json
#setting the path of the model_pipline.pkl file
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',  'model_pipeline.pkl'))

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



# create a Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)
#for running redis on docker
#redis_client = redis.Redis(host='redis', port=6379, db=0)


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
def predict(data: HousingDataInputList):
    # check if the result is already cached
    cache_key = str(data.dict())
    cached_result = redis_client.get(cache_key)
    if cached_result is not None:
        return HousingDataOutput(predictions=json.loads(cached_result))

    x = np.array([[bg.MedInc, bg.HouseAge, bg.AveRooms, bg.AveBedrms, bg.Population, bg.AveOccup, bg.Latitude, bg.Longitude] for bg in data.data])
    if x.size == 0:
        print("Input data should not be empty")
        return HousingDataOutput(predictions=[])
    if x.ndim != 2 or x.shape[1] != 8:
        print("Input data should have 8 columns")
        return
    if (x[:, 4] <= 0).any():
        raise HTTPException(status_code=422, detail="Population value should be greater than 0")
    try:
        predictions = model.predict(x)
        predictions_output = [[pred] for pred in predictions]
    except:
        print("Invalid input data")
        return HousingDataOutput(predictions=[])

    redis_client.set(cache_key, json.dumps(predictions_output))

    return HousingDataOutput(predictions=predictions_output)


# define the health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

