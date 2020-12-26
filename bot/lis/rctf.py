#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging, re
import traceback
import asyncio
from util import embedify, getPre, dbman
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

bot = commands.Bot(command_prefix=getPre.getPre)
boteth = None

class FalseReaction:
    def __init__(self, emoji, message):
        self.count = 0
        self.me = False
        self.emoji = emoji
        self.custom_emoji = emoji.is_custom_emoji()
        self.message = message

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@bot.listen('on_message')
async def on_msg(msg):
    ct = msg.content.lower()
    # Responds to 'F'
    if ct == 'f' and dbman.get('oth', 'rcf', id=msg.guild.id):
        fcontent = f'\\> <@{msg.author.id}>'
        fmessage = await msg.channel.send(
            embed = embedify.embedify(
                title = "PAY RESPECTS ;]",
                desc = f'{fcontent}'
            )
        )
        await fmessage.add_reaction('<:rcf:598516101638520857>')

    # Responds to 'no u'
    elif ct == "no u" and dbman.get('oth', 'nou', id=msg.guild.id):
        await msg.channel.send("```md\n#] GOT \'EM\n> Get Got M8```")

    # Responds to 'you fool'
    elif ct == 'you fool' and dbman.get('oth', 'ufl', id=msg.guild.id):
        fool = None
        lines = [
            ' you fool.',
            ' you absolute buffoon.',
            ' you think you can challenge me in my own home directory?',
            ' you think you can rebel against my sudo?',
            ' you dare come into my computer',
            ' and delete my /root',
            ' and put shutdown 0 in my .bashrc?',
            ' you thought you were safe',
            ' with your antivirus',
            ' behind that firewall of yours.',
            ' I will take this worm',
            ' and destroy you.',
            ' I didn\'t want cyberwar.',
            ' but i didn\'t start it,',
            ' **you incompetent buffoon**'
        ]
        for line in lines:
            async with msg.channel.typing():
                await asyncio.sleep(len(line)/16)
            if fool:
                await fool.edit(content=fool.content+line)
            else:
                fool = await msg.channel.send(line)

    # When Pinged
    elif re.match(r'(<@)!?(555862187403378699>)', ct):
        pre = dbman.get('pre', 'pre', id=msg.guild.id)
        await msg.channel.send(f'```md\n#] INFO\n> My prefix is "{pre}"\n> For example: "{pre}hlep"```')

async def plug_starboard(msg, emojis):
    stars = msg.guild.get_channel(dbman.get('star', 'channel', id = msg.guild.id))
    starred = []
    for reaction in msg.reactions:
        if str(reaction.emoji) in emojis:
            starred.append(str(reaction.count) + "x" + str(reaction.emoji))

    embed = embedify.embedify(
        title = 'STARBOARD ;]',
        desc = msg.content,
        fields = [
            ['AUTHOR', f'<@{msg.author.id}> `{str(msg.author)}`', True],
            ['CHANNEL', f'<#{msg.channel.id}>', True],
            [
                'LINK',
                f'[JUMP](https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id})',
                True
            ],
            ['STARS', '\n'.join(starred), True]
        ],
        thumb = str(msg.author.avatar_url)
    )
    attachments = [att.url for att in msg.attachments]
    link_attachment = False
    if " " not in msg.content and re.search(r"^https?://.*\.(png|jpg|gif|jpeg|bmp|tiff)$", msg.content.lower()):
        attachments.append(msg.content)
        link_attachment = True
    if len(attachments):
        embed.add_field(
            name = 'ATTACHMENTS',
            value = '\n'.join(attachments),
            inline = False
        )
        try:
            if not link_attachment:
                msg.attachments[0].height
            embed.set_image(url = attachments[0])
        except:
            pass
    stars_id = dbman.get('starboard', 'starboard_id', message_id = msg.id)
    try:
        if not stars_id:
            raise TypeError("stars_id isn't available yet")
        stars_msg = await stars.fetch_message(stars_id)
        await stars_msg.edit(embed = embed)
    except:
        stars_msg = await stars.send(embed = embed)
        dbman.insert('starboard', starboard_id = stars_msg.id, message_id = msg.id)

