from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProgress, UserBadge
from community.models import Post
from wellness.models import MoodEntry


@receiver(post_save, sender = Post)
def add_xp_on_community_post(sender, instance, created, **kwargs):
    if created:
        progress, _ = UserProgress.objects.get_or_create(user=instance.user)
        progress.total_xp += 15
        progress.save()

@receiver(post_save, sender = MoodEntry)
def add_xp_on_mood_log(sender, instance, created, **kwargs):

    if created:
        progress, _ = UserProgress.objects.get_or_create(user=instance.user)
        progress.total_xp += 10
        progress.save()
