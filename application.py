import os
import sys
os.chdir(sys.path[0])


from dotenv import load_dotenv
load_dotenv(sys.path[0]+"/.env")


from aiohttp import web
from views import routes
app = web.Application()
routes(app)
web.run_app(app, port=9812)