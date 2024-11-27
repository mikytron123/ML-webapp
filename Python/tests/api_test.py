from pathlib import Path
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.core.image import DockerImage
from testcontainers.generic import ServerContainer
import os
import sys
import pytest

path = os.getcwd()
parent_path = Path().parent.resolve()

if str(parent_path) not in sys.path:
    sys.path.append(str(parent_path))
if path not in sys.path:
    sys.path.append(path)


@pytest.fixture(scope="module")
def server_container():
    cur_path = Path(__file__).resolve()
    prom_path = cur_path.parent.parent.parent / "Prometheus"
    fluent_path = cur_path.parent.parent.parent / "FluentBit"

    # setup jaeger
    jaeger_container = DockerContainer(image="jaegertracing/all-in-one:latest")
    jaeger_container.with_exposed_ports(4318)
    jaeger_container.start()

    # setup prometheus
    prom_image = DockerImage(path=str(prom_path))
    prom_image.build()

    prom_container = DockerContainer(image=str(prom_image))
    prom_container.start()

    # setup fluentbit
    fluent_image = DockerImage(str(fluent_path))
    fluent_image.build()

    fluent_container = DockerContainer(image=str(fluent_image))
    fluent_container.with_volume_mapping(
        host="log_dir", container="/app/monitoring", mode="rw"
    )
    fluent_container.start()

    # make sure to build api image before hand
    api_image = "ml-webapp-api:latest"

    server = ServerContainer(port=8000, image=str(api_image))
    server.with_env("JAEGER_HOST", jaeger_container.get_container_host_ip())
    server.with_env("JAEGER_PORT", jaeger_container.get_exposed_port(4318))
    server.with_volume_mapping(host="log_dir", container="/app/monitoring", mode="rw")
    server.start()
    yield server

    server.stop()
    fluent_container.stop()
    fluent_image.remove()
    prom_container.stop()
    prom_image.remove()
    jaeger_container.stop()


def test_predict_endpoint(server_container):
    wait_for_logs(server_container, "Uvicorn running on http://0.0.0.0:8000")
    server_container.get_api_url = lambda: server_container._create_connection_url()
    client = server_container.get_client()

    payload = {
        "age": "0",
        "workclass": "State-gov",
        "fnlwgt": 13492,
        "education": "Bachelors",
        "marital-status": "Never-married",
        "occupation": "Adm-clerical",
        "relationship": "Not-in-family",
        "race": "White",
        "sex": "Male",
        "capitalgain": "0",
        "capitalloss": "0",
        "hoursperweek": "0",
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    print(response.json())


def test_upload_endpoint(server_container):
    wait_for_logs(server_container, "Uvicorn running on http://0.0.0.0:8000")
    server_container.get_api_url = lambda: server_container._create_connection_url()
    client = server_container.get_client()
    cur_path = Path(__file__).resolve()
    csv_path = cur_path.parent.parent / "test.csv"
    payload = {"file": open(str(csv_path.resolve()), "rb")}
    response = client.post("/uploadfile", files=payload)
    assert response.status_code == 200
