import os
import signal
from http.client import OK
from pathlib import Path
from subprocess import Popen
from time import sleep
from typing import Iterator

from httpx import Client
from pytest import fixture


def test_server_stores_vehicles_properly(client: Client, clean_workdir: Path, valid_vehicle_features_post: str):
    response = client.post(
        url="/backend/challenge",
        content=valid_vehicle_features_post,
        headers={"content-type": "application/json"}
    )

    assert response.status_code == OK

    customer_dir = Path(next(clean_workdir.iterdir()))
    assert len(list(customer_dir.iterdir())) == 2


@fixture
def client(running_server_url) -> Iterator[Client]:
    with Client(base_url=running_server_url, timeout=2) as client_:
        yield client_


@fixture
def running_server_url(clean_workdir) -> Iterator[str]:
    server_proc = Popen(
        args=["/usr/bin/bash", "-c", "make run"],
        env={
            **os.environ,
            "CAR_CUTTER_FILE_STORE_BASE_DIR": str(clean_workdir),
        },
    )

    # TODO: use a more elegant startup method without sleep
    sleep(2)
    yield "http://127.0.0.1:8080"
    server_proc.send_signal(signal.SIGTERM)
    server_proc.wait()
