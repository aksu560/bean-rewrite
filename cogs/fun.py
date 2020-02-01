# -*- coding: utf-8 -*-
from random import random
from discord.ext import commands

from cogs.tools import beanbase


class Fun(commands.Cog):
    """Fun commands"""

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Quote(self, ctx):
        """Get a random quote"""

        quote = random.choice(beanbase.GetQuotes(str(ctx.guild.id)))
        await ctx.send(f"{quote[0]}\nAdded by {quote[1]}")

    @commands.command()
    async def AddQuote(self, ctx, quote: str):
        """Add a quote"""

        beanbase.AddQuote(str(ctx.guild.id), str(ctx.author.nick), quote)
        await ctx.send("Quote Added")

    @AddQuote.error
    async def AddQuote_eh(self, ctx, err: Exception):
        await ctx.send("Something went wrong, I'm sorry :c")


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
