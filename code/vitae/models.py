from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.FileField(blank=True)
    profilePicContentType = models.TextField(default='image/jpg')
    hasProfilePic = models.BooleanField(default=False)


# Parent class for all profile sections
class ProfileSection(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # Profile that each section belongs to.


class IntroSection(ProfileSection):
    bio = models.TextField()
    linkedin = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    github = models.URLField()


class WorkExperienceSection(ProfileSection):
    sectionName = "Work Experience"
    companyName = models.TextField()
    title = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField() # TODO: Or current?
    description = models.TextField()


class EducationSection(ProfileSection):
    sectionName = "Education"
    schoolName = models.TextField()
    location = models.TextField()
    degree = models.TextField()
    gpa = models.FloatField()
    gradDate = models.DateField()


class ProjectsSection(ProfileSection):
    sectionName = "Projects"
    name = models.TextField()
    description = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()
    # TODO: Add photos/videos


class SkillsSection(ProfileSection):
    sectionName = "Skills"
    name = models.TextField()
    confidence = models.FloatField() # TODO: Set a range from 0-100

# TODO: Add research and awards

# Creates and links new sections to a given profile
def initSections(profile):
    IntroSection().profile = profile
    WorkExperienceSection().profile = profile
    EducationSection().profile = profile
    ProjectsSection().profile = profile
    SkillsSection().profile = profile
