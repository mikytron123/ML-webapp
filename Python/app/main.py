from typing import List
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing._label import LabelBinarizer
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sys,os

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    age: str
    workclass: str
    fnlwgt: float
    education: str
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capitalgain: str
    capitalloss: str
    hoursperweek: str

@app.post("/predict")
def predict(item:Item):
    item:dict = item.dict()
    df = pd.DataFrame(item,index=[1])
    df = df.rename(columns={"marital_status":"marital-status"})
    model:Pipeline = joblib.load("model.joblib")
    yenc:LabelBinarizer = joblib.load("ytransform.joblib")
    pred = yenc.inverse_transform(model.predict(df))
    return {"prediction":pred[0]}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    df = pd.read_csv(file.file)
    model:Pipeline = joblib.load("model.joblib")
    yenc:LabelBinarizer = joblib.load("ytransform.joblib")
    cat_cols:List[str] = model.named_steps["preprocessor"].transformers[1][-1]
    num_cols:List[str] = model.named_steps["preprocessor"].transformers[0][-1]
    for col in df.columns:
        if col in cat_cols:
            df[col] = df[col].astype("str")
        elif col in num_cols:
            df[col] = pd.to_numeric(df[col]).round(3)
    df = df.dropna(subset=cat_cols + num_cols)
    preds = model.predict(df)
    df["predicted"] = yenc.inverse_transform(preds)
    return {"data":df.to_dict(orient="records")}
    


