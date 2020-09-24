import discord
from discord.ext import commands

class Setup(commands.Cog):
    def __init__(self, bot):
        self.config = bot.get_cog("Config")
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def setup(self, ctx, command, *, arg=None):
        """ Command which allows any user with admin permissions to
            set server-specific configuration."""
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You cannot execute this command.")
            return
        command = command.lower()
        # Responds to command !setup queue_chat
        if command == "queue_chat":
            # Set this server's queue_id to the channel the admin executed the command in
            self.config.server_config = (ctx.guild.id, "queue_id", ctx.channel.id)
            await ctx.send(f"Queue chat has been set to {ctx.channel.mention}")
        elif command == "waiting_room":
            await self.set_waiting_room(ctx)
        elif command == "ta_role":
            ta_role = discord.utils.find(lambda role: role.name == arg, ctx.guild.roles)
            if ta_role == None:
                await ctx.send(f'Cannot find role {arg}. Are you sure it exists?')
            else:
                self.config.server_config = (ctx.guild.id, "ta_role_id", ta_role.id)
                await ctx.send(f"TA role set to {discord.utils.escape_mentions(ta_role.name)}")
        else:
            await ctx.send("Unexpected argument. Valid arguments: `queue_chat`, `waiting_room`, `ta_role Role Name`.")
    
    async def set_waiting_room(self, ctx):
        voice_channel = ctx.author.voice
        if voice_channel == None:
            await ctx.send("You must be in a voice channel to set the waiting room!")
            return
        else:
            self.config.server_config = (ctx.guild.id, "waiting_voice_id", voice_channel.channel.id)
            await ctx.send(f"Set the waiting voice channel to `{voice_channel.channel.name}`.")

def setup(bot):
    bot.add_cog(Setup(bot))