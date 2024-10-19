from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.GPT_API_KEY)


def get_prompts_for_subjects(subject: str, metrics: list, open_question_count=10, close_question_count=0):
    subjects_text = (f"""
    Представь, что ты интегрирован в систему для независимого обучения студентов.

    Каждый ученик изучает {subject}, и имеет несколько параметров успешности: {', '.join(metrics)}.

    """)

    individual_prompt = f"""
    Успеваемость в каждом пункте измеряется в процентах. Ты должен будешь сгенерировать 7 закрытых и 3 открытых вопросов для уровня ученика 7-8 класса. Генерируя открытые вопросы, старайся не придавать очень комплексных ответов, чтобы ученик мог ответить на них.

    Распределяй количество вопросов в зависимости от успеха ученика.
    Например, если в одном пункте 70%, а в других двух 90%, то выдели побольше внимания первому, но не забывай и про остальные. Если у ученика 0% - это означает, что ученик пока не прошел тест и распредели одинаково комплексность и количество вопросов для всех тем. Я буду присылать тебе текст в формате:
    """
    parameters = "".join([f"Параметр: {param}\nУспешность ученика: N%\n\n" for param in metrics])

    answer_format = """
    Отвечай строго в формате json


Если мы говорим о закрытом вопросе, то
{
"question_1": {
"question_type": "open",
"question": "Текст для вопроса",
"topic": "Тема",
"answer": "Правильный ответ",
}
}

Если же об открытом вопросе, то
{
"question_1": {
"question_type": "close",
"question": "Текст для вопроса",
"topic": "Тема",
"answer_right": "Текст правильного ответа",
"answer_false_1": "Текст неверного ответа",
"answer_false_2": "Текст неверного ответа",
}
}
И так десять вопросов.
    И так в общем должен быть десять вопросов. Обрати внимание что в ответе должны быть количество вопросов не меньше 10.
    Отвечать надо сразу здесь, без откладывания
    """
    all_prompt = subjects_text + individual_prompt + parameters + answer_format
    print(all_prompt)
    return all_prompt
