import sqlite3
from db import db


class UserRegisterModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls):
        return cls.query.filter_by(username=cls.username).first()

    @classmethod
    def find_by_id(cls, _id):
        user_id_check = cls.query.filter_by(id=_id).first()
        return user_id_check