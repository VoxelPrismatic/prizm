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
import json
from discord.ext import commands
from discord.ext.commands import Bot
from importlib import reload

print('##///  DONE  ///##')
print('##/// DEFINE ///##')

def getPre(bot,msg):
    try:
        return json.load(open('json/prefixes.json'))[str(msg.guild.id)]
    except Exception as ex:
        print(ex)
        return ";]"

bot = commands.Bot(command_prefix=getPre,case_insenitive=True)
bot.remove_command("help")
logging.basicConfig(level='INFO')
with open('secrets.txt', mode='r') as KEY:
    secrets = KEY.read().strip()
print(secrets)

print('##///  DONE  ///##')

##///---------------------///##
##///  IMPORT EXTRA CODE  ///##
##///---------------------///##

print('##/// IMPORT ///##')

st = ''
try:
    from util import pages
    pages.init()
    print('SUCCESS - PAGES')
    from util import embedify
    print('SUCCESS - EMBED')
    from util import vox
    print('SUCCESS - VOX')
    from chk import enbl
    print('SUCCESS - ENBL')
    from util import jsonSave
    print('SUCCESS - SAVER')
except Exception as ex:
    st = ex
    print(st)

from dyn import refresh, faces

def lext(name):
    print(f'>Lext {name}')
    bot.load_extension(name)
def rext(name):
    print(f'>Rext {name}')
    bot.reload_extension(name)
def uext(name):
    print(f'>Uext {name}')
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

@bot.listen()
async def on_ready():
    global st
    if st != '':
        await log('MODULE ERROR',st)
    await bot.change_presence(activity=discord.Activity(type=2,name="HDD clicking sounds",
                              url='https://discord.gg/Z84Nm6n'))
    for ext in range(len(allext)):
        for com in allext[ext]:
            lext(f'{lodtxt[ext]}{com}')
    jsons(bot)
    print(time.time())
    bot.load_extension('util.botlst')
    print('If an error didn\'t show up yet, then all should be good')
    gld = '>'+'\n>'.join(g.name for g in bot.guilds)
    print(f'''
GLD
{gld}

GG! PRIZM ;] // v{discord.__version__} // RESTART - CTRL Z, [up], [enter]
''')
    channel = bot.get_channel(556247032701124650)
    await channel.purge(limit=10)
    face = faces.faces()
    texts = faces.texts()
    await bot.change_presence(activity=discord.Activity(type=3,
                              name=f"{random.choice(texts)} {random.choice(face)}",
                              url='https://discord.gg/Z84Nm6n'))
    await channel.send(embed=embedify.embedify(desc=f'''```md
#] I\'M BACK ONLINE!!!
> All the Voxels are textured ;]
> I am still in the testing phase :C
> Watch me be entirely re-written 0.0
> Turned on: {str(datetime.datetime.now())} :D
#] HOPEFULLY UP 24/7 {random.choice(face)}```'''))
    pages.init()

@bot.listen()
async def on_disconnect():
    print('ATTEMPT LOGIN')
    await bot.connect()
    await asyncio.sleep(5)

##///---------------------///##
##///      BOT EVENT      ///##
##///---------------------///##

@bot.listen()
async def on_message(message):
    ct = message.content
    #words = json.load(open('json/servers.json'))[str(message.guild.id)]["wrd"]
    #for word in ct.split():
        #if len(words['wrd']) == 0: break
        #if word in words['wrd']:
            #if words['act'].lower() == 'ban': await message.author.ban(reason='Used a word on the banned word list')
            #elif words['act'].lower() == 'kick': await message.author.kick(reason='Used a word on the banned word list')
            #await message.delete()
            #break

    if "<@481591703959240706>" in message.content or "<@!481591703959240706>" in message.content:
        await message.add_reaction("<:prizblu:574993427314376704>")

@bot.command()
@commands.is_owner()
async def load(ctx):
    loadmain()
    reload(refresh)
    reload(faces)
    reload(pages)
    reload(embedify)
    reload(vox)
    reload(enbl)
    reload(jsonSave)
    pages.init()
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

@bot.command(aliases=['debug','r','rst','db','dbug'])
@commands.is_owner()
async def restart(ctx):
    fail = False
    msg = await ctx.send('```md\n#] UNLOADING COMMANDS```')
    allext,lodtxt=refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]:
            try:
                uext(f"{lodtxt[ext]}{com}")
            except:
                pass
    await msg.edit(content='```md\n#] RELOADING MODULES```')
    try:
        reload(refresh)
        reload(faces)
        reload(pages)
        reload(embedify)
        reload(vox)
        reload(enbl)
        reload(jsonSave)
        pages.init()
    except Exception as ex:
        await ctx.send(f'```diff\n-] MODULE ERROR\n=] {ex}```')
        fail = True
    else:
        await msg.edit(content='```md\n#] LOADING COMMANDS```')
    allext,lodtxt=refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]:
            try:
                lext(f"{lodtxt[ext]}{com}")
            except Exception as ex:
                await ctx.send(f'```diff\n-] COMMAND ERROR\n=] {ex}\n=] {com}```')
                fail = True
    await msg.edit(content='```md\n#] REFRESHING JSONs```')
    try:
        jsons(ctx.bot)
    except Exception as ex:
        await ctx.send(f'```diff\n-] JSON ERROR\n=] {ex}```')
        fail = True
    if not fail:
        await msg.edit(content='```md\n#] MODULES\n> Literally everything restarted, successfully too :D```')
    else:
        await msg.edit(content='```md\n#] MODULES\n> Restarting completed```')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##

key = secrets ##/// For security...
bot.run(key)
