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
    tables = dbman.getTabs()
    for g in bot.guilds:
        for table in tables:
            if table in ["starboard", "twitter"]:
                continue
            if (not dbman.get(table, 'id', id=g.id, return_null=True)) and \
                    table not in ["mod", "tag"]:
                dbman.insert(table, id=g.id)
            for gt in dbman.get(table, 'id', return_as_list = True):
                if gt not in gIDs:
                    dbman.remove(table, id=gt)
        dbman.update('srv', 'name', g.name, id=g.id)
        for command in bot.commands:
            try:
                dbman.addCol('com', command.name, 'INTEGER DEFAULT 1')
            except Exception as ex:
                pass
                #print(ex)
                # This means that the column already exists
                #// If you know of any 'ALTER TABLE name ADD COLUMN IF NOT EXISTS name',
                #// Please let me know :D

    if time.monotonic()-lastsave >= 10:
        dbman.save()
        lastsave = time.monotonic()
