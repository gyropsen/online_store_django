from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not user.is_superuser:
                user.delete()
        print(User.objects.all())
