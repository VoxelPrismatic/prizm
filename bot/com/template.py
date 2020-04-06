#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
from util import embedify, pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    help = 'cat',
    brief = '',
    usage = ';]',
    description = '''\
[NO INPUT FOR THIS COMMAND]
ARG [TYPE] - Description
'''
)
@commands.check(enbl)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(name)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('name')
    print('GOOD')

