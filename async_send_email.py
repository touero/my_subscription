from smtplib import SMTPException

import aiohttp
import smtplib
import os
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from constants import HOT_FILE

GITHUB_TOKEN = os.getenv("REPO_WATCHERS_TOKEN")
OWNER = "touero"
REPO = "my_subscription"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}",
}

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
AUTHORIZATION_CODE = os.getenv('AUTHORIZATION_CODE')
SENDER_NAME = "my_subscription"
SUBJECT = "GitHub Repo Action Email"


async def fetch_json(url, session):
    try:
        async with session.get(url, headers=HEADERS) as response:
            return await response.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return None


async def get_watchers():
    emails = []
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/subscribers"
    async with aiohttp.ClientSession() as session:
        watchers = await fetch_json(url, session)
        if not watchers or not isinstance(watchers, list):
            print(f"未获取到 watchers: {watchers}")
            return emails
        user_apis = [user_api['url'] for user_api in watchers]
        for user_api in user_apis:
            user = await fetch_json(user_api, session)
            if not user:
                print(f"未获取到 user: {user_api}")
                continue
            emails.append({'name': user['login'], 'email': user['email']})
        return emails


def send_email(receiver):
    message = MIMEMultipart()
    receiver_email = receiver['email']
    receiver_name = receiver['name']
    message['To'] = email.utils.formataddr((receiver_name, receiver_email))
    message['From'] = email.utils.formataddr((SENDER_NAME, SENDER_EMAIL))
    message['Subject'] = SUBJECT

    try:
        with open(HOT_FILE, "r", encoding="utf-8") as file:
            html_content = file.read()
        message.attach(MIMEText(html_content, 'html'))
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, AUTHORIZATION_CODE)
            server.sendmail(SENDER_EMAIL, [receiver_email], 
                            msg=message.as_string())
            print(f"邮件已发送给 {receiver_name}")
    except SMTPException as e:
        print(f"邮件发送出现异常: {e}")


async def send_watchers_emails():
    watchers_emails = await get_watchers()
    if not watchers_emails:
        print("没有可用的 watcher 邮箱")
        return
    print(watchers_emails)

    for watchers_email in watchers_emails:
        if watchers_email.get('email'):
            send_email(watchers_email)
