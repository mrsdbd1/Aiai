import random
import logging
import subprocess
import sys
import os
import re
import time
import concurrent.futures
import discord
from discord.ext import commands, tasks
import docker
import asyncio
from discord import app_commands
from discord.ui import Button, View, Select
import string
from datetime import datetime, timedelta
from typing import Optional, Literal

TOKEN = ''
RAM_LIMIT = '6g'
SERVER_LIMIT = 10
database_file = 'database.txt'
PUBLIC_IP = '0.0.0.0'

# Admin user IDs - add your admin user IDs here
ADMIN_IDS = [1368602087520473140]  # Replace with actual admin IDs

# === /create Command ===
class RewardSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="🎉 Invite: 8 Invites = 16GB", value="invite_8"),
            discord.SelectOption(label="🎉 Invite: 15 Invites = 32GB", value="invite_15"),
            discord.SelectOption(label="🚀 Boost: 1 Boost = 16GB", value="boost_1"),
            discord.SelectOption(label="🚀 Boost: 2 Boost = 32GB", value="boost_2"),
        ]
        super().__init__(placeholder="Select your reward plan", options=options)

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]
        ram = 16000
        cpu = 40
        user = interaction.user
        member = interaction.guild.get_member(user.id)

        if value == "invite_8" and not await has_required_invites(user, 8):
            await interaction.response.send_message("❌ You need at least 8 invites to claim this reward.", ephemeral=True)
            return
        elif value == "invite_15" and not await has_required_invites(user, 15):
            ram = 32000
            await interaction.response.send_message("❌ You need at least 15 invites to claim this reward.", ephemeral=True)
            return
        elif value == "boost_1" and not has_required_boost(member, 1):
            await interaction.response.send_message("❌ You must boost the server to claim this reward.", ephemeral=True)
            return
        elif value == "boost_2" and not has_required_boost(member, 2):
            ram = 32000
            await interaction.response.send_message("❌ You must boost the server with 2 boosts.", ephemeral=True)
            return

        username = user.name.replace(" ", "_")
        container_name = f"VPS_{username}_{generate_random_string(6)}"
        expiry = format_expiry_date(parse_time_to_seconds("7d"))

        async def os_selected(interaction2, os_type):
            await deploy_with_os(interaction2, os_type, ram, cpu, str(user.id), str(user.id), container_name, expiry)

        embed = discord.Embed(
            title="📀 Select Operating System",
            description="✅ Verified! Now choose your preferred OS.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, view=OSSelectView(os_selected), ephemeral=True)

class RewardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(RewardSelect())

@bot.tree.command(name="create", description="🎁 Claim a VPS reward by invite or boost")
async def create(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎁 VPS Reward Claim",
        description="Select your reward type. Invite-based or Boost-based.",
        color=discord.Color.blurple()
    )
    await interaction.response.send_message(embed=embed, view=RewardView(), ephemeral=True)
