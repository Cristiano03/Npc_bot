import discord
import os
from Backend.shared import query_ollama

# Usa variabile d'ambiente per il token
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")

if not DISCORD_TOKEN:
    print("⚠️  DISCORD_TOKEN non configurato. Il bot Discord non verrà avviato.")
    print("   Imposta la variabile d'ambiente DISCORD_TOKEN per abilitare il bot Discord.")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connesso come {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != "re-aedryan":
        return

    user_input = message.content.strip()
    if not user_input:
        return

    await message.channel.typing()
    reply = query_ollama(user_input)
    await message.channel.send(reply)

client.run(DISCORD_TOKEN)
