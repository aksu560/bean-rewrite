# -*- coding: utf-8 -*-
import random
import urllib
from urllib.error import HTTPError
from discord.ext import commands
from pyquery import PyQuery
from cogs.tools import shadownet_wiki
from cogs.tools.reddit import reddit
from fuzzywuzzy import fuzz
import math


class Shadownet(commands.Cog):
    """This cog has server specific commands, and only works on the specified servers."""

    def __init__(self, client: commands.Bot):
        self.client = client
        self.approved_guilds = [160034813040918528, 438287744683474947]

    def cog_check(self, ctx):

        return ctx.guild.id in self.approved_guilds

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

    @commands.command()
    async def Jobs(self, ctx):
        """View active jobs"""

        await ctx.send("This involves reddit stuff, so don't worry if it takes a while.")

        async with ctx.channel.typing():
            jobs = []
            for job in reddit.subreddit('shadownet').new(limit=None):
                if job.link_flair_text == "Job - Open":
                    jobs.append(job)
            jobAnnounce = f"{len(jobs)} jobs found."
            await ctx.send(jobAnnounce)

            for i in range(math.ceil(len(jobs) / 5)):
                jobListing = ""
                for listableJob in jobs[i * 5: i * 5 + 5]:

                    jobListing += f"{listableJob.title} by {listableJob.author.name}"

                    userflair = listableJob.author_flair_text
                    if userflair:
                        jobListing += f" <{userflair}>\n"
                    else:
                        jobListing += "\n"

                    jobListing += f"<{listableJob.url}>\n\n"

                await ctx.send(jobListing)

    @commands.command(brief="[Item]")
    async def illegal(self, ctx: commands.Context, *, item: str = ""):
        """Checks for legality of the specified thing"""

        async with ctx.channel.typing():

            if item == "":
                await self.client.reply(
                    "You do need to specify what to look for ya dumb dumb. If you were looking just "
                    "for the wiki page, here ya go <https://shadownet.run/Illegal_Things>")
                return

            address = "https://shadownet.run/Illegal_Things"

            fp = urllib.request.urlopen(str(address))
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            pq = PyQuery(mystr)

            table = pq("li")
            output = ""

            for hit in table:
                if fuzz.partial_ratio(str(hit.text).lower(), item.lower()) > 82:
                    output = str(hit.text)
                    break

            if output is not "":
                img = random.choice(["https://i.imgur.com/axlPKto.png", "https://i.kym-cdn.com/entries/icons/mobile/000/028/207/Screen_Shot_2019-01-17_at_4.22.43_PM.jpg"])
                await ctx.send(
                    f"{img}\n{output} is banned, sorry :c. Here is a link to the page of illegal things <{address}>")

            else:
                await ctx.send(f"{item} is cool! Here is a link to the page of illegal things <{address}>")

    @illegal.error
    async def illegal_eh(self, ctx: commands.Context, err):
        await ctx.send("Ok, how? Something has gone terribly wrong here, please alert Aksu#1010")


def setup(client: commands.Bot):
    client.add_cog(Shadownet(client))
