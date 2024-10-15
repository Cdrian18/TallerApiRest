# rabbitmq_producer.py
import pika
import json
from datetime import datetime
import time

APPLICATION_NAME = "UserManagementAPI"

class RabbitMQProducer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.connect()
        
    def connect(self):
        while not self.connection:
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host='rabbitmq',
                        port=5672,
                        credentials=pika.PlainCredentials('user', 'password')
                    )
                )
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue='logs_queue', durable=True, exclusive=False, auto_delete=False, arguments=None)
                print("Connected to RabbitMQ")
            except pika.exceptions.AMQPConnectionError:
                print("Failed to connect to RabbitMQ. Retrying in 5 seconds...")
                time.sleep(5)

    def send_log(self, log_type, module, summary, description):
        if not self.connection or self.connection.is_closed:
            print("Connection lost. Reconnecting...")
            self.connect()
        
        log_data = {
            "applicationName": APPLICATION_NAME,
            "logType": log_type,  # Ej: INFO, ERROR, WARNING
            "module": module,  # Ej: AuthModule, UserModule
            "summary": summary,  # Resumen corto del log
            "description": description or "",  # Detalles adicionales
            "timestamp": datetime.now().isoformat()  # Fecha en formato ISO
        }

        # Publicar el mensaje en la cola de logs
        self.channel.basic_publish(
            exchange='',
            routing_key='logs_queue',
            body=json.dumps(log_data)
        )
        print(f" [x] Log enviado: {log_data}")

    def close_connection(self):
        self.connection.close()

# Uso en la API
rabbitmq_producer = RabbitMQProducer()

def send_log(log_type, module, summary, description):
    rabbitmq_producer.send_log(log_type, module, summary, description)
