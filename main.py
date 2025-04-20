import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

YOUR_USER_ID = 720472929766211584
PRIVATE_CHANNEL_ID = 1183378760687423500

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.self_mute == False and after.self_mute == True:
        try:
            # Emojis
            oliviagrinning_emoji = "<:egg:1362865122581942614>"
            cracked_egg_emoji = "<:cracked_egg:1362864847523676240>"

            # DM the user
            await member.send(f"Hey there! Olivia here! {oliviagrinning_emoji} You've cracked it! Here's your egg! {cracked_egg_emoji}")

            # DM you (the owner)
            owner = await bot.fetch_user(YOUR_USER_ID)
            await owner.send(f"{member.display_name} cracked an egg and muted in {after.channel.name}! 🎉")

        except discord.errors.Forbidden:
            print(f"Could not DM {member.display_name}.")
            try:
                owner = await bot.fetch_user(YOUR_USER_ID)
                await owner.send(f"❌ Could not DM {member.display_name}, but they cracked an egg in {after.channel.name}.")
            except:
                print(f"Also couldn't DM you, check DMs are open.")

        # Log in private channel
        channel = bot.get_channel(PRIVATE_CHANNEL_ID)
        if channel:
            await channel.send(f"<@{YOUR_USER_ID}> {member.display_name} muted in {after.channel.name}.")

# Run the bot with environment variable
bot.run(os.getenv("DISCORD_TOKEN"))
