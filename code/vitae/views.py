from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files import File

from django.contrib.auth.models import User
from vitae.models import *
from vitae.forms import *


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
    registerForm = RegisterForm(request.POST, request.FILES)
    if not registerForm.is_valid():
        return render(request, 'vitae/register.html', {'form': registerForm})

    print("Valid register POST request received: ", request.POST)
    newUser = User.objects.create_user(
        username=registerForm.cleaned_data['username'],
        email=registerForm.cleaned_data['email'],
        password=registerForm.cleaned_data['password'],
        first_name=registerForm.cleaned_data['first_name'],
        last_name=registerForm.cleaned_data['last_name'])
    newUser.save()
    print("New user created:", newUser)

    # Create new empty profile associated with user
    newProfile = Profile(
        owner=newUser,
        bio=registerForm.cleaned_data['bio'],
        phone=registerForm.cleaned_data['phone'],
        location=registerForm.cleaned_data['location'],
        twitter=registerForm.cleaned_data['twitter'],
        linkedin=registerForm.cleaned_data['linkedin'],
        facebook=registerForm.cleaned_data['facebook'],
        github=registerForm.cleaned_data['github'],
        title1=registerForm.cleaned_data['title1'],
        title2=registerForm.cleaned_data['title2'],
        title3=registerForm.cleaned_data['title3'])

    if len(request.FILES) > 0:
        pic = registerForm.cleaned_data['profile_picture']
        print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
        newProfile.profile_pic = pic
        newProfile.profile_pic_ctype = type(pic)
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


def searchAction(request):
    if request.method == 'GET':
        return render(request, 'vitae/search.html')


def visitProfileAction(request, username):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        context = getProfileContext(user)
        return render(request, 'vitae/profile.html', context)


@login_required
def addProfileSection(request, sectionName):
    profile = request.user.profile
    if sectionName == 'work':
        form = WorkExperienceForm(request.POST)
        if not form.is_valid():
            context = getProfileContext(request.user)
            context['addWorkExperienceForm'] = form
            return redirect(reverse('profile', args=[request.user]))

        new_element = WorkExperienceElement(
            profile=profile,
            company_name=form.cleaned_data['company_name'],
            job_title=form.cleaned_data['job_title'],
            start_date=form.cleaned_data['start_date'],
            end_date=form.cleaned_data['end_date'],
            description=form.cleaned_data['description'])
        new_element.save()
        print("New work experience profile element")

    elif sectionName == 'education':
        form = EducationForm(request.POST)
        if not form.is_valid():
            context = getProfileContext(request.user)
            context['addEducationForm'] = form
            return redirect(reverse('profile', args=[request.user]))

        new_element = EducationElement(
            profile=profile,
            school_name=form.cleaned_data['school_name'],
            school_location=form.cleaned_data['school_location'],
            degree=form.cleaned_data['degree'],
            gpa=form.cleaned_data['gpa'],
            graduation_date=form.cleaned_data['graduation_date'])
        new_element.save()
        print("New education profile element")

    elif sectionName == 'project':
        form = ProjectsForm(request.POST)
        if not form.is_valid():
            context = getProfileContext(request.user)
            context['addProjectForm'] = form
            return redirect(reverse('profile', args=[request.user]))

        new_element = ProjectElement(
            profile=profile,
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            start_date=form.cleaned_data['start_date'],
            end_date=form.cleaned_data['end_date'])
        new_element.save()
        print("New project profile element")

    elif sectionName == 'skill':
        form = SkillsForm(request.POST)
        if not form.is_valid():
            context = getProfileContext(request.user)
            context['addSkillForm'] = form
            return redirect(reverse('profile', args=[request.user]))

        new_element = SkillElement(
            profile=profile,
            name=form.cleaned_data['name'],
            proficiency=form.cleaned_data['proficiency'],)
        new_element.save()
        print("New skill profile element")

    return redirect(reverse('profile', args=[request.user]))


