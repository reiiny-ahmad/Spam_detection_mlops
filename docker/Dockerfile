# # Dockerfile
# FROM python:3.9-slim  # Base image légère avec Python

# WORKDIR /app  # Dossier de travail dans le container

# COPY requirements.txt .  # Copie deps
# RUN pip install --no-cache-dir -r requirements.txt  # Installe sans cache pour réduire taille

# COPY . .  # Copie tout le code (api/, model/, app.py, etc.)

# EXPOSE 5000  # Port exposé pour Flask

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api.app:app"]  # Run avec Gunicorn pour prod (installe gunicorn dans requirements.txt)
# # Ou simplement CMD ["python", "api/app.py"] si tu utilises app.run() en dev


FROM python:3.9-slim

WORKDIR /app

# Copie depuis la racine du projet (pas depuis docker/)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code nécessaire (api/, model/, templates/, etc.)
COPY api/ ./api/
COPY model/ ./model/
COPY setup.py .               # si nécessaire
COPY *.pkl ./                 # ou COPY model/*.pkl ./

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api.app:app"]