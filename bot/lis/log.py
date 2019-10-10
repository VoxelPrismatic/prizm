#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback, json
from util import pages, getPre, dbman
from util.embedify import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)

def rtn(gID, nam, mbr:discord.Member=None):
    itm = dbman.get('log','bot',id=int(gID), rtn = bool)
    if not mbr:
        bt = False
    else:
        bt = mbr.bot
    lBOT = True
    if not itm and bt:
        lBOT = False
    try:
        return dbman.get('log','bot',id=int(gID), rtn=bool) and dbman.get('oth','lCH',id=int(gID),rtn=int) \
               and lBOT, dbman.get('oth','lCH',id=int(gID),rtn=int)
    except Exception as ex:
        print(ex)
        return False, None

def lnk(msg):
    return f'https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}'

def clnk(chn):
    return f'https://discordapp.com/channels/{chn.guild.id}/{chn.id}'

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def on_message_delete(msg):
    itm, chn = rtn(msg.guild.id,'del',msg.author)
    if itm:
        dic = {}
        for emb in msg.embeds:
            dic[f'EMBED {msg.embeds.index(emb)}'] = emb.to_dict()
        atts = '\n'.join([f'[[ATT {msg.attachments.index(att)}]]({str(att.url).replace("cdn.discordapp.com","media.discordapp.net")})' for att in msg.attachments])
        open('json/logging.json','w+').write(json.dumps(dic,indent=4))
        await msg.guild.get_channel(chn).send(embed=embedify(
            title='DELETED ;]',
            desc=f'''```md
#] MESSAGE DELETED
>  {str(msg.author)} IN #{msg.channel.name}```{msg.content}''',
            time='now',
            fields = [['```ATTACHMENTS ---```',atts if atts else '[NONE]', False]]),
        file = discord.File(fp=open('json/logging.json','rb')) if len(dic) else None)
        open('json/logging.json','w+').write('{}')

@bot.listen()
async def on_bulk_message_delete(msgs):
    itm, chn = rtn(msgs[0].guild.id,'blk')
    if itm:
        dic = {}
        for msg in msgs:
            dic[msg.id] = {'CONTENT':msg.content,'AUTHOR':str(msg.author)}
            for emb in msg.embeds:
                dic[msg.id][f'EMBED {msg.embeds.index(emb)}'] = emb.to_dict()
            for att in msg.attachments:
                dic[msg.id][f'ATTACHMENT {msg.attachments.index(att)}'] = str(att.url).replace("cdn.discordapp.com","media.discordapp.net")
        open('json/logging.json','w+').write(json.dumps(dic,indent=4))
        await msgs[0].guild.get_channel(chn).send(embed=embedify(
            title='BULK DELETION ;]',
            desc=f'''```md
#] MESSAGES DELETED
>  {len(msgs)} MESSAGES IN #{msgs[0].channel.name}
=] CONTENT IN ATTACHED FILE```''',
            time='now'),
        file = discord.File(fp=open('json/logging.json','rb')))
        open('json/logging.json','w+').write('{}')

@bot.listen()
async def on_message_edit(bfr,aft):
    if bfr.author.bot: return
    itm, chn = rtn(bfr.guild.id,'edt',bfr.author)
    if itm:
        dic = {'BEFORE':{'EMBED 0': "DOESNT EXIST"},'AFTER':{'EMBED 0': "DOESNT EXIST"}}
        has_emb = False

        for emb in bfr.embeds:
            dic['BEFORE'][f'EMBED {bfr.embeds.index(emb)}'] = emb.to_dict()
            has_emb = True
            del dic['BEFORE'][f'EMBED {bfr.embeds.index(emb)}']['timestamp']
        for emb in aft.embeds:
            dic['AFTER'][f'EMBED {aft.embeds.index(emb)}'] = emb.to_dict()
            has_emb = True
            del dic['AFTER'][f'EMBED {aft.embeds.index(emb)}']['timestamp']

        open('json/logging.json','w+').write(json.dumps(dic,indent=4))
        if dic['BEFORE'] == dic['AFTER'] and bfr.content == aft.content:
            return
        await bfr.guild.get_channel(chn).send(embed=embedify(
            title='MESSAGE EDIT ;]',
            desc=f'''```md
#] MESSAGE EDITED
>  {str(bfr.author)} IN #{bfr.channel.name}```''',
            time='now',
            fields=[['```BEFORE --------```',
                     bfr.content if len(bfr.content) else '[IS EMBED]',
                     False],
                    ['```AFTER ---------```',
                     aft.content if len(aft.content) else '[IS EMBED]',
                     False],
                    ['```LINK TO MSG ---```',
                    f'[[JUMP]]({lnk(bfr)})',
                    False]]),
        file = discord.File(fp=open('json/logging.json','rb')) if has_emb else None)
        open('json/logging.json','w+').write('{}')

