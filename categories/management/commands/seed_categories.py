from random import choice

from django.core.management.base import BaseCommand
from faker import Faker

from categories.models import Category

class Command(BaseCommand):
    help = "Generate fake Persian Categories"

    def add_arguments(self, parser):
        parser.add_argument('--categories', type=int, default=10, help='Number of categories to create')
        parser.add_argument('--clear', action='store_true', help='Delete existing data first')

    def handle(self, *args, **options):
        fake = Faker("fa_IR")
        categories_count = options['categories']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write("Deleting existing categories...")
            Category.objects.all().delete()

        self.stdout.write(f"Creating {categories_count} categories...")
        for _ in range(categories_count):

            Category.objects.create(
                title=fake.word(),
                slug=fake.slug(),
            )
        self.stdout.write(self.style.SUCCESS(f"{categories_count} categories created ✅"))
