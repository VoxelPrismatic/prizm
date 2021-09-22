import aiohttp
import re
import importlib

info = {
    "name": "markdown",
    "type": 1,
    "description": "Sends the raw markdown of a given message",
    "id": "markdown",
    "options": [
        {
            "name": "message-id",
            "description": "Message ID or URL",
            "type": 3,
            "required": True
        }
    ]
}

async def command(WS, msg):
    options = msg["data"]["options"][0]["value"]
    def get_ID(snow):
        try:
            if len(snow) < 17:
                raise IndentationError
            return msg['channel_id'], int(snow)
        except:
            print(f"^https?://(www\\.)?discord(app)?\\.com/channels/{msg['guild_id']}/{msg['channel_id']}/" + r"\d{17,19}$")
            if re.search(r"^https?://(www\.)?discord(app)?\.com/channels/\d{17,19}/\d{17,19}/\d{17,19}$", snow):
                return snow.split("/")[-2:]
            raise IndentationError

    try:
        c_snow, m_snow = get_ID(options)
    except IndentationError:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": f"The provided message ID, `{now}`, is not a valid message ID or URL",
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "flags": 1 << 6
            }
        }))
    resp = await WS.get(f"{WS.API}/channels/{c_snow}/messages/{m_snow}")
    print(resp)
    try:
        st = resp["content"]
    except:
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": f"I either don't have access to that message or that message doesn't exist.\n"
                                       f"Make sure I have read access in <#{c_snow}> and that message wasn't deleted.",
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "flags": 1 << 6
            }
        }))
    for s in "\\*<_|`~":
        st = st.replace(s, "\\" + s)
    return await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": st,
            "flags": 1 << 6
        }
    }))
