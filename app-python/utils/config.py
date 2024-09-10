from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Acceder a las variables de entorno
MONGO_DETAILS = os.getenv("MONGO_DETAILS")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# config.py
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "marlons.espinosaj@uqvirtual.edu.co"
SMTP_PASSWORD = "dpcc lqjt dooo diru"
FROM_EMAIL = "marlons.espinosaj@uqvirtual.edu.co"
