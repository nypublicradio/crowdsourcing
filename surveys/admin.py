from adminsortable2.admin import SortableInlineAdminMixin

from django.contrib import admin
from django.utils.html import format_html_join, format_html
from django.core.urlresolvers import reverse

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
    list_display = ('__str__', 'submitted_at', 'audio_files', 'survey_link')

    def audio_files(self, obj):
        return format_html_join(
            '\n',
            '<audio src="{}" controls />',
            ([file] for file in obj.audio_answers)) if obj.audio_answers else None
    audio_files.short_description = 'Audio Answers'

    def survey_link(self, obj):
        survey = obj.survey
        return format_html('<a href="{}">{}</a>',
                           reverse('admin:surveys_survey_change', args=(survey.pk,)), survey)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Submission, SubmissionAdmin)
