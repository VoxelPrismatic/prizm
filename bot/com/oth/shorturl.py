#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
from util import embedify, pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import os
import random
import json
import subprocess
import asyncio

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

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
        shorts = json.loads(open("/home/priz/prizm.dev/assets/script/redirect/shorts.js").read()[13:])
        for key in shorts:
            if shorts[key] == url:
                alias = key
                break
        else:
            while not alias or alias in shorts:
                alias = ""
                for x in range(16):
                    alias += random.choice(
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        "abcdefghijklmnopqrstuvwxyz"
                        "0123456789_+-=."
                    )
            shorts[alias] = url
            git = "/home/priz/prizm.dev/"
            proc = subprocess.Popen(
                f"git -C {git} pull".split()
            )
            while proc.poll() is None:
                await asyncio.sleep(1)
            open(f"{git}assets/script/redirect/shorts.js", "w").write(
                "var shorts = " + json.dumps(shorts, indent = 4)
            )
            os.system(f"git -C {git} commit --all --amend --no-edit")
            proc = subprocess.Popen(
                f"git -C {git}.git push -f".split()
            )
            while proc.poll() is None:
                await asyncio.sleep(1)

    await ctx.send(
        embed = embedify.embedify(
            title = "SHORT URL ;]",
            desc = "```md\n#] HERE YOU GO MATE ;]```" + \
                    f"[{alias}](https://voxelprismatic.github.io/prizm.dev/re?link={alias})",
            fields = [
                [
                    "Notices",
                    "```diff\n-] These short URLs aren't short yet because I don't have my own domain\n"
                    "-] These short URLs are completely public```"
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

