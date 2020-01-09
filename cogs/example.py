# -*- coding: utf-8 -*-
from discord.ext import commands


class Example(commands.Cog):
    """This is an example cog, to be used as a base for creating your own. Do not load it."""

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Example(self, ctx, arg1: str):
        """Example command"""
        await ctx.send(arg1)


def setup(client: commands.Bot):
    client.add_cog(Example(client))
