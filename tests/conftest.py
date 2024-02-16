from pathlib import Path
from shutil import rmtree
from typing import Iterator

from pytest import fixture

_BASE_DIR = Path(__file__).resolve().parent
_EXAMPLE_REQUESTS_DIR = _BASE_DIR / "example_requests"
_WORKDIR = Path(__file__).resolve().parent / "tmp"


@fixture
def clean_workdir() -> Iterator[Path]:
    if _WORKDIR.exists():
        rmtree(_WORKDIR)

    _WORKDIR.mkdir()
    yield _WORKDIR

    if _WORKDIR.exists():
        rmtree(_WORKDIR)


@fixture(scope="session")
def valid_vehicle_features_post() -> str:
    return _read_request_file("valid_vehicle_features_post.json")


@fixture(scope="session")
def invalid_vehicle_features_post() -> str:
    return _read_request_file("invalid_vehicle_features_post.json")


def _read_request_file(filename: str) -> str:
    return (_EXAMPLE_REQUESTS_DIR / filename).read_text()
