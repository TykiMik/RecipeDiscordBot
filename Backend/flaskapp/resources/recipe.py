from flask import Response, request, jsonify
from flaskapp.database.models import Recipes
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from bson.json_util import dumps

class RecipesApi(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        recipes = Recipes.objects().paginate(page=page, per_page=per_page)
        recipes_total_count = Recipes.objects.count()
        recipes_list = []
        for recipe in recipes.items:
            recipe_dict = recipe.to_mongo().to_dict()
            recipe_dict['creation_date'] = recipe.creation_date.isoformat()
            recipes_list.append(recipe_dict)
        resp = {"items": recipes_list, "total_count": recipes_total_count}
        return Response(dumps(resp), mimetype="application/json", status=200)

class RecipeApi(Resource):
    @jwt_required()
    def delete(self, id):
        Recipes.objects.get(id=id).delete()
        return '', 200