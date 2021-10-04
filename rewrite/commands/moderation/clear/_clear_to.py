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
    startingID = options["options"][0]["value"]
    try:
        startingID = get_ID(startingID)
    except TabError:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": f"The provided message URL, `{startingID}`, is not from this channel. "
                                        "Please only use the /clear command in the channel you intend to use it in.",
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "flags": 1 << 6
            }
        }))
    except IndentationError:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": f"The provided message ID, `{startingID}`, is not a valid message ID or URL.",
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "flags": 1 << 6
            }
        }))
    resp = await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "CLEARING ;]",
                        "description": f"Clearing all messages up to [this one]({channels_URL}{startingID})",
                        "color": 0x00ff00,
                        "timestamp": WS.NOW
                    }
                ]
            }
        }))
    print(resp)
    n = []
    while True:
        resp = await WS.get(f"{WS.API}/channels/{msg['channel_id']}/messages?after={startingID}&limit=100")
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
    resp = await WS.patch(WS.interaction(msg, 1), data = WS.form({
        "content": "",
        "embeds": [
            {
                "title": "CLEARED ;]",
                "description": f"Cleared {len(n)} message{'s' if len(n) > 1 else ''} up to [here]({channels_URL}{startingID})",
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
    print(resp)
