from typing import List
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pandas as pd
from pathlib import Path
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load('./model/model_binary.dat.gz')

# TYPES

class OneInput(BaseModel):
    Sex: str
    AccidentArea: str

    class Config:
        schema_extra = {
            'example': {
                "Sex": 'Male', 
                "AccidentArea": 'Rural'
            }
        }

class Input(BaseModel):
    inputs: List[OneInput]

    class Config:
        schema_extra = {
            'example': {
                "inputs": [
                    {
                        "Sex": 'Male', 
                        "AccidentArea": 'Rural'
                    },
                    {
                        "Sex": 'Female',
                        "AccidentArea": 'Urban'
                    }
                ]
            }
        }

class Output(BaseModel):
    prediction: List[float]

# MODEL FUNCTIONS

def get_model_response(input):
    X = pd.DataFrame(jsonable_encoder(input.__dict__['inputs']))
    pred = model.predict_proba(X)[:,1].round(2).tolist()

    return {'prediction': pred}

# API

@app.post("/predict", response_model=Output)
async def model_predict(input: Input):
    return get_model_response(input)