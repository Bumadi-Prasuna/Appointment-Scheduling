from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from project.users.models import  Company, User

user_admin = [
    {"name":"admin","password":"password"}
]
companies = ["Google","Apple"]
def create_superuser(username, password):
    print('Creating user {}:{}'.format(username, password))
    user, _ = User.objects.get_or_create(username=username)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    user.set_password(password)
    user.save()
    return user


class Command(BaseCommand):

    def handle(self, *args, **options):

        call_command('makemigrations')
        call_command('migrate')

        if settings.DEBUG:
            print('Creating dummy user')

        print('Creating users and bots')
        for k in user_admin:
            create_superuser(k["name"],k["password"])

        print('Creating companies')
        for company in companies:
            Company.objects.get_or_create(name=company)
        


