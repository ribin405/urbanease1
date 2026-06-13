from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count
from .models import User, ResidentProfile, SecurityProfile, ManagementProfile, MaintenanceRequest, VisitorRequest, EmergencyAlert
from .decorators import role_required

# ==========================================
# AUTHENTICATION VIEWS
# ==========================================

LOGIN_ROLE_LABELS = {
    'RESIDENT': 'Resident',
    'SECURITY': 'Security',
    'ADMIN': 'Management',
}

def ensure_profile_for_role(user):
    if user.role == 'ADMIN':
        ManagementProfile.objects.get_or_create(
            user=user,
            defaults={
                'department': 'Society Management',
                'designation': 'Manager',
                'phone_number': '',
            },
        )

def login_view(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        requested_role = request.POST.get('role')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            if requested_role in LOGIN_ROLE_LABELS and user.role != requested_role:
                messages.error(request, f"Please use the {LOGIN_ROLE_LABELS.get(user.role, 'correct')} login button for this account.")
                return redirect('login')
            ensure_profile_for_role(user)
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('login_redirect')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'auth/login.html', {'login_roles': LOGIN_ROLE_LABELS})

def register_resident_view(request):
    if request.user.is_authenticated:
        return redirect('login_redirect')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Resident-specific profile info
        apt = request.POST.get('apartment_number')
        phone = request.POST.get('phone_number')
        occ_type = request.POST.get('occupant_type')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, "Username already exists.")
        elif not apt or not phone:
            messages.error(request, "Apartment number and Phone number are required.")
        else:
            # Create user
            user = User.objects.create_user(username=u, password=p, email=email, first_name=first_name, last_name=last_name, role='RESIDENT')
            # Create profile
            ResidentProfile.objects.create(user=user, apartment_number=apt, phone_number=phone, occupant_type=occ_type)
            
            login(request, user)
            messages.success(request, "Registration successful! Welcome to UrbanEase.")
            return redirect('resident_dashboard')
            
    return render(request, 'auth/register.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def login_redirect(request):
    """Redirects users to their respective dashboards based on roles."""
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'SECURITY':
        return redirect('security_dashboard')
    elif request.user.role == 'RESIDENT':
        return redirect('resident_dashboard')
    else:
        # Fallback
        return redirect('login')


# ==========================================
# RESIDENT PORTAL VIEWS
# ==========================================

@login_required
@role_required('RESIDENT')
def resident_dashboard(request):
    user = request.user
    profile = getattr(user, 'resident_profile', None)
    
    # Statistics
    total_maintenance = MaintenanceRequest.objects.filter(resident=user).count()
    pending_maintenance = MaintenanceRequest.objects.filter(resident=user, status='Pending').count()
    total_visitors = VisitorRequest.objects.filter(resident=user).count()
    
    # Recent requests
    recent_requests = MaintenanceRequest.objects.filter(resident=user).order_by('-created_at')[:3]
    recent_visitors = VisitorRequest.objects.filter(resident=user).order_by('-expected_entry')[:3]
    
    # Active alerts (global to society)
    active_alerts = EmergencyAlert.objects.filter(status='Active').order_by('-created_at')[:5]

    context = {
        'profile': profile,
        'total_maintenance': total_maintenance,
        'pending_maintenance': pending_maintenance,
        'total_visitors': total_visitors,
        'recent_requests': recent_requests,
        'recent_visitors': recent_visitors,
        'active_alerts': active_alerts,
    }
    return render(request, 'resident/dashboard.html', context)

@login_required
@role_required('RESIDENT')
def resident_maintenance(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        priority = request.POST.get('priority')
        description = request.POST.get('description')
        
        MaintenanceRequest.objects.create(
            resident=request.user,
            title=title,
            category=category,
            priority=priority,
            description=description
        )
        messages.success(request, "Maintenance request submitted successfully!")
        return redirect('resident_maintenance')
        
    requests_list = MaintenanceRequest.objects.filter(resident=request.user).order_by('-created_at')
    context = {
        'requests_list': requests_list,
        'categories': MaintenanceRequest.CATEGORY_CHOICES,
        'priorities': MaintenanceRequest.PRIORITY_CHOICES,
    }
    return render(request, 'resident/maintenance.html', context)

@login_required
@role_required('RESIDENT')
def resident_visitors(request):
    if request.method == 'POST':
        name = request.POST.get('visitor_name')
        phone = request.POST.get('phone_number')
        purpose = request.POST.get('purpose')
        expected_entry = request.POST.get('expected_entry')
        
        VisitorRequest.objects.create(
            resident=request.user,
            visitor_name=name,
            phone_number=phone,
            purpose=purpose,
            expected_entry=expected_entry
        )
        messages.success(request, "Visitor pre-registered successfully!")
        return redirect('resident_visitors')
        
    visitors_list = VisitorRequest.objects.filter(resident=request.user).order_by('-expected_entry')
    context = {
        'visitors_list': visitors_list,
    }
    return render(request, 'resident/visitors.html', context)

@login_required
@role_required('RESIDENT')
def resident_alerts(request):
    if request.method == 'POST':
        alert_type = request.POST.get('alert_type')
        description = request.POST.get('description')
        
        EmergencyAlert.objects.create(
            raised_by=request.user,
            alert_type=alert_type,
            description=description
        )
        messages.error(request, "EMERGENCY ALERT RAISED! Security guards and Admins have been notified.")
        return redirect('resident_dashboard')
    return redirect('resident_dashboard')

@login_required
@role_required('RESIDENT')
def resident_profile(request):
    profile = get_object_or_404(ResidentProfile, user=request.user)
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        profile.phone_number = request.POST.get('phone_number')
        profile.apartment_number = request.POST.get('apartment_number')
        profile.occupant_type = request.POST.get('occupant_type')
        profile.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('resident_profile')
        
    return render(request, 'resident/profile.html', {'profile': profile})


# ==========================================
# SECURITY PORTAL VIEWS
# ==========================================

@login_required
@role_required('SECURITY')
def security_dashboard(request):
    # Active emergency alerts
    active_alerts = EmergencyAlert.objects.filter(status='Active').order_by('-created_at')
    
    # Today's Visitor Requests (Pre-registered or Approved or Checked In)
    today = timezone.localdate()
    visitors = VisitorRequest.objects.filter(
        expected_entry__date=today
    ).order_by('-expected_entry')
    
    # Quick analytics for Security charts
    status_counts = VisitorRequest.objects.values('status').annotate(count=Count('id'))
    stats = {item['status']: item['count'] for item in status_counts}
    visitor_stats = {
        'pre_registered': stats.get('Pre-Registered', 0),
        'approved': stats.get('Approved', 0),
        'checked_in': stats.get('Checked In', 0),
        'checked_out': stats.get('Checked Out', 0),
        'rejected': stats.get('Rejected', 0),
    }
    
    # Walk-in Registration form also handled here or on the page
    if request.method == 'POST':
        # Handled in security_walk_in view for cleanliness
        pass

    context = {
        'active_alerts': active_alerts,
        'visitors': visitors,
        'visitor_stats': visitor_stats,
    }
    return render(request, 'security/dashboard.html', context)

@login_required
@role_required('SECURITY')
def security_walk_in(request):
    if request.method == 'POST':
        name = request.POST.get('visitor_name')
        phone = request.POST.get('phone_number')
        purpose = request.POST.get('purpose')
        apt_no = request.POST.get('apartment_number')
        
        # Find resident by apartment number
        profile = ResidentProfile.objects.filter(apartment_number=apt_no).first()
        if not profile:
            messages.error(request, f"No resident found in Apartment {apt_no}")
            return redirect('security_dashboard')
            
        VisitorRequest.objects.create(
            resident=profile.user,
            visitor_name=name,
            phone_number=phone,
            purpose=purpose,
            expected_entry=timezone.now(),
            status='Checked In',
            actual_entry_time=timezone.now(),
            approved_by=request.user,
            gate_log_notes="Walk-in registered by security guard."
        )
        messages.success(request, f"Walk-in visitor {name} logged and Checked In!")
    return redirect('security_dashboard')

@login_required
@role_required('SECURITY')
def security_visitor_action(request, pk, action):
    visitor = get_object_or_404(VisitorRequest, pk=pk)
    next_page = request.GET.get('next')
    redirect_target = next_page if next_page in {'security_dashboard', 'security_gate_logs'} else 'security_dashboard'
    
    if action == 'approve':
        visitor.status = 'Approved'
        visitor.approved_by = request.user
        messages.success(request, f"Visitor {visitor.visitor_name} APPROVED.")
    elif action == 'reject':
        visitor.status = 'Rejected'
        visitor.approved_by = request.user
        messages.error(request, f"Visitor {visitor.visitor_name} REJECTED.")
    elif action == 'checkin':
        visitor.status = 'Checked In'
        visitor.actual_entry_time = timezone.now()
        visitor.approved_by = request.user
        messages.success(request, f"Visitor {visitor.visitor_name} CHECKED IN.")
    elif action == 'checkout':
        visitor.status = 'Checked Out'
        visitor.actual_exit_time = timezone.now()
        messages.info(request, f"Visitor {visitor.visitor_name} CHECKED OUT.")
        
    visitor.save()
    return redirect(redirect_target)

@login_required
@role_required('SECURITY')
def security_gate_logs(request):
    logs = VisitorRequest.objects.all().order_by('-expected_entry')
    return render(request, 'security/gate_logs.html', {'logs': logs})


# ==========================================
# ADMIN PORTAL VIEWS
# ==========================================

@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    # Total user counts
    residents_count = User.objects.filter(role='RESIDENT').count()
    security_count = User.objects.filter(role='SECURITY').count()
    
    # Active emergency alerts
    active_alerts = EmergencyAlert.objects.filter(status='Active').order_by('-created_at')
    
    # Maintenance Statistics by category
    m_categories = MaintenanceRequest.objects.values('category').annotate(count=Count('id'))
    category_data = {item['category']: item['count'] for item in m_categories}
    
    # Maintenance Status breakdown
    m_statuses = MaintenanceRequest.objects.values('status').annotate(count=Count('id'))
    status_data = {item['status']: item['count'] for item in m_statuses}
    
    # Visitor statistics
    v_statuses = VisitorRequest.objects.values('status').annotate(count=Count('id'))
    visitor_data = {item['status']: item['count'] for item in v_statuses}
    visitor_stats = {
        'pre_registered': visitor_data.get('Pre-Registered', 0),
        'approved': visitor_data.get('Approved', 0),
        'checked_in': visitor_data.get('Checked In', 0),
        'checked_out': visitor_data.get('Checked Out', 0),
        'rejected': visitor_data.get('Rejected', 0),
    }

    context = {
        'residents_count': residents_count,
        'security_count': security_count,
        'active_alerts': active_alerts,
        'category_data': category_data,
        'status_data': status_data,
        'visitor_stats': visitor_stats,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@role_required('ADMIN')
def admin_users(request):
    residents = ResidentProfile.objects.all().select_related('user')
    security_guards = SecurityProfile.objects.all().select_related('user')
    
    # Form to add a new security guard
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_security':
            u = request.POST.get('username')
            p = request.POST.get('password')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gate = request.POST.get('gate_no')
            shift = request.POST.get('shift')
            phone = request.POST.get('phone_number')
            
            if User.objects.filter(username=u).exists():
                messages.error(request, "Username already exists.")
            elif not gate or not phone:
                messages.error(request, "Gate Number and Phone Number are required.")
            else:
                user = User.objects.create_user(username=u, password=p, email=email, first_name=first_name, last_name=last_name, role='SECURITY')
                SecurityProfile.objects.create(user=user, gate_no=gate, shift=shift, phone_number=phone)
                messages.success(request, f"Security Guard {u} registered successfully!")
                return redirect('admin_users')
                
        elif action == 'delete_user':
            user_id = request.POST.get('user_id')
            user_to_del = get_object_or_404(User, id=user_id)
            if user_to_del == request.user:
                messages.error(request, "You cannot delete yourself.")
            else:
                username = user_to_del.username
                user_to_del.delete()
                messages.warning(request, f"User {username} has been deleted.")
                return redirect('admin_users')

    context = {
        'residents': residents,
        'security_guards': security_guards,
    }
    return render(request, 'admin/users.html', context)

@login_required
@role_required('ADMIN')
def admin_maintenance(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        m_req = get_object_or_404(MaintenanceRequest, id=request_id)
        m_req.status = new_status
        m_req.save()
        messages.success(request, f"Maintenance Request #{request_id} updated to {new_status}!")
        return redirect('admin_maintenance')
        
    requests_list = MaintenanceRequest.objects.all().order_by('-created_at')
    context = {
        'requests_list': requests_list,
    }
    return render(request, 'admin/maintenance_list.html', context)

@login_required
@role_required('ADMIN')
def admin_visitors(request):
    visitors_list = VisitorRequest.objects.all().order_by('-expected_entry')
    return render(request, 'admin/visitor_list.html', {'visitors_list': visitors_list})

@login_required
@role_required('ADMIN')
def admin_resolve_alert(request, pk):
    alert = get_object_or_404(EmergencyAlert, pk=pk)
    alert.status = 'Resolved'
    alert.resolved_at = timezone.now()
    alert.save()
    messages.success(request, f"Emergency Alert #{pk} resolved successfully.")
    return redirect('admin_dashboard')
