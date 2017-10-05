from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class Survey(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    thank_you = models.TextField('Thank You Message', blank=True)
    starts_at = models.DateTimeField('Starts At')

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions')
    question_text = models.TextField()
    label = models.CharField(max_length=100)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text


class Submission(models.Model):
    survey = models.ForeignKey(Survey)
    submitted_at = models.DateTimeField(default=timezone.now)
    answers = JSONField()

    def __str__(self):
        return "{0.title} submission on {1}".format(self.survey, self.submitted_at)
