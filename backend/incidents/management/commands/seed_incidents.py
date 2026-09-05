from django.core.management.base import BaseCommand
from django.db import transaction

from incidents.models import Incident


class Command(BaseCommand):
    help = 'Remove todos os incidentes, históricos e comentários e recria os três incidentes iniciais.'

    def handle(self, *args, **options):
        records = [
            {
                'title': 'Payment API instability',
                'description': 'The payment API is experiencing intermittent failures and elevated response times.',
                'severity': Incident.Severity.CRITICAL,
                'owner': 'Ana',
                'status': Incident.Status.OPEN,
            },
            {
                'title': 'Reconciliation delay',
                'description': 'Transaction reconciliation is delayed while the operations team investigates the processing backlog.',
                'severity': Incident.Severity.HIGH,
                'owner': 'Bruno',
                'status': Incident.Status.IN_PROGRESS,
            },
            {
                'title': 'Incorrect customer notification',
                'description': 'Customers received an incorrect notification. The notification content has been corrected and the issue resolved.',
                'severity': Incident.Severity.MEDIUM,
                'owner': 'Carla',
                'status': Incident.Status.RESOLVED,
            },
        ]

        with transaction.atomic():
            Incident.objects.all().delete()
            for record in records:
                Incident.objects.create(**record)

        self.stdout.write('Incidentes, históricos e comentários anteriores removidos.')
        for record in records:
            self.stdout.write(
                f"Criado: {record['title']} | {record['severity']} | {record['owner']} | {record['status']}"
            )
        self.stdout.write(self.style.SUCCESS('Seed concluído: 3 incidentes criados.'))
