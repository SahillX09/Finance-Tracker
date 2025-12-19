from django.core.management.base import BaseCommand
from tracker.models import Currency

class Command(BaseCommand):
    help = 'Setup default currencies'

    def handle(self, *args, **kwargs):
        currencies = [
            {'code': 'INR', 'name': 'Indian Rupee', 'symbol': '₹'},
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
            {'code': 'GBP', 'name': 'British Pound', 'symbol': '£'},
            {'code': 'JPY', 'name': 'Japanese Yen', 'symbol': '¥'},
        ]
        
        for curr in currencies:
            Currency.objects.get_or_create(
                code=curr['code'],
                defaults={'name': curr['name'], 'symbol': curr['symbol']}
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created currencies'))
