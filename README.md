# TABot

## Setup
- Go to your office hours queue channel and send `?setup queue_channel` in it.
- Join your waiting room voice channel and send `?setup waiting_room` in any channel.
- Add your TA's role by sending `?setup ta_role Role Name`. (For example: `?setup ta_role Teaching Assistants`)
- Done!

## Quick Start

### Self hosting
- Install `discord.py` if you haven't already (`pip install discord.py`)
- Insert your secret token into `config.ini` (If you don't have one, here's a [good guide](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token))
- Run `main.py`
- Invite your bot to your server
- Profit!

### Using the bot
- After setting the bot up, you can use the `?queue` command if you have the TA role to check which people are in queue and what order they're at
- Use the `?next` command to automatically disconnect all non-TA users and move in the next waiting user into the channel you're in.

## Features
- Queue automatically updates when the bot starts (users ordered in the order Discord reports them to the bot)
- Easy to configure (just 3 commands!)
- One instance can operate in multiple servers
- Does not require a database setup for people who want to self-host

## Known bugs
- (Not sure if that's desireable behavior) TAs are included in waiting lists if they join the waiting room.
- I don't know, you tell me? 😂
