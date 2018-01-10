from rest_framework import serializers

from .models import Survey, Question, Submission
from .validators import AnswerValidator


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
        fields = ('id', 'title', 'summary', 'thank_you', 'starts_at', 'questions')


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
                    'question': 'The specified question does not exist.'
                })
            answer['label'] = question['label']
            answer['input_type'] = question['input_type']
        return data

    def validate(self, data):
        data = self.fill_in_answers(data)
        data = AnswerValidator.answers_belong_to_survey(data)
        data = AnswerValidator.validate_answer_type(data)
        return data
