import discord, time
from util import dbman
from dyn import refresh
lastsave = time.monotonic()
def saver(bot) -> None:
    try:
        x = lastsave
    except:
        lastsave = time.monotonic()
    """
    >>> SAVES DATA TO JSON FILE <<<
    BOT [BOT] - Bot, has all commands and things
    """
    allext, lodtxt = refresh.refresh()
    gIDs = [g.id for g in bot.guilds]
    for g in bot.guilds:
        tables = dbman.getTabs()
        for table in tables:
            if not dbman.get(table, 'id', id=g.id, return_null=True) and table not in ["mod", "tag"]:
                dbman.insert(table, id=g.id)
            for gt in dbman.get(table, 'id'):
                if gt not in gIDs:
                    dbman.remove(table, id=gt)
        dbman.update('srv', 'name', g.name, id=g.id)
        for ext in allext[:-1]:
            for nam in ext:
                try:
                    dbman.addCol('com', bot.get_command(nam).name, 'INTEGER DEFAULT 1')
                except:
                    pass # This means that the column already exists
                    #// If you know of any 'ALTER TABLE name ADD COLUMN IF NOT EXISTS name',
                    #// Please let me know :D
   
    if time.monotonic()-lastsave >= 10:
        dbman.save()
        lastsave = time.monotonic()