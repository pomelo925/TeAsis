import asyncio
import discord
import logging
import os
import traceback
from discord import app_commands
from discord.ext import commands
from gtts import gTTS

logger = logging.getLogger(__name__)

class TTS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active_connections = {}
        
        # Force load Opus
        try:
            discord.opus.load_opus('/usr/lib/libopus.so.0')
            # logger.info("✅ Successfully loaded Opus codec")
        except Exception as e:
            logger.error(f"❌ Failed to load Opus codec: {e}")

    @app_commands.command(name="tts", description="語音播報系統 🔊")
    @app_commands.describe(
        text="我會播放你輸入的文字><",
        language="選擇語言 (預設: zh-tw)"
    )
    @app_commands.choices(language=[
        app_commands.Choice(name="繁體中文", value="zh-tw"),
        app_commands.Choice(name="簡體中文", value="zh-cn"),
        app_commands.Choice(name="English", value="en"),
        app_commands.Choice(name="日本語", value="ja"),
        app_commands.Choice(name="한국어", value="ko")
    ])
    async def tts(self, interaction: discord.Interaction, text: str, language: str = "zh-tw"):
        # 檢查使用者是否在語音頻道
        voice_state = interaction.user.voice
        if not voice_state or not voice_state.channel:
            embed = discord.Embed(
                title="❌ 無法使用 TTS",
                description="你必須先加入語音頻道才能使用這個功能！",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # 檢查文字長度
        if len(text) > 200:
            await interaction.response.send_message("❌ 文字太長了！請限制在 200 個字元以內。", ephemeral=True)
            return

        # 檢查文字內容
        if not text.strip():
            await interaction.response.send_message("❌ 請輸入要播放的文字！", ephemeral=True)
            return

        await interaction.response.send_message(f"🎵 正在生成語音: **{text}**")

        mp3_filename = f"tts_{interaction.user.id}_{interaction.id}.mp3"

        try:
            # Generate speech
            logger.info(f"Generating TTS for user {interaction.user}: {text[:50]}...")
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(mp3_filename)

            if not os.path.exists(mp3_filename):
                await interaction.followup.send("❌ 語音檔生成失敗，請稍後再試。", ephemeral=True)
                return

            file_size = os.path.getsize(mp3_filename)
            logger.info(f"Successfully generated TTS file: {mp3_filename}, size: {file_size} bytes")

            user_channel = voice_state.channel
            channel_id = user_channel.id

            # 檢查 bot 是否已連線到語音頻道
            vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

            if vc:
                if vc.channel.id != channel_id:
                    await vc.disconnect()
                    logger.info(f"Left voice channel: {vc.channel.name}")
                    vc = await user_channel.connect()
                    logger.info(f"Connected to new voice channel: {user_channel.name}")
                else:
                    logger.info(f"Bot already in same voice channel: {user_channel.name}")
            else:
                vc = await user_channel.connect()
                logger.info(f"Bot connected to voice channel: {user_channel.name}")

            self.active_connections[channel_id] = vc

            # FFmpeg 設定
            ffmpeg_options = {
                'options': '-hide_banner -loglevel error -vn',
                'executable': "/usr/bin/ffmpeg"
            }

            # 檢查是否正在播放其他音訊
            if vc.is_playing():
                vc.stop()
                await asyncio.sleep(0.5)

            audio_source = discord.FFmpegPCMAudio(mp3_filename, **ffmpeg_options)
            audio = discord.PCMVolumeTransformer(audio_source, volume=0.8)

            def after_playing(error):
                if error:
                    logger.error(f"Playback error: {error}")
                else:
                    logger.info(f"Audio file playback completed: {mp3_filename}")
                # Clean up file after playback
                asyncio.run_coroutine_threadsafe(
                    self._cleanup_file(mp3_filename, vc, interaction), 
                    self.bot.loop
                )

            vc.play(audio, after=after_playing)
            logger.info(f"Started playing audio file: {mp3_filename}")

            # 更新訊息
            embed = discord.Embed(
                title="🎵 正在播放",
                description=f"**內容:** {text}\n**語言:** {language}\n**頻道:** {user_channel.name}",
                color=discord.Color.green(),
                timestamp=interaction.created_at
            )
            embed.set_footer(text=f"由 {interaction.user.display_name} 請求")
            
            await interaction.edit_original_response(content=None, embed=embed)

        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            logger.error(traceback.format_exc())
            
            error_embed = discord.Embed(
                title="❌ TTS 錯誤",
                description="語音生成或播放時發生錯誤，請稍後再試。",
                color=discord.Color.red()
            )
            
            try:
                await interaction.edit_original_response(embed=error_embed)
            except:
                await interaction.followup.send(embed=error_embed, ephemeral=True)
            
            # 清理檔案
            try:
                if os.path.exists(mp3_filename):
                    os.remove(mp3_filename)
            except:
                pass

    @app_commands.command(name="stop", description="停止當前的語音播放")
    async def stop_tts(self, interaction: discord.Interaction):
        try:
            vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
            
            if not vc:
                await interaction.response.send_message("❌ Bot 目前沒有連線到任何語音頻道。", ephemeral=True)
                return
            
            if vc.is_playing():
                vc.stop()
                embed = discord.Embed(
                    title="⏹️ 已停止播放",
                    description="語音播放已停止。",
                    color=discord.Color.blue()
                )
                await interaction.response.send_message(embed=embed)
                logger.info(f"User {interaction.user} stopped voice playback")
            else:
                await interaction.response.send_message("❌ 目前沒有正在播放的語音。", ephemeral=True)
                
        except Exception as e:
            logger.error(f"Error stopping playback: {e}")
            await interaction.response.send_message("❌ 停止播放時發生錯誤。", ephemeral=True)

    @app_commands.command(name="leave", description="讓 Bot 離開語音頻道")
    async def leave_voice(self, interaction: discord.Interaction):
        try:
            vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
            
            if not vc:
                await interaction.response.send_message("❌ Bot 目前沒有連線到任何語音頻道。", ephemeral=True)
                return
            
            channel_name = vc.channel.name
            await vc.disconnect()
            
            # 清理連線記錄
            if vc.channel.id in self.active_connections:
                del self.active_connections[vc.channel.id]
            
            embed = discord.Embed(
                title="👋 已離開語音頻道",
                description=f"Bot 已離開 **{channel_name}**",
                color=discord.Color.blue()
            )
            await interaction.response.send_message(embed=embed)
            logger.info(f"User {interaction.user} made bot leave voice channel: {channel_name}")
            
        except Exception as e:
            logger.error(f"Error leaving voice channel: {e}")
            await interaction.response.send_message("❌ 離開語音頻道時發生錯誤。", ephemeral=True)

    async def _cleanup_file(self, filename: str, vc: discord.VoiceClient, interaction: discord.Interaction):
        """Clean up audio files and handle subsequent operations"""
        try:
            await asyncio.sleep(1)  # Ensure playback is complete
            
            # Delete audio file
            if os.path.exists(filename):
                os.remove(filename)
                logger.info(f"Cleaned up audio file: {filename}")
            
            # Bot stays in channel for a while then auto-leaves
            if vc.is_connected() and not vc.is_playing():
                await asyncio.sleep(10)  # Stay for 10 seconds
                if vc.is_connected() and not vc.is_playing():
                    await vc.disconnect()
                    logger.info("Bot automatically left voice channel")
                    
                    # Clean up connection records
                    if vc.channel.id in self.active_connections:
                        del self.active_connections[vc.channel.id]
                        
        except Exception as e:
            logger.error(f"Error during file cleanup: {e}")

# Bot setup
async def setup(bot: commands.Bot):
    await bot.add_cog(TTS(bot))
