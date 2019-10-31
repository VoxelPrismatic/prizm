from util import dbman
from util import priz_err as exc
def is_mod(ctx):
    if ctx.author == ctx.guild.owner or str(ctx.author) in dbman.get('mod', 'name', id=ctx.guild.id):
        return True
    raise exc.PrizmModeratorError
