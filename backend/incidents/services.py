from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Incident, IncidentStatusHistory


@transaction.atomic
def change_incident_status(incident, new_status):
    """Validate and persist a status change, returning the updated incident."""
    if new_status not in Incident.Status.values:
        raise ValidationError({'status': 'Status inválido. Use Open, In Progress ou Resolved.'})

    incident = Incident.objects.select_for_update().get(pk=incident.pk)
    previous_status = incident.status

    if new_status == previous_status:
        return incident

    if (
        incident.severity == Incident.Severity.CRITICAL
        and previous_status == Incident.Status.OPEN
        and new_status == Incident.Status.RESOLVED
    ):
        raise ValidationError({
            'status': 'Um incidente Critical deve passar por In Progress antes de ser resolvido.',
        })

    incident.status = new_status
    incident.save(update_fields=['status', 'updated_at'])
    IncidentStatusHistory.objects.create(
        incident=incident,
        previous_status=previous_status,
        new_status=new_status,
    )
    return incident
