from random import choice

from django.core.management.base import BaseCommand
from faker import Faker

from ads.models import Ad
from users.models import User


class Command(BaseCommand):
    help = "Generate fake Persian ads"

    def add_arguments(self, parser):
        parser.add_argument('--ads', type=int, default=100, help='Number of ads to create')
        parser.add_argument('--clear', action='store_true', help='Delete existing data first')

    def handle(self, *args, **options):
        fake = Faker("fa_IR")
        ads_count = options['ads']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write("Deleting existing users and ads...")
            Ad.objects.all().delete()

        self.stdout.write(f"Creating {ads_count} ads...")
        for _ in range(ads_count):
            users = User.objects.all()

            Ad.objects.create(
                creator=choice(users),
                title=fake.sentence(nb_words=5),
                description=fake.text(max_nb_chars=200)
            )
        self.stdout.write(self.style.SUCCESS(f"{ads_count} ads created ✅"))
