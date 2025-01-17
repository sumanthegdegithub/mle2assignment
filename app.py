import json
from typing import Any, List, Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, FastAPI
from fastapi.encoders import jsonable_encoder
from pipelines.inference_pipeline import inference
from pydantic import BaseModel
import json
import uvicorn


class PredictionResults(BaseModel):
    error: Any
    predicted_class: str | None
    class_probabilities: dict | None

app = FastAPI()

@app.get("/predict", response_model=PredictionResults, status_code=200)
async def predict(url: str):
    results = inference(url)
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)