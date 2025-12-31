# setup.py  (place-le à côté de README.md, requirements.txt, etc.)
from setuptools import setup, find_packages

setup(
    name="spam-detection-mlops",
    version="0.1.0",
    packages=find_packages(),  # trouve automatiquement api/, model/, etc.
    install_requires=[],       # pas besoin, car géré par requirements.txt
)