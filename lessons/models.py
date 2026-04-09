from django.db import models

from languages.models import Language


class Lesson(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.language.name} — {self.title}'

    class Meta:
        ordering = ['language', 'order']
        unique_together = ('language', 'order')


class Phrase(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='phrases')
    original = models.CharField(max_length=300)    # in target language
    translation = models.CharField(max_length=300) # in English
    example = models.TextField(blank=True)         # usage in a sentence
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.original} — {self.translation}'

    class Meta:
        ordering = ['order']
