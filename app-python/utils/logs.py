import requests
from datetime import datetime
from utils.config import LOGS_API_URL

APPLICATION_NAME = "API_Python"  # Nombre de tu aplicación

def send_log(log_type, module, summary, description=None):
    try:
        log_data = {
            "applicationName": APPLICATION_NAME,
            "logType": log_type,  # Ej: INFO, ERROR, WARNING
            "module": module,  # Ej: AuthModule, UserModule
            "summary": summary,  # Resumen corto del log
            "description": description or "",  # Detalles adicionales
            "timestamp": datetime.now().isoformat()  # ISO formato de la fecha actual
        }
        # Enviar el log al sistema de logs
        response = requests.post(LOGS_API_URL, json=log_data)
        # Mostrar que respondio
        print(f"Log enviado: {response}")
        response.raise_for_status()
    except Exception as e:
        print(f"Error al enviar el log: {e}")
