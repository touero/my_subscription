import asyncio
from async_get_data import get_data
from async_send_email import send_watchers_emails

async def main():
    await get_data()
    await send_watchers_emails()

if __name__ == '__main__':
    asyncio.run(main())
