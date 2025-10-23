from django.db import models
from django.conf import settings

# Use the custom user model from settings
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
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='upcoming'
    )

    def __str__(self):
        # This makes the admin and console output more readable
        return f"Appointment: {self.patient} with {self.therapist} ({self.status})"
