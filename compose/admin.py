from django.contrib import admin

from .models import DailyEntry


class DailyEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('word_count',)
    date_hierarchy = 'date'
    list_filter = ('user',)


admin.site.register(DailyEntry, DailyEntryAdmin)
