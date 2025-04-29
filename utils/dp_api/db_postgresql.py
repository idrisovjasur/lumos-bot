import asyncio
from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from django.templatetags.i18n import language

from data import config

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        # Create a pool of connections
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            phone VARCHAR(255) NOT NULL,
            class_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NULL,
            telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, name, surname, phone, class_name, username, telegram_id, language):
        sql = "INSERT INTO app_telegramusers (name, surname, phone, class_name, username, telegram_id, language) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, name, surname, phone, class_name,  username, telegram_id, language, fetchrow=True)

    async def add_appeal(self, name, surname, phone, class_name, text, question_type):
        sql = "INSERT INTO app_usersappeal (name, surname, phone, class_name, text, question_type) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, name, surname, phone, class_name, text, question_type, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM app_telegramusers WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_language(self, language: str, telegram_id: int):
        query = "UPDATE app_telegramusers SET language=$1 WHERE telegram_id=$2"
        await self.pool.execute(query, language, telegram_id)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)




