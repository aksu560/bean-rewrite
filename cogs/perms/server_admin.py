from discord.ext import commands
from ...tools import beanbase


def isServerAdmin(ctx: commands.Context):
    print(f"configuration command used by {ctx.author} in {ctx.channel.name}:{ctx.guild.name}")
    if ctx.author.guild_permissions.administrator or 'administrator' in beanbase.GetServerRoles(ctx.author, ctx.author):
        return True
    else:
        return False
