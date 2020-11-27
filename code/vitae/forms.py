from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from vitae.models import *

class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Confirm password'}))

    def clean(self):
        clean_data = super().clean()

        # Verify that passwords match.
        pwd1 = clean_data['password']
        pwd2 = clean_data['confirm_password']
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


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperienceElement
        exclude = ('section',)
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Company name'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Job title'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Start date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'End date'}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 2, 'placeholder': 'Role description'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationElement
        exclude = ('section',)
        widgets = {
           'school_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'School name'}),
           'school_location': forms.TextInput(attrs={'class': 'form-control','placeholder': 'School location'}),
           'degree': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Degree title'}),
           'start_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Start date'}),
           'end_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'End date'}),
           'gpa': forms.TextInput(attrs={'class': 'form-control','placeholder': 'GPA'}),
           'graduation_date': forms.DateInput(attrs={'class': 'form-control','placeholder': 'Graduation date'}),
        }


class ProjectsForm(forms.ModelForm):
    class Meta:
        model = ProjectElement
        exclude = ('section',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Project name'}),
            'description': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Project description'}),
            'start_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Start date'}),
            'end_date': forms.TextInput(attrs={'class': 'form-control','placeholder': 'End date'})
        }


class SkillsForm(forms.ModelForm):
    class Meta:
        model = SkillElement
        exclude = ('section',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skill name'}),
            'proficiency': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10, 'placeholder': 'Proficiency'})
        }

# TODO: Add forms for missing sections