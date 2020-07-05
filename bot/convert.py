#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, os, aiofiles
import PIL #Image Conversion
import ffmpy3 as FIL #Sound and Video Conversion
import discord, pandas as pd
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from chk.has import *
import asyncio
import random
from util import ez

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = ["change", "converter"],
    help = 'oth',
    brief = 'Converts a file to a {fmt} file! Supports 316 formats!',
    usage = ';]convert {fmt} <attach a file or have an embedable link>',
    description = '''\
FMT [TEXT] - The format to convert *to* eg "pdf"
'''
)
@commands.check(enbl)
@commands.check(has_attachment)
async def convert(ctx, fmt):
    msg = await ctx.send('```md\n#] INITIALIZING```')
    att = ctx.message.attachments[0]
    formats = eval(open("msc/formats.json").read())
    img_ext = formats["image"]
    txt_ext = formats["text"]
    aud_ext = formats["audio"]
    vid_ext = formats["video"]
    ffm_ext = formats["ffmpeg"]
    xls_ext = formats["sheet"]
    doc_ext = formats["doc"]
    ppt_ext = formats["slide"]
    ebk_ext = formats["ebook"]
    drw_ext = formats["draw"]
    mth_ext = formats["math"]

    ffmpeg_formats = [img_ext, aud_ext, vid_ext, ffm_ext]
    office_formats = [xls_ext, doc_ext, ppt_ext, ebk_ext, drw_ext, mth_ext]

    if att.size > 16777216:
        return await msg.edit(content = '```diff\n-] ATTACHMENT TOO LARGE [16MB MAX]```')
    new = fmt
    data = await att.read()
    old = att.filename.split('.')[-1]
    root = "/home/priz/Desktop/PRIZM/msc/RAW"
    if old == 'jpg':
        old = 'jpeg'
    if old == 'tif':
        old = 'tiff'
    if new == 'tif':
        new = 'tiff'
    old, new = old.lower(), new.lower()
    await msg.edit(content = "```md\n#] DOWNLOADING```")
    await att.save("msc/RAW." + old)
    await msg.edit(content = "```md\n#] CONVERTING```")
    if old.lower() in img_ext and new.lower() in img_ext:
        img = PIL.Image.open("msc/RAW." + old)
        if new not in ["png", "gif", "bmp", "tiff", "j2k"]:
            img = img.convert("RGB")
        img.save("msc/RAW." + new)
    elif old.lower() in txt_ext and new.lower() in txt_ext:
        os.rename("msc/RAW." + old, "msc/RAW." + new)
        await msg.edit(content = "```md\n#] UPLOADING TO DISCORD```")
        await ctx.send("```md\n#] CONVERTED ;]```", file = discord.File('msc/RAW.' + new))
        await msg.delete()
        return os.remove("msc/RAW." + new)
    elif any(old in group and new in group for group in ffmpeg_formats):
        proc = FIL.FFmpeg(
            inputs = {f"{root}.{old}": None},
            outputs = {f"{root}.{new}": None}
        )
        await proc.run_async()
        await proc.wait()
    elif any(old in group and new in group for group in office_formats):
        await ez.proc(f"soffice --headless --convert-to {new} {root}.{old}")
        os.rename(f"{root}.{new}", f"{root}.{new}")
    else:
        await msg.edit(
            content = f'''```md
#] CONVERSION FROM {old} TO {new} UNSUPPORTED\
>  I only support images, videos, text files, and office documents for now ;[
>  Make sure your conversion is within the same category...
```''')
        return os.remove('msc/RAW.' + old)

    if os.stat("msc/RAW." + new).st_size < 8388608:
        await msg.edit(content = "```md\n#] UPLOADING TO DISCORD```")
        await ctx.send("```md\n#] CONVERTED ;]```", file = discord.File('msc/RAW.' + new))
    else:
        await msg.edit(content = """```md
#] UPLOADING TO GITHUB
>  This file is too large to upload directly to discord""")
        new_name = "".join(random.choice("ABCDEF1234567890") for x in range(16))
        new_name += "." + new
        open("/home/priz/prizm-hosting/" + new_name, "wb+").write(
            open("msc/RAW." + new, "rb").read()
        )
        git = "/home/priz/prizm-hosting/"
        await ez.proc(f"git -C {git}.git {new_name}")
        await ez.proc(f"git -C {git}.git commit -m 'new file: " + new_name + "'")
        await ez.proc(f"git -C {git}.git push".split())
        await ctx.send(f"""```md
#] CONVERTED ;]``````diff
-] This file IS available to everybody that has this URL for 24 hours
=] Sorry about that mate```
**LINK:** https://github.com/VoxelPrismatic/prizm-hosting/blob/master/{name}""")
    await msg.delete()
    return os.remove("msc/RAW." + new), os.remove('msc/RAW.' + old)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(convert)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('convert')
    print('GOOD')
