from django.contrib import admin
from django.db import models
from people.models import Person
from tinymce.widgets import TinyMCE


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
   formfield_overrides = {
   models.TextField: {'widget': TinyMCE()}
   }
