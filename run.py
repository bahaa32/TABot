import discord
from discord.ext.commands import Bot
import configparser

# Initialize config
config = configparser.ConfigParser()
config.read("config.ini")

# Initialize bot and queue
client = Bot(command_prefix="!")
queue = []

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await update_channel(init=True) # Run update_channel with init=True to set
                                        # waiting_room_channel and queue_channel to either
                                            # None or a channel object
    # await fetch_waiting_users()

async def update_channel(channel_type:str="", init:bool=False):
    global queue_channel
    global waiting_room_channel
    # Get channel object from channel IDs
    if channel_type == "queue" or init:
        queue_channel = client.get_channel(config["Settings"].getint("QueueChannelId"))
    if channel_type == "waitingroom" or init:
        waiting_room_channel = client.get_channel(config["Settings"].getint("WaitingRoomId"))
    # Save config
    if not init:
        with open("config.ini", "w") as configfile:
            config.write(configfile)
    else:
        # Get users already in waiting room on start, in the order they were in
        global queue
        queue += waiting_room_channel.members


@client.event
async def on_voice_state_update(member, before, after):
    # If user wasn't in a channel then joined the waiting room, add to queue
    if before.channel == None and after.channel.id == waiting_room_channel.id:
        queue.append(member)
        try:
            await member.send(config["Locale"]["AddedToQueue"].format(position=len(queue)))
            # Forbidden is thrown when you try to DM a user that won't allow you to DM them
        except discord.Forbidden:
            # Only attempt to send fallback message if queue_channel is set
            if queue_channel != None:
                await queue_channel.send(config["Locale"]["DmBlocked"].format(mention=member.mention))

    # If user left waiting room channel, remove from queue
    elif before.channel.id == waiting_room_channel.id and after.channel == None:
        queue.remove(member)
        try:
            await member.send(config["Locale"]["RemovedFromQueue"].format(position=len(queue)))
        except discord.Forbidden:
            # Only attempt to send fallback message if queue_channel is set
            if queue_channel != None:
                await queue_channel.send(config["Locale"]["DmBlocked"].format(mention=member.mention))

@client.command()
async def setchannel(ctx, arg):
    # !setchannel queue
    if arg == "queue":
        config["Settings"]["QueueChannelId"] = str(ctx.channel.id)
        await update_channel(arg)
    # !setchannel waitingroom
    elif arg == "waitingroom":
        config["Settings"]["WaitingRoomId"] = str(ctx.author.voice.channel.id)
        await update_channel(arg)
    
# Start bot with token from config
client.run(config["Settings"]["Token"])
