#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
import youtube_dl as ytdl
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": False,
    "extract_flat": "in_playlist"
}

class Video:
    """
    >>> RETURNS INFO OF GIVEN URL <<<
    """

    def __init__(self, url_or_search, index):
        """
        >>> PLAYS OR SEARCHES FOR `URL`
        """
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            video = self._get_info(url_or_search, index)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]

    def _get_info(self, video_url, index):
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][index]["url"], index)  # get info for first video
            else:
                video = info
            return video

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help='music',
                  brief='Plays Music',
                  usage=';]play {vc} {link}',
                  description='''\
LINK [STR] - Link to some file, youtube video, or is a youtube search
           - YOUTUBE SEARCH
             > SYNTAX: ";]play {vc} yt-{search}"
             > SEARCH RESULT: append "-i={search result number}"
                              to get that result playing
VC   [VC ] - The VC I should join''')
@commands.check(enbl)
async def play(ctx,vc:discord.VoiceChannel, *, link):
    vcC = ctx.voice_client
    if not vcC:
        await vc.connect() # vcC is None if it doesnt exist
    else:
        await ctx.voice_client.disconnect() # Ensures the right VC
        await vc.connect()
    vcC = ctx.voice_client
    if 'https://youtu' in link or 'yt-' in link or 'youtube-' in link:
        index = 0
        if '-i=' in link or '-index=' in link or '-l=' in link or '-listing=' in link:
            for i in ['-i=','-index=','-l=','-listing=']:
                if link.find(i) != -1:
                    index = int(link[link.find(i)+1:(link+" ").find(' ')])
                    link.replace(f'{i}{index}','')
                    break
        try:
            link = Video(link.replace('yt-','').replace('youtube-','').strip(), index-1).stream_url
        except Exception as ex:
            return await ctx.send(f'```diff\n-] ERROR \'{str(ex)}\'```')
    vcC.play(discord.FFmpegPCMAudio(link))
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(play)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('play')
    print('GOOD')
