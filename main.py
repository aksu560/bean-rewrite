import discord
from discord.ext import commands
import configparser
import os
from tools import beanbase

client = commands.AutoShardedBot(command_prefix="&")

client.cfgParser = configparser.ConfigParser()
auth = open(os.getcwd() + "/auth.ini")
client.cfgParser.read_file(auth)
clientKey = client.cfgParser.get("discord", "key")


client.allCogs = [
    "cogs.upkeep",
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


client.run(clientKey)
