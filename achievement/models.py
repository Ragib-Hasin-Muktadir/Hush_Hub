from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.name

