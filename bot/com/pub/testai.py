#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing,logging
import discord                    #python3.7 -m pip install -U discord.py
from pprint import pprint as pp
import random 
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["ai"])
@commands.check(enbl)
async def testai(ctx, *, content):
    cont = content
    with open('PrismaticText','r') as a: txt = [txt.replace('\n','') for txt in a.readlines()]
    freq = {}
    for sent in txt:
        for x in range(len(sent.split())-1):
            word = sent.split()[x]; word2 = sent.split()[x+1]
            if word not in list(freq): freq[word]={}
            if word2 not in list(freq[word]): freq[word][word2]=0
            freq[word][word2]+=1
    ls = []; sn = []
    for z in range(100):
        start = random.choice(list(freq))
        for x in range(20): 
            for y in range(1,len(start.split())+1):
                try: 
                    sr = list(freq[start.split()[-y]].values())
                    st = list(freq[start.split()[-y]])[sr.index(max(sr))]
                    if st == start.split()[-1]:break
                    else: start+=f' {st}'
                    break
                except:pass
        count = 0
        for x in cont.split(): count += 1 if x in start else 0
        ls.append(count);sn.append(start)
    with open('PrismaticText','a') as a: a.write(cont+'\n')
    await ctx.send(sn[ls.index(max(ls))])

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(testai)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('testai')
    print('GOOD')
