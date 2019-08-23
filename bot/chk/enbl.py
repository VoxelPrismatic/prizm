import json
def enbl(ctx) -> bool:
    """
    >>> RETURNS TRUE IF THE COMMAND IS ENABLED <<<

    CTX [CTX] - Context, just used for the command name
    """
    try:
        if ctx.guild:
            return json.load(open('json/servers.json'))[str(ctx.guild.id)]["com"][ctx.command.name] # Command is en/disabled
        else: # In DMs
            return True
    except: # Just in case
        return True
