# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 10:56
# @Author  : CMJ
# @File    : auth_service.py
# @Software: PyCharm
from App.model.user import User
from App.service.blacklist_service import save_token
class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(username=data.get('username')).first()
            if user and user.check_password(data.get('password')):
                auth_token, rf_token = User.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode(),
                        'rf_token': rf_token.decode()
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'username or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        auth_token = data
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403


    @staticmethod
    def refresh_token(rf_token):
        if rf_token:
            resp = User.refresh_auth_token(rf_token)
            if isinstance(resp, bytes):
                response_object = {
                    'status': 'success',
                    'message': 'Successfully refresh Authorization',
                    'Authorization': resp.decode(),
                }
                return response_object
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403


    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                role_list = user.roles
                print(type(role_list))
                response_object = {
                    'status': 'success',
                    'data': {
                        'role': [role.name for role in role_list],
                        'user_id': user.id,
                        'email': user.email,
                        'registered_time': str(user.registered_time)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Please login to get token.'
            }
            return response_object, 401