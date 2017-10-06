from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class Survey(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    thank_you = models.TextField('Thank You Message', blank=True)
    starts_at = models.DateTimeField('Starts At', default=timezone.now)

    def __str__(self):
        return self.title

    def is_published(self):
        return self.starts_at <= timezone.now()


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

    survey = models.ForeignKey(Survey, related_name='questions')
    input_type = models.CharField('Question Type',
                                  max_length=1,
                                  choices=TYPE_CHOICES,
                                  default=TEXT)
    label = models.CharField('User-friendly Label', max_length=100)
    short_name = models.SlugField(max_length=100)
    question_text = models.TextField(blank=True, max_length=100)
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.label


class Submission(models.Model):
    survey = models.ForeignKey(Survey)
    submitted_at = models.DateTimeField(default=timezone.now)
    answers = JSONField()

    def __str__(self):
        return "{0.title} submission on {1}".format(self.survey, self.submitted_at)
