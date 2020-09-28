import discord
from discord.ext import commands


class Embeds(commands.Cog):
    async def generate_embed(self, current_user, next_user, in_progress: bool):
        """Generates an embed for queues that can be used directly in Context.send() calls.

        Args:
            current_user (str): Name of the user currently in office hours
            next_user (str): Name of the user up next
            in_progress (bool): Indicates whether or not office hours are currently in progress

        Returns:
            discord.Embed: The generated embed.
        """
        office_hours_status = "ongoing" if in_progress else "unavailable"
        embed = discord.Embed(colour=discord.Colour(
            0xf95069), description=f"Office hours are currently {office_hours_status}.")

        # embed.set_footer(text="This session will end at {}", icon_url="")

        embed.add_field(name="First In Line",
                        value=f"{current_user}", inline=True)
        embed.add_field(name="Next In Line",
                        value=f"{next_user}", inline=True)

        return embed

    # async def add_reactions(self, message):


def setup(bot):
    bot.add_cog(Embeds(bot))
