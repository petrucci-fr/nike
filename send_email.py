import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE
from email import encoders
from src.settings import EMAIL_CONFIG
from src.logger import Logger

logger = Logger(__name__)

def send_email(send_from, send_to, subject, body, signature, files=[]):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Subject'] = subject

    msg.attach(MIMEText(body + signature, 'plain'))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path(path).name))
        msg.attach(part)

    try:
        server = smtplib.SMTP(EMAIL_CONFIG["host"], EMAIL_CONFIG["port"])
        server.ehlo()
        server.starttls()
        server.login(EMAIL_CONFIG["user"], EMAIL_CONFIG["pass"])
        text = msg.as_string()
        server.sendmail(send_from, send_to, text)
        server.quit()
    except Exception as e:
        logger.exception(e)