import discord
from discord.ext import commands
import os
# Define the intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Replace with your user ID, private channel ID, and required role ID
YOUR_USER_ID = 720472929766211584
PRIVATE_CHANNEL_ID = 1183378760687423500
REQUIRED_ROLE_ID = 1363464294649565345  # <-- Replace this with your actual role ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    # Detect self-mute
    if before.self_mute == False and after.self_mute == True:
        # Check if the member has the required role
        required_role = discord.utils.get(member.roles, id=REQUIRED_ROLE_ID)
        if required_role is None:
            return  # Member doesn't have the role, so skip

        try:
            # Custom emojis from the server
            oliviagrinning_emoji = "<:egg:1362865122581942614>"
            cracked_egg_emoji = "<:cracked_egg:1362864847523676240>"

            # DM the member
            await member.send(f"Hey there! Olivia here! {oliviagrinning_emoji} You've cracked it! Here's your egg! {cracked_egg_emoji}")

            # Notify you (the bot owner)
            owner = await bot.fetch_user(YOUR_USER_ID)
            await owner.send(f"{member.display_name} just cracked an egg and muted themselves in {after.channel.name}! 🎉")

        except discord.errors.Forbidden:
            print(f"Could not DM {member.display_name}. They might have DMs disabled.")
            try:
                owner = await bot.fetch_user(YOUR_USER_ID)
                await owner.send(f"❌ Could not DM {member.display_name}, but they cracked an egg in {after.channel.name}.")
            except discord.errors.Forbidden:
                print(f"Could not DM you either. Check your DMs.")

        # Optional log in private channel
        channel = bot.get_channel(PRIVATE_CHANNEL_ID)
        if channel:
            await channel.send(f"<@{YOUR_USER_ID}> {member.display_name} just muted themselves in {after.channel.name}!")

bot.run(os.getenv("DISCORD_TOKEN"))
