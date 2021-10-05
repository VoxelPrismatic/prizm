from . import _info_emoji
from . import _info_role
from . import _info_channel
from . import _info_user
from . import _info_guild

info = {
    "name": "info",
    "description": "Gives information about a given object",
    "type": 1,
    "id": "echo",
    "options": [
        {
            "name": "emoji",
            "description": "Gives information about an emoji",
            "type": 1,
            "options": [
                {
                    "name": "emoji",
                    "type": 3,
                    "description": "The emoji to get info about",
                    "required": True
                }
            ]
        },
        {
            "name": "role",
            "description": "Gives information about a role",
            "type": 1,
            "options": [
                {
                    "name": "role",
                    "type": 8,
                    "description": "The role to get info about",
                    "required": True
                }
            ]
        },
        {
            "name": "channel",
            "description": "Gives information about a channel",
            "type": 1,
            "options": [
                {
                    "name": "channel",
                    "type": 7,
                    "description": "The channel to get info about",
                    "required": True
                }
            ]
        },
        {
            "name": "user",
            "description": "Gives information about a user",
            "type": 1,
            "options": [
                {
                    "name": "user",
                    "type": 6,
                    "description": "The user to get info about",
                    "required": True
                }
            ]
        },
        {
            "name": "guild",
            "description": "Gives information about this guild",
            "type": 1,
            "options": []
        }
    ]
}

extras = [
    _info_channel,
    _info_emoji,
    _info_guild,
    _info_role,
    _info_user
]

async def command(WS, msg):
    options = msg["data"]["options"][0]
    match options["name"]:
        case "channel":
            await _info_channel.c(WS, msg, options)
        case "emoji":
            await _info_emoji.c(WS, msg, options)
        case "guild":
            await _info_guild.c(WS, msg, options)
        case "role":
            await _info_role.c(WS, msg, options)
        case "user":
            await _info_user.c(WS, msg, options)
