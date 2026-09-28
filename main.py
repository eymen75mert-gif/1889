import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN .env dosyasında bulunamadı.")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(
    command_prefix=".",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")


@bot.command()
@commands.has_permissions(administrator=True)
async def durum(ctx, *, yeni_durum: str):
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=yeni_durum)
    )

    await ctx.send(f"Durum değiştirildi: **{yeni_durum}**")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild is not None:
        try:
            await message.add_reaction("✅")
        except (discord.Forbidden, discord.HTTPException):
            pass

    await bot.process_commands(message)


@durum.error
async def durum_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu kullanmak için yönetici olmalısın.")


bot.run(TOKEN)
