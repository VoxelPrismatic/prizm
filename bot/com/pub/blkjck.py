#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["blackjack","bj"],
                  help = 'fun',
                  brief = 'Virtual Black Jack',
                  usage = ';]blkjck',
                  description = '[NO ARGS FOR THIS COMMAND]')
@commands.check(enbl)
async def blkjck(ctx):
    deck = {'heart':[f'{x}<3' for x in ['A23456789TJQK']],
            'spade':[f'{x}<)' for x in ['A23456789TJQK']],
            'diamd':[f'{x}<>' for x in ['A23456789TJQK']],
            'clubs':[f'{x}>3' for x in ['A23456789TJQK']]}
    card2num = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':11,'K':11}
    TTLusr = 0
    TTLcpu = 0
    card_usr = []
    card_cpu = []
    while TTLusr <= 18:
        suite = random.choice(['heart','spade','diamd','clubs'])
        card = deck[suite].pop(deck[suite].index(random.choice(deck[suite])))
        num = card2num[card[0]]
        TTLusr += num
        card_usr.append(card)

    while ttl2 <= 18:
        suite = random.choice(['heart','spade','diamd','clubs'])
        card = deck[suite].pop(deck[suite].index(random.choice(deck[suite])))
        num = card2num[card[0]]
        TTLcpu += num
        card_cpu.append(card)
    STRusr = f'USER // {", ".join(card_usr)} [{TTLusr}] '
    STRcpu = f'COMP // {", ".join(card_cpu)} [{TTLcpu}] '
    if TTLusr == TTLcpu:
        STRusr += '[TIE]'
        STRcpu += '[TIE]'
    elif TTLusr == 21:
        STRusr += '[BLACK JACK]'
        STRcpu += '[LOSS]'
    elif TTLusr > 21:
        STRusr += '[BUST]'
    elif TTLusr > TTLcpu:
        STRusr += '[WIN]'
    elif TTLusr < TTLcpu:
        STRusr += '[LOSS]'
    if TTLusr == TTLcpu:
        pass
    elif TTLcpu == 21:
        STRcpu += '[BLACK JACK]'
        STRusr += '[LOSS]'
    if TTLcpu > 21:
        STRcpu += '[BUST]'
    elif TTLcpu > TTLusr:
        STRcpu += '[WIN]'
    elif TTLcpu < TTLusr:
        STRcpu += '[LOSS]'
    await ctx.send(f'```md\n#] BLACK JACK!``````diff\n+] {usrtxt}\n-] {cputxt}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(blkjck)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('blkjck')
    print('GOOD')
