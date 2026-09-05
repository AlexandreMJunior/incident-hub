from datetime import timedelta
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Incident, IncidentStatusHistory
from .services import change_incident_status


class ChangeIncidentStatusTests(TestCase):
    def setUp(self):
        self.incident = Incident.objects.create(
            title='Service unavailable',
            description='Requests are failing.',
            severity=Incident.Severity.CRITICAL,
            owner='Operations',
        )

    def test_critical_cannot_be_resolved_directly(self):
        original_updated_at = self.incident.updated_at
        with self.assertRaisesMessage(ValidationError, 'In Progress'):
            change_incident_status(self.incident, Incident.Status.RESOLVED)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, Incident.Status.OPEN)
        self.assertEqual(self.incident.updated_at, original_updated_at)
        self.assertFalse(self.incident.status_history.exists())

    def test_critical_can_progress_then_resolve_using_persisted_status(self):
        old_time = timezone.now() - timedelta(days=1)
        Incident.objects.filter(pk=self.incident.pk).update(updated_at=old_time)
        change_incident_status(self.incident, Incident.Status.IN_PROGRESS)
        # The original instance is stale; the service must read the saved status.
        result = change_incident_status(self.incident, Incident.Status.RESOLVED)
        self.incident.refresh_from_db()
        self.assertEqual(result.status, Incident.Status.RESOLVED)
        self.assertEqual(self.incident.status, Incident.Status.RESOLVED)
        self.assertGreater(self.incident.updated_at, old_time)
        history = list(self.incident.status_history.order_by('id'))
        self.assertEqual(
            [(entry.previous_status, entry.new_status) for entry in history],
            [('Open', 'In Progress'), ('In Progress', 'Resolved')],
        )
        self.assertTrue(all(entry.changed_at is not None for entry in history))

    def test_noncritical_can_be_resolved_directly(self):
        for severity in [Incident.Severity.LOW, Incident.Severity.MEDIUM, Incident.Severity.HIGH]:
            with self.subTest(severity=severity):
                incident = Incident.objects.create(
                    title='Issue', description='Details', severity=severity, owner='Operations',
                )
                change_incident_status(incident, Incident.Status.RESOLVED)
                incident.refresh_from_db()
                self.assertEqual(incident.status, Incident.Status.RESOLVED)
                self.assertEqual(incident.status_history.count(), 1)

    def test_repeated_status_does_not_create_history_or_update_timestamp(self):
        incident = change_incident_status(self.incident, Incident.Status.IN_PROGRESS)
        original_updated_at = incident.updated_at
        change_incident_status(incident, Incident.Status.IN_PROGRESS)
        incident.refresh_from_db()
        self.assertEqual(incident.status_history.count(), 1)
        self.assertEqual(incident.updated_at, original_updated_at)

    def test_unknown_status_is_rejected_without_changes(self):
        with self.assertRaisesMessage(ValidationError, 'Status inválido'):
            change_incident_status(self.incident, 'Closed')
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, Incident.Status.OPEN)
        self.assertFalse(self.incident.status_history.exists())

    def test_history_failure_rolls_back_status_and_timestamp(self):
        original_updated_at = self.incident.updated_at
        with patch.object(IncidentStatusHistory.objects, 'create', side_effect=RuntimeError('Failed')):
            with self.assertRaises(RuntimeError):
                change_incident_status(self.incident, Incident.Status.IN_PROGRESS)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, Incident.Status.OPEN)
        self.assertEqual(self.incident.updated_at, original_updated_at)
        self.assertFalse(self.incident.status_history.exists())
