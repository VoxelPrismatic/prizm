#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
import requests
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import json
import io

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

base_api = "https://discord.com/api/v8/"

obj_types = {
    "msg": (lambda cID, tID: base_api + f"channels/{cID}/messages/{tID}"),
}

@commands.command(
    aliases = [],
    help = 'dis',
    brief = 'Sends the raw JSON response of an object',
    usage = ';]api {?url} {?obj_type} {?...param}',
    description = '''\
     URL [STR] - URL to the API object. If this is used, you should not have OBJ_TYPE or PARAM
OBJ_TYPE [STR] - The object type.
...PARAM [???] - Params for the template URL if OBJ_TYPE is given.
'''
)
@commands.check(enbl)
async def api(ctx, url, *param):
    uri = ""
    if url.startswith("/"):
        uri = base_api + url[1:]
    elif url.startswith("http"):
        uri = url
    elif url in obj_types:
        if url == "msg" and len(param) == 1:
            param = [ctx.channel.id, param[0]]
        uri = obj_types[url](*param)
    else:
        return await ctx.send(f"```diff\n-] UNKNOWN TYPE `{url}'```")
    resp = requests.get(
        uri,
        headers = {
            "Authorization": f"Bot {ctx.bot.http.token}",
            "User-Agent": "DiscordBot (https://github.com/VoxelPrismatic/prizmatic, 1.0)"
        }
    )
    st = json.dumps(resp.json(), indent = 2)
    if len(st.replace("`", "`\u200b")) <= 1989:
        ct = "```json\n" + st.replace("`", "`\u200b") + "```"
    else:
        ct = "```md\n#] RESPONSE TOO LONG, CHECK ATTACHED FILE.```"
    await ctx.send(ct, file = discord.File(io.BytesIO(st.encode()), "response.json"))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(api)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('api')
    print('GOOD')
