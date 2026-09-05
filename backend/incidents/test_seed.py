from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from .models import Incident, IncidentStatusHistory
from .services import change_incident_status


class SeedIncidentsTests(TestCase):
    def run_seed(self):
        output = StringIO()
        call_command('seed_incidents', stdout=output)
        return output.getvalue()

    def assert_seed_records(self):
        self.assertEqual(Incident.objects.count(), 3)
        self.assertEqual(
            list(Incident.objects.order_by('title').values_list('title', 'severity', 'owner', 'status')),
            [
                ('Incorrect customer notification', 'Medium', 'Carla', 'Resolved'),
                ('Payment API instability', 'Critical', 'Ana', 'Open'),
                ('Reconciliation delay', 'High', 'Bruno', 'In Progress'),
            ],
        )
        for incident in Incident.objects.all():
            self.assertTrue(incident.description.strip())
            self.assertIsNotNone(incident.created_at)
            self.assertIsNotNone(incident.updated_at)
        self.assertFalse(IncidentStatusHistory.objects.exists())

    def test_creates_required_records_and_reports_them(self):
        output = self.run_seed()
        self.assert_seed_records()
        for incident in Incident.objects.all():
            self.assertIn(incident.title, output)
        self.assertIn('3 incidentes criados', output)

    def test_repeated_seed_resets_records_and_history_without_duplicates(self):
        self.run_seed()
        expected = list(Incident.objects.order_by('title').values(
            'title', 'description', 'severity', 'owner', 'status',
        ))
        incident = Incident.objects.get(title='Payment API instability')
        change_incident_status(incident, 'In Progress')
        Incident.objects.filter(pk=incident.pk).update(owner='Changed', description='Changed')
        Incident.objects.create(title='Extra', description='Extra incident', severity='Low', owner='Other')
        self.run_seed()
        self.assert_seed_records()
        self.assertEqual(list(Incident.objects.order_by('title').values(
            'title', 'description', 'severity', 'owner', 'status',
        )), expected)

    def test_failure_restores_previous_records_and_history(self):
        incident = Incident.objects.create(
            title='Existing', description='Existing incident', severity='Low', owner='Operations',
        )
        change_incident_status(incident, 'In Progress')
        with patch.object(Incident.objects, 'create', side_effect=RuntimeError('Failed')):
            with self.assertRaises(RuntimeError):
                self.run_seed()
        incident.refresh_from_db()
        self.assertEqual(incident.status, 'In Progress')
        self.assertEqual(Incident.objects.count(), 1)
        self.assertEqual(incident.status_history.count(), 1)
