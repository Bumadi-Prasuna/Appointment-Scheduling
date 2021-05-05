from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from .signals import create_auth_token  # noqa

class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Company(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", null=True)

    def __str__(self):
        return str(self.name)