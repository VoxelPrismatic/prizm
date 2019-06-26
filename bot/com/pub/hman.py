#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from random import choice as ch
from random import randint as rng
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##
games = {}; count = 0
@commands.command(aliases=["hman","hm"])
@commands.check(enbl)
async def hangman(ctx):
    global games
    if ctx.author.id in list(games): return await ctx.send('```diff\n-] YOUR ALREADY PLAYING SOMEWHERE UwU```')
    if ctx.channel.id in [x[1] for x in list(games)]: return await ctx.send('```A GAME IS ALREADY IN THIS CHANNEL UwU```')
    st = ch([x[:-1] for x in open('/usr/share/dict/words','r').readlines()]).upper()
    while "'" in st or len(st)<5: st = ch([x[:-1] for x in open('/usr/share/dict/words','r').readlines()]).upper()
    st2 = "\_ "*len(st); y = " "; guess = 0; ltr = []
    msg = await ctx.send(embed=embedify.embedify(desc=st2,foot=f"LIVES // {6-guess} || GUESSES // {','.join(ltr)} || Send 'stop' to stop"))
    def check(m):
        try:return m.author.id in list(games) and m.channel.id == games[m.author.id][1]
        except: return False
    games[ctx.author.id] = [msg,msg.channel.id]; y = " "
    while ''.join(st2.split()) != st and y != "STOP" and guess < 6:
        try: v = await ctx.bot.wait_for('message',timeout = 60, check=check)
        except:
            count += 1
            if count >= len(list(games)): games = {}; count = 0
        y = v.content.upper(); st2 = st2.replace('\_','_').split(); wrong = True
        for x in range(len(st)):
            if st[x] == y: st2[x] = y; wrong = False
        st2 = ' '.join(st2).replace('_','\_')
        if len(v.content)==1:
            if wrong and y not in ltr: guess += 1; ltr.append(y); await v.delete()
            elif y not in ltr: ltr.append(y); await v.delete()
        elif v.content == st: st2 == st
        await games[v.author.id][0].edit(embed=embedify.embedify(desc=st2,foot=f"LIVES // {6-guess} || GUESSES // {','.join(ltr)} || Send 'stop' to stop"))
    if guess >= 6: await ctx.send(f'```diff\n-] YOU LOST\n-] WORD // {st}```')
    elif y == 'STOP': await ctx.send(f'```diff\n-] FORCE GAME END\n-] WORD // {st}```')
    elif st == st2.replace(' ',''): await ctx.send('```md\n#] YOU WON!```')
    del games[v.author.id]


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hangman)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command(hangman)
    print('GOOD')