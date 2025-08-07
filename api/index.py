import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api import create_app

app = create_app()


