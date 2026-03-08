from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'

    error_messages = {
        'invalid_login': "Пожалуйста, введите правильные имя пользователя и пароль. Оба поля обязательны.",
        'inactive': "Этот аккаунт неактивен.",
    }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Переводим стандартные сообщения Django на русский
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


    # Отключаем стандартные валидаторы Django для пароля
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.password_validators = []

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        username = self.cleaned_data.get("username")
        errors = []
        if not password:
            raise forms.ValidationError("Пароль обязателен для заполнения")
        if not password.isascii():
            errors.append("Пароль должен быть только на английском языке (латиница)")
        if not re.search(r'[A-Z]', password):
            errors.append("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r'[^A-Za-z0-9]', password):
            errors.append("Пароль должен содержать хотя бы один специальный символ")
        if len(password) < 8:
            errors.append("Пароль должен содержать минимум 8 символов")
        if username and password.lower() == username.lower():
            errors.append("Пароль слишком похож на имя пользователя.")
        if password.isdigit():
            errors.append("Пароль не должен состоять только из цифр.")
        common_passwords = ["password", "123456", "12345678", "qwerty", "abc123", "111111", "123123", "12345", "1234", "123456789", "000000"]
        if password.lower() in common_passwords:
            errors.append("Пароль слишком простой.")
        if errors:
            raise forms.ValidationError(errors)
        return password

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise forms.ValidationError("Логин должен содержать только латинские буквы, цифры и _")
        if not username.isascii():
            raise forms.ValidationError("Логин должен быть только на английском языке (латиница)")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not password.isascii():
            raise forms.ValidationError("Пароль должен быть только на английском языке (латиница)")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r'[^A-Za-z0-9]', password):
            raise forms.ValidationError("Пароль должен содержать хотя бы один специальный символ")
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data
