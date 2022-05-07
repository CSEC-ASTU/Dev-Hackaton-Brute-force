from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


import uuid
#uuid is  universal unique  identifer is a python library which helps in generating random objects of 128 bits 

class Role(models.Model):

    choice = (
        ("PRESIDENT", "President"),
        ("V_PRESIDENT", "V President"),
        ("HEAD", "Head"),
        ("SPECIAL_COMMITTEE", "Special Committee"),
        ("MEMBER", "Member"),
    )
    role = models.CharField(max_length=20, choices=choice)

    def __str__(self):
        return f"{ self.role }"


def user_directory_path(instance, filename):
    ext = (filename).split(".")[-1]
    filename = str(uuid.uuid1())
    print(instance)
    return f"users/{instance.id}{filename}.{ext}"

class SocialAccountsLinks(models.Model):
    website = models.CharField(
        _("Website"), max_length=200, default="https://www.csec-astu.tech/?*Defautl*",blank=True, null=True
    )
    github = models.CharField(
        _("Github"), max_length=200, default="https://www.github.com/?*Defautl*",blank=True, null=True
    )
    twitter = models.CharField(
        _("Twitter"), max_length=200, default="https://www.twitter./?*Defautl*",blank=True, null=True
    )
    linkedin = models.CharField(
        _("Linkedin"), max_length=200, default="https://linkedin.com/in/?*Defautl*",blank=True, null=True
    )
    # github = models.URLField(_("Github"), max_length=200, default="https://www.github.com?*Defautl*")
    
    def __str__(self) -> str:
        return f'{ self.id }'


class User(AbstractUser):

    DIVISION = (
        ("cpd", "Competitive Programming"),
        ("development", "Development"),
        ("capacity", "Capacity Building"),
        ("unassigned", "Unassigned"),
        # ("cybersecurity","cyebr security"),
        # ("Data Science","Data Science")
    )

    student_id = models.CharField(max_length=20, blank=True, null=True)
    role = models.ForeignKey(
        Role,
        verbose_name=_("Role"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    division = models.CharField(
        max_length=20, choices=DIVISION, blank=True, null=True, default="unassigned"
    )
    profile = models.ImageField(
        _("Image"),
        upload_to=user_directory_path,
        default="users/null.png",
        blank=True,
        null=True,
    )
    socials = models.OneToOneField(
        SocialAccountsLinks,
        verbose_name=_("SocialAccountsLinks"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    phone = models.CharField(
        _("Phone"), max_length=50, default="+251900000000", blank=True, null=True
    )
    about = models.TextField(_("About"), default='', max_length = 250)
    
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.username}"

    @property
    def get_full_name(self) -> str:
        return super().get_full_name()

    @property
    def get_division(self):
        return self.division

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})
    
    def save(self,*args, **kwargs ):
        if self.socials is None:
            print("User Saved Model inside if case ")
            default_socials = SocialAccountsLinks()
            default_socials.save() 
            self.socials = default_socials
        
        print("User Model Save Called", self.first_name)
        return super().save()


