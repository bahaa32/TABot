import discord
from discord.ext import commands


class Control_Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog("Config")
        self.queue = bot.get_cog("Queue")
        self.embed_generator = bot.get_cog("Embeds")

    # TODO: Use cog checks to check for role instead (If that's possible?)
    async def move_next_user(self, ctx):
        ta_role_id = int(self.config.get_server_config(
            ctx.author.guild.id, "ta_role_id"))
        ta_role = ctx.author.guild.get_role(ta_role_id)
        if ta_role in ctx.author.roles:
            next_user = self.queue.next(ctx.author.guild.id)
            for member in ctx.author.voice.channel.members:
                # Check if member is NOT a TA
                if ta_role not in member.roles:
                    await member.move_to(None, reason="Next!")
            if next_user != None:
                await next_user.move_to(ctx.author.voice.channel)
            else:
                await ctx.send("No more users in queue.")


def setup(bot):
    bot.add_cog(Control_Panel(bot))
