from rest_framework import serializers

from .models import Survey, Question, Submission
from . import validators


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        resource_name = 'question'
        fields = ('id', 'survey', 'input_type', 'label', 'short_name', 'question_text', 'required')


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Survey
        resource_name = 'survey'
        fields = (
            'id',
            'title',
            'summary',
            'thank_you',
            'starts_at',
            'questions',
            'brand_logo',
            'brand_link',
            'brand_link_label',)

    brand_logo = serializers.SerializerMethodField()

    def get_brand_logo(self, obj):
        return {
            'url': obj.brand_logo.url,
            'height': obj.brand_logo.height,
            'width': obj.brand_logo.width,
        } if obj.brand_logo else {}


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        resource_name = 'submission'
        fields = ('id', 'survey', 'submitted_at', 'answers')

    def fill_in_answers(self, data):
        questions = data['survey'].questions.values()
        for answer in data['answers']:
            try:
                question = questions.get(pk=answer['question'])
            except Question.DoesNotExist:
                raise serializers.ValidationError({
                    'question': validators.MISSING_QUESTION
                })
            answer['label'] = question['label']
            answer['input_type'] = question['input_type']
        return data

    def validate(self, data):
        data = self.fill_in_answers(data)
        data = validators.AnswerValidator.answers_belong_to_survey(data)
        data = validators.AnswerValidator.validate_answer_type(data)
        return data
