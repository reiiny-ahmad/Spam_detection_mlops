# tests/test_api.py
import pytest
from api.app import app  # importe ton application Flask


@pytest.fixture
def client():
    """Crée un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_predict_endpoint_exists(client):
    """Vérifie que la route /predict existe et répond"""
    response = client.post('/predict', json={'text': 'Gagnez 1 million maintenant !'})
    assert response.status_code in [200, 400, 422]  # 200 OK ou erreur attendue


def test_predict_returns_json(client):
    """Vérifie que la réponse est bien du JSON"""
    response = client.post('/predict', json={'text': 'Bonjour comment vas-tu ?'})
    assert response.is_json
    data = response.get_json()
    assert 'prediction' in data or 'result' in data or 'spam' in data  # adapte selon ta clé


def test_predict_input_missing(client):
    """Teste le cas où le champ text manque"""
    response = client.post('/predict', json={})
    assert response.status_code in [400, 422]
    assert 'error' in response.get_json()