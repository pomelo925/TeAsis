import discord
import random
import logging
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)

class GameCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        # Different response messages
        self.pong_messages = [
            "大江大海江大海✓✓✓\n側楞著身子麼轉著回還☻☻☻\n♪♪♫一陣強力の間奏♫♫♪\n不會打歌麼學打歌!\n阿哥咋擺你咋擺▂▃▄",
            "🏓 Pong! Latency: {latency}ms",
            "🎮 Game started! Are you ready?",
            "⚡ Super fast response! Bot status is good!",
            "🎯 Target hit! Perfect shot!"
        ]

    @app_commands.command(name="pong", description="Classic Pong command - Test Bot response")
    async def pong(self, interaction: discord.Interaction):
        try:
            # Randomly select response message
            if random.random() < 0.3:  # 30% chance to show latency info
                latency = round(self.bot.latency * 1000)
                message = self.pong_messages[1].format(latency=latency)
            else:
                message = random.choice([self.pong_messages[0]] + self.pong_messages[2:])
            
            await interaction.response.send_message(message)
            logger.info(f"User {interaction.user} used pong command")
            
        except Exception as e:
            logger.error(f"Error executing pong command: {e}")
            await interaction.response.send_message("❌ An error occurred, please try again later.", ephemeral=True)

    @app_commands.command(name="ping", description="Check Bot's latency")
    async def ping(self, interaction: discord.Interaction):
        try:
            latency = round(self.bot.latency * 1000)
            
            embed = discord.Embed(
                title="🏓 Ping Test",
                color=discord.Color.green() if latency < 100 else discord.Color.orange() if latency < 200 else discord.Color.red(),
                timestamp=interaction.created_at
            )
            
            embed.add_field(
                name="📡 Latency Information",
                value=f"**WebSocket Latency:** {latency}ms\n"
                      f"**Status:** {'Excellent' if latency < 100 else 'Good' if latency < 200 else 'Slow'}",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed)
            logger.info(f"User {interaction.user} checked Bot latency: {latency}ms")
            
        except Exception as e:
            logger.error(f"Error executing ping command: {e}")
            await interaction.response.send_message("❌ An error occurred, please try again later.", ephemeral=True)

# Bot setup
async def setup(bot: commands.Bot):
    await bot.add_cog(GameCommands(bot))