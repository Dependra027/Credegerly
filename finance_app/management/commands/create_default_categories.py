"""
Management command to create default expense categories
"""
from django.core.management.base import BaseCommand
from finance_app.models import Category


class Command(BaseCommand):
    help = 'Creates default expense categories'

    def handle(self, *args, **options):
        default_categories = [
            {'name': 'Food & Dining', 'icon': '🍽️', 'description': 'Restaurants, groceries, and food delivery'},
            {'name': 'Transportation', 'icon': '🚗', 'description': 'Gas, public transport, car maintenance'},
            {'name': 'Shopping', 'icon': '🛍️', 'description': 'Clothing, electronics, general shopping'},
            {'name': 'Bills & Utilities', 'icon': '💡', 'description': 'Electricity, water, internet, phone bills'},
            {'name': 'Entertainment', 'icon': '🎬', 'description': 'Movies, games, subscriptions'},
            {'name': 'Healthcare', 'icon': '🏥', 'description': 'Medical expenses, pharmacy, insurance'},
            {'name': 'Education', 'icon': '📚', 'description': 'Courses, books, tuition'},
            {'name': 'Travel', 'icon': '✈️', 'description': 'Hotels, flights, vacation expenses'},
            {'name': 'Personal Care', 'icon': '💅', 'description': 'Haircuts, cosmetics, personal items'},
            {'name': 'Gifts & Donations', 'icon': '🎁', 'description': 'Gifts, charity, donations'},
            {'name': 'Home & Garden', 'icon': '🏠', 'description': 'Furniture, home improvement, gardening'},
            {'name': 'Other', 'icon': '📦', 'description': 'Miscellaneous expenses'},
        ]

        created_count = 0
        for cat_data in default_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'description': cat_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new categories!')
        )











