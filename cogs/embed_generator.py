import discord
from discord.ext import commands

class Embed_Generator(commands.Cog):
    async def generate_embed(self, in_progress: bool, current_student: str, next_student: str):
        office_hours_status = "ongoing" if in_progress else "unavailable"
        embed = discord.Embed(colour=discord.Colour(0xf95069), description=f"Office hours are currently {office_hours_status}.")

        # embed.set_footer(text="This session will end at {}", icon_url="")

        embed.add_field(name="Current Student", value=f"{current_student}", inline=True)
        embed.add_field(name="Next In Line", value=f"{next_student}", inline=True)

        return embed

def setup(bot):
    bot.add_cog(Embed_Generator(bot))