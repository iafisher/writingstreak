from django.contrib import admin

from .models import DailyEntry


class DailyEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('word_count',)


admin.site.register(DailyEntry, DailyEntryAdmin)
