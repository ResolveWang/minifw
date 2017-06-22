import logging
import asyncio
from aiohttp import web
from minifw.core.framewk import add_static, add_routes
from minifw.middleware import logger_factory, response_factory, init_jinja2, datetime_filter


logging.basicConfig(level=logging.INFO)

async def init(eloop):
    app = web.Application(
        loop=eloop,
        middlewares=[logger_factory, response_factory],
    )
    add_routes(app=app, module_name='minifw.handlers')
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_static(app=app)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 5000)
    logging.info('server started at http://127.0.0.1:5000')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()