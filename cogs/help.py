# -*- coding: utf-8 -*-
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Help(self, ctx, targetcog: str = ""):
        """Is a very helpful command"""

        if targetcog == "":
            commandsText = f"Here are all the cogs available, please use &help [cogname] for" \
                           f" help with individual commands```css\n"

            for cog in self.client.allCogs:
                commandsText += f"{cog[4:]}\n"
        else:
            targetcogobject = self.client.get_cog(targetcog.capitalize())
            if targetcogobject is None:
                await ctx.send(f"{targetcog} was not found :c")
                return
            commandsText = f"Here are all the commands in {targetcogobject.qualified_name}```css"

            for command in targetcogobject.get_commands():
                commandsText += f"\n    &{command.name} "
                commandsText += f"{command.brief} " if command.brief is not None else ""
                commandsText += f"/* {command.help} */"

        # Cuts the output to multiple messages if the output would go over Discord's character limit
        if len(commandsText) > 2000:
            texts = []
            pos1 = commandsText.find('\n', 1700, 1900)
            texts.append(commandsText[:pos1] + "```")
            texts.append(f"```css\n{commandsText[pos1:]}```")
            for i in texts:
                await ctx.send(i)
        else:
            await ctx.send(commandsText + "```")


def setup(client: commands.Bot):
    client.add_cog(Help(client))
