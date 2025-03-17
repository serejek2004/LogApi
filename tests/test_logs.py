import io
import pytest
from flask_jwt_extended import create_access_token
from app import app, db
# to start use export PYTHONPATH=$(pwd) + pytest


@pytest.fixture
def auth_header():
    with app.app_context():
        access_token = create_access_token(identity="testuser")
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def client():
    app.config.from_object('app.config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_upload_log_file(client, auth_header):
    data = {
        'file': (io.BytesIO(b"[2023-03-12 12:00:00] INFO: User logged in - ID: 123\n"), 'test_log.txt')
    }

    response = client.post('/logs', headers=auth_header, data=data)

    assert response.status_code == 201
    assert "Logs saved successfully" in response.get_json()["message"]

    response = client.get('/logs', headers=auth_header)

    expected_response = [
        {
            "id": 1,
            "created_at": "2023-03-12T12:00:00",
            "log_level": "INFO",
            "log_data": "User logged in - ID: 123",
        }
    ]

    assert response.status_code == 200
    assert response.get_json() == expected_response


def test_get_all_logs(client, auth_header):
    response = client.get('/logs', headers=auth_header)

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_logs_by_time(client, auth_header):
    start_datetime = "2024-01-01T00:00:00"
    end_datetime = "2026-01-01T00:00:00"

    client.post('/logs', headers=auth_header,
                data={'file': (io.BytesIO(b"[2023-03-12 12:00:00] INFO: User logged in - ID: 123\n"
                                          b"[2025-03-12 12:00:00] ERROR: User logged in - ID: 123\n"
                                          b"[2028-03-12 12:00:00] INFO: User logged in - ID: 123"), 'test_log.txt')})

    response = client.get(f'/logs/{start_datetime}/{end_datetime}', headers=auth_header)

    expected_response = [
        {
            "id": 2,
            "created_at": "2025-03-12T12:00:00",
            "log_level": "ERROR",
            "log_data": "User logged in - ID: 123",
        }
    ]

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert response.get_json() == expected_response


def test_get_logs_by_fragment(client, auth_header):
    fragment = "INFO"

    client.post('/logs', headers=auth_header,
                data={'file': (io.BytesIO(b"[2025-03-12 12:00:00] INFO: User logged in - ID: 123\n"
                                          b"[2025-03-12 12:00:00] ERROR: User logged in - ID: 123\n"
                                          b"[2028-03-12 12:00:00] INFO: User logged in - ID: 123"), 'test_log.txt')})

    response = client.get(f'/logs/{fragment}', headers=auth_header)

    expected_response = [
        {
            "id": 1,
            "created_at": "2025-03-12T12:00:00",
            "log_level": "INFO",
            "log_data": "User logged in - ID: 123",
        },
        {
            "id": 3,
            "created_at": "2028-03-12T12:00:00",
            "log_level": "INFO",
            "log_data": "User logged in - ID: 123",
        }
    ]

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert response.get_json() == expected_response


def test_get_logs_by_fragment_and_by_time(client, auth_header):
    fragment = "ERROR"
    start_datetime = "2024-01-01T00:00:00"
    end_datetime = "2026-01-01T00:00:00"

    client.post('/logs', headers=auth_header,
                data={'file': (io.BytesIO(b"[2025-03-12 12:00:00] INFO: User logged in - ID: 123\n"
                                          b"[2025-03-12 12:00:00] ERROR: User logged in - ID: 123\n"
                                          b"[2028-03-12 12:00:00] INFO: User logged in - ID: 123"), 'test_log.txt')})

    response = client.get(f'/logs/{fragment}/{start_datetime}/{end_datetime}', headers=auth_header)

    expected_response = [
        {
            "id": 2,
            "created_at": "2025-03-12T12:00:00",
            "log_level": "ERROR",
            "log_data": "User logged in - ID: 123",
        }
    ]

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert response.get_json() == expected_response
