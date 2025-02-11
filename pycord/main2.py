# Version 2
# Wenn du diese main2.py verwendest, entferne die 2 beim namen sodass diese main.py heißt
# Dies ist eine etwas fortgeschrittene Haupt Datei mit einer custom Start Nachricht

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from colorama import Fore, Style

load_dotenv()
TOKEN = os.getenv("Token")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    execute_directory = os.getcwd()
    cogs_directory = os.path.join(execute_directory, "cogs")
    
    cog_files_count = sum(
        [len(files) for _, _, files in os.walk(cogs_directory) if any(file.endswith(".py") for file in files)]
    )
    main_file_count = len(
        [file for file in os.listdir(execute_directory) if not os.path.isdir(os.path.join(execute_directory, file))]
    )
    file_count = cog_files_count + main_file_count
    command_count = len(bot.commands)
    pycord_version = discord.__version__
    latency = bot.latency * 1000  

    bot_name_width = max(len(bot.user.display_name), 16)
    version_width = max(len(pycord_version), 7)
    ping_width = max(len(f"{latency:.2f}ms"), 10)
    commands_width = max(len(str(command_count)), 9)
    files_width = max(len(str(file_count)), 6)

    total_width = 2 + bot_name_width + 2 + version_width + 2 + ping_width + 2 + commands_width + 2 + files_width + 2
    line_width = total_width - 4  

    print(Fore.LIGHTWHITE_EX + Style.BRIGHT + f"\n{bot.user} ist online und mit Discord verbunden!")
    print(Fore.WHITE + Style.BRIGHT + f"╭{'─' * line_width}╮" + Style.RESET_ALL)  

    header = (
        Fore.WHITE + Style.BRIGHT + "│  " +
        Fore.RED + "Bot".ljust(bot_name_width) + "  " +
        Fore.YELLOW + "Version".ljust(version_width) + "  " +
        Fore.BLUE + "Ping".ljust(ping_width) + "  " +
        Fore.GREEN + "Befehle:".ljust(commands_width) + "  " +
        Fore.MAGENTA + "Dateien:".ljust(files_width) + "  │" + Style.RESET_ALL
    )

    bot_status = (
        Fore.WHITE + Style.BRIGHT + "│  " + Style.RESET_ALL +
        Fore.RED + f"{bot.user.display_name}".ljust(bot_name_width) + "  " +
        Fore.YELLOW + f"{pycord_version}".ljust(version_width) + "  " +
        Fore.BLUE + f"{latency:.2f}ms".ljust(ping_width) + "  " +
        Fore.GREEN + f"{command_count}".ljust(commands_width) + "  " +
        Fore.MAGENTA + f"{file_count}".ljust(files_width) + "  │" + Style.RESET_ALL
    )

    print(header)
    print(bot_status)
    print(Fore.WHITE + Style.BRIGHT + f"╰{'─' * line_width}╯" + Style.RESET_ALL)  


async def load_cogs():
    base_path = "cogs"
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                relative_path = os.path.relpath(os.path.join(root, file), base_path)
                module = relative_path.replace(os.sep, ".")[:-3]  
                try:
                    await bot.load_extension(f"{base_path.replace(os.sep, '.')}.{module}")
                    print(Fore.GREEN + f"✅ Cog geladen: {module}" + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"❌ Fehler beim Laden von {module}: {e}" + Style.RESET_ALL)


async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
  
