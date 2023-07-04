from ftplib import FTP
from .settings import FTP_CONFIG

def connect_ftp():
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(FTP_CONFIG["host"], FTP_CONFIG["port"], FTP_CONFIG["timeout"])
    ftp.set_pasv(FTP_CONFIG["passive_mode"])
    ftp.login(FTP_CONFIG["user"], FTP_CONFIG["pass"], FTP_CONFIG["acct"])
    ftp.getwelcome()
    