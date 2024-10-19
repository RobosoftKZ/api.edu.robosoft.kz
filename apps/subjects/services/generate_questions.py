import json

from apps.subjects.adapters.gpt_client import client as gpt_client, text_open_question_answers
from apps.subjects.adapters.gpt_client import (
    get_prompt_for_getting_answer_quality
)


class OpenAIService:
    def generate_questions(self, user_id, subject_id,
                           subject_name, metrics, open_question_count=3, close_question_count=7):
        # gpt_client.history_chat = [
        #     {
        #         "content": get_prompts_for_subjects(subject_name, metrics, open_question_count=open_question_count,
        #                                             close_question_count=close_question_count),
        #         "role": "system"
        #     }
        # ]
        #
        # report = Report()
        # average_metrics = report.calculate_average_metrics(user_id, subject_id)
        # metrics_content = ""
        # for metric_name, avg_value in average_metrics.items():
        #     metrics_content += f'Параметр: {metric_name}\nУспешность ученика: {avg_value}%\n\n'
        # gpt_client.history_chat.append(
        #     {
        #         'role': 'user',
        #         'content': metrics_content
        #     }
        # )
        # completion = gpt_client.chat.completions.create(
        #     model='gpt-4o-mini',
        #     messages=gpt_client.history_chat,
        #     response_format={"type": "json_object"}
        # )
        #
        # gpt_client.history_chat.pop()
        #
        # raw_response = completion.choices[0].message.content
        # dict_response = json.loads(raw_response)  # todo: обработчик ошибок try-except
        dict_response = {'question_1': {'question_type': 'close',
                                        'question': 'Какой из перечисленных терминов относится к морфологии?',
                                        'topic': 'Морфология',
                                        'answer_right': 'Корень',
                                        'answer_false_1': 'Синоним',
                                        'answer_false_2': 'Интонация'},
                         'question_2': {'question_type': 'close',
                                        'question': 'Что изучает стилистика?',
                                        'topic': 'Стилистика',
                                        'answer_right': 'Стиль речи',
                                        'answer_false_1': 'Фонетику звуков',
                                        'answer_false_2': 'Синтаксис предложений'},
                         'question_3': {'question_type': 'close',
                                        'question': 'Какое из этих слов является существительным?',
                                        'topic': 'Фонетика',
                                        'answer_right': 'Стол',
                                        'answer_false_1': 'Бегущий',
                                        'answer_false_2': 'Быстро'},
                         'question_4': {'question_type': 'close',
                                        'question': "Какое из этих слов является антонимом к слову 'большой'?",
                                        'topic': 'Стилистика',
                                        'answer_right': 'Маленький',
                                        'answer_false_1': 'Громкий',
                                        'answer_false_2': 'Светлый'},
                         'question_5': {'question_type': 'close',
                                        'question': 'Что из перечисленного является частью речи?',
                                        'topic': 'Морфология',
                                        'answer_right': 'Глагол',
                                        'answer_false_1': 'Рифма',
                                        'answer_false_2': 'Диалект'},
                         'question_6': {'question_type': 'close',
                                        'question': 'Какой из этих терминов не относится к фонетике?',
                                        'topic': 'Фонетика',
                                        'answer_right': 'Синтаксис',
                                        'answer_false_1': 'Артикуляция',
                                        'answer_false_2': 'Интонация'},
                         'question_7': {'question_type': 'close',
                                        'question': 'Какой из предложенных вариантов является примером метафоры?',
                                        'topic': 'Стилистика',
                                        'answer_right': 'Он – лев в бою.',
                                        'answer_false_1': 'Он бежит быстро.',
                                        'answer_false_2': 'Он был синий.'},
                         'question_8': {'question_type': 'close',
                                        'question': 'Что такое морфема?',
                                        'topic': 'Морфология',
                                        'answer_right': 'Наименьшая значимая единица языка.',
                                        'answer_false_1': 'Большая группа слов.',
                                        'answer_false_2': 'Способность звучания.'},
                         'question_9': {'question_type': 'close',
                                        'question': 'Какое из этих слов имеет ударение на первый слог?',
                                        'topic': 'Фонетика',
                                        'answer_right': 'Груша',
                                        'answer_false_1': 'Капля',
                                        'answer_false_2': 'Дерево'},
                         'question_10': {'question_type': 'open',
                                         'question': 'Что такое синоним? Приведите пример.',
                                         'topic': 'Стилистика',
                                         'answer': ''}}

        return dict_response

    def calculate_anwers(self, quest_answer_dicts):
        gpt_client.history_chat = [
            {
                "content": get_prompt_for_getting_answer_quality(),
                "role": "system"
            }
        ]
        gpt_client.history_chat.append(
            {
                'role': 'user',
                'content': text_open_question_answers(quest_answer_dicts)
            }
        )
        completion = gpt_client.chat.completions.create(
            model='gpt-4o-mini',
            messages=gpt_client.history_chat,
            response_format={"type": "json_object"}
        )

        gpt_client.history_chat.pop()

        raw_response = completion.choices[0].message.content
        dict_response = json.loads(raw_response)  # todo: обработчик ошибок try-except
        return dict_response


openAI = OpenAIService()
