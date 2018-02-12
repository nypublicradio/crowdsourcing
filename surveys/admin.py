from adminsortable2.admin import SortableInlineAdminMixin

from django.contrib import admin
from django.utils.html import format_html_join, format_html
from django.urls import reverse

from .models import Survey, Submission, Question
from django.contrib import messages
import csv
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.admin.options import IncorrectLookupParameters
import io


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
        (None, {'fields': [('title', 'ends_at'), 'expired_message']}),
        ('Content', {'fields': ['summary', 'thank_you']}),
        ('Branding', {'fields': ['brand_logo', ('brand_link', 'brand_link_label')]}),
    ]
    inlines = [QuestionInline]
    list_display = ('view_id', 'title', 'view_ends_at', 'view_expired', 'view_submissions')

    def view_id(self, obj):
        return obj.id
    view_id.short_description = "Survey ID"
    view_id.empty_value_display = "Null"

    def view_ends_at(self, obj):
        return obj.ends_at
    view_ends_at.short_description = 'Ends At'
    view_ends_at.empty_value_display = 'Does not expire'

    def view_expired(self, obj):
        return obj.expired
    view_expired.admin_order_field = 'ends_at'
    view_expired.boolean = True
    view_expired.short_description = 'Expired?'

    def view_submissions(self, obj):
        return format_html('<a href="{}?survey__id__exact={}">View Submissions</a>',
                           reverse('admin:surveys_submission_changelist'), obj.id)
    view_submissions.short_description = ''


class SubmissionAdmin(admin.ModelAdmin):
    list_filter = ['survey', HasAudioFilter]
    list_display = ('__str__', 'submitted_at', 'audio_files', 'survey_link')
    readonly_fields = ('submitted_at',)
    actions = ['download_csv', 'global_csv_download']

    def changelist_view(self, request, extra_context=None):
        # conditions under which the error for actions on unselected items is thrown
        # override ModelAdmin changelist_view only for this case.
        exp = (request.POST.get('action', False) and request.method == 'POST' and
               'index' in request.POST and '_save' not in request.POST)
        if (exp):
            # override to allow for exporting of ALL records to CSV if no chkbox selected
            selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
            if request.GET:
                qd = request.GET.dict()
            else:
                qd = None
            print(request.GET)
            data = request.POST.copy()
            action = False
            try:
                action = self.get_actions(request)[data['action']][0]
                action_run_on_unselected = action.run_on_unselected
            except (KeyError, AttributeError):
                action_run_on_unselected = False
            if action and len(selected) == 0 and action_run_on_unselected:
                if action.is_global:
                    data['select_across'] = '1'
                    request.POST = data
                    response = self.response_action(request, queryset=self.get_queryset(request))
                    if response:
                        return response
                    else:
                        return HttpResponseRedirect(request.get_full_path())
                else:
                    if qd and qd.get('survey__id__exact', False):
                        # check for a survey filter - required by non-global actions
                        temp = data
                        data['select_across'] = '1'
                        request.POST = data
                        # select all object and use changelist to filter
                        try:
                            cl = self.get_changelist_instance(request)
                        except IncorrectLookupParameters:
                            # Wacky lookup parameters were given, allow modelAdmin (super)
                            # version of changelist_view to handle the error
                            request.POST = temp
                            super(SubmissionAdmin, self).changelist_view(request, extra_context)

                        response = self.response_action(request, queryset=cl.get_queryset(request))
                        if response:
                            return response
                        else:
                            return HttpResponseRedirect(request.get_full_path())

                    else:
                        # if action is not global and no survey filter is set, show error
                        message = 'Use global_csv_download to create a list of all submissions.'
                        self.message_user(request, message, level=messages.WARNING,
                                          extra_tags='', fail_silently=False)
                        # error message
                        return HttpResponseRedirect(request.get_full_path())

        return super(SubmissionAdmin, self).changelist_view(request, extra_context)

    def download_csv(self, request, queryset):
        f = io.StringIO()
        writer = csv.writer(f)
        writer.writerow(["Survey Id", "Survey", "Submitted At"] + queryset[0].labels)
        for s in queryset:
            writer.writerow([s.surveyid, s.surveytitle, s.submitted_at] + s.responses)
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=survey-responses.csv'
        return response
    download_csv.is_global = False
    download_csv.run_on_unselected = True

    def global_csv_download(self, request, queryset):
        f = io.StringIO()
        writer = csv.writer(f)
        queryset = Submission.objects.all()
        ordered = queryset.order_by('survey_id', '-submitted_at')
        x = queryset[0].surveyid
        writer.writerow(["Survey Id", "Survey", "Submitted At"] + queryset[0].labels)
        for s in ordered:
            if s.surveyid != x:
                writer.writerow([])
                writer.writerow(["Survey Id", "Survey", "Submitted At"] + s.labels)
                x = s.surveyid
            writer.writerow([s.surveyid, s.surveytitle, s.submitted_at] + s.responses)
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=global-survey-responses.csv'
        return response
    global_csv_download.is_global = True
    global_csv_download.run_on_unselected = True

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
