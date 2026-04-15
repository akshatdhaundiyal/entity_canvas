import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Provides a TestClient for FastAPI endpoints."""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_ast():
    """Provides a basic valid QueryAST structure."""
    return {
        "select": [{"table": "users", "column": "name"}],
        "from": "users",
        "limit": 10
    }
