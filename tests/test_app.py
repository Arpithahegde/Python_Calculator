
import pytest
from app import app, calculate


@pytest.mark.parametrize("a,b,operation,expected", [
    (10, 5, "add", 15),
    (10, 5, "subtract", 5),
    (10, 5, "multiply", 50),
    (3, 8, "subtract", -5)
])
def test_calculate(a, b, operation, expected):
    assert calculate(a, b, operation) == expected


@pytest.mark.parametrize("value", [0, -1, 1.5, "5", True, None])
def test_invalid_inputs(value):
    with pytest.raises(ValueError):
        calculate(value, 5, "add")


def test_invalid_operation():
    with pytest.raises(ValueError):
        calculate(10, 5, "divide")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_calculator_api(client):
    response = client.post(
        "/calculate",
        json={"a": 10, "b": 5, "operation": "multiply"}
    )

    assert response.status_code == 200
    assert response.json["result"] == 50


def test_invalid_api_input(client):
    response = client.post(
        "/calculate",
        json={"a": 0, "b": 5, "operation": "add"}
    )

    assert response.status_code == 400
