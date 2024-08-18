from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import pytest


@pytest.fixture
def client():
    yield TestClient(app)

def test_root(client):
    response=client.get("/")
    print(response.json())
    assert response.json() == "Hello World"
    assert response.status_code == 200

def test_create_user(client):
    res =client.post("/users/",json={
        "email":"joe123@gmail.com",
       "password":"12345"
    })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "joe123@gmail.com"
    assert res.status_code ==201