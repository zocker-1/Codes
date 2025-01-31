# Version 1
# Wenn du main1.py verwendest, entferne die 1 sodass diese main.py heißt!
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Lade die .env-Datei
load_dotenv()

# Hole den Token aus der .env-Datei
TOKEN = os.getenv("Token")

# Erstelle die Intents mit allen Berechtigungen
intents = discord.Intents.all()

# Erstelle den Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Setze den Status
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Hallo!")) #Bot Status hier festlegen
    print(f"Eingeloggt als {bot.user}")

# Lade alle Cogs aus dem Ordner "cogs"
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Starte den Bot
if __name__ == "__main__":
    bot.run(TOKEN)
