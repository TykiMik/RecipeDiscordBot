from .db import db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash


class Recipes(db.Document):
    creator = db.StringField()
    creator_id = db.IntField()
    name = db.StringField()
    content = db.StringField()
    tags = db.ListField(db.StringField())
    request_count = db.IntField()
    ratings = db.ListField(db.IntField())
    creation_date = db.DateTimeField()
    meta = {
        "collection": "recipes"
    }


class BannedUsers(db.Document):
    creator_id = db.IntField(required=True, unique=True)
    ban_date = db.DateTimeField(required=True)
    meta = {
        "collection": "banned_users"
    }


class Admins(db.Document):
    name = db.StringField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    meta = {
        "collection": "admins"
    }

    def hash_password(self):
        ph = PasswordHasher()
        self.password = ph.hash(self.password)

    def check_password(self, password):
        try:
            ph = PasswordHasher()
            return ph.verify(self.password, password)
        except (VerifyMismatchError, VerificationError, InvalidHash):
            return False
