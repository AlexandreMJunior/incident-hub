from rest_framework import serializers

from .models import Incident, IncidentComment, IncidentStatusHistory


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


class IncidentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentComment
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


class IncidentTimelineSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    occurred_at = serializers.DateTimeField(read_only=True)
    previous_status = serializers.CharField(read_only=True)
    new_status = serializers.CharField(read_only=True)
    author = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)
