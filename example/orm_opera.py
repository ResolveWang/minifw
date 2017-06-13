import asyncio
from minifw.db.base_db import get_pool
from minifw.db.orm import (Model,
                           StringField,
                           IntegerField
                           )


class User(Model):
    __table__ = 'user'
    id = IntegerField(primary_key=True)
    name = StringField()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    pool = loop.run_until_complete(get_pool(loop))
    rs = loop.run_until_complete(User.find(pool, 1))
    #user = User(id=3)
    # loop.run_until_complete(user.save(pool))
    # user.name = 'update_test'
    # loop.run_until_complete(user.update(pool))
    # loop.run_until_complete(user.remove(pool))
    #rs = loop.run_until_complete(User.find_all(pool, where='name=update_test'))
    print(rs)

