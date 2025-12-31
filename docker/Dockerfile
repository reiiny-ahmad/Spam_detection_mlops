FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY model/ ./model/

EXPOSE 5000

# Utilise le serveur dev Flask (simple et sans dépendance supplémentaire)
CMD ["python", "-m", "flask", "--app", "api.app", "run", "--host=0.0.0.0"]