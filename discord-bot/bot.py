import asyncio
import discord
import logging
import os
import traceback

from discord.ext import commands

# 設置日誌記錄
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Environment variables
intents = discord.Intents.default()
intents.message_content = True

# Instantiation
bot = commands.Bot(command_prefix="!", intents=intents)

# Login
@bot.event
async def on_ready():
    logger.info(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    logger.info(f"Discord.py version: {discord.__version__}")
    # logger.info(f"Connected to {len(bot.guilds)} servers")
    
    try:
        synced = await bot.tree.sync()
        logger.info(f"Successfully synced {len(synced)} slash commands")
    except Exception as e:
        logger.error(f"Error syncing slash commands: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Global command error handling"""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ Bot doesn't have sufficient permissions to execute this command!")
    else:
        logger.error(f"Unhandled error in command '{ctx.command}': {error}")
        logger.error(traceback.format_exc())
        await ctx.send("❌ An unknown error occurred, please try again later.")

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error):
    """Global slash command error handling"""
    logger.error(f"Error in slash command '{interaction.command}': {error}")
    logger.error(traceback.format_exc())
    
    if not interaction.response.is_done():
        await interaction.response.send_message("❌ An error occurred, please try again later.", ephemeral=True)
    else:
        await interaction.followup.send("❌ An error occurred, please try again later.", ephemeral=True)

async def load_extensions():
    """Load all extension modules"""
    extensions = [
        "admin.sync_cmd",
        "cmds.game.whoami",
        "cmds.game.pong",
        "cmds.voice.tts",
        "events.system.test_channel_msg"
    ]
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"✅ Extension: {extension}")
        except Exception as e:
            logger.error(f"❌ Failed to load extension {extension}: {e}")
            logger.error(traceback.format_exc())

async def main():
    """Main execution function"""
    logger.info("🚀 Launching Discord Bot...")
    
    # Check for Discord token first
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("❌ DISCORD_TOKEN environment variable not set")
        logger.info("💡 Please set your Discord bot token:")
        logger.info("   export DISCORD_TOKEN='your_bot_token_here'")
        return
    
    if len(token) < 50:  # Basic token length validation
        logger.error("❌ Invalid Discord token format (too short)")
        logger.info("💡 Make sure you're using the correct bot token from Discord Developer Portal")
        return
    
    # Load extension modules
    await load_extensions()
    
    # Start bot
    try:
        logger.info("🔐 Attempting to login with Discord token...")
        await bot.start(token)
    except discord.LoginFailure:
        logger.error("❌ Invalid Discord Token - Authentication failed")
        logger.info("💡 Please check your token at: https://discord.com/developers/applications")
    except discord.HTTPException as e:
        logger.error(f"❌ HTTP Error during login: {e}")
        logger.info("💡 This might be a network issue or rate limiting")
    except Exception as e:
        logger.error(f"❌ Bot startup failed: {e}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot has stopped running")