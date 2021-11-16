from flask import Response, request, jsonify
from flaskapp.database.models import Recipes
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class RecipesApi(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        recipes = Recipes.objects().paginate(page=page, per_page=per_page)

        return Response([recipe.to_json() for recipe in recipes.items], mimetype="application/json", status=200)

class RecipeApi(Resource):
    @jwt_required()
    def delete(self, id):
        Recipes.objects.get(id=id).delete()
        return '', 200