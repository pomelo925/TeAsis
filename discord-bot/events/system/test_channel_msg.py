# Required Configuration:
# 1. Set environment variable DISCORD_TOKEN with your bot token
# 2. The webhook URL is hardcoded in this file for the specific channel
# 3. No additional permissions or server membership required when using webhooks

import discord
from discord.ext import commands
import aiohttp
import os
import logging

logger = logging.getLogger(__name__)

# Constants
WEBHOOK_URL = "https://discord.com/api/webhooks/1419241764669100052/xZRuFrQ1vrEFVdKPOWERrYZYpyEj_4c4jVPb_ZGfWwnn4sOF3I3WdiR5gRYF6kjYRq0g"

class TestChannelMessage(commands.Cog):
    """Test cog to send a message to a specific Discord channel via webhook"""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def send_webhook_message(self, message: str, username: str = "Test Bot"):
        """Send a message using Discord webhook"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "content": message,
                    "username": username
                }
                
                async with session.post(WEBHOOK_URL, json=payload) as response:
                    if response.status == 204:
                        logger.info(f"✅ Webhook message sent successfully: {message}")
                        return True
                    else:
                        logger.error(f"❌ Webhook failed with status {response.status}: {await response.text()}")
                        return False
                        
        except aiohttp.ClientError as e:
            logger.error(f"❌ Network error sending webhook: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error sending webhook: {e}")
            return False
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Send test message when bot is ready"""
        await self.send_webhook_message("hello world!", "System Test Bot")
    
    @commands.command(name="testmsg")
    @commands.has_permissions(administrator=True)
    async def test_message_command(self, ctx, *, message: str = "hello world!"):
        """Manual command to send test message via webhook (Admin only)"""
        success = await self.send_webhook_message(message, f"Manual Test by {ctx.author.display_name}")
        
        if success:
            await ctx.send(f"✅ Webhook message sent: {message}")
        else:
            await ctx.send("❌ Failed to send webhook message")

async def setup(bot):
    """Setup function to load the cog"""
    await bot.add_cog(TestChannelMessage(bot))
