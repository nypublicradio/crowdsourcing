from rest_framework import viewsets, mixins

from .serializers import SurveySerializer, SubmissionSerializer
from .models import Survey, Submission


class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SubmissionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
