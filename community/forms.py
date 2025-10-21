from django import forms
from .models import Post, Comment, Message, MoodEntry


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'is_anonymous']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts...'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'})
        }



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }


class MoodForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood', 'note']
