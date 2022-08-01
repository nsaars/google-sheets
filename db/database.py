from time import sleep

from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI

db = Gino()


async def create_db_connection():
    print('db creating...')
    db.gino: GinoSchemaVisitor
    attempt = 1
    while True:
        sleep(3)
        try:
            await db.set_bind(POSTGRES_URI)
        except ConnectionRefusedError as e:
            print(f'Attempt {attempt} was failed', e)
            attempt += 1
        else:
            break
    await db.gino.create_all()
