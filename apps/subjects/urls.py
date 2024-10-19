from django.urls import path
from . import views

urlpatterns = [
    path("get-questions/", views.GenerateQuestionAPIView.as_view())
]
