from flask import Response, request
from flaskapp.database.models import BannedUsers
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from datetime import datetime


class BannedUsersApi(Resource):
    @jwt_required()
    def get(self):
        banned_users = BannedUsers.objects().to_json()
        return Response(banned_users, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        banned_user = BannedUsers(**body, ban_date=datetime.now())
        banned_user.save()
        id = banned_user.id
        return {'id': str(id)}, 200