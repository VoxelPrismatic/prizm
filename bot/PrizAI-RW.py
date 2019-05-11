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
print('##///  [22]  ///##')
from shlex import quote
from ast import literal_eval
from discord.ext import commands
print('##///  [25]  ///##')
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions

print('##///  DONE  ///##')
print('##/// DEFINE ///##')

bot = commands.Bot(command_prefix=";]")
client = discord.Client()
bot.remove_command("help")
logging.basicConfig(level='INFO')
with open('secrets.txt', mode='r') as KEY: secrets = KEY.readlines()

print('##///  DONE  ///##')

##///---------------------///##
##///  IMPORT EXTRA CODE  ///##
##///---------------------///##

print('##/// IMPORT ///##')

import PrizAI_CODE

def lext(name): bot.load_extension(name); print(f'>Lext {name}')
def rext(name): bot.reload_extension(name); print(f'>Rext {name}')
def uext(name): bot.unload_extension(name); print(f'>Uext {name}')

owncom = ["calc","clr0","clrin0","exe","helpown",
          "pin0","unpin0","pwr"]

modcom = ["ban","clr","clrin","kick","pin",
          "unpin"]

infcom = ["data","git","hlep","hlepmod","info",
          "os","ping", "hlepmini"]

pubcom = ["binary","blkjck","coin","cool","dnd",
          "echo","react","rick","rng","slots",
          "snd","spam","emji","rev",
          "asci","optn"]

discom = ["chnl","emj","gld","mbr","rol",
          "usr"]

mathcom = ["graph","quad","rto","stats","fct",
           "rad","fact"]

list_n = ["gld","err","mtn","com","rctf"]

allext = [owncom,modcom,infcom,pubcom,discom,mathcom,list_n]

lodtxt = ["com.own.","com.mod.","com.inf.","com.pub.","com.dis.","com.math.","lis."]

for ext in range(len(allext)):
    for com in allext[ext]: lext(f'{lodtxt[ext]}{com}')

print('##///  DONE  ///##')

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

print('##/// DEFINE ///##')


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

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)

async def exc(ctx, code: int):
    await log('EXCEPTION!',f'TYPE // {code}\n> OCCURED IN // {ctx.channel}\n> 1] BadReq // 2] AllForbid // 3] 404')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

async def log(head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

print('##///  DONE  ///##')

##///---------------------///##
##///      BOT LOOPS      ///##
##///---------------------///##

print('##// STARTING //##')

@bot.listen()
async def on_ready():
    print(time.time())
    FilesLoad('r')
    await ArraysLoad()
    print('If an error didn\'t show up yet, then all should be good')
    bot.locked = False
    print(f'''
{bot.guilds}

{[bot.get_all_channels()]}

GG! !] PRIZ AI ;] [! // v{discord.__version__}// RESTART - CTRL Z, [up], [enter]
''')
    channel = bot.get_channel(556247032701124650)
    await channel.purge(limit=10)
    texts = ["the Prisms fly by 0.0",
             "the Voxels get retextured 0.0",
             "the Prisms get some love <3",
             "the Voxels get built ;]",
             "the Prisms Shininess 0.0",
             "the Voxels Cubeness >.<"]
    await bot.change_presence(activity=discord.Activity(type=3, name=random.choice(texts), url='https://discord.gg/Z84Nm6n'))
    await channel.send(embed=embedify(f'''```md
#] I\'M BACK ONLINE!!!
> All the Voxels are textured ;]
> I am still in the testing phase :C
> Watch me be entirely re-written 0.0
> Turned on: {str(datetime.datetime.now())} :D
#] Turns Off at 8PM CST XC```'''))

##///---------------------///##
##///      BOT EVENT      ///##
##///---------------------///##

@bot.listen()
async def on_message(message):
    if "<@481591703959240706>" in message.content or "<@!481591703959240706>" in message.content:
        await message.add_reaction(bot.get_emoji(574993427314376704))
    elif bot.user != message.author: await PrizAI_CODE.on_message(bot, message)

##///---------------------///##
##///   LIVE  RELOADING   ///##
##///---------------------///##

@bot.command()
@commands.is_owner()
async def rld(ctx, *name):
    await log('EXT', 'Reloading ext(s)')
    if not len(name):
        for ext in range(len(allext)):
            for com in allext[ext]: rext(f'{lodtxt[ext]}{com}')
    else: rext(name[0])
    await log('EXT', 'ext(s) successfully reloaded')
    await ctx.message.add_reaction('👌')

@bot.command()
@commands.is_owner()
async def ld(ctx, *name):
    await log('EXT', 'Loading ext(s)')
    if not len(name):
        for ext in range(len(allext)):
            for com in allext[ext]: lext(f'{lodtxt[ext]}{com}')
    else: lext(name[0])
    await log('EXT', 'Ext(s) successfully loaded')
    await ctx.message.add_reaction('👌')

@bot.command()
@commands.is_owner()
async def uld(ctx, *name):
    await log('EXT', 'Unloading ext(s)')
    if not len(name):
        for ext in range(len(allext)):
            for com in allext[ext]: uext(f'{lodtxt[ext]}{com}')
    else: uext(name[0])
    await log('EXT', 'Ext(s) successfully unloaded')
    await ctx.message.add_reaction('👌')

@bot.command()
async def chng(ctx, *name):
    if len(name) != 0: texts = name
    else: texts = ["the Prisms fly by 0.0",
             "the Voxels get retextured 0.0",
             "the Prisms get some love <3",
             "the Voxels get built ;]",
             "the Prisms Shininess 0.0",
             "the Voxels Cubeness >.<"]
    await bot.change_presence(activity=discord.Activity(type=3, name=random.choice(texts), url='https://discord.gg/Z84Nm6n'))
    await ctx.message.add_reaction('👌')
##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##

key = secrets[0][:-1] ##/// For security...
bot.run(key)
client.run(key)
