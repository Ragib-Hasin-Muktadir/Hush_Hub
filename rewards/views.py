from django.shortcuts import render
from .models import UserProgress, UserBadge
from django.contrib.auth.decorators import login_required
from django.db.models import F


@login_required
def leaderboard_view(request):
    top_users = UserProgress.objects.select_related('user').order_by('-total_xp')[:20]

    context = {
        'top_users': top_users,
    }
    return render(request, 'rewards/leaderboard.html', context)


@login_required
def user_progress_view(request):
    user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    try:
        user_progress = UserProgress.objects.get(user=request.user)
    except UserProgress.DoesNotExist:
        user_progress = None

    context = {
        'user_badges': user_badges,
        'progress': user_progress,
    }
    return render(request, 'rewards/user_progress.html', context)