@bot.listen()
async def on_guild_channel_delete(chnl):
    itm, chn = rtn(chnl.guild.id,'gc-')
    if itm:
        open('json/logging.json','w').write(json.dumps(dict(chnl.overwrites),indent=4))
        await chnl.guild.get_channel(chn).send(embed=embedify(title='DELETED CHANNEL ;[',
            desc=f'```md\n#] CHANNEL DELETED - {str(chnl)}```',
            fields = [['`CHANNEL ---`',f'''```md
#] PROPERTIES
>     NAME // {chnl.name}
> POSITION // {chnl.position}
> OVERRIDE // In attached file
> CATAGORY // {str(chnl.category)}```''',False]],
            time = 'now'),
        file=discord.File(fp=open('json/logging.json','rb')))
        open('json/logging.json','w+').write('{}')

@bot.listen()
async def on_guild_channel_create(chnl):
    try:
        await chnl.send('FIRST LOL ;]')
    except:
        pass
    itm, chn = rtn(chnl.guild.id,'gc+')
    if itm:
        await chnl.guild.get_channel(chn).send(embed=embedify(title='CREATED CHANNEL ;]',
            desc=f'```md\n#] CHANNEL CREATED - {str(chnl)}```[[JUMP]]({clnk(chnl)})',
            time = 'now'))

@bot.listen()
async def on_guild_channel_update(bfr,aft):
    change = ''
    itm, chn = rtn(bfr.guild.id,'gc/')
    if itm:
        dic = {'BEFORE':{},'AFTER':{}}
        for rol in dict(bfr.overwrites):
            dic['BEFORE'][str(rol)] = {}
            for perm, val in dict(bfr.overwrites)[rol]:
                dic['BEFORE'][str(rol)][perm] = f'{str(val)} - [{"-" if str(val)=="False" else "+" if str(val)=="True" else "/"}]'
        for rol in dict(aft.overwrites):
            dic['AFTER'][str(rol)] = {}
            for perm, val in dict(aft.overwrites)[rol]:
                dic['AFTER'][str(rol)][perm] = f'{str(val)} - [{"-" if str(val)=="False" else "+" if str(val)=="True" else "/"}]'
        print(json.dumps(dic,indent=4))
        print(open('json/logging.json','w').write(json.dumps(dic,indent=4)))

        if bfr.name != aft.name:
            change += f'\nNAME // {str(bfr)} --> {str(aft)}'
        if bfr.position != aft.position:
            change += f'\nPOS // {bfr.position} --> {aft.position}'
        if bfr.changed_roles != aft.changed_roles:
            chng = []
            for perm in aft.changed_roles:
                if perm not in bfrP: chng.append(f'\n>   ADDED ] {perm}')
            for perm in bfr.changed_roles:
                if perm not in aftP: chng.append(f'\n> REMOVED ] {perm}')
            change += '\nOVERRIDES EDITED'+''.join(chng)
        if bfr.category != aft.category:
            change += f'\nCATAGORY // {str(bfr.category)} --> {str(aft.category)}'
        await bfr.guild.get_channel(chn).send(embed=embedify(title='CHANNEL EDIT ;]',
                    desc = f'```md\n#] CHANNEL {bfr.name} EDITED```',
                    fields = [['`BEFORE ---`',f'''```md
#] PROPERTIES
>     NAME // {bfr.name}
> POSITION // {bfr.position}
> OVERRIDE // In attached file
> CATAGORY // {str(bfr.category)}```''', False],
                              ['`AFTER ----`',f'''```md
#] PROPERTIES
>     NAME // {aft.name}
> POSITION // {aft.position}
> OVERRIDE // In attached file
> CATAGORY // {str(aft.category)}```''', False],
                              ['`CHANGES --`',f'```{change if len(change) else "[PERMISSIONS IN FILE]"}```',False]],
                    time = 'now'),
        file = discord.File(fp=open('json/logging.json','rb')))
        open('json/logging.json','w+').write('{}')


@bot.listen()
async def on_guild_channel_pins_update(chnl,lst): pass

@bot.listen()
async def on_guild_integrations_update(gld):pass

