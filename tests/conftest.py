import pytest
from fastapi.testclient import TestClient

from app.main import app, reset_storage


@pytest.fixture
def client() -> TestClient:
    reset_storage()
    return TestClient(app)
