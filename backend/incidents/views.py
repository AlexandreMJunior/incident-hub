from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Incident
from .serializers import (
    IncidentCommentSerializer,
    IncidentFilterSerializer,
    IncidentSerializer,
    IncidentStatusHistorySerializer,
    IncidentStatusSerializer,
    IncidentTimelineSerializer,
)
from .services import change_incident_status


class IncidentListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentSerializer

    def get_queryset(self):
        filters = IncidentFilterSerializer(data=self.request.query_params)
        filters.is_valid(raise_exception=True)
        return Incident.objects.filter(**filters.validated_data).order_by('id')


class IncidentDetailView(generics.RetrieveAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class IncidentStatusView(APIView):
    def patch(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        serializer = IncidentStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            incident = change_incident_status(incident, serializer.validated_data['status'])
        except DjangoValidationError as error:
            raise ValidationError(error.message_dict) from error
        return Response(IncidentSerializer(incident).data)


class IncidentHistoryView(generics.ListAPIView):
    serializer_class = IncidentStatusHistorySerializer

    def get_queryset(self):
        incident = get_object_or_404(Incident, pk=self.kwargs['pk'])
        return incident.status_history.order_by('changed_at', 'id')


class IncidentCommentListCreateView(generics.ListCreateAPIView):
    serializer_class = IncidentCommentSerializer

    def get_queryset(self):
        incident = get_object_or_404(Incident, pk=self.kwargs['pk'])
        return incident.comments.order_by('created_at', 'id')

    def perform_create(self, serializer):
        incident = get_object_or_404(Incident, pk=self.kwargs['pk'])
        serializer.save(incident=incident)


class IncidentTimelineView(APIView):
    def get(self, request, pk):
        incident = get_object_or_404(Incident, pk=pk)
        events = [
            {
                'id': entry.pk, 'type': 'status_change', 'occurred_at': entry.changed_at,
                'previous_status': entry.previous_status, 'new_status': entry.new_status,
            }
            for entry in incident.status_history.all()
        ]
        events.extend(
            {
                'id': comment.pk, 'type': 'comment', 'occurred_at': comment.created_at,
                'author': comment.author, 'content': comment.content,
            }
            for comment in incident.comments.all()
        )
        # Timestamp ties have a stable order: status changes, then comments, then ID.
        events.sort(key=lambda event: (
            event['occurred_at'], event['type'] == 'comment', event['id'],
        ))
        return Response(IncidentTimelineSerializer(events, many=True).data)


class DashboardView(APIView):
    def get(self, request):
        counts = Incident.objects.aggregate(
            open_count=Count('id', filter=Q(status=Incident.Status.OPEN)),
            critical_unresolved_count=Count(
                'id',
                filter=Q(severity=Incident.Severity.CRITICAL) & ~Q(status=Incident.Status.RESOLVED),
            ),
            resolved_count=Count('id', filter=Q(status=Incident.Status.RESOLVED)),
        )
        return Response(counts)
