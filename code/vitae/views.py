from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    registerForm = RegisterForm(request.POST)
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

    # Also create a new empty profile associated with this user and initialize its empty sections.
    newProfile = Profile(owner=newUser)
    newProfile.save()
    initSections(newProfile)

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
        return render(request, 'vitae/search.html', context={'form': SearchForm()})

    searchForm = SearchForm(request.POST)
    if not searchForm.is_valid():
        return render(request, 'vitae/search.html', context={'form': searchForm})

    print(f"~~~~~ THIS IS THE REQUEST: {request.POST} ~~~~")
    return render(request, 'vitae/searchResults.html', context={'results': profileSearch(searchForm.cleaned_data['query'])})

def profileSearch(query):
    """
    Conducts a search through all profiles for keywords in query and
    returns list of all usernames matching some portion of the query.
    @param query:
    @return: List of string usernames of profiles matching search query.
    """
    print(f"~~~ ENTERED PROFILE SEARCH: {query} ~~~")
    temporaryQuery = "chan zuck, educate, abnormal security, 4.0, distributed systems,"

    validProfiles = []
    for profile in Profile.objects.all():
        queryResults = searchForKeywordsInProfile(profile, query)
        print(f"Profile: {profile.owner}\n{queryResults}\n")
        if len(queryResults.keys()) > 0:
            validProfiles.append(profile.owner)

    print(validProfiles)
    return validProfiles

def searchForKeywordsInProfile(profile, keyphrases):
    # Build the profile query keys
    queryKeys = set()
    for keyphrase in keyphrases.split(","):
        keyphrase = keyphrase.strip()
        wordsInPhrase = keyphrase.split(" ")
        if len(wordsInPhrase) == 0 or len(keyphrase) == 0:
            continue
        elif len(wordsInPhrase) > 1:
            # In order to search for existence of each word of the phrase in the profile
            for word in wordsInPhrase:
                queryKeys.add(word)
        queryKeys.add(keyphrase)

    serializedProfile = serializeProfileAsString(profile)
    keywordsFound = dict()
    for key in queryKeys:
        foundCount = serializedProfile.count(key)
        if foundCount > 0:
            keywordsFound[key] = foundCount

    return keywordsFound

def serializeProfileAsString(profile):
    serialized = ""
    for workElem in profile.workSection.elements.all():
        serialized = serialized + workElem.__str__().lower() + "\n"
    for educationElem in profile.educationSection.elements.all():
        serialized = serialized + educationElem.__str__().lower() + "\n"
    for projectElem in profile.projectSection.elements.all():
        serialized = serialized + projectElem.__str__().lower() + "\n"
    for skillElem in profile.skillSection.elements.all():
        serialized = serialized + skillElem.__str__().lower() + "\n"

    return serialized

@login_required
def visitProfileAction(request, username):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        context = getProfileContext(user)
        return render(request, 'vitae/profile.html', context)


@login_required
def editProfile(request, sectionName):
    """
    General class to handle any and all modifications to a user's profile.
    @param TODO elementId identifier for the section element being modified or "new" if adding a new element. (Currently only adds new elements)
    """

    profile = request.user.profile
    if sectionName == 'work':
        form = WorkExperienceForm(request.POST)
        if not form.is_valid():
            context = getProfileContext(request.user)
            context['addWorkExperienceForm'] = form
            return redirect(reverse('profile', args=[request.user]))

        new_element = WorkExperienceElement(
            section=profile.workSection,
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
            section=profile.educationSection,
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
            section=profile.projectSection,
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
            section=profile.skillSection,
            name=form.cleaned_data['name'],
            proficiency=form.cleaned_data['proficiency'],)
        new_element.save()
        print("New skill profile element")

    # TODO: Render a confirmation popup or ideally add an animation of new element showing up on page instead of redirecting... (maybe AJAX?)
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
        'workElements': profileOwner.profile.workSection.elements.all(), # TODO: Sort in chronological order
        'educationElements': profileOwner.profile.educationSection.elements.all(),
        'projectElements': profileOwner.profile.projectSection.elements.all(),
        'skillElements': profileOwner.profile.skillSection.elements.all(),
    }
    return context


@login_required
def logoutAction(request):
    logout(request)
    return redirect(reverse('search'))
