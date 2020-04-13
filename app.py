from mcstatus import MinecraftServer
from aiohttp import web
import json

routes = web.RouteTableDef()

colours = {
    "black": "§0",
    "dark_blue": "§1",
    "dark_green": "§2",
    "dark_aqua": "§3",
    "dark_red": "§4",
    "dark_purple": "§5",
    "gold": "§6",
    "gray": "§7",
    "dark_gray": "§8",
    "blue": "§9",
    "green": "§a",
    "aqua": "§b",
    "red": "§c",
    "light_purple": "§d",
    "yellow": "§e",
    "white": "§f",
}

formats = {

}

@routes.get("/")
async def index(request):
    return web.Response(text='<iframe width="100%" height="100%" src="https://www.youtube.com/embed/YPN0qhSyWy8" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', content_type='text/html')

@routes.get("/server/{address}")
async def ping(request):
    data = {'online': False}
    try:
        server = MinecraftServer.lookup(request.match_info['address'])
        status = server.status()

        data['ping'] = status.latency
        data['online'] = True
        data['players'] = {'online': status.players.online, 'max': status.players.max}
        data['protocol'] = status.version.protocol
        data['favicon'] = status.favicon

        # weird motd things.
        motd = status.description
        if "extra" in motd:
            motd = ""
            for key in status.description['extra']:
                if key['color'] is not None:
                    motd = motd + colours[key['color']]
                motd = motd + key['text']
        elif "text" in motd:
            motd = motd['text']

        data['description'] = {'raw': status.description, 'normal': motd}
    except:
        pass
    return web.json_response(data)

app = web.Application()
app.add_routes(routes)
web.run_app(app)