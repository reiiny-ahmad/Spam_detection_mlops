# tests/test_api.py
import pytest
from api.app import app  # ← Assure-toi que c'est bien from api.app

@pytest.fixture
def client():
    """Crée un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_predict_endpoint_exists(client):
    """Vérifie que la route /api/predict existe et répond"""
    response = client.post('/api/predict', json={'text': 'Gagnez 1 million maintenant !'})
    assert response.status_code in [200, 400, 422]  # 200 OK ou erreur attendue

def test_predict_returns_json(client):
    """Vérifie que la réponse est bien du JSON"""
    response = client.post('/api/predict', json={'text': 'Bonjour comment vas-tu ?'})
    assert response.is_json
    data = response.get_json()
    # Adapte selon la structure réelle de ta réponse (regarde ton endpoint)
    assert 'success' in data or 'prediction' in data.get('data', {}) or 'error' in data

def test_predict_input_missing(client):
    """Teste le cas où le champ text manque"""
    response = client.post('/api/predict', json={})
    assert response.status_code in [400, 422]
    data = response.get_json()
    assert 'error' in data