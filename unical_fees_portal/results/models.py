import uuid
from django.db import models
from django.conf import settings
from unical_fees_portal.courses.models import Course

class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    session = models.CharField(max_length=20, default="2023/2024")
    semester = models.CharField(max_length=20, default="First")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['student', 'course', 'session', 'semester']

    def __str__(self):
        return f"{self.student} - {self.course.code} - {self.grade}"