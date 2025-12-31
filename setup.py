# setup.py (à la racine du projet)
from setuptools import setup, find_packages

setup(
    name="spam-detection",
    version="0.1",
    packages=find_packages(),  # trouve automatiquement api/, model/, etc.
)