# -*- coding: utf-8 -*-
import random
from discord.ext import commands
import datetime

from cogs.tools import beanbase


class Fun(commands.Cog):
    """Fun commands"""

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Quote(self, ctx):
        """Get a random quote"""
        print (datetime.date.today().day)
        if datetime.date.month == datetime.date.month(4):
            print("Date works")
            if datetime.date.day == 1 or datetime.date.day == 2:
                print("and so does the day :D")

        quote = random.choice(beanbase.GetQuotes(str(ctx.guild.id)))
        await ctx.send(f"{quote[0]}\nAdded by {quote[1]}. Quote ID:{quote[2]}")

    @commands.command()
    async def AddQuote(self, ctx, quote: str):
        """Add a quote"""

        quote_amount = len(beanbase.GetQuotes(str(ctx.guild.id)))
        if quote_amount >= 100 and beanbase.GetServer(str(ctx.guild.id))["level"] < 2:
            await ctx.send("You have reached the 100 quote limit for normal servers. Im sorry for this, but disk "
                           "space isnt free :c")
            return
        beanbase.AddQuote(str(ctx.guild.id), str(ctx.author.display_name), quote)
        await ctx.send("Quote Added")

    @AddQuote.error
    async def AddQuote_eh(self, ctx, err: Exception):
        await ctx.send("Something went wrong, I'm sorry :c")


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
