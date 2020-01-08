import discord
import configparser
import os

client = discord.Client()

client.cfgParser = configparser.ConfigParser()
auth = open(os.getcwd() + "/auth.ini")
client.cfgParser.read_file(auth)
clientKey = client.cfgParser.get("discord", "key")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(clientKey)