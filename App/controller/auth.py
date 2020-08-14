# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 10:44
# @Author  : CMJ
# @File    : auth_service.py
# @Software: PyCharm
from . import main
from flask import request, jsonify
from App.service.auth_service import Auth
from App.service.user_service import get_all_users, save_new_user, get_a_user
from App.utils.decorator import token_required




@main.route("/login", methods=['POST'])
def login():
    post_data = request.json
    return Auth.login_user(data=post_data)

@main.route("/token", methods=['POST'])
def refresh_token():
    rf_token = request.headers.get("rf_token")
    return Auth.refresh_token(rf_token)

@main.route("/logout", methods=['POST', 'GET'])
def logout():
    auth_header = request.headers.get('Authorization')
    return Auth.logout_user(data=auth_header)

@main.route("/user", methods=['GET'])
@token_required(["admin"])
def list_user():
    users = get_all_users()
    for i in users:
        print(i)
    return jsonify(users)

@main.route("/user", methods=['POST'])
@token_required()
def create_user():
    data = request.json
    ip = request.remote_addr
    return save_new_user(data, ip)

@main.route("/user/<userId>", methods=['GET'])
@token_required()
def get_user(userId):
    myuser = get_a_user(userId)
    if not myuser:
        main.abort(404)
    else:
        return jsonify(myuser)