from django.db import models
from django.utils import timezone
import uuid

class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class EmissionRecord(models.Model):
    SCOPE_CHOICES = [
        ('Scope 1', 'Scope 1'),
        ('Scope 2', 'Scope 2'),
        ('Scope 3', 'Scope 3'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('LOCKED', 'Locked for Auditing'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='emission_records')
    
    # Source Tracking
    source_system = models.CharField(max_length=100) # e.g. "SAP", "Utility Portal", "Concur"
    ingestion_timestamp = models.DateTimeField(default=timezone.now)
    
    # Data fields
    raw_data = models.JSONField(help_text="The exact raw JSON/dict parsed from the source")
    
    # Normalization
    normalized_unit = models.CharField(max_length=50, default="kg CO2e")
    normalized_value = models.FloatField(null=True, blank=True)
    
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES)
    
    # Workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    last_edited_by = models.CharField(max_length=255, null=True, blank=True)
    last_edited_at = models.DateTimeField(auto_now=True)

    # Some extracted fields to show on the UI easily without parsing JSON
    description = models.CharField(max_length=255, blank=True)
    date_of_activity = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.source_system} - {self.scope} - {self.status}"

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE, related_name='audit_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    changed_by = models.CharField(max_length=255, default="System")
    action = models.CharField(max_length=100) # "CREATED", "UPDATED", "STATUS_CHANGED", "LOCKED"
    previous_state = models.JSONField(null=True, blank=True)
    new_state = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.record.id} - {self.action} at {self.timestamp}"
