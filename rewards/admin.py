from django.contrib import admin
from .models import Badge, UserProgress, UserBadge

admin.site.register(Badge)
admin.site.register(UserProgress)
admin.site.register(UserBadge)