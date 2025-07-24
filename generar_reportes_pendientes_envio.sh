#!/bin/bash

# Ruta al archivo generado 
ENTRADA="pendientes/pendientes_envio.csv"
SALIDA="pendientes_envio.csv"

# Verifica si existe el archivo de entrada
if [ ! -f "$ENTRADA" ]; then
  echo "El archivo $ENTRADA no existe. Ejecuta primero el generador de facturas."
  exit 1
fi

# Encabezado de la salida
echo "name,ruta,estado,correo" > "$SALIDA"

# Leer archivo línea por línea
while IFS=',' read -r ruta correo
do
  # Extraer nombre desde el nombre del archivo PDF
  nombre=$(basename "$ruta" .pdf | sed 's/factura_//' | tr '_' ' ')
  
  echo "$nombre,$ruta,pendientes,$correo" >> "$SALIDA"

done < "$ENTRADA"

echo "Reporte generado en: $SALIDA"
