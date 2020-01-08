import discord
import configparser
import os

client = discord.Client()

client.cfgParser = configparser.ConfigParser()
auth = open(os.getcwd() + "/auth.ini")
client.cfgParser.read_file(auth)
clientKey = client.cfgParser.get("discord", "key")

client.allCogs = [
    "cogs.upkeep",
]


@client.event
async def on_ready():
    print("==== Starting to initialize ====")

    print("Loading cogs...")
    for cog in client.allCogs:
        try:
            client.load_extension(cog)
            print(f"Successfully loaded cog \"{cog}\"")
        except Exception as err:
            print(f"Failed to load cog \"{cog}\" [{type(err).__name__}: {err}]")

    print(f"-- Connected to {len(client.servers)} servers:")
    for server in client.servers:
        print(f":: {server.name}")

    print("==== Initialization success! ====")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(clientKey)
