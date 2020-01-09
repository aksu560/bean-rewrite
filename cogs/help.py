# -*- coding: utf-8 -*-
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command()
    async def Help(self, ctx: commands.Context):
        """Is a very helpful command"""
        commandsText = f"Here are all the cogs available, please use &help [cogname] for" \
                       f" help with individual commands```css\n"

        for cog in self.client.allCogs:
            commandsText += f".{cog}\n"

        # Cuts the output to multiple commands if the output would go over Discord's character limit
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