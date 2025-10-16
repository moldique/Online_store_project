from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import UserRegistrationForm, UserLoginForm
from .models import User


class UserRegistrationView(CreateView):
    """Представление для регистрации пользователя"""
    
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('catalog:home')
    
    def form_valid(self, form):
        """Обработка успешной регистрации"""
        response = super().form_valid(form)
        
        # Авторизуем пользователя после регистрации
        user = form.instance
        login(self.request, user)
        
        # Отправляем приветственное письмо
        self.send_welcome_email(user)
        
        # Добавляем сообщение об успешной регистрации
        messages.success(
            self.request,
            f'Добро пожаловать, {user.username}! Вы успешно зарегистрированы.'
        )
        
        return response
    
    def send_welcome_email(self, user):
        """Отправка приветственного письма пользователю"""
        try:
            subject = 'Добро пожаловать в наш сервис!'
            
            # Создаем HTML-шаблон письма
            html_message = render_to_string('users/welcome_email.html', {
                'user': user,
                'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000'
            })
            
            # Создаем текстовую версию письма
            plain_message = strip_tags(html_message)
            
            # Отправляем письмо
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
        except Exception as e:
            # Логируем ошибку, но не прерываем процесс регистрации
            print(f"Ошибка отправки письма: {e}")
            messages.warning(
                self.request,
                'Регистрация прошла успешно, но не удалось отправить приветственное письмо.'
            )


class UserLoginView(LoginView):
    """Представление для авторизации пользователя"""
    
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """URL для перенаправления после успешного входа"""
        return reverse_lazy('catalog:home')
    
    def form_valid(self, form):
        """Обработка успешной авторизации"""
        # Получаем email и пароль из формы
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        # Аутентифицируем пользователя по email
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(self.request, user)
            remember_me = form.cleaned_data.get('remember_me', False)
            
            if not remember_me:
                # Если не выбран "Запомнить меня", сессия истечет при закрытии браузера
                self.request.session.set_expiry(0)
            
            messages.success(self.request, f'Добро пожаловать, {user.username}!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Неверный email или пароль.')
            return self.form_invalid(form)


@login_required
def profile_view(request):
    """Представление профиля пользователя"""
    return render(request, 'users/profile.html', {'user': request.user})
