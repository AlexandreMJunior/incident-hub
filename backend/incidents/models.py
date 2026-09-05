from django.db import models


class Incident(models.Model):
    class Severity(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'
        CRITICAL = 'Critical', 'Critical'

    class Status(models.TextChoices):
        OPEN = 'Open', 'Open'
        IN_PROGRESS = 'In Progress', 'In Progress'
        RESOLVED = 'Resolved', 'Resolved'

    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=8, choices=Severity.choices)
    owner = models.CharField(max_length=255)
    status = models.CharField(
        max_length=11, choices=Status.choices, default=Status.OPEN,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class IncidentStatusHistory(models.Model):
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name='status_history',
    )
    previous_status = models.CharField(max_length=11, choices=Incident.Status.choices)
    new_status = models.CharField(max_length=11, choices=Incident.Status.choices)
    changed_at = models.DateTimeField(auto_now_add=True)
