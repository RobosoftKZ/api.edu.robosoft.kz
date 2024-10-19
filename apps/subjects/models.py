from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

User = get_user_model()


class SubjectChoices(models.TextChoices):
    MATH = "math", "Математика"
    RUSSIAN = "russian", "Русский язык"
    KAZAKH = "kazakh", "Казахский язык"


class SubjectMetrics(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subjects(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=20, choices=SubjectChoices.choices, unique=True)
    metrics = models.ManyToManyField(SubjectMetrics)
    open_questions_count = models.SmallIntegerField()
    close_questions_count = models.SmallIntegerField()

    def __str__(self):
        return f"{self.name}"


class ReportMetrics(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name="report_metrics")
    metric = models.ForeignKey(SubjectMetrics, on_delete=models.CASCADE, related_name="report_metrics")
    value = models.FloatField()

    def __str__(self):
        return f"{self.subject.name} | {self.metric.name} | {self.value}"


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name="reports")
    metrics = models.ManyToManyField(ReportMetrics)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} | {self.user}"

    def calculate_average_metrics(self, user_id, subject_id):
        # Фильтруем отчеты по пользователю и предмету
        user_reports = Report.objects.filter(user_id=user_id, subject_id=subject_id).prefetch_related('metrics')

        if not user_reports.exists():
            # Если отчётов нет, возвращаем метрики для данного предмета со значением "неизвестно"
            subject_metrics = SubjectMetrics.objects.filter(subjects__id=subject_id).values('name')
            return {metric['name']: '0' for metric in subject_metrics}

        # Собираем метрики, если отчёты есть
        metrics_data = ReportMetrics.objects.filter(
            report__in=user_reports
        ).values('metric__name').annotate(average_value=Avg('value'))

        # Формируем результат для каждого параметра
        result = {}
        for metric in metrics_data:
            metric_name = metric['metric__name']
            avg_value = metric['average_value']
            result[metric_name] = avg_value

        return result


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    topic = models.CharField(max_length=100)
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} | {self.question}"


class WrongAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="wrongs")
    answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question.question} | {self.answer}"
