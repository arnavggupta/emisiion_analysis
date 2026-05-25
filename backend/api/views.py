from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Tenant, EmissionRecord, AuditLog
from .serializers import TenantSerializer, EmissionRecordSerializer, AuditLogSerializer
from django.utils import timezone

class TenantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class EmissionRecordViewSet(viewsets.ModelViewSet):
    queryset = EmissionRecord.objects.all().order_by('-ingestion_timestamp')
    serializer_class = EmissionRecordSerializer

    def perform_update(self, serializer):
        # We need to track the audit log if state changes
        instance = self.get_object()
        old_status = instance.status
        old_value = instance.normalized_value

        updated_instance = serializer.save(last_edited_at=timezone.now())

        if old_status != updated_instance.status or old_value != updated_instance.normalized_value:
            # Determine action
            action_name = "UPDATED"
            if old_status != updated_instance.status:
                action_name = "STATUS_CHANGED"
                if updated_instance.status == "LOCKED":
                    action_name = "LOCKED"

            AuditLog.objects.create(
                record=updated_instance,
                changed_by=updated_instance.last_edited_by or "Analyst",
                action=action_name,
                previous_state={"status": old_status, "normalized_value": old_value},
                new_state={"status": updated_instance.status, "normalized_value": updated_instance.normalized_value}
            )

    @action(detail=True, methods=['get'])
    def audit_logs(self, request, pk=None):
        record = self.get_object()
        logs = record.audit_logs.all().order_by('-timestamp')
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data)
