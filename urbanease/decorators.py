from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access to views based on user roles.
    If the user has a different role, they are redirected to their correct portal's dashboard.
    """
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            # If user has incorrect role, redirect to their proper dashboard
            messages.warning(request, "You do not have permission to access that section.")
            if request.user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif request.user.role == 'SECURITY':
                return redirect('security_dashboard')
            else:
                return redirect('resident_dashboard')
                
        return _wrapped_view
    return decorator
