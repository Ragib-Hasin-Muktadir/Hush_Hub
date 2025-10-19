from django.contrib import admin

from .models import JournalEntry, MoodEntry, SelfCareTask, DailyRoutine


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'mood', 'created_at']
    list_filter = ['mood']


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at']

@admin.register(SelfCareTask)
class SelfCareTaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_name', 'category', 'is_completed']
    list_filter = ['category', 'is_completed']

@admin.register(DailyRoutine)
class DailyRoutineAdmin(admin.ModelAdmin):
    list_display = ['user', 'routine_date', 'morning_completed']
