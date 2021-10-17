info = {
    "name": "privacy",
    "type": 1,
    "description": "PRIZM ;]'s Privacy Policy",
    "id": "privacy"
}

async def command(WS, msg):
    resp = await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "embeds": [{
                "title": "PRIVACY ;]",
                "description": "I have a very simple privacy policy, you can view it [here](https://voxelprismatic.github.io/prizm.dev/prizm/privacy).\n"
                               "tl;dr: i only collect data necessary for the bot to function, all data is stored as anonymously as possible",
                "color": 0x00ff00
            }]
        }
    }))
