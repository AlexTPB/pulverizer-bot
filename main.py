import discord
import re
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

URL_REGEX = r"(https?://[^\s]+)"

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

@client.event
async def on_message(message):
    if not message.author.bot or not message.embeds:
        return

    links = []

    for embed in message.embeds:
        if embed.title:
            links += re.findall(URL_REGEX, embed.title)
        if embed.description:
            links += re.findall(URL_REGEX, embed.description)
        for field in embed.fields:
            links += re.findall(URL_REGEX, field.name)
            links += re.findall(URL_REGEX, field.value)

    unique_links = list(dict.fromkeys(links))

    if unique_links:
        for link in unique_links:
            await message.channel.send(link)

client.run(os.getenv("DISCORD_TOKEN"))