async def handle_reaction_add(reaction, user):
    if user is None:
        return
    chn = reaction.message.channel
    try:
        if user.id == 555862187403378699:
            return
        msg = reaction.message
        emojis = str(dbman.get('star', 'emoji', id = msg.guild.id))
        accept = str(reaction.emoji) in emojis
        multi = bool(dbman.get('star', 'multi', id = msg.guild.id))
        try:
            mng = msg.embeds[0].title == "SERVER MANAGEMENT ;]"
            if msg.embeds[0].title == "STARBOARD ;]" and accept:
                await chn.send(f"<@{user.id}>```diff\n-] YOU CAN'T STAR THE STARBOARD```", delete_after = 10.0)
                await reaction.remove(user)
                mng = True
        except IndexError:
            mng = False
        if accept and not mng:
            if user.id == msg.author.id:
                await chn.send(f"<@{user.id}>```diff\n-] YOU CAN'T STAR YOUR OWN MESSAGES```", delete_after = 10.0)
                await reaction.remove(user)
            else:
                cc = 0
                react_users = []
                for r in msg.reactions:
                    if str(r.emoji) in emojis:
                        cc += r.count
                        if not multi:
                            async for u in r.users():
                                if u.id in react_users:
                                    await chn.send(
                                        f"<@{user.id}>```diff\n-] YOU CAN'T STAR A MESSAGE MULTIPLE TIMES```",
                                        delete_after = 10.0
                                    )
                                    return await reaction.remove(user)
                                react_users.append(u.id)
                count = dbman.get('star', 'count', id = msg.guild.id)
                if count <= cc and count > 0:
                    await plug_starboard(msg, emojis)
        desc = reaction.message.embeds[0].description
        og = desc
        if str(reaction) == "<:rcf:598516101638520857>" and \
                reaction.message.author.id == 555862187403378699 and \
                user.id != 555862187403378699:
            if reaction.message.embeds[0].title == "PAY RESPECTS ;]" and f'<@{user.id}>' not in og:
                await reaction.message.edit(
                    embed = embedify.embedify(
                        title = "PAY RESPECTS ;]",
                        desc = f'{og}\n\\> <@{user.id}>'
                    )
                )
            elif 'PAY RESPECTS' in og and f'{user}' not in og:
                await reaction.message.edit(
                    embed = embedify.embedify(
                        desc = f'```md\n{og[5:-3]}\n> {user}```'
                    )
                )
    except IndexError:
        pass
    except Exception as ex:
        await chn.send(f"`{ex}` line {ex.__traceback__.tb_lineno}")

async def handle_reaction_remove(reaction, user):
    if user is None:
        return
    chn = reaction.message.channel
    try:
        if user.id == 555862187403378699:
            return
        msg = reaction.message
        emojis = str(dbman.get('star', 'emoji', id = msg.guild.id))
        try:
            mng = msg.embeds[0].title == "SERVER MANAGEMENT ;]"
        except IndexError:
            mng = False
        if str(reaction.emoji) in emojis and not mng:
            cc = 0
            for r in msg.reactions:
                cc += r.count if str(r.emoji) in emojis else 0
            count = dbman.get('star', 'count', id = msg.guild.id)
            if count <= cc and count > 0:
                await plug_starboard(msg, emojis)
            elif count > 0 and count > cc:
                stars = msg.guild.get_channel(dbman.get('star', 'channel', id = msg.guild.id))
                stars_id = dbman.get('starboard', 'starboard_id', message_id = msg.id)
                if stars_id:
                    stars_msg = await stars.fetch_message(stars_id)
                    await stars_msg.delete()
                    dbman.remove('starboard', starboard_id = stars_id, message_id = msg.id)
        desc = reaction.message.embeds[0].description
        og = desc
        if str(reaction) == "<:rcf:598516101638520857>" and \
                reaction.message.author.id == 555862187403378699 and \
                user.id != 555862187403378699:
            if reaction.message.embeds[0].title == "PAY RESPECTS ;]" and f'<@{user.id}>' in og:
                og = og.replace(f"\n\\> <@{user.id}>", "")
                og = og.replace(f"\\> <@{user.id}>\n", "")
                await reaction.message.edit(
                    embed = embedify.embedify(
                        title = "PAY RESPECTS ;]",
                        desc = f'{og}'
                    )
                )
            elif 'PAY RESPECTS' in og and f'{user}' in og:
                og = og.replace(f"\n> {user}", "")
                og = og.replace(f"> {user}\n", "")
                await reaction.message.edit(
                    embed = embedify.embedify(
                        desc = f'```md\n{og[5:-3]}```'
                    )
                )
    except IndexError:
        pass
    except Exception as ex:
        await chn.send(f"`{ex}` line {ex.__traceback__.tb_lineno}")

async def from_rct_payload(payload):
    chn = await boteth.fetch_channel(payload.channel_id)
    msg = await chn.fetch_message(payload.message_id)
    for reaction in msg.reactions:
        if str(reaction.emoji) == str(payload.emoji):
            if payload.member:
                return reaction, payload.member
            return reaction, chn.guild.get_member(payload.user_id)
    reaction = FalseReaction(payload.emoji, msg)
    return reaction, chn.guild.get_member(payload.user_id)

@bot.listen()
async def on_raw_reaction_add(payload):
    reaction, user = await from_rct_payload(payload)
    return await handle_reaction_add(reaction, user)

@bot.listen()
async def on_raw_reaction_remove(payload):
    reaction, user = await from_rct_payload(payload)
    return await handle_reaction_remove(reaction, user)

@bot.listen()
async def on_raw_message_delete(payload):
    stars_id = dbman.get('starboard', 'starboard_id', message_id = payload.message_id)
    if stars_id:
        dbman.remove('starboard', starboard_id = stars_id, message_id = payload.message_id)


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    global boteth
    boteth = bot
    print('+LIS')
    bot.add_listener(on_raw_reaction_add)
    bot.add_listener(on_raw_reaction_remove)
    bot.add_listener(on_msg, "on_message")
    print('GOOD')

def teardown(bot):
    print('-LIS')
    global boteth
    boteth = bot
    bot.remove_listener("on_msg", "on_message")
    bot.remove_listener("on_raw_reaction_add")
    bot.remove_listener("on_raw_reaction_remove")
    print('GOOD')