@login_required
def editProfileElement(request, sectionName, elementId):
    # If elementId is not an integer, don't try anything or it will break
    try:
        id = int(elementId)
    except:
        user = request.user
        context = getProfileContext(user)
        return render(request, 'vitae/profile.html', context)

    if sectionName == 'work':
        element = request.user.profile.workElements.get(id=id)
        if request.method == 'GET':
            form = WorkExperienceForm(instance=element)
            return render(request, 'vitae/edit_form.html', {'form': form, 'section': 'work', 'id': id})
        else:
            form = WorkExperienceForm(request.POST, instance=element)
            if form.is_valid():
                form.save()
            return redirect(reverse('profile', args=[request.user]))
    elif sectionName == 'education':
        element = request.user.profile.educationElements.get(id=id)
        if request.method == 'GET':
            form = EducationForm(instance=element)
            return render(request, 'vitae/edit_form.html', {'form': form, 'section': 'education', 'id': id})
        else:
            form = EducationForm(request.POST, instance=element)
            if form.is_valid():
                form.save()
            return redirect(reverse('profile', args=[request.user]))
    elif sectionName == 'project':
        element = request.user.profile.projectElements.get(id=id)
        if request.method == 'GET':
            form = ProjectsForm(instance=element)
            return render(request, 'vitae/edit_form.html', {'form': form, 'section': 'project', 'id': id})
        else:
            form = ProjectsForm(request.POST, instance=element)
            if form.is_valid():
                form.save()
            return redirect(reverse('profile', args=[request.user]))
    elif sectionName == 'skill':
        element = request.user.profile.skillElements.get(id=id)
        if request.method == 'GET':
            form = SkillsForm(instance=element)
            return render(request, 'vitae/edit_form.html', {'form': form, 'section': 'skill', 'id': id})
        else:
            form = SkillsForm(request.POST, instance=element)
            if form.is_valid():
                form.save()
            return redirect(reverse('profile', args=[request.user]))
    if sectionName == 'about':
        if request.method == 'GET':
            form = AboutForm(data={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.profile.phone,
                'location': request.user.profile.location,
                'twitter': request.user.profile.twitter,
                'github': request.user.profile.github,
                'facebook': request.user.profile.facebook,
                'linkedin': request.user.profile.linkedin,
                'bio': request.user.profile.bio,
                'title1': request.user.profile.title1,
                'title2': request.user.profile.title2,
                'title3': request.user.profile.title3,
            })
            return render(request, 'vitae/edit_form.html', {'form': form, 'section': 'about', 'id': id})
        else:
            form = AboutForm(request.POST, request.FILES)
            if form.is_valid():
                user = request.user
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                profile = request.user.profile
                profile.phone = form.cleaned_data['phone']
                profile.location = form.cleaned_data['location']
                profile.twitter = form.cleaned_data['twitter']
                profile.github = form.cleaned_data['github']
                profile.facebook = form.cleaned_data['facebook']
                profile.linkedin = form.cleaned_data['linkedin']
                profile.bio = form.cleaned_data['bio']
                profile.title1 = form.cleaned_data['title1']
                profile.title2 = form.cleaned_data['title2']
                profile.title3 = form.cleaned_data['title3']

                if len(request.FILES) > 0:
                    pic = form.cleaned_data['profile_picture']
                    print('Uploaded picture: {} (type={})'.format(pic, type(pic)))
                    profile.profile_pic = pic
                    profile.profile_pic_ctype = type(pic)

                profile.save()

            return redirect(reverse('profile', args=[request.user]))



@login_required
def removeProfileElement(request, sectionName, elementId):
    # If elementId is not an integer, don't try anything or it will break
    try:
        id = int(elementId)
    except:
        user = request.user
        context = getProfileContext(user)
        return render(request, 'vitae/profile.html', context)

    if sectionName == 'work':
            element = request.user.profile.workElements.get(id=id)
            element.delete()
            return redirect(reverse('profile', args=[request.user]))
    if sectionName == 'education':
        element = request.user.profile.educationElements.get(id=id)
        element.delete()
        return redirect(reverse('profile', args=[request.user]))
    if sectionName == 'projects':
        element = request.user.profile.projectElements.get(id=id)
        element.delete()
        return redirect(reverse('profile', args=[request.user]))
    if sectionName == 'skill':
        element = request.user.profile.skillElements.get(id=id)
        element.delete()
        return redirect(reverse('profile', args=[request.user]))


@login_required
def getPhoto(request, username):
    profile = get_object_or_404(User, username=username).profile
    return HttpResponse(profile.profile_pic, content_type=profile.profile_pic_ctype)


def getProfileContext(profileOwner):
    # Ideally, we could get the form using AJAX once the user clicks on
    # which type of experience they want to add... but passing in all of them for now
    context = {
        'profileOwner': profileOwner,
        'addWorkExperienceForm': WorkExperienceForm(),
        'addEducationForm': EducationForm(),
        'addProjectForm': ProjectsForm(),
        'addSkillForm': SkillsForm(),
        'workElements': profileOwner.profile.workElements.all(), # TODO: Sort in chronological order
        'educationElements': profileOwner.profile.educationElements.all(),
        'projectElements': profileOwner.profile.projectElements.all(),
        'skillElements': profileOwner.profile.skillElements.all(),
    }
    return context


@login_required
def logoutAction(request):
    logout(request)
    return redirect(reverse('search'))
