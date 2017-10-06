from rest_framework import serializers

from .models import Survey, Question, Submission


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'title', 'slug', 'summary', 'thank_you', 'starts_at', 'questions')


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'survey', 'submitted_at', 'answers')