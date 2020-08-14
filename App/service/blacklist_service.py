# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 10:57
# @Author  : CMJ
# @File    : blacklist_service.py
# @Software: PyCharm
from App.model.blacklist import BlacklistToken
from App import db
def save_token(token):
    blacklist_token = BlacklistToken(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 200