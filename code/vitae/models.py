from django.db import models
from django.contrib.auth.models import User

MAX_LENGTH = 100

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.FileField(blank=True)
    profile_pic_ctype = models.TextField(default='image/jpg')
    has_pic = models.BooleanField(default=False)


""" PROFILE SECTIONS """
class AboutSection(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    bio = models.TextField()
    linkedin = models.URLField()
    facebook = models.URLField()
    twitter = models.URLField()
    github = models.URLField()

# TODO: Maybe we don't need sections... just elements?
class WorkExperienceSection(models.Model):
    profile = models.OneToOneField(Profile, related_name="workSection", on_delete=models.CASCADE)

class EducationSection(models.Model):
    profile = models.OneToOneField(Profile, related_name="educationSection", on_delete=models.CASCADE)

class ProjectSection(models.Model):
    profile = models.OneToOneField(Profile, related_name="projectSection", on_delete=models.CASCADE)

class SkillSection(models.Model):
    profile = models.OneToOneField(Profile, related_name="skillSection", on_delete=models.CASCADE)
""" END OF PROFILE SECTIONS """


""" SECTION ELEMENTS """
class WorkExperienceElement(models.Model):
    section = models.ForeignKey(WorkExperienceSection, related_name="elements", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=MAX_LENGTH)
    job_title = models.CharField(max_length=MAX_LENGTH)
    start_date = models.CharField(max_length=MAX_LENGTH)
    end_date = models.CharField(max_length=MAX_LENGTH)
    description = models.TextField()

    def __str__(self):
        return "%s, %s, %s" % (self.company_name, self.job_title, self.description)

class EducationElement(models.Model):
    section = models.ForeignKey(EducationSection, related_name="elements", on_delete=models.CASCADE)
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
    section = models.ForeignKey(ProjectSection, related_name="elements", on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_LENGTH)
    description = models.CharField(max_length=MAX_LENGTH)
    start_date = models.CharField(max_length=MAX_LENGTH)
    end_date = models.CharField(max_length=MAX_LENGTH)
    # TODO: Add photos/videos
    # TODO: Add hyperlinks to additional resources (e.g. videos, github repos)

    def __str__(self):
        return "%s, %s" % (self.name, self.description)

class SkillElement(models.Model):
    section = models.ForeignKey(SkillSection, related_name="elements", on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_LENGTH)
    proficiency = models.FloatField()

    def __str__(self):
        return "%s" % (self.name)
""" END OF SECTION ELEMENTS """


# Helper method to initialize a profile's empty sections
# TODO: Consider adding to profile class?
def initSections(profile):
    AboutSection(profile=profile).save()
    WorkExperienceSection(profile=profile).save()
    EducationSection(profile=profile).save()
    ProjectSection(profile=profile).save()
    SkillSection(profile=profile).save()
