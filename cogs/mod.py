# -*- coding: utf-8 -*-
import io
from discord.ext import commands
import discord
import requests

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
            output_list.append(f"{line[0]} added by {line[1]}. Quote ID:{line[2]}")
        file_buffer = io.StringIO('\n'.join(output_list))
        await ctx.send(file=discord.File(fp=file_buffer, filename=f"{ctx.guild.name}-quotes.txt"))

    @commands.command()
    async def RemoveQuote(self, ctx, quote: int):
        """Remove a quote"""

        beanbase.RemoveQuote(str(ctx.guild.id), quote)
        await ctx.send("Quote Removed")

    @RemoveQuote.error
    async def RemoveQuote_eh(self, ctx, err: Exception):
        await ctx.send("Something went wrong :c")

    @commands.command(brief="[attach a text file, each quote on a new line]")
    async def ImportQuotes(self, ctx):
        """Import quotes in bulk"""
        attachment_url = ctx.message.attachments[0].url
        file_request = requests.get(attachment_url).text.split('\n')
        limit = None
        if beanbase.GetServer(str(ctx.guild.id))["level"] < 2:
            quote_amount = len(beanbase.GetQuotes(str(ctx.guild.id)))
            limit = 100-quote_amount
            print(limit)

        count = 0
        for quote in file_request:
            if limit is not None and count >= limit:
                break
            beanbase.AddQuote(str(ctx.guild.id), str(ctx.author.display_name), quote)
            count += 1
        await ctx.send(f"{count} quotes added!")

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

    @commands.command(brief="[Read the help text]")
    async def NukeQuotes(self, ctx, *, confirmation: str):
        """Deletes all Quotes"""
        if confirmation is None or confirmation != ctx.guild.name:
            await ctx.send("This command deletes all the quotes from the server. It has 2 safeguards built in. 1. "
                           "you have to give the name of the server as an argument for the command, and 2. It "
                           "dumps a list of all the ld quotes before deleting anything.")
        else:
            output_list = []
            quotes = beanbase.GetQuotes(str(ctx.guild.id))
            for line in quotes:
                output_list.append(f"{line[0]} added by {line[1]}. Quote ID:{line[2]}")
            file_buffer = io.StringIO('\n'.join(output_list))
            await ctx.send(file=discord.File(fp=file_buffer, filename=f"{ctx.guild.name}-quotes.txt"))
            for line in quotes:
                beanbase.RemoveQuote(str(ctx.server.id), line[2])
            await ctx.send("Quote's deleted")

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
