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
from PIL import Image
import os

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def hexcolor(st: str):
    return "".join(random.choice(st) for x in range(6))

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = ["rgb", "#"],
    help = 'oth',
    brief = 'Displays a random color in hex',
    usage = ';]colors {?color or scheme}',
    description = '''\
COLOR OR SCHEME [STR] - The color or scheme you want to display
'''
)
@commands.check(enbl)
async def colors(ctx, *colors):
    desc = ""
    disps = []
    colors = colors or [""]
    for color in colors:
        if re.search(r"^#[A-Fa-f0-9]{6}$", color):
            cat = "CUSTOM"
            disp = color[1:]
        elif re.search(r"^#[A-Fa-f0-9]{3}$", color):
            cat = "CUSTOM"
            disp = color[1] + color[1] + color[2] + color[2] + color[3] + color[3]
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
        desc += f"`{cat}` - `#{disp}`\n"
        disps.append(disp)
    img = Image.new("RGB", (256, 256))
    for i in range(len(colors)):
        disp = disps[i]
        r = int(disp[0:2], 16)
        g = int(disp[2:4], 16)
        b = int(disp[4:6], 16)
        xr = int(256 / len(colors))
        for x in range(xr * i, xr * (i + 1)):
            for y in range(256):
                img.putpixel((x, y), (r, g, b))
    img.save("color.png", "PNG")
    await ctx.send(
        embed = emb(
            title = "PRIZM COLORS ;]",
            desc = desc,
            color = int(disp, 16),
        ),
        file = discord.File(open("color.png", "rb"), disp.upper() + ".PNG")
    )
    os.remove("color.png")

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

