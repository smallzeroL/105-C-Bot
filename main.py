import asyncio
import sys
from datetime import timedelta
import discord
import os
from discord import app_commands, Intents
from discord.ext import commands
from dotenv import load_dotenv

BOT_ACT = "105°C的你,滴滴情純的蒸餾水"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True

# 指令前墜(之後版本更新會用)
bot = commands.Bot(command_prefix='!', intents=intents)

# BAN
@bot.tree.command(name="ban", description="封鎖指定使用者（僅限管理員）")
@app_commands.describe(user="要封鎖的使用者", reason="封鎖原因")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = None):

    if not interaction.user.guild_permissions.administrator: # 檢測是否有管理員權限
        return await interaction.response.send_message("你沒有權限執行這個指令。", ephemeral=True) # 死屁孩沒權限還想用會看到的

    try:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"{user.mention} 已被封鎖。原因：{reason}") # 成功
    except discord.Forbidden:
        await interaction.response.send_message(f"無法封鎖 {user.mention}，可能是權限問題。", ephemeral=True) # 服主沒搞好權限(大部分都這樣)
    except discord.HTTPException:
        await interaction.response.send_message(f"封鎖 {user.mention} 時發生錯誤。", ephemeral=True) # 回報我錯誤訊息吧@@

# KICK
@bot.tree.command(name="kick", description="踢出指定使用者（僅限管理員）")
@app_commands.describe(user="要踢出的使用者", reason="踢出的原因")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = None):

    if not interaction.user.guild_permissions.administrator: # 檢測是否有管理員權限
        return await interaction.response.send_message("你沒有權限執行這個指令。", ephemeral=True) # 死屁孩沒權限還想用會看到的

    try:
        await user.kick(reason=reason)
        await interaction.response.send_message(f"{user.mention} 已被踢出伺服器。原因：{reason}")  # 成功
    except discord.Forbidden:
        await interaction.response.send_message(f"無法踢出 {user.mention}，可能是權限問題。", ephemeral=True) # 服主沒搞好權限(大部分都這樣)
    except discord.HTTPException:
        await interaction.response.send_message(f"踢出 {user.mention} 時發生錯誤。", ephemeral=True) # 回報我錯誤訊息吧@@

# MUTE
@bot.tree.command(name="mute", description="對指定使用者進行暫時禁言（僅限管理員）")
@app_commands.describe(user="要禁言的使用者", duration="禁言持續時間（秒）", reason="禁言原因")
async def mute(interaction: discord.Interaction, user: discord.Member, duration: int, reason: str = None):

    if not interaction.user.guild_permissions.administrator: # 檢測是否有管理員權限
        return await interaction.response.send_message("你沒有權限執行這個指令。", ephemeral=True) # 死屁孩沒權限還想用會看到的

    try:
        until_time = discord.utils.utcnow() + timedelta(seconds=duration)
        await user.timeout(until_time, reason=reason)
        await interaction.response.send_message(f"{user.mention} 已被禁言 {duration} 秒。原因：{reason}") # 成功

    except discord.Forbidden:
        await interaction.response.send_message(f"無法禁言 {user.mention}，可能是權限問題。", ephemeral=True) # 服主沒搞好權限,或禁言對象是管理員(大部分都這樣)
    except discord.HTTPException:
        await interaction.response.send_message(f"禁言 {user.mention} 時發生錯誤。", ephemeral=True) # 回報我錯誤訊息吧@@

# READY
@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print("指令已經準備好進♂去♂你的Bot帳號了🥵🥵")

        # 設置 Bot 活動狀態：正在觀看 BOT_ACT
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=BOT_ACT
        )
        await bot.change_presence(status=discord.Status.online, activity=activity)
        print(f"程式碼順利進♂入♂你的Bot帳號🥵")

    except Exception as e:
        print(f"Error during command sync: {e}")

# TOKEN
load_dotenv("TOKEN.env")
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)
