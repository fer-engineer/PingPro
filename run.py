#!/usr/bin/env python3
"""
PING PONG PRO - Archivo principal de ejecución
Ejecutar: python run.py
"""

import sys
import os

# Agregar la carpeta src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()