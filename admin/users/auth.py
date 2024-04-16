import http

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from dotenv import load_dotenv
import os

load_dotenv()

User = get_user_model()

host=os.environ.get('auth_host')
port=os.environ.get('auth_port')

url = f'http://{host}:{port}/auth/api/v1/auth/token/'


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):

        payload = {'username': username, 'password': password}
        response = requests.post(url, data=payload)

        if response.status_code != http.HTTPStatus.OK:
            return None

        data = response.json()
        # if data.get('is_admin') is not True:
        #     return None

        try:
            user, created = User.objects.get_or_create(id=data['uuid'])
            user.username = data.get('username')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.is_active = data.get('is_active')
            user.is_staff = 'True'
            user.is_superuser = 'True'
            user.save()

        except Exception:
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
