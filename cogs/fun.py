# -*- coding: utf-8 -*-
import random
from discord.ext import commands
import datetime

from cogs.tools import beanbase


class Fun(commands.Cog):
    """Fun commands"""

    def __init__(self, client: commands.Bot):
        self.client = client

    async def cog_check(self, ctx):

        if str(datetime.date.today().month) == "4":
            print("Date works")
            if str(datetime.date.today().day) == "1" or str(datetime.date.day) == "2":
                print("and so does the day :D")
                if random.randint(0, 1) == 1:
                    await ctx.send(random.choice(["No", "Heck off!", "Do it yourself", "Seems like effort", "Nah", "Not feeling like it", "How would you feel if I asked you constantly for stuff?"]))
                    return False
        return True

    @commands.command()
    async def Quote(self, ctx):
        """Get a random quote"""
        if str(datetime.date.today().month) == "4":
            print("Date works")
            if str(datetime.date.today().day) == "1" or str(datetime.date.day) == "2":
                print("and so does the day :D")
                await ctx.send("<https://i.kym-cdn.com/photos/images/facebook/001/693/395/974.png>")
                return

        quote = random.choice(beanbase.GetQuotes(str(ctx.guild.id)))
        await ctx.send(f"{quote[0]}\nAdded by {quote[1]}. Quote ID:{quote[2]}")

    @commands.command()
    async def AddQuote(self, ctx, quote: str):
        """Add a quote"""

        # This limits the number of quotes per server to 100, unless upgraded
        quote_amount = len(beanbase.GetQuotes(str(ctx.guild.id)))
        if quote_amount >= 100 and beanbase.GetServer(str(ctx.guild.id))["level"] < 2:
            await ctx.send("You have reached the 100 quote limit for normal servers. Im sorry for this, but disk "
                           "space isnt free :c")
            return
        beanbase.AddQuote(str(ctx.guild.id), str(ctx.author.display_name), quote)
        await ctx.send("Quote Added")

    @AddQuote.error
    async def AddQuote_eh(self, ctx, err: Exception):
        if str(err) != "The check functions for command Illegal failed.":
            await ctx.send("Something went wrong, I'm sorry :c")


def setup(client: commands.Bot):
    client.add_cog(Fun(client))
