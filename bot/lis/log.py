#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, io
import discord                    #python3.7 -m pip install -U discord.py
import logging
import traceback, json
from util import pages, getPre, dbman
from util.embedify import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix = getPre.getPre)

def rtn(gID: int, nam, mbr: discord.Member = None):
    allowbot = dbman.get('log', 'bot', id= gID, rtn = bool)
    isbot = False if mbr is None else mbr.bot
    if not allowbot and isbot:
        return False, None
    try:
        bot = dbman.get('log', 'bot', id = gID, rtn = bool)
        chn = dbman.get('oth', 'lCH', id = gID)
        if chn is None:
            return False, None
        log = dbman.get('log', nam, id = gID, rtn = bool)
        return chn and log, chn
    except Exception as ex:
        print(ex)
        return False, None

def lnk(msg):
    return f'https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}'

def clnk(chn):
    return f'https://discordapp.com/channels/{chn.guild.id}/{chn.id}'

def filer(thing):
    fl = io.BytesIO(json.dumps(thing, indent=4).encode("utf-8"))
    ds = discord.File(fl, 'prizm_logging.json')
    return ds

def grabperm(thing):
    allow = [perm for perm, val in thing.permissions if str(val) == "True"]
    deny = [perm for perm, val in thing.permissions if str(val) == "False"]
    inhr = [perm for perm, val in thing.permissions if str(val) == "None"]
    return allow, deny, inhr

global permstr
permstr = {"False": "Deny [X]", "True": "Allow [\u221a]", "None": "Inherit [/]"}

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen()
async def on_message_delete(msg):
    itm, chn = rtn(msg.guild.id,'del',msg.author)
    if not itm: return
    dic = {
        'AUTHOR': f'@{str(msg.author)} [<@{msg.author.id}>]',
        'CONTENT': msg.content,
        'CHANNEL': f'#{str(msg.channel)} [<#{msg.channel.id}>]',
        'ID': msg.id,
        'SENT AT': str(msg.created_at),
        'EDITED AT': str(msg.edited_at)
    }
    for emb in msg.embeds:
        dic[f'EMBED {msg.embeds.index(emb)}'] = emb.to_dict()
    for att in msg.attachments:
        dic[f'FILE {msg.attachments.index(att)}'] = {
            'ID': att.id,
            'SIZE': f'{att.size/1024}KiB',
            'NAME': att.filename
        }
    await msg.guild.get_channel(chn).send(embed=embedify(
            title = f'DELETED ;] - @{str(msg.author)} in #{str(msg.channel)}',
            desc = msg.content,
            time = 'now',
            foot = 'All info available in attached file'),
        file = filer(dic))

@bot.listen()
async def on_bulk_message_delete(msgs):
    itm, chn = rtn(msgs[0].guild.id, 'blk')
    if not itm: return
    dic = {'NOTE': 'Not all messages may appear here, especially if I restarted after they were sent.'}
    for msg in msgs:
        dic[msg.id] = {
            'AUTHOR': f'@{str(msg.author)} [<@{msg.author.id}>]',
            'CONTENT': msg.content,
            'CHANNEL': f'#{str(msg.channel)} [<#{msg.channel.id}>]',
            'ID': msg.id,
            'SENT AT': str(msg.created_at),
            'EDITED AT': str(msg.edited_at)
        }
        for emb in msg.embeds:
            dic[msg.id][f'EMBED {msg.embeds.index(emb)}'] = emb.to_dict()
        for att in msg.attachments:
            dic[msg.id][f'FILE {msg.attachments.index(att)}'] = {
                'ID': att.id,
                'SIZE': f'{att.size/1024}KiB',
                'NAME': att.filename
            }
    await msgs[0].guild.get_channel(chn).send(embed=embedify(
            title = 'BULK DELETION ;]',
            desc = f'''```md
#] MESSAGES DELETED ;]
>  {len(msgs)} messages in #{msgs[0].channel.name}
=] All info available in the attached file```''',
            time='now'),
        file = filer(dic))

