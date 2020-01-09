from discord.ext import commands
import sys
import os


class Upkeep(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def reload(self, ctx):
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
    async def restart(self, ctx):
        """Restart the bot"""
        await ctx.send("Restarting.")
        os.execv(sys.executable, ['python3'] + sys.argv)


    @commands.command()
    async def die(self, ctx):
        """Kill the bot"""
        await ctx.send("Time for me to die :<")
        exit()

    @commands.command(brief="[channel/user ID] [message]")
    async def messageto(self, ctx, target: str, *, msg: str):
        """Send a custom message to any channel or user"""
        channel = self.client.get_channel(int(target))
        if channel is None:
            channel = await self.client.fetch_user(int(target))
        await channel.send(msg)

    @messageto.error
    async def messageTo_eh(self, ctx: commands.Context, err: Exception):
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} you forgot something... Baka...")
        elif isinstance(err, commands.CommandInvokeError):
            await ctx.send(f"{ctx.author.mention} invalid channel/user ID... Baka...")

    @commands.command()
    async def sep(self, ctx):
        """Just sends some separating lines to the server console. Used for debugging"""
        print("-------")


def setup(client: commands.Bot):
    client.add_cog(Upkeep(client))
