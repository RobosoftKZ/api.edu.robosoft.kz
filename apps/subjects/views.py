from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.subjects.models import Question, Subjects, SubjectChoices
from apps.subjects.serializers import QuestionSerializers
from apps.subjects.tasks import generate_questions_for_user


class GenerateQuestionAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializers
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subject_id = self.request.query_params.get('subject_id', None)
        if subject_id is None:
            subject = Subjects.objects.filter(slug=SubjectChoices.MATH).first()
            if subject:
                subject_id = subject.id
        queryset = Question.objects.filter(
            user=self.request.user, subject_id=subject_id
        ).select_related(
            "subject", "user"
        ).prefetch_related(
            "wrongs"
        )[:10]
        generate_questions_for_user.delay(self.request.user.id, subject_id=subject_id)
        return queryset
