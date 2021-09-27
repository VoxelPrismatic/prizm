import re
import json
import io

info = {
    "name": "clear",
    "type": 1,
    "description": "Clears messages",
    "id": "clear",
    "options": [
        {
            "name": "in",
            "description": "Clears all messages between two message IDs",
            "type": 1,
            "options": [
                {
                    "name": "starting-id",
                    "description": "Clear message history from this message. This one isn't deleted.",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "ending-id",
                    "description": "Clear message history to this message. This one isn't deleted.",
                    "type": 3,
                    "required": True
                }
            ]
        },
        {
            "name": "to",
            "description": "Clears all messages up to a message ID",
            "type": 1,
            "options": [
                {
                    "name": "message-id",
                    "description": "Clear all messages up to this message ID. This message isn't deleted.",
                    "type": 3,
                    "required": True
                }
            ]
        },
        {
            "name": "from",
            "description": "Clears *count* messages from a given message ID",
            "type": 1,
            "options": [
                {
                    "name": "message-id",
                    "description": "Message ID to clear *count* messages from. This message isn't deleted.",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "count",
                    "description": "How many messages to delete",
                    "type": 4,
                    "required": True
                }
            ]
        },
        {
            "name": "count",
            "description": "Clear *count* messages from here",
            "type": 1,
            "options": [
                {
                    "name": "count",
                    "description": "Clear *count* messages from here",
                    "type": 4,
                    "required": True
                }
            ]
        },
        {
            "name": "n",
            "description": "Clear *count* messages from here [alias for 'count']",
            "type": 1,
            "options": [
                {
                    "name": "count",
                    "description": "Clear *count* messages from here",
                    "type": 4,
                    "required": True
                }
            ]
        }
    ]
}

async def command(WS, msg):
    if "message" in list(msg):
        await WS.post(WS.interaction(msg), data = {"type": 6})
        if msg["member"]["user"] != msg["message"]["interaction"]["user"]:
            return
        return await WS.delete(f"{WS.API}/channels/{msg['channel_id']}/messages/{msg['message']['id']}")

    if not (int(msg["member"]["permissions"]) & (1 << 13)): # No MANAGE_MESSAGES
        return await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "ERROR ;[",
                        "description": f"You don't have sufficient permissions to do that.",
                        "color": 0xff0000,
                        "timestamp": WS.NOW
                    }
                ],
                "flags": 1 << 6
            }
        }))
    options = msg["data"]["options"][0]
    channels_URL = f"https://discord.com/channels/{msg['guild_id']}/{msg['channel_id']}/"
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
    if options["name"] == "in":
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
                            "description": f"The provided starting message URL, `{startingID}`, is not from this channel. "
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
                            "description": f"The provided starting message ID, `{startingID}`, is not a valid message ID or URL.",
                            "color": 0xff0000,
                            "timestamp": WS.NOW
                        }
                    ],
                    "flags": 1 << 6
                }
            }))
        endingID = options["options"][1]["value"]
        try:
            endingID = get_ID(endingID)
        except TabError:
            return await WS.post(WS.interaction(msg), data = WS.form({
                "type": 4,
                "data": {
                    "content": "",
                    "embeds": [
                        {
                            "title": "ERROR ;[",
                            "description": f"The provided ending message URL, `{endingID}`, is not from this channel. "
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
                            "description": f"The provided ending message ID, `{endingID}`, is not a valid message ID or URL.",
                            "color": 0xff0000,
                            "timestamp": WS.NOW
                        }
                    ],
                    "flags": 1 << 6
                }
            }))
        a = [startingID, endingID]
        startingID = max(a)
        endingID = min(a)
        await WS.post(WS.interaction(msg), data = WS.form({
            "type": 4,
            "data": {
                "content": "",
                "embeds": [
                    {
                        "title": "CLEARING ;]",
                        "description": f"Clearing messages from [here]({channels_URL}{startingID}) to [here]({channels_URL}{endingID})",
                        "color": 0x00ff00,
                        "timestamp": WS.NOW
                    }
                ]
            }
        }))
        n = []
        while True:
            resp = await WS.get(f"{WS.API}/channels/{msg['channel_id']}/messages?before={startingID}&limit=100")
            ids = [m['id'] for m in resp if int(m['id']) > endingID]
            n += [m for m in resp if int(m['id']) > endingID]
            print(ids)
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
        await WS.patch(WS.interaction(msg, 1), data = WS.form({
            "content": "",
            "embeds": [
                {
                    "title": "CLEARED ;]",
                    "description": f"Cleared {len(n)} message{'s' if len(n) > 1 else ''} from [here]({channels_URL}{startingID}) to [here]({channels_URL}{endingID})",
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
    elif options["name"] == "from":
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
                    ]
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
        count = options["options"][1]["value"]
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
                        "description": f"Clearing {count} message{'s' if count > 1 else ''} from [this one]({channels_URL}{startingID})",
                        "color": 0x00ff00,
                        "timestamp": WS.NOW
                    }
                ]
            }
        }))
        n = []
        while count > 0:
            resp = await WS.get(f"{WS.API}/channels/{msg['channel_id']}/messages?before={startingID}&limit={count}")
            ids = [m['id'] for m in resp]
            n += resp
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
                    "description": f"Cleared {len(n)} message{'s' if len(n) > 1 else ''} from [here]({channels_URL}{startingID})",
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
    elif options["name"] == "to":
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
    else:
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
