import re

info = {
    "name": "reverse",
    "type": 1,
    "description": "Sends the reverse of some text",
    "id": "reverse",
    "options": [
        {
            "name": "text",
            "description": "Text to reverse",
            "type": 3,
            "required": False
        }
    ]
}

async def command(WS, msg):
    return await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": msg["data"]["options"][0]["value"][::-1],
            "flags": 1 << 6,
            "allowed_mentions": []
        }
    }))
