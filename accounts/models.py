from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
