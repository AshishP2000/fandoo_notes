import logging

import jwt
from django.conf import settings
from rest_framework.response import Response

from .models import User

logging.basicConfig(filename='fundoo_notes.log', level=logging.INFO)


class JWT:
    def encode(self, data):
        try:
            data.update({"exp": settings.JWT_EXP})
            encoded_jwt = jwt.encode(data, "secret", algorithm="HS256")
            return encoded_jwt
        except Exception as ex:
            logging.error(ex)

    def decode(self, token):
        try:
            return jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            raise Exception("token expired")
        except jwt.exceptions.InvalidSignatureError:
            raise Exception("invalid token")
        except Exception as ex:
            logging.error(ex)


def get_user(request):
    try:
        token = request.headers.get('token')
        decode_token = JWT().decode(token)
        user = User.objects.get(id=decode_token.get('user_id'))
        return user
    except User.DoesNotExist:
        return None



def verify_user(function):
    def wrapper(self, request):
        user = get_user(request)
        if user is None:
            return Response({"message": "user not found"})
        request.data.update({'user': user.id})
        return function(self, request)
    return wrapper


def verify_is_superuser(function):
    def wrapper(self, request):
        user = get_user(request)
        if not user.is_superuser:
            return Response({"message": "user not authorized"})
        request.data.update({'user': user.id})
        return function(self, request)

    return wrapper
