from django.contrib import admin

from .models import DailyWriting, Streak, WordCountGoal


class DailyWritingAdmin(admin.ModelAdmin):
    readonly_fields = ('word_count',)


admin.site.register(DailyWriting, DailyWritingAdmin)
admin.site.register(Streak)
admin.site.register(WordCountGoal)
