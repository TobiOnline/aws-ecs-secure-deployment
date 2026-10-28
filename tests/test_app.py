import pytest

from app import create_app


@pytest.fixture()
def client():
    return create_app({"TESTING": True}).test_client()


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"service": "aws-ecs-secure-deployment", "status": "ok"}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.is_json
    assert response.json == {"status": "healthy"}


def test_missing_route(client):
    response = client.get("/missing")
    assert response.status_code == 404
    assert response.json == {"error": "Not Found"}


@pytest.mark.parametrize("path", ["/", "/health"])
def test_write_methods_rejected(client, path):
    response = client.post(path, json={"status": "changed"})
    assert response.status_code == 405
    assert "GET" in response.headers["Allow"]
    assert response.json == {"error": "Method Not Allowed"}


def test_unexpected_error_hides_details():
    app = create_app({"TESTING": False})

    @app.get("/test-failure")
    def fail():
        raise RuntimeError("sensitive internal detail")

    response = app.test_client().get("/test-failure")
    assert response.status_code == 500
    assert response.json == {"error": "Internal Server Error"}
    assert b"sensitive internal detail" not in response.data
