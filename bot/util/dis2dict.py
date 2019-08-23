import discord

def Message(msg:discord.Message):return {'TTS':msg.tts,
                                         'TYPE':str(msg.type),
                                         'AUTHOR':str(msg.author),
                                         'CONTENT':msg.content,
                                         'EMBEDS':Embeds(msg.embeds),
                                         'CHANNEL':str(msg.channel),
                                         'CALL':CallMessage(msg.call),
                                         'MENTION EVERYONE':msg.mention_everyone,
                                         'USER MENTIONS':abcUsers(msg.mentions),
                                         'CHANNEL MENTIONS'}

def Embed(emb:discord.Embed): return emb.to_dict()

    
def CallMessage(cll:discord.CallMessage): return {'ENDED':str(cll.ended_timestamp),
                                                  'PEOPLE':Users(cll.participants),
                                                  'ENDED':cll.call_ended,
                                                  'CHANNEL':GroupChannel(cll.channel),
                                                  'LENGTH':str(cll.duration)}

def User(usr:discord.User): return {'NAME':usr.name,
                                    'ID':usr.id,
                                    'DISCRIMINATOR':usr.discriminator,
                                    'AVATAR':usr.avatar,
                                    'BOT':usr.bot,
                                    'AVATAR URL':str(usr.avatar),
                                    'COLOR':usr.color}
    
def GroupChannel(grp:discord.GroupChannel): return {'PEOPLE':Users(grp.recipients),
                                                    'ID':grp.id,
                                                    'OWNER':User(grp.owner),
                                                    'ICON':grp.icon,
                                                    'NAME':grp.name}

def abcUser(abc:discord.abc.User): return {'NAME':abc.name,
                                           'ID':abc.id,
                                           'DISCRIMINATOR':abc.discriminator,
                                           'AVATAR':abc.avatar,
                                           'BOT':abc.bot,
                                           'DISPLAY NAME':abc.display_name,
                                           'AVATAR URL':str(abc.avatar),
                                           'MENTION':abc.mention}

def abcGuildChannel(abc:discord.abc.GuildChannel): return {'NAME':abc.name,
                                                           'GUILD':
                                                           'ID':abc.id,
                                                           'DISCRIMINATOR':abc.discriminator,
                                                           'AVATAR':abc.avatar,
                                                           'BOT':abc.bot,
                                                           'DISPLAY NAME':abc.display_name,
                                                           'AVATAR URL':str(abc.avatar),
                                                           'MENTION':abc.mention}

def Guild(gld:discord.Guild): return {'NAME':gld.name,
                                      'EMOJIS':Emojis(gld.emojis),
                                      'REGION':str(gld.region),
                                      'AFK TIMEOUT':gld.afk_timeout,
                                      }

def VoiceChannel(vcc:discord.VoiceChannel): return 

def Emoji(emj:discord.Emoji): return dict(emj)

def Permissions(prm:discord.Permssions): return dict(prm)

def PermissionOverwrite(prm:discord.PermissionOverwrite): return dict(prm)

def SystemChannelFlags(flg:discord.SystemChannelFlags): return dict(flg)

# ////////////
# ///GROUPS///
# ////////////

def Embeds(embs):
    dic = {}
    for emb in embs: dic[f'EMBED {embs.index(emb)}'] = Embed(emb)
    return dic

def Users(usrs):
    dic = {}
    for usr in usrs: dic[f'USER {usrs.index(usr)}'] = User(usr)
    return dic

def abcUsers(abcs):
    dic = {}
    for abc in abcs: dic[f'ABC USER {abcs.index(abc)}'] = abcUser(abc)
    return dic

def Emojis(emjs):
    dic = {}
    for emj in emjs: dic[f'EMOJI {abcs.index(abc)}'] = Emoji(emj)
    return dic
