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
