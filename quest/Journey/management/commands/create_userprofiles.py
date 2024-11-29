from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Journey.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile instances for all existing users'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            UserProfile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS('UserProfile instances created for all existing users.'))