@bot.listen()
async def on_message_edit(bfr,aft):
    itm, chn = rtn(bfr.guild.id,'edt',bfr.author)
    if not itm: return
    dic = {
        'AUTHOR': f'@{str(bfr.author)} [<@{bfr.author.id}>]',
        'BEFORE': {},
        'AFTER': {},
        'CHANNEL': f'#{str(bfr.channel)} [<#{bfr.channel.id}>]',
        'ID': bfr.id,
        'SENT AT': str(bfr.created_at),
        'EDITED AT': str(aft.edited_at)
    }
    for emb in bfr.embeds:
        dic['BEFORE'][f'EMBED {bfr.embeds.index(emb)}'] = emb.to_dict()
        del dic['BEFORE'][f'EMBED {bfr.embeds.index(emb)}']['timestamp']
    for emb in aft.embeds:
        dic['AFTER'][f'EMBED {aft.embeds.index(emb)}'] = emb.to_dict()
        del dic['AFTER'][f'EMBED {aft.embeds.index(emb)}']['timestamp']
    for att in aft.attachments: #Attachments cannot be changed
        dic[f'FILE {aft.attachments.index(att)}'] = {
            'ID': att.id,
            'SIZE': f'{att.size/1024}KiB',
            'NAME': att.filename
        }

    if dic['BEFORE'] == dic['AFTER'] and bfr.content == aft.content:
        return
    await bfr.guild.get_channel(chn).send(embed=embedify(
            title = 'MESSAGE EDIT ;]',
            desc = f'''```md
#] MESSAGE EDITED
>  {str(bfr.author)} in #{bfr.channel.name}```''',
            time='now',
            foot = 'All info available in attached file',
            fields=[[
                'BEFORE ---',
                bfr.content.ljust(2000, ' ')[:1024].strip() or '[EMPTY]',
                False
            ], [
                'AFTER ---',
                aft.content.ljust(2000, ' ')[:1024].strip() or '[EMPTY]',
                False
            ], [
                'LINK TO MSG ---',
                f'[[JUMP]]({lnk(bfr)})',
                False
            ]]),
        file = filer(dic))

@bot.listen()
async def on_guild_channel_delete(chnl):
    itm, chn = rtn(chnl.guild.id,'gc-')
    if not itm: return
    await chnl.guild.get_channel(chn).send(embed=embedify(
            title=f'DELETED CHANNEL ;[ - #{chnl.name}',
            desc="""```md
#] PROPERTIES
>     NAME ] {chnl.name}
> POSITION ] {chnl.position}
> OVERRIDE ] In attached file
> CATAGORY ] {str(chnl.category)}```""",
            time = 'now'),
        file = filer(dict(chnl.overwrites)))

@bot.listen()
async def on_guild_channel_create(chnl):
    try:
        await chnl.send('FIRST LOL ;]')
    except:
        pass
    itm, chn = rtn(chnl.guild.id,'gc+')
    if not itm: return
    await chnl.guild.get_channel(chn).send(embed=embedify(title='CREATED CHANNEL ;]',
            desc=f'```md\n#] CHANNEL CREATED - #{str(chnl)}```[[JUMP]]({clnk(chnl)})',
            time = 'now'))

@bot.listen()
async def on_guild_channel_update(bfr,aft):
    change = ''
    itm, chn = rtn(bfr.guild.id,'gc/')
    if not itm: return
    dic = {
        'BEFORE': {},
        'AFTER': {}
    }
    for rol in dict(bfr.overwrites):
        dic['BEFORE'][str(rol)] = {}
        for perm, val in dict(bfr.overwrites)[rol]:
            dic['BEFORE'][str(rol)][str(perm)] = permstr[str(val)]
    for rol in dict(aft.overwrites):
        dic['AFTER'][str(rol)] = {}
        for perm, val in dict(aft.overwrites)[rol]:
            dic['AFTER'][str(rol)][str(perm)] = permstr[str(val)]

    if bfr.name != aft.name:
        change += f'\nNAME ] {str(bfr)} --> {str(aft)}'

    if bfr.position != aft.position:
        change += f'\nPOS ] {bfr.position} --> {aft.position}'

    if bfr.category != aft.category:
        change += f'\nCATAGORY ] {str(bfr.category)} --> {str(aft.category)}'
    await bfr.guild.get_channel(chn).send(embed=embedify(title='CHANNEL EDIT ;]',
            desc = f'```md\n#] CHANNEL #{bfr.name} EDITED```',
            time = 'now',
            fields = [[
                'BEFORE ---',
                f'''```md
#] PROPERTIES
>     NAME ] {bfr.name}
> POSITION ] {bfr.position}
> OVERRIDE ] In attached file
> CATAGORY ] {str(bfr.category)}```''',
                False
            ], [
                'AFTER ---',
                f'''```md
#] PROPERTIES
>     NAME ] {aft.name}
> POSITION ] {aft.position}
> OVERRIDE ] In attached file
> CATAGORY ] {str(aft.category)}```''',
                False
            ], [
                'CHANGES ---',
                f'```{change or "OVERRIDE ] In attached file"}```',
                False
           ]]),
        file = filer(dic))


@bot.listen()
async def on_guild_channel_pins_update(chnl,lst):
    itm, chn = rtn(bfr.guild.id,'pin')
    if itm:
        await chnl.guild.get_channel(chn).send(embed=embedify(title='PINS UPDATE ;]',
                                               desc = f'```md\n#] PINS IN #{str(chnl)} WAS UPDATED```'))

@bot.listen()
async def on_guild_integrations_update(gld):pass

