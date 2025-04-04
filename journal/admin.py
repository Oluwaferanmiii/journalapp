from django.contrib import admin
from .models import JournalEntry


class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'mood')
    list_filter = ('mood', )
    search_fields = ('title', )


admin.site.register(JournalEntry, JournalEntryAdmin)
