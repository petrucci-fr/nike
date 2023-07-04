import os
from datetime import datetime
from pathlib import Path
from configparser import ConfigParser
import ast

config = ConfigParser(interpolation=None)
config.read('config.ini')

"""
-----------------
General Settings
-----------------
"""
DEBUG_MODE = True


"""
-----------------
Database Settings
-----------------
"""
db = config['MINERVA']
MINERVA_CONNECTION = f'mssql+pymssql://{db["USER"]}:{db["PASS"]}@{db["HOST"]}/{db["DATABASE"]}'

"""
-----------------
Email Settings
-----------------
"""
email = config['EMAIL']
EMAIL_CONFIG = {
    'host': email["HOST"],
    'port': int(email["PORT"]),
    'sender': email["SENDER"],
    'debug_recipients': ast.literal_eval(email["DEBUG_RECIPIENTS"]),
    'recipients': ast.literal_eval(email["RECIPIENTS"]),
    'user': email["USER"],
    'pass': email["PASS"],
    'subject': "Envíos Nike - " + datetime.now().strftime("%d/%m/%Y"),
    'message': f"""Hola,\n\n el envío de archivos de ventas y stock de Nike se ha realizado con éxito.\n\nMuchas gracias. \n\nSaludos, \n\n""",
    'signature': """DABRATEC – BI - Servicio Automático de Reporte
C. Panamericana Km. 25.600 | B1611 |  Don Torcuato | Buenos Aires |  Argentina
dexter.com.ar |  stockcenter.com.ar | moovbydexter.com.ar

Por consultas contactar a dabratecbi@grupodabra.com.ar
La información contenida en este mail es confidencial y restringida únicamente a los destinatarios del presente mail. 
Si usted no es el destinatario/s tenga en cuenta que cualquier distribución, copia o uso de esta comunicación o la información que contiene está estrictamente prohibida. 
Si usted ha recibido esta comunicación por error por favor notifíquelo por correo electrónico o por teléfono."""
}  

"""
-----------------
Nike FTP Server Settings
-----------------
"""
ftp = config['NIKE_FTP']
FTP_CONFIG = {
    'host': ftp["HOST"],
    'port': int(ftp["PORT"]),
    'user': ftp["USER"],
    'pass': ftp["PASS"],
    'timeout': int(ftp["TIMEOUT"]),
    'passive_mode': ftp["PASSIVE_MODE"],
    'acct': ftp["ACCT"]
}

"""
-----------------
General Settings
-----------------
"""
#ROOT_PATH='C:\\Users\\mcarballo\\Sistemas\\Proyectos\\Nike'
ROOT_PATH = Path(__file__).parent.parent

LOGS_PATH = os.path.join(ROOT_PATH, 'logs')
os.makedirs(LOGS_PATH, exist_ok=True)

QUERIES_PATH = os.path.join(ROOT_PATH, 'sql_queries')
os.makedirs(QUERIES_PATH, exist_ok=True)

REPORTS_FOLDER_PATH = os.path.join(ROOT_PATH, r"deliverables\reports")
BACKUP_FOLDER_PATH = os.path.join(ROOT_PATH, r"deliverables\backup")
UPLOADS_FOLDER_PATH = '\\\\172.16.0.70\\posnike-uploads\\UPLOADS'
