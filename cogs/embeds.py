import discord
from discord.ext import commands
import asyncio

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_messages = {}
        self.queue = bot.get_cog("Queue")
        self.control = bot.get_cog("Control")
        
    async def generate_embed(self, guild_id):
        """Generates an embed for queues that can be used directly in Context.send() calls.

        Args:
            guild_id (integer): ID of the guild to generate an embed for.

        Returns:
            discord.Embed: The generated embed.
        """
        # office_hours_status = "ongoing" if in_progress else "unavailable"
        embed = discord.Embed(colour=discord.Colour(
            0xf95069), description=f"Office hours queue:")

        # embed.set_footer(text="This session will end at {}", icon_url="")
        queue = await self.queue.padded_queue(guild_id)
        if len(queue) == 0:
            embed.add_field(name="Nobody in queue.", value="\u200b")
        
        for idx, member in enumerate(queue, 1):
            embed.add_field(value=str(idx) + ": " + member.name, name="\u200b", inline=True)
        return embed

    @commands.command(name="embed")
    async def send_embed(self, ctx):
        message = await ctx.send(embed=await self.generate_embed(ctx.guild.id))
        self.embed_messages[ctx.guild.id] =  message
        await self.add_reactions(message)
        def check(reaction, member):
            return reaction.message.id == message.id and (reaction.emoji == "🔳" 
                or reaction.emoji == "➡️") and member.bot == False
        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=check)
            # Remove user reaction
            await reaction.remove(user)
            if reaction.emoji == "➡️":
                await self.control.move_next_user(user)
                await self.update_embed(ctx.guild.id)
    
    async def update_embed(self, guild_id):
        if guild_id in self.embed_messages:
            embed_message = self.embed_messages[guild_id]
            await embed_message.edit(embed=await self.generate_embed(guild_id))

    async def add_reactions(self, message):
        await message.add_reaction("🔳")
        await message.add_reaction("➡️")


def setup(bot):
    bot.add_cog(Embeds(bot))

def teardown(bot):
    print("Clearing messages...")
    loop = asyncio.get_event_loop()
    for message in list(bot.get_cog("Embeds").embed_messages.values()):
        loop.run_until_complete(message.delete())
