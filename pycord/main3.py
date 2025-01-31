import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()
TOKEN = os.getenv("Token")

# Setze alle Intents
intents = discord.Intents.all()

# Erstelle den Bot
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    """Lädt automatisch alle Cogs aus dem 'cogs'-Ordner."""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog {filename} geladen")
            except Exception as e:
                print(f"❌ Fehler beim Laden von {filename}: {e}")

@bot.event
async def on_ready():
    """Wird ausgeführt, wenn der Bot startet."""
    await bot.change_presence(activity=discord.CustomActivity("Hallo!"))  # Setzt den Status
    print(f"Eingeloggt als {bot.user}")

async def main():
    """Startet den Bot und lädt alle Cogs."""
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

# Starte den Bot
asyncio.run(main())
