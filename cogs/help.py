# -*- coding: utf-8 -*-
from discord.ext import commands
from cogs.tools import beanbase


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Help(self, ctx, target_cog: str = ""):
        """Is a very helpful command"""

        # Marking cogs we don't want to show to everyone
        restricted_cogs = ["cogs.upkeep"]
        mod_cogs = ["cogs.mod"]

        # Pull a list of the server's custom commands...
        custom_commands = beanbase.GetCustomCommands(str(ctx.guild.id))
        # bot level admins...
        bot_admins = beanbase.GetBotAdmins()
        # and server level admins.
        server_admins = beanbase.GetServerAdmins(str(ctx.guild.id))

        # We do this to simplify further code, as you cannot iterate over an empty list. The user ID is always
        # numeric, so text will never match.
        if server_admins is None:
            server_admins.append("foo")

        # If no target cog was specified, we simply show all cogs.
        if target_cog == "":
            commands_text = f"Here are all the cogs available, please use &Help [cogname] for" \
                            f" help with individual commands```css\n"

            for cog in self.client.allCogs:

                # Check if iterated cog is restricted to bot admins.
                if cog in restricted_cogs:
                    if str(ctx.author.id) in bot_admins:
                        commands_text += f"{cog[4:]}\n"
                    else:
                        continue

                # Check if iterated cog is restricted to server admins.
                elif cog in mod_cogs:
                    if ctx.author.guild_permissions.administrator or str(ctx.author.id) in bot_admins or \
                            str(ctx.author.id) in server_admins:
                        commands_text += f"{cog[4:]}\n"

                # If cog is not restricted, just print it.
                else:
                    commands_text += f"{cog[4:]}\n"

            # If there is custom commands, add a fake cog called custom to the end of the list
            if custom_commands is not None:
                commands_text += ".custom\n"

        # If a cog is specified, show the commands from target cog
        else:

            # If the target cot is custom, show custom commands
            if target_cog.lower() == "custom":
                if custom_commands is not None:
                    commands_text = f"Here are all the commands in Custom```css"

                    for command in custom_commands:
                        commands_text += f"\n    &{command[1]} "
                        commands_text += f"/* {command[3]} */"

                # If the server has no custom commands, send an error
                else:
                    await ctx.send("There's no custom commands on this server.")

            else:

                # If an unauthorized user tries to access a restricted cog, send an error message
                if "cogs." + target_cog.lower() in restricted_cogs and str(ctx.author.id) not in bot_admins:
                    await ctx.send(">:c")
                    return

                # Turn the target cog text into an actual cog object we can iterate over
                target_cog_object = self.client.get_cog(target_cog.capitalize())

                # If no cog is found, send an error message
                if target_cog_object is None:
                    await ctx.send(f"{target_cog} was not found :c")
                    return

                commands_text = f"Here are all the commands in {target_cog_object.qualified_name}```css"

                for command in target_cog_object.get_commands():
                    commands_text += f"\n    &{command.name} "
                    commands_text += f"{command.brief} " if command.brief is not None else ""
                    commands_text += f"/* {command.help} */"

        # Cuts the output to multiple messages if the output would go over Discord's character limit
        if len(commands_text) > 2000:
            texts = []
            pos1 = commands_text.find('\n', 1700, 1900)
            texts.append(commands_text[:pos1] + "```")
            texts.append(f"```css\n{commands_text[pos1:]}```")
            for i in texts:
                await ctx.send(i)
        else:
            await ctx.send(commands_text + "```")

    @commands.command()
    async def ServerInfo(self, ctx):
        server_admins = ""
        for admin in beanbase.GetServerAdmins(str(ctx.guild.id)):
            server_admins += f"{self.client.get_user(int(admin)).name}, "
        server_admins = server_admins[:-2]

        server_quotes = beanbase.GetQuotes(str(ctx.guild.id))
        if server_quotes == []:
            quote_status = "no"
        else:
            quote_status = str(len(server_quotes))

        if int(quote_status) == 1:
            quote_plural = "quote"
        else:
            quote_plural = "quotes"

        output = f"```css\n" \
                 f"Info about {ctx.guild.name}\n" \
                 f"Server Admins are: {server_admins}\n" \
                 f"This server has {quote_status} {quote_plural}```"

        await ctx.send(output)


def setup(client: commands.Bot):
    client.add_cog(Help(client))
