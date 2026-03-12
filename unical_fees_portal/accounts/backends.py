from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import StudentProfile, AdminProfile, StaffProfile

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    """
    Custom authentication backend to allow users to log in
    using their email, matric number, or staff ID.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Overrides the default authenticate method to allow for various login identifiers.
        """
        if username is None:
            username = kwargs.get('email') or kwargs.get('username')
            
        if not username:
            return None

        try:
            # Try to fetch the user by username, email, matric number, or staff id.
            # The 'username' parameter from the login form can be any of these.
            user = User.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).first()

            if not user:
                # If no user is found, check student or admin profiles
                student_profile = StudentProfile.objects.filter(matric_number__iexact=username).first()
                if student_profile:
                    user = student_profile.user
                else:
                    admin_profile = AdminProfile.objects.filter(staff_id__iexact=username).first()
                    if admin_profile:
                        user = admin_profile.user
                    else:
                        staff_profile = StaffProfile.objects.filter(staff_id__iexact=username).first()
                        if staff_profile:
                            user = staff_profile.user

            # If a user is found, check the password
            # Also check if the user is active (standard Django behavior)
            if user and user.check_password(password) and self.user_can_authenticate(user):
                return user

        except Exception:
            # Catch unexpected errors to prevent 500s
            return None
