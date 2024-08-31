import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from fritzconnection.lib.fritzstatus import FritzStatus
import time

fc = FritzStatus(address="192.168.178.1", password="CHANGE_ME") # Change to your Fritz.Box password

# Discord-Bot-Token  https://discord.com/developers/applications
TOKEN = 'CHANGE_ME'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

channel_dict = {}

def get_traffic(fc):
    bytes_received = fc.bytes_received  # Downstream 
    bytes_sent = fc.bytes_sent          # Upstream 
    return bytes_received, bytes_sent

initial_received, initial_sent = get_traffic(fc)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="CHANGE_ME")) #Change Presence Status of your Bot
    try:
        await bot.tree.sync()
        print("Slash-Commands registered.")
    except Exception as e:
        print(f"Failed to register Slash-Commands: {e}")

@bot.tree.command(name='bandwidth', description='Starting monitoring bandwidth and traffic in this channel')
async def bandwidth(interaction: discord.Interaction):
    channel = interaction.channel
    server_id = interaction.guild.id

    channel_dict[server_id] = channel.id
    await interaction.response.send_message(f"Starting traffic surveillance {channel.mention}!")

    message = await channel.send("Waiting for traffic-data...")

    while True:
        download_bps, upload_bps = fc.transmission_rate

        download_kbps = download_bps / 1000
        upload_kbps = upload_bps / 1000

        current_received, current_sent = get_traffic(fc)
        received_since_start = (current_received - initial_received) / (1024**3)  # Downstream in GB
        sent_since_start = (current_sent - initial_sent) / (1024**3)              # Upstream in GB

        download_bar = create_progress_bar(download_kbps, 10000)
        upload_bar = create_progress_bar(upload_kbps, 10000)
        # There is a Bug in FritzBoxs API they unintentionally swapped upload and download speed
        download_color_code = ":red_circle: " if download_kbps > 1250 else "" # Red_circle if Upload is above 1250
        upload_color_code = ":red_circle: " if upload_kbps > 7500 else ""  # Red_circle if Download is above 7500 Kbit/s
        
        formatted_message = (
            f"Download: {upload_color_code}{upload_kbps:.2f} Kbit/s {upload_bar}\n"
            f"Upload: {download_color_code}{download_kbps:.2f} Kbit/s {download_bar}\n"
            f"Downstream traffic since Start: {received_since_start:.2f} GB\n"
            f"Upstream traffic since Start: {sent_since_start:.2f} GB"
        )

        await message.edit(content=formatted_message)

        await asyncio.sleep(1)

def create_progress_bar(value, max_value, bar_length=20):
    ratio = min(value / max_value, 1) 
    filled_length = int(bar_length * ratio)
    bar = f"[{'=' * filled_length}{'-' * (bar_length - filled_length)}]"
    return bar

bot.run(TOKEN)
