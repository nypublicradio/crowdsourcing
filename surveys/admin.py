from adminsortable2.admin import SortableInlineAdminMixin

from django.contrib import admin

from .models import Survey, Submission, Question


class QuestionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Question
    extra = 2
    fields = ['input_type', 'label', 'short_name', 'question_text', 'required']
    prepopulated_fields = {'short_name': ('label',)}


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Date Information', {'fields': ['starts_at'], 'classes': ['collapse']}),
        ('Content', {'fields': ['summary', 'thank_you'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]
    list_display = ('title', 'starts_at', 'is_published')


class SubmissionAdmin(admin.ModelAdmin):
    list_filter = ['survey']


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Submission, SubmissionAdmin)
