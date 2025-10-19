from django import forms
from .models import MoodEntry, JournalEntry, SelfCareTask


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'note']
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'How are you feeling?'}),
        }

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

class SelfCareTaskForm(forms.ModelForm):
    class Meta:
        model = SelfCareTask
        fields = ['task_name', 'category']
