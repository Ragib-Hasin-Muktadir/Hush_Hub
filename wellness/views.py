from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from wellness.forms import MoodEntryForm, JournalEntryForm, SelfCareTaskForm
from wellness.models import MoodEntry, JournalEntry, SelfCareTask, DailyRoutine


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

