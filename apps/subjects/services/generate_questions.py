from apps.subjects.adapters.gpt_client import client as gpt_client
from apps.subjects.adapters.gpt_client import prompt_for_russian_language
from apps.subjects.models import RussianLanguage
import json


class OpenAIService:
    def generate_russian_questions(self, user_id):
        gpt_client.history_chat = [{"content":prompt_for_russian_language, "role":"system" }]

        user_performance = RussianLanguage.objects.filter(user_id=user_id)

        if user_performance:
            morphology = user_performance.rus_morphology
            stylistics = user_performance.rus_stylistics
            phonetics = user_performance.rus_phonetics

        gpt_client.history_chat.append(
            {
                'role': 'user',
                'content': f'Параметр: морфология\nУспешность ученика: {morphology}%\n\nПараметр: стилистика\nУспешность ученика: {stylistics}%\n\nПараметр: фонетика\nУспешность ученика: {phonetics}%'
            }
        )
        completion = gpt_client.chat.completions.create(
            model='gpt-4',
            messages = gpt_client.history_chat,
            response_format={"type": "json_object"},
        )

        gpt_client.history_chat.pop()
        dict_response =dict()
        raw_response = completion.choices[0].message.content
        dict_response=json.loads(raw_response)     # todo: обработчик ошибок try-except 
        
        return dict_response
    
