#!/bin/bash

# --- Determinar el directorio del script (¡esto evita quemar rutas!) ---

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# El directorio del proyecto es el mismo que el directorio del script
PROJECT_DIR="$SCRIPT_DIR"


cd "$PROJECT_DIR" || { echo "Error: No se pudo cambiar al directorio $PROJECT_DIR" >&2; exit 1; }

#Activación del Entorno Conda

CONDA_INIT_SCRIPT="/home/julian/miniconda3/etc/profile.d/conda.sh"
CONDA_ENV_NAME="scripting"

if [ -f "$CONDA_INIT_SCRIPT" ]; then
    source "$CONDA_INIT_SCRIPT"
    conda activate "$CONDA_ENV_NAME"
    if [ $? -ne 0 ]; then
        echo "Error: No se pudo activar el entorno Conda '$CONDA_ENV_NAME'." >&2
        exit 1
    fi
else
    echo "Error: Archivo conda.sh no encontrado. Verifica la ruta: $CONDA_INIT_SCRIPT" >&2
    exit 1
fi


# Log del inicio del proceso
echo "--- Iniciando el proceso de generación de facturas: $(date) ---"

# --- Ejecutar el script de Python ---
# Ahora usamos rutas relativas al $PROJECT_DIR, que ya hemos cambiado
PYTHON_SCRIPT="generador_compras.py"
PYTHON_LOG="/tmp/generador_compras_cron.log" 

echo "Ejecutando $PYTHON_SCRIPT..."
"$PROJECT_DIR/$PYTHON_SCRIPT" >> "$PYTHON_LOG" 2>&1
PYTHON_EXIT_CODE=$?
if [ $PYTHON_EXIT_CODE -ne 0 ]; then
    echo "Error al ejecutar $PYTHON_SCRIPT. Código de salida: $PYTHON_EXIT_CODE" >> "$PYTHON_LOG"
    cat "$PYTHON_LOG" >&2 
    exit $PYTHON_EXIT_CODE
fi
echo "$PYTHON_SCRIPT terminado."


BASH_SCRIPT="generador_facturas.sh"
BASH_LOG="/tmp/generar_facturas_cron.log" 

echo "Ejecutando $BASH_SCRIPT..."
"$PROJECT_DIR/$BASH_SCRIPT" >> "$BASH_LOG" 2>&1
BASH_EXIT_CODE=$?
if [ $BASH_EXIT_CODE -ne 0 ]; then
    echo "Error al ejecutar $BASH_SCRIPT. Código de salida: $BASH_EXIT_CODE" >> "$BASH_LOG"
    cat "$BASH_LOG" >&2 
    exit $BASH_EXIT_CODE
fi
echo "$BASH_SCRIPT terminado."

echo "--- Proceso de generación de facturas completado: $(date) ---"