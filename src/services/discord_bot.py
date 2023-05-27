from discord import Intents
from discord.ext.commands import Bot, Context

from core.config import settings
import services.smite as smite

bot = Bot(command_prefix=settings.discord_config.prefix, intents=Intents.all())


@bot.command()
async def hello(ctx: Context):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')


@bot.command()
async def player(ctx: Context, player_name: str = ''):
    if player_name == '':
        player_name = ctx.message.author.name
    await ctx.send(smite.get_player_info(player_name))


@bot.command()
async def match(ctx: Context, player_name: str = ''):
    if player_name == '':
        player_name = ctx.message.author.name
    await ctx.send(smite.get_player_math(player_name))
