info = {
    "name": "ping",
    "type": 1,
    "description": "Sends 'pong!'",
    "id": "ping"
}

async def command(WS, msg):
    snow = (int(msg['id']) >> 22) + 1420070400000
    form = {
        "type": 4 if "message" not in list(msg) else 7,
        "data": {
            "content": "",
            "flags": 1 << 6,
            "embeds": [
                {
                    "title": "PONG ;]",
                    "description": f"**Latency:** {WS.LATENCY * 1000:.2f}ms\n**Response:** {time.time() * 1000 - snow:.2f}ms",
                    #"footer": {
                        #"text": "PRIZM ;]",
                        #"icon_url": "https://cdn.discordapp.com/avatars/555862187403378699/dc656061a4d9c9b114979d1088177f44.png?size=128"
                    #},
                    "timestamp": WS.NOW,
                    "color": 0x00ff00
                }
            ],
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 2,
                            "label": "Update",
                            "style": 2,
                            "custom_id": "ping"
                        }
                    ]
                }
            ]
        }
    }
    resp = await WS.post(WS.interaction(msg), data = WS.form(form))
    print(resp)
