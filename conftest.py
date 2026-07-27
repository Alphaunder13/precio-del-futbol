"""Permite que los tests importen `src` sin instalar el paquete."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
