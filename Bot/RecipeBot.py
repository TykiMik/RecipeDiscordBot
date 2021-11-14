import discord
import configparser
import logging
from pymongo import MongoClient
from discord.ext import commands

# bot declaration
description = '''BME SoftwareArchitecture HomeWork
Recipe sharing discord bot.'''
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', description=description, intents=intents)
database = None


# Constants
CONFIG_FILE = "recipebotconfig.ini"
BOT_CHANNEL = None

def get_database():
    config_obj = configparser.ConfigParser()
    config_obj.read(CONFIG_FILE)

    database_config = config_obj['MongoDB']
    client = MongoClient(database_config['mongodb_address'])
    return client[database_config['database']]


@bot.event
async def on_message(message):
    if message.channel.name != BOT_CHANNEL:
        return

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == "__main__":
    config_obj = configparser.ConfigParser()
    config_obj.read(CONFIG_FILE)
    token = config_obj['DiscordBot']['token']
    BOT_CHANNEL = config_obj['DiscordBot']['channel']

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    database = get_database()
    bot.run(token)