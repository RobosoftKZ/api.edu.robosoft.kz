from rest_framework import serializers
from .models import RussianLanguage

class RussianLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RussianLanguage
        fields = '__all__'