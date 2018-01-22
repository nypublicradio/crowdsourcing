from adminsortable2.admin import SortableInlineAdminMixin

from django.contrib import admin
from django.utils.html import format_html_join, format_html
from django.urls import reverse

from .models import Survey, Submission, Question


class HasAudioFilter(admin.SimpleListFilter):
    title = 'has audio response'
    parameter_name = 'has_audio'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Yes'),
            ('0', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(answers__contains=[{'input_type': Question.AUDIO}])
        if self.value() == '0':
            return queryset.exclude(answers__contains=[{'input_type': Question.AUDIO}])


class QuestionInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Question
    extra = 2
    fields = ['input_type', 'label', 'short_name', 'question_text', 'required']
    prepopulated_fields = {'short_name': ('label',)}


class SurveyAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Date Information', {'fields': ['starts_at']}),
        ('Content', {'fields': ['summary', 'thank_you']}),
        ('Branding', {'fields': ['brand_logo', ('brand_link', 'brand_link_label')]}),
    ]
    inlines = [QuestionInline]
    list_display = ('title', 'starts_at', 'is_published', 'view_submissions')

    def view_submissions(self, obj):
        return format_html('<a href="{}?survey__id__exact={}">View Submissions</a>',
                           reverse('admin:surveys_submission_changelist'), obj.id)
    view_submissions.short_description = ''


class SubmissionAdmin(admin.ModelAdmin):
    list_filter = ['survey', HasAudioFilter]
    list_display = ('__str__', 'submitted_at', 'audio_files', 'survey_link')
    readonly_fields = ('submitted_at',)

    def audio_files(self, obj):
        # `format_html_join` requires string values to be wrapped in an iterable
        audio_urls = [[answer['response']] for answer in obj.audio_answers]
        return format_html_join(
            '\n',
            '<audio src="{}" controls />',
            audio_urls)
    audio_files.short_description = 'Audio Answers'

    def survey_link(self, obj):
        survey = obj.survey
        return format_html('<a href="{}">{}</a>',
                           reverse('admin:surveys_survey_change', args=(survey.pk,)), survey)


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Submission, SubmissionAdmin)
