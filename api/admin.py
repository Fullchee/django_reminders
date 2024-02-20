from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from api.models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("last_accessed", "title", "keywords")
    list_filter = ("keywords",)
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
