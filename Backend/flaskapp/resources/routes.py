from .recipe import RecipesApi, RecipeApi
from .auth import RegisterApi, LoginApi
from .banned_user import BannedUsersApi

def initialize_routes(api):
    api.add_resource(RecipesApi, '/api/recipes')
    api.add_resource(RecipeApi, '/api/recipes/<id>')
    api.add_resource(RegisterApi, '/api/auth/register')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(BannedUsersApi, '/api/banned_users')
