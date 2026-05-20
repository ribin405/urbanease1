import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanease_project.settings')
django.setup()

from urbanease.models import User, ResidentProfile, SecurityProfile, MaintenanceRequest, VisitorRequest, EmergencyAlert

def seed_database():
    print("Starting UrbanEase Database Seeding...")

    # 1. Clean existing records to prevent duplicates
    print("Clearing old data...")
    EmergencyAlert.objects.all().delete()
    VisitorRequest.objects.all().delete()
    MaintenanceRequest.objects.all().delete()
    ResidentProfile.objects.all().delete()
    SecurityProfile.objects.all().delete()
    User.objects.all().delete()

    # 2. Create Admin User
    print("Creating Admin User...")
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@urbanease.com',
        first_name='System',
        last_name='Administrator',
        role='ADMIN'
    )
    admin_user.set_password('admin123')
    admin_user.save()

    # 3. Create Resident Users
    print("Creating Resident Users...")
    res_user1 = User.objects.create_user(
        username='resident',
        email='resident1@gmail.com',
        first_name='Alex',
        last_name='Turner',
        role='RESIDENT'
    )
    res_user1.set_password('resident123')
    res_user1.save()
    ResidentProfile.objects.create(
        user=res_user1,
        apartment_number='A-304',
        phone_number='9876543210',
        occupant_type='Owner'
    )

    res_user2 = User.objects.create_user(
        username='resident2',
        email='resident2@gmail.com',
        first_name='Sarah',
        last_name='Connor',
        role='RESIDENT'
    )
    res_user2.set_password('resident123')
    res_user2.save()
    ResidentProfile.objects.create(
        user=res_user2,
        apartment_number='B-102',
        phone_number='9988776655',
        occupant_type='Tenant'
    )

    res_user3 = User.objects.create_user(
        username='resident3',
        email='resident3@gmail.com',
        first_name='Michael',
        last_name='Scott',
        role='RESIDENT'
    )
    res_user3.set_password('resident123')
    res_user3.save()
    ResidentProfile.objects.create(
        user=res_user3,
        apartment_number='C-405',
        phone_number='9123456789',
        occupant_type='Owner'
    )

    # 4. Create Security Guards
    print("Creating Security Guards...")
    guard_user1 = User.objects.create_user(
        username='guard',
        email='guard1@urbanease.com',
        first_name='Rohan',
        last_name='Sharma',
        role='SECURITY'
    )
    guard_user1.set_password('guard123')
    guard_user1.save()
    SecurityProfile.objects.create(
        user=guard_user1,
        gate_no='Gate 1',
        shift='Day',
        phone_number='8877665544'
    )

    guard_user2 = User.objects.create_user(
        username='guard2',
        email='guard2@urbanease.com',
        first_name='Vikram',
        last_name='Singh',
        role='SECURITY'
    )
    guard_user2.set_password('guard123')
    guard_user2.save()
    SecurityProfile.objects.create(
        user=guard_user2,
        gate_no='Gate 2',
        shift='Night',
        phone_number='7766554433'
    )

    # 5. Create Maintenance Requests
    print("Creating Maintenance Requests...")
    # Alex requests
    MaintenanceRequest.objects.create(
        resident=res_user1,
        title='Water pipe leakage in master bathroom',
        description='The pipe under the sink has a severe crack and water is dripping continuously, flooding the floor.',
        category='Plumbing',
        priority='High',
        status='Pending'
    )
    MaintenanceRequest.objects.create(
        resident=res_user1,
        title='Flickering living room tubelight',
        description='The LED tube light in the living room flickers every 5 minutes. Needs replacement.',
        category='Electrical',
        priority='Low',
        status='Resolved'
    )

    # Sarah requests
    MaintenanceRequest.objects.create(
        resident=res_user2,
        title='Block B lift button stuck',
        description='The ground floor lift button for Block B gets stuck when pressed and does not register floor calls.',
        category='Lift',
        priority='High',
        status='In Progress'
    )

    # Michael requests
    MaintenanceRequest.objects.create(
        resident=res_user3,
        title='Front door wooden latch broken',
        description='The main entrance wooden frame latch is loose and doesn\'t align properly. Needs carpentary work.',
        category='Carpentry',
        priority='Medium',
        status='Pending'
    )

    # 6. Create Visitor Requests
    print("Creating Visitor Passes...")
    now = timezone.now()

    # Pre-registered Visitor in the future
    VisitorRequest.objects.create(
        resident=res_user1,
        visitor_name='Emily Watson',
        phone_number='9871234560',
        purpose='Family Friend Guest Visit',
        expected_entry=now + timedelta(days=1),
        status='Pre-Registered'
    )

    # Visitor Pre-registered for today, already Approved by security
    VisitorRequest.objects.create(
        resident=res_user1,
        visitor_name='John Carter (Courier)',
        phone_number='9922114433',
        purpose='Amazon Parcel Delivery',
        expected_entry=now - timedelta(minutes=30),
        status='Approved',
        approved_by=guard_user1
    )

    # Visitor currently checked-in today
    VisitorRequest.objects.create(
        resident=res_user2,
        visitor_name='Deepak Kumar (Mechanic)',
        phone_number='9898767654',
        purpose='AC Repairing service',
        expected_entry=now - timedelta(hours=2),
        status='Checked In',
        actual_entry_time=now - timedelta(hours=1, minutes=45),
        approved_by=guard_user1,
        gate_log_notes='AC repair technician carrying tool kit.'
    )

    # Historical completed visitor entry (Checked out)
    VisitorRequest.objects.create(
        resident=res_user2,
        visitor_name='Jessica Taylor',
        phone_number='9555112233',
        purpose='Social meeting',
        expected_entry=now - timedelta(days=1, hours=4),
        status='Checked Out',
        actual_entry_time=now - timedelta(days=1, hours=3, minutes=50),
        actual_exit_time=now - timedelta(days=1, hours=1, minutes=10),
        approved_by=guard_user1
    )

    # Rejected visitor
    VisitorRequest.objects.create(
        resident=res_user3,
        visitor_name='Unverified Marketing Agent',
        phone_number='9444123456',
        purpose='Sales pitch',
        expected_entry=now - timedelta(hours=3),
        status='Rejected',
        approved_by=guard_user1,
        gate_log_notes='No prior approval by resident. Resident declined on phone call.'
    )

    # 7. Create Emergency Alerts
    print("Creating active emergency alerts...")
    EmergencyAlert.objects.create(
        raised_by=res_user3,
        alert_type='Fire',
        description='Minor grease fire sparked in kitchen! Smoke detectors went off. Extinguisher used but need immediate guard inspection!',
        status='Active',
        created_at=now - timedelta(minutes=15)
    )

    print("\nUrbanEase Database Seeded Successfully!")
    print("------------------------------------------")
    print(f"Admin Access: admin / admin123")
    print(f"Resident Access: resident / resident123")
    print(f"Security Access: guard / guard123")
    print("------------------------------------------")

if __name__ == '__main__':
    seed_database()
