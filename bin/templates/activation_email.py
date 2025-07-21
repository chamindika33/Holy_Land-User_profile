import os
import configparser

from jinja2 import Template
from email.headerregistry import Address
from email.message import EmailMessage

config = configparser.RawConfigParser()
config.read(os.path.abspath(os.curdir) + '/.cfg')


class PasswordEmail():
    def __init__(self, subject: str, salutation: str, paragraph: str, recipient: str, code: str):
        print(recipient)
        self.salutation = salutation
        self.paragraph = paragraph
        self.recipient = recipient.split("@")
        self.code = code
        self.app = 'Holy Land'
        self.sender = os.getenv("SENDER_MAIL").split("@")
        self.subject = subject

    def __call__(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = Address(self.app, self.sender[0], self.sender[1])
        msg['To'] = Address(self.recipient[0], self.recipient[0], self.recipient[1])
        # msg.set_content(MIMEText(next(mail_body(self.fullname , self.code)),"html"))
        msg.set_content(next(mail_body(salutation=self.salutation, paragraph=self.paragraph, code=self.code)), "html")
        yield msg


def mail_body(salutation, paragraph, code):
    fp = open(os.path.abspath(os.curdir) + "/bin/templates/activation.html")
    html = fp.read()
    template = Template(html)

    yield template.render(salutation=salutation, paragraph=paragraph, otp=code)

