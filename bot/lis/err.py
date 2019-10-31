#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, aiofiles
import discord                    #python3.7 -m pip install -U discord.py
import logging, json, re
import traceback, sys
from util.priz_err import *
from util import embedify, getPre, dbman
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def escape(st):
    for regex in [r"(\_)", r"(\*)", r"(\~)", r"(\#)", 
                  r"(\@)", r"(\|)", r"(\`)", r"(\.)", r"(\:)"]:
        st = re.sub(regex, r" \1", str(st.encode("utf-8"))[2:-1])
    return st

async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify.embedify(desc=f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

##///---------------------///##
##///     BOT  EVENTS     ///##
##///---------------------///##

@bot.listen()
async def on_error(event, *args, **kwargs):
    print(event, *args, kwargs)

@bot.listen()
async def on_command_error(ctx, error):
    """
    >>> ERROR HANDLER <<<
    Only for discord errors, not syntax, out of bounds, etc
    """
    if isinstance(error, commands.CommandNotFound):
        return await ctx.invoke(ctx.bot.get_command('text'), convo=ctx.message.content[2:])
    try:
        if ctx.guild and not dbman.get('com', ctx.command.name, id=ctx.guild.id):
            return await ctx.send('```diff\n-] THIS COMMAND ISNT ENABLED```')
    except:
        pass
    try:
        errr = error.original
    except:
        errr = error
    if issubclass(type(errr), PrizmError):
        await handler(ctx.bot, "COMMAND FAILURE", errr, ctx=ctx, found=True)
        return await ctx.send(f"""```md
#] PRIZM {errr.typ} ;[
=] Something wrong happened internally
>  More info about the issue can be found below
``````{errr.syntax}
{errr.message}```""")
    st = str(type(errr)).split('.')[-1][:-2]
    found = False
    typ, obj, tb = sys.exc_info()
    errors = {
        'DiscordException': "Unknown",
        'LoginFailue': 'Verification',
        'NoMoreItems': 'Iter',
        'Forbidden': 'Forbidden',
        'NotFound': 'NotFound',
        'InvalidData': 'Invalid',
        'InvalidArgument': 'InvalidArg',
        'GatewayNotFound': 'Gateway',
        'ConnectionClosed': 'Connection',
        'OpusError': 'Opus',
        'Opus': 'Opus',
        'CommandError': 'Com',
        'ConversionError': 'Conversion',
        'MissingRequiredArgument': 'MissingArgs',
        'ArgumentParsingError': 'Parse',
        'UnexpectedQuoteError': 'BadQuotes',
        'InvalidEndOfQuoteStringError': 'BadQuotes',
        'ExpectedClosingQuoteError': 'MissingQuotes',
        'BadArgument': 'BadArgs',
        'BadUnionArgument': 'BadArgs',
        'PrivateMessageOnly': 'DMsOnly',
        'NoPrivateMessage': 'GuildOnly',
        'CheckFailure': 'Checks',
        'CommandNotFound': 'WtfHowDidWeGetHere', #This shouldn't ever happen
        'DisabledCommand': 'Disabled',
        'CommandInvokeError': 'Invoke',
        'TooManyArguments': 'TooManyArgs',
        'UserInputError': 'Input',
        'CommandOnCooldown': 'Cooldown',
        'NotOwner': 'Forbidden',
        'MissingPermissions': 'MissingPerms',
        'BotMissingPermissions': 'PrizmPerms',
        'MissingRole': 'MissingRole',
        'BotMissingRole': 'PrizmRole',
        'MissingAnyRole': 'MissingRole',
        'BotMissingAnyRole': 'PrizmRole',
        'NSFWChannelRequired': 'Nsfw',
        'ExtensionError': 'Ext',
        'ExtensionAlreadyLoaded': 'ExtLoaded',
        'ExtensionNotLoaded': 'ExtUnloaded',
        'NoEntryPointError': 'Entry',
        'ExtensionFailed': 'ExtFailed',
        'ExtensionNotFound': 'ExtNotFound'
    }
    if st in errors:
        await ctx.send(f'''```md
#] PRIZM {errors[st]}Error ;[
=] This is most likely an issue with what you did
>  More info about the issue can be found below
``````diff
-] {errr}```''')
        found = True
    await handler(ctx.bot, "COMMAND FAILURE", errr, ctx=ctx, found=found)

async def handler(bot, ex_type, ex, event=None, message=None, ctx = None, found=False):
    if message is None and event is not None and hasattr(event, "message"):
        message = event.message
    if message is None and ctx is not None:
        message = ctx.message
    try:
        tb = "".join(traceback.format_tb(ex.__traceback__)).replace('`','\u200b`')
        async with aiofiles.open("txt/tb.txt", "w+") as tbfile:
            await tbfile.write(tb)
        await bot.get_channel(569698278271090728).send(
            embed=embedify.embedify(title='AN ERROR OCCURED ;[',
                desc = '```md\n#] SEE BELOW FOR DETAILS```',
                fields = [['`EXCEPTION ---`',
                            f"```diff\n-] {type(ex)} '{str(ex)}'```",
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
                            f"""```;]{ctx.command.name} in #{'Private Message' if isinstance(ctx.channel, discord.abc.PrivateChannel) else f"{ctx.channel.name} [`{ctx.channel.id}`]"} by {str(ctx.author)} [`{ctx.author.id}`]```""",
                            False],
                        ['`MESSAGE -----`',
                            '```'+message.content+'```',
                            False],
                        ['`TRACEBACK ---`',
    '```'+(tb if len(tb) <= 1024 else 'IN ATTACHED FILE')+'```',
                            False]]
                ),
            file = discord.File('txt/tb.txt') if len(tb) > 1024 else None
        )
        if not found:
            await ctx.send(f"""```md
#] PRIZM {str(type(ex)).split("'")[1]} ;[
=] You found a bug, thank you ;]
>  More info about the issue can be found below
``````diff
-] {escape(str(ex))}
=] Traceback is available in the attached file
```""", file=discord.File("txt/tb.txt"))
    except Exception as ex:
        msgs = await log(bot, "SOMETHING IS SERIOUSLY FUCKED UP", f"ERROR // {ex}")

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
