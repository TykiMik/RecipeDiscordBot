from bson.json_util import dumps
import datetime
from flask import request, Response
from mongoengine import DoesNotExist

from flaskapp.database.models import Admins
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

def transform_models(admins):
    admins_list = []
    for admin in admins:
        admin_dict = admin.to_mongo().to_dict()
        del admin_dict['password']
        del admin_dict['_id']
        admins_list.append(admin_dict)

    return admins_list

class RegisterApi(Resource):
    @jwt_required()
    def get(self):
        admins = Admins.objects()
        admins_list = transform_models(admins)
        resp = {"items": admins_list}
        return Response(dumps(resp), mimetype="application/json", status=200)

    @jwt_required()
    def post(self):
        body = request.get_json()
        admin = Admins(**body)

        try:
            Admins.objects.get(name=admin.name)
        except DoesNotExist:
            admin.hash_password()
            admin.save()
            id = admin.id
            return {'id': str(id)}, 200

        return '', 405

    @jwt_required()
    def delete(self):
        if Admins.objects.count() <= 1:
            return '', 405

        current_user = get_jwt_identity()
        Admins.objects.get(id=current_user).delete()
        return '', 204


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        admin = None
        try:
            admin = Admins.objects.get(name=body.get('name'))
        except DoesNotExist:
            return {'error': 'name or password invalid'}, 401

        authorized = admin.check_password(body.get('password'))
        if not authorized:
            return {'error': 'name or password invalid'}, 401

        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=str(admin.id), expires_delta=expires)
        return {'token': access_token, 'expires_in': expires.seconds}, 200