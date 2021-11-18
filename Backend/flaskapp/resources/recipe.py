from flask import Response, request, jsonify
from mongoengine import DoesNotExist

from flaskapp.database.models import Recipes
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from bson.json_util import dumps

def transform_models(recipes):
    recipes_list = []
    for recipe in recipes.items:
        recipe_dict = recipe.to_mongo().to_dict()
        recipe_dict['creation_date'] = recipe.creation_date.isoformat()
        recipe_dict['id'] = str(recipe_dict['_id'])
        del recipe_dict['_id']
        ratings = recipe_dict['ratings']
        recipe_dict['rating'] = sum(ratings) / len(ratings)
        del recipe_dict['ratings']
        recipes_list.append(recipe_dict)

    return recipes_list

class RecipesApi(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)
        recipes = Recipes.objects().paginate(page=page, per_page=per_page)
        recipes_total_count = Recipes.objects.count()
        recipes_list = transform_models(recipes)
        resp = {"items": recipes_list, "total_count": recipes_total_count}
        return Response(dumps(resp), mimetype="application/json", status=200)

    def delete(self):
        body = request.get_json()
        items = body['items']
        for item in items:
            try:
                Recipes.objects.get(id=item).delete()
            except DoesNotExist:
                pass
        return '', 204

class RecipeApi(Resource):
    def delete(self, id):
        Recipes.objects.get(id=id).delete()
        return '', 204