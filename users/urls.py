from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
