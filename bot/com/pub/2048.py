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

def getString(grid:list, disp = False):
    gridString = ''
    for row in grid:
        for col in row:
            if type(col) == str and disp:
                gridString += f'[>{col:^2}<]'
            else:
                gridString += f'[{col:^4}]'
        gridString += '\n'
    return gridString.replace('0',' ')

def clearBlank(row):
    for loop in range(3):
        for col in range(len(row)-1):
            row[col] = int(row[col])
            row[col+1] = int(row[col+1])
            pt1 = int(row[col])
            pt2 = int(row[col+1])
            if pt2 == 0:
                row[col+1] = int(row[col])
                row[col] = 0
    return row

def groupRow(row, score):
    row = clearBlank(row)[::-1]
    skip = False
    for col in range(len(row)-1):
        if skip:
            skip = False
            continue
        pt1 = row[col]
        pt2 = row[col+1]
        if pt1 == pt2:
            row[col] = 0
            row[col+1] *= 2
            score += row[col+1]
            skip = True
    row = clearBlank(row[::-1])
    return row, score

def invertGrid(grid):
    for y in range(len(grid)):
        for x in range(y,len(grid[y])):
            temp = grid[y][x]
            grid[y][x] = grid[x][y]
            grid[x][y] = temp
    return grid

def mRight(grid, score):
    for row in range(len(grid)):
        grid[row], score = groupRow(grid[row], score)
    return grid, score

def mLeft(grid, score):
    for row in range(len(grid)):
        grid[row], score = groupRow(grid[row][::-1], score)
        grid[row] = grid[row][::-1]
    return grid, score

def mDown(grid, score):
    grid, score = mRight(invertGrid(grid), score)
    grid = invertGrid(grid)
    return grid, score

def mUp(grid, score):
    grid, score = mDown(grid[::-1], score)
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
SIZE [INT] - The size [is square] DEFAULT: 4
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
    msg = await ctx.send(embed=embedify(title='2048 ;]',
                                        desc = f'```{getString(grid)}\nSCORE ] 0```'))

    games[msg.id] = {'scr':score,
                     'msg':msg,
                     'usr':ctx.author,
                     'grd':grid,
                     'tme':time.monotonic()}

    for rct in ['<:al:598301447066484747>', '<:aD:612745739650727937>', '<:stp:598301603069689876>', '<:aU:612745775105179648>', '<:ar:598301483645141003>']:
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
                    await imsg.edit(title='2048 ;]',
                                    desc = f'```{getString(grid)}\nSCORE ] {games[tmsg]["scr"]}```',
                                    foot = 'TIMEOUT')
                    await imsg.clear_reactions()
            for m in delet:
                del games[m]
        else:
            if time.monotonic() - updated < .5:
                continue
            moves = {'<:ar:598301483645141003>': mRight,
                     '<:al:598301447066484747>': mLeft ,
                     '<:aD:612745739650727937>': mDown ,
                     '<:aU:612745775105179648>': mUp   }
            move = str(rct.emoji)

            if move in moves:
                gridNow = getString(grid)
                grid, score = moves[move](grid, score)
                games[rct.message.id] = {'scr':score,
                             'msg':rct.message,
                             'usr':usr,
                             'grd':grid,
                             'tme':time.monotonic()}
            elif move == '<:stp:598301603069689876>':
                del games[rct.message.id]
                await rct.message.edit(embed=embedify(title='2048 ;]',
                           desc = f'```{getString(grid)}\nSCORE ] {score}```',
                           foot = 'YOU ENDED THE GAME'))
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
                able = False
                for row in range(len(grid)):
                    for col in range(len(grid[row])):
                        if grid[row][col] == grid[row][col+1] and col != len(grid[row])-1:
                            able = True
                        elif grid[row][col] == grid[row][col-1] and col != 0:
                           able = True
                        elif grid[row][col] == grid[row+1][col] and row != len(grid)-1:
                           able = True
                        elif grid[row][col] == grid[row-1][col] and row != 0:
                           able = True
                        if 0 in grid[row]:
                           able = True
                if not able:
                    del games[msg.id]
                    await rct.message.edit(embed=embedify(title='2048 ;]',
                           desc = f'```{getString(grid)}\nSCORE ] {score}```',
                           foot = 'YOU LOST'))
                try:
                    await rct.message.clear_reactions()
                except:
                    pass
                continue
            elif getString(grid) != gridNow:
                grid[y][x] = choice(['2','4'])
                score += int(grid[y][x])
            await rct.message.edit(embed=embedify(title='2048 ;]',
                           desc = f'```{getString(grid, True)}\nSCORE ] {score}```'))
            await rct.message.remove_reaction(rct, usr)
            games[rct.message.id] = {'scr':score,
                             'msg':rct.message,
                             'usr':usr,
                             'grd':grid,
                             'tme':time.monotonic()}


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
