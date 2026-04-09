from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, LANGUAGE_CHOICES


class RegisterForm(UserCreationForm):
    target_language = forms.ChoiceField(choices=LANGUAGE_CHOICES, label='I want to learn')

    class Meta:
        model = User
        fields = ('username', 'email', 'target_language', 'password1', 'password2')


class LanguageSelectForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('target_language',)
        labels = {'target_language': 'I want to learn'}
