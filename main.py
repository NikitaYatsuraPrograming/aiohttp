from aiohttp import web

from aiohttpdemo_polls.settings import config
from aiohttpdemo_polls.routes import setup_routes
from aiohttpdemo_polls.db import close_pg, init_pg

app = web.Application()
setup_routes(app)
app['config'] = config
app.on_cleanup.append(init_pg)
app.on_cleanup.append(close_pg)

web.run_app(app, port=9000)

