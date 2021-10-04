import io
import json
import re

async def c(WS, msg, options):
    def get_ID(snow):
        try:
            if len(snow) < 17:
                raise IndentationError
            return int(snow)
        except:
            print(f"^https?://(www\\.)?discord(app)?\\.com/channels/{msg['guild_id']}/{msg['channel_id']}/" + r"\d{17,19}$")
            if re.search(f"^https?://(www\\.)?discord(app)?\\.com/channels/{msg['guild_id']}/{msg['channel_id']}/" + r"\d{17,19}$", snow):
                return int(snow.split("/")[-1])
            elif re.search(r"^https?://(www\.)?discord(app)?\.com/channels/\d{17,19}/\d{17,19}/\d{17,19}$", snow):
                raise TabError
            raise IndentationError
    count = options["options"][0]["value"]
    if count < 1:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": f"The provided count, `{count}`, is too small. Please enter a number greater than 0",
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "flags": 1 << 6
            }
        }))
    await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": "",
            "embeds": [
                {
                    "title": "CLEARING ;]",
                    "description": f"Clearing {count} message{'s' if count > 1 else ''}",
                    "color": 0x00ff00,
                    "timestamp": WS.NOW
                }
            ]
        }
    }))
    n = []
    count += 1
    while count > 0:
        resp = await WS.get(f"{WS.API}/channels/{msg['channel_id']}/messages?limit={count}")
        ids = [m['id'] for m in resp[1:]]
        n += resp[1:]
        if len(ids) == 0:
            break
        elif len(ids) == 1:
            resp = await WS.delete(
                f"{WS.API}/channels/{msg['channel_id']}/messages/{ids[0]}",
                headers = {
                    "X-Audit-Log-Reason": "As per request of " + WS.member(msg)
                }
            )
        else:
            resp = await WS.post(
                f"{WS.API}/channels/{msg['channel_id']}/messages/bulk-delete",
                json = {"messages": ids},
                headers = {
                    "X-Audit-Log-Reason": "As per request of " + WS.member(msg)
                }
            )
        count -= 100
        if resp:
            return await WS.patch(WS.interaction(msg, 1), data = WS.form({
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": "I don't have sufficient permissions to do that",
                        "footer": {"text": "Make sure I have the 'Manage Messages' permission"},
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
                                "custom_id": "clear"
                            }
                        ]
                    }
                ]
            }))
    await WS.patch(WS.interaction(msg, 1), data = WS.form({
        "content": "",
        "embeds": [
            {
                "title": "CLEARED ;]",
                "description": f"Cleared {len(n)} message{'s' if len(n) > 1 else ''}",
                "footer": {"text": "See the attached file for the deleted message contents"},
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
                        "custom_id": "clear"
                    }
                ]
            }
        ]
    }, {
        "value": io.BytesIO(json.dumps(n, indent = 4).encode()),
        "filename": "messages.json"
    }))
