import aiohttp
import time
import importlib
info = {
    "name": "reload",
    "type": 1,
    "description": "Reloads a command",
    "id": "reload",
    "options": [
        {
            "name": "command",
            "description": "Command name",
            "type": 3,
            "required": True
        }
    ],
    "default_permission": False
}

async def command(WS, msg):
    options = msg["data"]["options"][0]["value"]
    try:
        current = WS.cache.commands[options].module
        importlib.reload(current)
        WS.cache.commands[options].command = current.command
        resp = WS.post(WS.cache.commands[options].url, headers = {"Authorization": "Bot " + WS.TOKENS.bot}, json = current.info)
        print(resp)
        WS.cache.commands[current.info["name"]] = WS.classify({
            "command": current.command,
            "module": current,
            "data": resp,
            "url": WS.cache.commands[options].url
        })
        WS.cache.commands[options].data
        resp = await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "embeds": [
                    {
                        "title": "RELOADED ;]",
                        "description": f"Command `/{options}` reloaded",
                        "color": 0x00ff00
                    }
                ]
            }
        }))
    except Exception as ex:
        print(f"\x1b[91;1m{ex}\x1b[0m")
        resp = await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "embeds": [
                    {
                        "title": "FAILED ;[",
                        "description": f"Command `/{options}` not found",
                        "color": 0xff0000
                    }
                ]
            }
        }))
    #print(resp)

