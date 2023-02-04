from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    raise HTTPException(status_code=501, detail="Not Implemented")

@app.get("/hello")
async def hello(name: str = None):
    if name is None:
        raise HTTPException(status_code=400, detail="Name not specified")
    return {"message": f"Hello {name}"}

@app.get("/docs")
async def docs():
    return {"message": "browsable while API is running"}


@app.get("/openapi.json")
async def openapi_json():
    return {"openapi_json": "browsable while API is running"}






