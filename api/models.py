from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import ModelForm


class Link(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    title = models.CharField(max_length=200, null=True)
    keywords = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, unique=True)
    notes = models.TextField(null=True, blank=True)
    last_accessed = models.DateField(auto_now_add=True, blank=True)
    views = models.PositiveIntegerField(default=0)  # view count
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flag = models.BooleanField(default=False)

    # will override the `t` query param in the URL for YouTube videos
    start_time_in_sec = models.PositiveIntegerField(default=0)

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


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = '__all__'
