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
async def PageThis(ctx, lit, name, low="", thumb=None, mono = True,typ = 'md'):
    """
    >>> MAIN PAGINATOR FOR MOST COMMANDS <<<
      CTX - [CTX ] Context, allows this paginator to grab the author, channel, and other things
      LIT - [LIST] Pages in the form of a list, easy paging
      LOW - [STR ] Footer, on every page, none by default
      TYP - [STR ] Sets the monospace syntax highlighting, MarkDown by default
     NAME - [STR ] Title text
     MONO - [STR ] Sets the input text to monospace, on by default
    THUMB - [STR ] Link to thumbnail to an **IMAGE** [only http[s] supported], None by default
    """
    bot = ctx.bot
    num = 0
    usr = ctx.author

    def emb(text, thumb=None, foot=None):
        "EMBED MAKER"
        return embedify.embedify(title="PRIZM ;]",
                                 desc=text,
                                 color=0x00ffff,
                                 thumb=thumb,
                                 foot=foot)

    def check(reaction, user):
        """
        CHECKS IF THE REACTION AUTHOR IS THE SAME AS THE PERSON WHO
        INVOKED THE COMMAND
        """
        try: return user == _inst[reaction.message.id]['usr']
        except: pass

    def save(msg,lit,num,usr,low,name,thumb,mono,typ):
        """
        >>> SAVES THE CONTENTS TO A DICT <<<
      CTX - [CTX ] Context, allows this paginator to grab the author, channel, and other things
      LIT - [LIST] Pages in the form of a list, easy paging
      LOW - [STR ] Footer, on every page, none by default
      TYP - [STR ] Sets the monospace syntax highlighting, MarkDown by default
      NUM - [INT ] The location
     NAME - [STR ] Title text
     MONO - [STR ] Sets the input text to monospace, on by default
    THUMB - [STR ] Link to thumbnail to an **IMAGE** [only http[s] supported], None by default
        """
        _inst[msg.id]={'msg':msg,  #Message Instance
                       'lit':lit,  #Pages in list
                       'num':num,  #Page Number
                       'usr':usr,  #Author Instance
                       'end':low,  #Footer
                       'nam':name, #Header
                       'img':thumb,#Thumbnail
                       'mono':mono,#Is Monospace?
                       'typ':typ}  #Monospace Syntax Highlighting
    #to get these emojis please let your bot join https://discord.gg/eYMyfcd
    r = ['<:sl:598301530667483137>',   #Skip Left
         '<:al:598301447066484747>',   #Arrow Left
         '<:stp:598301603069689876>',  #Stop
         '<:ar:598301483645141003>',   #Arrow Right
         '<:sr:598301570387542036>',   #Skip Right
         '<:num:598301671642234919>',  #Numbers
         '<:del:598301635718152241>']  #Recycle
    async def react(msg):
        "ADDS REACTIONS"
        for rct in r:await msg.add_reaction(rct)
        return msg

    def page(mID):
        """
        >>> CREATES A PAGE <<<
        mID - [INT] The message ID
        """
        itm = _inst[mID]
        return f"```md\n#] PRIZM {itm['nam']} ;]```"+('```'+itm['typ']+'\n' if itm['mono'] else '')+itm['lit'][itm['num']]+('```' if itm['mono'] else '\n')+itm['end']

    if [list(foo.values())[3] for foo in _inst.values()].count(ctx.author) > 2:return await ctx.send('''```md
#] TOO MANY INSTANCES
> You already have 3 commands open
> Please close one to continue
> This helps prevent spam :D```''')

    if len(lit) == 1:
        return await ctx.send(embed=emb(f"```md\n#] PRIZM {name} ;]```"+('```'+typ+'\n' if mono else '')+lit[num]+('```' if mono else '\n')+low,
                                        foot=f"[1/{len(lit)}] // PRIZM ;]",
                                        thumb=thumb))

    msg = await react(await ctx.send(embed=embedify.embedify(title='LOADING ;]',
                                                             desc='```md\n#] STARTING... PLEASE WAIT```')))

    await msg.edit(embed=emb(f"```md\n#] PRIZM {name} ;]```"+('```'+typ+'\n' if mono else '')+lit[num]+('```' if mono else '\n')+low,
                         foot=f"[1/{len(lit)}] // PRIZM ;]",
                         thumb=thumb))

    if len(lit) > 1 and msg.id not in _inst:
        save(msg,lit,num,usr,low,name,thumb,mono,typ)
        while len(_inst) > 0:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                delet = []
                for tmsg in list(_inst)[:]:
                    imsg=_inst[tmsg]["msg"]
                    if imsg.edited_at is None:
                        tm = imsg.created_at.timestamp()
                    else:
                        tm = imsg.edited_at.timestamp()
                    if float(datetime.datetime.utcnow().timestamp()-tm) > 59:
                        delet.append(tmsg)
                        await imsg.edit(embed=emb(page(imsg.id),foot=f"[{num+1}/{len(lit)}] // TIMEOUT", thumb=thumb))
                        await imsg.clear_reactions()
                for m in delet: del _inst[m]
            else:
                if reaction.message.id in _inst:
                    msg, lit, num, usr, low, name, thumb, mono, typ = _inst[reaction.message.id].values()
                    e = reaction.emoji
                    s = f'<:{e.name}:{e.id}>'

                    if s == r[0]: #Skip Left
                        num = 0

                    elif s == r[1]: #Arrow Left
                        num -= 1

                    elif s == r[2]: #Stop
                        await msg.edit(embed=emb(page(msg.id),foot=f"[{num+1}/{len(lit)}] // STOPPED", thumb=thumb))
                        try:
                            await msg.clear_reactions()
                        except:
                            pass
                        try:
                            del _inst[reaction.message.id]
                        except:
                            pass

                    elif s == r[6]: #Recycle
                        del _inst[reaction.message.id]
                        return await msg.delete()

                    elif s == r[3]: #Arrow Right
                        num += 1

                    elif s == r[4]: #Skip Right
                        num = len(lit) - 1

                    elif s == r[5]: #Numbers
                        ms = await ctx.send('```md\n#]ENTER PAGE NUMBER```')
                        def chk(ms1):
                            return ms1.author==user
                        try:
                            ms1 = await bot.wait_for('message', timeout=10.0, check=chk)
                        except asyncio.TimeoutError:
                            await ms.delete()
                            await ctx.send('```diff\n-]TIMEOUT [10s]```', delete_after=3.0)
                        else:
                            try:
                                await ms.delete(); await ms1.delete()
                            except:
                                pass
                            try:
                                num = int(ms1.content)-1
                            except:
                                await ctx.send('```diff\n-] INVALID RESPONSE```', delete_after=3.0)

                    if num < 0:
                        num = len(lit) - 1

                    elif num > (len(lit) - 1):
                        num = 0

                    try:
                        await msg.remove_reaction(reaction, usr)
                    except:
                        pass

                    save(msg,lit,num,usr,low,name,thumb,mono,typ)

                    await msg.edit(embed=emb(page(msg.id),
                                             foot=f'[{num+1}/{len(lit)}] // '+('PLEASE RE-REACT' if type(msg.channel)==discord.DMChannel else 'PRIZM ;]'),
                                             thumb=thumb))