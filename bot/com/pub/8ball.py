#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ["8b","8bl",'8ball'],
                  help='fun',
                  brief='I definitely predict the future',
                  usage=';]8ball {question}',
                  description='''\
QUESTION [STR] What do you want me to answer
''')
@commands.check(enbl)
async def ball8(ctx, question = ""):
    choices = ['As I see it, yee',
               'Ask again later',
               'I shouldn\'t tell you',
               'Woops, I forgot what I was going to say',
               'Concentrate on your answer, and I\'ll repeat it',
               'Don\'t count on it mate',
               'Certainly',
               'Probably',
               'Most likely',
               'Maybe',
               'I say no',
               'My [1] source[s] say no',
               'Seems good',
               'Seems not so good',
               'I didn\'t care to answer this time, try again',
               'I doubt it and I\'m a downer',
               'With many or none doubts',
               'Yee fam',
               'Yeet!',
               'Boi you can believe it',
               'Bruh why are you asking a silly 8ball command']
    await ctx.send('```'+random.choice(choices)+'```')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(ball8)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('ball8')
    print('GOOD')
