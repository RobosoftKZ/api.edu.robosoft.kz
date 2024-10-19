import logging

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.subjects.models import (
    Question, Subjects, SubjectChoices, WrongAnswer, Report, ReportMetrics, SubjectMetrics
)
from apps.subjects.serializers import QuestionSerializers, AnswerSubmissionSerializer, SubjectSerializer
# from apps.subjects.services.generate_questions import openAI
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


class AnswerSubmissionView(APIView):
    serializer_class = AnswerSubmissionSerializer

    def post(self, request, *args, **kwargs):
        serializer = AnswerSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            answers = serializer.validated_data['answers']
            correct_answers_count = 0
            open_questions = []
            subject = None
            # Словарь для хранения метрик и их значений
            metrics_data = {}

            for answer_data in answers:
                question_id = answer_data['question_id']
                user_answer = answer_data['userAnswer']
                try:
                    question = Question.objects.get(id=question_id)
                    subject = question.subject

                    # Проверка, является ли вопрос открытым
                    if not WrongAnswer.objects.filter(question=question).exists():
                        open_questions.append({
                            'question': question.question,
                            'user_answer': user_answer
                        })
                    else:
                        # Если ответ правильный
                        metric_name = question.topic
                        if metric_name not in metrics_data:
                            metrics_data[metric_name] = {"total": 0, "right": 0}

                        metrics_data[metric_name]["total"] += 1
                        if user_answer.lower() == question.answer.lower():
                            correct_answers_count += 1
                            metrics_data[metric_name]['right'] += 1
                except Question.DoesNotExist:
                    continue
            # Отправка открытых вопросов на проверку в ChatGPT
            # if open_questions:
            #     gpt_responses = openAI.calculate_anwers(open_questions)
            #     try:
            #         count_of_ones = gpt_responses["marks"].count(1)
            #         correct_answers_count += count_of_ones
            #     except Exception as e:
            #         logging.error(str(e))

            # Создание отчета
            report = Report.objects.create(user=request.user, subject=subject)

            # Сохранение метрик в отчете
            for metric_name, counts in metrics_data.items():
                # Получаем метрику из базы данных
                try:
                    subject_metric = SubjectMetrics.objects.get(name=metric_name)

                    # Извлекаем значения total и right
                    total = counts["total"]
                    right = counts["right"]

                    # Вычисляем значение по формуле right / total * 100, если total не равен 0
                    value = (right / total * 100) if total > 0 else 0

                    report_metric, _created = ReportMetrics.objects.get_or_create(
                        subject=subject,
                        metric=subject_metric,
                        value=value  # Используем новое значение
                    )

                    report.metrics.add(report_metric)  # Связываем метрику с отчетом
                except SubjectMetrics.DoesNotExist:
                    logging.error(f"Метрика {metric_name} не найдена.")
            # report.delete()  # TODO: uncomment this
            return Response({"correct_answers_count": correct_answers_count}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectsViewSet(generics.ListAPIView):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # Добавляем контекст с запросом, чтобы передать user_id
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
