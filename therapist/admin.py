from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'patient', 'start_time', 'status')
    list_filter = ('status', 'start_time')
    search_fields = ('therapist__username', 'patient__username', 'reason')
