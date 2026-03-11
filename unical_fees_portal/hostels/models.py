import uuid
from django.db import models
from django.conf import settings

class Hostel(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('MIXED', 'Mixed'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(default=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MIXED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HostelRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hostel_requests')
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    hostel_name = models.CharField(max_length=255, blank=True, null=True, help_text="Preferred hostel (optional)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    comment = models.TextField(blank=True, null=True, help_text="Reason for rejection or allocation details")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hostel Request - {self.student.username} ({self.status})"