@bot.listen()
async def on_webhooks_update(chnl):pass

@bot.listen()
async def on_member_join(mbr):
    itm, chn = rtn(mbr.guild.id,'mb+')
    if itm:
        await mbr.guild.get_channel(chn).send(embed=embedify(title='MEMBER JOIN ;]',
                    desc=f'''```md\n#] {str(mbr)} HAS JOINED THE GUILD
>  Use ';]mbr {str(mbr)}' to view more```''',
                    thumb = str(mbr.avatar_url).replace('webp','png'),
                    time = 'now',
                    foot = f'MEMBERS // {len(mbr.guild.members)}'))

@bot.listen()
async def on_member_remove(mbr):
    itm, chn = rtn(mbr.guild.id,'mb-')
    if itm:
        await mbr.guild.get_channel(chn).send(embed=embedify(title='MEMBER LEFT ;[',
                    desc=f'''```md\n#] {str(mbr)} HAS LEFT THE GUILD
>  JOINED // {mbr.joined_at}```''',
                    thumb = str(mbr.avatar_url).replace('webp','png'),
                    time = 'now',
                    foot = f'MEMBERS // {len(mbr.guild.members)}'))

@bot.listen()
async def on_member_update(bfr,aft): pass

@bot.listen()
async def on_guild_update(bfr,aft): pass

@bot.listen()
async def on_guild_role_create(rol):
    itm, chn = rtn(rol.guild.id,'rl+')
    if itm:
        await rol.guild.get_channel(chn).send(embed=embedify(title='ROLE CREATED ;]',
            desc = f'```md\n#] ROLE @{rol.name} CREATED```',
            time='now'))

@bot.listen()
async def on_guild_role_delete(rol):
    itm, chn = rtn(rol.guild.id,'rl-')
    if itm:
        perm = []
        await rol.guild.get_channel(chn).send(embed=embedify(title='ROLE DELETED ;[',
            desc = f'```md\n#] ROLE @{rol.name} DELETED```',
            fields = [['`ROLE ---`',f'''```md
#] PROPERTIES
>       ID // {rol.id}
>     NAME // {rol.name}
>    PERMS // {', '.join(perm for perm, val in rol.permissions if val)}
>    COLOR // {str(rol.color)}
>    HOIST // {rol.hoist}
> POSITION // {rol.position}
>  MANAGED // {rol.managed}
> PINGABLE // {rol.mentionable}```''', False]],
            time='now'))

@bot.listen()
async def on_guild_role_update(bfr,aft):
    itm, chn = rtn(bfr.guild.id,'rl/')
    if itm:
        change = ''
        if bfr.name != aft.name:
            change += '\nNAME // `{bfr.name}` --> `{aft.name}`'
        if bfr.permissions != aft.permissions:
            chng = []
            bfrP = [perm for perm, val in bfr.permissions if val]
            aftP = [perm for perm, val in aft.permissions if val]
            for perm in aftP:
                if perm not in bfrP:
                    chng.append(f'\n>   ADDED ] {perm}')
            for perm in bfrP:
                if perm not in aftP:
                    chng.append(f'\n> REMOVED ] {perm}')
            change += '\nPERMS EDITED'+''.join(chng)
        if bfr.colour != aft.colour:
            change += f'\nCOLOR // {str(bfr.colour)} --> {str(aft.colour)}'
        if bfr.hoist != aft.hoist:
            change += f'\nHOIST // {aft.hoist}'
        if bfr.position != aft.position:
            change += f'\nPOS // {bfr.position} --> {aft.position}'
        if bfr.managed != aft.managed:
            change += f'\nMANAGED // {aft.managed}'
        if bfr.mentionable != aft.mentionable:
            change += f'\nPING // {aft.mentionable}'
        await bfr.guild.get_channel(chn).send(embed=embedify(title='ROLE EDIT ;]',
                    desc = f'```md\n#] ROLE {bfr.name} EDITED```',
                    fields = [['`BEFORE ---`',f'''```md
#] PROPERTIES
>       ID // {bfr.id}
>     NAME // {bfr.name}
>    PERMS // {', '.join(perm for perm, val in bfr.permissions if val)}
>    COLOR // {str(bfr.color)}
>    HOIST // {bfr.hoist}
> POSITION // {bfr.position}
>  MANAGED // {bfr.managed}
> PINGABLE // {bfr.mentionable}```''', False],
                              ['`AFTER ----`',f'''```md
#] PROPERTIES
>       ID // {aft.id}
>     NAME // {aft.name}
>    PERMS // {', '.join(perm for perm, val in aft.permissions if val)}
>    COLOR // {str(aft.color)}
>    HOIST // {aft.hoist}
> POSITION // {aft.position}
>  MANAGED // {aft.managed}
> PINGABLE // {aft.mentionable}```''', False],
                              ['`CHANGES --`',f'```{change}```',False]],
                    time = 'now'))


