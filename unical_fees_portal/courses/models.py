import uuid
from django.db import models
from unical_fees_portal.core.models import Department

class Course(models.Model):
    SEMESTER_CHOICES = (
        ('First', 'First'),
        ('Second', 'Second'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True) # e.g., CSC101
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    level = models.PositiveIntegerField() # e.g., 100, 200
    units = models.PositiveIntegerField(default=1)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, default='First')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"