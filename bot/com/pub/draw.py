#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, random, typing, re
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.embedify import embedify
import PIL

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

def cl(rgb):
    return hex(rgb)[2:].zfill(2)
def larger(img):
    img = img.resize((1024, 1024))
    img.save("msc/pub_img.png")
    return img

def smaller(img):
    img = img.resize((128, 128))
    img.save("msc/pub_img.png")
    return img

@commands.command(aliases = ['paint', 'color', 'canvas', 'painting', 'drawing', 'coloring'],
                      help = 'fun',
                      brief = 'Have fun drawing with others!',
                      usage = ';]draw {?color} {?x1} {?y1} {?x2} {?y2} {...} {?xN} {?yN}',
                      description = '''\
COLOR  [TEXT] - The color you want to place, MUST BE HEX
xN, yN [ANY ] - The XY coordinates [MAX - 127, MIN - 0]
> You can use ranges like 0-16
> You can be relative like ~1
> You can use relative ranges like ~9-26
*If no params are passed, the image is sent
*If only coordinates are passed, the color at that coordinate is sent along with the image
*ALL relative points are relative to YOUR last point
''')
@commands.check(enbl)
async def draw(ctx, color: str = "", *args: str):
    sr = re.search
    img = PIL.Image.open("msc/pub_img.png")
    if not len(args) or (len(args)%2 and not len(args) == 1):
        img = larger(img)
        await ctx.send("```md\n#] CURRENT PAINTING```",
                       file=discord.File("msc/pub_img.png"))
        smaller(img)
    elif sr(r"^\d+$", color) and sr(r"^\d+$", args[0]) and len(args) == 1:
        x, y = int(color), int(args[0])
        rgb = img.getpixel((x, y))
        larger(img)
        await ctx.send(f"```md\n#] COLOR AT {x}, {y} ] #{(cl(rgb[0])+cl(rgb[1])+cl(rgb[2])).upper()}```",
                       file= discord.File("msc/pub_img.png"))
        img = smaller(img)
    elif not color or not sr(r"^\#[A-Fa-f0-9]{6}$", color):
        x, y = int(args[0]), int(args[1])
        rgb = PIL.Image.open("msc/pub_img.png").getpixel((x, y))
        await ctx.send(f"```md\n#] COLOR AT {x}, {y} ] #{(cl(rgb[0])+cl(rgb[1])+cl(rgb[2])).upper()}```",
                       file= discord.File("msc/pub_img.png"))
    else:
        X, Y = 0, 0
        rgb = (int(color[1:3], 16), int(color[3:5], 16), int(color[5:], 16))
        coord = []
        for x, y in [(args[x], args[x+1]) for x in range(0, len(args), 2)]:
            if sr(r"^\d+$", x):
                Nx = [int(x)] #Just an int
            elif sr(r"^\~\d+$", x):
                Nx = [X+int(x[1:])] #Relative
            elif sr(r"^\d+-\d+$", x):
                Nx = [Rx for Rx in range(int(x.split("-")[0]), int(x.split("-")[1])+1)] #Range
            elif sr(r"^\~\d+-\d+$", x):
                Nx = [Rx for Rx in range(X+int(x.split("-")[0][1:]), X+int(x.split("-")[1])+1)] #Relative Range
            else:
                Nx = [X]
            if sr(r"^\d+$", y):
                Ny = [int(y)] #Just an int
            elif sr(r"^\~\d+$", y):
                Ny = [Y+int(y[1:])] #Relative
            elif sr(r"^\d+-\d+$", y):
                Ny = [Ry for Ry in range(int(y.split("-")[0]), int(y.split("-")[1])+1)] #Range
            elif sr(r"^\~\d+-\d+$", y):
                Ny = [Ry for Ry in range(Y+int(y.split("-")[0][1:]), Y+int(y.split("-")[1])+1)] #Relative Range
            else:
                Ny = [Y]
            for Wx in Nx:
                for Wy in Ny:
                    coord.append((Wx, Wy))

            X, Y = coord[-1]

        for x, y in coord:
            img.putpixel((x, y), rgb)
        img.save("msc/pub_img.png", "png")
        img = larger(img)
        await ctx.send(f"```md\n#] COLOR {color} PLACED```",
                      file=discord.File("msc/pub_img.png"))
        smaller(img)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(draw)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('draw')
    print('GOOD')
