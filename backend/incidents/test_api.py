from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Incident
from .services import change_incident_status


class IncidentAPITests(APITestCase):
    def setUp(self):
        self.payload = {
            'title': 'Service unavailable', 'description': 'Requests are failing.',
            'severity': 'Critical', 'owner': 'Operations',
        }
        self.incident = Incident.objects.create(**self.payload)
        self.list_url = reverse('incidents:incident-list')

    def incident_url(self, action, pk=None):
        return reverse(f'incidents:incident-{action}', args=[pk or self.incident.pk])

    def test_create_valid_incident(self):
        response = self.client.post(self.list_url, self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        incident = Incident.objects.get(pk=response.data['id'])
        self.assertEqual(incident.status, 'Open')
        self.assertEqual(incident.title, self.payload['title'])
        self.assertIsNotNone(incident.created_at)
        self.assertIsNotNone(incident.updated_at)
        self.assertFalse(incident.status_history.exists())

    def test_create_cannot_override_status_or_timestamps(self):
        response = self.client.post(self.list_url, {
            **self.payload, 'status': 'Resolved',
            'created_at': '2000-01-01T00:00:00Z', 'updated_at': '2000-01-01T00:00:00Z',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        incident = Incident.objects.get(pk=response.data['id'])
        self.assertEqual(incident.status, 'Open')
        self.assertNotEqual(incident.created_at.year, 2000)
        self.assertNotEqual(incident.updated_at.year, 2000)

    def test_invalid_creation(self):
        for field, value in [('title', ''), ('description', ''), ('severity', 'Unknown'), ('owner', '')]:
            with self.subTest(field=field):
                response = self.client.post(self.list_url, {**self.payload, field: value}, format='json')
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
        response = self.client.post(self.list_url, {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data), set(self.payload))
        self.assertEqual(Incident.objects.count(), 1)

    def test_list_incidents(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['id'] for item in response.data], [self.incident.pk])
        for field in ['title', 'severity', 'owner', 'status']:
            self.assertEqual(response.data[0][field], getattr(self.incident, field))

    def test_filters(self):
        other = Incident.objects.create(**{**self.payload, 'severity': 'Low'})
        change_incident_status(other, 'Resolved')
        cases = [
            ({'status': 'Open'}, [self.incident.pk]),
            ({'severity': 'Low'}, [other.pk]),
            ({'status': 'Open', 'severity': 'Critical'}, [self.incident.pk]),
            ({'status': 'Resolved', 'severity': 'Critical'}, []),
        ]
        for params, expected in cases:
            with self.subTest(params=params):
                response = self.client.get(self.list_url, params)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([item['id'] for item in response.data], expected)

    def test_invalid_filters(self):
        for field in ['status', 'severity']:
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: 'Unknown'})
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)

    def test_details(self):
        response = self.client.get(self.incident_url('detail'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data), {
            'id', 'title', 'description', 'severity', 'owner', 'status', 'created_at', 'updated_at',
        })
        self.assertEqual(response.data['id'], self.incident.pk)
        for field, value in self.payload.items():
            self.assertEqual(response.data[field], value)

    def test_valid_status_change_uses_service(self):
        original_updated_at = self.incident.updated_at
        with patch('incidents.views.change_incident_status', wraps=change_incident_status) as service:
            response = self.client.patch(self.incident_url('status'), {'status': 'In Progress'}, format='json')
        self.assertEqual(response.status_code, 200)
        service.assert_called_once()
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'In Progress')
        self.assertEqual(response.data['status'], 'In Progress')
        self.assertGreater(self.incident.updated_at, original_updated_at)
        history = self.incident.status_history.get()
        self.assertEqual((history.previous_status, history.new_status), ('Open', 'In Progress'))
        response = self.client.patch(self.incident_url('status'), {'status': 'Resolved'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'Resolved')

    def test_invalid_critical_transition(self):
        response = self.client.patch(self.incident_url('status'), {'status': 'Resolved'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('In Progress', str(response.data['status']))
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'Open')
        self.assertFalse(self.incident.status_history.exists())

    def test_invalid_status_input(self):
        for payload in [{}, {'status': 'Unknown'}, {'status': None}]:
            with self.subTest(payload=payload):
                response = self.client.patch(self.incident_url('status'), payload, format='json')
                self.assertEqual(response.status_code, 400)
                self.assertIn('status', response.data)
        self.assertFalse(self.incident.status_history.exists())

    def test_repeated_status_does_not_duplicate_history(self):
        url = self.incident_url('status')
        self.client.patch(url, {'status': 'In Progress'}, format='json')
        self.incident.refresh_from_db()
        original_updated_at = self.incident.updated_at
        response = self.client.patch(url, {'status': 'In Progress'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.updated_at, original_updated_at)
        self.assertEqual(self.incident.status_history.count(), 1)

    def test_history_is_ordered_and_scoped_to_incident(self):
        change_incident_status(self.incident, 'In Progress')
        change_incident_status(self.incident, 'Resolved')
        other = Incident.objects.create(**self.payload)
        change_incident_status(other, 'In Progress')
        response = self.client.get(self.incident_url('history'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [(item['previous_status'], item['new_status']) for item in response.data],
            [('Open', 'In Progress'), ('In Progress', 'Resolved')],
        )
        for item in response.data:
            self.assertEqual(set(item), {'previous_status', 'new_status', 'changed_at'})
            self.assertIsNotNone(item['changed_at'])

    def test_empty_history(self):
        response = self.client.get(self.incident_url('history'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_missing_incident_returns_404(self):
        for action in ['detail', 'history', 'status']:
            with self.subTest(action=action):
                url = self.incident_url(action, self.incident.pk + 100)
                response = (
                    self.client.patch(url, {'status': 'In Progress'}, format='json')
                    if action == 'status' else self.client.get(url)
                )
                self.assertEqual(response.status_code, 404)

    def test_dashboard(self):
        for severity, status in [
            ('Critical', 'In Progress'), ('Critical', 'Resolved'),
            ('Low', 'Open'), ('High', 'Resolved'), ('Medium', 'In Progress'),
        ]:
            Incident.objects.create(**{**self.payload, 'severity': severity, 'status': status})
        response = self.client.get(reverse('incidents:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'open_count': 2, 'critical_unresolved_count': 2, 'resolved_count': 2,
        })
        for new_status, expected in [
            ('In Progress', {'open_count': 1, 'critical_unresolved_count': 2, 'resolved_count': 2}),
            ('Resolved', {'open_count': 1, 'critical_unresolved_count': 1, 'resolved_count': 3}),
        ]:
            with self.subTest(status=new_status):
                update = self.client.patch(
                    self.incident_url('status'), {'status': new_status}, format='json',
                )
                self.assertEqual(update.status_code, 200)
                response = self.client.get(reverse('incidents:dashboard'))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data, expected)

    def test_empty_dashboard(self):
        Incident.objects.all().delete()
        response = self.client.get(reverse('incidents:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'open_count': 0, 'critical_unresolved_count': 0, 'resolved_count': 0,
        })

    def test_detail_does_not_allow_generic_updates_or_deletion(self):
        url = self.incident_url('detail')
        self.assertEqual(self.client.patch(url, {'status': 'Resolved'}).status_code, 405)
        self.assertEqual(self.client.put(url, self.payload).status_code, 405)
        self.assertEqual(self.client.delete(url).status_code, 405)
