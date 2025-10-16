from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        }),
        help_text='Обязательное поле. Используется для входа в систему.'
    )
    
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        help_text='Пароль должен содержать минимум 8 символов.'
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        help_text='Введите тот же пароль для подтверждения.'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
        self.fields['username'].help_text = 'Обязательное поле. 150 символов или меньше. Только буквы, цифры и @/./+/-/_.'
    
    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean_password2(self):
        """Проверка совпадения паролей"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        return password2


class UserLoginForm(forms.Form):
    """Форма авторизации пользователя"""
    
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        })
    )
    
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        label='Запомнить меня',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def __init__(self, *args, **kwargs):
        # Удаляем request из kwargs, если он есть
        kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
