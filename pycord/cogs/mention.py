import discord
import random
from discord.ext import commands

class MentionResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = [
            "Hat man mich gerufen? [Präfix: /]",
            "Wie kann ich helfen? [Präfix: /]",
            "Jemand hat nach mir verlangt? [Präfix: /]"
        ] # Lege Antworten fest, die der Bot sagen kann

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            response = random.choice(self.responses)
            msg = await message.channel.send(response)
            await msg.delete(delay=10)

def setup(bot):
   bot.add_cog(MentionResponse(bot))
