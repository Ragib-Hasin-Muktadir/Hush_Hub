from django.contrib import admin
from .models import Post, Comment, Message, MoodEntry

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(MoodEntry)



