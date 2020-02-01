# -*- coding: utf-8 -*-
import urllib
from urllib.error import HTTPError
from discord.ext import commands
from pyquery import PyQuery
from cogs.tools import shadownet_wiki
from fuzzywuzzy import fuzz


class Example(commands.Cog):
    """This cog has server specific commands, and only works on the specified servers."""

    def __init__(self, client: commands.Bot):
        self.client = client

    def cog_check(self, ctx):
        approved_guilds = [160034813040918528, 438287744683474947]
        return ctx.guild.id in approved_guilds

    @commands.command(brief="[Character Name]")
    async def Character(self, ctx, input: str = None):
        """Displays a shadownet characters wiki page"""
        async with ctx.channel.typing():

            # get all the characters and their wiki pages
            charlinks = shadownet_wiki.GetWikiCharacters()

            highestscore = 0
            highestname = ""

            # get all the keys in the character list
            for char in list(charlinks.keys()):
                # run fuzzysearch for input against the keys
                charscore = fuzz.partial_ratio(char.lower(), input.lower())

                # check if current character scores better than so far highest score
                if charscore > highestscore:
                    # storing the character name and their score
                    highestname = char
                    highestscore = charscore

            # Thank you to https://stackoverflow.com/a/18269491 for this
            try:
                url = f"http://www.shadownet.run{charlinks[highestname]}"
                fp = urllib.request.urlopen(url)
                mybytes = fp.read()
                mystr = mybytes.decode("utf8")
                fp.close()
                pq = PyQuery(mystr)
                output = ""

                # Checking if the character was made with the old or the new character form
                if pq('table.infobox'):
                    # Finding the character infobox
                    infobox = pq('table.infobox > tbody > tr')
                    output = highestname + "\n"
                    # Checking if the character has an image linked
                    try:
                        output += "http://www.shadownet.run" + pq(infobox).find('img').eq(0).attr('src') + "\n"
                    except TypeError:
                        pass
                    output += "```css\n"
                    # Iterate over every item in the box to get the name and value
                    for item in infobox:
                        name = pq(item).find('th').eq(0).text()
                        value = pq(item).find('td').eq(0).text()
                        # If neither of the values are empty, add it to the output
                        if name != "" and value != "":
                            output += "%s: %s\n" % (name, value)

                    output += "```"
                # There are different kinds of infoboxes for characters, this is to deal with them.
                elif pq('div.mw-parser-output'):
                    infobox = pq('div.mw-parser-output').find("table").eq(0)
                    infobox = infobox("tbody > tr")

                    # Everything from here is pretty much a repeat of the other case
                    try:
                        output += "http://www.shadownet.run" + pq(infobox).find('img').eq(0).attr('src') + "\n"
                    except TypeError:
                        pass
                    output += "```css\n"
                    for item in infobox:
                        name = pq(item).find('th').eq(0).text()
                        value = pq(item).find('td').eq(0).text()

                        if name != "" and value != "":
                            output += "%s: %s\n" % (name, value)
                    output += "```"

                    if output == "```css\n```":
                        output = "Character does not have an infobox on the wiki :c"

                else:
                    output = "Im sorry, I have no idea how to display this character. It has probably been created using " \
                             "one of the unsupported forms :c"
            except HTTPError:
                output = "Character not found! 💔"

            await ctx.send(output)

    @Character.error
    async def character_eh(self, ctx: commands.Context, err: Exception):
        await ctx.send("You didn't specify a character to look for :c")


def setup(client: commands.Bot):
    client.add_cog(Example(client))
