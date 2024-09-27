from django import forms
from django.contrib.auth.forms import UserCreationForm
from login.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')  # Add any fields you want for registration