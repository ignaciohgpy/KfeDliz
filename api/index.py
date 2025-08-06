import sys
import os

# Agrega la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Importa la app desde index.py
from index import app

