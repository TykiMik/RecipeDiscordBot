import os
from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from flaskapp.models.RecipeModel import RecipeModel

application = Flask(__name__)
api = Api(application)
application.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + \
            os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(application)
db = mongo.db
recipe_collection = db['Recipes']


class Recipes(Resource):
    def get(self):
        recipes = []
        for recipe in recipe_collection.find({}):
            recipes.append(RecipeModel(**recipe))
        return {
            "recipes": [recipe.to_json() for recipe in recipes],
        }


api.add_resource(Recipes, '/', '/Recipes')


if __name__ == "__main__":
    ENV_DEBUG = os.environ.get("APP_DEBUG", True)
    ENV_PORT = os.environ.get("APP_PORT", 5000)

    application.run(host='0.0.0.0', port=ENV_PORT, debug=ENV_DEBUG)
