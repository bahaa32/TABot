import discord
from discord.ext import commands


class Control_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = bot.get_cog("Queue")
        self.config = bot.get_cog("Config")
        self.control = bot.get_cog("Control_Panel")

    @commands.command()
    async def next(self, ctx):
        await self.control.move_next_user(ctx)

    @commands.command(name="queue")
    async def queue_query(self, ctx):
        guild_id = ctx.author.guild.id
        ta_role_id = int(self.config.get_server_config(
            guild_id, "ta_role_id"))
        is_ta = True if discord.utils.find(
            lambda role: role.id == ta_role_id, ctx.author.roles) else False
        if is_ta:
            queue = await self.queue.padded_queue(guild_id, response_size=-1)
            if len(queue) == 0:
                return await ctx.send("Nobody is in queue.")
            waiting_list = ""
            for idx, member in enumerate(queue, start=1):
                waiting_list += f"{idx}. {member.name}\n"
            await ctx.send(f"Users in queue right now:\n```{waiting_list}```")


def setup(bot):
    bot.add_cog(Control_Commands(bot))
