#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, time
import discord                    #python3.7 -m pip install -U discord.py
import logging, random, asyncio, datetime
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from random import choice
from random import randint
from util.embedify import embedify

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

def coord(grid):
    height = list(range(len(grid)))
    width = list(range(len(grid[0])))
    return choice(width), choice(height)

def get_str(grid:list, disp = False):
    gridString = ''
    for row in grid:
        for col in row:
            if type(col) == str and disp:
                gridString += f'[>{col:^2}<]'
            else:
                gridString += f'[{col:^4}]'
        gridString += '\n'
    return gridString.replace('0',' ')
    
def merge(r, score):
    for x in range(len(r)-1, -1, -1):
        for c in range(x, len(r)-1):
            if r[c] != 0 and r[c+1] == 0:
                r[c], r[c+1] = r[c+1], r[c]
    r = r[::-1]
    for c in range(len(r)-1):
        if r[c] == r[c+1]:
            r[c], r[c+1] = 0, r[c]*2
            score += r[c+1]
    r = r[::-1]
    for x in range(len(r)-1, -1, -1):
        for c in range(x, len(r)-1):
            if r[c] != 0 and r[c+1] == 0:
                r[c], r[c+1] = r[c+1], r[c]
    return r

def invert(grid):
    """
    Inverts the grid for up/down movement
    """
    grid = grid[::-1]
    for y in range(len(grid)):
        grid[y] = grid[y][::-1]
    return grid

def mR(grid, score):
    """
    Moves all squares right
    """
    for row in range(len(grid)):
        grid[row], score = merge(grid[row], score)
    return grid, score

def mL(grid, score):
    """
    Moves all squares left
    """
    for row in range(len(grid)):
        grid[row], score = merge(grid[row][::-1], score)
        grid[row] = grid[row][::-1]
    return grid, score

def mD(grid, score):
    """
    Moves all squares down
    """
    grid, score = mR(invert(grid), score)
    grid = invert(grid)
    return grid, score

def mU(grid, score):
    """
    Moves all squares up
    """
    grid, score = mD(grid[::-1], score)
    grid = grid[::-1]
    return grid, score

games = {}

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ['2048'],
                  help='fun',
                  brief='2048 but in Discord',
                  usage=';]2048 {?size}',
                  description='''\
SIZE [NUMBER] - The size [is square] DEFAULT: 4
''')
@commands.check(enbl)
async def _2048(ctx, size:int=4):
    grid = [[0 for x in range(size)] for y in range(size)]
    x, y = coord(grid)
    grid[y][x] = 2
    x, y = coord(grid)
    while grid[y][x] != 0:
        x, y = coord(grid)
    grid[y][x] = 2
    score = 0
    msg = await ctx.send(
        embed = embedify(
            title='2048 ;]',
            desc = f'```{getString(grid)}\nSCORE ] 0```',
            foot = "PRIZM ;] // REACT TO MOVE"
        )
    )

    games[msg.id] = {
        'scr':score,
        'msg':msg,
        'usr':ctx.author,
        'grd':grid,
        'tme':time.monotonic()
    }

    for rct in [
            '<:al:598301447066484747>', 
            '<:aD:612745739650727937>',
            '<:stp:598301603069689876>',
            '<:aU:612745775105179648>',
            '<:ar:598301483645141003>'
        ]:
        await msg.add_reaction(rct)

    def verify(rct, usr):
        try:
            return usr == games[rct.message.id]['usr']
        except:
            pass
    while len(games):
        try:
            rct, usr = await ctx.bot.wait_for('reaction_add', timeout = 60.0, check = verify)
            try:
                score, msg, usr, grid, updated = games[rct.message.id].values()
            except:
                raise asyncio.TimeoutError
        except asyncio.TimeoutError:
            delet = []
            for tmsg in list(games)[:]:
                imsg=games[tmsg]["msg"]
                if imsg.edited_at is None:
                    tm = imsg.created_at.timestamp()
                else:
                    tm = imsg.edited_at.timestamp()
                if float(datetime.datetime.utcnow().timestamp()-tm) > 59:
                    delet.append(tmsg)
                    await imsg.edit(
                        embed = embedify(
                            title='2048 ;]',
                            desc = f'```{getString(grid)}\nSCORE ] {games[tmsg]["scr"]}```',
                            foot = 'PRIZM ;] // TIMEOUT'
                        )
                    )
                    try:
                        await imsg.clear_reactions()
                    except:
                        pass
            for m in delet:
                del games[m]
        else:
            if time.monotonic() - updated < .5:
                continue
            moves = {
                '<:ar:598301483645141003>': mR,
                '<:al:598301447066484747>': mL,
                '<:aD:612745739650727937>': mD,
                '<:aU:612745775105179648>': mU
            }
            move = str(rct.emoji)

            if move in moves:
                gridNow = getString(grid)
                grid, score = moves[move](grid, score)
                games[rct.message.id] = {
                    'scr':score,
                    'msg':rct.message,
                    'usr':usr,
                    'grd':grid,
                    'tme':time.monotonic()
                }
            elif move == '<:stp:598301603069689876>':
                del games[rct.message.id]
                await rct.message.edit(
                    embed = embedify(
                        title = '2048 ;]',
                        desc = f'```{getString(grid)}\nSCORE ] {score}```',
                        foot = 'PRIZM ;] // STOPPED'
                    )
                )
                try:
                    await rct.message.clear_reactions()
                except:
                    pass
                continue
            tries = []
            x, y = coord(grid)
            ttlCOL = len(grid[0])
            ttlROW = len(grid)
            while grid[y][x] != 0 and len(tries) != ttlCOL * ttlROW:
                x, y = coord(grid)
                if [y, x] not in tries:
                    tries.append([y, x])

            if len(tries) == ttlCOL * ttlROW:
                able = True
                if grid == mU(grid) and grid == mD(grid) \
                        and grid == mR(grid) and grid == mL(grid):
                    able = False
                
                if not able:
                    del games[msg.id]
                    await rct.message.edit(
                        embed = embedify(
                            title = '2048 ;]',
                            desc = f'```{getString(grid)}\nSCORE ] {score}```',
                            foot = 'PRIZM ;] // GAME OVER'
                        )
                    )
                try:
                    await rct.message.clear_reactions()
                except:
                    pass
                continue
            elif getString(grid) != gridNow:
                grid[y][x] = choice(['2','4'])
                score += int(grid[y][x])
            try:
                await rct.message.remove_reaction(rct, usr)
                r = "REACT"
            except:
                r = "RE-REACT"
            await rct.message.edit(
                embed = embedify(
                    title = '2048 ;]',
                    desc = f'```{getString(grid, True)}\nSCORE ] {score}```',
                    foot = f'PRIZM ;] // {r} TO MOVE'
                )
            )
            games[rct.message.id] = {
                'scr':score,
                'msg':rct.message,
                'usr':usr,
                'grd':grid,
                'tme':time.monotonic()
            }


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(_2048)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('_2048')
    print('GOOD')
