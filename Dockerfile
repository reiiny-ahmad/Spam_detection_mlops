# FROM python:3.9-slim

# WORKDIR /app

# # Copy dependencies first (good for caching)
# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# # Copy your code
# COPY api/ ./api/
# COPY model/ ./model/

# # If you have templates inside api/ (you do!)
# # The COPY api/ already includes templates/

# EXPOSE 5000

# # Use Flask dev server for simplicity (no extra dep needed)
# CMD ["python", "-m", "flask", "--app", "api.app", "run", "--host=0.0.0.0"]


FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt (vérifiez qu'il est à la racine du repo)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier TOUT le contenu du repo
COPY . .

# Alternative: copier spécifiquement ce dont on a besoin
# COPY api/ ./api/
# COPY model/ ./model/
# COPY templates/ ./templates/  # Si templates est séparé

EXPOSE 5000

# Changer la commande CMD
CMD ["python", "api/app.py"]