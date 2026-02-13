from django.core.management.base import BaseCommand
from faker import Faker

from accounts.models import Account


class Command(BaseCommand):
    help = "Generate fake Persian accounts"

    def add_arguments(self, parser):
        parser.add_argument('--accounts', type=int, default=10, help='Number of accounts to create')
        parser.add_argument('--clear', action='store_true', help='Delete existing data first')

    def handle(self, *args, **options):
        fake = Faker("fa_IR")
        accounts_count = options['accounts']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write("Deleting existing accounts")
            Account.objects.all().delete()

        self.stdout.write(f"Creating {accounts_count} accounts...")
        accounts = []
        for _ in range(accounts_count):
            account = Account.objects.create(
                username=fake.user_name(),
                phone_number=fake.phone_number()[:15],
            )
            accounts.append(account)
        self.stdout.write(self.style.SUCCESS(f"{accounts_count} accounts created ✅"))
