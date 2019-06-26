#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print('##/// IMPORT ///##')

##/// DEPENDENCIES
import os
import ast
import typing
print('##///  [03]  ///##')
import discord                    #python3.7 -m pip install -U discord.py
import logging
import numpy as np                #python3.7 -m pip install -U numpy
print('##///  [06]  ///##')
import numexpr as ne              #python3.7 -m pip install -U numexpr
import datetime, time
import aiofiles, io, asyncio      #python3.7 -m pip install -U aiofiles
print('##///  [12]  ///##')
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib, math, statistics, random
import platform, sys, sysconfig, traceback, shlex
import subprocess,json
print('##///  [24]  ///##')
from shlex import quote
from ast import literal_eval
from discord.ext import commands
print('##///  [27]  ///##')
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from importlib import reload

print('##///  DONE  ///##')
print('##/// DEFINE ///##')

def getPre(bot,msg):
    id = msg.guild.id
    try:return json.load(open('prefixes.json'))[str(id)]
    except Exception as ex:print(ex);return ";]"

bot = commands.Bot(command_prefix=getPre)
client = discord.Client()
bot.remove_command("help")
logging.basicConfig(level='INFO')
with open('secrets.txt', mode='r') as KEY: secrets = KEY.readlines()

print('##///  DONE  ///##')

##///---------------------///##
##///  IMPORT EXTRA CODE  ///##
##///---------------------///##

print('##/// IMPORT ///##')

st = ''
try: 
    from util import pages; pages.init();print('SUCCESS - PAGES')
    from util import embedify; print('SUCCESS - EMBED')
    import PrizAI_CODE; print('SUCCESS - MAIN AI')
    import PrizAI_IMPROVED; print('SUCCESS - BETTER AI')
except Exception as ex: st = ex; print(st)

from dyn import refresh, faces

def lext(name): bot.load_extension(name); print(f'>Lext {name}')
def rext(name): bot.reload_extension(name); print(f'>Rext {name}')
def uext(name): bot.unload_extension(name); print(f'>Uext {name}')
def loadmain():
    et = ["ld","rld","uld","fld"]
    for ec in et:
        try: bot.load_extension(f"com.own.{ec}")
        except: bot.reload_extension(f"com.own.{ec}")

allext, lodtxt = refresh.refresh()

loadmain()

print('##///  DONE  ///##')

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

print('##/// DEFINE ///##')

def jsons():
    pre = json.load(open('prefixes.json'))
    com = json.load(open('servers.json'))
    for g in bot.guilds:
        try: x = pre[str(g.id)]
        except: pre[str(g.id)] = ';]'
        try: x = com[str(g.id)]
        except:
            com[str(g.id)]={}
            com[str(g.id)]["com"]={}
            com[str(g.id)]["tag"]={}
        for c in bot.commands:
            try: x = com[str(g.id)]["com"][c.name]
            except: com[str(g.id)]["com"][c.name] = True
    open('servers.json','w').write(json.dumps(com,sort_keys=True,indent=4))
    open('prefixes.json','w').write(json.dumps(pre,sort_keys=True,indent=4))

def FilesLoad(rw): #// Making life easy when the actual code comes
    global PrizM2MR, PrizM2MC, PrizTXT, PrizMATHl, PrizSCIl, PrizENGl, PrizMATHr, PrizSCIr, PrizENGr #Or this wont work at all
    PrizM2MR = aiofiles.open('PrismaticM2M-R', mode=rw)     #M2M Read File
    PrizM2MC = aiofiles.open('PrismaticM2M-C', mode=rw)     #M2M Send File
    PrizTXT = aiofiles.open('PrismaticText', mode=rw)       #Response Data
    PrizMATHl = aiofiles.open('MathIn', mode=rw)            #Learned Math Words
    PrizSCIl = aiofiles.open('SciIn', mode=rw)              #Learned Sci Words
    PrizENGl = aiofiles.open('EngIn', mode=rw)              #Learned Eng Words
    PrizMATHr = aiofiles.open('MathOut', mode=rw)           #Math Response
    PrizSCIr = aiofiles.open('SciOut', mode=rw)             #Sci Response
    PrizENGr = aiofiles.open('EngOut', mode=rw)             #Eng Response
    print('R/W TO FILES')
