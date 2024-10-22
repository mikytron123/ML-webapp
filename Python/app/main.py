from pathlib import Path
from time import perf_counter
from typing import List
import joblib
from prometheus_client import start_http_server
from sklearn.pipeline import Pipeline
from sklearn.preprocessing._label import LabelBinarizer
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from contextlib import asynccontextmanager
import pandas as pd
import sys
import os
import structlog

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from shared.api_models import BatchPrediction, Item, ModelPrediction

start_http_server(port=8001)

JAEGER_HOST = os.getenv("JAEGER_HOST", default="localhost")

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

resource = Resource(attributes={SERVICE_NAME: "fastapi-ml"})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint=f"http://{JAEGER_HOST}:4318/v1/traces")
)
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

tracer = trace.get_tracer("tracer.fastapi")


metric_reader = PrometheusMetricReader()

meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])

# Sets the global default meter provider
metrics.set_meter_provider(meter_provider)

# Creates a meter from the global meter provider
meter = metrics.get_meter("fastapi.metrics")

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt=None, utc=True),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.WriteLoggerFactory(
        file=Path("/app/monitoring/data.log").with_suffix(".log").open("wt")
    ),
)
log = structlog.get_logger()


y_encoder: LabelBinarizer
model: Pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    global y_encoder
    global model
    y_encoder = joblib.load("app/ytransform.joblib")
    model = joblib.load("app/model.joblib")

    yield


app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(
    app, tracer_provider=traceProvider, meter_provider=meter_provider
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

num_predictions = meter.create_counter(
    name="pred_counter", unit="1", description="counts number of predictions made"
)
request_duration = meter.create_histogram(
    "req_duration", "s", description="counts request duration"
)


@app.post("/predict")
def predict(item: Item) -> ModelPrediction:
    with tracer.start_as_current_span("preprocessing"):
        start_time = perf_counter()
        data: dict = item.model_dump()
        log.info("preprocessing json", role="feature", **data)
        df = pd.DataFrame(data, index=[1])
        df = df.rename(columns={"marital_status": "marital-status"})
    with tracer.start_as_current_span("prediction", record_exception=True):
        pred = y_encoder.inverse_transform(model.predict(df))
        num_predictions.add(amount=1)
        end_time = perf_counter() - start_time
        request_duration.record(amount=end_time)
        log.info("prediction", role="prediction", prediction=str(pred[0]))
        return ModelPrediction(prediction=str(pred[0]))


@app.post("/uploadfile", response_model=list[BatchPrediction])
async def create_upload_file(file: UploadFile):
    with tracer.start_as_current_span("preprocessing"):
        start_time = perf_counter()
        df = pd.read_csv(file.file)
        cat_cols: List[str] = model.named_steps["preprocessor"].transformers[1][-1]
        num_cols: List[str] = model.named_steps["preprocessor"].transformers[0][-1]
        for col in df.columns:
            if col in cat_cols:
                df[col] = df[col].astype("str")
            elif col in num_cols:
                df[col] = pd.to_numeric(df[col]).round(3)
        df = df.dropna(subset=cat_cols + num_cols)
        for row in df.to_dict(orient="records"):
            log.info("preprocessing file", **row, role="feature")
    with tracer.start_as_current_span("prediction", record_exception=True):
        preds = model.predict(df[cat_cols + num_cols])
        df["prediction"] = y_encoder.inverse_transform(preds)
        df["prediction"] = df["prediction"].astype(str)
        num_predictions.add(amount=len(df))
        request_duration.record(perf_counter() - start_time)
        return df.to_dict(orient="records")
