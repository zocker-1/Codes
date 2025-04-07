# Version 2.1
# Genauso wie die main2.py nur mit besseren Fehler Meldungen
# Um diese main datei zu verwenden, entferne beim Namen 2-1 sodass die Datei nicht main2-1.py sondern main.py heißt
import discord
from discord.ext import commands
import os
import asyncio
import traceback
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
                module_path = os.path.join(root, file)
                relative_module = os.path.relpath(module_path, base_path).replace(os.sep, ".")[:-3]
                cog_name = f"{base_path}.{relative_module}"
                try:
                    await bot.load_extension(cog_name)
                    print(Fore.GREEN + f"✅ Cog geladen: {cog_name}" + Style.RESET_ALL)
                except Exception as e:
                    error_info = traceback.format_exc()
                    print(Fore.RED + f"❌ Fehler beim Laden von {cog_name}:\n{error_info}" + Style.RESET_ALL)


async def main():
    try:
        async with bot:
            await load_cogs()
            await bot.start(TOKEN)
    except Exception as e:
        error_info = traceback.format_exc()
        print(Fore.RED + f"❌ Schwerwiegender Fehler beim Start des Bots:\n{error_info}" + Style.RESET_ALL)


if __name__ == "__main__":
    asyncio.run(main())
