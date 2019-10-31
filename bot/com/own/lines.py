#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
import aiofiles

@commands.command(help="own")
@commands.is_owner()
async def lines(ctx, filename, line: int):
    async with aiofiles.open(filename) as fl:
        await ctx.send('```'+''.join(list(await fl.readlines())[line-10:line+11]).replace('`', '`\u200b`')+'```')

def setup(bot):
    bot.add_command(lines)

def teardown(bot):
    bot.remove_command("lines")