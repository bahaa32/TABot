import discord
from discord.ext import commands


class Queue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_cog("Config")
        self.queue = {}
        self.voice_channel_cache = {}

    def next(self, guild_id):
        """Return next member in queue and remove them from it.

        Args:
            guild_id (integer): ID of the guild you want to fetch the member from.

        Returns:
            discord.py Member if the queue isn't empty, otherwise returns None.
        """
        if len(self.queue[guild_id]) == 0:
            return None
        return self.queue[guild_id].pop(0)

    # TODO: Beautify, this is kind of ugly
    async def padded_queue(self, guild_id, response_size: int=-1):
        """Returns an optionally padded array that's response_size long.

        Args:
            guild_id (integer): ID of the guild to retreive the queue of
            response_size (integer): Length of the list needed returns the whole
                queue if it is set to -1. Defaults to -1.

        Returns:
            list: The padded list.
        """
        queue_len = len(self.queue[guild_id])
        # Return response with "padding" according to requested
        # response size, might be useful for the future
        if not guild_id in self.queue or queue_len == 0:
            if response_size == -1:
                return []
            return [None] * response_size
        # If response size is greater than 0 and length of queue is bigger or equal to that,
        # only return requested size
        if response_size > 0:
            if queue_len >= response_size:
                return self.queue[guild_id][:response_size - 1]
            else:
                return self.queue[guild_id] + ([None] * (response_size - queue_len))
        elif response_size == -1:
            return self.queue[guild_id]

    # Get users already waiting in waiting rooms. Used when bot first starts up.
    @commands.Cog.listener()
    async def on_ready(self):
        """Runs when bot is ready. Fetches users in all waiting rooms and
            adds them to the relevant queues so that the queue and next commands
            are instantly ready for use.
        """
        for guild_id in self.config.parser.sections()[1:]:
            guild_id = int(guild_id)
            channel_id = int(self.config.get_server_config(
                guild_id, "waiting_voice_id"))
            channel = self.bot.get_channel(channel_id)
            if channel == None and channel_id != None:
                # TODO: Use a proper logger
                print("Invalid waiting channel! ID:", channel_id)
                continue
            self.queue.update({guild_id: channel.members})

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """https://discordpy.readthedocs.io/en/latest/api.html#discord.VoiceClient.on_voice_state_update

        Handles adding and removing members from queue.
        """
        voice_channel_id = self.config.get_server_config(
            member.guild.id, "waiting_voice_id")
        # TODO: Compare IDs directly since it's faster (if it won't break)
        if after.channel == self.get_voice_cached(voice_channel_id):
            await self.on_join(member)
        elif after.channel == None and member in self.queue[member.guild.id]:
            await self.on_leave(member)

    async def on_join(self, member):
        guild_id = member.guild.id
        if not guild_id in self.queue:
            self.queue[guild_id] = []
        # Doing this has multiple advantages, including not searching for the user again
        # and being consistent with the get_waiting_users function, since channel.members returns a list of `discord.Member`s
        # but it uses more memory
        self.queue[guild_id].append(member)

    async def on_leave(self, member):
        self.queue[member.guild.id].remove(member)

    # TODO: Maybe figure out another cleaner way to cache channels?
    def get_voice_cached(self, channel_id):
        """Looks for channel with ID and stores it in memory for the first call,
            but instantly returns cached channel from memory on any subsequent call.

        Args:
            channel_id: ID of the channel to be retreived

        Returns:
            Discord channel with ID channel_id, None if it doesn't exist.
        """
        channel_id = int(channel_id)
        if channel_id in self.voice_channel_cache:
            return self.voice_channel_cache[channel_id]
        else:
            channel = self.voice_channel_cache[channel_id] = self.bot.get_channel(
                channel_id)
            return channel


def setup(bot):
    bot.add_cog(Queue(bot))
