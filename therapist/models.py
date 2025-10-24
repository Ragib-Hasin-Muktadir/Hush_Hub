from django.db import models
from django.conf import settings

# use the project's custom user model
User = settings.AUTH_USER_MODEL


class Appointment(models.Model):
    STATUS = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('cancelled', 'Cancelled'),
        ('finished', 'Finished'),
    )

    therapist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_therapist'
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_patient'
    )
    reason = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Appointment: {self.patient} with {self.therapist} ({self.status})"


class SessionNote(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='session_note'
    )
    therapist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='session_notes'
    )
    notes = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.appointment}"
