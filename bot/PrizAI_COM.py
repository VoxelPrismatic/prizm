#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os
import ast
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import numpy as np                #python3.7 -m pip install -U numpy
import numexpr as ne              #python3.7 -m pip install -U numexpr
import datetime, time
import aiofiles, io, asyncio      #python3.7 -m pip install -U aiofiles
import matplotlib.pyplot as pyplt #python3.7 -m pip install -U matplotlib // SEE SITE FOR MORE
import matplotlib, math, statistics, random
import platform, sys, sysconfig, traceback, shlex
from shlex import quote
from ast import literal_eval
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
bot = commands.Bot(command_prefix=";]")
bot.remove_command("help")
logging.basicConfig(level='INFO')

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
async def log(bot, head, text):
    chnl = bot.get_channel(569698278271090728)
    msgs = await chnl.send(embed=embedify(f'''```md\n#] {head}!\n> {text}```'''))
    return msgs

async def com(bot, command):
    msgs = await log(bot, "COMMAND USED", f'COMMAND // {command}')
    print(f']{command}')
    return msgs
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

class own(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log(self.bot, "It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

    @commands.command(aliases=["helpown"])
    async def hlepown(self, ctx):
        result = 0
        def check(reaction, user): return user == ctx.author
        lit = ["""
] ";]hlepown"
> Brings up this message :)
] ";]clrin0"
> An override for ";]clrin"
] ";]clr0"
> An override for ";]clr"
] ";]calc"
> A calculator
] ";]exe"
> Executables""",
                """] ";]pwr"
> Shuts down
] ";]rld"
> Reloads extensions
] ";]ld"
> Loads extensions
] ";]uld"
> Unloads extensions""",
                """] ";]pin0"
> An override for ";]pin"
] ";]unpin0"
> An override for ";]unpin" """]
        msg = await ctx.send(embed=embedify(f'''```diff
+] !] PRIZ AI ;] [! OWNER STUFF``````md
{lit[result]}``````diff
+] To see commands, use ";]hlep"
+] To have a conversation, use "]<your text here>""
+] Some of your data is stored, use ";]data" to see more
```'''))
        await msg.add_reaction('⏪')
        await msg.add_reaction('◀')
        await msg.add_reaction('⏹')
        await msg.add_reaction('▶')
        await msg.add_reaction('⏩')
        while True:
            try: reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError: return await msg.clear_reactions()
            else:
                if str(reaction.emoji) == '⏪':
                    result = 0
                    await msg.remove_reaction('⏪', ctx.author)
                elif str(reaction.emoji) == '◀':
                    await msg.remove_reaction('◀', ctx.author)
                    result = result - 1
                    if result < 0: result = 0
                elif str(reaction.emoji) == '⏹':
                    return await msg.clear_reactions()
                elif str(reaction.emoji) == '▶':
                    await msg.remove_reaction('▶', ctx.author)
                    result = result+1
                    if result > (len(lit) - 1): result = len(lit) - 1
                elif str(reaction.emoji) == '⏩':
                    result = len(lit) - 1
                    await msg.remove_reaction('⏩', ctx.author)
                await msg.edit(embed=embedify(f'''```diff
+] !] PRIZ AI ;] [! OWNER STUFF``````md
{lit[result]}``````diff
+] To see commands, use ";]hlep"
+] To have a conversation, use "]<your text here>""
+] Some of your data is stored, use ";]data" to see more
```'''))
        await com(self.bot, "OWN HELP")

    @commands.command()
    @commands.is_owner()
    async def exe(self, ctx, *, code): await ctx.send(f'{exec(code)}')

    @commands.command()
    @commands.is_owner()
    async def clrin0(self, ctx, int1: int, Int2: int):
        try:
            await ctx.channel.purge(limit=1)
            clrh = await ctx.fetch_message(min(int1, int2))
            clrl = await ctx.fetch_message(max(int1, int2))
            await ctx.channel.purge(limit=2000, before=clrl, after=clrh)
            await com(self.bot, f'CLEARED INBETWEEN {int1}&{int2}')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @commands.is_owner()
    async def calc(self, ctx, *, eq):
        try:
            msg = await ctx.send('`]CALCULATING`')
            eq = eq.strip().replace('^', '**').replace('x', '*')
            await ctx.send(embed=embedify(f'{eval(eq)}'))
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)
        await com(self.bot, f'CALC {eq}')

    @commands.command()
    @commands.is_owner()
    async def clr0(self, ctx, arg: int):
        try:
            await ctx.channel.purge(limit=arg+1)
            await com(self.bot, f'CLEAR [{arg}]')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @commands.is_owner()
    async def pin0(self, ctx, mID: int):
        try:
            message = await ctx.fetch_message(mID)
            await message.pin()
            await com(self.bot, 'PINNED')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @commands.is_owner()
    async def unpin0(self, ctx, mID: int):
        try:
            message = await ctx.fetch_message(mID)
            await message.unpin()
            await ctx.send('`]UNPINNED`')
            await com(self.bot, 'UNPINNED')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

class mod(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log(self.bot, "It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clr(self, ctx, arg: int):
        try:
            await ctx.channel.purge(limit=arg+1)
            await com(self.bot, f'CLEAR [{arg}]')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @has_permissions(manage_roles=True, ban_members=True)
    async def ban(self, ctx, members: commands.Greedy[discord.Member],
                  delete_days: typing.Optional[int] = 0, *,
                  reason: str):
        for member in members:
            await com(self.bot, f'BANNED [{member}]')
            try: await member.ban
            except discord.HTTPException: await exc(ctx, 1)
            except discord.Forbidden: await exc(ctx, 2)
            except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @has_permissions(manage_roles=True, kick_members=True)
    async def kick(self, ctx, *members: discord.Member):
        await ctx.channel.purge(limit=1)
        for member in members:
            await com(self.bot, f'KICKED [{member}]')
            try: await kick(member, reason=f"REQUESTED BY {ctx.author}")
            except discord.HTTPException: await exc(ctx, 1)
            except discord.Forbidden: await exc(ctx, 2)
            except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clrin(self, ctx, int1: int, int2: int):
        try:
            await ctx.channel.purge(limit=1)
            clrh = await ctx.fetch_message(min(int1, int2))
            clrl = await ctx.fetch_message(max(int1, int2))
            await ctx.channel.purge(limit=2000, before=clrl, after=clrh)
            await com(self.bot, f'CLEARED INBETWEEN {int1}&{int2}')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, mID: int):
        try:
            message = await ctx.fetch_message(mID)
            await message.pin()
            await com(self.bot, 'PINNED')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, mID: int):
        try:
            message = await ctx.fetch_message(mID)
            await message.unpin()
            await ctx.send('`]UNPINNED`')
            await com(self.bot, 'UNPINNED')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

class public(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log(self.bot, "It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

    @commands.command()
    async def graph(self, ctx, eq, xmin: int, xmax: int):
        msg = await ctx.send('`]GRAPHING`')
        await com(self.bot, f'GRAPH {eq} -X[{xmin}] +X[{xmax}]')
        try:
            x = np.array(range(xmin, xmax))
            y = ne.evaluate(eq.replace("^", "**"))
            fig = pyplt.figure()
            fig, ax = pyplt.subplots()
            ax.set_facecolor('#002823')
            ax.tick_params(labelcolor='#0000ff')
            pyplt.plot(x, y)
            fig.patch.set_facecolor('#002823')
            plotimg = io.BytesIO()
            pyplt.savefig(plotimg, format='png')
            plotimg.seek(0)
            await msg.delete()
            await ctx.send(file=discord.File(plotimg, 'img.png'))
            pyplt.close()
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def cool(self, ctx, user: int):
        strtemp = '////////'
        await com(self.bot, 'DELAYED RICK')
        await ctx.channel.purge(limit = 1)
        coolthing = await ctx.send(strtemp)
        varslol = True
        rickroll = f'''
Never gonna give <@{user}> up!
Never gonna let <@{user}> down!
Never gonna run around, and, desert you!
Never gonna make <@{user}> cry!
Never gonna say goodbye!
Never gonna run around, and, desert you!
'''
        while varslol == True:
            try:
                for x in range(125):
                    strtemp = f'{strtemp}////////'
                    await coolthing.edit(content = f'{strtemp}')
                varslol = False
                await ctx.send(rickroll)
            except:
                if varslol == False: await coolthing.edit(rickroll)
                else:
                    await ctx.send('YOU WILL NOT END THIS!')
                    strtemp = '////////'
                    coolthing = await ctx.send(strtemp)

    @commands.command()
    async def react(self, ctx, mID: int, *reactions):
        await ctx.channel.purge(limit = 1)
        await com(self.bot, f"REACTIONS [{reactions}] TO mID[{mID}]")
        message = await ctx.fetch_message(mID)
        for reaction in reactions:
            try: await message.add_reaction(reaction)
            except discord.HTTPException: await exc(ctx, 1)
            except discord.Forbidden: await exc(ctx, 2)
            except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def stats(self, ctx, *data: int):
        try: mod = str(statistics.mode(data))
        except: mod = "[NONE]"
        await ctx.send(embed=embedify(f'''```md
#] STATS
>   MAX // {max(data)}
>   MIN // {min(data)}
>   AVG // {statistics.mean(data)}
>   MOD // {mod}
>   MED // {statistics.median(data)}
> RANGE // {max(data)-min(data)}
> STDEV // {statistics.stdev(data)}
> LOMED // {statistics.median_low(data)}
> HIMED // {statistics.median_high(data)}
```'''))
        await com(self.bot, f'STATS {data}')

    @commands.command()
    async def blkjck(self, ctx):
        try:
            heart = ['🂱','🂲','🂳','🂴','🂵','🂶','🂷','🂸','🂹','🂺','🂻','🂽','🂾']
            spade = ['🂡','🂢','🂣','🂤','🂥','🂦','🂧','🂨','🂩','🂪','🂫','🂭','🂮']
            diam = ['🃁','🃂','🃃','🃄','🃅','🃆','🃇','🃈','🃉','🃊','🃋','🃍','🃎']
            club = ['🃑','🃒','🃓','🃔','🃕','🃖','🃗','🃘','🃙','🃚','🃛','🃝','🃞']
            ttl1 = ttl2 = temp = stu = 0
            usr = cpu = cputxt = usrtxt = ""
            while ttl1 <= 18:
                temp = rand(0,12)
                if temp + ttl1 + 1 != 21:
                    stu = rand(0,3)
                    if stu == 1: usr = usr+heart.pop[temp]+' '
                    elif stu == 2: usr = usr+spade.pop[temp]+' '
                    elif stu == 3: usr = usr+diam.pop[temp]+' '
                    elif stu == 3: usr = usr+club.pop[temp]+' '
                    temp += 1
                    if temp > 10: temp = 10
                    ttl1 += temp
            while ttl2 <= 18:
                temp = rand(0,12)
                if temp + ttl2 + 1 != 21:
                    if stu == 1: cpu = cpu+heart.pop[temp]+' '
                    elif stu == 2: cpu = cpu+spade.pop[temp]+' '
                    elif stu == 3: cpu = cpu+diam.pop[temp]+' '
                    elif stu == 3: cpu = cpu+club.pop[temp]+' '
                    temp += 1
                    if temp > 10: temp = 10
                    ttl2 += temp
            if ttl1 > 21: usrtxt = f'USER // {usr} [{ttl1}] [BUST]'
            elif ttl1 > ttl2: usrtxt = f'USER // {usr} [{ttl1}] [WIN]'
            elif ttl1 < ttl2: usrtxt = f'USER // {usr} [{ttl1}] [LOSS]'
            if ttl2 > 21: cputxt = f'COMP // {cpu} [{ttl2}] [BUST]'
            elif ttl2 > ttl1: cputxt = f'COMP // {cpu} [{ttl2}] [WIN]'
            elif ttl2 < ttl1: cputxt = f'COMP // {cpu} [{ttl2}] [LOSS]'
            if ttl1 == ttl2:
                usrtxt = f'USER // {usr} [{ttl1}] [TIE]'
                cputxt = f'COMP // {cpu} [{ttl2}] [TIE]'
            await ctx.send(f'```md\n#]BLACK JACK!\n \n{usrtxt}\n \n{cputxt}```')
            await com(self.bot, 'BJ')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def spam(self, ctx, num: int):
        if num > 10000: num = 10000
        send = ""
        data = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcsdefghgijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+[]{}\"\'<,>./?\\|`~"
        for x in range(num):
            send = send+(data[rand(0,len(data)-1)])
            if len(send) == 2000:
                await ctx.send(send)
                send = ""
        if len(send) > 0: await ctx.send(send)
        await com(self.bot, 'SPAM')

    @commands.command()
    async def rto(self, ctx, int1: int, int2: int):
        factor = math.gcd(int1, int2)
        await ctx.send(f'```]FACT // {factor}\n]INT1 // {int1/factor}\n]INT2 // {int2/factor}```')
        await com(self.bot, 'RTOLO')

    @commands.command()
    async def snd(self, ctx, cID: int, mCTX):
        await ctx.channel.purge(limit=1)
        try:
            chnl = self.bot.get_channel(cID)
            await chnl.send(content=mCTX)
        except:
            await ctx.send('```diff\n-]WOOPS\n=]Make sure i have access to that channel uwu```')

    @commands.command()
    async def echo(self, ctx, mCTX):
        await ctx.channel.purge(limit=1)
        await ctx.send(content=mCTX)

    @commands.command()
    async def rad(self, ctx, D: int):
        K = 1
        for I in range(1,500):
            for J in range(2,1000):
                if not math.remainder(D, J**2):
                    D = D/(J**2); K = K*J
            if D == 1: break
        if D == 1: await ctx.send(f'```]ANS // {K}```')
        elif K == 1: await ctx.send(f'```]ANS // √{D}```')
        else: await ctx.send(f'```]ANS // {K}√{D}```')
        await com(self.bot, 'RADRED')

    @commands.command()
    async def usrinfo(self, ctx):
        try:
            perms = '|'.join(perm for perm, value in ctx.author.guild_permissions if value)
            await ctx.send(embed=embedify(f'''```
    USER // {ctx.author.name}
    NICK // {ctx.author.display_name}
  JOINED // {ctx.author.joined_at}
 CREATED // {ctx.author.created_at}
 DISCRIM // {ctx.author.discriminator}
   PERMS // {perms}
  STATUS // {ctx.author.status}
USER PFP // {ctx.author.avatar_url}```'''))
            await com(self.bot, 'USRINFO')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def quad(self, ctx, A: int, B: int, C: int):
        D = B**2 - 4*A*C; K = 1
        for I in range(1,500):
            for J in range(2,1000):
                if not math.remainder(D, J**2):
                    D = D/(J**2); K = K*J
            if D == 1:break
        if D == 1: STR = f'{K}'
        elif K == 1: STR = f'√{D}'
        else: STR = f'{K}√{D}'
        await ctx.send(embed=embedify(f'''```md
#]QUADRATICS``````
{-B}+-{STR}
------------
{2*A}``````diff
+] [{-B/(2*A)} + {K/(2*A)}√{D}] {(-B+((B**2)-2*A*C)**.5)/(2*A)}
-] [{-B/(2*A)} - {K/(2*A)}√{D}] {(-B-((B**2)-2*A*C)**.5)/(2*A)}```'''))
        await com(self.bot, 'QUAD FORM')

    @commands.command()
    async def dnd(self, ctx):
        await com(self.bot, ']DND')
        try: await ctx.send(embed=embedify(f"```md\n# DND!\nD4 ~ {rand(1,4)}\nD6 ~ {rand(1,6)}\nD8 ~ {rand(1,8)}\nD10 ~ {rand(1,10)}\nD12 ~ {rand(1,12)}\nD20 ~ {rand(1,20)}\n```"))
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def rick(self, ctx):
        await com(self.bot, 'RICKROLLD')
        await ctx.send(embed=embedify('''Never gonna give you up!
Never gonna let you down!
Never gonna run around and, desert you!
Never gonna make you cry!
Never gonna say goodbye!
Never gonna run around and, desert you!'''))

    @commands.command()
    async def binary(self, ctx, *, st):
        try:
            sr = st.replace(' ', '')
            await ctx.send(embed=embedify(f'{"".join([chr(int(sr[i:i+8], 2)) for i in range(0, len(sr), 8)])}'))
        except ValueError:
            await ctx.send(embed=embedify(f'{"".join((bin(ord(x))[2:].zfill(8) for x in st))}'))
        await com(self.bot, "BINARY <> ASCII")

    @commands.command()
    async def coin(ctx, *nums: int):
        try:
            if len(nums) == 0: num = 1
            else: num = int(nums[0])
            tcnt = y = hcnt = 0
            outp = ""
            if num > 5000:
                await ctx.send('```]To prevent spam, MAX = 5000```')
                num = 5000
            await com(self.bot, "COIN FLIP")
            for x in range(num):
                if rand(0,1) == 1:
                    tcnt+=1; outp = outp+"[T] "
                else:
                    hcnt+=1; outp = outp+"[H] "
                if y == 497:
                    await ctx.send(f'```{outp}```')
                    outp = ""; y = 0
                else: y+=1
            if y != 0: await ctx.send(f'```{outp}```')
            await ctx.send(f'```]HEAD // {hcnt}\n]TAIL // {tcnt}```')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def rng(self, ctx, rngl: int, rngh: int, *nums: int):
        try:
            if len(nums) == 0: num = 1
            else: num = int(nums[0])
            if num > 2000:
                await ctx.send('```]To prevent spam, MAX = 2000```')
                num = 2000
            send = ""; temp = 0; ttl = []
            await ctx.send(f'```diff\n-] RNG BETWEEN {rngl} & {rngh}```')
            await com(self.bot, f'RNG BETWEEN {rngl} & {rngh}')
            for x in range(num):
                temp = random.randint(rngl,rngh)
                if len(f'{send} {temp} ')<=1994:
                    send += f'{temp} '; ttl.append(temp)
                else:
                    await ctx.send(f'```{send}```')
                    send = f'{temp} '; ttl.append(temp)
            if len(send) != 0: await ctx.send(f'```{send}```')
            await ctx.send(f'```COUNT // {len(ttl)}\nAVRGE // {sum(ttl)/len(ttl)}\nRANGE // {max(ttl)-min(ttl)}```')
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def slots(self, ctx):
        try:
            slot = ["[X]","[Y]","[Z]","[1]","[2]",
                    "[3]","[0]","[V]","[U]","[@]",
                    "[%]","[#]","[P]","[+]","[/]",
                    "[*]","[>]","[<]","[;]","[!]",
                    "[]]","[?]","[+]","[[]","[*]"]
            slot1 = rand(0,len(slot)-1)
            slot2 = rand(0,len(slot)-1)
            slot3 = rand(0,len(slot)-1)
            slotsend = f'''
-] {slot[slot1-1]}{slot[slot2-1]}{slot[slot3-1]}
+]>{slot[slot1]}{slot[slot2]}{slot[slot3]}<
-] {slot[slot1+1]}{slot[slot2+1]}{slot[slot3+1]}'''
            if slot1 == slot2 or slot1 == slot3 or slot2 == slot3:
                await ctx.send(embed=embedify(f'```diff\n-{slotsend}\n \n-] WIN!```'))
            else:
                await ctx.send(embed=embedify(f'```diff\n{slotsend}\n \n-] LOST```'))
            await com(self.bot, "SLOTS")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

class info(commands.Cog):
    def __init__(self, bot): self.bot = bot
    async def cog_command_error(self, ctx, error):
        await log(self.bot, "It fucked up :C", f'ERROR // {error}\n> TRACE // {sys.exc_info()}')
        await ctx.send(embed=embedify('GG, It fucked up. [Hopefully] all data was logged'))

    @commands.command(aliases=["help"])
    async def hlep(self, ctx):
        result = 0
        def check(reaction, user): return user == ctx.author
        lit = ["""
] ";]hlep"
> Brings up this message :)
] ";]sys"
> Shows some sys info :P
] ";]ping"
> Shows the ping time :L
] ";]slots"
> Slot machine :D
] ";]coin {x}" [Option: {x}]
> Flips a virtual coin {x} times 0.0""",
                """] ";]git"
> Shows the github/gitlab repo ;]
] ";]rng {x} {y} {z}" [Option: {z}]
> Prints an RNG from {x} to {y}, {z} times
] ";]usrinfo"
> Shows your user info 0.0
] ";]dnd"
> Roles all dice from Dragons and Dungeons!
] ";]info"
> Shows additional info""",
                """] ";]cool {uID}"
> Gives someone [{userID}] a sneaky surpise ;D
] ";]rick"
> Rick Roll! °ω°
] ";]blkjck"
> BLACKJACK! 0o0
] ";]spam {x}"
> Spams {x} amount of chars >.<
] ";]graph {eq} {xmin} {xmax}"
> Graphs {eq} from {xmin} to {xmax} 9.6""",
                """] ";]rto {x} {y}"
> Reduces the ratio of {x} and {y} ;-;
] ";]rad {x}"
> Reduces a radical, {x}! >:D
] ";]react {mID} {reactions}" [{reaction}.split " "]
> Adds {reactions} to a given {mID} .-.
] ";]stats {data}"
> Gives stats given {data} ._.
] ";]quad {a} {b} {c}"
> Uses {a}, {b}, and {c} to solve the Quad Formula 0o0"""]
        msg = await ctx.send(embed=embedify(f'''```md
#] !] PRIZ AI ;] [! COMMANDS LIST``````md
{lit[result]}``````md
#] To see mod commands, use ";]hlepmod"
#] To have a conversation, use "]<your text here>""
#] Some of your data is stored, use ";]data" to see more
```'''))
        await msg.add_reaction('⏪')
        await msg.add_reaction('◀')
        await msg.add_reaction('⏹')
        await msg.add_reaction('▶')
        await msg.add_reaction('⏩')
        while True:
            try: reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError: return await msg.clear_reactions()
            else:
                if str(reaction.emoji) == '⏪':
                    result = 0
                    await msg.remove_reaction('⏪', ctx.author)
                elif str(reaction.emoji) == '◀':
                    await msg.remove_reaction('◀', ctx.author)
                    result = result - 1
                    if result < 0: result = 0
                elif str(reaction.emoji) == '⏹':
                    return await msg.clear_reactions()
                elif str(reaction.emoji) == '▶':
                    await msg.remove_reaction('▶', ctx.author)
                    result = result+1
                    if result > (len(lit) - 1): result = len(lit) - 1
                elif str(reaction.emoji) == '⏩':
                    result = len(lit) - 1
                    await msg.remove_reaction('⏩', ctx.author)
                await msg.edit(embed=embedify(f'''```md
#] !] PRIZ AI ;] [! COMMANDS LIST``````md
{lit[result]}``````md
#] To see mod commands, use ";]hlepmod"
#] To have a conversation, use "]<your text here>"
#] Some of your data is stored, use ";]data" to see more
```'''))
        await com(self.bot, "HELP")

    @commands.command(aliases=["helpmod"])
    async def hlepmod(self, ctx):
        result = 0
        def check(reaction, user): return user == ctx.author
        lit = ["""
] ";]hlepmod"
> Brings up this message :)
] ";]ban {user} {delete days} {reason}"
> Bans a {user} and removes messages from {delete days} ago for a {reason}
] ";]kick {user}"
> Kicks a {user} from the server
] ";]clr {int}"
> Deletes a {int} amount of messages
] ";]clrin {messageID1} {messageID2}"
> Deletes messages between {messageID1} and {messageID2}""",
                """] ";]pin {mID}"
> Pins {mID}
] ";]unpin {mID}"
> Unpins {mID}"""]
        msg = await ctx.send(embed=embedify(f'''```diff
-] !] PRIZ AI ;] [! MOD STUFF``````md
{lit[result]}``````diff
-] To see mod commands, use ";]hlepmod"
-] To have a conversation, use "]<your text here>""
-] Some of your data is stored, use ";]data" to see more
```'''))
        await msg.add_reaction('⏪')
        await msg.add_reaction('◀')
        await msg.add_reaction('⏹')
        await msg.add_reaction('▶')
        await msg.add_reaction('⏩')
        while True:
            try: reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError: return await msg.clear_reactions()
            else:
                if str(reaction.emoji) == '⏪':
                    result = 0
                    await msg.remove_reaction('⏪', ctx.author)
                elif str(reaction.emoji) == '◀':
                    await msg.remove_reaction('◀', ctx.author)
                    result = result - 1
                    if result < 0: result = 0
                elif str(reaction.emoji) == '⏹':
                    return await msg.clear_reactions()
                elif str(reaction.emoji) == '▶':
                    await msg.remove_reaction('▶', ctx.author)
                    result = result+1
                    if result > (len(lit) - 1): result = len(lit) - 1
                elif str(reaction.emoji) == '⏩':
                    result = len(lit) - 1
                    await msg.remove_reaction('⏩', ctx.author)
                await msg.edit(embed=embedify(f'''```diff
-] !] PRIZ AI ;] [! MOD STUFF``````md
{lit[result]}``````diff
-] To see mod commands, use ";]hlepmod"
-] To have a conversation, use "]<your text here>""
-] Some of your data is stored, use ";]data" to see more
```'''))
        await com(self.bot, "MOD HELP")

    @commands.command()
    async def data(self, ctx):
        await ctx.send(embed=embedify('''```md
#] HOW YOUR DATA IS USED
Data is only stored when talking to the bot directly,
using "]{message}" or using commands
This data is stored forever on the owner's computer
This data only stores your message content, and nothing
more.
If you do not feel comfortable with this, dont talk to
this bot, or just dont say bad things.
#] TL;DR // Only messages are stored when using "]{msg}"
#] and when you use commands```'''))
        await com(self.bot, 'DATA USAGE')

    @commands.command()
    async def info(self, ctx):
        try:
            await ctx.send(embed=embedify('''```md
#] PRIZ AI
> An RNG based AI that compares strings... literally
> Originally written for the TI84+CSE and adapted into a way better Discord Bot!
> This is version [0]-RW, a rewritten version```'''))
            await com(self.bot, "BOT INFO")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def ping(self, ctx):
        try:
            await ctx.send(embed=embedify(f'```md\n#] !] PONG ;] [!\n> Ping Time: {bot.latency}s```'))
            await com(self.bot, "PING TIME")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command()
    async def git(self, ctx):
        try:
            await ctx.send('''`]GITHUB PAGE` https://github.com/VoxelPrismatic/basic-ai/
    `]GITLAB PAGE` https://gitlab.com/VoxelPrismatic/basic-ai/''')
            await com(self.bot, "GITHUB/GITLAB")
        except discord.HTTPException: await exc(ctx, 1)
        except discord.Forbidden: await exc(ctx, 2)
        except discord.NotFound: await exc(ctx, 3)

    @commands.command(aliases=["system"])
    async def os(self, ctx):
        platform = str(sysconfig.get_platform())
        pyver = str(sysconfig.get_python_version())
        await ctx.send(embed=embedify(f'''```diff
+] !] PRIZ AI ;] [! SYSTEM INFO``````md
  PLATFORM // {platform}
    PYTHON // {pyver}
DISCORD.PY // {discord.__version__}
   LOGGING // {logging.__version__}
  AIOFILES // {aiofiles.__version__}
MATPLOTLIB // {matplotlib.__version__}
     NUMPY // {np.__version__}
   NUMEXPR // {ne.__version__}
```'''))
        await com(self.bot, "SYS INFO")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('LOADING COGS')
    bot.add_cog(mod(bot))
    bot.add_cog(own(bot))
    bot.add_cog(public(bot))
    bot.add_cog(info(bot))
    print('COGS LOADED')

def teardown(bot):
    print('UNLOADING COGS')
    bot.remove_cog('mod')
    bot.remove_cog('own')
    bot.remove_cog('public')
    bot.remove_cog('info')
    print('COGS UNLOADED')
