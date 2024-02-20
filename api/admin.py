from django.contrib import admin
from django.db import models
from api.models import Link
from tinymce.widgets import TinyMCE


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("last_accessed", "title", "keywords")
    list_filter = ("keywords",)
    formfield_overrides = {models.TextField: {"widget": TinyMCE()}}
