from discord.ext import commands
import configparser
import os
from cogs.tools import beanbase
import logging
import datetime
import random

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = commands.AutoShardedBot(command_prefix="&", help_command=None)
client.remove_command("help")

client.cfgParser = configparser.ConfigParser()
auth = open(os.getcwd() + "/auth.ini")
client.cfgParser.read_file(auth)
clientKey = client.cfgParser.get("discord", "key")

client.allCogs = [
    "cogs.help",
    "cogs.fun",
    "cogs.upkeep",
    "cogs.mod",
    "cogs.shadownet"
]


@client.event
async def on_ready():
    print("==== Booting Up ====")

    print("Loading cogs...")
    for cog in client.allCogs:
        try:
            client.load_extension(cog)
            print(f"Successfully loaded cog \"{cog}\"")
        except Exception as err:
            print(f"Failed to load cog \"{cog}\" [{type(err).__name__}: {err}]")

    print(f"-- Connected to {len(client.guilds)} servers:")
    for server in client.guilds:
        print(f":: {server.name}")
        if beanbase.GetServer(str(server.id)) is None:
            print("-Server not found in database, server added.")
            beanbase.AddServer(str(server.id))

    print("==== Boot Success! ====")


@client.event
async def on_message(msg):
    await client.process_commands(msg)


@client.event
async def on_guild_join(guild):
    print(f"Joined {guild.name}. Added to db.")
    beanbase.AddServer(str(guild.id))


@client.event
async def on_guild_remove(guild):
    print(f"Left {guild.name}. Removed from db")
    beanbase.RemoveServer((str(guild.id)))


@client.event
async def on_command(ctx):
    if str(datetime.date.today().month) == "4":
        print("Date works")
        if str(datetime.date.today().day) == "1" or str(datetime.date.day) == "2":
            print("and so does the day :D")
            if random.randint(0, 1) == 1:
                print("bamboozled")
                await ctx.send("No")
                return
            else:
                print("Not Bamboozled")


@client.event
async def on_command_error(ctx, error):
    command_from_msg = ctx.message.content[1:]
    custom_commands = beanbase.GetCustomCommands(str(ctx.guild.id))
    if custom_commands is None:
        print(error)
        return
    for command in custom_commands:
        if command_from_msg == command[1]:
            await ctx.send(command[2])
            return
    print(error)


client.run(clientKey)
