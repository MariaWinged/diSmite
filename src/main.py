from core.config import settings
from services.discord_bot import bot

if __name__ == '__main__':
    bot.run(settings.discord_config.token)
