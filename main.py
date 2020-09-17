import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiohttpdemo_polls.settings import config, BASE_DIR
from aiohttpdemo_polls.routes import setup_routes
from aiohttpdemo_polls.db import close_pg, init_pg
from middlewares import setup_middlewares

app = web.Application()
app['config'] = config
aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(str(BASE_DIR / 'aiohttpdemo_polls' / 'templates')))

setup_routes(app)
app.on_startup.append(init_pg)
app.on_cleanup.append(close_pg)
setup_middlewares(app)

web.run_app(app, port=9090)

