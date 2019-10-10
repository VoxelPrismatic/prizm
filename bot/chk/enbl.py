from util import dbman
def enbl(ctx) -> bool:
    """
    >>> RETURNS TRUE IF THE COMMAND IS ENABLED <<<

    CTX [CTX] - Context, just used for the command name
    """
    try:
        if ctx.guild:
            return dbman.get('com', ctx.command.name, id=int(ctx.guild.id)) # Command is en/disabled
        else: # In DMs
            return True
    except: # Just in case
        return True
