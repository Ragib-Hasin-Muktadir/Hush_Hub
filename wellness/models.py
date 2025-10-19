from django.db import models
from django.utils import timezone
from accounts.models import User



class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('anxious', 'Anxious'),
        ('calm', 'Calm'),
        ('stressed', 'Stressed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.mood}'


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class SelfCareTask(models.Model):
    CATEGORY_CHOICES = [
        ('physical', 'Physical Health'),
        ('mental', 'Mental Health'),
        ('social', 'Social Connection'),
        ('spiritual', 'Spiritual Growth'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.task_name}'


class DailyRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine_date = models.DateField(default=timezone.now)
    morning_completed = models.BooleanField(default=False)
    afternoon_completed = models.BooleanField(default=False)
    evening_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'routine_date']

    def __str__(self):
        return f'{self.user.username} - {self.routine_date}'

