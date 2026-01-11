"""
Management command to create initial contact statuses.

Run with: python manage.py create_statuses
"""

from django.core.management.base import BaseCommand
from contacts.models import ContactStatus


class Command(BaseCommand):
    help = 'Creates initial contact statuses'

    def handle(self, *args, **options):
        statuses = [
            {'name': 'new', 'description': 'New contact'},
            {'name': 'in progress', 'description': 'Contact in progress'},
            {'name': 'lost', 'description': 'Lost contact'},
            {'name': 'outdated', 'description': 'Outdated contact'}
        ]

        created_count = 0
        existing_count = 0

        for status_data in statuses:
            status, created = ContactStatus.objects.get_or_create(
                name=status_data['name'],
                defaults={'description': status_data['description']}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created status: {status.name}')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'○ Status already exists: {status.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: {created_count} created, {existing_count} already existed'
            )
        )
