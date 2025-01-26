import asyncio
from get_weibo_data import get_weibo_data
from send_email import send_email

if __name__ == '__main__':
    asyncio.run(get_weibo_data())
    send_email()