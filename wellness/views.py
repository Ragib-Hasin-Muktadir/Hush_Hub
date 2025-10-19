import json
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from wellness.forms import MoodEntryForm, JournalEntryForm, SelfCareTaskForm
from wellness.models import MoodEntry, JournalEntry, SelfCareTask, DailyRoutine, MeditationSession, UserAffirmation, \
    WellnessTip, DailyAffirmation, Meditation


@login_required
def mood_tracker(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            messages.success(request, 'Mood logged!')
            return redirect('wellness:mood_tracker')
    else:
        form = MoodEntryForm()

    moods = MoodEntry.objects.filter(user=request.user)[:20]
    return render(request, 'wellness/mood_tracker.html', {'form': form, 'moods': moods})


@login_required
def journal(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.user = request.user
            journal.save()
            messages.success(request, 'Journal entry saved!')
            return redirect('wellness:journal')
    else:
        form = JournalEntryForm()

    journals = JournalEntry.objects.filter(user=request.user)
    return render(request, 'wellness/journal.html', {'form': form, 'journals': journals})



@login_required
def selfcare_checklist(request):
    if request.method == 'POST':
        form = SelfCareTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Self-care task added!')
            return redirect('wellness:selfcare_checklist')
    else:
        form = SelfCareTaskForm()

    today = timezone.now().date()
    tasks = SelfCareTask.objects.filter(user=request.user)
    pending_tasks = tasks.filter(is_completed=False)
    completed_tasks = tasks.filter(is_completed=True, completed_date=today)

    context = {
        'form': form,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'wellness/selfcare_checklist.html', context)


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(SelfCareTask, id=task_id, user=request.user)
    task.is_completed = True
    task.completed_date = timezone.now().date()
    task.save()
    messages.success(request, 'Task completed! 🎉')
    return redirect('wellness:selfcare_checklist')



@login_required
def routine_tracker(request):
    today = timezone.now().date()
    routine, created = DailyRoutine.objects.get_or_create(
        user=request.user,
        routine_date=today
    )

    if request.method == 'POST':
        routine.morning_completed = request.POST.get('morning') == 'on'
        routine.afternoon_completed = request.POST.get('afternoon') == 'on'
        routine.evening_completed = request.POST.get('evening') == 'on'
        routine.notes = request.POST.get('notes', '')
        routine.save()
        messages.success(request, 'Routine updated!')
        return redirect('wellness:routine_tracker')

    week_ago = today - timedelta(days=7)
    past_routines = DailyRoutine.objects.filter(
        user=request.user,
        routine_date__gte=week_ago
    ).order_by('-routine_date')

    context = {
        'routine': routine,
        'past_routines': past_routines,
    }
    return render(request, 'wellness/routine_tracker.html', context)



@login_required
def dashboard(request):
    # Get recent entries
    mood_entries = MoodEntry.objects.filter(user=request.user)[:5]
    journal_entries = JournalEntry.objects.filter(user=request.user)[:5]


    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    weekly_moods = MoodEntry.objects.filter(
        user=request.user,
        created_at__date__gte=week_ago
    ).count()

    weekly_journals = JournalEntry.objects.filter(
        user=request.user,
        created_at__date__gte=week_ago
    ).count()


    mood_counts = {}
    recent_moods = MoodEntry.objects.filter(user=request.user)[:30]
    for entry in recent_moods:
        mood_counts[entry.mood] = mood_counts.get(entry.mood, 0) + 1


    insights = []
    if weekly_moods > 5:
        insights.append("Great job! You've been consistently tracking your mood.")
    if weekly_journals > 3:
        insights.append("You're doing well with journaling!")
    if mood_counts.get('happy', 0) > mood_counts.get('sad', 0):
        insights.append("Your mood has been mostly positive lately!")
    elif mood_counts.get('stressed', 0) > 3:
        insights.append("You seem stressed. Try our relaxation exercises.")

    if not insights:
        insights.append("Start tracking your mood to get insights!")

    context = {
        'mood_entries': mood_entries,
        'journal_entries': journal_entries,
        'weekly_moods': weekly_moods,
        'weekly_journals': weekly_journals,
        'mood_counts': json.dumps(mood_counts),
        'insights': insights,
    }
    return render(request, 'wellness/dashboard.html', context)



@login_required
def meditation_library(request):
    meditations = Meditation.objects.all()
    user_sessions = MeditationSession.objects.filter(user=request.user)[:10]

    context = {
        'meditations': meditations,
        'user_sessions': user_sessions,
    }
    return render(request, 'wellness/meditation_library.html', context)


@login_required
def start_meditation(request, meditation_id):
    meditation = get_object_or_404(Meditation, id=meditation_id)

    if request.method == 'POST':
        duration = request.POST.get('duration_completed')
        if duration:
            MeditationSession.objects.create(
                user=request.user,
                meditation=meditation,
                duration_completed=int(duration)
            )
            messages.success(request, 'Meditation completed! 🧘')
            return redirect('wellness:meditation_library')

    return render(request, 'wellness/meditation_detail.html', {'meditation': meditation})



@login_required
def daily_affirmations(request):
    today = timezone.now().date()

    user_affirmation = UserAffirmation.objects.filter(
        user=request.user,
        viewed_date=today
    ).first()

    if not user_affirmation:
        affirmations = list(DailyAffirmation.objects.all())
        if affirmations:
            random_affirmation = random.choice(affirmations)
            user_affirmation = UserAffirmation.objects.create(
                user=request.user,
                affirmation=random_affirmation,
                viewed_date=today
            )

    favorites = UserAffirmation.objects.filter(user=request.user, is_favorite=True)
    wellness_tips = WellnessTip.objects.all()[:5]

    context = {
        'todays_affirmation': user_affirmation.affirmation if user_affirmation else None,
        'favorites': favorites,
        'wellness_tips': wellness_tips,
    }
    return render(request, 'wellness/daily_affirmations.html', context)



@login_required
def progress_charts(request):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)

    mood_timeline = {}
    moods = MoodEntry.objects.filter(
        user=request.user,
        created_at__date__gte=thirty_days_ago
    ).order_by('created_at')

    for mood in moods:
        date_str = mood.created_at.strftime('%Y-%m-%d')
        mood_timeline[date_str] = mood_timeline.get(date_str, 0) + 1

    journal_count = JournalEntry.objects.filter(
        user=request.user,
        created_at__date__gte=thirty_days_ago
    ).count()

    meditation_count = MeditationSession.objects.filter(
        user=request.user,
        completed_at__date__gte=thirty_days_ago
    ).count()

    total_tasks = SelfCareTask.objects.filter(user=request.user).count()
    completed_tasks = SelfCareTask.objects.filter(user=request.user, is_completed=True).count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    context = {
        'mood_timeline': json.dumps(mood_timeline),
        'journal_count': journal_count,
        'meditation_count': meditation_count,
        'completion_rate': round(completion_rate, 1),
    }
    return render(request, 'wellness/progress_charts.html', context)
