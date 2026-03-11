import uuid
from django.db import models

class Applicant(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ADMITTED', 'Admitted'),
        ('REJECTED', 'Rejected'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"