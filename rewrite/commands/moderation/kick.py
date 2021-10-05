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
    if "message" in list(msg):
        await WS.post(WS.interaction(msg), data = {"type": 6})
        if msg["member"]["user"] != msg["message"]["interaction"]["user"]:
            return
        return await WS.delete(f"{WS.API}/channels/{msg['channel_id']}/messages/{msg['message']['id']}")

    resp = await WS.delete(f"{WS.API}/guilds/{msg['guild_id']}/{msg['data']['options'][0]['value']}", headers = {
        "X-Audit-Log-Reason": "Requested by " + WS.member(msg) + "; " + \
            (msg['data']['options'][1]['value'] if msg['data']['options'][1]['name'] == 'reason' else "[no reason provided]")
    })
    if resp:
        print(f"\x1b[91;1m{resp}\x1b[0m")
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": "I don't have sufficient permissions to do that",
                        "footer": {"text": "Make sure I have the 'Ban Members' permission"},
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "label": "Delete",
                                "style": 4,
                                "custom_id": "ban"
                            }
                        ]
                    }
                ]
            }
        }))
    return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "BANNED ;]",
                        "description": f"<@{msg['data']['options'][0]['value']}> was banned",
                        "footer": {"text": f"I cannot see the member's name | User ID {msg['data']['options'][0]['value']}"},
                        "color": 0x00ff00,
                        "timestamp": WS.NOW
                    }
                ],
                "components": [
                    {
                        "type": 1,
                        "components": [
                            {
                                "type": 2,
                                "label": "Delete",
                                "style": 4,
                                "custom_id": "ban"
                            }
                        ]
                    }
                ]
            }
        }))
