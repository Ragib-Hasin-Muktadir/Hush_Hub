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

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wellness_moods'
    )

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

class ProgressReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start = models.DateField()
    week_end = models.DateField()
    total_moods = models.IntegerField(default=0)
    total_journals = models.IntegerField(default=0)
    average_mood_score = models.FloatField(default=0.0)
    insights = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - Week {self.week_start} to {self.week_end}'



class Meditation(models.Model):
    DURATION_CHOICES = [
        (5, '5 minutes'),
        (10, '10 minutes'),
        (15, '15 minutes'),
        (20, '20 minutes'),
        (30, '30 minutes'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(choices=DURATION_CHOICES)
    guide_text = models.TextField()
    category = models.CharField(max_length=50, default='mindfulness')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class MeditationSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(default=timezone.now)
    duration_completed = models.IntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.meditation.title}'


class DailyAffirmation(models.Model):
    affirmation_text = models.TextField()
    category = models.CharField(max_length=50, default='general')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.affirmation_text[:50]


class WellnessTip(models.Model):
    tip_text = models.TextField()
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.tip_text[:50]


class UserAffirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    affirmation = models.ForeignKey(DailyAffirmation, on_delete=models.CASCADE)
    viewed_date = models.DateField(default=timezone.now)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.affirmation}'
