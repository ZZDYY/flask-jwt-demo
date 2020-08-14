# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 10:41
# @Author  : CMJ
# @File    : user.py
# @Software: PyCharm
from .. import db, flask_bcrypt
import time
from App.model.blacklist import BlacklistToken
from ..config import key
import jwt
import datetime
roles_users = db.Table('roles_users',  # 用户权限中间表
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    registered_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_login_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    current_login_time = db.Column(db.DateTime(), default=datetime.datetime.now)
    registered_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


    def __init__(self, email, username=None, password=None, active=True
                 , registered_ip=None, current_login_ip=None):
        self.username = username
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
        self.active = True
        self.email = email
        self.registered_ip = registered_ip
        self.current_login_ip = current_login_ip


    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def keys(self):
        return ('username', 'email', 'registered_time', 'last_login_time', 'current_login_time', 'registered_ip', 'active')

    def __getitem__(self, item):
        return getattr(self, item)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        rfexp = datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5)
        exp = int(time.time()+600)
        try:
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            RFpayload = {
                'exp': rfexp,
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            ), jwt.encode(
                RFpayload,
                key,
                algorithm='HS512'
            )
        except Exception as e:
            return e

    @staticmethod
    def refresh_auth_token(rf_auth_token):
        try:
            payload = jwt.decode(rf_auth_token, key)
            sub = payload['sub']
            exp = int(time.time() + 600)
            payload = {
                'exp': exp,
                'iat': datetime.datetime.utcnow(),
                'sub': sub
            }
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        return jwt.encode(
            payload,
            key,
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        if len(auth_token) != 139:
            return "Invalid token. Please log in again."
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)

class Role(db.Model):  # 权限表
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description