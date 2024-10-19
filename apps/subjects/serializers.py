from rest_framework import serializers
from .models import RussianLanguage, Math

class RussianLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RussianLanguage
        fields = '__all__'

class MathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Math
        fields = '__all__'