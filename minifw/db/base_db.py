import aiomysql


conf = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'test'
}


async def get_pool(loop):
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='123456', db='test', loop=loop)
    return pool


async def select(pool, sql, args=(), size=None):
    # todo: find the reason that why using async with pool.acquire() as conn can't close the conn
    conn = await pool.acquire()
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(sql.replace('?', '%s'), args)
        if size:
            r = await cur.fetchmany(size)
        else:
            r = await cur.fetchall()
    conn.close()
    return r


async def execute(pool, sql, args=()):
    conn = await pool.acquire()
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute(sql.replace('?', '%s'), args)
        await conn.commit()
        affected_rows = cur.rowcount
    conn.close()
    return affected_rows





