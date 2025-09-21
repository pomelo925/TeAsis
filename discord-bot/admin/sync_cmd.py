import discord
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.has_permissions(administrator=True)
    async def sync_cmd(self, ctx):
        """Sync slash commands"""
        try:
            await ctx.send("🔄 [ADMIN] [INFO] Synchronizing slash commands...")
            synced = await self.bot.tree.sync()
            await ctx.send(f"✅ [ADMIN] [INFO] Successfully synced {len(synced)} slash commands")
            logger.info(f"Admin {ctx.author} synced slash commands")
        except Exception as e:
            await ctx.send(f"❌ [ADMIN] [ERROR] Sync failed: {str(e)}")
            logger.error(f"Error syncing slash commands: {e}")

    @commands.command(name="reload")
    @commands.has_permissions(administrator=True)
    async def reload_extension(self, ctx, extension_name: str = None):
        """Reload specified extension module"""
        if not extension_name:
            await ctx.send("❌ [ADMIN] [ERROR] Please specify the extension module name to reload")
            return
        
        try:
            await self.bot.reload_extension(extension_name)
            await ctx.send(f"✅ [ADMIN] [INFO] Successfully reloaded extension: {extension_name}")
            logger.info(f"Admin {ctx.author} reloaded extension: {extension_name}")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"❌ [ADMIN] [ERROR] Extension {extension_name} is not loaded")
        except commands.ExtensionNotFound:
            await ctx.send(f"❌ [ADMIN] [ERROR] Extension {extension_name} not found")
        except Exception as e:
            await ctx.send(f"❌ [ADMIN] [ERROR] Reload failed: {str(e)}")
            logger.error(f"Error reloading extension {extension_name}: {e}")

    @commands.command(name="status")
    @commands.has_permissions(administrator=True)
    async def status_cmd(self, ctx):
        """Display Bot status information"""
        embed = discord.Embed(
            title="🤖 Bot Status Information",
            color=discord.Color.blue(),
            timestamp=ctx.message.created_at
        )
        
        embed.add_field(
            name="📊 Basic Information",
            value=f"**Bot Name:** {self.bot.user.name}\n"
                  f"**Bot ID:** {self.bot.user.id}\n"
                  f"**Latency:** {round(self.bot.latency * 1000)}ms",
            inline=False
        )
        
        embed.add_field(
            name="🏠 Server Information",
            value=f"**Connected Servers:** {len(self.bot.guilds)}\n"
                  f"**Total Users:** {len(self.bot.users)}",
            inline=False
        )
        
        embed.add_field(
            name="🔧 Loaded Extensions",
            value="\n".join([f"• {ext}" for ext in self.bot.extensions.keys()]) or "None",
            inline=False
        )
        
        embed.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))