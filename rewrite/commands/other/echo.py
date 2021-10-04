import re

info = {
    "name": "echo",
    "type": 1,
    "description": "Echos a given message",
    "id": "echo",
    "options": [
        {
            "name": "content",
            "description": "Content to echo",
            "type": 3,
            "required": True
        }
    ]
}

async def command(WS, msg):
    return await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": msg["data"]["options"][0]["value"],
        }
    }))
