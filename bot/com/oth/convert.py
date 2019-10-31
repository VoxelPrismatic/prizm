#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing, os, aiofiles, subprocess
import PIL #Image Conversion
import ffmpy3 as FIL #Sound and Video Conversion
import discord, pandas as pd
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from chk.has import *

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["change", "converter"],
                  help='oth',
                  brief = 'Converts a file to a {fmt} file!',
                  usage = ';]convert {fmt} <attach a file or have an embedable link>',
                  description = 'FMT [TEXT] - The format to convert *to* eg "pdf"')
@commands.check(enbl)
@commands.check(has_attachment)
async def convert(ctx, fmt):
    msg = await ctx.send('```md\n#] INIT```')
    att = ctx.message.attachments[0]
    if att.size > 6291456:
        return await msg.edit(content='```diff\n-] ATTACHMENT TOO LARGE [4MB MAX]```')
    new = fmt
    data = await att.read()
    old = att.filename.split('.')[-1]
    if old == 'jpg': old = 'jpeg'
    old, new = old.upper(), new.upper()
    await msg.edit(content="```md\n#] DOWNLOADING```")
    await att.save("msc/RAW."+old)
    img_ext = ['bmp', 'dib', 'eps', 'gif', 'icns', 'ico',
              'im', 'jpeg', 'jpg', 'j2k', 'msp', 'pcx',
              'png', 'ppm', 'sgi', 'spider', 'tga', 'tiff',
              'webp', 'xbm']
    txt_ext = ['txt', 'py', 'pyc', 'js', 'java', 'cpp',
              'rhtml', 'gpp', 'cs', 'c', 'asp', 'css'
              'aspx', 'axd', 'asx', 'asmx', 'ashx',
              'htm', 'html', 'xhtml', 'jhtml', 'jsp', 'jspx',
              'wss', 'do', 'action', 'pl', 'php', 'php4',
              'php3', 'phtml', 'rb', 'shtml', 'xml', 'rss',
              'json', 'html5', 'css3', 'yaml', 'swift',
              'vbs', 'scss', 'less', 'bat', 'ps1', 'bash',
              'c++', 'csv']
    aud_ext = ['aa', 'aac', 'ac3', 'act', 'adts', 'aea',
               'aiff', 'alsa', 'ape', 'aptx', 'aptx_hd', 'asf',
               'asf', 'asf_o', 'asf_stream', 'ast', 'boa', 'caf',
               'f32be', 'f32le', 'f64be', 'f64le', 'flac', 'ircam',
               'jack', 'm4a', '3gp', '3g2', 'mj2', 'mp2',
               'mp3', 'mpeg', 'opus', 'oss', 'ogg', 'oga',
               'pulse', 's16be', 's16le', 's24be', 's24le', 's32be',
               's32le', 's8', 'sds', 'sndio', 'spx', 'u16be',
               'u16le', 'u24be', 'u24le', 'u32be', 'u32le', 'u8',
               'wav', 'wve', 'alaw', 'daud', 'dts', 'dtshd',
               'epaf', 'eac3', 'oma', 'sln', 'tta']
    vid_ext = ['a64', 'avi', 'avm2', 'avr', 'bethsoftvid',
               'cdg', 'cdxl', 'dv', 'dvd', 'ea', 'f4v',
               'filmstrip', 'flic', 'flv', 'gdv', 'h261', 'h263',
               'h264', 'hevc', 'hls', 'ipmovie', 'ipod', 'kmsgrab',
               'm4v', 'matroska', 'webm', 'mjpeg', 'mjpeg_2000', 'mlv',
               'mov', 'mp4', 'mpeg1video', 'mpeg2video', 'mpegvideo', 'nsv',
               'nuv', 'ogv', 'ogg', 'swf', 'vc1', 'vcd',
               'webm', 'webm_chunk', 'xv', 'gif', 'apng']
    fmg_ext = ['apng', 'anm', 'alias_pix', 'bmp_pipe', 'gif', 'ico',
               'image2', 'image2pipe', 'j2k_pipe', 'jpeg_pipe', 'jpegls_pipe',
               'mpjpeg', 'png_pipe', 'psd_pipe', 'singlejpeg', 'webp', 'webp_pipe']
    others = {
        "xls.csv": (lambda r, w: pd.read_excel(r).to_csv(w)),
        "xlsx.csv": (lambda r, w: pd.read_excel(r).to_csv(w)),
        "csv.xls": (lambda r, w: pd.read_csv(r).to_excel(w)),
        "csv.xlsx": (lambda r, w: pd.read_csv(r).to_excel(w))
    }
    await msg.edit(content="```md\n#] CONVERTING```")
    if old.lower() in img_ext and new.lower() in img_ext:
        img = PIL.Image.open("msc/RAW."+old)
        img.save("msc/RAW."+new)
        await msg.edit(content="```md\n#] UPLOADING TO DISCORD```")
        await ctx.send("```md\n#] CONVERTED ;]```", file=discord.File('msc/RAW.' + new))
        await msg.delete()
        return os.remove("msc/RAW."+new), os.remove("msc/RAW."+old)
    elif old.lower() in txt_ext and new.lower() in txt_ext:
        old_file = await aiofiles.open("msc/RAW."+old)
        new_file = await aiofiles.open("msc/RAW."+new, "w+")
        await new_file.write("".join(await old_file.readlines()))
        await new_file.close()
        await old_file.close()
        await msg.edit(content="```md\n#] UPLOADING TO DISCORD```")
        await ctx.send("```md\n#] CONVERTED ;]```", file=discord.File('msc/RAW.' + new))
        await msg.delete()
        return os.remove("msc/RAW."+new), os.remove("msc/RAW."+old)
    elif old.lower() in aud_ext and new.lower() in aud_ext:
        root = "/home/priz/Desktop/PRIZM/msc/RAW."
        proc = FIL.FFmpeg(
            inputs={f"/home/priz/Desktop/PRIZM/msc/RAW.{old}": None},
            outputs={f"/home/priz/Desktop/PRIZM/msc/RAW.{new}": None}
        )
        await proc.run_async()
        await proc.wait()
        await ctx.send("```md\n#] CONVERTED ;]```", file=discord.File('msc/RAW.' + new))
        await msg.delete()
        return os.remove("msc/RAW."+new), os.remove("msc/RAW."+old)
    elif old.lower() in vid_ext and new.lower() in vid_ext:
        root = "/home/priz/Desktop/PRIZM/msc/RAW."
        proc = FIL.FFmpeg(
            inputs={f"/home/priz/Desktop/PRIZM/msc/RAW.{old}": None},
            outputs={f"/home/priz/Desktop/PRIZM/msc/RAW.{new}": None}
        )
        await proc.run_async()
        await proc.wait()
        await ctx.send("```md\n#] CONVERTED ;]```", file=discord.File('msc/RAW.' + new))
        await msg.delete()
        return os.remove("msc/RAW."+new), os.remove("msc/RAW."+old)
    elif old.lower() in fmg_ext and new.lower() in fmg_ext:
        root = "/home/priz/Desktop/PRIZM/msc/RAW."
        proc = FIL.FFmpeg(
            inputs={f"/home/priz/Desktop/PRIZM/msc/RAW.{old}": None},
            outputs={f"/home/priz/Desktop/PRIZM/msc/RAW.{new}": None}
        )
        await proc.run_async()
        await proc.wait()
        await ctx.send("```md\n#] CONVERTED ;]```", file=discord.File('msc/RAW.' + new))
        await msg.delete()
        return os.remove("msc/RAW."+new), os.remove("msc/RAW."+old)
    await msg.edit(content=f'```diff\n-] CONVERSION FROM {old} TO {new} UNSUPPORTED\n=] Try converting an image to an image or text to text```')
    return os.remove('msc/RAW.'+old)

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
