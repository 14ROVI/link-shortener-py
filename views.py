from aiohttp import web
import dbio
import re
import os


regex = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE
)


async def setup_cons(app):
    app["db"] = await dbio.Database.connect()


async def index(request):
    return web.FileResponse("html/index.html")

async def add_redirect(request):
    redirect = request.query.get("redirect")
    password = request.query.get("password")
    if redirect is None or password is None:
        return web.HTTPUnauthorized()
    if password != os.getenv("LINK_SHORTENER_PASSWORD"):
        return web.HTTPBadRequest()
    search = regex.search(redirect)
    if search is None:
        return web.HTTPBadRequest()
    uri = await request.app["db"].add_redirect(search.group(0))
    return web.json_response({"uri": uri})
  
async def get_redirect(request):
    uri = request.match_info["uri"]
    redirect = await request.app["db"].get_redirect(uri)
    if redirect is None:
        return web.HTTPNotFound()
    return web.HTTPFound(redirect)

async def del_redirect(request):
    uri = request.match_info["uri"]
    try:
        await request.app["db"].del_redirect(uri)
        return web.HTTPOk()
    except:
        return web.HTTPError()




def routes(app):
    app.on_startup.append(setup_cons)

    app.router.add_get("/", index)

    app.router.add_post("/add", add_redirect)
    app.router.add_get("/{uri:[a-zA-Z0-9]+}", get_redirect)
    app.router.add_delete("/{uri:[a-zA-Z0-9]+}", del_redirect)