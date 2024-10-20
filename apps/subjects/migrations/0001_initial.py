# Generated by Django 5.0.9 on 2024-10-19 12:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def add_subjects_and_metrics(apps, schema_editor):
    # Получаем модели
    Subjects = apps.get_model('subjects', 'Subjects')
    SubjectMetrics = apps.get_model('subjects', 'SubjectMetrics')

    # Создаем метрики для Русского языка
    rus_morphology = SubjectMetrics.objects.create(name='Морфология')
    rus_stylistics = SubjectMetrics.objects.create(name='Стилистика')
    rus_phonetics = SubjectMetrics.objects.create(name='Фонетика')

    # Создаем метрики для Математики
    math_arithmetic = SubjectMetrics.objects.create(name='Арифметика')
    math_statistics = SubjectMetrics.objects.create(name='Статистика')
    math_percentages = SubjectMetrics.objects.create(name='Проценты')

    # Создаем предметы и связываем их с метриками
    russian_language = Subjects.objects.create(name='Русский язык', slug='russian', open_questions_count=10,
                                               close_questions_count=5)
    russian_language.metrics.set([rus_morphology, rus_stylistics, rus_phonetics])

    math = Subjects.objects.create(name='Математика', slug='math', open_questions_count=10, close_questions_count=5)
    math.metrics.set([math_arithmetic, math_statistics, math_percentages])

    kazakh_language = Subjects.objects.create(name='Қазақ тілі', slug='kazakh', open_questions_count=10,
                                              close_questions_count=5)
    kazakh_language.metrics.set([rus_morphology, rus_stylistics, rus_phonetics])


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(
                    choices=[('math', 'Математика'), ('russian', 'Русский язык'), ('kazakh', 'Казахский язык')],
                    max_length=20, unique=True)),
                ('open_questions_count', models.SmallIntegerField()),
                ('close_questions_count', models.SmallIntegerField()),
                ('metrics', models.ManyToManyField(to='subjects.subjectmetrics')),
            ],
        ),
        migrations.CreateModel(
            name='ReportMetrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_metrics',
                                             to='subjects.subjectmetrics')),
                ('subject',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_metrics',
                                   to='subjects.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports',
                                           to=settings.AUTH_USER_MODEL)),
                ('metrics', models.ManyToManyField(to='subjects.reportmetrics')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports',
                                              to='subjects.subjects')),
            ],
        ),
        migrations.RunPython(add_subjects_and_metrics, reverse_code=migrations.RunPython.noop),
    ]
