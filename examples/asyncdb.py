import aiomysql
import asyncio 


async def select(pool, sql): 
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            r = await cur.fetchone()
            print(r)


async def insert(pool, sql): 
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            await conn.commit()


async def main(loop): 
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
    user='root', password='123456',
    db='test', loop=loop)
    c1 = select(pool, sql='select * from minifw')
    c2 = insert(pool, sql="insert into minifw (name) values ('hello')")
    tasks = [
        asyncio.ensure_future(c1),
        asyncio.ensure_future(c2)
    ]
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    cur_loop = asyncio.get_event_loop()
    cur_loop.run_until_complete(main(cur_loop))