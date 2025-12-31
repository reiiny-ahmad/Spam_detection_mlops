FROM python:3.9-slim

WORKDIR /app

# Copie les dépendances en premier (bon pour le cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copie le code source (depuis la racine du projet)
COPY api/ ./api/
COPY model/ ./model/

EXPOSE 5000

# Démarrage (ajoute gunicorn dans requirements.txt pour cette version)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api.app:app"]
# Alternative sans gunicorn (pour tester vite) :
# CMD ["python", "-m", "flask", "--app", "api.app", "run", "--host=0.0.0.0"]