@bot.listen()
async def on_guild_emojis_update(gld): pass

@bot.listen()
async def on_voice_state_update(mbr,bfr,aft):
    itm, chn = rtn(mbr.guild.id,'mVC')
    if itm:
        status = []
        bfrS = [vc for vc, val in [('guild_deaf',bfr.deaf),
                                   ('guild_mute',bfr.mute),
                                   ('self_mute',bfr.self_mute),
                                   ('self_deaf',bfr.self_deaf),
                                   ('self_video',bfr.self_video),
                                   ('afk',bfr.afk)] if val]

        aftS = [vc for vc, val in [('guild_deaf',aft.deaf),
                                   ('guild_mute',aft.mute),
                                   ('self_mute',aft.self_mute),
                                   ('self_deaf',aft.self_deaf),
                                   ('self_video',aft.self_video),
                                   ('afk',aft.afk)] if val]
        for st in bfrS:
            if st not in aftS:
                status.append(f'-] {st}')
        for st in aftS:
            if st not in bfrS:
                status.append(f'+] {st}')

        await mbr.guild.get_channel(chn).send(embed=embedify(title='VOICE CHANGE ;]',
            desc = f'''```md\n#] MEMBER {str(mbr)} HAS {"JOINED" if aft.channel else "LEFT"} {str(aft.channel) if aft.channel else str(bfr.channel)}```''',
            fields = [['`BEFORE ---`',f'''```md
> CHANNEL // {str(bfr.channel)}
>  STATUS // {', '.join(bfrS)}```''',False],
                      ['`AFTER ----`',f'''```md
> CHANNEL // {str(aft.channel)}
>  STATUS // {', '.join(aftS)}```''',False],
                      ['`CHANGES --`',
                       '```diff\n'+'\n'.join(status)+(f'=] {str(bfr.channel)} --> {str(aft.channel)}' if bfr.channel != aft.channel else '')+'```',
                      False]],
            time = 'now'))

@bot.listen()
async def on_member_ban(gld,usr):
    itm, chn = rtn(gld.id,'bn+')
    if itm:
        await gld.get_channel(ch).send(embed=embedify(title='MEMBER BANNED ;[',
            desc=f'```md\n#] MEMBER {str(usr)} WAS BANNED FROM THE GUILD```',
            thumb = str(usr.avatar_url).replace('webp','png'),
            time = 'now'))


@bot.listen()
async def on_member_unban(gld,usr):
    itm, chn = rtn(gld.id,'bn-')
    if itm:
        await gld.get_channel(ch).send(embed=embedify(title='MEMBER UNBANNED ;]',
            desc=f'```md\n#] MEMBER {str(usr)} WAS UNBANNED FROM THE GUILD```',
            thumb = str(usr.avatar_url).replace('webp','png'),
            time = 'now'))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    for com in [on_message_delete,
                on_message_edit, on_bulk_message_delete, on_guild_update,
                on_guild_channel_create, on_guild_channel_delete,
                on_guild_channel_update, on_guild_channel_pins_update,
                on_guild_integrations_update, on_webhooks_update,
                on_member_join, on_member_remove, on_member_update,
                on_guild_role_create,on_guild_role_delete, on_guild_role_update,
                on_guild_emojis_update, on_voice_state_update,
                on_member_ban, on_member_unban]:
        print('+LIS [LOG]')
        bot.add_listener(com)
    print('GOOD')

def teardown(bot):
    for com in ['on_message_delete',
                'on_message_edit', 'on_bulk_message_delete',
                'on_guild_channel_create', 'on_guild_channel_delete',
                'on_guild_channel_update', 'on_guild_channel_pins_update',
                'on_guild_integrations_update', 'on_webhooks_update',
                'on_member_join', 'on_member_remove', 'on_member_update',
                'on_guild_update', 'on_guild_role_create',
                'on_guild_role_delete', 'on_guild_role_update',
                'on_guild_emojis_update', 'on_voice_state_update',
                'on_member_ban', 'on_member_unban']:
        print('-LIS [LOG]')
        bot.add_listener(com)
        print('DONE')
    print('GOOD')
