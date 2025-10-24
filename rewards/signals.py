from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProgress, UserBadge, Badge
from community.models import Post
from wellness.models import MoodEntry

def check_and_award_badges(user_progress):
    current_xp = user_progress.total_xp

    eligible_badges = Badge.objects.filter(xp_reward__lte=current_xp).all()

    for badge in eligible_badges:

        has_badge = UserBadge.objects.filter(
            user=user_progress.user,
            badge=badge
        ).exists()

        if not has_badge:

            UserBadge.objects.create(
                user=user_progress.user,
                badge=badge
            )
            print(f"DEBUG: Awarded badge: {badge.name} to {user_progress.user.username}")


@receiver(post_save, sender=Post)
def add_xp_on_community_post(sender, instance, created, **kwargs):
    if created:
        progress, _ = UserProgress.objects.get_or_create(user=instance.user)
        progress.total_xp += 15
        progress.save()

        check_and_award_badges(progress)


@receiver(post_save, sender=MoodEntry)
def add_xp_on_mood_log(sender, instance, created, **kwargs):
    if created:
        progress, _ = UserProgress.objects.get_or_create(user=instance.user)
        progress.total_xp += 10
        progress.save()

        check_and_award_badges(progress)