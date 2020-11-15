from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
    firstName = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First name'}))
    lastName = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm password'}))

    def clean(self):
        clean_data = super().clean()

        # Verify that passwords match.
        pwd1 = clean_data['password']
        pwd2 = clean_data['confirmPassword']
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError("Passwords do not match.")

        # Verify that username is unique.
        username = clean_data['username']
        if User.objects.all().filter(username__exact=username):
            raise forms.ValidationError("Username already exists.")

        return clean_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))

    def clean(self):
        clean_data = super().clean()
        username = clean_data['username']
        password = clean_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password.')

        return clean_data