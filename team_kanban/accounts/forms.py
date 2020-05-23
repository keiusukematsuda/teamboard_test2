from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy


from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",
                  "password1",
                  "password2",
                  "icon",
                  "sex",
                  "position")

    def clean_password(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 4:
            return forms.ValidationError("パスワードは4文字以上である必要があります")
        return password


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる
