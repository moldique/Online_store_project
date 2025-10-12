from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка для модели пользователя"""
    
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'country', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'country')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'avatar', 'phone_number', 'country')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
