import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
import datetime
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

def init():
    global _inst
    _inst = dict()
async def PageThis(ctx, lit, name, low="", thumb=None):
    bot = ctx.bot; num = 0; usr = ctx.author
    r = ['\u23EA','\u25C0','\u23F9','\u25B6','\u23E9', '\N{INPUT SYMBOL FOR NUMBERS}','\u267b']

    def emb(text, thumb=None, foot=None):
        return embedify.embedify(title="!] PRIZ AI ;] [!", desc=text, color=0x00ffff, thumb=thumb, foot=foot)

    def check(reaction, user):
        try: return user == _inst[reaction.message.id]['usr']
        except: pass
    if len(_inst) > 1:
        if [list(foo.values()) for foo in _inst.values()][0].count(ctx.author) >= 5:
            return await ctx.send('''```md
#] TOO MANY INSTANCES
> You already have 5 commands open
> Please close one to continue
> This helps prevent spam :D''')

    msg = await ctx.send(embed=emb(f'''```md
#] !] PRIZ AI ;] [! {name}``````md
{lit[num]}```{low}''', foot=f"[{num+1}/{len(lit)}]", thumb=thumb))
    if len(lit) > 1:
        _inst[msg.id]={
            'msg':msg,
            'lit':lit,
            'num':num,
            'usr':usr,
            'end':low,
            'nam':name,
            'img':thumb
            }
        print(len(_inst))
        for rct in r: await msg.add_reaction(rct)
        while True:
            try: reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                delet = []
                for tmsg in list(_inst)[:]:
                    imsg = await ctx.fetch_message(tmsg)
                    if imsg.edited_at is None: tm = imsg.created_at.timestamp()
                    else: tm = imsg.edited_at.timestamp()
                    if float(datetime.datetime.utcnow().timestamp()-tm-21600) > 59:
                        delet.append(tmsg); await imsg.clear_reactions(); break
                for m in delet: del _inst[m]
            else:
                if reaction.message.id in _inst:
                    msg, lit, num, usr, low, name, thumb = _inst[reaction.message.id].values()
                    s = str(reaction.emoji)
                    if s == r[0]: num = 0
                    elif s == r[1]: num = num - 1
                    elif s == r[2]:
                        del _inst[reaction.message.id]
                        return await msg.clear_reactions()
                    elif s == r[6]:
                        del _inst[reaction.message.id]
                        return await msg.delete()
                    elif s == r[3]: num = num+1
                    elif s == r[4]: num = len(lit) - 1
                    elif s == r[5]:
                        ms = await ctx.send('```md\n#]ENTER PAGE NUMBER```')
                        def chk(ms1): return ms1.author==user
                        try: ms1 = await bot.wait_for('message', timeout=10.0, check=chk)
                        except asyncio.TimeoutError:
                            await ms.delete()
                            await ctx.send('```diff\n-]TIMEOUT [10s]```', delete_after=3.0)
                        else:
                            await ms.delete()
                            await ms1.delete()
                            try:
                                num = int(ms1.content)-1
                                if num < 0: num = 0
                                elif num > (len(lit) - 1): num = len(lit) - 1
                            except: await ctx.send('```diff\n-]INVALID RESPONSE```', delete_after=3.0)
                    await msg.remove_reaction(reaction, usr)
                    if num < 0: num = len(lit) - 1
                    elif num > (len(lit) - 1): num = 0
                    await msg.edit(embed=emb(f'''```md
#] !] PRIZ AI ;] [! {name}``````md
{lit[num]}```{low}''', foot=f"[{num+1}/{len(lit)}]", thumb=thumb))
                    _inst[msg.id]={
                        'msg':msg,
                        'lit':lit,
                        'num':num,
                        'usr':usr,
                        'end':low,
                        'nam':name,
                        'img':thumb
                        }