@bot.listen()
async def on_webhooks_update(chnl):pass

@bot.listen()
async def on_member_join(mbr):
    itm, chn = rtn(mbr.guild.id,'mb+')
    if itm:
        await mbr.guild.get_channel(chn).send(embed=embedify(title='MEMBER JOIN ;]',
                    desc=f'''```md\n#] @{str(mbr)} HAS JOINED THE GUILD
>  Use ';]mi {str(mbr)}' to view more```''',
                    thumb = str(mbr.avatar_url).replace('webp','png'),
                    time = 'now',
                    foot = f'MEMBERS ] {len(mbr.guild.members)}'))

@bot.listen()
async def on_member_remove(mbr):
    itm, chn = rtn(mbr.guild.id,'mb-')
    if itm:
        await mbr.guild.get_channel(chn).send(embed=embedify(title='MEMBER LEFT ;[',
                    desc=f'''```md\n#] @{str(mbr)} HAS LEFT THE GUILD
>  JOINED ] {mbr.joined_at}```''',
                    thumb = str(mbr.avatar_url).replace('webp','png'),
                    time = 'now',
                    foot = f'MEMBERS ] {len(mbr.guild.members)}'))

@bot.listen()
async def on_member_update(bfr,aft): pass


@bot.listen()
async def on_guild_update(bfr,aft): pass

@bot.listen()
async def on_guild_role_create(rol):
    itm, chn = rtn(rol.guild.id,'rl+')
    if itm:
        await rol.guild.get_channel(chn).send(embed=embedify(title='ROLE CREATED ;]',
            desc = f'```md\n#] ROLE &{rol.name} CREATED```',
            time='now'))

@bot.listen()
async def on_guild_role_delete(rol):
    itm, chn = rtn(rol.guild.id,'rl-')
    if itm:
        perm = []
        await rol.guild.get_channel(chn).send(embed=embedify(title=f'ROLE DELETED ;[ - &{rol.name}',
            desc = f'''```md
#] PROPERTIES
>       ID ] {rol.id}
>     NAME ] {rol.name}
>    COLOR ] {str(rol.color)}
>    HOIST ] {rol.hoist}
> POSITION ] {rol.position}
>  MANAGED ] {rol.managed}
> PINGABLE ] {rol.mentionable}``````diff
+] {perm for perm, val in rol.permissions if str(val) == "True"}
-] {perm for perm, val in rol.permissions if str(val) == "False"}
=] {perm for perm, val in rol.permissions if str(val) == "None"}
```''',
            time='now'))

@bot.listen()
async def on_guild_role_update(bfr,aft):
    itm, chn = rtn(bfr.guild.id,'rl/')
    if itm:
        change = ''
        if bfr.name != aft.name:
            change += '\nNAME ] `{bfr.name}` --> `{aft.name}`'
        if bfr.colour != aft.colour:
            change += f'\nCOLOR ] {str(bfr.colour)} --> {str(aft.colour)}'
        if bfr.hoist != aft.hoist:
            change += f'\nHOIST ] {aft.hoist}'
        if bfr.position != aft.position:
            change += f'\nPOS ] {bfr.position} --> {aft.position}'
        if bfr.managed != aft.managed:
            change += f'\nMANAGED ] {aft.managed}'
        if bfr.mentionable != aft.mentionable:
            change += f'\nPING ] {aft.mentionable}'
        if bfr.permissions != aft.permissions:
            aP, bP = grabperm(bfr), grabperm(aft)
            allow, deny, inherit = set(aP[0]) ^ set(bP[0]), set(aP[1]) ^ set(bP[1]), set(aP[2]) ^ set(bP[2])
            change += f'+] ALLOWED ] {", ".join(allow)}\n-]  DENIED ] {", ".join(deny)}\n=] INHERIT ] {", ".join(inherit)}'
        await bfr.guild.get_channel(chn).send(embed=embedify(title='ROLE EDIT ;]',
                    desc = f'```md\n#] ROLE &{bfr.name} EDITED```',
                    fields = [['BEFORE ---', f'''```md
#] PROPERTIES
>       ID ] {rol.id}
>     NAME ] {rol.name}
>    COLOR ] {str(rol.color)}
>    HOIST ] {rol.hoist}
> POSITION ] {rol.position}
>  MANAGED ] {rol.managed}
> PINGABLE ] {rol.mentionable}``````diff
+] {perm for perm, val in bfr.permissions if str(val) == "True"}
-] {perm for perm, val in bfr.permissions if str(val) == "False"}
=] {perm for perm, val in bfr.permissions if str(val) == "None"}
```''', False],
                              ['AFTER ---', f'''```md
#] PROPERTIES
>       ID ] {rol.id}
>     NAME ] {rol.name}
>    COLOR ] {str(rol.color)}
>    HOIST ] {rol.hoist}
> POSITION ] {rol.position}
>  MANAGED ] {rol.managed}
> PINGABLE ] {rol.mentionable}``````diff
+] {perm for perm, val in aft.permissions if str(val) == "True"}
-] {perm for perm, val in aft.permissions if str(val) == "False"}
=] {perm for perm, val in aft.permissions if str(val) == "None"}
```''', False],
                              ['CHANGES --',f'```diff\n{change}```',False]],
                    time = 'now'))


