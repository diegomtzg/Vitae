from django.db import models
from django.contrib.auth.models import User

MAX_CHARFIELD_LENGTH = 50

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.FileField(blank=True)
    profilePicContentType = models.TextField(default='image/jpg')
    hasProfilePic = models.BooleanField(default=False)


# Parent class for all profile sections
class ProfileSection(models.Model):
    sectionName = models.CharField(max_length=MAX_CHARFIELD_LENGTH)


class Intro(ProfileSection):
    # Intro section uses user data to populate contact info
    bio = models.TextField()
    # TODO: Add socials


class WorkExperience(ProfileSection):
    companyName = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    title = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    startDate = models.DateField()
    endDate = models.DateField() # TODO: Or current?
    description = models.TextField()

class Education(ProfileSection):
    schoolName = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    location = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    degree = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    gpa = models.FloatField()
    gradDate = models.DateField()

# TODO: Add Projects, Skills, Research and Awards
