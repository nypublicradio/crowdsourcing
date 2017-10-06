from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from django.contrib import admin

from surveys import views


router = DefaultRouter()
router.register(r'survey', views.SurveyViewSet)
router.register(r'submission', views.SubmissionViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
