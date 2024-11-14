# config.py
import os

class Config:
    # Secret key to maintain session security
    SECRET_KEY = os.environ.get('secret_key.py')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'  # Using SQLite for development
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables modification tracking to save memory

    # Mail server configuration for sending emails (e.g., appointment confirmation)
    MAIL_SERVER = 'smtp.gmail.com'  
    MAIL_PORT = 587  # Port for TLS
    MAIL_USE_TLS = True  # Enable Transport Layer Security
    MAIL_USERNAME = os.environ.get('Medease55')  # Your email username, ideally set in environment variables
    MAIL_PASSWORD = os.environ.get('Medease@123')  # Your email password, also ideally set in environment variables
