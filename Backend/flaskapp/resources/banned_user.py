from flask import Response, request
from mongoengine import DoesNotExist

from flaskapp.database.models import BannedUsers
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from datetime import datetime
from bson.json_util import dumps


def transform_models(banned_users):
    user_list = []
    for user in banned_users.items:
        user_dict = user.to_mongo().to_dict()
        user_dict['ban_date'] = user.ban_date.isoformat()
        user_dict['id'] = str(user_dict['_id'])
        del user_dict['_id']
        user_list.append(user_dict)

    return user_list

class BannedUsersApi(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 30, type=int)

        banned_users = BannedUsers.objects().paginate(page=page, per_page=per_page)
        users_total_count = BannedUsers.objects().count()
        user_list = transform_models(banned_users)
        resp = {"items": user_list, "total_count": users_total_count}
        return Response(dumps(resp), mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        body = request.get_json()
        banned_user = BannedUsers(**body, ban_date=datetime.now())
        banned_user.save()
        id = banned_user.creator_id
        return {'id': str(id)}, 200

    @jwt_required()
    def delete(self):
        body = request.get_json()
        items = body['items']
        for item in items:
            try:
                BannedUsers.objects.get(id=item).delete()
            except DoesNotExist:
                pass
        return '', 204