from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('urbanease.urls')),
    path('accounts/', include('accounts.urls')),
    path('visitors/', include('visitors.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('security/', include('securityportal.urls')),
]
