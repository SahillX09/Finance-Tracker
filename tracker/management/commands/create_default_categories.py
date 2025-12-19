from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Category

class Command(BaseCommand):
    help = 'Creates default categories for all users'

    def handle(self, *args, **kwargs):
        default_categories = [
            # Income categories
            ('Salary', 'income'),
            ('Freelance', 'income'),
            ('Investment Returns', 'income'),
            ('Business', 'income'),
            ('Gift', 'income'),
            ('Other Income', 'income'),
            
            # Expense categories
            ('Food & Dining', 'expense'),
            ('Transportation', 'expense'),
            ('Shopping', 'expense'),
            ('Entertainment', 'expense'),
            ('Bills & Utilities', 'expense'),
            ('Healthcare', 'expense'),
            ('Education', 'expense'),
            ('Rent', 'expense'),
            ('Groceries', 'expense'),
            ('Other Expense', 'expense'),
        ]
        
        users = User.objects.all()
        for user in users:
            for name, cat_type in default_categories:
                Category.objects.get_or_create(
                    name=name,
                    category_type=cat_type,
                    user=user
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully created default categories'))
