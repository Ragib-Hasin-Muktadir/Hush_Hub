from .models import UserBadge, Badge, UserProgress
from django.db import IntegrityError
from datetime import timedelta


def award_badge(user, badge_name):
    try:
        badge = Badge.objects.get(name=badge_name)
    except Badge.DoesNotExist:
        print(f"Error: Badge '{badge_name}' does not exist.")
        return

    try:
        UserBadge.objects.create(user=user, badge=badge)

        progress, created = UserProgress.objects.get_or_create(user=user)
        progress.total_xp += badge.xp_reward
        progress.calculate_level()
        print(f"Badge awarded: {badge_name} to {user.user_ld}")
        return True
    except IntegrityError:
        print(f"{user.user_ld} already has badge: {badge_name}")
        return False


def check_daily_streak_badge(user):

    today = timezone.now().date()
    pass