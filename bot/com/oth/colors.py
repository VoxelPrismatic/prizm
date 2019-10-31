#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord
import random, re
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.embedify import *

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def hexcolor(st: str):
    return "".join(random.choice(st) for x in range(6))

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["hex"],
                  help='oth',
                  brief='Displays a random color in hex',
                  usage=';]colors {?color or scheme}',
                  description='COLOR OR SCHEME [STR] - The color or scheme you want to display')
@commands.check(enbl)
async def colors(ctx, color=""):
    if re.search(r"^#[A-Fa-f0-9]{6}$", color):
        cat = "CUSTOM"
        disp = color[1:]
    elif color.lower() == "pastel":
        cat = "PASTEL"
        disp = hexcolor("fca864")
    elif color.lower() == "dark":
        cat = "DARK"
        disp = hexcolor("76543210")
    elif color.lower() == "light":
        cat = "LIGHT"
        disp = hexcolor("fedcba98")
    elif color.lower() == "prizm":
        cat = "PRIZM ;]"
        disp = random.choice(
            ["00ffff", "00ff00", "ff0000", "ff8800", #Cyan, Green, Red, Orange
             "ffff00", "8800ff", "ff00ff", "ff0088", #Yellow, Purple, Magenta, Pink
             "888888", "112222", "aaffff", "00ff88", #Grey, Dark, Light, Seafoam
             "0088ff", "88ff00", "880088", "008888"] #Blurple, Green-Yellow, Purple, Turqoise
        )
    else:
        cat = "RNG"
        disp = hexcolor("0123456789abcdef")
    await ctx.send(embed=emb(title="PRIZM COLORS ;]", 
                   desc=f"[{cat}] - #{disp}", color = int(disp, 16)))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(colors)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('colors')
    print('GOOD')

