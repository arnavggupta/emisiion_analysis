from rest_framework import serializers
from core.models import Tenant, EmissionRecord, AuditLog

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class EmissionRecordSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.name', read_only=True)
    
    class Meta:
        model = EmissionRecord
        fields = '__all__'
        read_only_fields = ['id', 'source_system', 'ingestion_timestamp', 'raw_data', 'normalized_unit']
