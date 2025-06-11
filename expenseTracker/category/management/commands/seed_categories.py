from django.core.management.base import BaseCommand
from django.db import transaction
from category.models import Category

class Command(BaseCommand):
    help = 'Seed predefined global income and expense categories'

    def handle(self, *args, **options):
        seed_data = [
            # Income categories
            {'name': 'Salary', 'type': 'income', 'description': 'Regular salary income'},
            {'name': 'Freelance', 'type': 'income', 'description': 'Freelance and contract work'},
            {'name': 'Investment', 'type': 'income', 'description': 'Investment returns and dividends'},
            {'name': 'Business', 'type': 'income', 'description': 'Business income'},

            # Expense categories
            {'name': 'Food & Dining', 'type': 'expense', 'description': 'Food, restaurants, and dining'},
            {'name': 'Transportation', 'type': 'expense', 'description': 'Transport and travel expenses'},
            {'name': 'Shopping', 'type': 'expense', 'description': 'Retail shopping and purchases'},
            {'name': 'Entertainment', 'type': 'expense', 'description': 'Entertainment and leisure'},
            {'name': 'Healthcare', 'type': 'expense', 'description': 'Medical and healthcare expenses'},
            {'name': 'Utilities', 'type': 'expense', 'description': 'Utility bills and services'},
            {'name': 'Education', 'type': 'expense', 'description': 'Education and learning expenses'},
            {'name': 'Travel', 'type': 'expense', 'description': 'Travel and vacation expenses'},
            {'name': 'Personal Care', 'type': 'expense', 'description': 'Personal care and grooming'},
            {'name': 'Other', 'type': 'expense', 'description': 'Miscellaneous expenses'}
        ]

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for item in seed_data:
                category, created = Category.objects.get_or_create(
                    name=item['name'],
                    type=item['type'],
                    defaults={
                        'description': item['description'],
                        'is_custom': False,
                        'is_active': True,
                        'user': None
                    }
                )
                if created:
                    created_count += 1
                    self.stdout.write(f"Created: {category.name}")
                else:
                    updated_count += 1
                    self.stdout.write(f"Exists: {category.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded categories — {created_count} created, {updated_count} skipped'
            )
        )