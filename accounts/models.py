"""Models for accounts package"""

from django.contrib.auth import get_user_model


class EmailBackend(object):
    """custom authentication backend"""

    def authenticate(self, request, username=None, password=None):
        """Method to authenticate"""
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if getattr(user, "is_active", False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
