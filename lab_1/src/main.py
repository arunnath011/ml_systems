from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/hello")
async def hello(name: str):
    if name is None:
        raise HTTPException(status_code=400, detail="Name not specified")
    return {"message": f"Hello {name}"}

@app.get("/")
async def root():
    raise HTTPException(status_code=501, detail="Not Implemented")


@app.get("/docs")
async def docs():
    return {"docs": "API docs here"}

@app.get("/openapi.json")
async def openapi_json():
    return {"openapi": "3.0.0"}







