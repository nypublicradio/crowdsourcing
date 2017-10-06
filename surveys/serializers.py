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

    def validate(self, data):
        allowed_questions = set([q.pk for q in data['survey'].questions.all()])
        answered_questions = set([a['question'] for a in data['answers']])
        if not allowed_questions.issuperset(answered_questions):
            # only accept answers for the given survey
            raise serializers.ValidationError(
                'Submission includes answers to questions that do not belong to this survey.'
            )
        return data

    def create(self, validated_data):
        questions = validated_data['survey'].questions.values()
        # add metadata from the question to answers in the JSON blob
        for answer in validated_data['answers']:
            question = questions.get(pk=answer['question'])
            answer['label'] = question['label']
            answer['input_type'] = question['input_type']
        return super().create(validated_data)
