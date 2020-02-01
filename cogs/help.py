# -*- coding: utf-8 -*-
from discord.ext import commands
from cogs.tools import beanbase


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Help(self, ctx, target_cog: str = ""):
        """Is a very helpful command"""

        restricted_cogs = ["cogs.upkeep"]
        mod_cogs = ["cogs.mod"]
        custom_commands = beanbase.GetCustomCommands(str(ctx.guild.id))
        bot_admins = beanbase.GetBotAdmins()
        server_admins = beanbase.GetServerAdmins(str(ctx.guild.id))
        # We do this to simplify further code, as you cannot iterate over an empty list. The user ID is always
        # numeric, so text will never match
        if server_admins is None:
            server_admins.append("foo")

        if target_cog == "":
            commands_text = f"Here are all the cogs available, please use &Help [cogname] for" \
                            f" help with individual commands```css\n"

            for cog in self.client.allCogs:
                if cog in restricted_cogs:
                    if str(ctx.author.id) in bot_admins:
                        commands_text += f"{cog[4:]}\n"
                    else:
                        continue
                elif cog in mod_cogs:

                    if ctx.author.guild_permissions.administrator or str(ctx.author.id) in bot_admins or \
                            str(ctx.author.id) in server_admins:
                        commands_text += f"{cog[4:]}\n"
                else:
                    commands_text += f"{cog[4:]}\n"

            if custom_commands is not None:
                commands_text += ".custom\n"

        else:

            if target_cog.lower() == "custom":
                if custom_commands is not None:
                    commands_text = f"Here are all the commands in Custom```css"

                    for command in custom_commands:
                        commands_text += f"\n    &{command[1]} "
                        commands_text += f"/* {command[3]} */"

                else:
                    await ctx.send("There's no custom commands on this server.")

            else:
                if "cogs." + target_cog.lower() in restricted_cogs and str(ctx.author.id) not in bot_admins:
                    await ctx.send(">:c")
                    return

                target_cog_object = self.client.get_cog(target_cog.capitalize())
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


def setup(client: commands.Bot):
    client.add_cog(Help(client))
