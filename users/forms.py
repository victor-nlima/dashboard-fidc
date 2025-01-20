from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","password"]
        labels = {'username':"Nome",'password':'Senha'}
        widgets = {
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'username': forms.TextInput(attrs={'class':'form-control'})
        }