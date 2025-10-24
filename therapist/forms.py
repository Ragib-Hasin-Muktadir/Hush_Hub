from django import forms
from .models import SessionNote

class SessionNoteForm(forms.ModelForm):
    class Meta:
        model = SessionNote
        fields = ['notes', 'treatment_plan']
        widgets = {
            'notes': forms.Textarea(attrs={'rows':6}),
            'treatment_plan': forms.Textarea(attrs={'rows':4}),
        }
