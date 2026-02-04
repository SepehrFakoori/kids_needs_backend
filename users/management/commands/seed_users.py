from django.core.management.base import BaseCommand
from faker import Faker

from users.models import User

class Command(BaseCommand):
    help = "Generate fake Persian users"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10, help='Number of users to create')
        parser.add_argument('--clear', action='store_true', help='Delete existing data first')

    def handle(self, *args, **options):
        fake = Faker("fa_IR")
        users_count = options['users']
        # ads_count = options['ads']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write("Deleting existing users and ads...")
            # Ad.objects.all().delete()
            User.objects.all().delete()

        self.stdout.write(f"Creating {users_count} users...")
        users = []
        for _ in range(users_count):
            user = User.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:15],
                email=fake.email(),
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"{users_count} users created ✅"))

        # self.stdout.write(f"Creating {ads_count} ads...")
        # for _ in range(ads_count):
        #     Ad.objects.create(
        #         creator=random.choice(users),
        #         title=fake.sentence(nb_words=5),
        #         description=fake.text(max_nb_chars=200)
        #     )
        # self.stdout.write(self.style.SUCCESS(f"{ads_count} ads created ✅"))
