from pathlib import Path
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs
from testcontainers.core.image import DockerImage
from testcontainers.generic import ServerContainer
import os
import sys
import pytest

path = os.getcwd()
parent_path = Path("../").resolve()

if str(parent_path) not in sys.path:
    sys.path.append(str(parent_path))
if path not in sys.path:
    sys.path.append(path)

print(sys.path)


def test_predict_endpoint():
    prom_path = Path("../Prometheus").resolve()
    print(str(prom_path))

    # setup jaeger
    jaeger_cont = DockerContainer(image="jaegertracing/all-in-one:latest")
    jaeger_cont.with_exposed_ports(4318)
    with jaeger_cont as jaeger:
        with DockerImage(path=str(prom_path)) as prom_image:
            with DockerContainer(image=str(prom_image)) as prom_cont:
                with DockerImage("../FluentBit") as fluent_image:
                    fluent_container = DockerContainer(image=str(fluent_image))
                    fluent_container.with_volume_mapping(
                        host="log_dir", container="/app/monitoring", mode="rw"
                    )
                    with fluent_container:
                        # make sure to build api image before hand
                        api_image = "ml-webapp-api:latest"
                        server = ServerContainer(port=8000, image=str(api_image))
                        server.with_env("JAEGER_HOST", jaeger.get_container_host_ip())
                        server.with_env("JAEGER_PORT", jaeger.get_exposed_port(4318))
                        server.with_volume_mapping(
                            host="log_dir", container="/app/monitoring", mode="rw"
                        )
                        with server:
                            delay = wait_for_logs(
                                server, "Uvicorn running on http://0.0.0.0:8000"
                            )
                            server.get_api_url = lambda: server._create_connection_url()
                            client = server.get_client()

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

def test_upload_endpoint():
    prom_path = Path("../Prometheus").resolve()
    print(str(prom_path))

    # setup jaeger
    jaeger_cont = DockerContainer(image="jaegertracing/all-in-one:latest")
    jaeger_cont.with_exposed_ports(4318)
    with jaeger_cont as jaeger:
        with DockerImage(path=str(prom_path)) as prom_image:
            with DockerContainer(image=str(prom_image)) as prom_cont:
                with DockerImage("../FluentBit") as fluent_image:
                    fluent_container = DockerContainer(image=str(fluent_image))
                    fluent_container.with_volume_mapping(
                        host="log_dir", container="/app/monitoring", mode="rw"
                    )
                    with fluent_container:
                        # make sure to build api image before hand
                        api_image = "ml-webapp-api:latest"
                        server = ServerContainer(port=8000, image=str(api_image))
                        server.with_env("JAEGER_HOST", jaeger.get_container_host_ip())
                        server.with_env("JAEGER_PORT", jaeger.get_exposed_port(4318))
                        server.with_volume_mapping(
                            host="log_dir", container="/app/monitoring", mode="rw"
                        )
                        with server:
                            delay = wait_for_logs(
                                server, "Uvicorn running on http://0.0.0.0:8000"
                            )
                            server.get_api_url = lambda: server._create_connection_url()
                            client = server.get_client()

                            payload = {"file":open("test.csv","rb")
                            }
                            response = client.post("/uploadfile", files=payload)
                            assert response.status_code == 200
                            
