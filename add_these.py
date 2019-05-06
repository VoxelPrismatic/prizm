##/// RESTART
import subprocess
@commands.command()
@commands.in_owner()
async def rst(ctx):
    await ctx.send('#]COMING BACK SOON 0.0')
    await bot.logout()
    subprocess.call([sys.executable, "bot.py"])
    
##/// NLP
import nltk
@bot.listen()
async def on_message(message):
    wrdTOK = word_tokenize(message.content)
    sntTOK = sent_tokenize(message.content)
    NOT COMPLETE
    
##/// EXEC
@bot.command()
@commands.is_owner()
async def exe(self, ctx, code):
    try:
        with open('execthis.py','w') as writecode:
            writecode.write(code)
        await ctx.message.add_reaction('')
    except:
        await ctx.send('```md\n#]UH OH!\n> Something went wrong while trying to execute this command```')

@bot.command()
@commands.is_owner()
async def run(self, ctx, typ: int, *args):
    try:
        import execthis
        if typ: await execthis(*args)
        else: execthis(*args)
    except:
        await ctx.send('```md\n#]UH OH!\n> Something went wrong while trying to execute this command```')
  
