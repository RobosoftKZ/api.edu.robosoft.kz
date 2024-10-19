from django.urls import path
from . import views

urlpatterns = [
    path("get-questions/", views.GenerateQuestionAPIView.as_view()),
    path("submit-answers/", views.AnswerSubmissionView.as_view()),
    path("get-tables/", views.AnswerSubmissionView.as_view()),
]
