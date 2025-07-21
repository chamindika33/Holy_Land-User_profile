import os
import ssl
import certifi
import smtplib
import configparser

from datetime import datetime
from email.message import EmailMessage

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir) + '/.cfg')

_host = os.getenv("HOST")
_port = os.getenv("PORT")
_sender = os.getenv("SENDER_MAIL")
_password = os.getenv("SENDER_PW")
_encryption = os.getenv("ENCRYPT")
_appname = os.getenv("APP_NAME")


class _SessionMaker():

    def __init__(self, host, port, email, password):
        self.host = _host
        self.port = _port
        self.email = email
        self.password = password
        print("--- %s :: Initializing email server" % (datetime.now()))

    def __call__(self):
        print("--- %s :: Connecting to the server..." % (datetime.now()))
        # Create a secure SSL context
        context = ssl.create_default_context(cafile=certifi.where())
        if _encryption == 'SSL':
            server = smtplib.SMTP_SSL(self.host, self.port, context=context)
            server.ehlo('Hello Lets Talk')

        if _encryption == 'STARTTLS':
            server = smtplib.SMTP(self.host, self.port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection

        return server


SeverLocal = _SessionMaker(host=_host, port=_port, email=_sender, password=_password)


def send_e_mail(email: EmailMessage):
    con = SeverLocal()
    try:
        con.login(_sender, _password)
        print("--- %s :: Login Success..." % (datetime.now()))
        con.send_message(email)
        print("--- %s :: Email Sent Success ..." % (datetime.now()))
        return True

    except Exception as e:
        return False
        raise e

    finally:
        print("--- %s :: Connection Terminated ... " % (datetime.now()))
        con.close()
