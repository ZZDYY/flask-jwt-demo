# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 14:30
# @Author  : CMJ
# @File    : decorator.py
# @Software: PyCharm

from functools import wraps

from flask import request

from App.service.auth_service import Auth



def token_required(role=None):
    def func(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            data, status = Auth.get_logged_in_user(request)
            token = data.get('data')
            if not token:
                return data, status
            if role is not None:
                _role = token.get('role')
                print(role)
                print(_role)
                if not set(role) <= set(_role):
                    response_object = {
                        'status': 'fail',
                        'message': 'not enough permissions. token required'
                    }
                    return response_object, 401

            return f(*args, **kwargs)
        return decorated
    return func

