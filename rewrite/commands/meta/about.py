import time
info = {
    "name": "about",
    "type": 1,
    "description": "About PRIZM ;]",
    "id": "about"
}

async def command(WS, msg):
    resp = await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "embeds": [{
                "title": "ABOUT ;]",
                "description": "I have lots of cool features, you can learn about me [here](https://voxelprismatic.github.io/prizm.dev/prizm)\n"
                               "My code is all hosted on [GitHub](https://github.com/voxelprismatic/prizm)",
                "color": 0x00ff00
            }]
        }
    }))
