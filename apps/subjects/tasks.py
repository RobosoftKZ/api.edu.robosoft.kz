from celery import shared_task

from apps.subjects.services.generate_questions import OpenAIService
from .models import Question, Subjects, SubjectChoices, WrongAnswer

openai_service = OpenAIService()


@shared_task
def generate_questions_for_user(user_id, subject_id=None):
    if subject_id is None:
        subject = Subjects.objects.filter(slug=SubjectChoices.RUSSIAN).first()
        if subject:
            subject_id = subject.id
    # Логика генерации вопросов для данного пользователя
    # Например, создание нескольких вопросов
    questions = Question.objects.filter(user_id=user_id, subject_id=subject_id)
    if questions.count() < 10:
        # Считаем, сколько вопросов еще нужно сгенерировать
        needed_questions = 10 - questions.count()

        # Вызываем метод генерации вопросов
        generated_questions = openai_service.generate_questions(
            user_id=user_id,
            subject_id=subject_id,
            subject_name=subject.name,  # Передаем название предмета
            metrics={},  # Передаем метрики, если это необходимо
            close_question_count=needed_questions  # Генерируем только недостающие вопросы
        )

        # Сохраняем сгенерированные вопросы в базу данных
        for q_key, q_value in generated_questions.items():
            question = Question(
                user_id=user_id,
                question=q_value['question'],
                subject_id=q_value['topic'],
                answer=q_value['answer_right']  # Сохраняем правильный ответ
            )
            question.save()  # Сохраняем вопрос

            # Сохраняем неправильные ответы
            for i in range(1, 3):  # Предполагаем, что у нас два неправильных ответа
                wrong_answer = WrongAnswer(
                    question=question,
                    answer=q_value[f'answer_false_{i}']
                )
                wrong_answer.save()

