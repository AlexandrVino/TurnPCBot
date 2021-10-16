import asyncio
import logging

from data.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )


'''async def create_db():
    logging.info('Connecting with table.')
    with open('db/create_table.sql', 'r') as sql_file:
        sql_command = sql_file.read()
    conn: asyncpg.Connection = await asyncpg.connect(
        user=DB_USER, password=DB_PASS, database=DB_NAME
    )
    await conn.execute(sql_command)
    await conn.close()
    logging.info('Table has been created successfully.')


async def create_pool():
    return await asyncpg.create_pool(
        user=DB_USER, password=DB_PASS, database=DB_NAME
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
'''