import aiomysql


conf = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'test'
}


# todo: use connection pool
async def select(loop, sql, args=(), size=None):
    async with aiomysql.connect(**conf, loop=loop) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                if size:
                    r = await cur.fetchmany(size)
                else:
                    r = await cur.fetchall()
                return r


async def insert(loop, sql, args=()):
    async with aiomysql.connect(**conf, loop=loop) as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql.replace('?', '%s'), args)
            await conn.commit()
            return cur.rowcount





