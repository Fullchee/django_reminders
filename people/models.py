from django.db import models
from tinymce.models import HTMLField


class Person(models.Model):
    class Meta:
        verbose_name_plural = "people"

    name = models.TextField()
    mnemonic = HTMLField()
    last_updated = models.DateTimeField(auto_now=True)
    topics = HTMLField()
    notes = HTMLField()
    # LinkedIn URL: get the profile picture?

    def __str__(self):
        return f"Person<{self.name}>"


class Tag(models.Model):
    name = models.TextField()


class Meeting(models.Model):
    name = models.TextField()
    description = models.TextField()
    date = models.DateField()
    reporter = models.ForeignKey(Person, on_delete=models.CASCADE)