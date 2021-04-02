import discord
from discord.ext import commands


class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog("Config")
        self.queue = bot.get_cog("Queue")
        self.embed_generator = bot.get_cog("Embeds")

    # TODO: Use cog checks to check for role instead (If that's possible?)
    async def move_next_user(self, member):
        ta_role_id = int(self.config.get_server_config(
            member.guild.id, "ta_role_id"))
        ta_role = member.guild.get_role(ta_role_id)
        if ta_role in member.roles:
            next_user = self.queue.next(member.guild.id)
            for member in member.voice.channel.members:
                # Check if member is NOT a TA
                if ta_role not in member.roles:
                    await member.move_to(None, reason="Next!")
            if next_user != None:
                await next_user.move_to(member.voice.channel)
            else:
                await member.send("No more users in queue.")


def setup(bot):
    bot.add_cog(Control(bot))
