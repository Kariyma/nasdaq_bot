from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            database=config.PGDATABASE,
            host=config.IP
        )
        self.pool = pool

    async def create1(self):
        async with asyncpg.create_pool(user='postgres',
                                       password=config.PGPASSWORD,
                                       database=config.PGDATABASE,
                                       host=config.IP,
                                       command_timeout=60) as pool:
            self.pool = pool

    async def close(self):
        await self.pool.close()

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT NOT NULL,
            Name varchar(255) NOT NULL,
            email varchar(255),
            PRIMARY KEY (user_id)
            );
             """
        await self.pool.execute(sql)

    async def delete_table_users(self):
        await self.pool.execute("DROP TABLE IF EXISTS Users;")

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num + 1}" for num, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, user_id: int, name: str, email: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
        sql = """
        INSERT INTO Users(user_id, Name, email) VALUES($1, $2, $3)
        """
        await self.pool.execute(sql, user_id, name, email)

    async def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return await self.pool.fetch(sql)

    async def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = f"""
        SELECT * FROM Users WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def count_users(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Users")

    async def update_user_email(self, email, user_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE Users SET email=$1 WHERE user_id=$2
        """
        return await self.pool.execute(sql, email, user_id)

    async def delete_users(self):
        await self.pool.execute("DELETE FROM Users WHERE TRUE")

    async def select_all_fruits(self):

        sql = "SELECT * FROM fruits"

        return await self.pool.fetch(sql)

    async def update_fruit_rate(self, fruit_id, rate_changer):

        sql = "UPDATE fruits SET rate=rate+$1 WHERE fruit_id=$2"

        return await self.pool.execute(sql, rate_changer, fruit_id)

    async def select_fruits(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = f"""
        SELECT * FROM fruits WHERE 
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.pool.fetch(sql, *parameters)
