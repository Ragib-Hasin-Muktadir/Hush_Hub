from django.contrib import admin

from wellness.models import JournalEntry, MoodEntry


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood', 'created_at']
    list_filter = ['mood']


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at']
