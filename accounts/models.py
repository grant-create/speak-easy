import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)

    def update_streak(self):
        today = timezone.now().date()
        if self.last_activity_date == today:
            return  # already counted today
        if self.last_activity_date == today - datetime.timedelta(days=1):
            self.streak += 1
        else:
            self.streak = 1
        self.last_activity_date = today
        self.save(update_fields=['streak', 'last_activity_date'])

    @property
    def active_language(self):
        ul = self.user_languages.filter(is_active=True).select_related('language').first()
        return ul.language if ul else None


class UserLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_languages')
    language = models.ForeignKey('languages.Language', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'language')

    def __str__(self):
        return f'{self.user.username} — {self.language.name}'
