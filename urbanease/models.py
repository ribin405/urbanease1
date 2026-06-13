from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Management'),
        ('RESIDENT', 'Resident'),
        ('SECURITY', 'Security'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='RESIDENT')

    def __str__(self):
        return f"{self.username} ({self.role})"

class ResidentProfile(models.Model):
    OCCUPANT_CHOICES = (
        ('Owner', 'Owner'),
        ('Tenant', 'Tenant'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resident_profile')
    apartment_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    occupant_type = models.CharField(max_length=10, choices=OCCUPANT_CHOICES, default='Owner')

    def __str__(self):
        return f"Resident: {self.user.username} - Apt {self.apartment_number}"

class SecurityProfile(models.Model):
    SHIFT_CHOICES = (
        ('Day', 'Day Shift'),
        ('Night', 'Night Shift'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_profile')
    gate_no = models.CharField(max_length=20)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, default='Day')
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Guard: {self.user.username} - Gate {self.gate_no}"

class ManagementProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='management_profile')
    department = models.CharField(max_length=50, default='Society Management')
    designation = models.CharField(max_length=50, default='Manager')
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Management: {self.user.username} - {self.designation}"

class MaintenanceRequest(models.Model):
    CATEGORY_CHOICES = (
        ('Plumbing', 'Plumbing'),
        ('Electrical', 'Electrical'),
        ('Lift', 'Lift'),
        ('Carpentry', 'Carpentry'),
        ('Others', 'Others'),
    )
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )

    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Others')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.id}: {self.title} ({self.status})"

class VisitorRequest(models.Model):
    STATUS_CHOICES = (
        ('Pre-Registered', 'Pre-Registered'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
    )

    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitor_requests')
    visitor_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    purpose = models.CharField(max_length=200)
    expected_entry = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pre-Registered')
    actual_entry_time = models.DateTimeField(null=True, blank=True)
    actual_exit_time = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_visitors')
    gate_log_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Visitor: {self.visitor_name} to Apt {self.resident.resident_profile.apartment_number if hasattr(self.resident, 'resident_profile') else 'N/A'}"

class EmergencyAlert(models.Model):
    ALERT_CHOICES = (
        ('Fire', 'Fire Alert'),
        ('Medical', 'Medical Emergency'),
        ('Security', 'Security Threat'),
        ('Others', 'Other Emergency'),
    )
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Resolved', 'Resolved'),
    )

    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_CHOICES, default='Others')
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Emergency [{self.alert_type}]: Raised by {self.raised_by.username} ({self.status})"
