#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, json
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.embedify import embedify

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='oth',
                  brief = 'Custom commands, kinda',
                  usage = ';]tag {action} {!name} {!data}',
                  description='''\
ACTION [STR] - The action you want to take
             > Use the tag name to view the tag
             > Use 'edit {name} {content}' to edit your tag
             > Use 'add {name} {content}' to create a tag
             > Use 'delete {name}' to delete your tag
!NAME  [STR] - Only used when adding or editing a tag
!DATA  [STR] - The content when adding or editing a tag''')
@commands.check(enbl)
@commands.guild_only()
async def tag(ctx, *arg):
    try:
        dic = json.load(open('json/servers.json'))
        tags = dic[str(ctx.guild.id)]["tag"]

        if len(arg) == 0:
            if len(tags) > 0: await ctx.send(embed=embedify(desc='```md\n#] CREATED TAGS\n> '+"\n> ".join(list(tags))+'```'))
            else: await ctx.send('```diff\n-] NO TAGS CREATED YET```')
        elif len(arg) == 1: await ctx.send(tags[arg[0]][0])

        elif arg[0] in ['-','destroy','remove','delete','kill']:
            if tags[arg[1]][1] == ctx.author.id:
                del dic[str(ctx.guild.id)]["tag"][arg[1]]
                open('json/servers.json','w').write(json.dumps(dic,sort_keys=True,indent=4))
                return await ctx.message.add_reaction('<:wrk:608810652756344851>')
            else: return await ctx.send('```diff\n-] YOU DIDNT MAKE THIS TAG```')

        elif arg[0] in ['+','make','add','create','new'] and arg[1] not in tags:
            dic[str(ctx.guild.id)]["tag"][arg[1]] = [ctx.message.content.split(maxsplit=3)[-1], ctx.author.id]
            open('json/servers.json','w').write(json.dumps(dic,sort_keys=True,indent=4))
            return await ctx.message.add_reaction('<:wrk:608810652756344851>')

        elif arg[0] in ['/','edit'] and arg[1] in tags:
            if tags[arg[1]][1] == ctx.author.id:
                del dic[str(ctx.guild.id)]["tag"][arg[1]]
                open('json/servers.json','w').write(json.dumps(dic,sort_keys=True,indent=4))
                dic = json.load(open('json/servers.json'))
                dic[str(ctx.guild.id)]["tag"][arg[1]] = [ctx.message.content.split(maxsplit=3)[-1], ctx.author.id]
                open('json/servers.json','w').write(json.dumps(dic,sort_keys=True,indent=4))
                return await ctx.message.add_reaction('<:wrk:608810652756344851>')
            else: return await ctx.send('```diff\n-] YOU DIDNT MAKE THIS TAG```')

        elif arg[0] in ['+','make','add','create','new'] and arg[1] in tags: await ctx.send('```diff\n-] TAG ALREADY EXISTS```')

        elif arg[0] in ['/','edit'] and arg[1] not in tags: await ctx.send('```diff\n-] TAG DOESN\'T EXIST```')

        else: await ctx.send('```diff\n-] TAG MODIFY ALIAS NOT FOUND```')

    except KeyError: await ctx.send('```diff\n-] TAG DOESN\'T EXIST```')

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
