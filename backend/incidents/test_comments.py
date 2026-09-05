from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import Incident, IncidentComment
from .services import change_incident_status


class IncidentCommentAPITests(APITestCase):
    def setUp(self):
        self.incident = Incident.objects.create(
            title='Service unavailable', description='Requests fail.',
            severity='Critical', owner='Operations',
        )
        self.other = Incident.objects.create(
            title='Other incident', description='Other issue.', severity='Low', owner='Other',
        )
        self.payload = {'author': 'Ana', 'content': 'Provider contacted.'}

    def url(self, action, incident=None):
        return reverse(f'incidents:incident-{action}', args=[(incident or self.incident).pk])

    def test_create_persists_comment_on_correct_incident(self):
        response = self.client.post(self.url('comments'), {
            **self.payload, 'incident': self.other.pk,
            'created_at': '2000-01-01T00:00:00Z',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        comment = IncidentComment.objects.get(pk=response.data['id'])
        self.assertEqual(comment.incident_id, self.incident.pk)
        self.assertEqual(comment.author, self.payload['author'])
        self.assertEqual(comment.content, self.payload['content'])
        self.assertIsNotNone(comment.created_at)
        self.assertNotEqual(comment.created_at.year, 2000)
        self.assertEqual(set(response.data), {'id', 'author', 'content', 'created_at'})
        # A separate HTTP request reads the persisted record again.
        listed = self.client.get(self.url('comments'))
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.data, [response.data])
        self.assertEqual(self.client.get(self.url('comments', self.other)).data, [])
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'Open')
        self.assertFalse(self.incident.status_history.exists())

    def test_required_and_nonblank_fields(self):
        for field in ['author', 'content']:
            for value in [None, '', '   ', '\n\t ']:
                with self.subTest(field=field, value=value):
                    response = self.client.post(self.url('comments'), {
                        **self.payload, field: value,
                    }, format='json')
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.data)
            payload = {key: value for key, value in self.payload.items() if key != field}
            response = self.client.post(self.url('comments'), payload, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
        self.assertFalse(IncidentComment.objects.exists())

    def test_author_length_and_whitespace_trimming(self):
        response = self.client.post(self.url('comments'), {
            **self.payload, 'author': 'A' * 256,
        }, format='json')
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.url('comments'), {
            'author': ' Ana ', 'content': ' Provider contacted. \n',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], 'Ana')
        self.assertEqual(response.data['content'], 'Provider contacted.')

    def test_multiple_comments_are_ordered_and_scoped(self):
        ids = []
        for content in ['First', 'Second']:
            response = self.client.post(self.url('comments'), {
                **self.payload, 'content': content,
            }, format='json')
            self.assertEqual(response.status_code, 201)
            ids.append(response.data['id'])
        IncidentComment.objects.create(incident=self.other, **self.payload)
        response = self.client.get(self.url('comments'))
        self.assertEqual([item['id'] for item in response.data], ids)
        self.assertEqual(self.incident.comments.count(), 2)

    def test_timeline_combines_events_chronologically_and_preserves_history(self):
        change_incident_status(self.incident, 'In Progress')
        change_incident_status(self.incident, 'Resolved')
        first, last = self.incident.status_history.order_by('id')
        comment = IncidentComment.objects.create(incident=self.incident, **self.payload)
        start = timezone.now() - timedelta(hours=1)
        self.incident.status_history.filter(pk=first.pk).update(changed_at=start)
        IncidentComment.objects.filter(pk=comment.pk).update(created_at=start + timedelta(minutes=1))
        self.incident.status_history.filter(pk=last.pk).update(changed_at=start + timedelta(minutes=2))
        IncidentComment.objects.create(incident=self.other, **self.payload)
        change_incident_status(self.other, 'Resolved')
        response = self.client.get(self.url('timeline'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([event['type'] for event in response.data], ['status_change', 'comment', 'status_change'])
        times = [event['occurred_at'] for event in response.data]
        self.assertEqual(times, sorted(times))
        self.assertEqual(response.data[0]['previous_status'], 'Open')
        self.assertEqual(response.data[0]['new_status'], 'In Progress')
        self.assertEqual(response.data[1]['author'], 'Ana')
        self.assertEqual(response.data[1]['content'], self.payload['content'])
        self.assertEqual(response.data[2]['new_status'], 'Resolved')
        history = self.client.get(self.url('history'))
        self.assertEqual(history.status_code, 200)
        self.assertEqual(len(history.data), 2)
        self.assertEqual(set(history.data[0]), {'previous_status', 'new_status', 'changed_at'})

    def test_timeline_timestamp_ties_are_deterministic(self):
        comments = [IncidentComment.objects.create(incident=self.incident, **self.payload) for _ in range(2)]
        change_incident_status(self.incident, 'In Progress')
        timestamp = timezone.now()
        self.incident.comments.update(created_at=timestamp)
        self.incident.status_history.update(changed_at=timestamp)
        expected = [('status_change', self.incident.status_history.get().pk)]
        expected.extend(('comment', comment.pk) for comment in comments)
        for _ in range(2):
            response = self.client.get(self.url('timeline'))
            self.assertEqual([(event['type'], event['id']) for event in response.data], expected)

    def test_empty_timeline_and_missing_incident(self):
        self.assertEqual(self.client.get(self.url('timeline')).data, [])
        for action in ['comments', 'timeline']:
            url = reverse(f'incidents:incident-{action}', args=[self.other.pk + 100])
            self.assertEqual(self.client.get(url).status_code, 404)
            if action == 'comments':
                self.assertEqual(self.client.post(url, self.payload, format='json').status_code, 404)
        self.assertFalse(IncidentComment.objects.exists())

    def test_comment_does_not_bypass_critical_rule(self):
        self.client.post(self.url('comments'), self.payload, format='json')
        response = self.client.patch(self.url('status'), {'status': 'Resolved'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.status, 'Open')
        self.assertFalse(self.incident.status_history.exists())
        self.assertEqual([event['type'] for event in self.client.get(self.url('timeline')).data], ['comment'])
