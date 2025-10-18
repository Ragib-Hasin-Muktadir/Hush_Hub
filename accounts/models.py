import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('therapist', 'Therapist'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username

    def get_anonymous_id(self):
        hash_object = hashlib.md5(str(self.id).encode())
        return f"anon_{hash_object.hexdigest()[:6]}"


class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
