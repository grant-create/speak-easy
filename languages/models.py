from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=10, unique=True)  # 'es', 'fr', 'ga'
    name = models.CharField(max_length=100)              # 'Spanish'
    flag = models.CharField(max_length=4, blank=True)    # '🇪🇸'

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
