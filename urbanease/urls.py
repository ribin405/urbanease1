from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_resident_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
    
    # Resident Portal
    path('resident/dashboard/', views.resident_dashboard, name='resident_dashboard'),
    path('resident/maintenance/', views.resident_maintenance, name='resident_maintenance'),
    path('resident/visitors/', views.resident_visitors, name='resident_visitors'),
    path('resident/alerts/', views.resident_alerts, name='resident_alerts'),
    path('resident/profile/', views.resident_profile, name='resident_profile'),
    
    # Security Portal
    path('security/dashboard/', views.security_dashboard, name='security_dashboard'),
    path('security/walk-in/', views.security_walk_in, name='security_walk_in'),
    path('security/visitor-action/<int:pk>/<str:action>/', views.security_visitor_action, name='security_visitor_action'),
    path('security/gate-logs/', views.security_gate_logs, name='security_gate_logs'),
    
    # Admin Portal
    path('admin-portal/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-portal/users/', views.admin_users, name='admin_users'),
    path('admin-portal/maintenance/', views.admin_maintenance, name='admin_maintenance'),
    path('admin-portal/visitors/', views.admin_visitors, name='admin_visitors'),
    path('admin-portal/resolve-alert/<int:pk>/', views.admin_resolve_alert, name='admin_resolve_alert'),
]
