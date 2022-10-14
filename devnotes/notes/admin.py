from django.contrib import admin

from notes.models import Note, Theme


@admin.register(Theme)
class ThemesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Note)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'theme', 'pub_date', 'author',)
    search_fields = ('title',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
    list_editable = ('theme',)
