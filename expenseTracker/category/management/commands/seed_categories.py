# management/commands/seed_categories.py
from django.core.management.base import BaseCommand
from django.db import transaction
from category.models import PredefinedCategory, PredefinedCategoryKeyword

class Command(BaseCommand):
    help = 'Seed predefined categories and their keywords'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Income categories
            income_categories = [
                {
                    'name': 'Salary',
                    'type': 'income',
                    'description': 'Regular salary income',
                    'keywords': ['salary', 'payroll', 'wages', 'pay', 'income']
                },
                {
                    'name': 'Freelance',
                    'type': 'income',
                    'description': 'Freelance and contract work',
                    'keywords': ['freelance', 'contract', 'consulting', 'gig', 'project']
                },
                {
                    'name': 'Investment',
                    'type': 'income',
                    'description': 'Investment returns and dividends',
                    'keywords': ['dividend', 'interest', 'investment', 'returns', 'profit', 'capital gain']
                },
                {
                    'name': 'Business',
                    'type': 'income',
                    'description': 'Business income',
                    'keywords': ['business', 'revenue', 'sales', 'commission']
                }
            ]

            # Expense categories
            expense_categories = [
                {
                    'name': 'Food & Dining',
                    'type': 'expense',
                    'description': 'Food, restaurants, and dining',
                    'keywords': ['foodpanda', 'foodie', 'restaurant', 'dining', 'meal', 'lunch', 'dinner', 'breakfast', 'cafe', 'pizza', 'burger', 'grocery', 'supermarket', 'brunch', 'buffet']
                },
                {
                    'name': 'Transportation',
                    'type': 'expense',
                    'description': 'Transport and travel expenses',
                    'keywords': ['uber', 'pathao', 'taxi', 'bus', 'metro', 'fuel', 'petrol', 'diesel', 'gas', 'parking', 'toll', 'auto', 'rickshaw', 'ovai']
                },
                {
                    'name': 'Shopping',
                    'type': 'expense',
                    'description': 'Retail shopping and purchases',
                    'keywords': ['daraz', 'apex','bata', 'aarong' 'shopping', 'purchase', 'buy', 'retail', 'clothes', 'clothing', 'shoes', 'accessories']
                },
                {
                    'name': 'Entertainment',
                    'type': 'expense',
                    'description': 'Entertainment and leisure',
                    'keywords': ['netflix','chorki', 'movie', 'cinema', 'entertainment', 'game', 'music', 'streaming', 'spotify', 'youtube', 'subscription']
                },
                {
                    'name': 'Healthcare',
                    'type': 'expense',
                    'description': 'Medical and healthcare expenses',
                    'keywords': ['hospital', 'doctor', 'medical', 'medicine', 'pharmacy', 'health', 'clinic', 'treatment', 'insurance']
                },
                {
                    'name': 'Utilities',
                    'type': 'expense',
                    'description': 'Utility bills and services',
                    'keywords': ['electricity', 'water', 'gas', 'internet', 'phone', 'mobile', 'broadband', 'utility', 'bill']
                },
                {
                    'name': 'Education',
                    'type': 'expense',
                    'description': 'Education and learning expenses',
                    'keywords': ['education', 'course', 'training', 'book', 'school', 'college', 'university', 'tuition', 'fee']
                },
                {
                    'name': 'Travel',
                    'type': 'expense',
                    'description': 'Travel and vacation expenses',
                    'keywords': ['travel', 'vacation', 'hotel', 'flight', 'trip', 'tour', 'booking', 'airbnb']
                },
                {
                    'name': 'Personal Care',
                    'type': 'expense',
                    'description': 'Personal care and grooming',
                    'keywords': ['salon', 'haircut', 'beauty', 'cosmetics', 'grooming', 'spa', 'personal care']
                },
                {
                    'name': 'Other',
                    'type': 'expense',
                    'description': 'Miscellaneous expenses',
                    'keywords': ['other', 'miscellaneous', 'misc', 'general']
                }
            ]

            all_categories = income_categories + expense_categories

            created_count = 0
            updated_count = 0

            for cat_data in all_categories:
                keywords = cat_data.pop('keywords', [])
                
                category, created = PredefinedCategory.objects.get_or_create(
                    name=cat_data['name'],
                    type=cat_data['type'],
                    defaults=cat_data
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f"Created category: {category.name}")
                else:
                    updated_count += 1
                    # Update existing category
                    for key, value in cat_data.items():
                        setattr(category, key, value)
                    category.save()
                    self.stdout.write(f"Updated category: {category.name}")

                # Add keywords
                existing_keywords = set(
                    category.keywords.values_list('keyword', flat=True)
                )
                
                for keyword in keywords:
                    if keyword.lower() not in existing_keywords:
                        PredefinedCategoryKeyword.objects.create(
                            predefined_category=category,
                            keyword=keyword.lower(),
                            priority=2 if keyword in ['foodpanda', 'pathao', 'uber', 'ovai', 'daraz', 'pharmacy'] else 1
                        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed categories: {created_count} created, {updated_count} updated'
            )
        )