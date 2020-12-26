import dbl, discord
from discord.ext import commands
import asyncio, logging

class dblAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU1NTg2MjE4NzQwMzM3ODY5OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNTY0MDY4NDM1fQ.tNLvZbOe1r614gw_1wQ2Tf_lL10nND4WGtL_aNJ3oPU' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.updating = self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        while not self.bot.is_closed():
            print('> UPDATING INFO [DBL]')
            try:
                await self.dblpy.post_guild_count()
                print('- COMPLETE')
            except Exception as ex:
                print('- ERROR ]',str(ex))
            await asyncio.sleep(86400)

def setup(bot):
    print('+COG')
    bot.add_cog(dblAPI(bot))
    print('GOOD')

