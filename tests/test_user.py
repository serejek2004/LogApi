import pytest
from app import app, db
# to start use export PYTHONPATH=$(pwd) + pytest

@pytest.fixture
def client():
    app.config.from_object('app.config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_register(client):
    response = client.post('/user/register', json={"username": "user", "password": "1234"})

    assert response.status_code == 201
    assert response.get_json()["id"] == 1
    assert response.get_json()["username"] == "user"


def test_get_all(client):
    client.post('/user/register', json={"username": "user1", "password": "1234"})
    client.post('/user/register', json={"username": "user2", "password": "4321"})

    response = client.get('/user')

    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_login(client):
    client.post('/user/register', json={"username": "user1", "password": "1234"})
    response = client.post('/user/login', json={"username": "user1", "password": "1234"})

    assert response.status_code == 200

    response = client.post('/user/login', json={"username": "user2", "password": "43"})

    assert response.status_code == 404
