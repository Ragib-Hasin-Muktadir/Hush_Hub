from django import forms
from .models import MoodEntry, JournalEntry


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