import importlib
import traceback

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
        },
        {
            "name": "send",
            "description": "Update command JSON?",
            "type": 5,
            "required": False
        }
    ],
    "default_permission": False
}

async def command(WS, msg):
    options = msg["data"]["options"][0]["value"]
    try:
        update = msg["data"]["options"][1]["value"]
        print(update)
    except:
        update = False
    try:
        current = WS.cache.commands[options].module
        try:
            current.extras
        except:
            pass
        else:
            for m in current.extras:
                importlib.reload(m)
        importlib.reload(current)
        WS.cache.commands[options].command = current.command
        if update: #str(current.info) != str(WS.cache.commands[options].info):
            resp = await WS.post(WS.cache.commands[options].url, headers = {"Authorization": "Bot " + WS.TOKENS.bot}, json = current.info)
            print(resp)
            WS.cache.commands[current.info["name"]] = WS.classify({
                "command": current.command,
                "module": current,
                "info": current.info,
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
        tb = "\n".join(traceback.format_tb(ex.__traceback__))
        resp = await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "embeds": [
                    {
                        "title": f"{type(ex)} ;[",
                        "description": f'{ex}\n```{tb}```',
                        "color": 0xff0000
                    }
                ]
            }
        }))
    #print(resp)

