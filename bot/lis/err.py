#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback, sys
import json
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
def getPre(bot,msg):
    id = msg.guild.id
    try:return json.load(open('prefixes.json'))[str(id)]
    except Exception as ex:print(ex);return ";]"

bot = commands.Bot(command_prefix=getPre)

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify.embedify(desc=f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///     BOT  EVENTS     ///##
##///---------------------///##

@bot.listen()
async def on_error(event, *args, **kwargs):
    t, exception, info = sys.exc_info()
    await handler(bot, "EVENT FAILED", exception, event, None, None, *args, **kwargs)

@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): return await ctx.message.add_reaction('\u2753')
    if not json.load(open('servers.json'))[str(ctx.guild.id)]["com"][ctx.command.name]:
        return await ctx.send('```diff\n-] ERROR\n=] THIS COMMAND ISNT ENABLED```')
    try: errr = error.original
    except: errr = error
    st = str(type(errr)).split('.')[-1][:-2]
    typ, obj, tb = sys.exc_info() 
    errors = {
        'BadArgument': [400,'BAD ARGUMENT'],
        'BotMissingPermissions': [503,'BOT FORBIDDEN'],
        'MissingPermissions': [403,'USER FORBIDDEN'],
        'ConversionError': [503, 'UNAVAILABLE'],
        'MissingRequiredArgument': [416, 'MISSING ARGUMENTS'],
        'ArgumentParsingError': [418, 'IM A TEAPOT'],
        'TooManyArguments': [429, 'TOO MANY ARGUMENTS'],
        'DisabledCommand': [423,'LOCKED COMMAND'],
        'NotOwner': [401,'UNAUTHORIZED'],
        'ExtensionAlreadyLoaded': [500, "EXT[s] LOADED xd"],
        'ExtensionNotLoaded': [500,"EXT[s] UNLOADED xd"],
        "ExtensionError": [500, "CHECK FOR SYNTAX ERRORS"],
        "UnexpectedQuoteError": [417, "UNEXPECTED QUOTE"],
        "ExpectedClosingQuoteError": [417, "MISSING QUOTE"],
        "PrivateMessageOnly": [405, "IN DMs ONLY"],
        "NoPrivateMessage": [405, "IN SERVERS ONLY"],
        "UserInputError": [400, "INPUT ERROR"],
        "CommandOnCooldown": [400, "COMMAND COOLDOWN"],
        "MissingAnyRole": [401, "MISSING ROLE[S]"],
        "BotMissingAnyRole": [401, "BOT MISSING ROLE[S]"],
        "NSFWChannelRequired": [406, "NSFW CHANNEL ONLY"],
        "ExtensionNotFound": [404, "EXT[s] NOT FOUND xd"],
        "Forbidden": [403,'BOT FORBIDDEN'],
        "HTTPException": [409, 'HTTP ERROR'],
        "NotFound": [400, 'NOT FOUND'],
        "InvalidArgument": [406, 'INVALID ARG']
        }
    if st in errors: 
        await ctx.send(f'```diff\n-]ERROR {errors[st][0]}\n=]{errors[st][1]}``````md\n#] {errr}```')
        return
    await handler(ctx.bot, "COMMAND FAILURE", errr, ctx=ctx)

async def handler(bot, exception_type, exception, event=None, message=None, ctx = None, *args, **kwargs):
    if message is None and event is not None and hasattr(event, "message"): message = event.message
    if message is None and ctx is not None: message = ctx.message
    try:
        tb = f"""TYPE // {exception_type}
#>>>>>>>> ALL  INFO <<<<<<<<#
#//////// EXCEPTION ////////#
{str(exception)} [{type(exception)})]
-
#////////    ARG    ////////#"
{ctx.args}
-
#////////   KWARG   ////////#
{ctx.kwargs}
-
#/////// STACK TRACE ///////#
{"".join(traceback.format_tb(exception.__traceback__))}
-
#////////   NAMES   ////////#
{event}
-
#////////  COMMAND  ////////#
   NAME // {ctx.command.name}
CHANNEL // {'Private Message' if isinstance(ctx.channel, discord.abc.PrivateChannel) else f"{ctx.channel.name} [`{ctx.channel.id}`]"}
   USER // {str(ctx.author)} [`{ctx.author.id}`]
"""
        msgs = await log(bot, "GG MATE, SOMEBODY FUCKED IT ALL UP!",tb)
        await log(bot, "GG MATE, SOMEBODY FUCKED IT ALL UP!",f"""See the message 0.0
#////////  OG  MSG  ////////#
///>  {message.content}
///]  {message.channel}
""")
        await ctx.send(f"""```md
#] GG MATE, YOU FOUND A BUG!
> But that's okay, cuz you finding bugs
> is how I can get better at preventing
> that from happening... :D``````diff
-] {str(exception).replace('`','` ')}```""")
    except Exception as exc:
        msgs = await log(bot, "SOMETHING IS SERIOUSLY FUCKED UP", f"ERROR // {exc}")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+LIS')
    bot.add_listener(on_command_error)
    bot.add_listener(on_error)
    print('GOOD')

def teardown(bot):
    print('-LIS')
    bot.remove_listener('on_command_error')
    bot.remove_listener('on_error')
    print('GOOD')