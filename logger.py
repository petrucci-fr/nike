import os
import logging
import logging.handlers
from unidecode import unidecode
from .settings import LOGS_PATH, EMAIL_CONFIG


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name, level=logging.DEBUG)

        # Configure the CLI handler
        stream_handler = logging.StreamHandler()

        # Configure the file handler
        file_handler = logging.FileHandler(os.path.join(LOGS_PATH, f'{unidecode("_".join(name.lower().strip().split()))}.log'))

        # Configure the SMTP handler
        smtp_handler = logging.handlers.SMTPHandler(mailhost=(EMAIL_CONFIG["host"], EMAIL_CONFIG["port"]),
                                                    fromaddr=EMAIL_CONFIG["sender"],
                                                    toaddrs=EMAIL_CONFIG["debug_recipients"],                                                    
                                                    subject=f'{name} - Error',
                                                    credentials=(EMAIL_CONFIG["user"], EMAIL_CONFIG["pass"]),
                                                    secure=())
        
        # Set handlers levels
        stream_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.INFO)  
        smtp_handler.setLevel(logging.ERROR)
      
        # Set the formatter for the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s --> %(message)s\n\n', "%Y-%m-%d %H:%M:%S")
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        smtp_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.addHandler(stream_handler)
        self.addHandler(file_handler)
        self.addHandler(smtp_handler)
