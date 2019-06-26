#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing,logging
import discord                    #python3.7 -m pip install -U discord.py
from pprint import pprint as pp
import random 
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def exc(bot, ctx, code: int):
    await log(bot, 'EXCEPTION!',f'TYPE // {code}\n> OCCURED IN // {ctx.channel}\n> 1] BadReq // 2] AllForbid // 3] 404')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///     THE AI BITS     ///##
##///---------------------///##

async def on_message(bot, message):
    cont = message.content[1:]
    with open('PrismaticText','r') as a: txt = [txt.replace('\n','') for txt in a.readlines()]
    freq = {}
    for sent in txt:
        for x in range(len(sent.split())-1):
            word = sent.split()[x]; word2 = sent.split()[x+1]
            if word not in list(freq): freq[word]={}
            if word2 not in list(freq[word]): freq[word][word2]=0
            freq[word][word2]+=1
    ls = []; sn = []
    for z in range(300):
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
        #print(start)
        count = 0
        for x in cont.split(): count += 1 if x in start else 0
        ls.append(count);sn.append(start)
    with open('PrismaticText','a') as a: a.write(cont+'\n')
    await message.channel.send(sn[ls.index(max(ls))])
    with open('PrismaticText','r') as a: txt = [txt.replace('\n','') for txt in a.readlines()]
    tx = []
    for t in txt:
        for st in '.,><;:\'"[]{}-=_+!@#$%^&\\':
            while st+st in t:t = t.replace(st+st,st)
        if t not in tx:tx.append(t.lower().strip())
    with open('PrismaticText','w') as a: a.write('\n'.join(tx)+'\n')
    pp(freq)
