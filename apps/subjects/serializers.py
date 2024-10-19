from rest_framework import serializers

from .models import Question, WrongAnswer


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
