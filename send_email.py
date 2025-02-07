import smtplib
import email.utils
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from constants import HOT_FILE


def send_email():
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 465))
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    receiver_name = os.getenv('RECEIVER_NAME', 'Receiver Name')
    authorization_code = os.getenv('AUTHORIZATION_CODE')
    sender_name = "GithubActionNewsBot"
    subject = "Hot News"
    filename = HOT_FILE
    message = MIMEMultipart()
    message['To'] = email.utils.formataddr((receiver_name, receiver_email))
    message['From'] = email.utils.formataddr((sender_name, sender_email))
    message['Subject'] = subject
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()
    message.attach(MIMEText(html_content, 'html'))
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    try:
        server.login(sender_email, authorization_code)
        server.set_debuglevel(True)
        server.sendmail(sender_email, [receiver_email], msg=message.as_string())
        print("已成功发送")

    finally:
        server.quit()

