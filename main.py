import asyncio
from async_get_data import get_data
from send_email import send_email

if __name__ == '__main__':
    asyncio.run(get_data())
    send_email()
