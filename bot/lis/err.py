#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback, sys
import json
from util import embedify, getPre
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify.embedify(desc=f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

##///---------------------///##
##///     BOT  EVENTS     ///##
##///---------------------///##

@bot.listen()
async def on_error(event, *args, **kwargs):
    t, exception, info = sys.exc_info()
    await handler(bot, "EVENT FAILED", exception, event, None, None, *args, **kwargs)
    await ctx.send('```diff\n-] AN ERROR OCCURED```')

@bot.listen()
async def on_command_error(ctx, error):
    """
    >>> ERROR HANDLER <<<
    Only for discord errors, not syntax, out of bounds, etc
    """
    if isinstance(error, commands.CommandNotFound):
        return await ctx.invoke(ctx.bot.get_command('text'), convo=ctx.message.content[2:])
    try:
        if ctx.guild and not json.load(open('json/servers.json'))[str(ctx.guild.id)]["com"][ctx.command.name]:
            return await ctx.send('```diff\n-] ERROR\n=] THIS COMMAND ISNT ENABLED```')
    except:
        pass
    try:
        errr = error.original
    except:
        errr = error
    st = str(type(errr)).split('.')[-1][:-2]
    found = False
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
              'NotOwner': [403,'FORBIDDEN'],
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
              "NotFound": [404, 'NOT FOUND'],
              "InvalidArgument": [406, 'INVALID ARG'],
              "ClientException": [400, 'CLIENT ERROR']}
    if st in errors:
        await ctx.send(f'```diff\n-] ERROR {errors[st][0]} {errors[st][1]}``````md\n#] {errr}```')
        found = True
    await handler(ctx.bot, "COMMAND FAILURE", errr, ctx=ctx, found=found)

async def handler(bot, exception_type, exception, event=None, message=None, ctx = None, found=False,*args, **kwargs):
    if message is None and event is not None and hasattr(event, "message"):
        message = event.message
    if message is None and ctx is not None:
        message = ctx.message
    try:
        tb = "".join(traceback.format_tb(exception.__traceback__)).replace('`',' `')
        open('txt/tb','w+').write(tb)
        await bot.get_channel(569698278271090728).send(embed=embedify.embedify(title='AN ERROR OCCURED ;[',
                                                      desc = '```md\n#] SEE BELOW FOR DETAILS```',
                                                      fields = [['`EXCEPTION ---`',
                                                                 f"```diff\n-] {type(exception)} '{str(exception)}'```",
                                                                 False],
                                                                ['`ARGS --------`',
                                                                 '```'+str(ctx.args)+'```',
                                                                 False],
                                                                ['`KWARGS ------`',
                                                                 '```'+json.dumps(ctx.kwargs,indent=4)+'```',
                                                                 False],
                                                                ['`EVENT INFO --`',
                                                                 '```'+str(event)+'```',
                                                                 False],
                                                                ['`COMMAND -----`',
                                                                 f"""```NAME // {ctx.command.name}
CHANNEL // {'Private Message' if isinstance(ctx.channel, discord.abc.PrivateChannel) else f"{ctx.channel.name} [`{ctx.channel.id}`]"}
   USER // {str(ctx.author)} [`{ctx.author.id}`]```""",
                                                                 False],
                                                                ['`MESSAGE -----`',
                                                                 '```'+message.content+'```',
                                                                 False],
                                                                ['`TRACEBACK ---`',
'```'+(tb if len(tb) <= 1024 else 'IN ATTACHED FILE')+'```',
                                                                 False]]
                                                        ),
                                    file = discord.File(fp=open('txt/tb','rb')) if len(tb) > 1024 else None
                            )
        if not found:
            await ctx.send(f"""```md
#] GG MATE, YOU FOUND A BUG!
> But that's okay, cuz you finding bugs
> is how I can get better at preventing
> that from happening... :D``````diff
-] {str(exception).replace('`',' `')}```""")
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