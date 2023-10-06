"""
API for Flight Delay Prediction
Author: Ronierison Maciel
Date: 2023-10-06
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import pandas as pd
import numpy as np
import os

from .model import DelayModel

app = FastAPI()

# Constants
TOP_10_FEATURES = ["N", "I"]
VALID_MONTHS = set(range(1, 13))


# Initialization
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def prepare_model() -> DelayModel:
    absolute_path = os.path.dirname(__file__)
    relative_path = "../data/data.csv"
    full_path = os.path.join(absolute_path, relative_path)
    data = load_data(full_path)
    
    model = DelayModel()
    features, target = model.preprocess(data, "delay")
    model.fit(features, target)
    return model


model = prepare_model()


# Request and Response models
class Feature(BaseModel):
    OPERA: str
    TIPOVUELO: Optional[str]
    MES: Optional[int]


class Body(BaseModel):
    flights: List[Feature]


# Routes
@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {"status": "OK"}


@app.post("/predict", status_code=200)
async def post_predict(body: Body) -> dict:
    try:
        data_entry = pd.DataFrame(0, index=np.arange(len(body.flights)), columns=model.top_10_features)

        for i, flight in enumerate(body.flights):
            _validate_flight_data(flight, i)
            _populate_data_entry(data_entry, flight, i)

        pred = model.predict(data_entry)
        return {"predict": pred}

    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=ve.errors())

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions
def _validate_flight_data(flight: Feature, index: int):
    if flight.OPERA not in model.airlines:
        raise ValueError(f"La propiedad OPERA en el indice {index} debe ser una de las aerolineas usadas en el modelo")

    if flight.TIPOVUELO and flight.TIPOVUELO not in TOP_10_FEATURES:
        raise ValueError("La propiedad TIPOVUELO debe ser 'N' o 'I'")

    if flight.MES and flight.MES not in VALID_MONTHS:
        raise ValueError("La propiedad MES debe estar entre 1 y 12")


def _populate_data_entry(data_entry: pd.DataFrame, flight: Feature, index: int):
    if flight.OPERA in model.top_10_features:
        data_entry.loc[index]['OPERA_' + flight.OPERA] = 1
        
    if flight.TIPOVUELO:
        data_entry.loc[index]['TIPOVUELO_I'] = int(flight.TIPOVUELO == 'I')

    if flight.MES:
        month = 'MES_' + str(flight.MES)
        if month in model.top_10_features:
            data_entry.loc[index][month] = 1
