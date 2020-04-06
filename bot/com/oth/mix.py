#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os, signal
import typing, asyncio
import discord                    #python3.7 -m pip install -U discord.py
import logging, subprocess
from util import embedify, pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [],
    help = 'ai',
    brief = 'A noise generator with 2 inputs',
    usage = ';]mix {action} {?args}',
    description = '''\
ACTION [TEXT] - [slot1, slot2, imgs, view, slots, kill]
> slot1 - Load an attached image into the "image" file
> slot2 - Load an attached image into the "pattern" file
> imgs  - View currently loaded images
> view  - View the status of the current mix
> slots - Start the mixing
> kill  - Kills the current process if you started it
ARGS   [TEXT] - [-iter=, -np]
> -iter= - Set the number of iterations [max 120, min 5]
>    -np - Do not ping when finished
'''
)
@commands.check(enbl)
async def mix(ctx, *, action):

    if action.split()[0] in ['slot1','s1','1','img1']:
        if open('mix/status').read().strip() != 'DONE':
            return await ctx.send(
                '```diff\n-] I AM GENERATING SOMETHING, CHECK BACK LATER\n'
                '=] Or use \';]mix view\' to see the latest iter```'
            )
        try:
            if ctx.message.attachments[0].size > 1024*1024*4:
                return await ctx.send('```diff\n-] TOO BIG\n=] Max file size is 4MB```')
            await ctx.message.attachments[0].save("mix/s1.jpg")
            await ctx.message.attachments[0].save("mix/now.png")
            await ctx.message.attachments[0].save("mix/s1.png")
            await ctx.message.add_reaction('<:wrk:608810652756344851>')
        except IndexError:
            return await ctx.send('```diff\n-] PLEASE SEND AN IMAGE```')

    elif action.split()[0] in ['slot2','s2','2','img2']:
        if open('mix/status').read().strip() != 'DONE':
            return await ctx.send(
                '```diff\n-] I AM GENERATING SOMETHING, CHECK BACK LATER\n'
                '=] Or use \';]mix view\' to see the latest iter```'
            )
        try:
            if ctx.message.attachments[0].size > 1024*1024*4:
                return await ctx.send('```diff\n-] TOO BIG\n=] Max file size is 4MB```')
            await ctx.message.attachments[0].save("mix/s2.jpg")
            await ctx.message.attachments[0].save("mix/s2.png")
            await ctx.message.add_reaction('<:wrk:608810652756344851>')
        except IndexError:
            return await ctx.send('```diff\n-] PLEASE SEND AN IMAGE```')

    elif action.split()[0] in ['run','start','slots']:
        if open('mix/status').read().strip() != 'DONE':
            return await ctx.send(
                '```diff\n-] I AM GENERATING SOMETHING, CHECK BACK LATER\n'
                '=] Or use \';]mix view\' to see the latest iter```'
            )
        mc = ctx.message.content
        settings = {
            'iter': 60,
            'ping': True
        }
        mc += ' '
        if '-i=' in mc:
            settings['iter'] = int(
                mc[mc.find('-i=') + 3: mc.find(' ', mc.find('-i='))]
            )
        elif '-iter=' in mc:
            settings['iter'] = int(
                mc[mc.find('-iter=')+6: mc.find(' ', mc.find('-iter='))]
            )
        elif 'max' in mc or '-m' in mc: settings['iter'] = 60
        if '-no' in mc or '-np' in mc: settings['ping'] = False

        it = settings['iter']
        it = max([5,min([it,120])])

        settings['iter'] = it

        open('mix/status','w+').write('WAIT')
        open('mix/loc','w+').write('INIT')
        open('mix/iter','w+').write(str(settings['iter']))

        proc = subprocess.Popen(["python3.7", "mixGEN.py"])

        ratio_h = 1
        ratio_w = 1
        image_w, image_h = Image.open('mix/s1.jpg').size
        if image_h > 600: ratio_h = image_h/600
        image_h /= ratio_h
        image_w /= ratio_h
        if image_w > 800: ratio_w = image_w/800
        image_h /= ratio_w
        image_w /= ratio_w

        image_h = int(image_h)
        image_w = int(image_w)
        time = int(open("mix/iter").read())+5
        res =  (image_h*image_w) / (800*600)
        time = int(time*res*3/4)

        await ctx.send(f'''```md
#] I AM GENERATING THE IMAGE, I WILL SEND IT WHEN ITS DONE ;]
>  Or use \';]mix kill\' to stop it now
=] THIS WILL TAKE UP TO {time} MIN, PLEASE STAND BY```''')
        while open('mix/status').read() != 'DONE':
            loc = open("mix/loc").read()
            def chek(m): return m.author == ctx.author and m.channel == ctx.channel
            while loc == open('mix/loc').read() and open('mix/status').read() != 'DONE':
                try: m = await ctx.bot.wait_for('message',check=chek,timeout=10.0)
                except asyncio.TimeoutError as ex: pass
                else:
                    if m.content.lower() in [
                            ';]mix kill', ';]mix stop', ';]mix clear',
                            ';]mix end', ';]mix break', ';]mix complete',
                            ';]mix empty',';]smix send'
                    ]:
                        open('mix/status','w').write('DONE')
                        os.kill(proc.pid,signal.SIGKILL)

        return await ctx.send(
            (f'<@{ctx.author.id}> ' if settings['ping'] else '') + f'```md\n#] GENERATED!```',
            file=discord.File('mix/now.png')
        )

    elif action.split()[0] in ['see','view','where']:
        loc = open("mix/loc").read()
        ttl = open("mix/iter").read()
        stt = open('mix/status').read()
        try:
            content = f'`[{int(loc)/int(ttl)*100:.2f}% - {loc}/{ttl}] {stt}`'
        except:
            content=f'`[{loc}] {stt}`'
        await ctx.send(content,file=discord.File(fp=open('mix/now.png','rb')))
    elif action.split()[0] == 'reset' and ctx.author.id == 481591703959240706:
        open('mix/status','w').write('DONE')
        await ctx.message.add_reaction('<:wrk:608810652756344851>')
    elif action.split()[0] in ['kill','stop','clear','end','break','complete','empty','send']:
        pass
    elif action.split()[0] in ['slots','imgs','images']:
        await ctx.send(
            files = [
                discord.File(fp=open('mix/s1.png','rb')),
                discord.File(fp=open('mix/s2.png','rb'))
            ]
        )
    else:
        return await ctx.send(f'```diff\n-] KEY {action} WAS NOT FOUND [s1, s2, kill, view]```')



##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(mix)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('mix')
    print('GOOD')

