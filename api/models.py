from django.db import models
from django.contrib.postgres.fields import ArrayField


class Link(models.Manager):
    title = models.CharField(max_length=200, null=True)
    keywords = ArrayField(models.CharField(max_length=200), null=True)
    url = models.URLField(max_length=200, null=True)
    notes = models.TextField(null=True)
    last_accessed = models.DateField(auto_now_add=True, null=True)
    views = models.PositiveIntegerField(default=0)

    class LinkTypes(models.TextChoices):
        PODCAST = 'PODCAST', 'Podcast'
        MUSIC = 'MUSIC', 'Music'
        YOUTUBE = 'YOUTUBE', 'YouTube'

    type = models.CharField(max_length=7, choices=LinkTypes.choices, null=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['last_accessed', ])
        ]


class Quote(models.Model):
    text = models.TextField(null=True)
    author = models.CharField(max_length=200)

    def __str__(self):
        return self.text
