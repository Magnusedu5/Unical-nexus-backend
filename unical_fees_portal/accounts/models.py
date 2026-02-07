from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.query import QuerySet

class User(AbstractUser):
    """
    Custom user model inheriting from AbstractUser.
    Specifies user roles (ADMIN, STUDENT) and basic user information.
    """
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STUDENT = 'STUDENT', 'Student'
        STAFF = 'STAFF', 'Staff'

    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.STUDENT)
    email = models.EmailField(unique=True)

    def get_full_name(self) -> str:
        """
        Returns the user's full name.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.username


class StudentProfile(models.Model):
    """
    Profile for users with the STUDENT role.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matric_number = models.CharField(max_length=20, unique=True)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    level = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Student: {self.user.username}"


class AdminProfile(models.Model):
    """
    Profile for users with the ADMIN role.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"Admin: {self.user.username}"
    
class StaffProfile(models.Model):
    """
    Profile for users with the STAFF role.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"Staff: {self.user.username}"