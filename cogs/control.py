import discord
from discord.ext import commands


class Control_Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.get_cog("Config")
        self.queue = self.bot.get_cog("Queue")
        self.embed_generator = self.bot.get_cog("Embeds")

    # TODO: Use cog checks to check for role instead (If that's possible?)
    @commands.command()
    async def next(self, ctx):
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

    @commands.command(name="queue")
    async def queue_query(self, ctx):
        ta_role_id = int(self.config.get_server_config(
            ctx.author.guild.id, "ta_role_id"))
        is_ta = True if discord.utils.find(
            lambda role: role.id == ta_role_id, ctx.author.roles) else False
        if is_ta:
            if not ctx.author.guild.id in self.queue.queue:
                return await ctx.send("Nobody is in queue.")
            if len(self.queue.queue[ctx.author.guild.id]) == 0:
                return await ctx.send("Nobody is in queue.")
            waiting_list = ""
            for idx, member in enumerate(self.queue.queue[ctx.author.guild.id], start=1):
                waiting_list += f"{idx}. {member.name}\n"
            await ctx.send(f"Users in queue right now:\n```{waiting_list}```")

def setup(bot):
    bot.add_cog(Control_Panel(bot))
