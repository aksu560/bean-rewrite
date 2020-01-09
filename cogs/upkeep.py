import inspect

from discord.ext import commands
import discord
import sys
import os
from .tools import beanbase


class Upkeep(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    def cog_check(self, ctx):
        print(f"Upkeep command used by {ctx.author} in {ctx.channel.name}:{ctx.guild.name}")
        bot_admins = beanbase.GetBotAdmins()
        print(f"{ctx.author.id} in {str(bot_admins)}")
        return str(ctx.author.id) in bot_admins


    @commands.command()
    async def Reload(self, ctx):
        """Reload all the cogs"""
        reloadMessage = "Reloading cogs:```css\n"
        failedOne = False

        for cog in self.client.allCogs:
            try:
                self.client.unload_extension(cog)
                self.client.load_extension(cog)
                reloadMessage += f"{cog[4:]} - success\n"
            except Exception as err:
                failedOne = True
                reloadMessage += f"{cog[4:]} - failed\n"
                print(f"[reload] Failed to reload cog \"{cog}\" [{type(err).__name__}: {err}]")

        reloadMessage += "```"
        reloadMessage += "**Something's wrong!**" if failedOne == True else ""
        await ctx.send(reloadMessage)

    @commands.command()
    async def Restart(self, ctx):
        """Restart the bot"""
        await ctx.send("Restarting.")
        os.execv(sys.executable, ['python3'] + sys.argv)

    @commands.command()
    async def Die(self, ctx):
        """Kill the bot"""
        await ctx.send("Time for me to die :c")
        exit()

    @commands.command(brief="[channel/user ID] [message]")
    async def MessageTo(self, ctx, target: str, *, msg: str):
        """Send a custom message to any channel or user"""
        channel = self.client.get_channel(int(target))
        if channel is None:
            channel = await self.client.fetch_user(int(target))
        await channel.send(msg)

    @commands.command(brief="[tag someone]")
    async def AddBotAdmin(self, ctx, new_admin: discord.Member):
        """Add new bot administrator"""
        success = beanbase.AddBotAdmin(str(new_admin.id), str(ctx.author.id))
        if success:
            await ctx.send(f"User <@{new_admin.id}> added as a bot level administrator.")
        else:
            await ctx.send(f"User <@{new_admin.id}> is already a bot level administrator.")

    @commands.command(brief="[tag someone]")
    async def RemoveBotAdmin(self, ctx, removed_admin: discord.Member):
        """Add new bot administrator"""
        success = beanbase.RemoveBotAdmin(str(removed_admin.id), str(ctx.author.id))
        if success:
            await ctx.send(f"User <@{removed_admin.id}> bot level administrative rights have been revoked.")
        else:
            await ctx.send(f"User <@{removed_admin.id}> is not a bot level administrator.")

    @MessageTo.error
    async def MessageTo_eh(self, ctx: commands.Context, err: Exception):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} you forgot something... Baka...")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} invalid channel/user ID... Baka...")

    @commands.command()
    async def Sep(self, ctx):
        """Just sends some separating lines to the server console. Used for debugging"""
        print("-------")

    @commands.command()
    async def cr(self, ctx, target_func):
        print(globals())
        output = "```py\n"
        output += inspect.getsource(globals()[target_func])
        if len(output) > 2000:
            looping = True
            texts = []
            while looping:
                pos1 = output.find('\n', 1700, 1900)
                texts.append()
                output = output[pos1:]

                if len(output) < 1996:
                    looping = False

            print(len(texts))
            for i in texts:
                await ctx.send(i)
        else:
            await ctx.send(output + "```")

    @cr.error
    async def cr_eh(self, ctx, err: Exception):
        await ctx.send(f"```{str(err)}```")


def setup(client: commands.Bot):
    client.add_cog(Upkeep(client))
