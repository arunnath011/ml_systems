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
from sklearn.impute import SimpleImputer

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_pipeline.pkl")


# define pydantic models for input and output
 #Define input data model
class InputModel(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: int
    AveOccup: float
    Latitude: float
    Longitude: float




# Define output data model
class HousingDataOutput(BaseModel):
    predictions: List[float]


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



@app.post("/predict")
def predict(input: InputModel):
    input_dict = input.dict()
    input_vector = np.array([input_dict[key] for key in input_dict])
    input_vector = np.reshape(input_vector, (1, -1))
    imputer = SimpleImputer()
    X_imputed = imputer.fit_transform(input_vector)
    prediction = model.predict(X_imputed)
    prediction_output = HousingDataOutput(predictions=[float(prediction)])
    return prediction_output



# define the health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

