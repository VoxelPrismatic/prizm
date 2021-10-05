import random
import re

info = {
    "name": "mock",
    "type": 1,
    "description": "Mocks the given message",
    "id": "mock",
    "options": [
        {
            "name": "message-id",
            "description": "Message ID or URL, leave empty to grab the latest message",
            "type": 3,
            "required": False
        }
    ]
}

async def command(WS, msg):
    try:
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
                            "description": f"The provided message ID, `{options}`, is not a valid message ID or URL",
                            "color": 0xff0000,
                            "timestamp": WS.NOW
                        }
                    ],
                    "flags": 1 << 6
                }
            }))
        resp = await WS.get(f"{WS.API}/channels/{c_snow}/messages/{m_snow}")
    except KeyError:
        resp = (await WS.get(f"{WS.API}/channels/{msg['channel_id']}/messages?limit=1"))[0]
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
    return await WS.post(WS.interaction(msg), data = WS.form({
        "type": 4,
        "data": {
            "content": ''.join([x.upper() if random.randint(0, 1) else x.lower() for x in st]),
            #"flags": 1 << 6,
            "allowed_mentions": []
        }
    }))
