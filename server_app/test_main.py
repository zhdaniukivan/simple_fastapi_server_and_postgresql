from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_main():
    response = client.get('/get_questions/')
    assert response.status_code == 405

    # assert response.json() == {}
    #

def test_read_main():
    response = client.get('/get_info/')
    assert response.status_code == 200
    assert response.json() == {'msg': "that program get many questions"}


