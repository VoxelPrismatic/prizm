#!/gld/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from util import ez
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [
        "guildinfo", "guildi", "iguild", "gldi", "igld",
        "serverinfo", "srvi", "isrv", "si", "serveri", "iserver"
    ],
    help='dis',
    brief = 'Shows info about this guild',
    usage = ';]gi',
    description = '''\
[NO INPUT FOR THS COMMAND]
'''
)
@commands.check(enbl)
async def gi(ctx):
    async with ctx.channel.typing():
        pass
    _gld = ctx.guild
    features = "\n> ".join(_gld.features) if len(_gld.features) else "[NONE]"
    lit = [f"""
#] INFO FOR ${_gld.name}
      ID ] {_gld.id}
     AFK ] {_gld.afk_timeout} - {_gld.afk_channel}
    DESC ] {_gld.description}
    SIZE ] {ez.ifstr(_gld.large, "SMALL", "LARGE")}
   OWNER ] {_gld.owner}
  BANNER ] {_gld.banner_url}
  REGION ] {_gld.region}
  NOTIFS ] {_gld.default_notifications}
  VERIFY ] {_gld.verification_level}
 CREATED ] {_gld.created_at}
 2FA LVL ] {_gld.mfa_level}
 MEMBERS ] {_gld.member_count}
NSFW BAN ] {str(_gld.explicit_content_filter)}""",
           f"""
#] FEATURES FOR ${_gld.name}
> {features}
""",
           f"""
#] OTHER INFO ABOUT ${_gld.name}
       VCs ] {len(_gld.voice_channels)}
    SPLASH ] {_gld.splash}
  BOOSTERS ] {_gld.premium_subscription_count}
  CHANNELS ] {len(_gld.text_channels)}
 BOOST LVL ] {_gld.premium_tier}
CATEGORIES ] {len(_gld.categories)}
"""]

    lit.extend(
        ez.pager(
            _gld.channels, 2000,
            ["#", discord.TextChannel],
            ["%", discord.VoiceChannel],
            ["+", discord.CategoryChannel],
            head = "CHANNELS ] "
        )
    )

    lit.extend(
        ez.pager(
            _gld.roles, 2000,
            ['&', "ANY"],
            head = "ROLES ] "
        )
    )

    lit.extend(
        ez.pager(
            _gld.emojis, 2000,
            [':', "ANY"],
            head = "EMOJI NAMES ] "
        )
    )

    await pages.PageThis(
        ctx, lit, "GUILD INFO",
        thumb = str(_gld.icon_url).replace('webp', 'png')
    )

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(gi)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('gi')
    print('GOOD')
