from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Cliente

class ClienteBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            cliente = Cliente.objects.get(email=username)
            if check_password(password, cliente.password):
                return cliente
        except Cliente.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Cliente.objects.get(pk=user_id)
        except Cliente.DoesNotExist:
            return None
