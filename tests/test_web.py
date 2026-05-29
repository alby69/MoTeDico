from fastapi.testclient import TestClient
from motedico.web.app import app
client = TestClient(app)
def test_read_main(): assert client.get("/").status_code == 200
