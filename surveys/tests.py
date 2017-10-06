from django.urls import reverse

from mixer.backend.django import mixer

from rest_framework import status
from rest_framework.test import APITestCase

from surveys.models import Survey, Question


class SubmissionTests(APITestCase):
    def setUp(self):
        self.survey = mixer.blend(Survey)
        self.questions = mixer.cycle(5).blend(Question, survey=self.survey)

    def test_submission_with_unrelated_questions(self):
        url = reverse('submission-list')
        other_question = mixer.blend(Question, type=Question.TEXT)
        data = {
            'survey': self.survey.pk,
            'answers': [{
                'question': other_question.pk,
                'response': 'foo',
            }]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_created_submissions(self):
        url = reverse('submission-list')
        data = {
            'survey': self.survey.pk,
            'answers': [{'question': q.pk, 'response': 'foo'} for q in self.questions]
        }
        response = self.client.post(url, data, format='json')

        expected_keys = sorted(['question', 'label', 'input_type', 'response'])
        saved_answers = response.data['answers']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for answer in saved_answers:
            question = list(filter(lambda q: q.pk == answer['question'], self.questions))[0]
            self.assertEqual(expected_keys, sorted(answer.keys()))
            self.assertEqual(answer['input_type'], question.input_type)
            self.assertEqual(answer['label'], question.label)
