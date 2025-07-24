#!/bin/bash


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

BASE_DIR="$SCRIPT_DIR"

cd "$BASE_DIR" || { echo "Error: No se pudo cambiar al directorio $BASE_DIR" >&2; exit 1; }

# Directorios
mkdir -p facturas logs pendientes

LOG_DIARIO="logs/log_diario.log"
echo "----- LOG DEL DÍA: $(date) -----" >> "$LOG_DIARIO"

# Archivo CSV pasado como parámetro
CSV_FILE=$(ls -t "$BASE_DIR"/*.csv 2>/dev/null | head -n 1)
# CSV_FILE="$1"

if [[ -z "$CSV_FILE" ]]; then 
  echo "Error: No se encontró ningún archivo CSV en $BASE_DIR." >> "$LOG_DIARIO"
  exit 1
fi

# Limpiar archivo pendientes
> pendientes/pendientes_envio.csv

# Leer CSV saltando la cabecera
tail -n +2 "$CSV_FILE" | while IFS=',' read -r nombre ciudad direccion correo telefono ip cantidad monto modalidad estado timestamp
do
  # Limpiar espacios y comillas
  nombre=$(echo "$nombre" | sed 's/^ *//;s/ *$//;s/"//g')
  ciudad=$(echo "$ciudad" | sed 's/^ *//;s/ *$//;s/"//g')
  direccion=$(echo "$direccion" | sed 's/^ *//;s/ *$//;s/"//g')
  correo=$(echo "$correo" | sed 's/^ *//;s/ *$//;s/"//g')
  telefono=$(echo "$telefono" | sed 's/^ *//;s/ *$//;s/"//g')
  cantidad=$(echo "$cantidad" | sed 's/^ *//;s/ *$//;s/"//g')
  monto=$(echo "$monto" | sed 's/^ *//;s/ *$//;s/"//g')
  modalidad=$(echo "$modalidad" | sed 's/^ *//;s/ *$//;s/"//g')
  estado=$(echo "$estado" | sed 's/^ *//;s/ *$//;s/"//g')
  timestamp=$(echo "$timestamp" | sed 's/^ *//;s/ *$//;s/"//g')

  # Nombre de archivo seguro (sin espacios)
  nombre_limpio=$(echo "$nombre" | tr ' ' '_' | tr -d ',')
  archivo_tex="facturas/factura_${nombre_limpio}.tex"
  archivo_pdf="facturas/factura_${nombre_limpio}.pdf"
  log_factura="logs/factura_${nombre_limpio}.log"

  # Copiar plantilla a nuevo archivo .tex
  cp template.tex "$archivo_tex"

  # Reemplazar placeholders en el .tex con sed
  sed -i "s/{nombre}/$nombre/g" "$archivo_tex"
  sed -i "s/{ciudad}/$ciudad/g" "$archivo_tex"
  sed -i "s/{direccion}/$direccion/g" "$archivo_tex"
  sed -i "s/{correo}/$correo/g" "$archivo_tex"
  sed -i "s/{telefono}/$telefono/g" "$archivo_tex"
  sed -i "s/{cantidad}/$cantidad/g" "$archivo_tex"
  sed -i "s/{monto}/$monto/g" "$archivo_tex"
  sed -i "s/{modalidad}/$modalidad/g" "$archivo_tex"
  sed -i "s/{estado}/$estado/g" "$archivo_tex"
  sed -i "s/{timestamp}/$timestamp/g" "$archivo_tex"

  # Compilar pdf con pdflatex
  pdflatex -interaction=nonstopmode -output-directory facturas "$archivo_tex" > "$log_factura" 2>&1

  # Revisar si hubo error (buscar líneas con "!")
  if grep -q "^!" "$log_factura"; then
    echo "Error en factura $archivo_pdf. Ver logs $log_factura"
    # Guardar en pendientes
    echo "$archivo_pdf,$correo" >> pendientes/pendientes_envio.csv
    echo "$(date) ERROR factura $archivo_pdf" >> "$LOG_DIARIO"
  else
    echo "Factura generada: $archivo_pdf"
    echo "$(date) OK factura $archivo_pdf" >> "$LOG_DIARIO"
    echo "$archivo_pdf,$correo" >> pendientes/pendientes_envio.csv
  fi

done

echo "Proceso terminado. Revisa $LOG_DIARIO y pendientes/pendientes_envio.csv"
