#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
bot = commands.Bot(command_prefix=";]")

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)
async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
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
    if isinstance(error, commands.BadArgument):
        await ctx.send('```diff\n-]ERROR 400\n=]BAD ARGUMENT```')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.add_reaction('🇫')
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send('```diff\n-]ERROR 503\n=]BOT FORBIDDEN```')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('```diff\n-]ERROR 403\n=]USER FORBIDDEN```')
    elif isinstance(error, commands.ConversionError):
        await ctx.send('```diff\n-]ERROR 503\n=]UNAVAILABLE```')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('```diff\n-]ERROR 416\n=]MISSING ARGS```')
    elif isinstance(error, commands.ArgumentParsingError):
        await ctx.send('```diff\n-]ERROR 418\n=]IM A TEAPOT```')
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send('```diff\n-]ERROR 429\n=]TOO MANY ARGS```')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send('```diff\n-]ERROR 423\n=]LOCKED COMMAND```')
    elif isinstance(error, commands.NotOwner):
        await ctx.send('```diff\n-]ERROR 401\n=]UNAUTHORIZED```')
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send('```diff\n-]ERROR 500\n=]The extensions are already loaded xd```')
    elif isinstance(error, commands.ExtensionNotLoaded):
        await ctx.send('```diff\n-]ERROR 500\n=]The extensions are already unloaded xd```')
    elif isinstance(error, commands.ExtensionError):
        await ctx.send('```diff\n-]ERROR 500\n=]An error occured, check for syntax errors```')
    else:
        await handler(ctx.bot, "COMMAND FAILURE", error.original, ctx=ctx)
        await ctx.send("""```md
#] GG MATE, YOU FUCKED IT UP
> But that's okay, cuz you breaking shit
> is how I can get better at preventing
> that from happening... :D```""")

async def handler(bot, exception_type, exception, event=None, message=None, ctx = None, *args, **kwargs):
    if message is None and event is not None and hasattr(event, "message"): message = event.message
    if message is None and ctx is not None: message = ctx.message
    try:
        msgs = await log(bot, "GG MATE, SOMEBODY FUCKED IT ALL UP!",f"""TYPE // {exception_type}
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
""")
        await log(bot, "GG MATE, SOMEBODY FUCKED IT ALL UP!",f"""See the message 0.0
#////////  OG  MSG  ////////#
///>  {message.content}  <///
///]  {message.channel}  [///
""")
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

