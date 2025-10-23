from django.db import models

# Create your models here.

from django.conf import settings

class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon_url = models.URLField(blank=True, null=True)
    xp_reward = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')




class UserProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_xp = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)

    def calculate_level(self):
        if self.total_xp >= 1000:
            self.current_level = 5
        elif self.total_xp >= 500:
            self.current_level = 4
        self.save()

    def __str__(self):
        return f"{self.user.user_ld}: Level {self.current_level} ({self.total_xp} XP)"