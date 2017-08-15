import asyncio
import unittest
import aiomysql
from minifw.db import base_db
from examples.orm_opera import User


class TestDB(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()
        self.pool = self.loop.run_until_complete(aiomysql.create_pool(host='127.0.0.1', port=3306,
                                                                      user='root', password='123456',
                                                                      db='test', loop=self.loop))

    def test_select(self):
        sql = 'select * from minifw where id = (%s)'
        rs = self.loop.run_until_complete(base_db.select(self.pool, sql, args=(1,), size=1))
        self.assertEqual(len(rs), 1)

    def test_execute(self):
        sql = 'insert into `minifw` (`name`) values (?)'
        rs = self.loop.run_until_complete(base_db.execute(self.pool, sql, args=('test_val',)))
        self.assertEqual(rs, 1)

    def test_save(self):
        user = User(id=100, name='hello')
        rs = self.loop.run_until_complete(user.save(self.pool))
        self.assertEqual(rs, 1)

    def test_find(self):
        user = self.loop.run_until_complete(User.find(self.pool, 100))
        self.assertEqual(user.name, 'hello')

    def test_update(self):
        user = self.loop.run_until_complete(User.find(self.pool, 100))
        user.name = 'test'
        rs = self.loop.run_until_complete(user.update(self.pool))
        self.assertEqual(rs, 1)

    def tearDown(self):
        self.pool.close()
        del self.pool


if __name__ == '__main__':
    unittest.main()
