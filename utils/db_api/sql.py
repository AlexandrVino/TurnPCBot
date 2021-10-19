import asyncio
import logging
from dataclasses import dataclass

import aiogram.types
import asyncpg
from asyncpg import Connection

from data.config import DB_HOST, DB_USER, DB_PASS, DB_NAME

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )


@dataclass
class DBSession:
    user: str
    password: str
    database: str
    port: int
    path: str

    async def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if key not in ['path', 'COMMANDS', 'pool']}

    async def start(self):
        self.COMMANDS: dict = {
            'ADD_NEW_USER': "INSERT INTO public.userinfo(chat_id, language_code, comps) VALUES ($1, $2, $3) RETURNING id",
            'SELECT_USER': "SELECT * FROM public.userinfo WHERE chat_id = $1",
            'UPDATE_USER_COMPS': "UPDATE public.userinfo SET comps = $1 WHERE chat_id = $2"
        }
        self.pool = await asyncpg.create_pool(**await self.to_dict())

    async def get_user(self, *args):
        return await self.pool.fetchrow(self.COMMANDS['SELECT_USER'], *args)

    async def add_user(self, *args) -> None:
        if not 2 <= len(args) <= 3:
            return
        await self.pool.execute(self.COMMANDS['ADD_NEW_USER'], *args)

    async def update_user_comps(self, *args):
        return await self.pool.execute(self.COMMANDS['UPDATE_USER_COMPS'], *args)

    async def get_user_comps(self, **kwargs):
        user = await self.get_user(kwargs['chat_id'])
        if user is None:
            await self.add_user(*kwargs.values())
        return user.get('comps') if user is not None and user.get('comps') is not None else '[]'


async def create_db(database: DBSession):
    logging.info('Connecting with table.')

    with open(database.path + 'db/create_table.sql', 'r') as sql_file:
        sql_command = sql_file.read()
    conn: asyncpg.Connection = await asyncpg.connect(**await database.to_dict())
    try:
        await conn.execute(sql_command)
    except (asyncpg.exceptions.PostgresSyntaxError, asyncpg.exceptions.DuplicateTableError):
        pass
    await conn.close()

    logging.info('Table has been created successfully.')


async def create_pool(**kwargs) -> DBSession:
    db = DBSession(**kwargs)
    await db.start()
    return db


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_pool())
