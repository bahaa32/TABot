import discord
from discord.ext import commands
import configparser

class Config(commands.Cog):
    def __init__(self, bot):
        # Initialize config
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.token = self.config["Settings"]["Token"]

    # Just a wrapper for the config function, makes it a little more convient to use.
    def get_server_config(self, server_id, key):
        return self.config[str(server_id)][str(key)]

    # Takes tuple, unpacks and sets changes and saves them to local config
    def set_server_config(self, data: tuple):
        (server_id, key, value) = data
        try:
            self.config[str(server_id)]
        except KeyError:
            self.config[str(server_id)] = {}
        self.config[str(server_id)][str(key)] = str(value)
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
        return
    
    server_config = property(get_server_config, set_server_config)

def setup(bot):
    bot.add_cog(Config(bot))