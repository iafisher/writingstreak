from django.contrib import admin

from .models import DailyWriting


class DailyWritingAdmin(admin.ModelAdmin):
    readonly_fields = ('word_count',)

admin.site.register(DailyWriting, DailyWritingAdmin)
