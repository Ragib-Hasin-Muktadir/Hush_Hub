from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from wellness.forms import MoodEntryForm, JournalEntryForm
from wellness.models import MoodEntry, JournalEntry


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
