from typing import List, Literal
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing._label import LabelBinarizer
from pydantic import BaseModel, Field
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sys
import os
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    age: Literal["0", "1", "2", "3","4"]
    workclass: Literal[
        "State-gov",
        "Self-emp-not-inc",
        "Private",
        "Federal-gov",
        "Local-gov",
        "Self-emp-inc",
        "Without-pay",
    ]
    fnlwgt: float = Field(ge=13492,le=1490400)
    education: Literal[
        "Bachelors",
        "HS-grad",
        "11th",
        "Masters",
        "9th",
        "Some-college",
        "Assoc-acdm",
        "Assoc-voc",
        "7th-8th",
        "Doctorate",
        "Prof-school",
        "5th-6th",
        "10th",
        "Preschool",
        "12th",
        "1st-4th",
    ]
    marital_status: Literal[
        "Never-married",
        "Married-civ-spouse",
        "Divorced",
        "Married-spouse-absent",
        "Separated",
        "Married-AF-spouse",
        "Widowed",
    ] = Field(alias="marital-status")
    occupation: Literal[
        "Adm-clerical",
        "Exec-managerial",
        "Handlers-cleaners",
        "Prof-specialty",
        "Other-service",
        "Sales",
        "Craft-repair",
        "Transport-moving",
        "Farming-fishing",
        "Machine-op-inspct",
        "Tech-support",
        "Protective-serv",
        "Armed-Forces",
        "Priv-house-serv",
    ]
    relationship: Literal[
        "Not-in-family", "Husband", "Wife", "Own-child", "Unmarried", "Other-relative"
    ]
    race: Literal["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"]
    sex: Literal["Male", "Female"]
    capitalgain: Literal[
        "0",
        "1",
        "2",
        "3",
        "4"
    ]
    capitalloss: Literal[
        "0",
        "1",
        "2",
        "3",
        "4"
    ]
    hoursperweek: Literal[
        "0",
        "1",
        "2",
        "3",
        "4",
    ]

class ModelPrediction(BaseModel):
    prediction: Literal["<=50K",">50K"]

class BatchPrediction(Item):
    prediction: Literal["<=50K",">50K"]

@app.post("/predict")
def predict(item: Item)->ModelPrediction:
    data: dict = item.model_dump()
    df = pd.DataFrame(data, index=[1])
    df = df.rename(columns={"marital_status": "marital-status"})
    model: Pipeline = joblib.load("app/model.joblib")
    yenc: LabelBinarizer = joblib.load("app/ytransform.joblib")
    pred = yenc.inverse_transform(model.predict(df))
    return ModelPrediction(prediction=str(pred[0]))


@app.post("/uploadfile",response_model=list[BatchPrediction])
async def create_upload_file(file: UploadFile):
    df = pd.read_csv(file.file)
    model: Pipeline = joblib.load("app/model.joblib")
    yenc: LabelBinarizer = joblib.load("app/ytransform.joblib")
    cat_cols: List[str] = model.named_steps["preprocessor"].transformers[1][-1]
    num_cols: List[str] = model.named_steps["preprocessor"].transformers[0][-1]
    for col in df.columns:
        if col in cat_cols:
            df[col] = df[col].astype("str")
        elif col in num_cols:
            df[col] = pd.to_numeric(df[col]).round(3)
    df = df.dropna(subset=cat_cols + num_cols)
    preds = model.predict(df[cat_cols+num_cols])
    df["prediction"] = yenc.inverse_transform(preds)
    df["prediction"] = df["prediction"].astype(str)
    return df.to_dict(orient="records")
