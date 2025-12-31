"""
API Flask pour la détection de spam d'emails - Version Simplifiée
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de Flask
app = Flask(__name__)

# Variables globales pour le modèle
MODEL = None
VECTORIZER = None

def load_ml_models():
    """
    Charge le modèle ML et le vectorizer depuis les fichiers pickle
    """
    global MODEL, VECTORIZER
    
    try:
        # Chemin relatif
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'model.pkl')
        vectorizer_path = os.path.join(base_dir, 'vectorizer.pkl')
        
        # Pour debug: afficher les chemins
        print(f"Recherche du modèle à: {model_path}")
        print(f"Recherche du vectorizer à: {vectorizer_path}")
        
        # Vérifier si les fichiers existent
        if not os.path.exists(model_path):
            print(f"❌ Fichier modèle non trouvé: {model_path}")
            # Créer un modèle minimal si non existant
            create_minimal_model()
            MODEL = joblib.load(model_path)
        else:
            MODEL = joblib.load(model_path)
            
        if not os.path.exists(vectorizer_path):
            print(f"❌ Fichier vectorizer non trouvé: {vectorizer_path}")
            # Créer un vectorizer minimal si non existant
            create_minimal_model()
            VECTORIZER = joblib.load(vectorizer_path)
        else:
            VECTORIZER = joblib.load(vectorizer_path)
        
        print("✅ Modèle et vectorizer chargés avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {str(e)}")
        # Créer un modèle minimal d'urgence
        create_minimal_model()
        MODEL = joblib.load(os.path.join(base_dir, 'model.pkl'))
        VECTORIZER = joblib.load(os.path.join(base_dir, 'vectorizer.pkl'))

def create_minimal_model():
    """
    Crée un modèle minimal si les fichiers sont manquants
    """
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction.text import CountVectorizer
    import pandas as pd
    
    print("🔧 Création d'un modèle minimal...")
    
    # Données d'entraînement minimales
    data = pd.DataFrame({
        'text': [
            'gagner million dollars gratuitement',
            'cliquez ici pour prix exclusif',
            'offre spéciale limitée dans le temps',
            'urgent répondez immédiatement',
            'réunion demain à 10 heures',
            'bonjour voici le rapport mensuel',
            'merci pour votre collaboration',
            'prochain rendez-vous jeudi prochain'
        ],
        'label': [1, 1, 1, 1, 0, 0, 0, 0]  # 1=spam, 0=ham
    })
    
    # Vectorisation
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data['text'])
    
    # Modèle
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, data['label'])
    
    # Sauvegarde
    base_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(model, os.path.join(base_dir, 'model.pkl'))
    joblib.dump(vectorizer, os.path.join(base_dir, 'vectorizer.pkl'))
    
    print("✅ Modèle minimal créé et sauvegardé")

# Charger les modèles au démarrage
print("🚀 Démarrage de l'application Flask...")
load_ml_models()

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Page d'accueil avec l'interface web"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de vérification de santé"""
    status = {
        'status': 'healthy' if MODEL is not None else 'unhealthy',
        'model_loaded': MODEL is not None,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
    return jsonify(status), 200

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Endpoint API pour la prédiction de spam
    """
    try:
        # Validation
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 415
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Clé "text" manquante'}), 400
        
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Texte vide'}), 400
        
        # Vérifier que les modèles sont chargés
        if MODEL is None or VECTORIZER is None:
            return jsonify({'error': 'Modèle non chargé'}), 503
        
        # Vectorisation
        text_vectorized = VECTORIZER.transform([text])
        
        # Prédiction
        prediction = MODEL.predict(text_vectorized)[0]
        probabilities = MODEL.predict_proba(text_vectorized)[0]
        
        # Résultats
        is_spam = bool(prediction)
        spam_prob = round(float(probabilities[1]) * 100, 2)
        ham_prob = round(float(probabilities[0]) * 100, 2)
        
        # Mots-clés suspects
        spam_keywords = ['gagner', 'gratuit', 'million', 'dollar', 'prix', 
                        'cliquez', 'offre', 'exclusif', 'urgent', 'limité']
        detected = [word for word in spam_keywords if word in text.lower()]
        
        response = {
            'success': True,
            'data': {
                'prediction': 'SPAM' if is_spam else 'HAM',
                'is_spam': is_spam,
                'probabilities': {
                    'spam': spam_prob,
                    'ham': ham_prob
                },
                'confidence': 'Élevé' if max(probabilities) > 0.8 else 'Moyen' if max(probabilities) > 0.6 else 'Faible',
                'analysis': {
                    'text_length': len(text),
                    'word_count': len(text.split()),
                    'detected_keywords': detected
                },
                'message': 'SPAM détecté!' if is_spam else 'Email légitime',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        print(f"✅ Prédiction: {'SPAM' if is_spam else 'HAM'} ({spam_prob}%)")
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Erreur lors de la prédiction: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Endpoint de test simple"""
    return jsonify({
        'message': 'API fonctionnelle',
        'timestamp': datetime.now().isoformat(),
        'model_status': 'loaded' if MODEL else 'not loaded'
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trouvé'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Erreur interne du serveur',
        'details': str(error) if app.debug else None
    }), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    # Démarrage du serveur
    host = '0.0.0.0'
    port = 5000
    debug = True
    
    print(f"🌐 Serveur démarré sur http://{host}:{port}")
    print(f"📊 Modèle chargé: {MODEL is not None}")
    print(f"🔧 Mode debug: {debug}")
    
    app.run(host=host, port=port, debug=debug)