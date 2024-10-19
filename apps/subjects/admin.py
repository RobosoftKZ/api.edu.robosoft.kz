from django.contrib import admin

from .models import ReportMetrics, Report, SubjectMetrics, Subjects, Question


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    ...


@admin.register(ReportMetrics)
class ReportMetricsAdmin(admin.ModelAdmin):
    ...


@admin.register(SubjectMetrics)
class SubjectMetricsAdmin(admin.ModelAdmin):
    ...


@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    ...


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "subject", "question"]

# Register your models here.
