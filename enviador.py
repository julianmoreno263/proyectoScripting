#!/home/julian/miniconda3/envs/scripting/bin/python

import csv
import re
import smtplib
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime

# --- Configuración de Mailtrap ---
SMTP_SERVER = 'sandbox.smtp.mailtrap.io'
SMTP_PORT = 2525
SENDER_EMAIL = '4aa080c9bbd88e'
SENDER_PASSWORD = '15fa8788acf514'

# obtener rutas de archivos y carpetas para poder ejecutarlos con cron
script_dir = os.path.dirname(os.path.abspath(__file__))

PENDING_FILE = os.path.join(script_dir, 'pendientes_envio.csv')
PDF_FOLDER = os.path.join(script_dir, 'facturas') 
LOG_CSV_FILE = os.path.join(script_dir, 'log_envios.csv') 


# --- Expresión Regular para Validación de Correo ---
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def enviar_email_adjunto(destino, asunto, cuerpo, archivoAdjunto):
   
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = destino
        msg['Subject'] = asunto

        # Adjuntar el cuerpo del correo como texto plano
        msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))

        # Adjuntar PDF
        if not os.path.exists(archivoAdjunto):
            raise FileNotFoundError(f"Archivo adjunto no encontrado: {archivoAdjunto}")

        with open(archivoAdjunto, 'rb') as adjunto:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(adjunto.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(archivoAdjunto)}',
        )
        msg.attach(part)

        # Conexión con el servidor SMTP de Mailtrap
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Mailtrap usa TLS para encriptación
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True, "exitoso" # Cambiado a "exitoso" para el log CSV
    except FileNotFoundError:
        return False, "fallido - Archivo PDF no encontrado"
    except smtplib.SMTPException as smtp_error:
        return False, f"fallido - Error SMTP: {smtp_error}"
    except Exception as e:
        return False, f"fallido - Error inesperado: {e}"

def registrar_envios_correo(pending_rows_data, log_entries_csv_data):
  
    # --- Actualizar pendientes_envio.csv ---
    # Crear un nuevo DataFrame con las filas que deben permanecer en pendientes
    df_new_pending = pd.DataFrame(pending_rows_data, columns=['invoice_name', 'recipient_email'])
    # Sobrescribir el archivo original con las filas pendientes
    df_new_pending.to_csv(PENDING_FILE, index=False, header=False, encoding='utf-8')
    print(f"\nArchivo '{PENDING_FILE}' actualizado. Se han eliminado las líneas exitosas.")

    # --- Generar log_envios.csv ---
    # Crear un DataFrame con todas las entradas de log
    df_log_csv = pd.DataFrame(log_entries_csv_data)
    # Guardar el log en un nuevo archivo CSV
    df_log_csv.to_csv(LOG_CSV_FILE, index=False, encoding='utf-8')
    print(f"Archivo de log '{LOG_CSV_FILE}' generado con los resultados de los envíos.")



def main():
 
    # Verificar si la carpeta de PDFs existe
    if not os.path.exists(PDF_FOLDER):
        print(f"Error: La carpeta '{PDF_FOLDER}' no existe. Por favor, créala y coloca los PDFs de las facturas allí.")
        return

    # Verificar si el archivo CSV de pendientes existe
    if not os.path.exists(PENDING_FILE):
        print(f"Error: El archivo '{PENDING_FILE}' no se encontró. Asegúrate de que exista y esté en el mismo directorio.")
        return

    # Listas para almacenar los datos a procesar y los resultados de los logs
    pending_rows = [] # Para almacenar las filas que deben permanecer en pendientes_envio.csv
    log_entries_csv = []  # Para almacenar todas las entradas del log_envios.csv
   

    try:
        # Leer el archivo CSV de pendientes en un DataFrame de pandas
        # Se asume que el CSV no tiene encabezados y contiene dos columnas
        df_pending = pd.read_csv(PENDING_FILE, header=None, names=['invoice_name', 'recipient_email'])

        if df_pending.empty:
            print("El archivo pendientes_envio.csv está vacío. No hay correos para enviar.")
            return

        # Iterar sobre cada fila del DataFrame
        for index, row in df_pending.iterrows():
            invoice_name = str(row['invoice_name']).strip()
            recipient_email = str(row['recipient_email']).strip()
            pdf_path = os.path.join(PDF_FOLDER, invoice_name)
            
            current_status_csv = "" # Para el estado final del intento de envío en el CSV

            print(f"Procesando: {invoice_name} para {recipient_email}...")

            # Validar formato del correo electrónico
            if not re.match(EMAIL_REGEX, recipient_email):
                current_status_csv = "fallido - Formato de correo inválido"

                print(f"Error: Correo inválido para '{recipient_email}'. Se ha registrado en el log.")
                pending_rows.append([invoice_name, recipient_email]) # Mantener en pendientes
            elif not os.path.exists(pdf_path):
                current_status_csv = "fallido - Archivo PDF no encontrado"
                # current_status_txt = "ERROR" (eliminado)
                # current_message_txt = "Archivo PDF no encontrado." (eliminado)
                print(f"Error: Archivo PDF no encontrado para '{invoice_name}'. Se ha registrado en el log.")
                pending_rows.append([invoice_name, recipient_email]) # Mantener en pendientes
            else:
                # Si las validaciones básicas pasan, intentar enviar el correo
                subject = f"Tu Factura: {invoice_name.replace('.pdf', '')}"
                body = f"Estimado cliente,\n\nAdjuntamos tu factura {invoice_name}. Gracias por tu compra.\n\nSaludos cordiales,\nTu Empresa"
                success, message = enviar_email_adjunto(recipient_email, subject, body, pdf_path)
                
                current_status_csv = message # 'exitoso' o 'fallido - ...'

                if not success:
                    pending_rows.append([invoice_name, recipient_email]) # Si falla, mantener en pendientes
                    print(f"Fallo al enviar correo a {recipient_email} para {invoice_name}: {message}. Se ha registrado en el log.")
                else:
                    print(f"Correo enviado exitosamente a {recipient_email} para {invoice_name}.")
            
    
            # Registrar la entrada en la lista para el log CSV (log_envios.csv)
            log_entries_csv.append({
                'factura': invoice_name,
                'destinatario': recipient_email,
                'estado': current_status_csv
            })
        
        # Una vez procesadas todas las filas, llamar a la función para registrar resultados consolidados
        # Se ha eliminado el argumento log_entries_txt de la llamada
        registrar_envios_correo(pending_rows, log_entries_csv)

    except pd.errors.EmptyDataError:
        print(f"El archivo '{PENDING_FILE}' está vacío o no tiene el formato esperado. No hay correos para procesar.")
    except FileNotFoundError:
        print(f"Error crítico: El archivo '{PENDING_FILE}' no se encontró. Asegúrate de que el nombre y la ruta sean correctos.")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante el procesamiento: {e}")

if __name__ == '__main__':
    main()
