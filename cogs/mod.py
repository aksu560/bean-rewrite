# -*- coding: utf-8 -*-
import io
from discord.ext import commands
import discord

from cogs.tools import beanbase


class Mod(commands.Cog):
    """Cog for server moderation"""

    def __init__(self, client: commands.Bot):
        self.client = client

    def cog_check(self, ctx):
        user = str(ctx.author.id)
        bot_admins = beanbase.GetBotAdmins()
        if user in bot_admins:
            return True
        if ctx.author.guild_permissions.administrator:
            return True
        return False

    @commands.command()
    async def ListQuotes(self, ctx):
        output_list = []
        quotes = beanbase.GetQuotes(str(ctx.guild.id))
        for line in quotes:
            output_list.append(f"{line[0]} added by {line[1]}")
        file_buffer = io.StringIO('\n'.join(output_list))
        await ctx.send(file=discord.File(fp=file_buffer, filename=f"{ctx.guild.name}-quotes.txt"))

    @commands.command()
    async def RemoveQuote(self, ctx, quote: str):
        """Remove a quote"""

        beanbase.RemoveQuote(str(ctx.guild.id), quote)
        await ctx.send("Quote Removed")

    @commands.command()
    async def AddCommand(self, ctx, command: str, content: str, help: str):
        """Add a custom command for the server"""
        server_commands = beanbase.GetCustomCommands(str(ctx.guild.id))
        server_level = beanbase.GetServer(str(ctx.guild.id))["level"]
        print(command)

        if " " in command:
            await ctx.send("No spaces in command names. How do I know whats the command, and what's the argument then?")
            return

        if server_commands:

            if server_level < 2 and len(server_commands) >= 10:
                await ctx.send("You are over your cap of 10 commands :c Sorry, but drive space isnt free.")
                return

            if command in server_commands:
                await ctx.send("Command already exists")
                return

            for client_command in self.client.commands:
                if client_command.name.capitalize() == command.capitalize():
                    await ctx.send("Command conflicts with a premade command")
                    return

        if beanbase.AddCustomCommand(ctx.guild.id, command.capitalize(), content, help):
            await ctx.send(f"Command &{command.capitalize()} has been added")
        else:
            await ctx.send("Something went wrong")

    @commands.command()
    async def RemoveCommand(self, ctx, command: str):
        """Remove a custom command"""
        response = beanbase.RemoveCustomCommand(str(ctx.guild.id), command.capitalize())

        if response is None:
            await ctx.send("There are no custom commands on this server.")
        if response is True:
            await ctx.send(f"Custom Command {command.capitalize()} has been removed.")
        if response is False:
            await ctx.send(f"No custom command {command.capitalize()} found.")

    @commands.command(brief="[tag someone]")
    async def AddServerAdmin(self, ctx, new_admin: discord.Member):
        """Add new server administrator"""
        success = beanbase.AddServerAdmin(str(ctx.guild.id), str(new_admin.id))
        if success:
            await ctx.send(f"User <@{new_admin.id}> added as a server level administrator.")
        else:
            await ctx.send(f"User <@{new_admin.id}> is already a server level administrator.")

    @commands.command(brief="[tag someone]")
    async def RemoveServerAdmin(self, ctx, removed_admin: discord.Member):
        """Add new server administrator"""
        success = beanbase.RemoveServerAdmin(str(ctx.guild.id), str(removed_admin.id))
        if success:
            await ctx.send(f"User <@{removed_admin.id}> server level administrative rights have been revoked.")
        else:
            await ctx.send(f"User <@{removed_admin.id}> is not a server level administrator.")


def setup(client: commands.Bot):
    client.add_cog(Mod(client))
