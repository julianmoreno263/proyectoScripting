#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# El directorio del proyecto es el mismo que el directorio del script
PROJECT_DIR="$SCRIPT_DIR"

# Cambiar al directorio del proyecto para asegurar que todas las operaciones relativas funcionen
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


# Log del inicio del proceso de envío de correos
echo "--- Iniciando el proceso de envío de correos: $(date) ---"


PYTHON_SENDER_SCRIPT="enviador.py"

SENDER_LOG="/tmp/enviador_cron.log" 

echo "Ejecutando $PYTHON_SENDER_SCRIPT..."
"$PROJECT_DIR/$PYTHON_SENDER_SCRIPT" >> "$SENDER_LOG" 2>&1
SENDER_EXIT_CODE=$?
if [ $SENDER_EXIT_CODE -ne 0 ]; then
    echo "Error al ejecutar $PYTHON_SENDER_SCRIPT. Código de salida: $SENDER_EXIT_CODE" >> "$SENDER_LOG"
    cat "$SENDER_LOG" >&2 
    exit $SENDER_EXIT_CODE
fi
echo "$PYTHON_SENDER_SCRIPT terminado."

echo "--- Proceso de envío de correos completado: $(date) ---"