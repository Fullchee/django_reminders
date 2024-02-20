from django.contrib import admin

from .models import Link, Quote


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "keywords")
    list_filter = ("keywords",)


admin.site.register(Quote)
