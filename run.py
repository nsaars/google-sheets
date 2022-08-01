import asyncio

from controller import main, notify_outdated
from db.database import create_db_connection


async def run():
    await create_db_connection()
    await asyncio.gather(main(), notify_outdated())


if __name__ == '__main__':
    asyncio.run(run())
