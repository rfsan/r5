from typing import List
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pandas as pd
from pydantic import BaseModel

from models.predict import get_proba

app = FastAPI()

# TYPES

class OneInput(BaseModel):
    AccidentArea: str
    Sex: str
    VehicleCategory: str
    BasePolicy: str
    Yearr: int
    AgeOfPolicyHolder: str

    class Config:
        schema_extra = {
            'example': {
                "AccidentArea": 'Rural',
                "Sex": 'Male', 
                "VehicleCategory": 'Sport',
                'BasePolicy': 'Liability',
                'Yearr': 1996,
                'AgeOfPolicyHolder': '51 to 65'
            }
        }

class Input(BaseModel):
    inputs: List[OneInput]

    class Config:
        schema_extra = {
            'example': {
                "inputs": [
                    {
                        "AccidentArea": 'Rural',
                        "Sex": 'Male', 
                        "VehicleCategory": 'Sport',
                        'BasePolicy': 'Liability',
                        'Yearr': 1996,
                        'AgeOfPolicyHolder': '51 to 65'
                    },
                    {
                        "AccidentArea": 'Urban',
                        "Sex": 'Male', 
                        "VehicleCategory": 'Utility',
                        'BasePolicy': 'Collision',
                        'Yearr': 1994,
                        'AgeOfPolicyHolder': '16 to 17'
                    }
                ]
            }
        }

class Output(BaseModel):
    prediction: List[float]

# MODEL FUNCTIONS

def get_model_proba(input):
    X = pd.DataFrame(jsonable_encoder(input.__dict__['inputs']))
    return {'prediction': get_proba(X)}

# API

@app.post("/predict", response_model=Output)
async def model_predict(input: Input):
    return get_model_proba(input)