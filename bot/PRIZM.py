#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('##/// IMPORT ///##')

##/// DEPENDENCIES
import typing
import discord
import logging
import datetime
import time
print('##///  [05]  ///##')
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from importlib import reload
import asyncio
print('##///  [10]  ///###')
import random
from util.getPre import getPre
from util import dbman
import re
import os
import subprocess
print('##///  [15]  ///###')
from lis import twitter
import traceback
import io

print('##///  DONE  ///##')
print('##/// DEFINE ///##')

bot = commands.Bot(command_prefix = getPre, case_insenitive = True)
bot.remove_command("help")
logging.basicConfig(level='INFO')

print('##///  DONE  ///##')

##///---------------------///##
##///  IMPORT EXTRA CODE  ///##
##///---------------------///##

print('##/// EXTRAS ///##')

try:
    from util import pages
    pages.init()
    from util import embedify
    from util import vox
    from chk import enbl
    from util import jsonSave
    from util import logic
    from util import ez
    from chk import has
except Exception as ex:
    print("MODULE ERROR -", ex)
from dyn import refresh, faces

def lext(name):
    print(f'> lEXT {name}')
    bot.load_extension(name)
def rext(name):
    print(f'>  rEXT {name}')
    bot.reload_extension(name)
def uext(name):
    print(f'> uEXT {name}')
    bot.unload_extension(name)
def loadmain():
    try:
        bot.load_extension(f"com.own.cld")
    except:
        bot.reload_extension(f"com.own.cld")

allext, lodtxt = refresh.refresh()

loadmain()

print('##///  DONE  ///##')

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

print('##/// DEFINE ///##')

def jsons(bot):
    jsonSave.saver(bot)

async def log(head, text):
    print(f'##///{head}\n{text}')
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify.embedify(desc=f'```md\n#] {head}!\n> {text}```'))
    return msgs

print('##///  DONE  ///##')

##///---------------------///##
##///      BOT LOOPS      ///##
##///---------------------///##

print('##// STARTING //##')

ever_connected = False

async def run_twitter():
    while True:
        try:
            await twitter.on_tweet(bot)
        except Exception as ex:
            await bot.get_channel(569698278271090728).send(
                "<@481591703959240706>",
                file = discord.File(
                    io.BytesIO(
                        (str(ex) + "\n" +  "\n".join(traceback.format_tb(ex.__traceback__))).encode()
                    ),
                    "tb.txt"
                )
            )
        await asyncio.sleep(15)

@bot.listen()
async def on_connect():
    await bot.change_presence(
        activity = discord.Activity(
            type = 2,
            name = "RAM Burning Noises",
            url='https://discord.gg/Z84Nm6n'
        ),
        status = discord.Status.dnd
    )
    global ever_connected
    if ever_connected:
        bot.load_extension('util.botlst')
        bot.unload_extension('util.botlst')
        await channel.send(
            embed = embedify.embedify(
                desc = f'''```md
#] PRIZM IS ONLINE ;]``````md
> https://voxelprismatic.github.io/prizm.dev/
> You can support development over on Patreon!
> - https://patreon.com/voxelprismatic
] {' '.join(random.choice(face) for x in range(3))}```''',
                time = 'now'
            )
        )
        await run_twitter()


@bot.listen()
async def on_ready():
    msg = await bot.get_channel(569698278271090728).send("```md\n#] STARTING...```")
    ctx = await bot.get_context(msg)
    try:
        await ctx.invoke(restart)
    except Exception as ex:
        await bot.get_channel(556247032701124650).send(f"<@481591703959240706> Something broke: ```{type(ex)}: {ex}``````{ex.__traceback__.tb_lineno}```")
    face = faces.faces()
    texts = faces.texts()
    await bot.change_presence(
        activity = discord.Activity(
            type = 3,
            name = f"{random.choice(texts)} {random.choice(face)}",
            url = 'https://discord.gg/Z84Nm6n'
        ),
        status = discord.Status.idle
    )
    jsons(bot)
    print(time.time())
    bot.load_extension('util.botlst')
    bot.unload_extension('util.botlst')
    pages.init()
    gld = '>'+'\n>'.join(g.name for g in bot.guilds)
    print(f'''
GLD
{gld}

GG! PRIZM ;] // v{discord.__version__}
''')
    global ever_connected
    ever_connected = True
    await run_twitter()

@bot.listen()
async def on_disconnect():
    dbman.save()
    channel = bot.get_channel(556247032701124650)
    await channel.purge(limit = 10)



##///---------------------///##
##///      BOT EVENT      ///##
##///---------------------///##

@bot.listen()
async def on_message(message):
    ct = message.content
    if re.search(r"\<\@\!?481591703959240706\>", message.content):
        await message.add_reaction("<:prizblu:574993427314376704>")

