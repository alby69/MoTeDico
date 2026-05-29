import pytest
from fastapi.testclient import TestClient
from motedico.web.app import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "MoTeDico" in response.text

def test_create_project_web():
    response = client.post(
        "/projects",
        data={"title": "Web Project", "description": "Description", "owner": "WebUser"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert "Web Project" in response.text

def test_project_not_found_web():
    response = client.get("/projects/non_existent")
    assert response.status_code == 404
