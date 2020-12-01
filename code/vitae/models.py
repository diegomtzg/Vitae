from django.db import models
from django.contrib.auth.models import User

MAX_LENGTH = 100

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.FileField(blank=True)
    profile_pic_ctype = models.TextField(default='image/jpg')
    bio = models.TextField()
    phone = models.CharField(max_length=MAX_LENGTH)
    location = models.CharField(max_length=MAX_LENGTH)
    linkedin = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    github = models.URLField()
    title1 = models.CharField(max_length=MAX_LENGTH)
    title2 = models.CharField(max_length=MAX_LENGTH)
    title3 = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return ("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.owner, self.owner.first_name, self.owner.last_name, self.bio, self.location,
            self.linkedin, self.facebook, self.twitter, self.github,
            self.title1, self.title2, self.title3)
        ).replace(",", " ")

class WorkExperienceElement(models.Model):
    profile = models.ForeignKey(Profile, related_name='workElements', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=MAX_LENGTH)
    location = models.CharField(max_length=MAX_LENGTH)
    job_title = models.CharField(max_length=MAX_LENGTH)
    start_date = models.CharField(max_length=MAX_LENGTH)
    end_date = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()

    def __str__(self):
        return "%s, %s, %s" % (self.company_name, self.job_title, self.description)

class EducationElement(models.Model):
    profile = models.ForeignKey(Profile, related_name='educationElements', on_delete=models.CASCADE)
    school_name = models.CharField(max_length=MAX_LENGTH)
    school_location = models.CharField(max_length=MAX_LENGTH)
    degree = models.CharField(max_length=MAX_LENGTH)
    # TODO: Add Major section
    # TODO: Allow users to provide additional information e.g. second majors, minors, honors, deans list
    gpa = models.CharField(max_length=MAX_LENGTH)
    graduation_date = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return "%s, %s, %s, %s" % (self.school_name, self.school_location, self.degree, self.graduation_date)

class ProjectElement(models.Model):
    profile = models.ForeignKey(Profile, related_name='projectElements', on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()
    start_date = models.CharField(max_length=MAX_LENGTH)
    end_date = models.CharField(max_length=MAX_LENGTH)
    # TODO: Add photos/videos
    # TODO: Add hyperlinks to additional resources (e.g. videos, github repos)

    def __str__(self):
        return "%s, %s" % (self.name, self.description)

class SkillElement(models.Model):
    profile = models.ForeignKey(Profile, related_name='skillElements', on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_LENGTH)
    proficiency = models.FloatField()

    def __str__(self):
        return "%s" % (self.name)