##/// Currently, the above is only used to READ data for the below section, but i'd rather have it now in case i need it later

async def ArraysLoad():
    global M2M1, M2M2, AI, MATHl, SCIl, ENGl, MATHr, SCIr, ENGr
    FilesLoad('r')
    async with PrizM2MR as mm1, PrizM2MC as mm2, PrizTXT as textR, PrizMATHl as math1R, PrizSCIl as sci1R, PrizENGl as eng1R, PrizMATHr as math2R, PrizSCIr as sci2R, PrizENGr as eng2R:
        M2M1 = await mm1.readlines()
        M2M2 = await mm2.readlines()
        AI = await textR.readlines()
        MATHl = await math1R.readlines()
        SCIl = await sci1R.readlines()
        ENGl = await eng1R.readlines()
        MATHr = await math2R.readlines()
        SCIr = await sci2R.readlines()
        ENGr = await eng2R.readlines()
        print('LOADED ARRAYS')

async def exc(ctx, code: int):
    await log('EXCEPTION!',f'TYPE // {code} \n> OCCURED IN // {ctx.channel}\n> 1] BadReq // 2] AllForbid // 3] 404')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

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
    jsons()
    if st != '': await log('MODULE ERROR',st)
    await bot.change_presence(activity=discord.Activity(type=2,name="HDD clicking sounds",
                              url='https://discord.gg/Z84Nm6n'))
    for ext in range(len(allext)):
        for com in allext[ext]: lext(f'{lodtxt[ext]}{com}')
    print(time.time())
    FilesLoad('r')
    await ArraysLoad()
    print('If an error didn\'t show up yet, then all should be good')
    print(f'''
{bot.guilds}

{[bot.get_all_channels()]}

GG! !] PRIZ AI ;] [! // v{discord.__version__} // RESTART - CTRL Z, [up], [enter]
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


##///---------------------///##
##///      BOT EVENT      ///##
##///---------------------///##

@bot.listen()
async def on_message(message):
    ct = message.content
    if "<@481591703959240706>" in message.content or "<@!481591703959240706>" in message.content:
        await message.add_reaction("<:prizblu:574993427314376704>")
    elif bot.user != message.author:
        if ct.startswith(']'): await PrizAI_CODE.on_message(bot, message)
        elif ct.startswith('}'): await PrizAI_IMPROVED.on_message(bot, message)
        elif message.channel.id== 590691192430133269: open('PrismaticText','a').write(ct.lower()+'\n')

@bot.command()
@commands.is_owner()
async def load(ctx):
    loadmain()
    reload(refresh)
    reload(faces)
    reload(pages)
    reload(embedify)
    reload(PrizAI_CODE)
    reload(PrizAI_IMPROVED)
    pages.init()
    await ctx.message.add_reaction('\N{OK HAND SIGN}')

@bot.command(aliases=['debug','r','rst','db','dbug'])
@commands.is_owner()
async def restart(ctx):
    fail = False
    msg = await ctx.send('```md\n#] UNLOADING COMMANDS```')
    allext,lodtxt=refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]: 
            try: uext(f"{lodtxt[ext]}{com}")
            except: pass
    await msg.edit(content='```md\n#] RELOADING MODULES```')
    try:
        reload(refresh)
        reload(faces)
        reload(pages)
        reload(embedify)
        reload(PrizAI_CODE)
        reload(PrizAI_IMPROVED)
        pages.init()
    except Exception as ex: await ctx.send(f'```diff\n-] MODULE ERROR\n=] {ex}```'); fail = True
    else: await msg.edit(content='```md\n#] LOADING COMMANDS```')
    allext,lodtxt=refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]: 
            try: lext(f"{lodtxt[ext]}{com}")
            except Exception as ex: 
                await ctx.send(f'```diff\n-] COMMAND ERROR\n=] {ex}\n=] {com}```'); fail = True
    await msg.edit(content='```md\n#] REFRESHING JSONs```')
    try: jsons()
    except Exception as ex: await ctx.send(f'```diff\n-] JSON ERROR\n=] {ex}```')
    if not fail: await msg.edit(content='```md\n#] MODULES\n> Literally everything reloaded, successfully too :D```')
    

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##

key = secrets[0] ##/// For security...
bot.run(key)
client.run(key)
