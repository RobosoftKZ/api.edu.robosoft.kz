from django.db import models
from django.contrib.auth.models import User

class RussianLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rus_morphology = models.FloatField()
    rus_stylistics = models.FloatField()
    rus_phonetics = models.FloatField()