from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from project.users.forms import UserChangeForm, UserCreationForm
from . import models

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location',)

admin.site.site_header = 'Project'
admin.site.site_title = 'Project'