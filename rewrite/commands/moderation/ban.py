info = {
    "name": "ban",
    "description": "Bans a user",
    "type": 1,
    "id": "ban",
    "options": [
        {
            "name": "user",
            "description": "User to ban",
            "type": 6,
            "required": True
        },
        {
            "name": "reason",
            "description": "Add a reason",
            "type": 3,
            "required": False
        }
    ]
}

async def command(WS, msg):
    await WS.post(WS.interaction(msg), form = WS.form({
        "type": 4,
        "data": {
            "content": f"```json\n{msg['options'][0]['value']}```"
        }
    }))
    #resp = await WS.post(f"{WS.API}/guilds/{msg['guild_id']}/bans/{msg['
