from rest_framework import serializers

from .models import Question, WrongAnswer, SubjectMetrics, ReportMetrics, Subjects, Report


class WrongAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrongAnswer
        fields = "__all__"


class QuestionSerializers(serializers.ModelSerializer):
    wrongs = WrongAnswerSerializer(many=True)
    subject_name = serializers.StringRelatedField(source="subject.name")
    username = serializers.StringRelatedField(source="user.username")

    class Meta:
        model = Question
        fields = "__all__"


class UserAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    userAnswer = serializers.CharField()


class AnswerSubmissionSerializer(serializers.Serializer):
    answers = UserAnswerSerializer(many=True)


class SubjectMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectMetrics
        fields = ['name']


class ReportMetricsSerializer(serializers.ModelSerializer):
    metric = SubjectMetricsSerializer()

    class Meta:
        model = ReportMetrics
        fields = ['metric', 'value']


class SubjectSerializer(serializers.ModelSerializer):
    metrics = serializers.SerializerMethodField()

    class Meta:
        model = Subjects
        fields = ['name', 'metrics']

    def get_metrics(self, obj):
        request = self.context.get('request')
        user_id = request.user.id if request else None

        # Проверяем, есть ли отчеты для данного предмета и пользователя
        reports = Report.objects.filter(user_id=user_id, subject=obj)
        if not reports.exists():
            return []

        # Вызываем метод calculate_average_metrics из модели Report
        metrics_data = reports.first().calculate_average_metrics(user_id=user_id, subject_id=obj.id)

        # Формируем метрики для отображения
        metrics_list = []
        for metric_name, avg_value in metrics_data.items():
            metrics_list.append({
                'metric': metric_name,
                'average_value': avg_value
            })
        return metrics_list
