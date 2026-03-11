from django.db import models

class PortalSettings(models.Model):
    current_session = models.CharField(max_length=20, default="2023/2024")
    current_semester = models.CharField(max_length=20, default="First")
    admissions_open = models.BooleanField(default=True)
    course_registration_open = models.BooleanField(default=True)
    result_upload_open = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk and PortalSettings.objects.exists():
            # Enforce Singleton
            self.pk = PortalSettings.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return "Portal Configuration"