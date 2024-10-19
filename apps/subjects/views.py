from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.subjects.services.generate_questions import OpenAIService
from rest_framework import viewsets
from .models import RussianLanguage
from .serializers import RussianLanguageSerializer

class RussianViewSet(viewsets.ModelViewSet):
    queryset = RussianLanguage.objects.all()
    serializer_class = RussianLanguageSerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        