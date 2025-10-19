from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """Кастомный бэкенд аутентификации по email"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Аутентификация пользователя по email"""
        try:
            # Ищем пользователя по email
            user = User.objects.get(email=username)
            
            # Проверяем пароль
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
        return None
    
    def get_user(self, user_id):
        """Получение пользователя по ID"""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
