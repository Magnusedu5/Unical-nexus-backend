from django.core.management.base import BaseCommand
from unical_fees_portal.accounts.models import User, StudentProfile, StaffProfile, AdminProfile
from unical_fees_portal.core.models import Faculty, Department

class Command(BaseCommand):
    help = 'Seeds the database with initial data (Faculties, Departments, Users)'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding database...")

        # 1. Create Faculty & Department
        science, _ = Faculty.objects.get_or_create(name="Faculty of Science")
        compsci, _ = Department.objects.get_or_create(name="Computer Science", faculty=science)
        self.stdout.write(f"✅ Created Faculty: {science.name} & Department: {compsci.name}")

        # 2. Create Admin User
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@unical.demo",
                password="Admin@1234",
                role="ADMIN",
                first_name="Super",
                last_name="Admin"
            )
            if not hasattr(admin, 'admin_profile'):
                 AdminProfile.objects.create(user=admin, staff_id="ADMIN001", department="Registry")
            self.stdout.write(f"✅ Created Admin: username='admin'")
        else:
            self.stdout.write("ℹ️  Admin user already exists")

        # 3. Create Staff User
        if not User.objects.filter(username="STF/2024/001").exists():
            staff = User.objects.create_user(
                username="STF/2024/001",
                email="staff@unical.demo",
                password="Staff@1234",
                role="STAFF",
                first_name="John",
                last_name="Doe"
            )
            StaffProfile.objects.create(user=staff, staff_id="STF/2024/001", department="Computer Science")
            self.stdout.write(f"✅ Created Staff: username='STF/2024/001'")
        else:
            self.stdout.write("ℹ️  Staff user already exists")

        # 4. Create Student User
        if not User.objects.filter(username="22/071145217").exists():
            student = User.objects.create_user(
                username="22/071145217",
                email="student@unical.demo",
                password="Demo@1234",
                role="STUDENT",
                first_name="Jane",
                last_name="Student"
            )
            StudentProfile.objects.create(
                user=student,
                matric_number="22/071145217",
                faculty=science.name,
                department=compsci.name,
                level=200
            )
            self.stdout.write(f"✅ Created Student: username='22/071145217'")
        else:
            self.stdout.write("ℹ️  Student user already exists")