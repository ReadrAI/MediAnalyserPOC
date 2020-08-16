import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
receiver_email = "jean.haizmann@gmail.com"


@DeprecationWarning
class EmailSender:

    SMTP_PORT = 465  # For SSL
    SMTP_SERVER = "smtp.gmail.com"

    email = ""
    password = ""
    context = None
    server = None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT, context=self.context)
        self.server.login(email, password)

    def sendEmail(self, receiver_email, subject, plain_message, html_message=None):
        if self.server is not None:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.email
            message["To"] = receiver_email

            part1 = MIMEText(plain_message, "plain")
            message.attach(part1)
            if html_message is not None:
                part2 = MIMEText(html_message, "html")
                message.attach(part2)

            return self.server.sendmail(self.email, receiver_email, message.as_string())
