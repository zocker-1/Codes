# Ein einfaches Willkommen und Leave System in einem.
# In Zeile/Line 10 Kanal ID Einsetzen. Also 1234 gegen echte Kanal ID ersetzen

import discord
from discord.ext import commands

class WelcomeLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1234  # <- Ersetze mit deiner Channel-ID

    def count_real_members(self, guild: discord.Guild):
        return sum(1 for member in guild.members if not member.bot)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return  

        channel = member.guild.get_channel(self.channel_id)
        if channel:
            real_member_count = self.count_real_members(member.guild)
            embed = discord.Embed(
                title="Neues Mitglied!",
                description=(
                    f"Willkommen auf **{member.guild.name}**!\n"
                    f"Wir freuen uns, dass du hier bist!\n"
                    f"Du bist das **{real_member_count}**. Mitglied.\n"
                    f"Viel Spaß auf unserem Server."
                ),
                color=discord.Color.green()
            )
            await channel.send(content=member.mention, embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.bot:
            return  # Ignoriere Bots

        channel = member.guild.get_channel(self.channel_id)
        if channel:
            real_member_count = self.count_real_members(member.guild)
            embed = discord.Embed(
                title="Mitglied Verloren",
                description=(
                    f"{member.name} hat uns leider verlassen.\n"
                    f"Wir sind jetzt noch **{real_member_count}** Mitglieder."
                ),
                color=discord.Color.red()
            )
            await channel.send(content=member.mention, embed=embed)

async def setup(bot):
    await bot.add_cog(WelcomeLeave(bot))
