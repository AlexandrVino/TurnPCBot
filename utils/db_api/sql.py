from dataclasses import dataclass

import asyncio
import logging
import asyncpg

# set logging format
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG
                    )


# class, which will keep data for connection with your database
@dataclass
class DBData:
    user: str
    password: str
    database: str
    host: str
    port: int
    path: str


# class, which will interact with your database
class DBSession(DBData):
    def __init__(self, **kwargs):
        super(DBSession, self).__init__(**kwargs)
        self.pool = None
        self.COMMANDS: dict = {}
        self.extra_attributes = ['path', 'COMMANDS', 'pool', 'extra_attributes']

    async def to_dict(self, extra_keys=[]) -> dict:
        return {key: value for key, value in self.__dict__.items() if key not in self.extra_attributes + extra_keys}

    async def start(self):
        try:
            # trying connect to database
            self.pool = await asyncpg.create_pool(**await self.to_dict())
        except asyncpg.exceptions.InvalidCatalogNameError as err:
            # this error will be thrown if the database isn't created
            await create_db(self)  # create database
            logging.error(err)
            self.pool = await asyncpg.create_pool(**await self.to_dict())

        # create table, which will keep info about users
        await self.create_table()

        # taking sql commands from txt file
        with open(self.path + 'db/commands.txt') as sql_file:
            self.COMMANDS = {key: value for key, value in [item.split('==') for item in sql_file.readlines()]}

    async def create_table(self) -> None:
        """
        :param:
        :returns None:
        function, which will be create sql table
        """

        with open(self.path + 'db/create_table.sql', 'r') as sql_file:
            sql_create_table = sql_file.read()
        conn: asyncpg.Connection = await asyncpg.connect(**await self.to_dict())
        await conn.execute(sql_create_table)
        logging.info('Table has been created successfully.')
        await conn.close()

    async def get_user(self, *args) -> asyncpg.Record:
        """
        :param args: list with user data (id)
        :returns asyncpg.Record:
        function, which will be return user by id
        """
        return await self.pool.fetchrow(self.COMMANDS['SELECT_USER'], *args)

    async def add_user(self, *args) -> asyncpg.Record:
        """
        :param args: list with user data (id, language)
        :returns asyncpg.Record:
        function, which will be register user
        """
        if not 2 <= len(args) <= 4:
            return
        await self.pool.execute(self.COMMANDS['ADD_NEW_USER'], *args)

    async def update_user_computers(self, *args) -> asyncpg.Record:
        """
        :param args: list with user data (id, user_ps)
        :returns asyncpg.Record:
        function, which will be updating user pc
        """
        return await self.pool.execute(self.COMMANDS['UPDATE_USER_COMPS'], *args)

    async def update_user_server(self, **kwargs) -> asyncpg.Record:
        """
        :param kwargs: dict with with user data (id, user_ps)
        :returns asyncpg.Record:
        function, which will be updating user pc
        """
        user = await self.get_user(kwargs['chat_id'])
        if user is None:
            return await self.add_user(*kwargs.values())
        return await self.pool.execute(self.COMMANDS['UPDATE_USER_SERVER'], *[kwargs['server'], kwargs['chat_id']])

    async def get_user_computers(self, **kwargs) -> str:
        """
        :param kwargs: dict with user data (id, language and etc)
        :returns asyncpg.Record:
        function, which will return user pc
        """
        user = await self.get_user(kwargs['chat_id'])
        if user is None:
            await self.add_user(*kwargs.values())
        return user.get('computers') if user is not None and user.get('computers') is not None else '[]'

    async def get_user_info(self, **kwargs) -> asyncpg.Record:
        """
        :param kwargs: dict with user data (id, language and etc)
        :returns asyncpg.Record:
        function, which will return user pc
        """
        user = await self.get_user(kwargs['chat_id'])
        if user is None:
            await self.add_user(*kwargs.values())
        return await self.get_user(kwargs['chat_id'])


async def create_db(database: DBSession):
    """
    :param database: exemplar DBSession
    :returns None:
    function, which will be create sql database
    """
    with open(database.path + 'db/create_db.sql', 'r') as sql_file:
        sql_create_db = sql_file.read()
    conn: asyncpg.Connection = await asyncpg.connect(**await database.to_dict(extra_keys=['database']))
    try:
        await conn.execute(sql_create_db)
        logging.info('DataBase has been created successfully.')
    except asyncpg.exceptions.DuplicateTableError as err:
        logging.info(err)
    await conn.close()


async def create_pool(**kwargs) -> DBSession:
    """
    :param kwargs: data for connect to database
    :returns None:
    function, which will return DBSession
    """
    db = DBSession(**kwargs)
    await db.start()
    await asyncio.sleep(10)
    return db
