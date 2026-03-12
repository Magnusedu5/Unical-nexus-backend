import os
import django

def seed():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unical_fees_portal.settings')
    django.setup()

    from django.contrib.auth import get_user_model
    from unical_fees_portal.accounts.models import StudentProfile, AdminProfile, StaffProfile

    User = get_user_model()

    print("Checking for initial data...")

    # --- Create Student ---
    if not User.objects.filter(username='student').exists():
        print("Creating student user...")
        student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            role=User.Roles.STUDENT
        )
        # Create the profile
        StudentProfile.objects.create(
            user=student,
            matric_number='CSC/2024/001',
            faculty='Physical Sciences',
            department='Computer Science',
            level=100
        )
        print("✅ Student user created.")
    else:
        student = User.objects.get(username='student')
        student.set_password('password123')
        student.save()
        print("ℹ️ Student user updated (password reset).")

    # --- Create Admin ---
    if not User.objects.filter(username='admin').exists():
        print("Creating admin user...")
        admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123',
            first_name='Super',
            last_name='Admin',
            role=User.Roles.ADMIN,
            is_staff=True,
            is_superuser=True
        )
        # Create the profile
        AdminProfile.objects.create(
            user=admin,
            staff_id='ADMIN001',
            department='Registry'
        )
        print("✅ Admin user created.")
    else:
        admin = User.objects.get(username='admin')
        admin.set_password('password123')
        admin.save()
        if not AdminProfile.objects.filter(user=admin).exists():
            AdminProfile.objects.create(
                user=admin,
                staff_id='ADMIN001',
                department='Registry'
            )
        print("ℹ️ Admin user updated (password reset).")

    # --- Create Staff ---
    if not User.objects.filter(username='staff').exists():
        print("Creating staff user...")
        staff = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='password123',
            first_name='Academic',
            last_name='Staff',
            role=User.Roles.STAFF
        )
        # Create the profile
        StaffProfile.objects.create(
            user=staff,
            staff_id='STAFF001',
            department='Computer Science'
        )
        print("✅ Staff user created.")
    else:
        staff = User.objects.get(username='staff')
        staff.set_password('password123')
        staff.save()
        print("ℹ️ Staff user updated (password reset).")

if __name__ == '__main__':
    seed()