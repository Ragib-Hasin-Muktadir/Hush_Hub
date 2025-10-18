from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, EmergencyContact


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2', 'bio', 'phone', 'profile_picture']


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone_number', 'relationship']
