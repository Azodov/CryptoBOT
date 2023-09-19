from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
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
                      execute: bool = False
                      ):
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

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        telegram_id BIGINT NULL UNIQUE,
        otp BIGINT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(255) NOT NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        language VARCHAR(255) NOT NULL DEFAULT 'uz',
        phone_number VARCHAR(255) NOT NULL,
        wallet_address VARCHAR(255) NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    async def create_table_currencies(self):
        sql = """
        CREATE TABLE IF NOT EXISTS currencies (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        btc_rate VARCHAR NOT NULL,
        eth_rate VARCHAR NOT NULL,
        usdt_rate VARCHAR NOT NULL,
        humo_rate VARCHAR NOT NULL,
        uzcard_rate VARCHAR NOT NULL,
        visa_rate VARCHAR NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        """
        return await self.execute(sql, execute=True)

    async def create_table_orders(self):
        sql = """
        CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        currency_id BIGINT NOT NULL,
        amount VARCHAR NOT NULL,
        wallet_address VARCHAR NOT NULL,
        cheques VARCHAR NOT NULL,
        payment_method VARCHAR NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        status VARCHAR NOT NULL DEFAULT 'PENDING',
        FOREIGN KEY (user_id) REFERENCES users (telegram_id),
        FOREIGN KEY (currency_id) REFERENCES currencies (id)
        );
        """
        return await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    """
    ---------------------------------------------CONTROL ADMINS--------------------------------------------------------
    """

    async def add_admin(self, telegram_id: int, name: str, otp: int):
        sql = """
                INSERT INTO admins(telegram_id, name, otp) VALUES($1, $2, $3)
                """
        await self.execute(sql, telegram_id, name, otp, execute=True)

    async def select_admin(self, **kwargs):
        sql = """
            SELECT * FROM admins WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_admin(self, **kwargs):
        sql = """
            DELETE FROM admins WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def update_admin(self, telegram_id: int, action: str, otp: int):
        sql = """
            UPDATE admins SET telegram_id=$1, otp=$2 WHERE otp=$3
            """
        return await self.execute(sql, telegram_id, action, otp, execute=True)

    async def select_all_admins(self):
        sql = """
            SELECT * FROM admins
            """
        return await self.execute(sql, fetch=True)

    """
    ---------------------------------------------USER CONTROLLER--------------------------------------------------------
    """

    async def add_user(self, fullname: str, telegram_id: int, language: str, phone_number: str,
                       wallet_address: str = None):
        sql = """
                INSERT INTO users(fullname, telegram_id, language, phone_number, wallet_address) VALUES($1, $2, $3, $4, $5)
                """
        await self.execute(sql, fullname, telegram_id, language, phone_number, wallet_address, execute=True)

    async def select_user(self, **kwargs):
        sql = """
            SELECT * FROM users WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def delete_user(self, **kwargs):
        sql = """
            DELETE FROM users WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def update_user_wallet_address(self, telegram_id: int, wallet_address: str):
        sql = """
            UPDATE users SET wallet_address=$1 WHERE telegram_id=$2
            """
        return await self.execute(sql, wallet_address, telegram_id, execute=True)

    async def select_all_users(self):
        sql = """
            SELECT * FROM users
            """
        return await self.execute(sql, fetch=True)


    async def update_user_language(self, telegram_id: int, language: str):
        sql = """
            UPDATE users SET language=$1 WHERE telegram_id=$2
            """
        return await self.execute(sql, language, telegram_id, execute=True)

    async def update_user_phone_number(self, telegram_id: int, phone_number: str):
        sql = """
            UPDATE users SET phone_number=$1 WHERE telegram_id=$2
            """
        return await self.execute(sql, phone_number, telegram_id, execute=True)

    async def update_user_fullname(self, telegram_id: int, fullname: str):
        sql = """
            UPDATE users SET fullname=$1 WHERE telegram_id=$2
            """
        return await self.execute(sql, fullname, telegram_id, execute=True)

    """
    ---------------------------------------------CURRENCIES CONTROLLER--------------------------------------------------
    """

    async def add_currency(self, name: str, btc_rate: str, eth_rate: str, usdt_rate: str, humo_rate: str,
                           uzcard_rate: str, visa_rate: str):
        sql = """
                INSERT INTO currencies(name, btc_rate, eth_rate, usdt_rate, humo_rate, uzcard_rate, visa_rate)
                VALUES($1, $2, $3, $4, $5, $6, $7)
                """
        await self.execute(sql, name, btc_rate, eth_rate, usdt_rate, humo_rate, uzcard_rate, visa_rate, execute=True)

    async def select_currency(self, **kwargs):
        sql = """
            SELECT * FROM currencies WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_currencies(self):
        sql = """
            SELECT * FROM currencies
            """
        return await self.execute(sql, fetch=True)

    async def update_currency(self, id: int, btc_rate: str, eth_rate: str, usdt_rate: str, humo_rate: str,
                              uzcard_rate: str, visa_rate: str):
        sql = """
            UPDATE currencies SET btc_rate=$1, eth_rate=$2, usdt_rate=$3, humo_rate=$4, uzcard_rate=$5, visa_rate=$6
            WHERE id=$7
            """
        return await self.execute(sql, btc_rate, eth_rate, usdt_rate, humo_rate, uzcard_rate, visa_rate, id,
                                  execute=True)

    async def update_currency_name(self, id: int, name: str):
        sql = """
            UPDATE currencies SET name=$1 WHERE id=$2
            """
        return await self.execute(sql, name, id, execute=True)

    async def delete_currency(self, **kwargs):
        sql = """
            DELETE FROM currencies WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    """
    ---------------------------------------------ORDERS CONTROLLER--------------------------------------------------
    """

    async def add_order(self, user_id: int, currency_id: int, amount: str, wallet_address: str, cheques: str,
                        payment_method: str, status: str = "PENDING"):
        sql = """
                INSERT INTO orders(user_id, currency_id, amount, wallet_address, cheques, payment_method, status)
                VALUES($1, $2, $3, $4, $5, $6, $7) RETURNING *
                """
        return await self.execute(sql, user_id, currency_id, amount, wallet_address, cheques, payment_method, status,
                           fetchrow=True)

    async def select_order(self, **kwargs):
        sql = """
            SELECT * FROM orders WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_orders(self):
        sql = """
            SELECT * FROM orders
            """
        return await self.execute(sql, fetch=True)

    async def delete_order(self, **kwargs):
        sql = """
            DELETE FROM orders WHERE 
            """
        sql, parameters = self.format_args(sql, kwargs)
        await self.execute(sql, *parameters, execute=True)

    async def update_order_status(self, id: int, status: str):
        sql = """
            UPDATE orders SET status=$1 WHERE id=$2
            """
        return await self.execute(sql, status, id, execute=True)

    async def select_user_wallets(self, user_id):
        sql = """
            SELECT DISTINCT ON (wallet_address) wallet_address 
            FROM orders WHERE user_id=$1
            """
        return await self.execute(sql, user_id, fetch=True)
