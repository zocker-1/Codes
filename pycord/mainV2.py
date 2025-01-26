#Dies ist eine etwas fortgeschrittene Haupt Datei mit einer custom Start Nachricht

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from colorama import Fore, Style

# Lade die .env-Datei
load_dotenv()
TOKEN = os.getenv("Token")

# Erstelle die Intents mit allen Berechtigungen
intents = discord.Intents.all()

# Erstelle den Bot
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Hallo!")) #Bot Status festlegen
    # Daten sammeln
    execute_directory = os.getcwd()
    cogs_directory = os.path.join(execute_directory, 'cogs')
    cog_files_count = len([file for file in os.listdir(cogs_directory) if file.endswith('.py')])
    main_file_count = len(
        [file for file in os.listdir(execute_directory) if not os.path.isdir(os.path.join(execute_directory, file))])
    file_count = cog_files_count + main_file_count
    command_count = len(bot.commands)
    pycord_version = discord.__version__
    latency = bot.latency * 1000  # In Millisekunden umrechnen

    # Breite jeder Spalte definieren
    bot_name_width = max(len(bot.user.display_name), 16)
    version_width = max(len(pycord_version), 7)
    ping_width = max(len(f"{latency:.2f}ms"), 10)
    commands_width = max(len(str(command_count)), 9)
    files_width = max(len(str(file_count)), 6)

    # Gesamtbreite der Tabellenelemente definieren
    total_width = 2 + bot_name_width + 2 + version_width + 2 + ping_width + 2 + commands_width + 2 + files_width + 2
    line_width = total_width - 4  # Randzeichen an beiden Enden abziehen

    # Bot-Status ausgeben
    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + f"\n{bot.user} ist online und mit Discord verbunden!")
    print(Fore.WHITE + Style.BRIGHT + f"╭{'─' * line_width}╮" + Style.RESET_ALL)  # Obere Linie mit runden Ecken

    header = (Fore.WHITE + Style.BRIGHT + "│  " +
              Fore.RED + Style.BRIGHT + "Bot".ljust(bot_name_width) + "  " +
              Fore.YELLOW + "Version".ljust(version_width) + "  " +
              Fore.BLUE + "Ping".ljust(ping_width) + "  " +
              Fore.GREEN + "Befehle:".ljust(commands_width) + "  " +
              Fore.MAGENTA + "Dateien:".ljust(files_width) + "  │" + Style.RESET_ALL)

    print(header)

    bot_status = (Fore.WHITE + Style.BRIGHT + "│  " + Style.RESET_ALL +
                  Fore.RED + f"{bot.user.display_name}".ljust(bot_name_width) + "  " +
                  Fore.YELLOW + f"{pycord_version}".ljust(version_width) + "  " +
                  Fore.BLUE + f"{latency:.2f}ms".ljust(ping_width) + "  " +
                  Fore.GREEN + f"{command_count}".ljust(commands_width) + "  " +
                  Fore.MAGENTA + f"{file_count}".ljust(files_width) + "  │" + Style.RESET_ALL)

    print(bot_status)

    print(Fore.WHITE + Style.BRIGHT + f"╰{'─' * line_width}╯" + Style.RESET_ALL)  # Untere Linie mit runden Ecken


# Lade alle Cogs aus dem Ordner "cogs"
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Starte den Bot
if __name__ == "__main__":
    bot.run(TOKEN)
