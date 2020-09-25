import discord
from discord.ext import commands

initial_extensions = [
    "cogs.config",
    "cogs.embed_generator",
    "cogs.embed_reaction",
    "cogs.queue",
    "cogs.setup"
    ]

# TODO: Change command prefix to be server-configurable
bot = commands.Bot(command_prefix="?", description="A bot to help TAs with queuing.")

@bot.event
async def on_ready():
    print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nDiscord.py Version: {discord.__version__}\n')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)
    token = bot.get_cog("Config").token
    bot.run(token, bot=True, reconnect=True)