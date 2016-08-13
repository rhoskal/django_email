from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from .models import Client

class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        UserModel = get_user_model()

        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
