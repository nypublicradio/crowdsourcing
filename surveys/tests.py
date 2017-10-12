from unittest.mock import Mock, patch

from django.urls import reverse

from mixer.backend.django import mixer

from rest_framework import status
from rest_framework.test import APITestCase

from surveys.models import Survey, Question, Submission


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
        self.assertEqual(Submission.objects.filter(survey=self.survey.pk).count(), 1)
        for answer in saved_answers:
            question = list(filter(lambda q: q.pk == answer['question'], self.questions))[0]
            self.assertEqual(expected_keys, sorted(answer.keys()))
            self.assertEqual(answer['input_type'], question.input_type)
            self.assertEqual(answer['label'], question.label)

    @patch('surveys.validators.requests.head')
    def test_validations(self, mock_head):
        url = reverse('submission-list')
        survey = mixer.blend(Survey,)
        email_question = mixer.blend(Question, input_type=Question.EMAIL,
                                     label='email', survey=survey)
        audio_question = mixer.blend(Question, input_type=Question.AUDIO,
                                     label='audio', survey=survey)
        bad_email = 'bademail@'
        bad_audio = 'http://not-a-file.mp3'
        data = {
            'survey': survey.pk,
            'answers': [{
                'question': email_question.pk,
                'response': bad_email,
            }, {
                'question': audio_question.pk,
                'response': bad_audio
            }]
        }
        mock_head.return_value = Mock(status_code=404)
        response = self.client.post(url, data, format='json')
        errors = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_head.assert_called_with(bad_audio)
        self.assertEqual(errors['audio'], ['Audio file {} does not exist.'.format(bad_audio)])
        self.assertEqual(errors['email'], ['Enter a valid email address.'])