@bot.listen()
async def on_guild_emojis_update(*a): pass

@bot.listen()
async def on_voice_state_update(mbr, bfr, aft):
    itm, chn = rtn(mbr.guild.id, 'mVC')
    if itm:
        status = []
        bfrS = [vc for vc, val in [
            ('guild_deaf',bfr.deaf),
            ('guild_mute',bfr.mute),
            ('self_mute',bfr.self_mute),
            ('self_deaf',bfr.self_deaf),
            ('self_video',bfr.self_video),
            ('afk',bfr.afk)
        ] if val]

        aftS = [vc for vc, val in [
            ('guild_deaf',aft.deaf),
            ('guild_mute',aft.mute),
            ('self_mute',aft.self_mute),
            ('self_deaf',aft.self_deaf),
            ('self_video',aft.self_video),
            ('afk',aft.afk)
        ] if val]

        for st in bfrS:
            if st not in aftS:
                status.append(f'-] {st}')
        for st in aftS:
            if st not in bfrS:
                status.append(f'+] {st}')

        desc = f'```md\n#] MEMBER {str(mbr)} HAS'
        desc += "JOINED" if aft.channel else "LEFT"
        desc += f'{str(aft.channel) if aft.channel else str(bfr.channel)}```'

        await mbr.guild.get_channel(chn).send(
            embed = embedify(
                title = 'VOICE CHANGE ;]',
                fields = [
                    [
                        'BEFORE ---',
                        f'''```md
> CHANNEL ] {str(bfr.channel)}
>  STATUS ] {', '.join(bfrS)}```''',
                    False
                    ],
                    [
                        '`AFTER ----`',
                        f'''```md
> CHANNEL ] {str(aft.channel)}
>  STATUS ] {', '.join(aftS)}```''',
                    False
                    ],
                    [
                        '`CHANGES --`',
                        '```diff\n' + '\n'.join(status) + (
                            f'=] {str(bfr.channel)} --> {str(aft.channel)}' \
                                if bfr.channel != aft.channel else ''
                        ),
                        False
                    ]
                ],
                time = 'now'
            )
        )

@bot.listen()
async def on_member_ban(gld,usr):
    itm, chn = rtn(gld.id,'bn+')
    if itm:
        await gld.get_channel(ch).send(embed=embedify(title='MEMBER BANNED ;[',
            desc=f'```md\n#] MEMBER @{str(usr)} WAS BANNED FROM THE GUILD```',
            thumb = str(usr.avatar_url).replace('webp', 'png'),
            time = 'now'))

@bot.listen()
async def on_member_unban(gld,usr):
    itm, chn = rtn(gld.id,'bn-')
    if itm:
        await gld.get_channel(ch).send(embed=embedify(title='MEMBER UNBANNED ;]',
            desc=f'```md\n#] MEMBER @{str(usr)} WAS UNBANNED FROM THE GUILD```',
            thumb = str(usr.avatar_url).replace('webp','png'),
            time = 'now'))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    for com in [
            on_message_delete, on_message_edit, on_bulk_message_delete,
            on_guild_update, on_guild_channel_create, on_guild_channel_delete,
            on_guild_channel_update, on_guild_channel_pins_update,
            on_guild_integrations_update, on_webhooks_update,
            on_member_join, on_member_remove, on_member_update,
            on_guild_role_create,on_guild_role_delete, on_guild_role_update,
            on_guild_emojis_update, on_voice_state_update,
            on_member_ban, on_member_unban
    ]:
        print('+LIS [LOG]')
        bot.add_listener(com)
    print('GOOD')

def teardown(bot):
    for com in [
            'on_message_delete', 'on_message_edit', 'on_bulk_message_delete',
            'on_guild_channel_create', 'on_guild_channel_delete',
            'on_guild_channel_update', 'on_guild_channel_pins_update',
            'on_guild_integrations_update', 'on_webhooks_update',
            'on_member_join', 'on_member_remove', 'on_member_update',
            'on_guild_update', 'on_guild_role_create',
            'on_guild_role_delete', 'on_guild_role_update',
            'on_guild_emojis_update', 'on_voice_state_update',
            'on_member_ban', 'on_member_unban'
    ]:
        print('-LIS [LOG]')
        bot.add_listener(com)
        print('DONE')
    print('GOOD')
