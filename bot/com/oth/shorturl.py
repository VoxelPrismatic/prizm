#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
from util import embedify, pages, ez
import discord
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import os
import random
import json
import subprocess
import io
import asyncio

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

async def commit(shorts, users):
    git = "/home/priz/prizm.dev/"
    await ez.aio_write(
        f"{git}assets/script/redirect/shorts.js",
        "var shorts = " + json.dumps(shorts, indent = 4)
    )
    await ez.aio_write(
        f"{git}assets/script/redirect/short_users.js",
        "var users = " + json.dumps(users, indent = 4)
    )
    await ez.proc(f"git -C {git} commit --all --amend --no-edit")
    await ez.proc(f"git -C {git}.git push -f")

@commands.command(
    aliases = ["shortlink", "shortlnk"],
    help = 'oth',
    brief = 'Creates a short link!',
    usage = ';]shorturl {url} {?alias}',
    description = '''\
URL   [TEXT] - The URL to shorten
ALIAS [TEXT] - Custom alias, if available
'''
)
@commands.check(enbl)
async def shorturl(ctx, url: str, alias: str = ""):
    created = False
    async with ctx.channel.typing():
        git = "/home/priz/prizm.dev/"
        await ez.proc(f"git -C {git} pull")
        shorts = json.loads(
            (await ez.aio_read("/home/priz/prizm.dev/assets/script/redirect/shorts.js"))[13:]
        )
        users = json.loads(
            (await ez.aio_read("/home/priz/prizm.dev/assets/script/redirect/short_users.js"))[12:]
        )
        if url.lower() == "list":
            st = ""
            for short in shorts:
                if users[short] == ctx.author.id:
                    st += short + "  -  " + shorts[short] + "\n"
            return await ctx.send(
                "```md\n#] Your URLs are in the attached file```",
                file = discord.File(io.BytesIO(st.encode()), str(ctx.author.id) + ".txt")
            )
        if url.lower() == "delete":
            try:
                if users[alias] == ctx.author.id:
                    del users[alias]
                    del shorts[alias]
                commit()
                return await ctx.send("```md\n#] SUCCESS, your URL has been deleted```")
            except:
                return await ctx.send(
                    "```diff\n-] That URL either doesn't exist or doesn't belong to you.```"
                )
        warn = ""
        for key in shorts:
            if shorts[key] == url:
                alias = key
                warn = "-] This URL was already created, so you may not manage it in the future"
                break
        else:
            while not alias or alias in shorts:
                alias = ""
                for x in range(4):
                    alias += random.choice(
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        "abcdefghijklmnopqrstuvwxyz"
                        "0123456789_-"
                    )
            shorts[alias] = url
            users[alias] = ctx.author.id
            await commit(shorts, users)


    await ctx.send(
        embed = embedify.embedify(
            title = "SHORT URL ;]",
            desc = "```md\n#] HERE YOU GO MATE ;]```" + \
                    f"[{alias}](https://voxelprismatic.github.io/prizm.dev/re#{alias})",
            fields = [
                [
                    "Notices",
                    "```diff\n-] These short URLs aren't short yet because I don't have my own domain\n"
                    "-] These short URLs are completely public\n" + warn + "```"
                ]
            ]
        )
    )



##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(shorturl)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('shorturl')
    print('GOOD')
