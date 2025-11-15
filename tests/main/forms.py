from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'})
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'})
    )
    patronymic = forms.CharField(
        label='Отчество',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите отчество'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя пользователя'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Введите email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите фамилию'}),
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают')
        return password_confirm

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email


class EmailAuthenticationForm(forms.Form):
    """Форма входа по email"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Введите email'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Введите пароль'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                self.user_cache = authenticate(username=user.username, password=password)
                if self.user_cache is None:
                    raise ValidationError('Неверный email или пароль')
            except User.DoesNotExist:
                raise ValidationError('Неверный email или пароль')
        
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)
