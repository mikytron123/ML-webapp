
from typing import Literal
from pydantic import BaseModel, Field


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