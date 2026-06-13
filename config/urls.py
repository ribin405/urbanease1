from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),  # ADD THIS
    path('', include('urbanease.urls')),
    #path('accounts/', include('accounts.urls')),
    #path('visitors/', include('visitors.urls')),
    #path('maintenance/', include('maintenance.urls')),
]
