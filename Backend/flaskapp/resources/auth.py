from bson import json_util
import json
from flask import request
from mongoengine import DoesNotExist

from flaskapp.database.models import Admins
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
import datetime

class RegisterApi(Resource):
    @jwt_required()
    def post(self):
        body = request.get_json()
        admin = Admins(**body)
        admin.hash_password()
        admin.save()
        id = admin.id
        return {'id': str(id)}, 200

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