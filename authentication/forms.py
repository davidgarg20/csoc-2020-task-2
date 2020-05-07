from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MaxLengthValidator

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=30,help_text='Required. ')
    email = forms.EmailField(max_length=254, help_text='Required. ' )

    class Meta:
        model = User
        fields = ('username', 'name', 'email',  'password1', 'password2' )