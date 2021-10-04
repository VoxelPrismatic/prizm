import re
import json
import io
from . import _clear_n
from . import _clear_to
from . import _clear_from
from . import _clear_in

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

extras = [
    _clear_n,
    _clear_to,
    _clear_from,
    _clear_in
]

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
    match options["name"]:
        case "in":
            await _clear_in.c(WS, msg, options)
        case "from":
            await _clear_from.c(WS, msg, options)
        case "to":
            await _clear_to.c(WS, msg, options)
        case "n" | "count":
            await _clear_n.c(WS, msg, options)
