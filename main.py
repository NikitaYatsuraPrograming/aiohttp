from aiohttp import web

from aiohttpdemo_polls.settings import config
from aiohttpdemo_polls.routes import setup_routes

app = web.Application()
setup_routes(app)
app['config'] = config
web.run_app(app)
