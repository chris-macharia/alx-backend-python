import asyncio
import aiomysql
import aiosqlite

async def async_fetch_users(pool):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM user_data")
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)

async def async_fetch_older_users(pool):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT * FROM user_data WHERE age > 40")
            rows = await cursor.fetchall()
            print("Users older than 40:")
            for row in rows:
                print(row)

async def fetch_concurrently():
    # Replace with your database configuration
    db_config = {
        "host": "localhost",
        "user": "chris",
        "password": "D@tabreach2024",
        "db": "ALX_prodev"
    }

    # Create a connection pool
    pool = await aiomysql.create_pool(**db_config)

    try:
        await asyncio.gather(
            async_fetch_users(pool),
            async_fetch_older_users(pool)
        )
    finally:
        pool.close()
        await pool.wait_closed()

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
