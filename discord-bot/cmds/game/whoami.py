import discord
import logging
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)

# 遊戲設定
WRONG_MESSAGE = "草你根本不了解我。"
CORRECT_BIRTHDAY = "9/25"
CORRECT_AGE = "25歲"
SUCCESS_MESSAGE = "你好了解我 >///< !!"

class WhoAmIGame:
    """Who Am I 遊戲的 UI 組件"""
    
    class RestartView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=300)  # 5分鐘超時

        @discord.ui.button(label="我想再認識一次!", style=discord.ButtonStyle.blurple, emoji="🔄")
        async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            try:
                await interaction.response.edit_message(
                    content="我們重新開始吧^_^！我的生日是幾號呢？",
                    view=WhoAmIGame.BirthdayView()
                )
                logger.info(f"User {interaction.user} restarted whoami game")
            except Exception as e:
                logger.error(f"Error restarting game: {e}")
                await interaction.response.send_message("❌ 發生錯誤，請稍後再試。", ephemeral=True)

        async def on_timeout(self):
            for item in self.children:
                item.disabled = True

    class AgeView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=300)
            ages = ["5歲", "15歲", "20歲", "25歲", "30歲"]
            for age in ages:
                button = discord.ui.Button(
                    label=age,
                    style=discord.ButtonStyle.secondary,
                    emoji="🎂"
                )
                button.callback = self.create_age_callback(age)
                self.add_item(button)

        def create_age_callback(self, age):
            async def age_callback(interaction: discord.Interaction):
                try:
                    if age == CORRECT_AGE:
                        embed = discord.Embed(
                            title="🎉 恭喜！",
                            description=SUCCESS_MESSAGE,
                            color=discord.Color.green(),
                            timestamp=interaction.created_at
                        )
                        embed.set_footer(text="感謝你陪我玩這個遊戲 💕")
                        await interaction.response.edit_message(content=None, embed=embed, view=None)
                        logger.info(f"User {interaction.user} completed whoami game")
                    else:
                        await interaction.response.edit_message(
                            content=WRONG_MESSAGE,
                            view=WhoAmIGame.RestartView()
                        )
                        logger.info(f"User {interaction.user} answered wrong in age stage")
                except Exception as e:
                    logger.error(f"Error during age selection: {e}")
                    await interaction.response.send_message("❌ 發生錯誤，請稍後再試。", ephemeral=True)
            return age_callback

        async def on_timeout(self):
            for item in self.children:
                item.disabled = True

    class BirthdayView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=300)
            birthdays = ["2/31", "4/6", "9/25", "13/1"]
            for date in birthdays:
                button = discord.ui.Button(
                    label=date,
                    style=discord.ButtonStyle.secondary,
                    emoji="🗓️"
                )
                button.callback = self.create_birthday_callback(date)
                self.add_item(button)

        def create_birthday_callback(self, date):
            async def birthday_callback(interaction: discord.Interaction):
                try:
                    if date == CORRECT_BIRTHDAY:
                        await interaction.response.edit_message(
                            content="哇！你竟然記得我的生日🥹 那你知道我幾歲嗎？",
                            view=WhoAmIGame.AgeView()
                        )
                        logger.info(f"User {interaction.user} answered correctly in birthday stage")
                    else:
                        await interaction.response.edit_message(
                            content=WRONG_MESSAGE,
                            view=WhoAmIGame.RestartView()
                        )
                        logger.info(f"User {interaction.user} answered wrong in birthday stage")
                except Exception as e:
                    logger.error(f"Error during birthday selection: {e}")
                    await interaction.response.send_message("❌ 發生錯誤，請稍後再試。", ephemeral=True)
            return birthday_callback

        async def on_timeout(self):
            for item in self.children:
                item.disabled = True

class WhoAmI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="whoami", description="柚子茶妹妹的真實身份?! 🍊")
    async def whoami(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="🤔 Who Am I?",
                description="想要了解我嗎？讓我們來玩個小遊戲吧！\n我的生日是幾號呢？",
                color=discord.Color.purple(),
                timestamp=interaction.created_at
            )
            embed.set_footer(text="選擇正確的日期來繼續遊戲！")
            
            await interaction.response.send_message(
                embed=embed,
                view=WhoAmIGame.BirthdayView()
            )
            logger.info(f"User {interaction.user} started whoami game")
            
        except Exception as e:
            logger.error(f"Error executing whoami command: {e}")
            await interaction.response.send_message("❌ 發生錯誤，請稍後再試。", ephemeral=True)

# Bot setup
async def setup(bot: commands.Bot):
    await bot.add_cog(WhoAmI(bot))