@bot.command()
@commands.is_owner()
async def load(ctx):
    loadmain()
    reload(pages)
    reload(embedify)
    reload(vox)
    reload(enbl)
    reload(jsonSave)
    reload(logic)
    reload(ez)
    reload(has)
    reload(refresh)
    reload(faces)
    pages.init()
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@bot.command(aliases=['debug','r','rst','db','dbug'])
@commands.is_owner()
async def restart(ctx):
    await bot.change_presence(
        activity = discord.Activity(
            type = 2,
            name = "HDD Clicking Sounds",
            url = 'https://discord.gg/Z84Nm6n'
        ),
        status = discord.Status.dnd
    )
    face = faces.faces()
    texts = faces.texts()
    channel = bot.get_channel(556247032701124650)
    await channel.purge(limit = 10)
    m = await channel.send(
        embed = embedify.embedify(
            desc = f'''```diff
+] PRIZM IS LOADING ;]``````md
> Currently loading commands and things
> This may take a while, please stand by
> - If it takes too long, I will restart
] {' '.join(random.choice(face) for x in range(3))}```''',
            time = 'now'
        )
    )
    fail = False
    msg = await ctx.send('```md\n#] SAVING DATABASE```')
    dbman.save()
    await msg.edit(content = '```md\n#] UNLOADING COMMANDS```')
    allext,lodtxt = refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]:
            try:
                uext(f"{lodtxt[ext]}{com}")
            except:
                pass
    await msg.edit(content = '```md\n#] RELOADING MODULES```')
    try:
        reload(pages)
        reload(embedify)
        reload(vox)
        reload(enbl)
        reload(jsonSave)
        reload(logic)
        reload(ez)
        reload(has)
        reload(refresh)
        reload(faces)
        pages.init()
    except Exception as ex:
        await ctx.send(f'```diff\n-] MODULE ERROR - {ex}```')
        fail = True
    else:
        await msg.edit(content = '```md\n#] LOADING COMMANDS```')
    allext, lodtxt = refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]:
            try:
                lext(f"{lodtxt[ext]}{com}")
            except Exception as ex:
                await ctx.send(f'```diff\n-] COMMAND ERROR `{ex}` IN {com}```')
                fail = True
    await msg.edit(content = '```md\n#] REFRESHING DATABASE```')
    try:
        jsons(ctx.bot)
    except Exception as ex:
        await ctx.send(f'```diff\n-] DATABASE ERROR - {ex}```')
        fail = True
    await msg.edit(content = "```md\n#] CHECKING GITHUB HOSTING```")
    git = "/home/priz/prizm-hosting/"
    n = 0
    for f in os.listdir(git):
        if f != "README.md" and time.time() - os.stat(git + f).st_mtime >= 86400:
            os.system(f"git -C {git} rm {f}")
            n += 1
    if n:
        await msg.channel.send("<@481591703959240706> Check github hosting")
    await msg.edit(content = '```md\n#] SAVING DATABASE```')
    dbman.save()
    await channel.purge(limit = 10)
    if not fail:
        await msg.edit(content = '```md\n#] RESTARTED SUCCESSFULLY```')
        await channel.send(
            embed = embedify.embedify(
                desc = f'''```md
#] PRIZM IS ONLINE ;]``````md
> https://voxelprismatic.github.io/prizm.dev/
> You can support development over on Patreon!
> - https://patreon.com/voxelprismatic
] {' '.join(random.choice(face) for x in range(3))}```''',
                time = 'now'
            )
        )
    else:
        await msg.edit(content = '```md\n#] SOME MODULES FAILED TO RESTART```')
        await channel.send(
            embed = embedify.embedify(
                desc = f'''```diff
-] PRIZM IS BROKEN ;[``````md
> Some features may not work correctly
> Be sure to report any bugs using this command:
> - ;]bug {'{the bug}'}
] {' '.join(random.choice(face) for x in range(3))}```''',
                time = 'now'
            )
        )
    bot.broken = fail
    face = faces.faces()
    texts = faces.texts()
    await bot.change_presence(
        activity = discord.Activity(
            type = 3,
            name = f"{random.choice(texts)} {random.choice(face)}",
            url = 'https://discord.gg/Z84Nm6n'
        ),
        status = discord.Status.idle
    )

@bot.listen()
async def on_guild_join(gld):
    msg = await bot.get_channel(569698278271090728).send(
        f"```md\n#] JOINED A GUILD, RESTARTING\n> {gld.name}```"
    )
    ctx = await bot.get_context(msg)
    await ctx.invoke(restart)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##

reconnect = 0
secrets = open("secrets.txt").read().strip()
bot.run(secrets) #Security...
