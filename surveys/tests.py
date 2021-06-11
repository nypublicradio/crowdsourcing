import json
from datetime import timedelta
from django.utils import timezone
from unittest.mock import Mock, patch

import pytest
import csv
import io
from django.urls import reverse

from mixer.backend.django import mixer

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test.client import Client

from surveys.models import Survey, Question, Submission
from surveys.validators import MISSING_QUESTION, EXPIRED_SURVEY


pytestmark = pytest.mark.django_db


class SubmissionTests(APITestCase):
    def setUp(self):
        self.survey = mixer.blend(Survey)
        self.questions = mixer.cycle(5).blend(Question, survey=self.survey)

    def test_submission_with_unrelated_questions(self):
        url = reverse('submission-list')
        other_question = mixer.blend(Question, type=Question.TEXT)
        data = {
            'answers': [{
                'question': other_question.pk,
                'response': 'foo',
            }],
            'survey': self.survey.pk
        }
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['question'][0], MISSING_QUESTION)

    def test_created_submissions(self):
        url = reverse('submission-list')
        data = {
            'answers': [{'question': q.pk, 'response': 'foo'} for q in self.questions],
            'survey': self.survey.pk
        }
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')

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
        survey = mixer.blend(Survey)
        email_question = mixer.blend(Question, input_type=Question.EMAIL,
                                     label='email', survey=survey)
        audio_question = mixer.blend(Question, input_type=Question.AUDIO,
                                     label='audio', survey=survey)
        bad_email = 'bademail@'
        bad_audio = 'http://not-a-file.mp3'
        data = {
            'answers': [{
                'question': email_question.pk,
                'response': bad_email,
            }, {
                'question': audio_question.pk,
                'response': bad_audio
            }],
            'survey': survey.pk
        }
        mock_head.return_value = Mock(status_code=404)
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        errors = response.data
        audio_error = errors['audio'][0]
        email_error = errors['email'][0]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_head.assert_called_with(bad_audio)
        self.assertEqual(audio_error, 'Audio file {} does not exist.'.format(bad_audio))
        self.assertEqual(email_error, 'Enter a valid email address.')

    def test_expired_survey(self):
        url = reverse('submission-list')
        expired_survey = mixer.blend(Survey, ends_at=timezone.now() - timedelta(1))
        questions = mixer.cycle(5).blend(Question, survey=expired_survey)

        data = {
            'answers': [{'question': q.pk, 'response': 'foo'} for q in questions],
            'survey': expired_survey.pk
        }
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['survey'][0], EXPIRED_SURVEY)


class SurveyTests(APITestCase):

    def test_fields(self):
        survey = mixer.blend(Survey)
        url = reverse('survey-detail', args=[survey.pk])
        response = self.client.get(url, content_type='application/json')

        self.assertEqual(sorted(response.data.keys()),
                         sorted(['id', 'title', 'summary', 'thank_you', 'expired_message',
                                 'expired', 'questions', 'brand_logo', 'brand_link',
                                 'brand_link_label']))


class AdminTests(APITestCase):

    def test_csv_action(self):
        self.client = Client()
        user = User.objects.create_superuser(
            username='test',
            password='test',
            email='test'
        )
        self.client.force_login(user)
        url = reverse('admin:surveys_submission_changelist')
        survey = mixer.blend(Survey)
        questions = mixer.cycle(5).blend(Question, survey=survey)
        answers = [{'question': q.pk, 'label': q.label,
                    'input_type': q.input_type, 'response': 'foo'} for q in questions]
        submissions = mixer.cycle(3).blend(Submission, survey=survey, answers=answers)

        data = {'action': 'download_csv', '_selected_action': [s.pk for s in submissions]}
        response = self.client.post(url, data)

        reader = csv.reader(io.StringIO(response.content.decode('utf-8')))
        header = next(reader)
        self.assertEqual(["Survey Id", "Survey", "Submitted At"] + submissions[0].labels, header)
        i = 0
        s = submissions[::-1]
        # reverse submissions as they will be ordered by date created
        for row in reader:
            srow = ["%i" % s[i].survey.id, s[i].survey.title,
                    s[i].submitted_at.isoformat(' ')] + s[i].responses
            self.assertEqual(row, srow)
            i += 1

        # should be three rows of responses
        self.assertEqual(i, 3)

    def test_global_csv_action(self):
        self.client = Client()
        user = User.objects.create_superuser(
            username='test',
            password='test',
            email='test'
        )
        self.client.force_login(user)
        url = reverse('admin:surveys_submission_changelist')
        survey1 = mixer.blend(Survey)
        questions1 = mixer.cycle(5).blend(Question, survey=survey1)
        answers1 = [{'question': q.pk, 'label': q.label,
                    'input_type': q.input_type, 'response': 'foo'} for q in questions1]
        submissions1 = mixer.cycle(3).blend(Submission, survey=survey1, answers=answers1)
        survey2 = mixer.blend(Survey)
        questions2 = mixer.cycle(5).blend(Question, survey=survey2)
        answers2 = [{'question': q.pk, 'label': q.label,
                    'input_type': q.input_type, 'response': 'foo'} for q in questions2]
        submissions2 = mixer.cycle(3).blend(Submission, survey=survey2, answers=answers2)
        submissions = submissions1 + submissions2

        data = {'action': 'global_csv_download', '_selected_action': [s.pk for s in submissions]}
        response = self.client.post(url, data)
        reader = csv.reader(io.StringIO(response.content.decode('utf-8')))
        header = next(reader)

        s1 = submissions1[::-1]
        # reverse submissions as they will be ordered by date created
        self.assertEqual(["Survey Id", "Survey", "Submitted At"] + submissions1[0].labels, header)
        i = 0
        for row in reader:
            if i == 3:
                self.assertEqual([], row)
                # empty row seperating different surveys
                break
            srow = ["%i" % s1[i].survey.id, s1[i].survey.title,
                    s1[i].submitted_at.isoformat(' ')] + s1[i].responses
            self.assertEqual(row, srow)
            i += 1

        header = next(reader)
        s2 = submissions2[::-1]
        # reverse submissions as they will be ordered by date created
        self.assertEqual(["Survey Id", "Survey", "Submitted At"] + submissions2[0].labels, header)
        i = 0
        for row in reader:
            if i == 3:
                break
            srow = ["%i" % s2[i].survey.id, s2[i].survey.title,
                    s2[i].submitted_at.isoformat(' ')] + s2[i].responses
            self.assertEqual(row, srow)
            i += 1
