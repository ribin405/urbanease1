from django.contrib import admin
from .models import User, ResidentProfile, SecurityProfile, ManagementProfile, MaintenanceRequest, VisitorRequest, EmergencyAlert

admin.site.register(User)
admin.site.register(ResidentProfile)
admin.site.register(SecurityProfile)
admin.site.register(ManagementProfile)
admin.site.register(MaintenanceRequest)
admin.site.register(VisitorRequest)
admin.site.register(EmergencyAlert)
