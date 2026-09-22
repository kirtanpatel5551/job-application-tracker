import os
os.environ["DATABASE_URL"] = "sqlite:///./test_jobtracker.db"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

def setup_module():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_register_login_and_crud():
    r = client.post("/auth/register", json={"email": "test@example.com", "password": "secret123"})
    assert r.status_code == 201

    r = client.post("/auth/login", data={"username": "test@example.com", "password": "secret123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "company": "Example Corp",
        "position": "Python Developer",
        "location": "Philadelphia, PA",
        "status": "Applied",
        "job_url": "https://example.com/job",
        "notes": "Portfolio test application"
    }
    r = client.post("/api/applications", json=payload, headers=headers)
    assert r.status_code == 201
    application_id = r.json()["id"]

    r = client.get("/api/applications", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1

    payload["status"] = "Interview"
    r = client.put(f"/api/applications/{application_id}", json=payload, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "Interview"

    r = client.get("/api/dashboard", headers=headers)
    assert r.status_code == 200
    assert r.json()["interview"] == 1

    r = client.delete(f"/api/applications/{application_id}", headers=headers)
    assert r.status_code == 204
