import asyncio
import unittest
from minifw.db import base_db


class TestDB(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def test_select(self):
        sql = 'select * from minifw where id = (%s)'
        rs = self.loop.run_until_complete(base_db.select(self.loop, sql, args=(1,), size=1))
        self.assertEqual(len(rs), 1)

    def test_insert(self):
        sql = 'insert into `minifw` (`name`) values (?)'
        rs = self.loop.run_until_complete(base_db.insert(self.loop, sql, args=('test_val',)))
        self.assertEqual(rs, 1)

    def tearDown(self):
        self.loop.close()
        del self.loop

if __name__ == '__main__':
    unittest.main()