# -*- coding: utf-8 -*-
from discord.ext import commands
from cogs.tools import beanbase


class Mod(commands.Cog):
    """Cog for server moderation"""

    def __init__(self, client: commands.Bot):
        self.client = client

    def cog_check(self, ctx):
        bot_admins = beanbase.GetBotAdmins()
        return str(ctx.author.id) in bot_admins

    @commands.command()
    async def AddCommand(self, ctx, command: str, content: str, help: str):
        """Add a custom command for the server"""
        server_commands = beanbase.GetCustomCommands(str(ctx.guild.id))
        server_level = beanbase.GetServer(str(ctx.guild.id))["level"]

        if server_level < 2 and len(server_commands) > 10:
            await ctx.send("You are over your cap of 10 commands :c Sorry, but drive space isnt free.")
            return

        if command in server_commands:
            await ctx.send("Command already exists")

        if beanbase.AddCustomCommand(ctx.guild.id, command, content, help):
            await ctx.send(f"Command &{command} has been added")
        else:
            await ctx.send("Something went wrong")


def setup(client: commands.Bot):
    client.add_cog(Mod(client))
