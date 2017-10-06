from rest_framework import serializers

from .models import Survey, Question, Submission


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'survey', 'input_type', 'label', 'short_name', 'question_text', 'required')


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'title', 'summary', 'thank_you', 'starts_at', 'questions')


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'survey', 'submitted_at', 'answers')
