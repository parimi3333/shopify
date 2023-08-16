from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import customUsers

class CustomAuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = customUsers.objects.get(
                Q(phone=username) | Q(username=username) | Q(email=username)
            )
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except customUsers.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return customUsers.objects.get(pk=user_id)
        except customUsers.DoesNotExist:
            return None