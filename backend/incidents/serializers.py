from rest_framework import serializers

from .models import Incident, IncidentStatusHistory


class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id', 'title', 'description', 'severity', 'owner', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class IncidentStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Incident.Status.choices)


class IncidentFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Incident.Status.choices, required=False)
    severity = serializers.ChoiceField(choices=Incident.Severity.choices, required=False)


class IncidentStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentStatusHistory
        fields = ['previous_status', 'new_status', 'changed_at']
        read_only_fields = fields
