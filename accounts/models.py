from django.contrib.auth.models import AbstractUser
from django.db import models


LANGUAGE_CHOICES = [
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('ja', 'Japanese'),
    ('zh', 'Mandarin Chinese'),
    ('ko', 'Korean'),
    ('ar', 'Arabic'),
    ('ru', 'Russian'),
]


class User(AbstractUser):
    target_language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        blank=True,
    )
