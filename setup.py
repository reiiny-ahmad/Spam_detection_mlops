# setup.py
from setuptools import setup, find_packages

setup(
    name="spam-detection-mlops",
    version="0.1.0",
    packages=find_packages(),  # détecte automatiquement api/, model/, etc.
    install_requires=[],       # pas besoin ici, car requirements.txt gère déjà
)