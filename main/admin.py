from django.contrib import admin

# Register your models here.
from .models import Phrase, Lesson, UserProfile, Prompt, Response, Story

class PhraseInLine(admin.StackedInline):
    model = Phrase
    extra = 10

class LessonAdmin(admin.ModelAdmin):
    inlines = [PhraseInLine]



admin.site.register(Phrase)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(UserProfile)
admin.site.register(Prompt)
admin.site.register(Response)
admin.site.register(Story)