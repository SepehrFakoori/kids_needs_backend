from django.core.management.base import BaseCommand
from faker import Faker

from accounts.models import User


class Command(BaseCommand):
    help = "Generate fake Persian users"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--clear', action='store_true', help='Delete existing data first')

    def handle(self, *args, **options):
        fake = Faker("fa_IR")
        users_count = options['users']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write("Deleting existing users")
            User.objects.all().delete()

        self.stdout.write(f"Creating {users_count} users...")
        users = []
        for _ in range(users_count):
            account = User.objects.create(
                username=fake.user_name(),
                phone_number=fake.phone_number()[:15],
            )
            users.append(account)
        self.stdout.write(self.style.SUCCESS(f"{users_count} users created ✅"))
