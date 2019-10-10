from util import dbman
def getPre(bot,msg):
    try:
        return dbman.get('pre','pre',id=int(msg.guild.id))
    except Exception as ex:
        print(ex)
        return ";]"
