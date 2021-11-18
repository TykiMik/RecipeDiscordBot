import discord
import configparser
import logging
import uuid
import io
import json

from pymongo import MongoClient
from discord.ext import commands
from pathlib import Path
from statistics import mean, StatisticsError

# Constants
CONFIG_FILE = "recipebotconfig.ini"
TMP_DIR = Path("./tmp")


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


class BotCommands(commands.Cog, name='Command module for recipe bot'):
    def __init__(self, bot):
        database = get_database()
        config_obj = configparser.ConfigParser()
        config_obj.read(CONFIG_FILE)
        db_config = config_obj['MongoDB']

        self.recipes = database[db_config['recipes_collection']]
        self.bot = bot

    @commands.command(name="upload_recipe")
    async def upload_recipe_command(self, ctx, name: str, content: str, *tags):
        query = {
            "creator": f"{ctx.author.name}#{ctx.author.discriminator}",
            "name": name
        }
        stored_recipe = self.recipes.find_one(query)
        if stored_recipe is not None:
            await ctx.send(f'There is a recipe already stored as \"{ctx.author.name}#{ctx.author.discriminator}\\{name}\"')
            return

        recipe = self.create_recipe(f"{ctx.author.name}#{ctx.author.discriminator}", ctx.author.id, name, content, tags)

        self.recipes.insert_one(recipe)
        await ctx.send(f'Recipe added, request it anytime with !get_recipe \"{ctx.author.name}#{ctx.author.discriminator}\\{name}\"')

    @commands.command(name="upload_recipe_file")
    async def upload_recipe_file_command(self, ctx, *tags):
        if (number_of_messages := len(ctx.message.attachments)) > 0:
            if number_of_messages > 1:
                await ctx.send('Use only a single text file when uploading a recipe as a file!')
                return
            recipe_file = ctx.message.attachments[0]
            if "text/plain" in recipe_file.content_type:
                if recipe_file.size > 64_000:
                    await ctx.send('Maximum recipe file size exceeded! (max. 64 KB)')
                    return

                tmp_filename = Path(TMP_DIR, str(uuid.uuid4().hex))
                await recipe_file.save(fp=tmp_filename)
                with open(tmp_filename) as f:
                    file_content = f.read()
                    split_content = file_content.split('\n', 1)
                    name = split_content[0]
                    content = split_content[1]
                tmp_filename.unlink()

                query = {
                    "creator": f"{ctx.author.name}#{ctx.author.discriminator}",
                    "name": name
                }
                stored_recipe = self.recipes.find_one(query)
                if stored_recipe is not None:
                    await ctx.send(f'There is a recipe already stored as \"{ctx.author.name}\\{name}\"')
                    return
                else:
                    self.recipes.find_one_and_update(query, {'$inc': {'request_count': 1}})

                stored_recipe = self.recipes.find_one(query)
                if stored_recipe is not None:
                    await ctx.send(f'There is a recipe already stored as \"{ctx.author.name}\\{name}\"')
                    return

                recipe = self.create_recipe(f"{ctx.author.name}#{ctx.author.discriminator}", ctx.author.id, name, content, tags)

                self.recipes.insert_one(recipe)
                await ctx.send(f'Recipe added, request it anytime with !get_recipe \"{ctx.author.name}\\{name}\"')
            else:
                await ctx.send('Recipe file must be a text/plain document!')
                return

    @commands.command(name="get_recipe")
    async def get_recipe_command(self, ctx, extended_name, private: bool = False, file: bool = False):
        (creator, name) = extended_name.split('\\')
        query = {
            "creator": creator,
            "name": name
        }
        stored_recipe = self.recipes.find_one(query)
        if stored_recipe is None:
            await ctx.send(f'Sorry I couldn\'t find any recipe as \"{extended_name}\"')
            return
        else:
            self.recipes.find_one_and_update(query, {'$inc': {'request_count': 1}})

        if not file:
            response = self.create_recipe_message(
                stored_recipe['creator'],
                stored_recipe['name'],
                stored_recipe['content'],
                stored_recipe['tags'],
                stored_recipe['request_count'],
                stored_recipe['ratings']
            )
            if not private:
                await ctx.send(embed=response)
            else:
                await ctx.author.send(embed=response)
        else:
            response = self.create_recipe_file(
                stored_recipe['creator'],
                stored_recipe['name'],
                stored_recipe['content'],
                stored_recipe['tags'],
                stored_recipe['request_count'],
                stored_recipe['ratings']
            )
            file_name = stored_recipe['name'].replace(' ', '_')
            if not private:
                await ctx.send(file=discord.File(response, f'{file_name}.txt'))
            else:
                await ctx.author.send(file=discord.File(response, f'{file_name}.txt'))

    @commands.command(name="search_recipe")
    async def search_recipe_command(self, ctx, *filters):
        query = {}
        for query_filter in filters:
            (key, filter_value) = query_filter.strip().split('=')
            if len(filter_value) == 0:
                continue

            if key == 'name':
                filter_value_array = filter_value.split(',')
                query['name'] = {"$regex": "|".join(filter_value_array), "$options": 'i'}
            elif key == 'creator':
                query['creator'] = {"$regex": filter_value, "$options": 'i'}
            elif key == 'tags':
                filter_value = filter_value.replace(' ', '_')
                filter_value_array = filter_value.split(',')
                query['tags'] = {"$all": filter_value_array}
            elif key == 'ingredient':
                filter_value_array = filter_value.split(',')
                query['content'] = {"$regex": "|".join(filter_value_array), "$options": 'i'}
            elif key == 'popularity':
                query['request_count'] = {"$gte": int(filter_value)}  # TODO: lte?
            elif key == 'ratings':
                query['ratings'] = {"$gte": float(filter_value)}  # TODO: lte?

        results = list(self.recipes.find(query))
        if len(results) == 0:
            await ctx.send(f'There are no recipes matching your search criteria!')
            return
        result_recipe_names = []
        for r in results:
            try:
                result_recipe_names.append(f"\"{r['creator']}\\{r['name']}\" (Popularity: {str(r['request_count'])}, Avg. rating: {str(mean(r['ratings']))})")
            except StatisticsError:
                result_recipe_names.append(f"\"{r['creator']}\\{r['name']}\" (Popularity: {str(r['request_count'])}, Avg. rating: No ratings yet)")

        result_str = "\n".join(result_recipe_names)
        await ctx.send(f'I found these:\n{result_str}')

    @commands.command(name="tag")
    async def tag_command(self, ctx, extended_name, *tags):
        (creator, name) = extended_name.split('\\')
        if f"{ctx.author.name}#{ctx.author.discriminator}" != creator:
            ctx.send(f'You can only add tags to your own recipes!')
            return
        query = {
            "creator_id": ctx.author.id,
            "name": name
        }
        tags = map(lambda x: x.replace(' ', '_'), tags)
        if self.recipes.find_one_and_update(query, {'$push': {'tags': {'$each': tags}}}) is None:
            await ctx.send(f'Sorry I couldn\'t find any recipe as \"{extended_name}\"')
            return
        await ctx.send(f'I added the tags [{", ".join(tags)}] to the recipe \"{extended_name}\".')

    @commands.command(name="untag")
    async def untag_command(self, ctx, extended_name, *tags):
        (creator, name) = extended_name.split('\\')
        if f"{ctx.author.name}#{ctx.author.discriminator}" != creator:
            ctx.send(f'You can only remove tags from your own recipes!')
            return
        query = {
            "creator_id": ctx.author.id,
            "name": name
        }
        tags = map(lambda x: x.replace(' ', '_'), tags)
        if self.recipes.find_one_and_update(query, {'$pullAll': {'tags': tags}}) is None:
            await ctx.send(f'Sorry I couldn\'t find any recipe as \"{extended_name}\"')
            return
        await ctx.send(f'I removed the tags [{", ".join(tags)}] from the recipe \"{extended_name}\".')

    @commands.command(name="untag_all")
    async def untag_all_command(self, ctx, extended_name):
        (creator, name) = extended_name.split('\\')
        if f"{ctx.author.name}#{ctx.author.discriminator}" != creator:
            ctx.send(f'You can only remove tags from your own recipes!')
            return
        query = {
            "creator_id": ctx.author.id,
            "name": name
        }
        if self.recipes.find_one_and_update(query, {'$set': {'tags': []}}) in None:
            await ctx.send(f'Sorry I couldn\'t find any recipe as \"{extended_name}\"')
            return
        await ctx.send(f'I removed all tags from the recipe \"{extended_name}\".')

    @commands.command(name="rate")
    async def rate(self, ctx, extended_name, rating):
        (creator, name) = extended_name.split('\\')
        query = {
            "creator": creator,
            "name": name
        }
        if (r := self.recipes.find_one_and_update(query, {'$push': {'ratings': int(rating)}})) is None:
            await ctx.send(f'Sorry I couldn\'t find any recipe as \"{extended_name}\"')
            return
        await ctx.send(f'You have rated \"{extended_name}\" {rating}/5. Its new average rating is: {mean(r["ratings"])}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandNotFound):
            await ctx.send('I do not know that command?!')

    @staticmethod
    def create_recipe(creator, creator_id, recipe_name, content, tags):
        return {
            "creator": creator,
            "creator_id": creator_id,
            "name": recipe_name,
            "content": content,
            "tags": tags,
            "request_count": 0,
            "ratings": []
        }

    @staticmethod
    def create_recipe_file(creator, name, content, tags, request_count, ratings):
        text = f'''
        {creator}
        
        {name}
        
        Recipe:
        {content}
        
        Tags:
        {tags}
        
        Popularity:
        {request_count}
        
        Avg. rating:
        {str(mean(ratings)) if len(ratings) > 0 else 'No ratings yet'}'''

        return io.StringIO(text)

    @staticmethod
    def create_recipe_message(creator, name, content, tags, request_count, ratings):
        embed = discord.Embed(
            title=name,
            color=discord.Color.blurple()
        )
        embed.set_author(name=creator)
        embed.add_field(name="**Recipe**", value=content, inline=False)
        embed.add_field(name="*Tags*", value=tags, inline=False)
        embed.add_field(name="*Popularity*", value=request_count, inline=False)
        embed.add_field(name="*Avg. rating*", value=str(mean(ratings)) if len(ratings) > 0 else 'No ratings yet', inline=False)

        return embed


class RecipeBot(commands.Bot):
    bot_channel = None
    banned_users_db = None

    async def on_ready(self):
        config_obj = configparser.ConfigParser()
        config_obj.read(CONFIG_FILE)
        bot_config = config_obj['DiscordBot']

        self.bot_channel = bot_config['channel']

        database = get_database()
        db_config = config_obj['MongoDB']
        self.banned_users_db = database[db_config['banned_users_collection']]

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if self.user == message.author:
            return

        if message.channel.name != self.bot_channel:
            return

        if self.banned_users_db.find_one({'creator_id': message.author.id}) is not None:
            return

        await self.process_commands(message)


if __name__ == "__main__":
    main()
