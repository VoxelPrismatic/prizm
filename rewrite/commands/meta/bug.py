import time
info = {
    "name": "bug",
    "type": 1,
    "description": "Submits a bug report",
    "id": "bug",
    "options": [
        {
            "name": "summary",
            "description": "Summary of the bug",
            "type": 3,
            "required": True
        },
        {
            "name": "command",
            "description": "Command you used",
            "type": 3,
            "required": True
        },
        {
            "name": "traceback",
            "description": "Link to traceback file",
            "type": 3,
            "required": False
        }
    ]
}

async def command(WS, msg):
    options = msg['data']['options']
    await WS.post(f"{WS.API}/channels/597577735065436171/messages", data = WS.form({
        "embeds": [{
            "title": "REPORT ;[",
            "description": f"{options[1]['value']}\n```{options[0]['value']}```\n{options[2]['value'] if len(options) == 3 else ''}",
            "color": 0xff0088
        }]
    }))
    await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": "Your report has been sent, this is what it looks like:",
            "embeds": [{
                "title": "REPORT ;[",
                "description": f"{options[1]['value']}\n```{options[0]['value']}```\n{options[2]['value'] if len(options) == 3 else ''}",
                "color": 0xff0088
            }],
            "flags": 1 << 6
        }
    }))
