from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class Survey(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    thank_you = models.TextField('Thank You Message', blank=True)
    ends_at = models.DateTimeField('Ends At', blank=True, null=True)
    expired_message = models.TextField('Expiration Message', blank=True, help_text="""
        Message to display to users after this survey has expired.
    """)

    # branding
    brand_logo = models.ImageField('Brand Logo', upload_to='media/surveys/logos', blank=True,
                                   help_text="This image should be a square.")
    brand_link = models.URLField('Brand Link', blank=True, help_text="""
        The logo and text will link out to this url,
        e.g. https://www.wnycstudios.org/shows/deathsexmoney.
    """)
    brand_link_label = models.CharField('Link Text', max_length=200, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "%s/%i" % (settings.CLIENT_URL_PREFIX, self.id)

    @property
    def expired(self):
        return self.ends_at <= timezone.now() if self.ends_at else False


class Question(models.Model):
    AUDIO = 'a'
    EMAIL = 'e'
    TEXT = 't'
    TEXT_AREA = 'x'
    TYPE_CHOICES = (
        (TEXT, 'Simple Text'),
        (TEXT_AREA, 'Longer Text'),
        (EMAIL, 'Email'),
        (AUDIO, 'Audio'),
    )

    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    input_type = models.CharField('Question Type',
                                  max_length=1,
                                  choices=TYPE_CHOICES,
                                  default=TEXT)
    label = models.CharField('User-friendly Label', max_length=100)
    short_name = models.SlugField(max_length=100)
    question_text = models.TextField(blank=True, max_length=1000)
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.label


class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(default=timezone.now)
    answers = JSONField()

    def __str__(self):
        return "{0.title} submission".format(self.survey)

    @property
    def audio_answers(self):
        return [x for x in filter(lambda x: x['input_type'] == 'a', self.answers)]

    @property
    def labels(self):
        return [x['label'] for x in self.answers]

    @property
    def responses(self):
        return [x.get('response', '') for x in self.answers]

    @property
    def surveyid(self):
        return self.survey.id

    @property
    def surveytitle(self):
        return self.survey.title
