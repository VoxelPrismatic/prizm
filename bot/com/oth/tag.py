#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import dbman
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.embedify import embedify

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                      help = 'oth',
                      brief = 'Custom commands, kinda',
                      usage = ';]tag {action} {?name} {?data}',
                      description = '''\
ACTION [TEXT] - The action you want to take
> Use the tag name to view the tag
> Use ';]edit {name} {content}' to edit your tag
> Use ';]add {name} {content}' to create a tag
> Use ';]delete {name}' to delete your tag
NAME   [TEXT] - Only used when adding or editing a tag
DATA   [TEXT] - The content when adding or editing a tag

    ''')
@commands.check(enbl)
async def tag(ctx, *, arg = ""):
    arg = arg.split()
    if len(arg) > 1:
        curTag = dbman.get('tag', 'stuff', id = ctx.guild.id, name = arg[1])
    if len(arg) == 0:
        await ctx.send(embed=embedify(desc='```md\n#] CREATED TAGS\n> '+"\n> ".join(dbman.get('tag', 'name', id = ctx.guild.id, return_as_list = True))+'```'))
    elif len(arg) == 1:
        itm = dbman.get('tag', 'stuff', id = ctx.guild.id, name = arg[0], return_null = True)
        if itm:
            return await ctx.send(itm.replace(">[\\n]<", "\n"))
        else:
            return await ctx.send('```diff\n-] TAG DOESN\'T EXIST```')

    elif arg[0] in ['-','destroy','remove','delete','kill'] and curTag:
        if dbman.get('tag', 'auth', id=ctx.guild.id, name=arg[1], rtn = int) == ctx.author.id:
            dbman.remove('tag', id = ctx.guild.id, name = arg[1])
            return await ctx.message.add_reaction('<:wrk:608810652756344851>')
        else:
            return await ctx.send('```diff\n-] YOU DIDNT MAKE THIS TAG```')


    elif arg[0] in ['+','make','add','create','new'] and not curTag:
        dbman.insert('tag', id = ctx.guild.id, name = arg[1], stuff = ctx.message.content.split(' ', 3)[-1].replace("\n", ">[\\n]<"), auth = ctx.author.id)
        return await ctx.message.add_reaction('<:wrk:608810652756344851>')

    elif arg[0] in ['/','edit'] and curTag:
        if dbman.get('tag', 'auth', id = ctx.guild.id, name = arg[1], rtn = int) == ctx.author.id:
            dbman.update('tag', 'stuff', ctx.message.content.split(' ', 3)[-1].replace("\n", ">[\\n]<"), id = ctx.guild.id, name = arg[1])
            return await ctx.message.add_reaction('<:wrk:608810652756344851>')
        else:
            return await ctx.send('```diff\n-] YOU DIDNT MAKE THIS TAG```')

    elif arg[0] in ['+','make','add','create','new'] and curTag:
        await ctx.send('```diff\n-] TAG ALREADY EXISTS```')

    elif arg[0] in ['/','edit', '-','destroy','remove','delete','kill'] and not curTag:
        await ctx.send('```diff\n-] TAG DOESN\'T EXIST```')

    else:
        await ctx.send('```diff\n-] TAG MODIFY ALIAS NOT FOUND```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(tag)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('tag')
    print('GOOD')
