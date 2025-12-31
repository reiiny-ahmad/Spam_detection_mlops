def test_addition():
    """Test basique pour vérifier que pytest fonctionne"""
    assert 1 + 1 == 2

def test_imports():
    """Test des imports"""
    try:
        import flask
        import sklearn
        import pandas
        import joblib
        import numpy
        assert True
    except ImportError:
        assert False, "Certaines dépendances ne sont pas installées"