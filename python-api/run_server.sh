#!/bin/bash
# Crear el directorio central de caché si no existe
mkdir -p $(pwd)/__pycache_central__

# Configurar Python para usar solo este directorio
export PYTHONPYCACHEPREFIX=$(pwd)/__pycache_central__

# Ejecutar el servidor
uvicorn main:app --reload
