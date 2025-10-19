from django.contrib import admin

from .models import JournalEntry, MoodEntry, SelfCareTask, DailyRoutine, Meditation, MeditationSession, \
    DailyAffirmation, WellnessTip, UserAffirmation, ProgressReport


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

@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'category']

@admin.register(MeditationSession)
class MeditationSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'meditation', 'completed_at']

@admin.register(DailyAffirmation)
class DailyAffirmationAdmin(admin.ModelAdmin):
    list_display = ['affirmation_text', 'category']

@admin.register(WellnessTip)
class WellnessTipAdmin(admin.ModelAdmin):
    list_display = ['tip_text', 'category']

@admin.register(UserAffirmation)
class UserAffirmationAdmin(admin.ModelAdmin):
    list_display = ['user', 'affirmation', 'is_favorite']

@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'week_start', 'total_moods']
