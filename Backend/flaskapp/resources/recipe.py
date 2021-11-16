from flask import Response
from flaskapp.database.models import Recipes
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class RecipesApi(Resource):
    @jwt_required()
    def get(self):
        recipes = Recipes.objects().to_json()
        return Response(recipes, mimetype="application/json", status=200)

class RecipeApi(Resource):
    @jwt_required()
    def delete(self, id):
        Recipes.objects.get(id=id).delete()
        return '', 200