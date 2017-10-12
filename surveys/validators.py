import requests

from django.core.validators import validate_email
from rest_framework.serializers import ValidationError

from .models import Question


def remote_file_lookup(url):
    try:
        r = requests.head(url)
    except requests.exceptions.RequestException as e:
        raise ValidationError('Url failure: {}'.format(e))
    if r.status_code != requests.codes.ok:
        raise ValidationError('Url {} file does not exist'.format(url))


class AnswerValidator:
    VALIDATORS = {
        Question.EMAIL: [validate_email],
        Question.AUDIO: [remote_file_lookup],
    }

    @staticmethod
    def answers_belong_to_survey(data):
        survey_questions = set([q.pk for q in data['survey'].questions.all()])
        answered_questions = set([a['question'] for a in data['answers']])
        if not survey_questions.issuperset(answered_questions):
            # only accept answers for the given survey
            message = 'Submission includes answers to questions that do not belong to this survey.'
            raise ValidationError({
                'answers': message
            })
        return data

    @classmethod
    def validate_answer_type(cls, data):
        for answer in data['answers']:
            validators = cls.VALIDATORS.get(answer['input_type'], [])
            for validator in validators:
                validator(answer['response'])
        return data
