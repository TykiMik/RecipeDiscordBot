import discord
import configparser
import logging
from pymongo import MongoClient
from discord.ext import commands

# Constants
CONFIG_FILE = "recipebotconfig.ini"


def main():
    config_obj = configparser.ConfigParser()
    config_obj.read(CONFIG_FILE)
    token = config_obj['DiscordBot']['token']

    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    description = '''BME SoftwareArchitecture HomeWork Recipe sharing discord bot.'''
    intents = discord.Intents.default()
    bot = RecipeBot(command_prefix='!', description=description, intents=intents)
    bot.add_cog(BotCommands(bot))

    bot.run(token)


def get_database():
    config_obj = configparser.ConfigParser()
    config_obj.read(CONFIG_FILE)

    database_config = config_obj['MongoDB']
    client = MongoClient(database_config['mongodb_address'])
    return client[database_config['database']]


def create_recipe(creator, creator_id, recipe_name, content, tags):
    return {
        "creator": creator,
        "creator_id": creator_id,
        "name": recipe_name,
        "content": content,
        "tags": tags
    }


class BotCommands(commands.Cog, name='Command module for recipe bot'):
    def __init__(self, bot):
        database = get_database()
        config_obj = configparser.ConfigParser()
        config_obj.read(CONFIG_FILE)
        db_config = config_obj['MongoDB']

        self.recipes = database[db_config['recipes_collection']]
        self.bot = bot

    @commands.command(name="test")
    async def test_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command(name="upload_recipe")
    async def upload_recipe_command(self, ctx, name: str, content: str, *tags):
        query = {
            "creator": ctx.author.name,
            "name": name
        }
        stored_recipe = self.recipes.find_one(query)
        if stored_recipe is not None:
            await ctx.send(f'A recipe already stored as \"{ctx.author.name}\\{name}\"')
            return

        recipe = create_recipe(ctx.author.name, ctx.author.id, name, content, tags)

        self.recipes.insert_one(recipe)
        await ctx.send(f'Recipe added, request it anytime with !get_recipe \"{ctx.author.name}\\{name}\"')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send('I do not know that command?!')


class RecipeBot(commands.Bot):
    bot_channel = None

    async def on_ready(self):
        config_obj = configparser.ConfigParser()
        config_obj.read(CONFIG_FILE)
        bot_config = config_obj['DiscordBot']

        self.bot_channel = bot_config['channel']

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if self.user == message.author:
            return

        if message.channel.name != self.bot_channel:
            return

        await self.process_commands(message)


if __name__ == "__main__":
    main()