from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from catalog.forms import StyleFormMixin
from users.models import User


class UserAuthenticationForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User


class UserRegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserUserChangeForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class RestorePasswordForm(StyleFormMixin, forms.Form):
    email = forms.EmailField()
