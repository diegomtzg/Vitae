from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers

from django.contrib.auth.models import User
from vitae.models import *
from vitae.forms import *

import json

defaultProfilePicPath = settings.ASSETS_ROOT + 'img/defaultProfilePic.jpg'


def loginAction(request):
    if request.method == 'GET':
        # If user is already logged in, redirect to their profile.
        if request.user.is_authenticated:
            return redirect(reverse('profile', args=[request.user.username]))

        return render(request, 'vitae/login.html', {'form': LoginForm()})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'vitae/login.html', {'form': form})

    user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
    print("User logged in:", form.cleaned_data['username'])
    login(request, user)
    return redirect(reverse('profile', args=[user.username]))


def registerAction(request):
    # Send empty register form for user to fill out.
    if request.method == 'GET':
        return render(request, 'vitae/register.html', {'form': RegisterForm()})

    # Received register form. Validate and create new user.
    registerForm = RegisterForm(request.POST)
    if not registerForm.is_valid():
        return render(request, 'vitae/register.html', {'form': registerForm})

    print("Valid register POST request received: ", request.POST)
    newUser = User.objects.create_user(
        username=registerForm.cleaned_data['username'],
        email=registerForm.cleaned_data['email'],
        password=registerForm.cleaned_data['password'],
        first_name=registerForm.cleaned_data['firstName'],
        last_name=registerForm.cleaned_data['lastName'])
    newUser.save()
    print("New user created:", newUser)

    # Also create a new profile associated with this user and create its (empty) sections.
    newProfile = Profile()
    # initSections(newProfile)
    newProfile.owner = newUser
    newProfile.save()
    print("New profile created for new user:", newProfile)

    # After registering users, automatically log them in.
    authUser = authenticate(username=registerForm.cleaned_data['username'],
                            password=registerForm.cleaned_data['password'])
    # authUser should never be None since we're using the correct username/password
    print("Logging new user in automatically...", newUser.username)
    login(request, authUser)

    # After logging user in, redirect them to their profile.
    return redirect(reverse('profile', args=[newUser.username]))


@login_required
def visitProfileAction(request, username):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        context = getProfileContext(user)
        return render(request, 'vitae/profile.html', context)


def getAddSectionForm(request, sectionName):
    form = None
    if sectionName == WorkExperienceSection.sectionName:
        form = WorkExperienceForm()
    elif sectionName == EducationSection.sectionName:
        form = EducationForm()
    elif sectionName == ProjectsSection.sectionName:
        form = ProjectsForm()
    elif sectionName == SkillsSection.sectionName:
        form = SkillsForm()

    response = serializers.serialize("json", form)
    print(response)
    response = HttpResponse(response, content_type='application/json')
    return response

@login_required
def getPhoto(request, username):
    profile = get_object_or_404(User, username=username).profile
    return HttpResponse(profile.profilePic, content_type=profile.profilePicContentType)


def getProfileContext(profileUser):
    context = {
        'profileOwner': profileUser,
    }
    return context


# Used temporarily for debugging...
def debugLogout(request):
    logout(request)
    return redirect(reverse('login'))
def debugDelete(request):
    print("Deleting everything...")
    User.objects.all().delete()
    Profile.objects.all().delete()
    logout(request)
    return redirect(reverse('register'))