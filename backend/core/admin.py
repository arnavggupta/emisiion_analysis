from django.contrib import admin
from .models import Tenant, EmissionRecord, AuditLog

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ('source_system', 'scope', 'status', 'normalized_value', 'tenant')
    list_filter = ('status', 'scope', 'source_system', 'tenant')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('record', 'action', 'timestamp', 'changed_by')
    list_filter = ('action', 'timestamp')
